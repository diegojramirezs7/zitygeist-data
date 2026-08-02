# TMDB — findings

What we've *learned* (vs. `possible-insights.md`, which is what we hope). Fill in as exploration answers each section; a source graduates to the Django repo when all sections are covered (see `docs/exploration-plan.md`).

## Fetch recipe
<!-- endpoints, auth, rate limits, cadence, backfill depth -->
- Daily ID exports: retention ~90 days, nobody sells history — collector is Phase 1 priority.
- **Confirmed (Aug 2 2026)**: `http://files.tmdb.org/p/exports/{type}_MM_DD_YYYY.json.gz`, no auth, published ~08:00 UTC daily. S3 answers **403** (not 404) for dates outside retention.
- **Actual retention is 121 days**, not the documented ~90 (confirmed Aug 2 2026: oldest available file was Apr 4; Apr 3 and older return 403).
- **Local capture complete (Aug 2 2026)**: full 121-day window (2026-04-04 → 2026-08-02), 3 types × 121 days, 12GB in `data/raw/tmdb/exports/`. From here forward only the daily pull matters.
- Collector: `scripts/fetch_tmdb_exports.py` (stdlib-only, idempotent, atomic writes) → `data/raw/tmdb/exports/<YYYY-MM-DD>/{type}.json.gz`. Default types: movie_ids, tv_series_ids, person_ids.
- Sizes per day: movies 26MB gz / 1.23M lines, people 71MB / 4.85M, TV 4.7MB / 228K → **~102MB/day, ~9GB per 90-day window**.
- **Daily pull automated (Aug 2 2026)**: `.github/workflows/tmdb-daily-export.yml`, cron 09:30 UTC (after TMDB's publish), `--backfill 2` for self-healing against a missed run, syncs to `s3://zitygeist-data-373286627077-ca-west-1-an/tmdb/exports/` (region ca-west-1). IAM user scoped to PutObject/GetObject/ListBucket on this bucket only. Full 121-day local backfill seeded to the same S3 prefix the same day.
- S3 is now the durable copy of record; local `data/raw/tmdb/exports/` stays as the working copy for notebooks.

## Schema & quirks
<!-- native shape, junk patterns, gotchas found on real data -->
- Export line schemas (JSON-lines): movies `{adult, id, original_title, popularity, video}`; people `{adult, id, name, popularity}`; TV `{id, original_name, popularity}`.
- `original_title`/`original_name` is the original-language title (e.g. プライド) — display names need the API, exports are join-by-id only.

## Granularity
<!-- confirmed spatial + temporal granularity on real data -->

## Observation-spine mapping
<!-- which signal_types, which dims (place/entity/theme), cohort? -->

## Insights produced
<!-- notebook links + one-line takeaways -->
