"""Assembles the Phase 2.1 deliverable: cleaned, Q-id-resolved top lists.

Combines three already-proven pieces — wikimedia_raw (load persisted backfill),
wikimedia_noise (drop structural junk), wikimedia_qid (title -> Wikidata Q-id)
— into one tidy table, one row per kept article per country/day.

Q-id resolution is deduped across the whole requested grid before any lookup
happens: the same titles recur heavily day-to-day and across countries, so
resolving per-row would waste requests on titles we've already resolved.
"""

from dataclasses import dataclass
from datetime import date

import pandas as pd

from wikimedia_noise import is_noise
from wikimedia_qid import resolve_qids
from wikimedia_raw import load_day


@dataclass
class TopListsResult:
    table: pd.DataFrame
    missing_days: list[tuple[str, date]]
    unresolvable_projects: set[str]


def build_top_lists(countries: list[str], days: list[date]) -> TopListsResult:
    kept_rows = []
    missing_days: list[tuple[str, date]] = []
    unresolvable_projects: set[str] = set()

    for country in countries:
        for day in days:
            articles = load_day(country, day)
            if articles is None:
                missing_days.append((country, day))
                continue
            for a in articles:
                # a handful of "project" values (e.g. api.wikimedia) are API
                # gateway domains, not real wikis — no siteinfo to query, so
                # there's no way to classify them as content vs. noise. Drop
                # them rather than let one bad project crash the whole build.
                try:
                    noise = is_noise(a["article"], a["project"])
                except Exception:
                    unresolvable_projects.add(a["project"])
                    continue
                if noise:
                    continue
                kept_rows.append(
                    {
                        "country": country,
                        "date": day,
                        "rank": a["rank"],
                        "project": a["project"],
                        "article": a["article"],
                        "views_ceil": a["views_ceil"],
                    }
                )

    titles_by_project: dict[str, set[str]] = {}
    for row in kept_rows:
        titles_by_project.setdefault(row["project"], set()).add(row["article"])

    qid_by_project_title: dict[tuple[str, str], str | None] = {}
    for project, titles in titles_by_project.items():
        resolved = resolve_qids(project, sorted(titles))
        for title, qid in resolved.items():
            qid_by_project_title[(project, title)] = qid

    for row in kept_rows:
        row["qid"] = qid_by_project_title.get((row["project"], row["article"]))

    table = pd.DataFrame(
        kept_rows,
        columns=["country", "date", "rank", "project", "article", "views_ceil", "qid"],
    )
    table = table.sort_values(["country", "date", "rank"]).reset_index(drop=True)

    return TopListsResult(
        table=table, missing_days=missing_days, unresolvable_projects=unresolvable_projects
    )
