# XP ↔ AE alignment map

`index.html` is the map. Nothing in it should be edited by hand. Every change goes into a CSV or a
named constant in `tiering/update_whole_team_map.py`, and then a script rewrites the page.

```
index.html                      the page (generated; do not hand-edit)
XP_AE_Rebalance_Model.xlsx      the book the growth tiers are built from
research/*.md                   market research the territory scores read
tiering/
  account_overrides.csv         ← one account, one change
  fy2027_pipeline.csv           ← committed pipeline (new logos + expansion ARR)
  ae_territories.csv            ← which states each AE covers
  state_overlay.csv             ← hand-judged state inputs to the growth score
  update_whole_team_map.py      ← group-level rules (AE groups, Local SMG, pods, caps)
  build_tiering.py              ← growth-tier model and weights
  update_ae_territories.py, inject_html.py, update_workbook.py
```

---

## Where to make a change

| I want to… | Edit | Then run |
|---|---|---|
| Move one **Enterprise** account (State or Local ENT) to another XP | `account_overrides.csv` → `new_xp` (check the rules below first) | `update_whole_team_map.py` |
| Move a **whole AE group** to one XP | `AE_OWNER` in `update_whole_team_map.py` | `update_whole_team_map.py` |
| Move a **Local SMG** account | Not per account. Change the AE group's line in `LOCAL_SMG_DESTINATION`, or the named lists `SOUTHERN_CA_LOCAL_SMG` / `SE_MM_SOUTH_FL` | `update_whole_team_map.py` |
| Change an account's **segment** (Enterprise ↔ Local SMG) | `account_overrides.csv` → `new_segment` | `update_whole_team_map.py` |
| **Remove** an account from the map | `account_overrides.csv` → `remove` = `yes` (permanent; see gotchas) | `update_whole_team_map.py` |
| Change **NY/NJ state**, **Kentucky state** or **North Dakota** owner | `NY_NJ_STATE_XP`, `KY_STATE_XP` / `KY_COUNTABLE`, or the ND block in `apply_assignments` | `update_whole_team_map.py` |
| Change who holds Marcy's former **enterprise** book | `TATIANA_ENTERPRISE_AES` / `TATIANA_ENTERPRISE_ACCOUNTS` | `update_whole_team_map.py` |
| Add **pipeline** (new logo or expansion ARR) | `fy2027_pipeline.csv` | `update_whole_team_map.py` |
| Say someone **holds no book** (manager, departed) | `NO_BOOK` | `update_whole_team_map.py` |
| Change **book-size caps** | `ENTERPRISE_TARGET`, `ENTERPRISE_MAX`, `LOCAL_SMG_MAX` | `update_whole_team_map.py` |
| Change the **pod-aligned** view (seats, who sits in them) | `POD_ASSIGNED`, `REGION_SHAPE`, `pod_seat()` | `update_whole_team_map.py` |
| Change an **AE's territory** | `ae_territories.csv` | `update_ae_territories.py` |
| Change a **state's** purchasing access, IT signal, etc. | `state_overlay.csv` | `build_tiering.py` → `inject_html.py` |
| Change **growth-tier weights** | `W_STATE_SIDE`, `W_LOCAL_SIDE`, bands, blend in `build_tiering.py` | `build_tiering.py` → `inject_html.py` |

All scripts run from the project root, e.g. `python3 tiering/update_whole_team_map.py`.

---

## Why an override didn't stick: the order rules run in

`update_whole_team_map.py` applies these in order for every account. **A later step overwrites an
earlier one.** `account_overrides.csv` runs second, so almost everything below it can overrule it.

1. Nathan Williamson's accounts → Jr Wycinsky.
2. **`account_overrides.csv`** — segment change, then `new_xp`.
3. `AE_OWNER` — the whole AE group goes to its fixed XP.
4. Bill Anderson's Texas accounts → `BILL_ANDERSON_TEXAS_XP` (Paige).
5. NY and NJ **State** accounts → `NY_NJ_STATE_XP` (Taylor).
6. North Dakota → Carolina Prieto; sister agencies become allocated children.
7. Kentucky **State** → `KY_STATE_XP` (Andy); anything not in `KY_COUNTABLE` becomes an allocated child.
8. `remove = yes` rows are dropped.
9. New pipeline logos from `fy2027_pipeline.csv` are added.
10. **Every Local SMG account** is reassigned by `local_smg_destination()`. `new_xp` on a Local SMG account is always ignored.
11. Tatiana enterprise rule (`TATIANA_ENTERPRISE_AES`, `TATIANA_ENTERPRISE_ACCOUNTS`).
12. Validations. Any failure stops the run and nothing is written.

In practice, a `new_xp` override only works when the account is Enterprise **and** none of steps 3–7
or 11 apply to it. When one does, the script now prints:

```
OVERRIDES IGNORED (2): new_xp in account_overrides.csv was overruled. Change the named rule instead:
  Ocala, FL: asked for Natalia Sanchez, got Ricardo Castro — set by Local SMG cut (...)
```

Fix those by changing the named rule, or delete the override row since it does nothing.

---

## Recipes by account type

**State or Local ENT account, AE not in any group rule.** Add a row to `account_overrides.csv`:

```
account,new_xp,new_segment,remove,note
"Albuquerque, NM",Colleen Moran,,,Why it moved
```

The name must match the page exactly, including punctuation. Quote any name containing a comma.
(`Connecticut Public Utilities Regulatory Authority [PURA],` really does end in a comma.)

**An account whose AE is in `AE_OWNER`.** The override is ignored. Either move the whole group by
changing the `AE_OWNER` line, or remove the AE from `AE_OWNER` and then use overrides for each account.
Removing an AE from `AE_OWNER` also removes the check that keeps that group together.

