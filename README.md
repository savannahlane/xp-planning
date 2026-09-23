# XP ↔ AE Alignment Model

Internal and confidential. Contains account names, ARR and staffing. **Keep this repository private.** Do not enable GitHub Pages or share a public link.

GitHub: [savannahlane/xp-planning](https://github.com/savannahlane/xp-planning)

## Contents

- `index.html`: interactive whole-US-team map across Enterprise, Local SMG and federal books. Toggle between the proposed and current assignments, and filter by segment. Open it in any browser; it needs no server.
- `XP_AE_Rebalance_Model.xlsx`: the working model. Revised XP assignments (editable dropdown), the holds check, AE fan-out, capacity checks, per-account growth tiers, and the `Growth Tiers` territory sheet.
- `research/`: the sourced research behind the tiering, plus the tiering hypothesis itself.
- `tiering/`: the scoring model and its outputs.

## Whole-team proposed assignment

The proposed view in `index.html` applies these staffing rules:

- Savannah Lane, Kristen Murphy and Ashley Hill carry no proposed accounts.
- Ashley's current Enterprise accounts route only to her direct reports. The open Pacific XP
  reports to Ashley.
- Carolina Prieto is a Team Lead, not a manager.
- When those three books were removed, each displaced Local SMG AE group moved intact to an XP
  who already worked with that AE. This reduced proposed XP↔AE relationships from 161 to 145,
  reduced excess AE partners from 97 to 81, and reduced the maximum number of XPs working with
  one AE from 11 to 9.
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
python3 tiering/update_whole_team_map.py  # reapply whole-team assignment rules to index.html
```

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

## File types in this repo (and ones you might add)

You already have the two files the model needs. Everything else is optional GitHub plumbing.

| File | Type | Do you need it? |
| --- | --- | --- |
| `index.html` | HTML webpage (CSS and JavaScript are inside this one file) | **Yes.** Open it in a browser to view the XP ↔ AE map. |
| `XP_AE_Rebalance_Model.xlsx` | Excel workbook (Office Open XML; binary in Git) | **Yes.** This is the working capacity / assignment model. |
| `README.md` | Markdown | **Yes.** GitHub shows this on the repo home page. |
| `.gitignore` | Plain text list of files Git should skip | **Yes.** Stops Excel lock files (`~$…xlsx`), OS junk, and secrets from being committed. |
| `.gitattributes` | Git settings for how files are stored | **Useful.** Tells Git `.xlsx` is binary so it will not try to merge the spreadsheet. |
| `LICENSE` | Legal terms | **No** for this internal repo. A public open-source license would invite sharing. Default copyright (all rights reserved) is enough. |
| `.github/workflows/*.yml` | GitHub Actions (CI) | **Not needed yet.** There is no test suite or deploy step. Add later if you want automated checks. |
| `.github/ISSUE_TEMPLATE/` | Issue forms | Optional. Helpful if several people file work in GitHub Issues. |
| `CONTRIBUTING.md` | How to propose changes | Optional. Useful only if more than one person regularly edits the repo. |
| `.env` / credentials | Secrets | **Never commit.** Use a private password manager or a private Drive folder instead. |
| Extra `.css` / `.js` | Stylesheets and scripts | Optional. Only if you split `index.html` into separate files. The map works as a single HTML file. |

**Do not add** a `CNAME` file or GitHub Pages settings while the data is confidential. Pages would publish the map on the public web.

When you edit the spreadsheet, close Excel before committing so Git does not pick up the temporary `~$XP_AE_Rebalance_Model.xlsx` lock file.

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
