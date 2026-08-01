# Project Overview: Cultural Zeitgeist & Trend Analysis

## Goal
Find and combine datasets/APIs that reveal **cultural shifts and the zeitgeist across locations over time** — this is about understanding people, not just cataloguing data. The core interest is what people pay attention to, value, believe, and fight over — how that differs by region and evolves across time, and also the global-level sentiment and trends that don't split cleanly by either.

## What We're Looking For
Criteria that came out of scoping each source, used to decide what stays in a source's insight list and what gets cut:

- **People over plumbing.** Every angle should ultimately answer something about people — curiosity, values, contested beliefs, collective memory — not just describe a system's own mechanics (release logistics, API structure, infrastructure metadata). Logistics gets cut unless it's in service of a people-signal.
- **Splittable by region/time is the ideal, not a requirement.** It's what makes sources joinable and comparable, so we prefer it when it's there. But global sentiment and signals that are only strong on one axis (like TMDB's production-country data instead of audience geography) are still genuinely valuable, not a fallback — see "Global signals" under Analytical Framing.
- **Augment thin categories rather than settle for them.** Where a source's built-in taxonomy is too coarse or doesn't exist (GDELT's action codes, TMDB's genres/keywords), we classify it ourselves (NLP/LLM) instead of dropping the idea or accepting the source's categories as final.
- **Relative over raw.** Baseline against a country's, cohort's, or title's own history and look at deviations, not raw totals — raw magnitude is usually confounded (recency bias, "the internet is just bigger now," structural background noise).
- **Attention vs. contention/investment are different signals.** What people look at/consume isn't the same as what they act on, produce, or fight over. Keep both where a source offers both (Wikipedia views vs. edits, TMDB what's made vs. what's watched, Pew stated favorability vs. stated preference), rather than collapsing them into one number.
- **Cross-referencing is a first-class goal.** The same entity, place, or time window should be checkable across sources, not just within one.

## Analytical Framing
No single source covers demographics + culture + geography + time cleanly. The intended pattern is:
- **Spatial-temporal backbone**: a geographic/demographic dataset defines the regions and time buckets everything else gets joined onto.
- **Attention signals**: cultural/media/search datasets get joined onto that backbone by region + time period.
- **Entity backbone**: Wikidata Q-ids resolve the same real-world entity (a person, film, concept, event) across GDELT, TMDB, and Wikipedia, so sources can be joined by entity, not just by region + time. Worth locking in early since it's what turns several separate datasets into one.
- **Global signals**: not everything splits cleanly by region and time, and that's fine — a global mood index, an aggregate sentiment score, an overall cultural shift are real, deliberate targets of this project, not consolation prizes for sources that fall short of the ideal. These get computed and shown as their own layer rather than being forced into the region/time grid, and every source's insight doc should call out where it has something to say at the global level even if it can't be split further.

## Sources
The six sources currently in scope. Each has a detailed brainstorm doc under `data-sources/<name>/possible-insights.md` — this is just the one- or two-line role each plays.

- **Pew Research – Global Attitudes Survey**: the only source that asks people directly what they think and value, across 24 countries with deep demographic slicing (age, religion, income, ideology). Fielded annually since 2002, so it's also the project's main lever for genuine attitude trend lines rather than a single snapshot.
- **GDELT**: global, geocoded news event and tone data updated continuously. Measures what the world's media covers and how emotionally, giving a high-frequency mood/attention proxy across place and time that can be checked against Pew's field dates or spikes in Wikipedia/Trends.
- **TMDB**: a strong content and entity layer — genres, our own theme classification, and per-country production metadata reveal what stories a place's film industry is telling, a real cultural signal even without per-country audience data (its popularity metric is global-only).
- **Wikimedia (Wikipedia)**: pageviews are the most direct curiosity signal in the project — what people look up, where, when. Edits, reverts, and talk-page volume add a second, distinct signal for what people actively contest or invest effort in, and Wikidata Q-ids double as the entity-resolution backbone tying the other sources together.
- **Spotify Charts**: city-level, weekly top-tracks data with tight geography and time resolution. Lets us measure how musical taste clusters, converges, or diverges across cities, and whether shifts in taste track real-world events.
- **Google Trends**: normalized search interest by region and time, down to DMA/metro level in the US — the most direct "what are people actively curious about" signal available, and the natural cross-check for spikes found in GDELT or Wikipedia. Access is pending (alpha API, awaiting invite).

Other candidate sources we scoped out or set aside for now are tracked in `potential_sources.md`.

## Possible UX
Use the same idea of map layers to add insights on top of each other and see how different things tie together. Global/non-splittable signals won't fit that map-layer model — they need their own presentation (e.g. a headline or aggregate view) surfaced alongside the regional layers, not squeezed into them. Keep this in mind once we start building insights and the UI, not just while scoping sources.

## How I'll use this doc
In future sessions I'll ask about **specific use cases of a given source** (e.g. how to pull a particular signal, how to join two sources, what a given API can/can't do) — the per-source `possible-insights.md` docs have the detailed brainstorms, this file is the standing context on project goals, values, and which sources are actually in scope.
