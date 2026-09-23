#!/usr/bin/env python3
"""Build the ENT book growth tiering from the research corpus and the assignment model.

Reads:
  research/state-fiscal-capacity-and-it-modernization-fy2026-fy2027.md   section 2 table
  research/govtech-grant-funding-landscape-2026.md                       section 2 table
  research/govtech-state-demand-growth-2026.md                           section 11 table
  tiering/state_overlay.csv                                              hand-curated judgements
  XP_AE_Rebalance_Model.xlsx                                             the book

Writes:
  tiering/state_tiers.csv        one row per state, every input and every sub-score
  tiering/account_tiers.csv      one row per account
  tiering/xp_tier_summary.csv    one row per XP under the revised book
  tiering/tiering.json           everything the HTML view needs

Run:  python3 tiering/build_tiering.py
"""

import csv
import json
import math
import re
import statistics
from collections import defaultdict
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
RESEARCH = ROOT / "research"
OUT = ROOT / "tiering"

# --------------------------------------------------------------------------------------
# Weights. Everything downstream is a function of these, so this block is the whole model.
# Two territory scores are computed because the book has two different motions in it:
# State-map accounts sell into state agencies, Local ENT accounts sell into counties and
# cities. The same state can be a good state-agency territory and a poor local one.
# --------------------------------------------------------------------------------------

# The organising principle is that growth potential is expected *incremental ARR*, which is a
# size quantity, not a rate. A territory growing 50% on a $50k base deserves less XP capacity
# than one growing 10% on a $5M base. Scale terms therefore carry real weight, and an untouched
# small state does not outrank a large one on untouched-ness alone.

W_STATE_SIDE = {
    "agency_market_scale": 20,   # size of the prize: the agency estate and the budget behind it
    "penetration_headroom": 14,  # share of that prize we have not already claimed
    "fiscal_posture": 22,        # can the state fund anything new at all
    "it_modernization": 16,      # is there a named, funded modernization line to attach to
    "reserves": 6,               # cushion behind the posture call
    "purchasing_access": 12,     # is there a vehicle, or is every deal a fresh procurement
    "cycle_friction": 10,        # annual budgets give twice the buying windows of biennial
}

W_LOCAL_SIDE = {
    "whitespace": 26,            # enterprise-scale jurisdictions we do not yet hold
    "penetration_headroom": 8,   # how hard we have already worked the locals we do hold
    "demand_momentum": 20,       # population, domestic migration, permit volume and trend
    "funding_environment": 16,   # state grant programs to locals, net of ARPA cliff exposure
    "local_fiscal_headwind": 8,  # property tax caps squeezing local own-source revenue
    "purchasing_access": 14,     # vehicle, net of an occupied league-endorsement channel
    "crosssell_depth": 8,        # room left inside the logos we already hold
}

# Territory tier cut points on the 0-100 blended score.
TERRITORY_BANDS = [("A", 58.0), ("B", 47.0), ("C", 37.0), ("D", 0.0)]

# Account growth-potential blend.
ACCOUNT_TERRITORY_WEIGHT = 0.60
ACCOUNT_WHITESPACE_WEIGHT = 0.40

# An account holding this many capabilities is treated as fully penetrated.
CAPABILITY_CEILING = 8

STATE_ABBR = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Hawai'i": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY",
    "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA",
    "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH",
    "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR",
    "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY",
}


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def scale(x, lo, hi):
    """Map x from [lo, hi] onto [0, 1], clamped at both ends."""
    if hi == lo:
        return 0.0
    return clamp((x - lo) / (hi - lo))


def read_md_table(path, header_contains):
    """Pull the first markdown pipe table whose header row contains every given substring."""
    rows = []
    header = None
    for line in path.read_text().splitlines():
        if not line.startswith("|"):
            if header is not None and rows:
                break
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            if all(any(h.lower() in c.lower() for c in cells) for h in header_contains):
                header = cells
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        if len(cells) != len(header):
            continue
        rows.append(dict(zip(header, cells)))
    if header is None:
        raise SystemExit(f"table not found in {path.name} for {header_contains}")
    return rows


