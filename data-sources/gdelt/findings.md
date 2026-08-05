# GDELT — findings

What we've *learned* (vs. `possible-insights.md`, which is what we hope). Fill in as exploration answers each section; a source graduates to the Django repo when all sections are covered (see `docs/exploration-plan.md`).

## Fetch recipe
<!-- endpoints, auth, rate limits, cadence, backfill depth -->
- **Two relevant endpoints, very different granularity.** GDELT 2.0's 15-minute export (`data.gdeltproject.org/gdeltv2/<timestamp>.export.CSV.zip`, pointer at `gdeltv2/lastupdate.txt`) is real-time but one file per 15 min — fine for a live snapshot, wasteful for a multi-month panel. GDELT 1.0's daily export (`data.gdeltproject.org/events/<YYYYMMDD>.export.CSV.zip`) is one file per *day* and already contains every country — this is the one that matters for the country-day panel.
- No auth, no observed rate limiting — it's a plain static file host, not an API. No shared throttle/retry module needed the way Wikimedia required.
- **`lastupdate.txt`'s pointer can be ahead of what's actually published** — hit a live ~30-minute gap where the pointer named a file that 404'd, and so did the interval before it. Not our bug; GDELT's own publishing pipeline has real gaps. Fixed by stepping back 15 minutes at a time until a file actually exists, rather than trusting the pointer blindly.
- Both schemas are fixed-width, no header row — column names have to be supplied positionally. GDELT 2.0's schema has 61 columns (includes `ADM2Code` per geo field), GDELT 1.0's has 58 (no `ADM2Code`) — genuinely different schemas, not a copy-paste bug. Verified both counts against real downloaded files before trusting either.

## Schema & quirks
<!-- native shape, junk patterns, gotchas found on real data -->
- Open question: are GKG theme tags usable as-is, or do we still need our own classification layer?
- **`CountryCode` fields are FIPS 10-4, not ISO 3166-1.** `UK` and `GM`, not `GB`/`DE` — used the ISO codes first and got ~0 rows for Germany and near-nothing for "GB" (a real but unrelated FIPS match) instead of an error, which made it an easy miss. CA/US/MX are identical in both standards, so this only bit newly-added countries. Worth remembering for every future country added.
- **Coverage is heavily wire-service/English-language skewed, not population-proportional.** Mean daily event count over a 90-day window (CA/US/MX/UK/GM): US ~29,700, UK ~5,380, CA ~2,600, GM ~825, MX ~490. Not proportional to population or news volume in any of those countries' own languages — matches the project's own brainstorm note that GDELT is wire-monitoring-driven, so non-English-source countries look artificially quiet.

## Granularity
<!-- confirmed spatial + temporal granularity on real data -->
- Daily is the practical floor for a multi-month panel (one request/day via GDELT 1.0). 15-minute granularity exists (GDELT 2.0) but at 96x the request volume for the same day — only worth it for near-real-time snapshots, not backfills.
- `ActionGeo_Type == 4` ("world city") is what lets you go finer than country — proven in the Canadian-city fingerprint (Toronto, Ottawa, Vancouver, etc. all separable within CA).

## Observation-spine mapping
<!-- which signal_types, which dims (place/entity/theme), cohort? -->
- First derived-observation experiment planned here: rolling per-country tone/volume baseline + deviation flags.
- **Done**: `notebooks/gdelt/gdelt.ipynb` builds a real country-day panel (CA/US/MX/UK/GM, 2026-05-06 to 2026-08-03, 450 country-days) with `events`/`goldstein`/`tone` per country-day, then a 14-day trailing rolling baseline (`shift(1)`, so a day's own value never leaks into its own baseline) with a z-score deviation flag on `tone`. 77/450 country-days flagged at `|z| > 1.5`. This is the "relative over raw" idea from the two-layer model, working on real data: **place** = country (FIPS code — needs a FIPS→ISO mapping to join against Wikimedia later), **temporal** = date, **signal_type** = `events`/`goldstein`/`tone` (raw) plus a derived `tone_z` (baseline deviation).

## Insights produced
<!-- notebook links + one-line takeaways -->
- **`notebooks/gdelt/gdelt.ipynb`** — split out of `source-exploration.ipynb`, now the dedicated GDELT notebook. Sections: 15-min raw snapshot + mood ranking, best/worst country-pair relationships (6-hour window), Canadian city topical fingerprinting (30-day GDELT 1.0 pull), country-day fetch mechanics check, the CA/US/MX/UK/GM 90-day tone/volume panel, and the rolling-baseline deviation-flag experiment. First two Phase 2.2 checklist items done (panel + derived-observation experiment); GKG theme tags still open.
