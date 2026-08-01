# Pew Global Attitudes — possible insights (brainstorm)

Same spirit as the GDELT list — this is about understanding people, not just ranking countries. Pew's Spring 2025 wave asks 24 countries (not the US itself) what they think of the US, China, and geopolitics broadly, with rich demographics (age, education, income, religion, ethnicity, party ID, ideology, urbanicity) to slice by. It's one wave on its own, but the same survey (or something close to it) has run most years since 2002 — most of this can become an actual trend line, not just a snapshot. Notes below, not a spec.

- **generational drift on moral/social questions**
    - age vs. the moral-acceptability battery (`moral_homosexuality`, `moral_abortion`, `moral_divorce`, etc.) — how do age groups differ within a country?
    - since it's one wave, age is our stand-in for time — where's the culture heading?
    - compare across countries: are they all drifting the same direction, or do some move faster / more aggressively than others?

- **liberalism / values clustering**
    - score countries on the moral battery, cluster who's similar to whom
    - do it again within age groups, not just country-wide — does a country's 18-29s look more like other countries' 18-29s than like their own 50+ group?

- **democracy satisfaction — hopeful or given up?**
    - `satisfied_democracy`/`polsys_satisfied` (system-level) vs. confidence elections are fair, trust in elected officials, belief the system *can* be reformed
    - lets us tell apart "things are bad but fixable" from "things are bad and nobody thinks it'll change"

- **power, problem, and who you'd still trade with**
    - who's seen as the bigger power (US vs. China — `econ_power`) vs. the bigger problem (rights record, military power, debt-trap risk — the `china_*`/`us_*` batteries)
    - compare both against who people actually want closer economic ties with (`us_or_china`) — do perception and preference line up, or is there a gap (hedging)?

- **domestic vs. foreign leaders — same yardstick?**
    - domestic: are elected officials seen as qualified/honest/caring (`officials_trait_*`)
    - foreign: is Trump seen as qualified/honest/dangerous/diplomatic (`trump_personality_*`)
    - same trait words asked both ways — are people harsher, or more forgiving, on their own leaders than on foreign ones?

- **how countries see other leaders, and whether it lines up with alliances**
    - confidence in Trump/Xi/Putin/Macron/Netanyahu/Zelenskyy — cluster which leaders rise and fall together across countries
    - cross against who a country actually names as its top ally / top threat (`allies_open`/`threats_open`) — does perceived leader trust match stated geopolitics?

- **pre/post-apartheid self- and group-perception (South Africa)**
    - the ladder question is asked both for today and 30 years ago, by racial group
    - rare case where the survey encodes its own before/after — perceived progress, not just a current-state snapshot

- **AI: awareness, feelings, and who they trust to regulate it**
    - heard of AI? excited or worried? trust the US/China/EU/own country to regulate it well?
    - an early read on tech-optimism vs. tech-anxiety, country by country

- **urbanicity, region, and diversity**
    - feelings mapped by region/urbanicity — is optimism/tolerance/threat-perception different in cities vs. elsewhere?
    - urban areas are usually more diverse (religion, ethnicity, caste) — can we measure that diversity directly and see if it correlates with attitudes, instead of just assuming "urban = more diverse, more liberal"?

- **do it all over time**
    - same survey has run most years since 2002 — download prior waves, same questions, same countries
    - turns every bullet above from a snapshot into an actual trend line, which is the whole point of the project

- **cross-reference with GDELT**
    - pull GDELT's mood/tone/volume for a country during its exact Pew field dates (`qdate_s`–`qdate_e`) — was the survey fielded during a calm stretch or mid-shock?