def clean(cell):
    """Strip markdown emphasis and footnote markers out of a table cell."""
    return re.sub(r"[*†]", "", cell).strip()


def to_num(cell):
    cell = clean(cell).replace(",", "").replace("+", "").replace("%", "")
    try:
        return float(cell)
    except ValueError:
        return None


# --------------------------------------------------------------------------------------
# Load the research inputs
# --------------------------------------------------------------------------------------

def load_signals():
    sig = defaultdict(dict)

    fiscal = read_md_table(
        RESEARCH / "state-fiscal-capacity-and-it-modernization-fy2026-fy2027.md",
        ["State", "posture", "RDF"],
    )
    for r in fiscal:
        name = clean(r["State"])
        ab = STATE_ABBR[name]
        sig[ab]["state"] = name
        sig[ab]["posture"] = clean(r[[c for c in r if "posture" in c.lower()][0]])
        sig[ab]["rdf_pct"] = to_num(r[[c for c in r if "RDF" in c][0]])
        sig[ab]["it_note"] = clean(r[[c for c in r if "IT modernization" in c][0]])
        sig[ab]["budget_cycle"] = clean(r[[c for c in r if c.strip() == "Cycle"][0]])
        sig[ab]["fiscal_confidence"] = clean(r[[c for c in r if "Conf" in c][0]]).lower()

    grants = read_md_table(
        RESEARCH / "govtech-grant-funding-landscape-2026.md",
        ["State", "Environment", "ARPA"],
    )
    for r in grants:
        ab = STATE_ABBR[clean(r["State"])]
        env = clean(r["Environment"]).lower()
        # Texas is recorded as "Rich (vehicles) / Thin (grants)". Its vehicles are already
        # credited in full under purchasing_access, so read the grant column as thin here
        # rather than paying for the same asset twice.
        env = "thin" if "thin" in env else env.split("(")[0].strip()
        sig[ab]["grant_env"] = env
        sig[ab]["grant_note"] = clean(r[[c for c in r if "Named state" in c][0]])
        sig[ab]["arpa_cliff"] = clean(r[[c for c in r if "ARPA" in c][0]]).lower()
        sig[ab]["grant_confidence"] = clean(r[[c for c in r if "Conf" in c][0]]).lower()

    demand = read_md_table(
        RESEARCH / "govtech-state-demand-growth-2026.md",
        ["State", "Pop 7/1/2025", "Permits CY2025"],
    )
    for r in demand:
        ab = STATE_ABBR[clean(r["State"])]
        g = lambda frag: to_num(r[[c for c in r if frag in c][0]])
        sig[ab]["population"] = g("Pop 7/1/2025")
        sig[ab]["pop_pct_chg"] = g("Pop % chg")
        sig[ab]["dom_mig_per_1k"] = g("per 1k")
        sig[ab]["permits_cy2025"] = g("Permits CY2025")
        sig[ab]["permits_cy2024"] = g("Permits CY2024")
        sig[ab]["permits_ytd2026"] = g("YTD Jul 2026")
        sig[ab]["permits_ytd2025"] = g("YTD Jul 2025")
        sig[ab]["juris_over_100k"] = g("over 100k")

    with (OUT / "state_overlay.csv").open() as fh:
        text = "\n".join(l for l in fh.read().splitlines() if not l.startswith("#"))
    for r in csv.DictReader(text.splitlines()):
        ab = STATE_ABBR[r["state"].strip()]
        sig[ab]["purchasing_access"] = r["purchasing_access"].strip()
        sig[ab]["channel_occupied"] = r["channel_occupied"].strip() == "yes"
        sig[ab]["local_capacity"] = r["local_capacity"].strip()
        sig[ab]["tax_cap_pressure"] = r["tax_cap_pressure"].strip() == "yes"
        sig[ab]["it_mod_signal"] = r["it_mod_signal"].strip()
        sig[ab]["overlay_note"] = r["note"].strip()

    missing = [ab for ab, v in sig.items() if len(v) < 18]
    if missing:
        raise SystemExit(f"incomplete signal rows: {missing}")
    return dict(sig)


