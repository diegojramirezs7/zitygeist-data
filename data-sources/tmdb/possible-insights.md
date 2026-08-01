# TMDB — possible insights (brainstorm)

Refocused: this is about what stories get told, not how a title moves between markets or platforms — logistics (release dates, certifications, watch providers, release lag, catalog overlap) are cut, they don't say anything about people. TMDB's real value here is as a content + entity layer: genres, keywords, overview text, and production-country metadata, augmented with our own classification where TMDB's built-in categories are too coarse. Notes below, not a spec.

- **daily ID exports — start now, nobody has the history**
    - the daily export files (popularity + a few flags, one JSON line per ID) are only retained ~90 days on TMDB's side — no vendor sells this historically
    - start pulling daily today and we build our own full-catalog attention panel that doesn't exist anywhere else
    - `/trending/movie/day` and `/week` as a second, faster-moving churn signal alongside popularity

- **build our own theme taxonomy, not just genres/keywords**
    - TMDB genres are ~19 fixed buckets, keywords are uncontrolled tags — neither one answers "what is this movie actually about"
    - classify `overview` text (+ keywords) ourselves into themes that matter for zeitgeist tracking: love/relationships, war/conflict, crime, financial anxiety/class, technology & AI, family, identity, climate, etc.
    - lets us ask "what are stories about right now" the same way we'd ask it of a survey or a news feed — and gives GDELT/Pew a comparable topic vocabulary instead of three incompatible ones

- **what does each country's film industry make**
    - `production_countries`/`with_origin_country` + our own theme taxonomy + genre, aggregated by year — what themes does country X's industry produce, and how does the mix shift year to year?
    - valuable on its own even with zero audience data for that country — what gets greenlit is a signal of what's culturally live in a place, independent of what people there say they think

- **creative risk vs. playing it safe**
    - franchise share (`belongs_to_collection`) — how much of what's made is existing IP vs. original?
    - `budget` lets us look at the distribution directly — is the mid-budget movie actually disappearing (a "barbell" of tentpoles + micro-budget genre films), or is that just a narrative we've absorbed?
    - pair with the theme taxonomy — are original/mid-budget stories exploring different themes than franchise output, or has everything converged on the same handful?

- **cultural memory**
    - nostalgia residuals — raw "sum popularity by release year" is mostly recency bias (TMDB's popularity score itself favors current activity). Better: track *renewed* popularity momentum long after the initial release-decay period, by release-year cohort — which eras keep getting rediscovered, not just which eras had a lot of activity when they were new?
    - attention half-life — the same recency confound distorts raw decay-rate comparisons across eras (today's titles simply have more total online activity feeding the metric). Normalize each title's trajectory to its own peak first, then compare decay *shape* across cohorts — a cleaner test of whether attention spans are actually shrinking
    - resurrection events — spikes in old titles' popularity; cross-check the same week in GDELT/Google Trends for the trigger (re-release, death, meme, sequel news)
    - reputation drift — does `vote_average` on older titles move over time as they get reassessed, separately from popularity spikes?

- **role in the project**
    - weak as a standalone attention source — one global popularity number, no regional split
    - strong as a **content + entity layer** — titles, themes, genres, production countries, resolved to canonical IDs
    - use it to drive Wikipedia pageviews / Google Trends queries by exact title + year — let those supply the regional attention TMDB can't
