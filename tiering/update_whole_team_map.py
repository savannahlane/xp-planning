#!/usr/bin/env python3
"""Apply the whole-team assignment corrections to index.html.

This script is intentionally narrow. It starts from the whole-team PAGE payload
that landed on main and changes only the proposed assignment (`newxp`):

* Jake Sager is a VP. Savannah Lane, Kristen Murphy and Ashley Hill are
  managers. None of the four holds a proposed account book.
* Nathan Williamson has left the team. His federal accounts sit with Jr
  Wycinsky in both the current and proposed views.
* Ashley's seven current Enterprise accounts land with direct reports.
* Enterprise XPs carry no Local SMG accounts. Nine dedicated Local SMG XPs
  cover whole AE groups except the forced California and transportation splits.
* Carolina Prieto is labelled Team Lead, not Manager. She keeps only the Idaho
  and North Dakota state book (Scott Mark, including the ND enterprise agreement).
  Kentucky state, including the COT enterprise agreement, sits with Andy O'Brien.
* `podxp` is a third view. It staffs pods from the account's state and segment
  and does not change `cur` or `newxp`.

Per-account moves live in account_overrides.csv, which is the file to edit when
an XP changes. It also carries segment changes and removals.

The current-assignment (`cur`) field is historical and is not rewritten,
except where Nathan Williamson still held an account: he has left, so those
rows move to Jr Wycinsky.
"""

from __future__ import annotations

import csv
import io
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"
OVERRIDES = Path(__file__).resolve().parent / "account_overrides.csv"
PIPELINE = Path(__file__).resolve().parent / "fy2027_pipeline.csv"

NO_BOOK = {
    "Jake Sager",
    "Nathan Williamson",
    "Savannah Lane",
    "Kristen Murphy",
    "Ashley Hill",
}
ASHLEY_REPORTS = {
    "Open XP2 (PT)",
    "Colleen Moran",
    "Cody Nichols",
    "Steffany Amador",
    "Marcy Castro",
    "Alejandro Solano",
}

# Canonical Local SMG books. Whole AE groups stay together wherever possible:
# California Local SMG is two books, not three. Carlos keeps every CA account
# he holds today and the rest of the North/Central seat (Jaxon Sher). Marcy
# keeps the rest of Tier 8, the southern list, including Jaxson McBride's
# water account. That puts Carlos over the cap if he also keeps his northeast
# groups, so those groups move whole to Eduardo. Florida Tier 4 splits the
# same way the pod does: Natalia keeps South Florida, Ricardo takes the
# north and central remainder on top of Alejandro's southeast accounts.
# Luke Mulvaney's Texas account follows Luis; New Jersey and Oregon follow
# the rest of Carlos's former northeast book to Eduardo.
LOCAL_SMG_DESTINATION = {
    "Local SMG Ter 6 (TX/OK/AR)": "Luis Aguilar",
    "Caleb Fort Jr": "Ricardo Castro",
    "Corey Andrade": "Eduardo Ruiz",
    "Emery Herrschel": "Kerrian Dailey",
    "Jared Cummings": "Kerrian Dailey",
    "Jeffrey Johnson": "David Treminio",
    "Kimberley Steelmann": "Andrés Pérez",
    "Amanda Brooks": "David Treminio",
    "Andrew Collinsworth": "Ricardo Castro",
    "Tommy Monaghan": "Eduardo Ruiz",
    "Brittany Greer": "Kerrian Dailey",
    "John Meah": "Ricardo Castro",
    "Not on maps provided": "Andrés Pérez",
    "Prachi Patel": "Eduardo Ruiz",
    "Michelle Cooper seat (open)": "Luis Aguilar",
}

LOCAL_SMG_XPS = {
    "Andrés Pérez",
    "Carlos Torres",
    "David Treminio",
    "Eduardo Ruiz",
    "Kerrian Dailey",
    "Luis Aguilar",
    "Marcy Castro",
    "Natalia Sanchez",
    "Ricardo Castro",
}

# Southern half of the California Tier 8 placeholder (LA, Orange County, San
# Diego and the inland south). Everything else in CA Local SMG is the
# North/Central seat, Jaxon Sher's book. Carlos's own southern accounts are
# named in the assignment function so they stay with him.
SOUTHERN_CA_LOCAL_SMG = {
    "Bell, CA",
    "Brawley CA",
    "Burbank CA",
    "Chino Valley Independent Fire District",
    "Coachella, CA",
    "Culver City, CA",
    "Eastvale CA",
    "El Monte, CA",
    "Encinitas, CA",
    "Fullerton, CA",
    "Hesperia, CA",
    "Imperial Irrigation District",
    "La Puente, CA",
    "Laguna Beach, CA",
    "Manhattan Beach, CA",
    "Metropolitan Water District of Southern California",
    "Newport Beach, CA",
    "Ontario International Airport",
    "Orange, CA",
    "Palm Springs, CA",
    "Pasadena, CA",
    "Perris, CA",
    "Rancho Santa Margarita, CA",
    "San Diego State University",
    "Santa Margarita Water District",
    "South Coast Water District",
    "Tustin, CA",
    "Victorville, CA",
    "Vista, CA",
    "Westminster, CA",
}

# Tatiana takes Marcy's enterprise book. These AE groups sit entirely with
# Marcy. David Cliff and the Farnham seat do not, so only their Marcy accounts
# are named.
TATIANA_ENTERPRISE_AES = {"Bettsy Desjarlais", "Bill Pintsak", "Chris Thiers"}
TATIANA_ENTERPRISE_ACCOUNTS = {
    "Jackson County MO",
    "Kansas City, MO, Police Department",
    "Ohio Workers' Compensation Bureau",
}

# North Dakota ITD is the billed parent of a statewide enterprise agreement.
# Sister agency rows travel with it and do not consume a countable slot.
# Kentucky COT is the same pattern, but that estate sits with Andy O'Brien.
ND_PARENT = "North Dakota Information Technology Department"
KY_PARENT = "Kentucky Commonwealth Office of Technology"
KY_STATE_XP = "Andy O'Brien"
# Countable Kentucky state accounts. Everything else on the Kentucky estate is
# an allocated child of COT, including the Tourism cabinet private-sector row.
KY_COUNTABLE = {
    KY_PARENT,
    "Kentucky Cabinet for Health & Family Services (CHFS)",
    "Kentucky Office of Homeland Security",
    "Kentucky Transportation Cabinet",
}

ENTERPRISE_SEGMENTS = {"State", "Local ENT"}

# Book size caps, counting countable accounts only.
ENTERPRISE_TARGET = 17
ENTERPRISE_MAX = 20
LOCAL_SMG_MAX = 30

# Whole AE groups that always sit with one XP, regardless of who held them.
AE_OWNER = {
    "Scott Mark": "Carolina Prieto",
    "Stephanie DelSignore": "Halena Martin",
    "Demi Washington": "Carolina Cambronero",
    "Desmond Davis": "Carolina Cambronero",
    "Bill Marshall": "Carolina Cambronero",
    "Sarah Duncan": "Taylor Roman",
    # Spencer's AL/GA locals sit with Taylor, who already holds Sarah Duncan's
    # AL/GA state book, rather than splitting the two Georgia AEs across XPs.
    "Spencer Ferrell": "Taylor Roman",
    # Steffany already holds San Antonio and VIA from this Texas SAM group.
    # Consolidating the remaining four accounts with her removes one AE split.
    "Cedric Simpkins": "Steffany Amador",
    # Gil Roy's Texas accounts join his Louisiana accounts with Cambronero, so
    # the whole SAM group sits with one XP and Steffany has room for Kent.
    "Gil Roy": "Carolina Cambronero",
    # After the Marcy swap on main, Territory 4a continues to Taylor with the
    # rest of the NY/NJ local-and-state book rather than remaining a Midwest
    # attachment.
    "Territory 4a (open)": "Taylor Roman",
    # Kent's T11b OH/IN/IL territory and the temporary Chicago/Columbus SAM
    # accounts sit together with Steffany, who keeps Cook County and Cleveland,
    # rather than splitting the AE group.
    "Kent Hartsfield": "Steffany Amador",
}

