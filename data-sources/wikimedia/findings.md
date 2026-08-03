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
- **Filter validated across a 3rd, unrelated country**: tested CA/US/MX same day (2026-08-01). Namespace rule generalized correctly to ~30 language editions it had never seen before (Fijian, Cornish, Manx Gaelic, Hausa, Rwandan, Slovak, Sotho...) — 100% correctly classified, zero false positives on real titles across all 3 countries.
- **Noise ratio varies a lot by country, and isn't really about the country**: CA 12/220 (~5%), US 91/1000 (~9%), MX 39/110 (~35%). MX's noise was almost entirely `Special:Search`/`Special:RecentChanges` hits across dozens of small, geographically-irrelevant wikis — reads like automated/bot traffic (crawlers, mirror sync, monitoring) that evaded Wikipedia's bot filter, geolocated to Mexico via hosting/VPN infra rather than real readers. It's visible in MX specifically because MX's real human traffic is smaller (see below), so the bot noise floor isn't buried under a large volume of real articles like it is in the US.
- `top-per-country`'s **list length itself varies hugely** and isn't a fixed 1000: CA 220, US 1000, MX 110 (same day). Likely reflects the API's confidence/threshold suppression for low-traffic country-article combos, not "Mexicans read fewer distinct articles." **Worth treating list length as a per-country/day data-quality signal** — a short list is both lower-confidence and proportionally noisier.
- Real (post-filter) overlap check, CA/US/MX same day: 20 titles shared across all 3 (mostly global entertainment/sports — Avengers, Spider-Man, Ronaldo, Haaland), a handful unique to each reflecting local content (CA: Caribana, Commonwealth Games; MX: Copa Mundial de Fútbol 2026, Día de la Pachamama; US: US election articles). Matches the project's expected mix of shared global signal + local distinctiveness.
- Checked the bot-traffic hypothesis on a sample of MX's noise pages via `per-article`'s `agent` split (`user`/`spider`/`automated`) — note this endpoint is **global, not country-scoped**, so it's circumstantial only. Sample of 10: median 45% non-"user" share, a few pages 43–61%. Suggestive of real automated traffic but not conclusive. Not worth digging further for now.

## Granularity
<!-- confirmed spatial + temporal granularity on real data -->
- `top-per-country` article *count* per country-day is not fixed/comparable across countries (see noise-ratio note above) — needs to be captured as metadata alongside any observation derived from it, not assumed constant.

## Q-id resolution
<!-- title → Wikidata Q-id flow, proven end to end — this is the project's join key -->
- **Proven end to end**: resolve via each project's own `action=query&prop=pageprops&ppprop=wikibase_item` (same per-project pattern as the noise filter's siteinfo calls). `Cristiano_Ronaldo` on `en.wikipedia` (pageid 623737) and `es.wikipedia` (pageid 210682) — two different pages — both resolve to `Q11571`. Confirms the join key actually works across language editions, not just in theory.
- **Reusable batched resolver**: `notebooks/wikimedia_qid.py` (`resolve_qid`/`resolve_qids`). `action=query` allows up to 50 titles/request — batching matters a lot here since this endpoint rate-limits much tighter than the pageviews REST API (hit real 429s on it twice already, see noise-filter notes). Handles redirects (`redirects=1`) and title normalization, returns `None` (not an error) for pages with no linked Wikidata item.
- **Real-scale test**: Canada's full 208-title kept list (2026-08-01) → **208/208 resolved (100%)**, in 6 batched requests instead of 208. Zero unresolved titles in this sample.
- **Side finding**: post-noise-filter, Canada's *real* content collapses to only 2 projects (`en.wikipedia`, `fr.wikipedia`) — `zh.wikipedia`/`zu.wikibooks`/`commons.wikimedia`/`wikitech.wikimedia` entries in the raw list were entirely mainpage/namespace noise, no real content survived from them. Tracks Canada's bilingual reality and is a small sanity check that the noise filter isn't hiding real diversity that was never there.

## Observation-spine mapping
<!-- which signal_types, which dims (place/entity/theme), cohort? -->

## Insights produced
<!-- notebook links + one-line takeaways -->
