"""Fetch TMDB daily ID export files into data/raw/tmdb/exports/<date>/.

TMDB publishes daily gzipped JSON-lines exports (one object per ID, with a
popularity score) at http://files.tmdb.org/p/exports/{type}_MM_DD_YYYY.json.gz,
by ~8:00 UTC each day, retained only ~90 days. No API key needed.

Usage:
  python scripts/fetch_tmdb_exports.py                    # today (UTC)
  python scripts/fetch_tmdb_exports.py --date 2026-08-01
  python scripts/fetch_tmdb_exports.py --backfill 95      # date and N-1 days before it
  python scripts/fetch_tmdb_exports.py --types movie_ids person_ids

Idempotent: existing files are skipped, so re-running a backfill only fetches
what's missing. Missing days (outside retention / not yet published) are
reported and skipped, not treated as errors.
"""

import argparse
import gzip
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

BASE_URL = "http://files.tmdb.org/p/exports"
DEFAULT_TYPES = ["movie_ids", "tv_series_ids", "person_ids"]
ALL_TYPES = DEFAULT_TYPES + [
    "collection_ids",
    "keyword_ids",
    "production_company_ids",
    "tv_network_ids",
]
OUT_ROOT = Path(__file__).resolve().parent.parent / "data" / "raw" / "tmdb" / "exports"
RETRIES = 3
CHUNK = 1 << 20


def export_url(export_type: str, day: date) -> str:
    return f"{BASE_URL}/{export_type}_{day.strftime('%m_%d_%Y')}.json.gz"


def valid_gzip(path: Path) -> bool:
    try:
        with gzip.open(path, "rb") as f:
            while f.read(CHUNK):
                pass
        return True
    except (OSError, EOFError):
        return False


def fetch_one(export_type: str, day: date) -> str:
    """Returns one of: 'ok', 'skipped', 'unavailable', 'failed'."""
    dest_dir = OUT_ROOT / day.isoformat()
    dest = dest_dir / f"{export_type}.json.gz"
    if dest.exists():
        return "skipped"

    url = export_url(export_type, day)
    dest_dir.mkdir(parents=True, exist_ok=True)
    part = dest.with_suffix(".gz.part")

    for attempt in range(1, RETRIES + 1):
        try:
            with urllib.request.urlopen(url, timeout=60) as resp, open(part, "wb") as out:
                while chunk := resp.read(CHUNK):
                    out.write(chunk)
            if not valid_gzip(part):
                raise OSError("downloaded file is not a valid gzip")
            part.rename(dest)
            return "ok"
        except urllib.error.HTTPError as e:
            # S3 answers 403 (not 404) for keys outside the retention window
            if e.code in (403, 404):
                part.unlink(missing_ok=True)
                if not any(dest_dir.iterdir()):
                    dest_dir.rmdir()
                return "unavailable"
            err = e
        except OSError as e:
            err = e
        part.unlink(missing_ok=True)
        if attempt < RETRIES:
            time.sleep(2**attempt)
    print(f"  ERROR {url}: {err}", file=sys.stderr)
    return "failed"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--date", type=date.fromisoformat, default=datetime.now(timezone.utc).date())
    parser.add_argument("--backfill", type=int, default=1, metavar="N", help="fetch N days ending at --date")
    parser.add_argument("--types", nargs="+", choices=ALL_TYPES, default=DEFAULT_TYPES)
    args = parser.parse_args()

    days = [args.date - timedelta(days=i) for i in range(args.backfill)]
    totals = {"ok": 0, "skipped": 0, "unavailable": 0, "failed": 0}
    for day in days:
        results = []
        for export_type in args.types:
            status = fetch_one(export_type, day)
            totals[status] += 1
            results.append(f"{export_type}: {status}")
        print(f"{day}  " + "  ".join(results), flush=True)

    print(f"\ndone — {totals}")
    return 1 if totals["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
