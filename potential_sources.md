# Potential Sources (not in scope yet)

Companion to `project_summary.md`. These are sources we scoped out or set aside while narrowing down to the current six — not rejected, just not worth the effort yet given what the six already cover. Each note says why it's here instead of in the main doc. Organized the same way the original candidate list was.

## Demographic / social attitudes

- **US Census Bureau APIs** (ACS, PEP) — deeply longitudinal, tract-level demographics, but US-only. Useful if we ever scope a US-focused sub-analysis; doesn't extend the spatial-temporal backbone to the rest of the project's countries.
- **Eurostat / UN Population Division** — the non-US equivalent of Census-style demographic data. Needed if we actually want the spatial-temporal backbone to cover the same footprint as Pew/GDELT/Trends instead of just the US.
- **General Social Survey (GSS)** — US attitudes/values/beliefs since 1972. Same role as Pew (direct self-reported values) but US-only and running even longer — a good source for extending the US trend line further back than Pew's ~2002 start.
- **World Values Survey / European Social Survey** — cross-national attitude trends, overlapping with Pew's role but different country coverage and question wording. Useful as a second opinion, or for countries Pew doesn't survey.
- **Afrobarometer / Latinobarómetro / Arab Barometer** — regional attitude surveys covering countries Pew's 24-country wave mostly skips (much of Africa, Latin America, MENA). Same self-reported-values role as Pew, filling in the map where it's thin.

## Entertainment / media

- **Last.fm API** — listening/scrobble data with tags and geographic charts. A more granular alternative or complement to Spotify's weekly city charts.
- **IMDb / Box Office Mojo** — box office by region and time. This is the piece that would actually give TMDB real audience geography, which TMDB itself can't provide (its popularity metric is global-only). Scraping-heavy, so deferred until there's a concrete need for it.
- **YouTube Data API** — trending videos by region, engagement metrics. Another revealed-attention signal with real geographic resolution.
- **Reddit API** — subreddit activity over time as a culture-shift signal. Watch rate limits.
- **App store trending charts** (Apple App Store / Google Play) — what people are downloading, by country. A revealed-behavior attention signal we haven't scoped in detail yet.

## Regional / temporal trend layers

- **Twitter/X** — historically strong signal but the API is now expensive/restricted; don't assume free access. The same caveat probably applies to TikTok/Instagram trending data if we ever look there.
- **Google Books Ngram Viewer** — long-run (centuries) word-frequency data from published books. A much slower-moving complement to Wikipedia's article-creation-date idea — useful for concept-adoption curves that predate Wikipedia's ~25-year existence.
