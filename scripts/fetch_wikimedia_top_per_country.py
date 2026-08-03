"""Fetch Wikimedia's daily top-per-country pageview rankings.

Endpoint: https://wikimedia.org/api/rest_v1/metrics/pageviews/top-per-country/
{country}/all-access/{YYYY}/{MM}/{DD} — the ranked list (up to ~1000) of
articles a country's readers viewed most that day. No API key needed.

Wikimedia's Robot Policy (https://wikitech.wikimedia.org/wiki/Robot_policy)
and User-Agent Policy (https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy)
require a compliant, identifiable User-Agent and cap unauthenticated REST API
traffic at <5 req/s — a vague/generic User-Agent can be silently blocked,
which earlier looked exactly like broken data availability until traced back
to this. Both are handled here.

Usage:
  python scripts/fetch_wikimedia_top_per_country.py                    # yesterday (UTC), default countries
  python scripts/fetch_wikimedia_top_per_country.py --date 2026-08-01
  python scripts/fetch_wikimedia_top_per_country.py --backfill 365     # date and N-1 days before it
  python scripts/fetch_wikimedia_top_per_country.py --countries CA US MX

Idempotent: existing files are skipped, so re-running a backfill only fetches
what's missing. Raw responses are stored untouched (no noise filtering, no
Q-id resolution) — those are transforms applied later, not part of capture.
A day that isn't loaded yet (429, or 404 with "not loaded yet") is retried
with backoff, not immediately treated as permanently missing.
"""

import argparse
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

USER_AGENT = (
    f"zitygeist-exploration/0.1 (diegojramirezs7@gmail.com) "
    f"Python-urllib/{sys.version_info.major}.{sys.version_info.minor}"
)
BASE_URL = "https://wikimedia.org/api/rest_v1/metrics/pageviews/top-per-country"
DEFAULT_COUNTRIES = ["CA", "US", "MX"]
OUT_ROOT = Path(__file__).resolve().parent.parent / "data" / "raw" / "wikimedia" / "top_per_country"
RETRIES = 4
MIN_INTERVAL = 0.5  # seconds between requests -> max 2 req/s, well under the 5 req/s policy cap

_last_request_time = 0.0


def _throttle() -> None:
    global _last_request_time
    wait = MIN_INTERVAL - (time.monotonic() - _last_request_time)
    if wait > 0:
        time.sleep(wait)
    _last_request_time = time.monotonic()


def fetch_one(country: str, day: date) -> str:
    """Returns one of: 'ok', 'skipped', 'unavailable', 'failed'."""
    dest_dir = OUT_ROOT / country
    dest = dest_dir / f"{day.isoformat()}.json"
    if dest.exists():
        return "skipped"

    url = f"{BASE_URL}/{country}/all-access/{day.year}/{day.month:02d}/{day.day:02d}"
    dest_dir.mkdir(parents=True, exist_ok=True)
    part = dest.with_suffix(".json.part")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    for attempt in range(1, RETRIES + 1):
        _throttle()
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                part.write_bytes(resp.read())
            part.rename(dest)
            return "ok"
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            not_loaded_yet = e.code == 404 and "not loaded yet" in body
            if (e.code == 429 or not_loaded_yet) and attempt < RETRIES:
                retry_after = e.headers.get("Retry-After")
                time.sleep(int(retry_after) if retry_after else 2**attempt)
                continue
            if e.code == 404:
                part.unlink(missing_ok=True)
                return "unavailable"
            err = e
        except OSError as e:
            err = e
        if attempt < RETRIES:
            time.sleep(2**attempt)
    print(f"  ERROR {url}: {err}", file=sys.stderr)
    part.unlink(missing_ok=True)
    return "failed"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    yesterday = datetime.now(timezone.utc).date() - timedelta(days=1)
    parser.add_argument("--date", type=date.fromisoformat, default=yesterday)
    parser.add_argument("--backfill", type=int, default=1, metavar="N", help="fetch N days ending at --date")
    parser.add_argument("--countries", nargs="+", default=DEFAULT_COUNTRIES)
    args = parser.parse_args()

    days = [args.date - timedelta(days=i) for i in range(args.backfill)]
    totals = {"ok": 0, "skipped": 0, "unavailable": 0, "failed": 0}
    for day in days:
        results = []
        for country in args.countries:
            status = fetch_one(country, day)
            totals[status] += 1
            results.append(f"{country}: {status}")
        print(f"{day}  " + "  ".join(results), flush=True)

    print(f"\ndone — {totals}")
    return 1 if totals["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