# --------------------------------------------------------------------------------------
# Load the book
# --------------------------------------------------------------------------------------

def parse_caps(s):
    """Capability strings use an Oxford comma inside one product name."""
    if not s:
        return []
    s = str(s).replace("Websites, Portals, & Intranets", "Websites/Portals/Intranets")
    return [x.strip() for x in s.split(",") if x.strip()]


def load_roster():
    wb = openpyxl.load_workbook(ROOT / "XP_AE_Rebalance_Model.xlsx")
    ws = wb["Lookups"]
    roster = {}
    for xp, mgr, level, loc, tz, *_ in ws.iter_rows(min_row=2, values_only=True):
        if xp:
            roster[xp] = {"manager": mgr, "level": level, "location": loc, "tz": tz}
    return roster


def load_book():
    wb = openpyxl.load_workbook(ROOT / "XP_AE_Rebalance_Model.xlsx")
    ws = wb["Assignments"]
    hdr = [c.value for c in ws[1]]
    out = []
    for raw in ws.iter_rows(min_row=2, values_only=True):
        if not raw[0]:
            continue
        r = dict(zip(hdr, raw))
        caps = parse_caps(r["Capabilities Counted"])
        out.append({
            "account": r["Account Name"],
            "state": (r["State"] or "").strip(),
            "side": r["Map"],
            "ae": r["AE / SAM"],
            "xp_new": r["Revised XP"],
            "xp_wip": r["WIP Proposed XP"],
            "manager": None,
            "arr": float(r["ARR"] or 0),
            "countable": r["Counts vs Cap"] == "Yes",
            "allocated": r["Counts vs Cap"] == "No (Allocated)",
            "ncap": len(caps),
            "caps": caps,
            "segment": r["Market Segment (export)"],
        })
    return out


# --------------------------------------------------------------------------------------
# Territory scoring
# --------------------------------------------------------------------------------------

POSTURE_PTS = {"expanding": 1.00, "stable": 0.70, "constrained": 0.35, "distressed": 0.10}
GRANT_PTS = {"rich": 1.00, "moderate": 0.55, "thin": 0.20}
CLIFF_PTS = {"low": 1.00, "low–med": 0.80, "low-med": 0.80, "med": 0.55, "high": 0.20}
IT_MOD_PTS = {"funded": 1.00, "governance": 0.35, "neutral": 0.30, "none": 0.15, "headwind": 0.05}
ACCESS_PTS = {"strong": 1.00, "present": 0.60, "coop_only": 0.25}
CYCLE_PTS = {"Annual": 1.00, "Biennial": 0.65}
CAPACITY_PTS = {"typical": 1.00, "constrained": 0.55}


def cliff_pts(v):
    # New York is recorded as "Low (state) / Med (NYC & locals)"; split the difference.
    if "/" in v and "low" in v and "med" in v:
        return 0.70
    for key in sorted(CLIFF_PTS, key=len, reverse=True):
        if v.startswith(key):
            return CLIFF_PTS[key]
    return 0.55