# Bill Anderson's Texas state accounts sit with Paige, who already holds his
# Washington accounts. His California accounts stay with the open Pacific XP.
BILL_ANDERSON_TEXAS_XP = "Paige Wendle"

# Current Ashley Hill Enterprise accounts that may leave her reporting line.
# Name any exception here so it is deliberate rather than silent drift. Columbus
# no longer needs one: it sits with Steffany, who reports to Ashley.
ASHLEY_HOLD_RELEASED: set[str] = set()

# New York and New Jersey state agencies sit with Taylor, including the
# DelSignore rows that would otherwise follow the AE_OWNER rule above.
NY_NJ_STATE_XP = "Taylor Roman"

# Carolina keeps the Scott Mark group, which is otherwise Idaho and North
# Dakota. This committed logo is the first account on his mapped Wyoming
# territory, so it stays with that AE rather than opening a second XP.
CAROLINA_BEYOND_ID_ND = {"Wyoming Department of Environmental Quality"}

# Pod aligned ignores who holds the accounts today. Accounts follow the state
# into a regional seat, then the seat is named with an XP.
#
# US staff have to sit within one hour of every account on the seat. Costa Rica
# staff have no timezone requirement. All nine dedicated midmarket XPs are in
# Costa Rica. A seat stays Open when no remaining XP fits.
US_XP_TZ = {
    "Colleen Moran": "PT",
    "Paige Wendle": "MT",
    "Taylor Roman": "ET",
    "Steffany Amador": "ET",
    "Brooke Minichino": "ET",
    "Andy O'Brien": "ET",
    "Halena Martin": "ET",
    "Open XP2 (PT)": "PT",
}
CR_XPS = LOCAL_SMG_XPS | {
    "Cody Nichols",
    "Tatiana Montero",
    "Alejandro Solano",
    "Carolina Cambronero",
}
TZ_OFFSET = {"AKT": -9, "PT": -8, "MT": -7, "CT": -6, "ET": -5}
STATE_TZ = {
    "CT": "ET", "DE": "ET", "DC": "ET", "FL": "ET", "GA": "ET", "IN": "ET",
    "KY": "ET", "ME": "ET", "MD": "ET", "MA": "ET", "MI": "ET", "NH": "ET",
    "NJ": "ET", "NY": "ET", "NC": "ET", "OH": "ET", "PA": "ET", "RI": "ET",
    "SC": "ET", "VT": "ET", "VA": "ET", "WV": "ET",
    "AL": "CT", "AR": "CT", "IL": "CT", "IA": "CT", "KS": "CT", "LA": "CT",
    "MN": "CT", "MS": "CT", "MO": "CT", "NE": "CT", "ND": "CT", "OK": "CT",
    "SD": "CT", "TN": "CT", "TX": "CT", "WI": "CT",
    "AZ": "MT", "CO": "MT", "ID": "MT", "MT": "MT", "NM": "MT", "UT": "MT",
    "WY": "MT",
    "CA": "PT", "NV": "PT", "OR": "PT", "WA": "PT",
    "AK": "AKT", "HI": "HT",
}
# District of Columbia is a Paige hold in every view, including pod aligned.
PAIGE_DC = "District of Columbia"
STATE_SAM_SEAT = {
    "Bill Anderson": "SAM · Bill Anderson",
    "State SAM – Farnham seat (open)": "SAM · Farnham",
    "Gil Roy": "SAM · Gil Roy",
    "Benjamin Shor": "SAM · Benjamin Shor",
}

# Gil Roy is the Texas State SAM. His own Louisiana accounts stay on the same
# seat. Texas rows still filed under Bill Anderson, and the unconfirmed Texas
# State SAM, move here with him.
def on_gil_roy_sam(row: dict) -> bool:
    if row["segment"] == "Local SMG":
        return False
    if row["person"] in {"Gil Roy", "TX State SAM (unconfirmed)"}:
        return True
    return row["person"] == "Bill Anderson" and row["state"] == "TX"

# seat id, XP, role, card label, territory filter. Open seats have no XP who fits.
# Cards are seats, not people: Andy holds both Mid-Atlantic enterprise seats and
# they stay separate. Halena holds New England. Steffany holds Ohio, Indiana and
# Pennsylvania, which is where Columbus sits.
POD_ASSIGNED = [
    ("SAM · Bill Anderson", "Alejandro Solano", "SAM", "State SAM · CA/WA", "State SAM · CA/WA"),
    ("SAM · Farnham", "Open · SAM Farnham", "SAM", "State SAM · Farnham", "State SAM · Farnham"),
    ("SAM · Gil Roy", "Carolina Cambronero", "SAM", "State SAM · TX", "State SAM · TX"),
    ("SAM · Benjamin Shor", "Brooke Minichino", "SAM", "State SAM · MD/NY", "State SAM · MD/NY"),
    ("Northwest ENT", "Colleen Moran", "ENT", "Northwest · ENT", "Northwest"),
    ("Northwest MM", "Open · Northwest MM", "MM", "Northwest · MM", "Northwest"),
    ("Northeast ENT · New England", "Halena Martin", "ENT", "New England · ENT", "Northeast"),
    ("Northeast ENT · OH/IN/PA", "Steffany Amador", "ENT", "Ohio/Indiana/Pennsylvania · ENT", "Northeast"),
    ("Northeast MM", "Eduardo Ruiz", "MM", "Northeast · MM", "Northeast"),
    ("California MM · South", "Marcy Castro", "MM", "California · South", "California"),
    ("California MM · North", "Carlos Torres", "MM", "California · North", "California"),
    ("California ENT", "Open XP2 (PT)", "ENT", "California · ENT", "California"),
    ("Southwest ENT", "Cody Nichols", "ENT", "Southwest · ENT", "Southwest"),
    ("Southwest MM", "David Treminio", "MM", "Southwest · MM", "Southwest"),
    ("Mountain Plains ENT", "Paige Wendle", "ENT", "Mountain Plains · ENT", "Mountain Plains"),
    ("Mountain Plains MM", "Open · Mountain Plains MM", "MM", "Mountain Plains · MM", "Mountain Plains"),
    ("Texas ENT", "Open · Texas ENT", "ENT", "Texas · ENT", "Texas"),
    ("Texas MM", "Luis Aguilar", "MM", "Texas · MM", "Texas"),
    ("Great Lakes ENT", "Tatiana Montero", "ENT", "Great Lakes · ENT", "Great Lakes"),
    ("Great Lakes MM · Illinois", "Andrés Pérez", "MM", "Illinois · MM", "Great Lakes"),
    ("Great Lakes MM · Upper Midwest", "Kerrian Dailey", "MM", "Upper Midwest · MM", "Great Lakes"),
    ("Southeast ENT", "Taylor Roman", "ENT", "Southeast · ENT", "Southeast"),
    ("Southeast MM · South FL", "Natalia Sanchez", "MM", "South Florida · MM", "Southeast"),
    ("Southeast MM · North FL", "Ricardo Castro", "MM", "North Florida · MM", "Southeast"),
    ("Southeast MM · GA/LA/SC", "Ricardo Castro", "MM", "Georgia/Louisiana/SC · MM", "Southeast"),
    ("Mid-Atlantic ENT · MD/VA/NC", "Andy O'Brien", "ENT", "Mid-Atlantic · MD/VA/NC", "Mid-Atlantic"),
    ("Mid-Atlantic ENT · KY/TN", "Andy O'Brien", "ENT", "Mid-Atlantic · KY/TN", "Mid-Atlantic"),
    ("Mid-Atlantic MM", "Open · Mid-Atlantic MM", "MM", "Mid-Atlantic · MM", "Mid-Atlantic"),
    ("Federal", "Jr Wycinsky", "Federal", "Federal", "Federal"),
]
# The recommended regional shape. The written "24" is one short of this list.
REGION_SHAPE = {
    "Northwest": {"ENT": 1, "MM": 1},
    "Northeast": {"ENT": 2, "MM": 1},
    "California": {"ENT": 1, "MM": 2},
    "Southwest": {"ENT": 1, "MM": 1},
    "Mountain Plains": {"ENT": 1, "MM": 1},
    "Texas": {"ENT": 1, "MM": 1},
    "Great Lakes": {"ENT": 1, "MM": 2},
    "Southeast": {"ENT": 1, "MM": 3},
    "Mid-Atlantic": {"ENT": 2, "MM": 1},
}
SEAT_XP = {seat: xp for seat, xp, _role, _label, _terr in POD_ASSIGNED}
SEAT_ROLE = {seat: role for seat, _xp, role, _label, _terr in POD_ASSIGNED}
SEAT_TERR = {seat: terr for seat, _xp, _role, _label, terr in POD_ASSIGNED}
# Names published by the first pod view. Drop them once seats are people.
RETIRED_POD_NAMES = {
    "SAM · Bill Anderson",
    "SAM · Farnham",
    "SAM · Gil Roy",
    "SAM · Benjamin Shor",
    "Northwest ENT",
    "Northwest MM",
    "Northeast ENT · New England",
    "Northeast ENT · OH/IN/PA",
    "Northeast MM",
    "California MM · LA/OC",
    "California MM · SD/Inland",
    "California MM · South",
    "California MM · North",
    "Open · California SD/Inland",
    "Open · North Florida MM",
    "California ENT · uncovered",
    "California ENT",
    "Southwest ENT",
    "Southwest MM",
    "Mountain Plains ENT",
    "Mountain Plains MM",
    "Texas ENT",
    "Texas MM",
    "Great Lakes ENT",
    "Great Lakes MM · Illinois",
    "Great Lakes MM · Upper Midwest",
    "Southeast ENT",
    "Southeast MM · South FL",
    "Southeast MM · North FL",
    "Southeast MM · GA/LA/SC",
    "Mid-Atlantic ENT · MD/VA/NC",
    "Mid-Atlantic ENT · KY/TN",
    "Mid-Atlantic ENT",
    "Mid-Atlantic MM",
    "Federal",
    "Open · Northeast ENT",
}

