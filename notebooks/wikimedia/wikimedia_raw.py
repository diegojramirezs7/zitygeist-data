"""Loading Wikimedia's persisted top-per-country backfill from disk.

scripts/fetch_wikimedia_top_per_country.py writes one untouched raw response
per country/day to data/raw/wikimedia/top_per_country/<country>/<date>.json.
This module reads that back in — no network calls, no cleaning.
"""

import json
from datetime import date, timedelta
from pathlib import Path

_ROOT = (
    Path(__file__).resolve().parent.parent.parent
    / "data"
    / "raw"
    / "wikimedia"
    / "top_per_country"
)


def date_range(start: date, end: date) -> list[date]:
    """Inclusive of both endpoints."""
    n = (end - start).days
    return [start + timedelta(days=i) for i in range(n + 1)]


def load_day(country: str, day: date) -> list[dict] | None:
    """Articles for one country/day, or None if that file was never fetched."""
    path = _ROOT / country / f"{day.isoformat()}.json"
    if not path.exists():
        return None
    with open(path) as f:
        payload = json.load(f)
    return payload["items"][0]["articles"]
