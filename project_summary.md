# Project Overview: Cultural Zeitgeist & Trend Analysis

# Project Overview: Cultural Zeitgeist & Trend Analysis
## Goal
Find and combine datasets/APIs that reveal **cultural shifts and the zeitgeist across
locations over time**. The core interest is spotting trends in what people pay attention
to, listen to, watch, and believe — and how those trends differ by region and evolve
across time.
 
## Analytical Framing
No single source covers demographics + culture + geography + time cleanly. The intended
pattern is:
- **Spatial-temporal backbone**: a geographic/demographic dataset (e.g. Census) defines
  the regions and time buckets.
- **Attention signals**: cultural/media/search datasets get joined onto that backbone by
  region + time period.
 
Google Trends and GDELT are the primary starting points because both are explicitly
normalized for cross-region, cross-time comparison. Most entertainment APIs give
snapshots and leave the longitudinal assembly to the user.
 
## Candidate Sources
 
### Demographic / social attitudes
- **Google Trends API** (pytrends / official beta) — normalized search interest by region
  and time; DMA/metro-level in the US. Best proxy for attention shifts.
- **US Census Bureau APIs** — ACS (demographics, income, migration, households down to
  tract level), PEP (population estimates). Deeply longitudinal.
- **General Social Survey (GSS)** — US attitudes/values/beliefs since 1972.
- **World Values Survey / European Social Survey** — cross-national attitude trends.
- **Pew Research** — downloadable social/political/religious trend datasets.
 
### Entertainment / media
- **Spotify Charts** — country-level daily/weekly top tracks going back years. (Note:
  Spotify's public API deprecated audio-features/recommendation endpoints in late 2024.)
- **TMDB API** — free film/TV metadata, popularity scores, release dates.
- **Last.fm API** — listening/scrobble data with tags and geographic charts.
- **IMDb / Box Office Mojo** — box office by region and time (scraping-heavy).
- **YouTube Data API** — trending videos by region, engagement metrics.
- **Reddit API** — subreddit activity over time as a culture-shift signal (watch rate limits).
 
### Regional / temporal trend layers
- **GDELT** — global, geocoded news coverage + event/tone data, updated every 15 min; free
  via BigQuery. Built for measuring shifts in what the world discusses across place and time.
- **Wikipedia Pageviews API** — daily article views by country; clean attention proxy.
- **Twitter/X** — historically strong but API now expensive/restricted; don't assume free access.
 
## How I'll use this doc
In future sessions I'll ask about **specific use cases of a given source** (e.g. how to
pull a particular signal, how to join two sources, what a given API can/can't do). This
file exists so Claude has the project goal and source landscape as context.

## Possible UX
Use the same idea of map layers to add insights on top of each other and see how different things tie together. 