def score_territories(sig, book):
    # Book facts per state
    local_accounts = defaultdict(int)
    state_arr = defaultdict(float)
    local_arr = defaultdict(float)
    caps_local = defaultdict(list)
    for a in book:
        if not a["state"]:
            continue
        if a["side"] == "Local ENT":
            local_accounts[a["state"]] += 1
            local_arr[a["state"]] += a["arr"]
            caps_local[a["state"]].append(a["ncap"])
        elif a["side"] == "State":
            state_arr[a["state"]] += a["arr"]

    # Penetration is measured as ARR per million residents. The cap is set at the 80th
    # percentile of states where we hold any ARR at all, so the handful of deeply penetrated
    # states anchor the top of the scale instead of the mean.
    def penetration_scale(arr_by_state):
        per_m = {ab: arr_by_state.get(ab, 0.0) / (sig[ab]["population"] / 1e6) for ab in sig}
        held = sorted(v for v in per_m.values() if v > 0)
        cap = statistics.quantiles(held, n=5)[3] if len(held) >= 5 else max(held or [1.0])
        return per_m, cap

    per_m, pen_cap = penetration_scale(state_arr)
    local_per_m, local_pen_cap = penetration_scale(local_arr)

    rows = {}
    for ab, s in sig.items():
        # ---- shared inputs
        posture = POSTURE_PTS[s["posture"].lower()]
        reserves = scale(s["rdf_pct"] or 0, 0, 25)
        it_mod = IT_MOD_PTS[s["it_mod_signal"]]
        access = ACCESS_PTS[s["purchasing_access"]]
        cycle = CYCLE_PTS[s["budget_cycle"]]
        capacity = CAPACITY_PTS[s["local_capacity"]]
        channel = 0.60 if s["channel_occupied"] else 1.00

        # ---- state-agency side
        headroom = 1.0 - scale(per_m[ab], 0, pen_cap)
        market_scale = scale(math.log10(s["population"]), math.log10(600_000), math.log10(40_000_000))
        st = {
            "fiscal_posture": posture,
            "reserves": reserves,
            "it_modernization": it_mod,
            "penetration_headroom": headroom,
            "agency_market_scale": market_scale,
            "purchasing_access": access,
            "cycle_friction": cycle,
        }
        state_score = sum(W_STATE_SIDE[k] * v for k, v in st.items())

        # ---- local ENT side
        addressable = s["juris_over_100k"] or 0
        covered = local_accounts.get(ab, 0)
        open_juris = max(0.0, addressable - covered)
        ws_ratio = (open_juris / addressable) if addressable else 0.0
        ws_absolute = math.sqrt(open_juris / 110.0)
        # Weighted toward the absolute count: holding none of Montana's five large
        # jurisdictions is not the same opportunity as holding none of California's 112.
        whitespace = clamp(0.25 * ws_ratio + 0.75 * ws_absolute)

        permit_chg = statistics.mean([
            (s["permits_cy2025"] / s["permits_cy2024"] - 1) * 100 if s["permits_cy2024"] else 0,
            (s["permits_ytd2026"] / s["permits_ytd2025"] - 1) * 100 if s["permits_ytd2025"] else 0,
        ])
        permits_per_100k = s["permits_cy2025"] / (s["population"] / 1e5)
        demand = (
            0.30 * scale(s["pop_pct_chg"], -0.30, 1.30)
            + 0.30 * scale(s["dom_mig_per_1k"], -4.0, 8.0)
            + 0.20 * scale(permit_chg, -12.0, 12.0)
            + 0.20 * scale(permits_per_100k, 120, 800)
        )

        funding = 0.55 * GRANT_PTS[s["grant_env"]] + 0.45 * cliff_pts(s["arpa_cliff"])
        headwind = 0.35 if s["tax_cap_pressure"] else 1.00

        depth = caps_local.get(ab, [])
        crosssell = (
            1.0 - statistics.mean(min(c, CAPABILITY_CEILING) for c in depth) / CAPABILITY_CEILING
            if depth else 0.60  # no local presence yet: neutral, the whitespace term carries it
        )

        lo = {
            "whitespace": whitespace,
            "penetration_headroom": 1.0 - scale(local_per_m[ab], 0, local_pen_cap),
            "demand_momentum": demand,
            "funding_environment": funding,
            "local_fiscal_headwind": headwind,
            "purchasing_access": access * channel * capacity,
            "crosssell_depth": crosssell,
        }
        local_score = sum(W_LOCAL_SIDE[k] * v for k, v in lo.items())

        rows[ab] = {
            "abbr": ab,
            "state": s["state"],
            "state_side_score": round(state_score, 1),
            "local_side_score": round(local_score, 1),
            "state_side_parts": {k: round(v, 3) for k, v in st.items()},
            "local_side_parts": {k: round(v, 3) for k, v in lo.items()},
            "permit_chg_pct": round(permit_chg, 1),
            "permits_per_100k": round(permits_per_100k, 0),
            "addressable_over_100k": int(addressable),
            "local_accounts_held": covered,
            "open_jurisdictions": int(open_juris),
            "state_arr": round(state_arr.get(ab, 0.0)),
            "local_arr": round(local_arr.get(ab, 0.0)),
            "state_arr_per_million": round(per_m[ab]),
            "confidence": min(s["fiscal_confidence"], s["grant_confidence"],
                              key=lambda c: {"low": 0, "med": 1, "high": 2}.get(c, 1)),
            **{k: s[k] for k in (
                "posture", "rdf_pct", "budget_cycle", "grant_env", "arpa_cliff",
                "purchasing_access", "channel_occupied", "local_capacity",
                "tax_cap_pressure", "it_mod_signal", "population", "pop_pct_chg",
                "dom_mig_per_1k", "it_note", "grant_note", "overlay_note",
            )},
        }

    # Each state gets a tier per side, because the two motions genuinely diverge: California
    # is a deeply penetrated state-agency estate inside a budget deficit, and simultaneously
    # the largest pool of unheld 100k-plus jurisdictions in the country. The blended score is
    # a reporting convenience weighted by where this book's accounts actually sit; the
    # per-side tiers are what drive account scoring.
    mix = defaultdict(lambda: [0, 0])
    for a in book:
        if a["state"] in rows and a["countable"]:
            mix[a["state"]][0 if a["side"] == "State" else 1] += 1

    def band(score):
        for tier, floor in TERRITORY_BANDS:
            if score >= floor:
                return tier
        return "D"

    for ab, r in rows.items():
        n_state, n_local = mix.get(ab, (0, 0))
        if n_state + n_local == 0:
            blended = 0.5 * (r["state_side_score"] + r["local_side_score"])
        else:
            blended = (n_state * r["state_side_score"] + n_local * r["local_side_score"]) / (n_state + n_local)
        r["blended_score"] = round(blended, 1)
        r["in_book_state_accounts"] = n_state
        r["in_book_local_accounts"] = n_local
        r["state_side_tier"] = band(r["state_side_score"])
        r["local_side_tier"] = band(r["local_side_score"])
        r["territory_tier"] = band(blended)
        r["split_territory"] = r["state_side_tier"] != r["local_side_tier"]
    return rows