# Two enterprise seats in a region keep whole states together.
NORTHEAST_ENT_NEW_ENGLAND = {"ME", "NY", "NJ", "DE", "MA", "RI", "VT", "CT", "NH"}
NORTHEAST_ENT_OHIO = {"PA", "OH", "IN"}
MID_ATLANTIC_ENT_COAST = {"MD", "VA", "WV", "NC"}
MID_ATLANTIC_ENT_INLAND = {"AR", "TN", "KY"}
COLUMBUS = "Columbus OH"

# California midmarket is two seats. The southern list is Tier 8 outside
# Jaxon Sher's North/Central book. North is everything else in the state.

# Southeast midmarket is three seats. South Florida is named; the rest of
# Florida is the north seat; Georgia, Louisiana, Alabama and South Carolina
# are the third seat.
SE_MM_SOUTH_FL = {
    "Aventura, FL",
    "Boca Raton, FL",
    "Coral Gables, FL",
    "Delray Beach, FL",
    "Doral, FL",
    "Hallandale Beach, FL",
    "Miramar, FL",
    "Palmetto Bay, FL",
    "Pembroke Pines, FL",
    "Pinecrest, FL",
    "Sunrise, FL",
    "Tamarac, FL",
    "West Palm Beach, FL",
    "Weston, FL",
}

def pod_seat(row: dict) -> str:
    """Return the pod seat id for one account. Ignores current and proposed owners."""
    if row["acct"] == PAIGE_DC:
        return "Mountain Plains ENT"
    if row["segment"] == "Federal" or not row.get("state"):
        return "Federal"
    if on_gil_roy_sam(row):
        return "SAM · Gil Roy"
    if row["person"] in STATE_SAM_SEAT:
        return STATE_SAM_SEAT[row["person"]]
    state = row["state"]
    mm = row["segment"] == "Local SMG"
    if state in {"WA", "OR", "AK"}:
        return "Northwest MM" if mm else "Northwest ENT"
    if state in NORTHEAST_ENT_NEW_ENGLAND | NORTHEAST_ENT_OHIO:
        if mm:
            return "Northeast MM"
        if state in NORTHEAST_ENT_NEW_ENGLAND:
            return "Northeast ENT · New England"
        return "Northeast ENT · OH/IN/PA"
    if state == "CA":
        if not mm:
            return "California ENT"
        if row["acct"] in SOUTHERN_CA_LOCAL_SMG:
            return "California MM · South"
        return "California MM · North"
    if state in {"NV", "UT", "CO", "NM", "AZ"}:
        return "Southwest MM" if mm else "Southwest ENT"
    if state in {"ID", "WY", "MT", "SD", "ND", "NE", "KS", "OK"}:
        return "Mountain Plains MM" if mm else "Mountain Plains ENT"
    if state == "TX":
        return "Texas MM" if mm else "Texas ENT"
    if state in {"MN", "WI", "IA", "MO", "IL", "MI"}:
        if not mm:
            return "Great Lakes ENT"
        return "Great Lakes MM · Illinois" if state == "IL" else "Great Lakes MM · Upper Midwest"
    if state in {"LA", "FL", "MS", "AL", "GA", "SC"}:
        if not mm:
            return "Southeast ENT"
        if state != "FL":
            return "Southeast MM · GA/LA/SC"
        if row["acct"] in SE_MM_SOUTH_FL:
            return "Southeast MM · South FL"
        return "Southeast MM · North FL"
    if state in MID_ATLANTIC_ENT_COAST | MID_ATLANTIC_ENT_INLAND:
        if mm:
            return "Mid-Atlantic MM"
        if state in MID_ATLANTIC_ENT_COAST:
            return "Mid-Atlantic ENT · MD/VA/NC"
        return "Mid-Atlantic ENT · KY/TN"
    raise RuntimeError(
        f"No pod for {row['acct']!r} ({row['state']}, {row['segment']}, {row['person']})"
    )


