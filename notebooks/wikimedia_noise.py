"""Wikimedia top-per-country noise filtering.

Distinguishes real articles from structural pages (main pages, search, portals)
using each project's own siteinfo (mainpage title + real namespace names),
rather than a hand-maintained denylist — namespace names are localized per
language (e.g. "Wikipédia:" vs "Wikipedia:"), so guessing doesn't scale.

See data-sources/wikimedia/findings.md for what this catches and misses.
"""

from functools import lru_cache

import requests

USER_AGENT = "zitygeist-exploration (personal project)"


@lru_cache(maxsize=None)
def fetch_siteinfo(project: str) -> dict:
    """project like 'en.wikipedia', 'zu.wikibooks' -> {'mainpage', 'namespaces'}."""
    r = requests.get(
        f"https://{project}.org/w/api.php",
        params={"action": "query", "meta": "siteinfo", "siprop": "general|namespaces", "format": "json"},
        headers={"User-Agent": USER_AGENT},
    )
    d = r.json()["query"]
    return {
        "mainpage": d["general"]["mainpage"].replace(" ", "_"),
        "namespaces": {ns["*"].replace(" ", "_") for ns in d["namespaces"].values() if ns["*"]},
    }


def is_noise(article: str, project: str) -> bool:
    info = fetch_siteinfo(project)
    if article == info["mainpage"]:
        return True
    if ":" in article and article.split(":", 1)[0] in info["namespaces"]:
        return True
    return False
