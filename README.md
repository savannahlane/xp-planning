# XP ↔ AE Alignment Model

Internal and confidential. Contains account names, ARR and staffing. Keep this repository private.

## Contents

- `index.html`: interactive whole-US-team map across Enterprise, Local SMG and federal books. Toggle between the proposed and current assignments, and filter by segment. Open it in any browser; it needs no server.
- `XP_AE_Rebalance_Model.xlsx`: the working model. Revised XP assignments (editable dropdown), the holds check, AE fan-out, capacity checks, per-account growth tiers, and the `Growth Tiers` territory sheet.
- `research/`: the sourced research behind the tiering, plus the tiering hypothesis itself.
- `tiering/`: the scoring model and its outputs.

## Changing who owns an account

Edit **`tiering/account_overrides.csv`**, then run `python3 tiering/update_whole_team_map.py`.
That is the only file to touch for a per-account change; `index.html` is generated and should
not be hand-edited.

One row per account, with these columns:

| Column | What it does |
|---|---|
| `account` | Must match the account name in `index.html` exactly. An unmatched name fails the run rather than silently doing nothing. |
| `new_xp` | The proposed XP. Blank keeps whatever the base map proposed. |
| `new_segment` | `State`, `Local ENT` or `Local SMG`. `Local SMG` moves the account to midmarket and clears the Enterprise flag. Blank keeps the segment. |
| `remove` | `yes` drops the account from the map entirely. |
| `note` | Why. Free text, not parsed. |

Rules that are not per-account stay in `tiering/update_whole_team_map.py`: who cannot hold
accounts at all, where a displaced AE group goes, and the Kentucky and North Dakota
enterprise-agreement rollup.

## Whole-team proposed assignment

The proposed view in `index.html` applies these staffing rules:

- Jake Sager, Nathan Williamson, Savannah Lane, Kristen Murphy and Ashley Hill carry no
  proposed accounts.
- Ashley's current Enterprise accounts route only to her direct reports. The open Pacific XP
  reports to Ashley.
- Carolina Prieto is a Team Lead, not a manager. She keeps the Kentucky and North Dakota
  statewide enterprise agreements (two customers; sister agencies count as allocated children)
  plus Kentucky CHFS, Homeland Security and Transportation for state-book consolidation. She
  does not keep the scattered local accounts (Nashville, Oakland, Aurora, Glendale, Allegheny
  County Treasurer, Outagamie County, and the Pittsburgh Housing Authority).
- Non-SAM special districts are Local SMG. SAM special districts stay Enterprise: GLAVCD
  remains with Colleen. Luke Mulvaney's three districts sit with Carlos Torres so Halena is not
  paired with that vertical.
- Nathan's three federal accounts consolidate with Jr Wycinsky. Jake's Local SMG groups move
  by AE: Emery Herrschel to Kerrian Dailey, Kimberley Steelmann to Andrés Pérez, and Luke
  Mulvaney to Carlos Torres.
- The three Nevada state agencies sit with Cody Nichols, who already works with Cameron
  Chadsey on Arizona and New Mexico. Virginia Department of General Services is removed from
  the map.
- When those three books were removed, each displaced Local SMG AE group moved intact to an XP
  who already worked with that AE. Together with the Carolina rebalance and special-district
  moves, proposed XP↔AE relationships fell from 161 to 131.
- Connecticut PURA is the necessary exception to the no-new-relationship rule. Ashley's
  reporting-line constraint moves it from Halena to Steffany while Halena retains the broader
  Connecticut estate, so Stephanie DelSignore works with two XPs rather than one.

The `Current assignment` view is historical and still shows Savannah, Kristen and Ashley's
current books.

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
python3 tiering/update_workbook.py    # refresh the xlsx
python3 tiering/update_whole_team_map.py  # reapply assignment rules and account_overrides.csv
```

`tiering/account_overrides.csv` is the per-account assignment table described above. The update
script is idempotent, so running it twice changes nothing the second time.

`tiering/inject_html.py` targets the earlier Enterprise-only page payload. Do not run it against
the whole-team `PAGE` payload in the current `index.html`.

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
- Local SMG includes special districts except SAM territories
