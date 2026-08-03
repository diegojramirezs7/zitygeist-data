"""Wikimedia top-per-country noise filtering.

Distinguishes real articles from structural pages (main pages, search, portals)
using each project's own siteinfo (mainpage title + real namespace names),
rather than a hand-maintained denylist — namespace names are localized per
language (e.g. "Wikipédia:" vs "Wikipedia:"), so guessing doesn't scale.

See data-sources/wikimedia/findings.md for what this catches and misses.
"""

import json
import time
from pathlib import Path

import requests

USER_AGENT = "zitygeist-exploration (personal project)"

# Namespace names essentially never change, so this is cached to disk, not just
# in-memory — a fresh kernel/session shouldn't have to re-hit action=query (which
# rate-limits much tighter than the pageviews REST API) for projects we've
# already seen before. A single country's top list can touch 60+ distinct
# projects, so a cold cache means dozens of first-time network calls.
_CACHE_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "wikimedia" / "siteinfo_cache.json"


def _load_cache() -> dict:
    if not _CACHE_PATH.exists():
        return {}
    with open(_CACHE_PATH) as f:
        raw = json.load(f)
    return {p: {"mainpage": v["mainpage"], "namespaces": set(v["namespaces"])} for p, v in raw.items()}


def _save_cache(cache: dict) -> None:
    _CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    serializable = {
        p: {"mainpage": v["mainpage"], "namespaces": sorted(v["namespaces"])} for p, v in cache.items()
    }
    with open(_CACHE_PATH, "w") as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)


_siteinfo_cache = _load_cache()


def fetch_siteinfo(project: str) -> dict:
    """project like 'en.wikipedia', 'zu.wikibooks' -> {'mainpage', 'namespaces'}."""
    if project in _siteinfo_cache:
        return _siteinfo_cache[project]

    for attempt in range(4):
        r = requests.get(
            f"https://{project}.org/w/api.php",
            params={
                "action": "query",
                "meta": "siteinfo",
                "siprop": "general|namespaces",
                "format": "json",
            },
            headers={"User-Agent": USER_AGENT},
        )
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", 2**attempt)))
            continue
        r.raise_for_status()
        d = r.json()["query"]
        info = {
            "mainpage": d["general"]["mainpage"].replace(" ", "_"),
            "namespaces": {
                ns["*"].replace(" ", "_") for ns in d["namespaces"].values() if ns["*"]
            },
        }
        _siteinfo_cache[project] = info
        _save_cache(_siteinfo_cache)
        return info
    raise RuntimeError(f"siteinfo for {project} still rate-limited after retries")


def is_noise(article: str, project: str) -> bool:
    info = fetch_siteinfo(project)
    if article == info["mainpage"]:
        return True
    if ":" in article and article.split(":", 1)[0] in info["namespaces"]:
        return True
    return False