# --------------------------------------------------------------------------------------
# Account scoring
# --------------------------------------------------------------------------------------

TIER_LABEL = {
    1: "Growth engine",
    2: "Expansion",
    3: "Defend",
    4: "Maintain",
}
GROWTH_LOAD = {1: 1.00, 2: 0.80, 3: 0.50, 4: 0.30}


def score_accounts(terr, book):
    countable = [a for a in book if a["countable"]]

    # Capability data is missing for most State-map records. Impute from the median depth of
    # State-map accounts that do have data, and flag it, rather than scoring them as pure
    # whitespace and letting a data gap masquerade as opportunity.
    known = [a["ncap"] for a in countable if a["side"] == "State" and a["caps"]]
    imputed_state_depth = statistics.median(known) if known else 2

    for a in book:
        t = terr.get(a["state"])
        if t is None:
            a.update(territory_tier=None, territory_score=None, account_whitespace=None,
                     growth_potential=None, tier=None, tier_label="Unmapped",
                     capability_data="n/a")
            continue
        is_state_side = a["side"] == "State"
        side_score = t["state_side_score"] if is_state_side else t["local_side_score"]
        side_tier = t["state_side_tier"] if is_state_side else t["local_side_tier"]

        if a["caps"]:
            depth, flag = a["ncap"], "reported"
        else:
            depth, flag = imputed_state_depth, "imputed"
        whitespace = 1.0 - min(depth, CAPABILITY_CEILING) / CAPABILITY_CEILING

        gp = (ACCOUNT_TERRITORY_WEIGHT * side_score / 100.0
              + ACCOUNT_WHITESPACE_WEIGHT * whitespace)
        a.update(
            territory_tier=side_tier,
            territory_score=round(side_score, 1),
            account_whitespace=round(whitespace, 3),
            growth_potential=round(gp, 4),
            capability_data=flag,
        )

    # Split on the countable book so the allocated $0 child records cannot move the cut points.
    gp_cut = statistics.median(a["growth_potential"] for a in countable)
    arr_cut = statistics.median(a["arr"] for a in countable)

    for a in book:
        if a["growth_potential"] is None:
            continue
        hi_growth = a["growth_potential"] >= gp_cut
        hi_arr = a["arr"] >= arr_cut
        tier = 1 if (hi_growth and hi_arr) else 2 if hi_growth else 3 if hi_arr else 4
        a["tier"] = tier
        a["tier_label"] = TIER_LABEL[tier]
    return {"growth_cut": round(gp_cut, 4), "arr_cut": round(arr_cut)}