def assign_pods(page: dict, rows: list[dict]) -> dict[str, int]:
    """Staff podxp from geography, then name the XP on the seat."""
    for retired in RETIRED_POD_NAMES:
        page["meta"].pop(retired, None)
    page["order"] = [xp for xp in page["order"] if xp not in RETIRED_POD_NAMES]
    open_names = [xp for _seat, xp, _role, _label, _terr in POD_ASSIGNED if xp.startswith("Open ·")]
    page["order"] = [xp for xp in page["order"] if xp not in open_names]
    for key in list(page["meta"]):
        if key.startswith("Open ·") and key not in open_names:
            page["meta"].pop(key, None)
    shape: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for seat, _xp, role, _label, terr in POD_ASSIGNED:
        if role in {"ENT", "MM"}:
            shape[terr][role] += 1
    if {terr: dict(roles) for terr, roles in shape.items()} != REGION_SHAPE:
        raise RuntimeError(f"Pod seats do not match the recommendation: { {t: dict(r) for t, r in shape.items()} }")
    if sum(1 for _s, _x, role, _l, _t in POD_ASSIGNED if role == "SAM") != 4:
        raise RuntimeError("State SAMs must be 4 seats")
    pod_order = []
    pod_label = {}
    pod_role = {}
    pod_xp = {}
    territories = []
    for seat, xp, role, label, terr in POD_ASSIGNED:
        if seat in pod_label:
            raise RuntimeError(f"Duplicate pod seat {seat}")
        pod_order.append(seat)
        pod_label[seat] = label
        pod_role[seat] = role
        pod_xp[seat] = xp
        if terr not in territories:
            territories.append(terr)
        if xp.startswith("Open ·"):
            page["meta"][xp] = ["—", "n/a", "Open", label]
            page["order"].append(xp)
    page["podOrder"] = pod_order
    page["podLabel"] = pod_label
    page["podRole"] = pod_role
    page["podXp"] = pod_xp
    page["territories"] = territories

    named_ca = SOUTHERN_CA_LOCAL_SMG
    ca_smg = {
        r["acct"]
        for r in rows
        if r["state"] == "CA" and r["segment"] == "Local SMG" and not r["alloc"]
    }
    missing_ca = sorted(named_ca - ca_smg)
    if missing_ca:
        raise RuntimeError(
            "California midmarket cut names accounts that are not CA Local SMG: "
            + ", ".join(missing_ca)
        )
    fl_smg = {
        r["acct"]
        for r in rows
        if r["state"] == "FL" and r["segment"] == "Local SMG" and not r["alloc"]
    }
    missing_fl = sorted(SE_MM_SOUTH_FL - fl_smg)
    if missing_fl:
        raise RuntimeError(
            "South Florida cut names accounts that are not FL Local SMG: "
            + ", ".join(missing_fl)
        )

    load: dict[str, int] = defaultdict(int)
    seat_states: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        seat = pod_seat(row)
        xp = SEAT_XP[seat]
        row["podseat"] = seat
        row["podxp"] = xp
        row["podterr"] = SEAT_TERR[seat]
        if row["alloc"]:
            continue
        role = SEAT_ROLE[seat]
        if role == "MM" and row["segment"] != "Local SMG":
            raise RuntimeError(f"{row['acct']} is {row['segment']} on midmarket seat {seat}")
        if role in {"ENT", "SAM"} and row["segment"] == "Local SMG":
            raise RuntimeError(f"{row['acct']} is Local SMG on {seat}")
        if role == "Federal" and row["segment"] != "Federal":
            raise RuntimeError(f"{row['acct']} is {row['segment']} on the Federal seat")
        if row["segment"] == "Federal" and row["acct"] != PAIGE_DC and role != "Federal":
            raise RuntimeError(f"{row['acct']} is federal but not on the Federal seat")
        if role == "SAM":
            if seat == "SAM · Gil Roy":
                if not on_gil_roy_sam(row):
                    raise RuntimeError(f"{row['acct']} on Gil Roy's Texas SAM belongs to {row['person']}")
            else:
                owner = next(person for person, sam_seat in STATE_SAM_SEAT.items() if sam_seat == seat)
                if row["person"] != owner:
                    raise RuntimeError(f"{row['acct']} on {seat} belongs to {row['person']}")
        if row.get("state"):
            seat_states[seat].add(row["state"])
        load[seat] += 1

    missing = [seat for seat in pod_order if seat not in load]
    if missing:
        raise RuntimeError("Pod seats with no countable accounts: " + ", ".join(missing))
    if PAIGE_DC not in {r["acct"] for r in rows if r["podxp"] == "Paige Wendle"}:
        raise RuntimeError("District of Columbia is not on Paige Wendle's pod seat")
    columbus = [r for r in rows if r["acct"] == COLUMBUS and not r["alloc"]]
    if len(columbus) != 1 or columbus[0]["podxp"] != "Steffany Amador" or columbus[0]["podseat"] != "Northeast ENT · OH/IN/PA":
        raise RuntimeError("Columbus is not on Steffany Amador's Ohio seat in the pod model")
    if pod_xp["Northeast ENT · New England"] != "Halena Martin":
        raise RuntimeError("New England is not Halena Martin's seat")

    unverified = []
    for seat, states in sorted(seat_states.items()):
        xp = SEAT_XP[seat]
        if xp in CR_XPS or xp.startswith("Open") or SEAT_ROLE[seat] == "Federal":
            continue
        if xp not in US_XP_TZ:
            unverified.append(xp)
            continue
        xp_off = TZ_OFFSET[US_XP_TZ[xp]]
        for state in sorted(states):
            if xp == "Paige Wendle" and state == "DC":
                continue
            state_tz = STATE_TZ.get(state)
            if state_tz not in TZ_OFFSET:
                raise RuntimeError(f"No timezone for {state} on {xp}'s pod seat")
            if abs(xp_off - TZ_OFFSET[state_tz]) > 1:
                raise RuntimeError(
                    f"{xp} ({US_XP_TZ[xp]}) is more than an hour from {state} ({state_tz})"
                )
    page["podUnverified"] = unverified
    return dict(load)


def load_overrides(path: Path) -> dict[str, dict]:
    """Read the per-account override table, ignoring the comment header."""
    body = "\n".join(
        line for line in path.read_text().splitlines() if not line.startswith("#")
    )
    overrides: dict[str, dict] = {}
    for record in csv.DictReader(io.StringIO(body)):
        account = (record["account"] or "").strip()
        if not account:
            continue
        if account in overrides:
            raise RuntimeError(f"Duplicate override row for {account!r}")
        segment = (record["new_segment"] or "").strip()
        if segment and segment not in ENTERPRISE_SEGMENTS | {"Local SMG"}:
            raise RuntimeError(f"Unknown segment {segment!r} for {account!r}")
        overrides[account] = {
            "xp": (record["new_xp"] or "").strip(),
            "segment": segment,
            "remove": (record["remove"] or "").strip().lower() in {"yes", "true", "1"},
        }
    return overrides


def extract_page(source: str) -> tuple[dict, int, int]:
    start = source.index("const PAGE = ") + len("const PAGE = ")
    end = source.index(";\nconst ROWS_ALL", start)
    return json.loads(source[start:end]), start, end


def proposed_edges(rows: list[dict]) -> set[tuple[str, str]]:
    return {(r["newxp"], r["person"]) for r in rows if r.get("newxp")}


def load_pipeline(path: Path) -> list[dict]:
    """Read the FY2027 committed-pipeline extract."""
    body = "\n".join(
        line for line in path.read_text().splitlines() if not line.startswith("#")
    )
    pipeline = []
    for record in csv.DictReader(io.StringIO(body)):
        account = (record["account"] or "").strip()
        if not account:
            continue
        included = (record["in_us_book"] or "").strip().lower()
        if included not in {"yes", "no"}:
            raise RuntimeError(f"{account!r} must set in_us_book to yes or no")
        try:
            nnarr = float(record["nnarr"])
        except ValueError as exc:
            raise RuntimeError(f"{account!r} has no numeric nnarr") from exc
        tier = (record["tier"] or "").strip()
        pipeline.append(
            {
                "account": account,
                "state": (record["state"] or "").strip().upper(),
                "ae": (record["ae"] or "").strip(),
                "xp": (record["xp"] or "").strip(),
                "tier": int(tier) if tier else None,
                "nnarr": nnarr,
                "included": included == "yes",
                "note": (record["note"] or "").strip(),
            }
        )
    return pipeline


