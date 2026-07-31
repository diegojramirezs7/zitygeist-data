# GDELT — possible insights (brainstorm)

Goal: understand people better across geography and time. What do people care about,
and when? GDELT's Event/Mentions tables aren't topic-tagged — they're actor/action based —
so a lot of this needs augmentation (NLP, our own classification, or GDELT's GKG table)
on top of the raw columns. Notes below, not a spec.

- **who shows up often, and who doesn't**
    - which actors are consistently present vs. spike once and vanish?
    - actor type (`Actor1Type1Code`: govt/military/business/civil society/etc.) tells us
      who's actually driving the narrative — powerful vs. not, top-down vs. ground-up
    - churn in the "top actors" list week to week = how volatile a country's news cycle is
      right now

- **which actions, where — and does it match what we'd expect**
    - some countries' bar for "this is news" is different — a protest that's front-page in
      one place is background noise in another
    - could build a per-country baseline (rolling avg of volume/tone/Goldstein) and flag
      deviations as "more/less relevant than expected" — needs some baselining work, but
      doable

- **tone (pos/neg)**
    - `AvgTone`/`GoldsteinScale` are blunt, dictionary-based scores — could layer our own
      sentiment/emotion model on the actual article text for something richer

- **topics**
    - CAMEO event codes describe actions (what X did to Y), not topics — doesn't map
      cleanly to politics/crime/sports/business/arts
    - would need our own classification layer: NLP on headlines/articles (via
      `SOURCEURL`), or pull GDELT's GKG table, which actually does have theme tags
      (separate table, not in our current dictionary, but same project — worth grabbing)
    - once we have real categories: which get the most mentions, how long do they stay in
      the news, per country/region over time

- **international vs. domestic attention**
    - ratio of events where a country's own actors act on itself vs. events where foreign
      actors are acting on/around it — is a society looking inward or outward right now?

- **what's a country "known for" in the news**
    - dominant, recurring event-type mix per country = its news personality — civil
      unrest, entrepreneurship, arts, a government that dominates daily-life headlines,
      etc.

- **identity/ethnicity salience**
    - `Actor1EthnicCode`/`Actor1Religion1Code` are usually blank — when they're populated,
      someone in the source text explicitly framed things in ethnic/religious terms
    - tracking that rate over time = how often identity is actually on people's minds in a
      given place, not just assumed

- **who's watching whom**
    - country-to-country attention (`Actor1CountryCode` → `Actor2CountryCode`), by volume
      and tone, tracked over time
    - can we tell when the attention flips from positive to negative, or vice versa?

- **consensus vs. contradicting coverage**
    - compare tone variance across `MentionDocTone` for the same event, across different
      sources
    - which topics/places see more disagreement in how they're reported, and does that
      shift over time?

- **how long does something stay in the news**
    - first mention to last mention on a `GlobalEventID` = story lifespan
    - does it fully die out, or resurface later (anniversaries, follow-ups, retrials)?

- **cross-referencing with the rest of the project**
    - dominant topics/mood per country or region, laid next to Spotify charts, Wikipedia
      pageviews, census data — does the mood/attention line up with what people are
      actually listening to, searching, or doing?

- **Pew tie-in**
    - pull the mood/tone/volume for a country during its exact Pew field dates — did the
      survey catch people in a normal mood or mid-shock?