def summarise_xps(book, roster, scenario="xp_new"):
    rollup = defaultdict(lambda: {
        "level": None, "manager": None,
        "accounts": 0, "countable": 0, "arr": 0.0,
        "t1": 0, "t2": 0, "t3": 0, "t4": 0,
        "t1_arr": 0.0, "t2_arr": 0.0, "t3_arr": 0.0, "t4_arr": 0.0,
        "growth_load": 0.0, "imputed": 0,
        "terr_a": 0, "terr_b": 0, "terr_c": 0, "terr_d": 0,
    })
    for a in book:
        xp = a[scenario]
        if not xp or a["tier"] is None:
            continue
        r = rollup[xp]
        meta = roster.get(xp, {})
        r["level"] = meta.get("level")
        r["manager"] = meta.get("manager")
        r["accounts"] += 1
        r["arr"] += a["arr"]
        if a["capability_data"] == "imputed":
            r["imputed"] += 1
        if a["countable"]:
            r["countable"] += 1
            r[f"t{a['tier']}"] += 1
            r["growth_load"] += GROWTH_LOAD[a["tier"]]
            if a["territory_tier"]:
                r[f"terr_{a['territory_tier'].lower()}"] += 1
        r[f"t{a['tier']}_arr"] += a["arr"]
    for xp, r in rollup.items():
        n = r["countable"] or 1
        r["growth_share"] = round((r["t1"] + r["t2"]) / n, 3)
        r["growth_load_per_account"] = round(r["growth_load"] / n, 3)
        r["arr"] = round(r["arr"])
        for k in ("t1_arr", "t2_arr", "t3_arr", "t4_arr"):
            r[k] = round(r[k])
    return dict(rollup)


# --------------------------------------------------------------------------------------

