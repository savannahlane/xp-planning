# XP ↔ AE Alignment Model (Enterprise)

Internal and confidential. Contains account names, ARR and staffing. Keep this repository private.

## Contents

- `index.html`: interactive map of which State and Local ENT AEs each Experience Partner works with, plus the growth-tier and territory-tier views. Toggle between the revised book and the WIP proposed book. Open it in any browser; it needs no server.
- `XP_AE_Rebalance_Model.xlsx`: the working model. Revised XP assignments (editable dropdown), the holds check, AE fan-out, capacity checks, per-account growth tiers, and the `Growth Tiers` territory sheet.
- `research/`: the sourced research behind the tiering, plus the tiering hypothesis itself.
- `tiering/`: the scoring model and its outputs.

## Growth tiering

`research/ENT-book-growth-tiering-hypothesis.md` is the working hypothesis. The short version:
growth potential separates by which side of the house you sell into within a state, not by
state. The two sides land in different tiers in 32 of 51 jurisdictions. Texas is the only
territory that is top-tier on both. California is the reverse of how it is usually described —
a deeply penetrated state-agency estate inside a distressed budget, next to the largest pool
of unheld 100k-plus jurisdictions in the country.

For the book, the finding is that the 17-account cap balances workload but not opportunity:
growth load varies 2.3x across the thirteen Enterprise seats.

Every account carries a tier, crossing growth potential (60% territory, 40% remaining
capability whitespace) against ARR:

| Tier | | What the XP is being asked to do |
|---|---|---|
| 1 | Growth engine | Expansion, exec relationships, roadmap |
| 2 | Expansion | Land and expand; coachable, lower risk |
| 3 | Defend | Retention, adoption, renewal risk |
| 4 | Maintain | Efficient or pooled coverage |

### Rebuilding

```
python3 tiering/build_tiering.py      # score territories and accounts
python3 tiering/inject_html.py        # refresh index.html
python3 tiering/update_workbook.py    # refresh the xlsx
```

`tiering/state_overlay.csv` holds the judgement calls that cannot be parsed out of the research
tables — purchasing vehicles, occupied league channels, local IT capacity, property tax caps —
with a note on each. Edit it there, then rebuild.

### The caveat that matters most

Whitespace is an upper bound. The model counts a jurisdiction over 100k as open if it is not in
this book, and the ENT book holds 83 of 959 nationally. But Granicus company-wide already
serves 48 of the 50 largest US cities, so most of those "open" jurisdictions sit in another
segment's book. **Local-side scores rank states against each other reliably and are inflated in
absolute terms until the rest of the XP team's books are loaded.** That is the single biggest
reason to extend this model beyond Enterprise; what it needs is set out at the end of the
hypothesis document.

## Sources

- Account Team export, 9/21/26
- Proposed Book (WIP)
- State territory map (updated 6/12/26) and Local ENT map (current as of 6/30/26)
- Tiering research, all in `research/`: state fiscal capacity and IT modernization (NASBO
  Spring 2026, NASCIO, state budget documents); the grant and ARPA-cliff landscape (Treasury
  SLFRF guidance, GAO-26-108587, NTIA, CMS, FEMA, DOJ ADA Title II); demand growth (Census
  Vintage 2025, Building Permits Survey, Census of Governments, FHFA, BLS); and Granicus's
  competitive and purchasing-vehicle position. Each report carries its own source list and an
  explicit note on what its author was least sure about.

## Rules modeled

- No more than 17 countable accounts per Enterprise XP
- Complex accounts (more than 7 capabilities, or Service Cloud Advanced) no more than one third of a book
- XP time zone plus or minus one hour
- Holds: San Antonio with Steffany, DC with Paige, Denver with a Savannah report, Columbus with an Ashley report, LA and GLACVCD with Colleen, WA with Paige, CT and ME with Halena