def apply_pipeline(rows: list[dict], pipeline: list[dict]) -> dict:
    """Add FY2027 pipeline without double-counting it on a later run.

    New logos enter the proposed book only. Expansion on an account that is
    already in the book stays in `fy27` and the page adds it to proposed ARR.
    """
    by_name = {row["acct"]: row for row in rows}
    added = []
    expanded = []
    for record in pipeline:
        if not record["included"]:
            continue
        existing = by_name.get(record["account"])
        label = f"FY2027 committed pipeline ${record['nnarr']:,.0f}"
        if record["note"]:
            label += f" · {record['note']}"
        if existing:
            existing["fy27"] = record["nnarr"]
            if label not in (existing.get("flag") or ""):
                existing["flag"] = (
                    f"{existing['flag']} · {label}" if existing.get("flag") else label
                )
            expanded.append(record)
            continue
        if record["tier"] not in {1, 2, 3, 4}:
            raise RuntimeError(f"{record['account']!r} needs a tier")
        siblings = [row for row in rows if row["person"] == record["ae"]]
        if not siblings:
            raise RuntimeError(
                f"{record['account']!r} names AE {record['ae']!r}, who is not on the map"
            )
        xp = AE_OWNER.get(record["ae"], record["xp"])
        if record["state"] in {"NY", "NJ"}:
            xp = NY_NJ_STATE_XP
        if not xp:
            raise RuntimeError(f"{record['account']!r} has no proposed XP")
        row = {
            "acct": record["account"],
            "state": record["state"],
            "segment": "State",
            "side": "State",
            "person": record["ae"],
            "terr": siblings[0]["terr"],
            "flag": label,
            "cur": xp,
            "newxp": xp,
            "arr": 0,
            "alloc": False,
            "ncap": 1,
            "ent": True,
            "tier": record["tier"],
            "fy27": record["nnarr"],
            "pipe": True,
        }
        rows.append(row)
        by_name[row["acct"]] = row
        added.append(record)
    outside = [record for record in pipeline if not record["included"]]
    return {"added": added, "expanded": expanded, "outside": outside}


def local_smg_destination(row: dict) -> str:
    """Return the canonical XP for one Local SMG account."""
    if row["state"] == "CA" and row["segment"] == "Local SMG":
        # Two books. Carlos is not pulled off the CA accounts he holds today,
        # and he also holds the rest of Jaxon Sher's North/Central seat.
        # Marcy holds the rest of Tier 8 (the southern list), including
        # Jaxson McBride's water account.
        if row["cur"] == "Carlos Torres" or row["acct"] not in SOUTHERN_CA_LOCAL_SMG:
            return "Carlos Torres"
        return "Marcy Castro"
    if row["person"] == "Local SMG FL (Ter 4)":
        # Natalia keeps South Florida. Ricardo takes the north and central
        # remainder, which includes Alejandro Solano's Flagler accounts, on
        # top of the southeast groups already moving to him.
        if row["acct"] in SE_MM_SOUTH_FL:
            return "Natalia Sanchez"
        return "Ricardo Castro"
    if row["person"] == "Luke Mulvaney":
        return "Luis Aguilar" if row["state"] == "TX" else "Eduardo Ruiz"
    try:
        return LOCAL_SMG_DESTINATION[row["person"]]
    except KeyError as exc:
        raise RuntimeError(
            f"No Local SMG destination for AE group {row['person']!r}"
        ) from exc


