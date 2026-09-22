# XP ↔ AE Alignment Model (Enterprise)

Internal and confidential. Contains account names, ARR and staffing. **Keep this repository private.** Do not enable GitHub Pages or share a public link.

GitHub: [savannahlane/xp-planning](https://github.com/savannahlane/xp-planning)

## Contents

- `index.html`: interactive map of which State and Local ENT AEs each Experience Partner works with. Toggle between the revised book and the WIP proposed book. Open it in any browser; it needs no server.
- `XP_AE_Rebalance_Model.xlsx`: the working model. Revised XP assignments (editable dropdown), the holds check, AE fan-out, and capacity checks.

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

## Rules modeled

- No more than 17 countable accounts per Enterprise XP
- Complex accounts (more than 7 capabilities, or Service Cloud Advanced) no more than one third of a book
- XP time zone plus or minus one hour
- Holds: San Antonio with Steffany, DC with Paige, Denver with a Savannah report, Columbus with an Ashley report, LA and GLACVCD with Colleen, WA with Paige, CT and ME with Halena
