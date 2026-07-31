# TMDB — possible insights (brainstorm)

Same spirit as the GDELT and Pew lists — understanding people, not just cataloguing movies.
TMDB's honest role in this project is different from the other sources though: it's not
really an attention-by-geography source (popularity is one global number, no regional
split), it's the best **entity resolution layer** we have — titles, IDs, genres, dates,
keywords, collections — that other sources can be pointed at. Notes below, not a spec.

- **daily ID exports — start now, nobody has the history**
    - the daily export files (popularity + a few flags, one JSON line per ID) are only
      retained ~90 days on TMDB's side — there's no vendor selling this historically
    - start pulling daily today and we build our own full-catalog attention panel that
      doesn't exist anywhere else — the earlier we start, the more of a moat this becomes
    - `/trending/movie/day` and `/week` are a second, faster-moving signal worth pulling
      alongside popularity — how much does the trending list itself churn day to day?

- **geography hooks that actually exist**
    - `/movie/{id}/release_dates` — per-country release dates + local certification
    - `/movie/{id}/watch/providers` — per-country streaming availability (JustWatch)
    - `discover?with_watch_providers=X&watch_region=Y` — one country per call, but workable
    - watch out: `with_origin_country`/`original_language`/`production_countries` describe
      where a title was *made*, not who's watching it — don't confuse supply-side
      geography with audience geography

- **cultural memory**
    - nostalgia residuals — sum popularity by release year, which years keep outperforming
      the normal decay curve?
    - attention half-life — post-release decay rate; is it getting shorter cohort over
      cohort (shorter attention spans, or just more competition for it)?
    - resurrection events — spikes in old titles' popularity; cross-check the same week in
      GDELT/Google Trends for the trigger (re-release, death, meme, sequel news)
    - reputation drift — does `vote_average` on older titles move over time as they get
      reassessed, separately from popularity spikes?

- **supply-side drift (what gets made vs. what gets watched)**
    - genre share of new releases vs. genre share of attention (popularity) — is supply
      chasing demand, or lagging it?
    - `/movie/{id}/keywords` — tag frequency by release year (AI, surveillance, pandemic,
      climate...) — rougher than real topic modeling, but keywords are a much richer,
      less-controlled vocabulary than the ~19 fixed genres
    - franchise share (`belongs_to_collection`), runtime creep, mid-budget collapse — all
      readable straight from the catalog, no audience data needed

- **cross-country signals without audience data**
    - certification divergence — country×country distance matrix on age ratings for the
      same title, tracked over decades — where is "acceptable content" drifting apart vs.
      converging?
    - release lag — days from first release to release in country X; shrinking lag =
      cultural simultaneity increasing
    - cultural export network — which countries' content increasingly shows up first (or
      at all) elsewhere; a supply-side echo of the "who's watching whom" idea from the
      GDELT list
    - catalog overlap — Jaccard similarity of what's available on Netflix-US vs. -JP vs.
      -BR, local-content share; doable via `discover` + `watch_region`, just needs
      enumerating rather than one clean endpoint

- **role in the project**
    - weak as a standalone attention source — one global popularity number, no regional
      split
    - strong as an **entity dimension table** — resolves titles → canonical IDs, genres,
      dates, keywords, collections
    - use it to drive Wikipedia pageviews / Google Trends queries by exact title + year —
      let those supply the regional attention TMDB can't