def apply_assignments(page: dict, overrides: dict[str, dict]) -> dict:
    rows = page["rows"]
    before_edges = proposed_edges(rows)
    carolina_countable = {
        ND_PARENT,
        "Idaho Labor Department",
    }

    # The open Pacific XP is an Ashley report. That preserves the coherent,
    # single-XP California State AE groups while satisfying the reporting rule.
    page["meta"]["Open XP2 (PT)"][0] = "Ashley Hill"
    page["meta"]["Carolina Prieto"] = ["—", "—", "Team Lead", "Not specified"]
    page["meta"].pop("Carolina Torres", None)
    page["order"] = [xp for xp in page["order"] if xp != "Carolina Torres"]
    for xp in ("Tatiana Montero", "Luis Aguilar", "Ricardo Castro"):
        page["meta"].setdefault(xp, ["—", "n/a", "—", "—"])
        if xp not in page["order"]:
            page["order"].append(xp)
    for xp in LOCAL_SMG_XPS:
        page["meta"].setdefault(xp, ["—", "CT", "XP1", "Costa Rica"])
        page["meta"][xp][1] = "CT"
        page["meta"][xp][3] = "Costa Rica"
    page["meta"]["Tatiana Montero"][1] = "CT"
    page["meta"]["Tatiana Montero"][3] = "Costa Rica"
    # The seat rename is a text replacement, so an older name and its new name
    # can both survive into the order. Keep the first occurrence.
    page["order"] = list(dict.fromkeys(page["order"]))

    # A blank level is an XP1 seat. These seats have an explicit role instead.
    named_level = {
        "Wendy Bhagat": "Director",
        "Jr Wycinsky": "XP4",
        "Jake Sager": "VP",
        "Kristen Murphy": "Manager",
        "Ashley Hill": "Manager",
        "Savannah Lane": "Manager",
    }
    page["meta"].pop("Nathan Williamson", None)
    page["order"] = [xp for xp in page["order"] if xp != "Nathan Williamson"]
    for xp, meta in page["meta"].items():
        if xp in named_level:
            meta[2] = named_level[xp]
        elif str(meta[2]).strip() in {"", "—", "n/a"}:
            meta[2] = "XP1"

    moved = []
    matched = set()
    for row in rows:
        old = row["newxp"]

        # Nathan has left. Jr already holds this federal book in the proposal,
        # and the current view should not keep a departed XP on the team.
        if row["cur"] == "Nathan Williamson":
            row["cur"] = "Jr Wycinsky"
        if row["newxp"] == "Nathan Williamson":
            row["newxp"] = "Jr Wycinsky"

        override = overrides.get(row["acct"])
        if override:
            matched.add(row["acct"])
            if override["segment"]:
                row["segment"] = override["segment"]
                row["ent"] = override["segment"] in ENTERPRISE_SEGMENTS
            if override["xp"]:
                row["newxp"] = override["xp"]

        if row["person"] in AE_OWNER:
            row["newxp"] = AE_OWNER[row["person"]]

        if row["person"] == "Bill Anderson" and row["state"] == "TX":
            row["newxp"] = BILL_ANDERSON_TEXAS_XP

        if row["state"] in {"NY", "NJ"} and row["segment"] == "State":
            row["newxp"] = NY_NJ_STATE_XP

        # North Dakota is a statewide enterprise agreement: sister agencies
        # travel with the billed parent and do not consume a countable slot.
        if row["state"] == "ND" and (
            old == "Carolina Prieto" or row["newxp"] == "Carolina Prieto"
        ):
            row["newxp"] = "Carolina Prieto"
            if row["acct"] not in carolina_countable:
                row["alloc"] = True

        # Kentucky state (and the Tourism cabinet row) sits with Andy. COT is
        # the billed parent; CHFS, Homeland Security and Transportation stay
        # countable because they were already billed separately.
        if row["state"] == "KY" and row["segment"] != "Local ENT":
            row["newxp"] = KY_STATE_XP
            if row["acct"] not in KY_COUNTABLE:
                row["alloc"] = True

        if row["newxp"] != old:
            moved.append((row["acct"], old, row["newxp"], row["person"]))

    # Removals are exempt: once an account is gone, a re-run finds nothing.
    unmatched = sorted(
        account
        for account, override in overrides.items()
        if account not in matched and not override["remove"]
    )
    if unmatched:
        raise RuntimeError(
            "Override accounts not found in the map (check the exact name): "
            + ", ".join(unmatched)
        )

    removed = [r["acct"] for r in rows if overrides.get(r["acct"], {}).get("remove")]
    rows = [r for r in rows if not overrides.get(r["acct"], {}).get("remove")]
    pipeline = apply_pipeline(rows, load_pipeline(PIPELINE))
    page["rows"] = rows

    # Enterprise and Local SMG are separate books. Once every other rule has
    # run, apply the canonical nine-XP Local SMG cut. This is unconditional so
    # reruns converge after older per-account balancing overrides and after the
    # source PAGE has already been rewritten once.
    offloaded = []
    for row in rows:
        if row["segment"] != "Local SMG":
            continue
        destination = local_smg_destination(row)
        if row["newxp"] != destination:
            offloaded.append((row["acct"], row["newxp"], destination))
            moved.append((row["acct"], row["newxp"], destination, row["person"]))
            row["newxp"] = destination

    # Tatiana and Marcy swap books. Tatiana takes the enterprise accounts that
    # had settled with Marcy; Marcy takes Southern California through the Local
    # SMG cut above. Doing it from the account and AE, not from the current
    # name, keeps a second run from swapping them back.
    for row in rows:
        if row["segment"] == "Local SMG":
            continue
        if (
            row["person"] in TATIANA_ENTERPRISE_AES
            or row["acct"] in TATIANA_ENTERPRISE_ACCOUNTS
        ):
            row["newxp"] = "Tatiana Montero"

    enterprise_xps = {r["newxp"] for r in rows if r.get("ent") and not r["alloc"]}
    hybrid = sorted(
        {
            r["newxp"]
            for r in rows
            if r["segment"] == "Local SMG" and r["newxp"] in enterprise_xps
        }
    )
    if hybrid:
        raise RuntimeError(f"Enterprise XPs still holding Local SMG: {hybrid}")

    enterprise_load: dict[str, int] = defaultdict(int)
    smg_load: dict[str, int] = defaultdict(int)
    smg_arr: dict[str, float] = defaultdict(float)
    smg_complex: dict[str, int] = defaultdict(int)
    smg_tiers: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0, 0])
    for row in rows:
        if row["alloc"]:
            continue
        if row.get("ent"):
            enterprise_load[row["newxp"]] += 1
        elif row["segment"] == "Local SMG":
            xp = row["newxp"]
            smg_load[xp] += 1
            smg_arr[xp] += row["arr"]
            smg_complex[xp] += row["ncap"] > 7
            smg_tiers[xp][row["tier"] - 1] += 1

    over_enterprise = {
        xp: n for xp, n in enterprise_load.items() if n > ENTERPRISE_MAX
    }
    if over_enterprise:
        raise RuntimeError(
            f"Enterprise books above the {ENTERPRISE_MAX}-account maximum: "
            + ", ".join(f"{xp} {n}" for xp, n in sorted(over_enterprise.items()))
        )

    over_smg = {xp: n for xp, n in smg_load.items() if n > LOCAL_SMG_MAX}
    if over_smg:
        raise RuntimeError(
            f"Local SMG books above the {LOCAL_SMG_MAX}-account cap: "
            + ", ".join(f"{xp} {n}" for xp, n in sorted(over_smg.items()))
        )

    over_complex = {
        xp: smg_complex[xp]
        for xp, n in smg_load.items()
        if smg_complex[xp] * 3 > n
    }
    if over_complex:
        raise RuntimeError(
            "Local SMG books above the one-third complex-account ceiling: "
            + ", ".join(
                f"{xp} {complex_n}/{smg_load[xp]}"
                for xp, complex_n in sorted(over_complex.items())
            )
        )

    missing_smg_xps = sorted(LOCAL_SMG_XPS - set(smg_load))
    if missing_smg_xps:
        raise RuntimeError(
            "Local SMG XPs with no proposed accounts: " + ", ".join(missing_smg_xps)
        )

    foreign_smg_xps = sorted(set(smg_load) - LOCAL_SMG_XPS)
    if foreign_smg_xps:
        raise RuntimeError(
            "Local SMG accounts assigned outside the nine-XP roster: "
            + ", ".join(foreign_smg_xps)
        )

    wrong_smg_owner = [
        f"{r['acct']} → {r['newxp']}"
        for r in rows
        if r["segment"] == "Local SMG"
        and r["newxp"] != local_smg_destination(r)
    ]
    if wrong_smg_owner:
        raise RuntimeError(
            "Local SMG accounts outside the canonical cut: "
            + ", ".join(wrong_smg_owner)
        )

    ca_accounts = {
        r["acct"]
        for r in rows
        if r["segment"] == "Local SMG"
        and r["state"] == "CA"
        and not r["alloc"]
    }
    missing_southern_ca = sorted(SOUTHERN_CA_LOCAL_SMG - ca_accounts)
    if missing_southern_ca:
        raise RuntimeError(
            "Southern California cut names accounts not in the CA Local SMG book: "
            + ", ".join(missing_southern_ca)
        )

    over_target = {
        xp: n
        for xp, n in enterprise_load.items()
        if ENTERPRISE_TARGET < n <= ENTERPRISE_MAX
    }

    carolina_countable |= {
        r["acct"]
        for r in rows
        if r["person"] == "Scott Mark" and not r["alloc"]
    }

    # Hard validations: fail loudly instead of publishing a subtly wrong map.
    for xp in NO_BOOK:
        assigned = [r["acct"] for r in rows if r["newxp"] == xp]
        if assigned:
            raise RuntimeError(f"{xp} still has proposed accounts: {assigned}")

    ashley_enterprise = [
        r for r in rows if r["cur"] == "Ashley Hill" and r.get("ent")
    ]
    bad = [
        r
        for r in ashley_enterprise
        if r["newxp"] not in ASHLEY_REPORTS
        and r["person"] not in AE_OWNER
        and r["acct"] not in ASHLEY_HOLD_RELEASED
    ]
    if bad:
        raise RuntimeError(
            "Ashley's Enterprise accounts outside her reporting line: "
            + ", ".join(f"{r['acct']} → {r['newxp']}" for r in bad)
        )

    carolina = [r for r in rows if r["newxp"] == "Carolina Prieto"]
    carolina_rows = [r for r in carolina if not r["alloc"]]
    extra = [
        r["acct"]
        for r in carolina_rows
        if r["acct"] not in carolina_countable
    ]
    if extra:
        raise RuntimeError(
            "Carolina Prieto has unexpected countable accounts: "
            + ", ".join(extra)
        )
    missing = carolina_countable - {r["acct"] for r in carolina_rows}
    if missing:
        raise RuntimeError(f"Carolina is missing consolidated accounts: {sorted(missing)}")

    for ae, xp in AE_OWNER.items():
        stray = [
            r["acct"]
            for r in rows
            if r["person"] == ae
            and r["newxp"] != xp
            and not (r["state"] in {"NY", "NJ"} and r["segment"] == "State")
        ]
        if stray:
            raise RuntimeError(f"{ae} accounts not with {xp}: " + ", ".join(stray))

    ny_nj_stray = [
        f"{r['acct']} → {r['newxp']}"
        for r in rows
        if r["state"] in {"NY", "NJ"}
        and r["segment"] == "State"
        and r["newxp"] != NY_NJ_STATE_XP
    ]
    if ny_nj_stray:
        raise RuntimeError(
            "NY/NJ state agencies not with Taylor: " + ", ".join(ny_nj_stray)
        )

    ky_stray = [
        f"{r['acct']} → {r['newxp']}"
        for r in rows
        if r["state"] == "KY"
        and r["segment"] != "Local ENT"
        and r["newxp"] != KY_STATE_XP
    ]
    if ky_stray:
        raise RuntimeError(
            "Kentucky state accounts not with Andy: " + ", ".join(ky_stray)
        )

    carolina_not_id_nd = [
        r["acct"]
        for r in carolina
        if r["state"] not in {"ID", "ND"} and r["acct"] not in CAROLINA_BEYOND_ID_ND
    ]
    if carolina_not_id_nd:
        raise RuntimeError(
            "Carolina Prieto still holding accounts outside Idaho and North Dakota: "
            + ", ".join(carolina_not_id_nd)
        )

    halena_luke = [
        r["acct"]
        for r in rows
        if r["newxp"] == "Halena Martin" and r["person"] == "Luke Mulvaney"
    ]
    if halena_luke:
        raise RuntimeError(
            "Halena still paired with Luke Mulvaney: " + ", ".join(halena_luke)
        )

    glavcd = next(
        r
        for r in rows
        if r["acct"] == "Greater Los Angeles County Vector Control District CA"
    )
    if glavcd["newxp"] != "Colleen Moran" or not glavcd.get("ent"):
        raise RuntimeError("GLAVCD must stay Enterprise with Colleen")

    palm_beach = next(
        r
        for r in rows
        if r["acct"] == "Health Care District of Palm Beach County - FL"
    )
    if palm_beach["newxp"] != "Carolina Cambronero" or not palm_beach.get("ent"):
        raise RuntimeError(
            "Health Care District of Palm Beach County must stay Enterprise "
            "with Carolina Cambronero"
        )

    still_torres = [r["acct"] for r in rows if r["newxp"] == "Carolina Torres"]
    if still_torres:
        raise RuntimeError(
            "Carolina Torres is Carolina Cambronero; stray proposed accounts: "
            + ", ".join(still_torres)
        )

    after_edges = proposed_edges(rows)
    pod_load = assign_pods(page, rows)
    return {
        "moved": moved,
        "removed": removed,
        "offloaded": offloaded,
        "enterprise_load": dict(enterprise_load),
        "smg_load": dict(smg_load),
        "smg_arr": dict(smg_arr),
        "smg_complex": dict(smg_complex),
        "smg_tiers": dict(smg_tiers),
        "over_target": over_target,
        "before_edges": before_edges,
        "after_edges": after_edges,
        "pod_load": pod_load,
        "ashley_enterprise": ashley_enterprise,
        "carolina_countable": carolina_rows,
        "pipeline": pipeline,
    }


