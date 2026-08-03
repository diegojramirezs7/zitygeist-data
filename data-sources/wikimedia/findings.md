# Wikimedia — findings

What we've *learned* (vs. `possible-insights.md`, which is what we hope). Fill in as exploration answers each section; a source graduates to the Django repo when all sections are covered (see `docs/exploration-plan.md`).

## Fetch recipe
<!-- endpoints, auth, rate limits, cadence, backfill depth -->

## Schema & quirks
<!-- native shape, junk patterns, gotchas found on real data -->
- Key question: how much of a raw top-1000 per country is structural junk (main pages, "Deaths in…", search artifacts), and what cleaning rule works?
- `top-per-country` mixes projects, not just en.wikipedia — Canada's list (2026-08-01) included `fr.wikipedia`, `zh.wikipedia`, `en.wiktionary`, `zu.wikibooks`, `commons.wikimedia`, `wikitech.wikimedia`.
- **Naive colon-prefix filtering false-positives on real titles** (`Spider-Man:_Brand_New_Day`, `Avengers:_Doomsday`) — a colon isn't a namespace marker by itself.
- **Working rule**: `notebooks/wikimedia_noise.py` (`is_noise(article, project)`) — pulls each project's real mainpage title + localized namespace names from its own `action=query&meta=siteinfo` endpoint, then flags an article only if it equals the mainpage or its colon-prefix matches a real namespace name for that specific project. On CA/2026-08-01: 220 → 12 noise, 208 kept, zero false positives on real titles.
- **Known gap**: doesn't catch structurally-recurring-but-real articles like `Deaths_in_2026` (no namespace prefix). Needs a separate small regex/pattern list, not yet promoted out of the notebook — want more countries first to see the fuller pattern set before committing to one.

## Granularity
<!-- confirmed spatial + temporal granularity on real data -->

## Q-id resolution
<!-- title → Wikidata Q-id flow, proven end to end — this is the project's join key -->

## Observation-spine mapping
<!-- which signal_types, which dims (place/entity/theme), cohort? -->

## Insights produced
<!-- notebook links + one-line takeaways -->