def main():
    sig = load_signals()
    book = load_book()
    roster = load_roster()
    terr = score_territories(sig, book)
    cuts = score_accounts(terr, book)
    xp_new = summarise_xps(book, roster, "xp_new")
    xp_wip = summarise_xps(book, roster, "xp_wip")

    OUT.mkdir(exist_ok=True)

    cols = ["abbr", "state", "territory_tier", "state_side_tier", "local_side_tier",
            "split_territory", "blended_score", "state_side_score",
            "local_side_score", "confidence", "posture", "rdf_pct", "budget_cycle", "it_mod_signal",
            "grant_env", "arpa_cliff", "purchasing_access", "channel_occupied",
            "local_capacity", "tax_cap_pressure", "population", "pop_pct_chg",
            "dom_mig_per_1k", "permit_chg_pct", "permits_per_100k",
            "addressable_over_100k", "local_accounts_held", "open_jurisdictions",
            "in_book_state_accounts", "in_book_local_accounts", "state_arr", "local_arr",
            "state_arr_per_million", "it_note", "grant_note", "overlay_note"]
    with (OUT / "state_tiers.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in sorted(terr.values(), key=lambda r: -r["blended_score"]):
            w.writerow(r)

    acols = ["account", "state", "side", "ae", "xp_new", "xp_wip", "arr", "countable",
             "ncap", "capability_data", "territory_tier", "territory_score",
             "account_whitespace", "growth_potential", "tier", "tier_label"]
    with (OUT / "account_tiers.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=acols, extrasaction="ignore")
        w.writeheader()
        for a in sorted(book, key=lambda a: (a["tier"] or 9, -a["arr"])):
            w.writerow(a)

    xcols = ["xp", "level", "manager", "accounts", "countable", "arr", "t1", "t2", "t3", "t4", "growth_share",
             "growth_load", "growth_load_per_account", "t1_arr", "t2_arr", "t3_arr",
             "t4_arr", "terr_a", "terr_b", "terr_c", "terr_d", "imputed"]
    with (OUT / "xp_tier_summary.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=xcols, extrasaction="ignore")
        w.writeheader()
        for xp, r in sorted(xp_new.items(), key=lambda kv: -kv[1]["growth_load"]):
            w.writerow({"xp": xp, **r})

    (OUT / "tiering.json").write_text(json.dumps({
        "weights": {"state_side": W_STATE_SIDE, "local_side": W_LOCAL_SIDE,
                    "territory_bands": TERRITORY_BANDS,
                    "account_blend": {"territory": ACCOUNT_TERRITORY_WEIGHT,
                                      "whitespace": ACCOUNT_WHITESPACE_WEIGHT},
                    "capability_ceiling": CAPABILITY_CEILING,
                    "growth_load": GROWTH_LOAD},
        "cuts": cuts,
        "territories": terr,
        "accounts": [{k: a[k] for k in acols} for a in book],
        "xp_new": xp_new,
        "xp_wip": xp_wip,
    }, indent=1))

    # ---- console report
    print(f"cut points: growth_potential >= {cuts['growth_cut']}, ARR >= ${cuts['arr_cut']:,}\n")
    for label, key in (("State-agency", "state_side"), ("Local ENT", "local_side")):
        bands = defaultdict(list)
        for r in terr.values():
            bands[r[key + "_tier"]].append(r)
        print(f"--- {label} territory tiers")
        for tier in "ABCD":
            rs = sorted(bands[tier], key=lambda r: -r[key + "_score"])
            print(f"  {tier} ({len(rs):2}): " + ", ".join(f"{r['abbr']} {r[key+'_score']:.0f}" for r in rs))
    print()
    inbook = sorted((r for r in terr.values() if r["in_book_state_accounts"] + r["in_book_local_accounts"]),
                    key=lambda r: -r["blended_score"])
    print(f"{'':4} {'blend':>6} {'state':>13} {'local':>13} {'ARR':>12} {'accts':>6}  conf")
    for r in inbook:
        print(f"{r['abbr']:4} {r['blended_score']:6.1f} "
              f"{r['state_side_tier']:>7} {r['state_side_score']:5.1f} "
              f"{r['local_side_tier']:>7} {r['local_side_score']:5.1f} "
              f"${r['state_arr']+r['local_arr']:11,.0f} "
              f"{r['in_book_state_accounts']+r['in_book_local_accounts']:6}  {r['confidence']}")
    print()
    tot = defaultdict(lambda: [0, 0.0])
    for a in book:
        if a["countable"] and a["tier"]:
            tot[a["tier"]][0] += 1
            tot[a["tier"]][1] += a["arr"]
    for t in (1, 2, 3, 4):
        n, arr = tot[t]
        print(f"Tier {t} {TIER_LABEL[t]:<14} {n:4} accounts  ${arr:12,.0f}")
    print()
    print(f"{'XP':<22} {'lvl':<8} {'cnt':>4} {'T1':>3} {'T2':>3} {'T3':>3} {'T4':>3} "
          f"{'grw%':>6} {'load':>6} {'ARR':>12} {'defendARR':>12}")
    for xp, r in sorted(xp_new.items(), key=lambda kv: -kv[1]["growth_load"]):
        print(f"{xp:<22} {str(r['level']):<8} {r['countable']:4} {r['t1']:3} {r['t2']:3} "
              f"{r['t3']:3} {r['t4']:3} {r['growth_share']*100:5.0f}% {r['growth_load']:6.1f} "
              f"${r['arr']:11,.0f} ${r['t3_arr']:11,.0f}")
    loads = [r["growth_load"] for r in xp_new.values()]
    print(f"\ngrowth load: min {min(loads):.1f}  max {max(loads):.1f}  "
          f"spread {max(loads)/min(loads):.2f}x  mean {statistics.mean(loads):.1f}")


if __name__ == "__main__":
    main()