def update_markup(source: str) -> str:
    # Normalize renamed seats and the complete Taylor book on every run. These
    # replacements are safe before the PAGE payload is rewritten below.
    source = source.replace("Tatiana Salazar", "Tatiana Montero")
    source = source.replace("Ricardo Rodriguez", "Ricardo Castro")
    source = source.replace(
        "Sarah Duncan, and Territory 4a",
        "Sarah Duncan, Spencer Ferrell, and Territory 4a",
    )

    source = source.replace(
        "<title>XP ↔ AE alignment, Enterprise</title>",
        "<title>XP ↔ AE alignment, US team</title>",
    )
    source = source.replace(
        "<li>Segmentation: every State and Local ENT account by sales segment is "
        "Enterprise, with no special-entity overrides, plus DC.</li>",
        "<li>Segmentation: State and Local ENT accounts are Enterprise, plus DC. "
        "Non-SAM special districts are Local SMG; SAM special districts stay "
        "Enterprise.</li>",
    )

    # Remove the requested section, including its table target.
    source = re.sub(
        r'\n  <section>\n    <h2>Open seats and unmapped coverage</h2>.*?</section>\n',
        "\n",
        source,
        count=1,
        flags=re.S,
    )

    # Remove "Mapping notes" and its list, while retaining the concise method
    # notes above it.
    source = re.sub(
        r'\n    <h3 style="margin-top:22px">Mapping notes</h3>\n'
        r'    <ul class="notes">.*?</ul>',
        "",
        source,
        count=1,
        flags=re.S,
    )

    source = source.replace(
        'Counts exclude allocated child records. "AEs today" is the same count '
        "under current assignments. Complex means more than 7 capabilities. "
        "Only the Enterprise book was remodeled, so Mid-Market and federal XPs "
        "read the same in both views.",
        'Counts exclude allocated child records. "AEs today" is the same count '
        "under current assignments. Complex means more than 7 capabilities. "
        "The proposed view removes account books from Jake Sager, Savannah "
        "Lane, Kristen Murphy and Ashley Hill; the current view remains "
        "historical. Nathan Williamson has left the team, and his federal "
        "accounts sit with Jr Wycinsky.",
    )

    if "When those three books were removed" not in source:
        source = source.replace(
            "<li>Account counts exclude Allocated child records (they carry $0 and "
            "travel with the parent). ARR is the export's converted ARR.</li>",
            "<li>Account counts exclude Allocated child records (they carry $0 and "
            "travel with the parent). ARR is the export's converted ARR.</li>\n"
            "      <li>Jake Sager, Nathan Williamson, Savannah Lane, Kristen Murphy "
            "and Ashley Hill carry no accounts "
            "in the proposed book. Ashley's current Enterprise accounts route only "
            "to her reports; Carolina Prieto is a Team Lead, not a manager.</li>\n"
            "      <li>When those three books were removed, each displaced Local SMG "
            "AE group moved intact to an XP who already works with that AE. This "
            "strictly reduces coordination fan-out without creating a new relationship. "
            "The exception is Connecticut PURA: Ashley's reporting-line rule requires "
            "one additional Stephanie DelSignore relationship for Steffany while "
            "Halena retains the broader Connecticut estate.</li>",
        )

    if "Enterprise and Local SMG are separate books" not in source:
        source = source.replace(
            "<li>Account counts exclude Allocated child records (they carry $0 and "
            "travel with the parent). ARR is the export's converted ARR.</li>",
            "<li>Account counts exclude Allocated child records (they carry $0 and "
            "travel with the parent). ARR is the export's converted ARR.</li>\n"
            "      <li>Enterprise and Local SMG are separate books. No Enterprise XP "
            "carries a Local SMG account; each Local SMG AE group moves whole to a "
            "dedicated Local SMG XP, so the AE works with one XP instead of several."
            "</li>",
        )

    if "Carolina Cambronero holds the Florida Enterprise book" not in source:
        source = source.replace(
            "Carolina Torres holds the Florida Enterprise book",
            "Carolina Cambronero holds the Florida Enterprise book",
        )
    if "Carolina Cambronero holds the Florida Enterprise book" not in source:
        source = source.replace(
            "Halena retains the broader Connecticut estate.</li>",
            "Halena retains the broader Connecticut estate.</li>\n"
            "      <li>Carolina Cambronero holds the Florida Enterprise book (Desmond Davis, "
            "Bill Marshall, Demi Washington) plus Health Care District of Palm Beach "
            "County. Taylor Roman holds Benjamin Shor, Stephanie DelSignore's New York "
            "and New Jersey accounts, Sarah Duncan, Spencer Ferrell, and Territory 4a; "
            "Stephanie's Connecticut accounts stay with Halena.</li>",
        )

    if (
        "Carolina Prieto keeps only the Idaho" not in source
        and "enterprise agreements (two customers" not in source
    ):
        source = source.replace(
            "Halena retains the broader Connecticut estate.</li>",
            "Halena retains the broader Connecticut estate.</li>\n"
            "      <li>Carolina Prieto keeps only the Idaho and North Dakota state "
            "book (Scott Mark, including the North Dakota enterprise agreement). "
            "Andy O'Brien holds Kentucky state, including the COT enterprise "
            "agreement plus CHFS, Homeland Security and Transportation; sister "
            "agencies are allocated children. She releases scattered local accounts "
            "to XPs who already work with those AEs. Glendale AZ is the exception: "
            "Conrad Taylor has no other book, so it goes to Colleen with her other "
            "Pacific SAM work.</li>\n"
            "      <li>Local SMG includes special districts except SAM territories. "
            "GLAVCD stays Enterprise with Colleen. Luke Mulvaney's three districts "
            "sit with Carlos Torres so Halena is not paired with that vertical.</li>",
        )

    # The replacement contains its own search text, so a plain str.replace would
    # prepend the two names again on every run. Collapse any number of copies.
    source = re.sub(
        r"(?:Jake Sager, Nathan Williamson, )*"
        r"Savannah Lane, Kristen Murphy and Ashley Hill carry no accounts in the "
        r"proposed book\.",
        "Jake Sager, Nathan Williamson, Savannah Lane, Kristen Murphy and Ashley "
        "Hill carry no accounts in the proposed book.",
        source,
    )
    source = source.replace(
        "The proposed view removes account books from Savannah Lane, Kristen "
        "Murphy and Ashley Hill; the current view remains historical.",
        "The proposed view removes account books from Jake Sager, Savannah "
        "Lane, Kristen Murphy and Ashley Hill; the current view remains "
        "historical. Nathan Williamson has left the team, and his federal "
        "accounts sit with Jr Wycinsky.",
    )
    source = source.replace(
        "The proposed view removes account books from Jake Sager, Nathan "
        "Williamson, Savannah Lane, Kristen Murphy and Ashley Hill; the "
        "current view remains historical.",
        "The proposed view removes account books from Jake Sager, Savannah "
        "Lane, Kristen Murphy and Ashley Hill; the current view remains "
        "historical. Nathan Williamson has left the team, and his federal "
        "accounts sit with Jr Wycinsky.",
    )
    source = source.replace(
        "Carolina Prieto keeps the Kentucky and North Dakota statewide "
        "enterprise agreements (two customers; sister agencies are allocated "
        "children), plus CHFS, Homeland Security and Transportation for Kentucky "
        "consolidation. She releases scattered local accounts",
        "Carolina Prieto keeps only the Idaho and North Dakota state book "
        "(Scott Mark, including the North Dakota enterprise agreement). Andy "
        "O'Brien holds Kentucky state, including the COT enterprise agreement "
        "plus CHFS, Homeland Security and Transportation; sister agencies are "
        "allocated children. She releases scattered local accounts",
    )
    source = source.replace(
        "enterprise agreements (two customers; sister agencies are allocated "
        "children) and releases the scattered local accounts",
        "Carolina Prieto keeps only the Idaho and North Dakota state book. She "
        "releases scattered local accounts",
    )
    source = source.replace(
        "Luke Mulvaney's three districts sit with one SMG XP so Halena is not "
        "paired with that vertical.",
        "Luke Mulvaney's three districts sit with Carlos Torres so Halena is not "
        "paired with that vertical.",
    )
    source = source.replace(
        "GLAVCD stays Enterprise with Colleen. Luke Mulvaney's three districts",
        "GLAVCD stays Enterprise with Colleen. Health Care District of Palm Beach "
        "County stays Enterprise with Carolina Cambronero and the rest of the Florida "
        "book. Luke Mulvaney's three districts",
    )
    source = source.replace(
        "each Local SMG AE group moves whole to a dedicated Local SMG XP, so the "
        "AE works with one XP instead of several.",
        "nine dedicated Local SMG XPs cover whole AE groups wherever the 30-account "
        "cap permits. Carlos Torres keeps the California Local SMG accounts he "
        "holds today and the rest of the North/Central seat. Marcy Castro holds "
        "the rest of southern Tier 8. Eduardo Ruiz holds the northeast groups "
        "that had been Carlos's. Luis Aguilar holds Texas. Natalia Sanchez holds "
        "South Florida, and Ricardo Castro holds north and central Florida plus "
        "the Southeast and Mid-Atlantic, including Alejandro Solano's accounts "
        "that move with those groups. Tatiana Montero holds Marcy's former "
        "Missouri, Illinois, Ohio and Nebraska enterprise book.",
    )
    source = source.replace(
        "Luke Mulvaney's three districts sit with Carlos Torres so Halena is not "
        "paired with that vertical.",
        "Luke Mulvaney's Texas district sits with Luis Aguilar; his New Jersey and "
        "Oregon districts sit with Eduardo Ruiz.",
    )
    source = source.replace(
        "County. Taylor Roman holds Benjamin Shor",
        "County. Cedric Simpkins's Texas SAM group consolidates with Steffany "
        "Amador, who already held San Antonio and VIA. Taylor Roman holds Benjamin "
        "Shor",
    )

    # The coverage section is gone, so tables() must no longer write into #gaps.
    source = re.sub(
        r'function tables\(\)\{\n'
        r'  const gaps=.*?\n'
        r'    gaps\.map\(.*?\)\.join\(""\)\+`</tbody>`;\n',
        "function tables(){\n",
        source,
        count=1,
        flags=re.S,
    )
    # Carolina Torres was a duplicate name for Carolina Cambronero.
    source = source.replace("Carolina Torres", "Carolina Cambronero")

    # The modeling notes are working commentary, not part of the page.
    source = re.sub(
        r'\n  <section>\n    <h2>How this was modeled</h2>.*?</section>\n',
        "\n",
        source,
        count=1,
        flags=re.S,
    )
    pipeline_note = (
        " The proposed view adds the US state logos and expansion ARR from the "
        "visible Q3 FY2027 pipeline extract. UK pipeline stays off this map."
    )
    anchor = "accounts sit with Jr Wycinsky."
    if pipeline_note not in source:
        source = source.replace(anchor, anchor + pipeline_note)
    return source


