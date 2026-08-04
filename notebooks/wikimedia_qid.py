"""Wikidata Q-id resolution for Wikipedia titles.

Resolves a project + title to its Wikidata Q-id via that project's own API
(action=query, prop=pageprops, wikibase_item) — same per-project pattern as
wikimedia_noise.fetch_siteinfo. Q-ids are the project's cross-source join key:
the same real-world entity should resolve to the same Q-id whichever language
edition (or, eventually, GDELT/TMDB) you found it in.

See data-sources/wikimedia/findings.md.
"""

import json
import time
from pathlib import Path

from wikimedia_http import get

# MediaWiki's action=query allows up to 50 titles per request (anonymous) —
# batching matters here: this endpoint rate-limits much tighter than the
# pageviews REST API (we've hit 429s on it repeatedly this session), and a
# country's kept list can easily be 100-1000 titles.
_MAX_TITLES_PER_REQUEST = 50

# A title's Q-id essentially never changes, and the same titles recur heavily
# across days/countries (65-84% day-to-day overlap), so cache to disk like
# wikimedia_noise's siteinfo cache — avoids re-resolving the same titles across
# kernel restarts or repeated pipeline runs.
_CACHE_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
    / "wikimedia"
    / "qid_cache.json"
)


def _cache_key(project: str, title: str) -> str:
    return f"{project}::{title}"


def _load_cache() -> dict[str, str | None]:
    if not _CACHE_PATH.exists():
        return {}
    with open(_CACHE_PATH) as f:
        return json.load(f)


def _save_cache(cache: dict[str, str | None]) -> None:
    _CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(_CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)


_qid_cache = _load_cache()


def resolve_qids(project: str, titles: list[str]) -> dict[str, str | None]:
    """Resolve many titles on one project to Q-ids in as few requests as possible.

    Returns {title: qid_or_None}, keyed by the *original* title passed in even
    though MediaWiki may normalize or redirect it internally. Missing pages or
    pages with no linked Wikidata item map to None. Cached to disk, so already
    -seen titles cost nothing.
    """
    results: dict[str, str | None] = {}
    to_fetch = []
    for title in titles:
        key = _cache_key(project, title)
        if key in _qid_cache:
            results[title] = _qid_cache[key]
        else:
            to_fetch.append(title)

    for i in range(0, len(to_fetch), _MAX_TITLES_PER_REQUEST):
        batch = to_fetch[i : i + _MAX_TITLES_PER_REQUEST]
        resolved = _resolve_batch(project, batch)
        results.update(resolved)
        for title, qid in resolved.items():
            _qid_cache[_cache_key(project, title)] = qid
    if to_fetch:
        _save_cache(_qid_cache)

    return results


def resolve_qid(project: str, title: str) -> str | None:
    return resolve_qids(project, [title])[title]


def _resolve_batch(project: str, titles: list[str]) -> dict[str, str | None]:
    for attempt in range(4):
        r = get(
            f"https://{project}.org/w/api.php",
            params={
                "action": "query",
                "prop": "pageprops",
                "ppprop": "wikibase_item",
                "titles": "|".join(titles),
                "redirects": 1,
                "format": "json",
            },
        )
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", 2**attempt)))
            continue
        r.raise_for_status()
        break
    else:
        raise RuntimeError(
            f"Q-id resolution for {project} still rate-limited after retries"
        )

    q = r.json()["query"]

    # chain original title -> normalized title -> redirect target, so we can
    # key the final result by what was actually asked for
    resolved_title = {t: t for t in titles}
    for n in q.get("normalized", []):
        resolved_title = {
            t: (n["to"] if v == n["from"] else v) for t, v in resolved_title.items()
        }
    for rd in q.get("redirects", []):
        resolved_title = {
            t: (rd["to"] if v == rd["from"] else v) for t, v in resolved_title.items()
        }

    qid_by_final_title: dict[str, str | None] = {}
    for page in q["pages"].values():
        if "missing" in page:
            continue
        qid_by_final_title[page["title"]] = page.get("pageprops", {}).get(
            "wikibase_item"
        )

    return {t: qid_by_final_title.get(final) for t, final in resolved_title.items()}
