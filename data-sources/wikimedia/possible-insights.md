# Wikimedia — possible insights (brainstorm)

Pageviews are the most direct "what are people curious about, right now, here" signal in the whole project — more direct than GDELT (measures what media covers) or TMDB (measures what gets produced). Wikipedia is also unusual among our sources in having a real supply side: people write and fight over the content itself, not just consume it. Notes below, not a spec.

- **seeds don't need to be manual**
    - `top-per-country` returns 1,000 articles per country-day — take the union across countries over a period and seeds emerge bottom-up
    - use the per-article pageviews endpoint to backfill a full time series for anything that looks interesting
    - only seed manually when we're testing a specific hypothesis, not as the default discovery method

- **language editions are a second geography, and the real structural gift here**
    - the same concept gets a separate article in ~300 languages, linked by a shared Wikidata Q-id — country and language are different cultural axes, and the gap between them is itself a signal
    - cross-language attention on the same Q-id: a spike in one language edition = local event, a spike everywhere at once = global event
    - measure the lag between languages picking up the same Q-id → an attention-diffusion map showing how an idea propagates across linguistic communities, and in what order

- **article length per language, same Q-id — a documentation-effort signal**
    - proxy for how much a culture thinks a topic is worth documenting, not just reading — compare `Abortion`, `Genocide`, `Nuclear power` across en/de/ar/ja
    - the asymmetry is the signal; the most basic version of it is binary — does the article even exist yet in that language at all

- **edits, not just views — attention ≠ contention**
    - revision counts, revert rates, edit wars, page protection, talk-page volume — what a culture is actively fighting about, not just looking at
    - crossing views × edits gives a real 2x2: high-view/high-edit = live public argument, high-view/low-edit = settled and passively consumed, low-view/high-edit = a niche ideological battleground nobody else is watching
    - the same length-asymmetry technique works here too — same Q-id, calm edit history in one language, a war zone in another

- **article creation dates — when a concept enters public consciousness**
    - track first-article-date by language → concept-adoption curves
    - worth lining up against GDELT's first heavy coverage of the same entity, or TMDB's release date for a film's Q-id — how long between something existing and it becoming "a thing"?

- **seasonality and recurrence**
    - answers "what topics keep coming up" — annual cycles: holidays, religious observances, exam seasons, tax deadlines
    - what recurs *where* is a culture fingerprint; hourly granularity is available too, for circadian patterns within a single day

- **country-similarity — but baseline it first**
    - raw top-1000 overlap is dominated by structural background — main pages, "Deaths in 2026," search artifacts, adult content — countries will look similar mostly because the internet is similar
    - detrend against each country's own baseline and compare anomalies, not raw overlap

- **strategic: Wikidata Q-ids are the join key for the whole project**
    - resolves TMDB films, GDELT entities, and Wikipedia articles into one shared entity space
    - worth locking in early — this is the piece that turns four separate sources into one