def main() -> None:
    source = HTML.read_text()
    page, start, end = extract_page(source)
    result = apply_assignments(page, load_overrides(OVERRIDES))

    source = source[:start] + json.dumps(page, separators=(", ", ": ")) + source[end:]
    source = update_markup(source)
    HTML.write_text(source)

    moved = result["moved"]
    print(f"moved {len(moved)} proposed account records")
    if result["removed"]:
        print("removed from the map: " + ", ".join(sorted(result["removed"])))
    if result["offloaded"]:
        counts: dict[tuple[str, str], int] = defaultdict(int)
        for _, source_xp, destination in result["offloaded"]:
            counts[(source_xp, destination)] += 1
        print(f"Local SMG reassigned to canonical books: {len(result['offloaded'])}")
        for (source_xp, destination), n in sorted(counts.items()):
            print(f"  {source_xp} → {destination}: {n}")
    print(
        "XP↔AE edges: "
        f"{len(result['before_edges'])} → {len(result['after_edges'])} "
        f"({len(result['after_edges']) - len(result['before_edges']):+d})"
    )
    for xp in sorted(NO_BOOK):
        print(f"{xp}: 0 proposed accounts")
    print("Ashley's Enterprise destinations:")
    for row in result["ashley_enterprise"]:
        released = " (hold released)" if row["acct"] in ASHLEY_HOLD_RELEASED else ""
        print(f"  {row['acct']} → {row['newxp']}{released}")
    print(
        f"Enterprise books (target {ENTERPRISE_TARGET}, max {ENTERPRISE_MAX}): "
        f"max {max(result['enterprise_load'].values())}"
    )
    for xp, n in sorted(result["over_target"].items()):
        print(f"  over target, within max: {xp} {n}")
    print(
        f"Local SMG books (cap {LOCAL_SMG_MAX}): "
        f"max {max(result['smg_load'].values())}"
    )
    for xp, n in sorted(result["smg_load"].items()):
        tiers = result["smg_tiers"][xp]
        print(
            f"  {xp}: {n}, ${result['smg_arr'][xp]:,.0f} ARR, "
            f"T1/T2/T3/T4 {'/'.join(map(str, tiers))}, "
            f"complex {result['smg_complex'][xp]}"
        )
    pipeline = result["pipeline"]
    print(
        "FY2027 pipeline: "
        f"{len(pipeline['added'])} new logos, "
        f"{len(pipeline['expanded'])} expansions, "
        f"{len(pipeline['outside'])} outside the US book"
    )
    for record in pipeline["added"] + pipeline["expanded"]:
        kind = "new" if record in pipeline["added"] else "expansion"
        print(f"  {kind}: {record['account']} ${record['nnarr']:,.0f}")
    outside_arr = sum(record["nnarr"] for record in pipeline["outside"])
    if pipeline["outside"]:
        print(f"  outside the US book: ${outside_arr:,.0f}")
    print("Pod aligned seats (countable accounts, ignoring current owners):")
    for seat, xp, role, label, _terr in POD_ASSIGNED:
        print(f"  {label} — {xp} ({role}): {result['pod_load'].get(seat, 0)}")
    unverified = page.get("podUnverified") or []
    if unverified:
        print(
            "Pod timezone not on the roster, so the one-hour rule was not applied: "
            + ", ".join(unverified)
        )
    print("Carolina countable consolidated accounts:")
    for row in result["carolina_countable"]:
        print(f"  {row['acct']} ${row['arr'] + row.get('fy27', 0):,.0f}")


if __name__ == "__main__":
    main()