**Local SMG account.** Destinations are set per AE group, not per account:

- Most groups: `LOCAL_SMG_DESTINATION["<AE>"] = "<XP>"`.
- California: Carlos keeps what he holds today plus North/Central; accounts named in
  `SOUTHERN_CA_LOCAL_SMG` go to Marcy. Add or remove names there.
- Florida Ter 4: names in `SE_MM_SOUTH_FL` go to Natalia; the rest go to Ricardo.
- Luke Mulvaney: Texas → Luis, everything else → Eduardo (inside `local_smg_destination()`).

A Local SMG XP must be in `LOCAL_SMG_XPS`, must end up with at least one account, stays under
`LOCAL_SMG_MAX` (30), and keeps complex accounts (more than 7 capabilities) at a third of the book or less.

**Moving an account between Enterprise and Local SMG.** Set `new_segment` to `State`, `Local ENT` or
`Local SMG`. Moving to Local SMG hands the account to the Local SMG cut (step 10). Its AE must have an
entry in `LOCAL_SMG_DESTINATION`, or the run fails with "No Local SMG destination for AE group".

**Statewide enterprise agreements (Kentucky COT, North Dakota ITD).** The parent is countable; sister
agencies ride along as allocated $0 children. To make a Kentucky agency count toward the book, add
it to `KY_COUNTABLE`. For North Dakota, edit `carolina_countable` in `apply_assignments`.

**New logo from pipeline.** Add a row to `fy2027_pipeline.csv` with `in_us_book = yes`, a `tier`,
and an `ae` who already has accounts on the map. The XP comes from `AE_OWNER` if the AE is in it,
Taylor for NY/NJ, otherwise the `xp` column. A name already on the map is treated as expansion:
`nnarr` is added to its proposed ARR and nothing else changes.

**Federal and DC.** Every federal account is in DC and sits on the Federal pod seat with Jr
Wycinsky. District of Columbia is a Paige hold in every view (`PAIGE_DC`).

**Pod-aligned view.** It ignores current and proposed owners completely. Accounts go to a seat by
state and segment (`pod_seat()`), and each seat has one XP in `POD_ASSIGNED`. Overrides do not
touch it. US-based XPs must be within one hour of every state on their seat (`US_XP_TZ`).
The seat count per region is fixed in `REGION_SHAPE`. California's three midmarket seats are North
(Carlos), LA/Orange (Marcy) and San Diego/Inland (open, the names in `SD_INLAND_CA_LOCAL_SMG`).
Holds in `pod_seat()` keep the same person across proposed and pod for Kent Hartsfield → Steffany
(Cook County and the Ohio group), Andrew Wyzkoski → Halena (Pennsylvania), and Washington state
agencies → Paige (with DC).

---

## Run order after a batch of edits

```
python3 tiering/build_tiering.py          # only if the workbook, overlay or weights changed
python3 tiering/inject_html.py            # only after build_tiering
python3 tiering/update_workbook.py        # only if you want the xlsx refreshed too
python3 tiering/update_whole_team_map.py  # assignments, pipeline, pods
python3 tiering/update_ae_territories.py  # last: it checks AEs against the final book
```

Read the console output. It lists every moved account, ignored overrides, book sizes against the
caps, and Local SMG loads per XP.

---

## Gotchas

- **Overrides are sticky.** The script edits `index.html` in place and reads its own previous output
  next time. Deleting an override row does **not** put the account back. To reverse a move, change
  the row to name the XP you want now.
- **`remove = yes` is permanent** for the same reason. The account is gone from the page. To bring it
  back, restore `index.html` from version control and re-run.
- **Pipeline rows are sticky too.** Removing one from `fy2027_pipeline.csv` leaves the logo or the
  `fy27` ARR on the page.
- **Keep a copy of `index.html` before running.** A failed run writes nothing, but a successful run
  with a wrong rule overwrites the page.
- **Growth tiers come from the workbook, not the page.** Moving an account never changes its tier.
  The tier is a property of the account and state, rebuilt only by `build_tiering.py`.
- `ae_territories.csv` needs a row for every AE on the map. Adding a pipeline logo under a new AE
  name will make `update_ae_territories.py` fail until that row exists.

## Common errors

| Message | Meaning / fix |
|---|---|
| `Override accounts not found in the map` | Name in `account_overrides.csv` doesn't exactly match the page. Check punctuation and trailing commas. |
| `No Local SMG destination for AE group 'X'` | A Local SMG account's AE has no line in `LOCAL_SMG_DESTINATION`. Add one. |
| `Enterprise books above the 20-account maximum` | Someone's countable Enterprise book exceeds `ENTERPRISE_MAX`. Move accounts off, or raise the cap. |
| `Local SMG books above the 30-account cap` / `one-third complex-account ceiling` | Rebalance `LOCAL_SMG_DESTINATION` or the CA/FL lists. |
| `<XP> still has proposed accounts` | Someone in `NO_BOOK` was assigned an account, usually through an override or `AE_OWNER`. |
| `<AE> accounts not with <XP>` | An `AE_OWNER` group got split. Usually a later rule (NY/NJ, Kentucky, Tatiana) collided with it. |
| `Carolina Prieto has unexpected countable accounts` | Something outside Idaho/North Dakota landed on Carolina. Add it to `CAROLINA_BEYOND_ID_ND` if intentional. |
| `<XP> (TZ) is more than an hour from <state>` | Pod seat breaks the timezone rule. Fix `POD_ASSIGNED` or `pod_seat()`. |
| `AEs on the map with no row in ae_territories.csv` | Add the AE to `ae_territories.csv`. |
