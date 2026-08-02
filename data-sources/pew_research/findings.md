# Pew Global Attitudes — findings

What we've *learned* (vs. `possible-insights.md`, which is what we hope). Fill in as exploration answers each section; a source graduates to the Django repo when all sections are covered (see `docs/exploration-plan.md`).

## Fetch recipe
<!-- endpoints, auth, rate limits, cadence, backfill depth -->
- 2025 wave dataset: `data/raw/pew_research/global-attitudes-2025-dataset.csv` (manual download).
- Data dictionary: `global-attitudes-dictionary/` (Variables + Values tables), kept here in data-sources/.
- TODO: download one earlier wave (~2015?) to prove the trend-line join.

## Schema & quirks
<!-- native shape, junk patterns, gotchas found on real data -->

## Granularity
<!-- confirmed spatial + temporal granularity on real data -->
- Stress-tests the model's odd cases: `granularity = wave` (field dates `qdate_s`–`qdate_e`), cohort slices → `cohort` jsonb.

## Observation-spine mapping
<!-- which signal_types, which dims (place/entity/theme), cohort? -->

## Insights produced
<!-- notebook links + one-line takeaways -->
