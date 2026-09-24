#!/usr/bin/env python3
"""Apply the whole-team assignment corrections to index.html.

This script is intentionally narrow. It starts from the whole-team PAGE payload
that landed on main and changes only the proposed assignment (`newxp`):

* Jake Sager, Nathan Williamson, Savannah Lane, Kristen Murphy and Ashley Hill
  hold no proposed accounts.
* Ashley's seven current Enterprise accounts land with direct reports.
* Enterprise XPs carry no Local SMG accounts. Nine dedicated Local SMG XPs
  cover whole AE groups except the forced California and transportation splits.
* Carolina Prieto is labelled Team Lead, not Manager. She keeps only the Idaho
  and North Dakota state book (Scott Mark, including the ND enterprise agreement).
  Kentucky state, including the COT enterprise agreement, sits with Andy O'Brien.

Per-account moves live in account_overrides.csv, which is the file to edit when
an XP changes. It also carries segment changes and removals.

The current-assignment (`cur`) field is historical and is not rewritten.
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
# 16 of the 19 seats work with exactly one XP. California has 47 accounts and
# must split at the 30-account cap, so its placeholder seat is divided
# North/Central (Eduardo) and Southern (Tatiana). Luke Mulvaney's national
# transportation vertical is the other split: its TX account follows Luis,
# while NJ and OR stay with Carlos.
LOCAL_SMG_DESTINATION = {
    "Local SMG FL (Ter 4)": "Natalia Sanchez",
    "Local SMG Ter 6 (TX/OK/AR)": "Luis Aguilar",
    "Caleb Fort Jr": "Ricardo Castro",
    "Corey Andrade": "Carlos Torres",
    "Emery Herrschel": "Kerrian Dailey",
    "Jared Cummings": "Kerrian Dailey",
    "Jeffrey Johnson": "David Treminio",
    "Kimberley Steelmann": "Andrés Pérez",
    "Amanda Brooks": "David Treminio",
    "Andrew Collinsworth": "Ricardo Castro",
    "Tommy Monaghan": "Carlos Torres",
    "Brittany Greer": "Kerrian Dailey",
    "John Meah": "Ricardo Castro",
    "Not on maps provided": "Andrés Pérez",
    "Prachi Patel": "Carlos Torres",
    "Michelle Cooper seat (open)": "Luis Aguilar",
}

LOCAL_SMG_XPS = {
    "Andrés Pérez",
    "Carlos Torres",
    "David Treminio",
    "Eduardo Ruiz",
    "Kerrian Dailey",
    "Luis Aguilar",
    "Natalia Sanchez",
    "Ricardo Castro",
    "Tatiana Montero",
}

# Provisional geographic cut of the four-seat California placeholder. The
# source payload does not identify its LA, Bay Area, San Diego and North/Central
# sub-seats, so this uses account geography and is intentionally explicit for
# review. Everything not named here goes to Eduardo's North/Central book.
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
    # Consolidating the remaining four accounts with her removes one AE split
    # and leaves Steffany at the 20-account maximum.
    "Cedric Simpkins": "Steffany Amador",
    # After the Marcy swap on main, Territory 4a continues to Taylor with the
    # rest of the NY/NJ local-and-state book rather than remaining a Midwest
    # attachment.
    "Territory 4a (open)": "Taylor Roman",
}

# Kent Hartsfield carries his own T11b OH/IN/IL territory plus the Chicago and
# Columbus SAM accounts on a temporary basis. Those two blocks now split: the
# SAM accounts go to Halena in account_overrides.csv and T11b stays with Marcy,
# which is why this AE group is not in AE_OWNER above.
#
# Columbus is one of them and is a current Ashley Hill account, so the rule that
# her Enterprise book routes only to her reports has to give way. Named here so
# the released hold is a deliberate, visible exception rather than silent drift.
ASHLEY_HOLD_RELEASED = {"Columbus OH"}

# New York and New Jersey state agencies sit with Taylor, including the
# DelSignore rows that would otherwise follow the AE_OWNER rule above.
NY_NJ_STATE_XP = "Taylor Roman"


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


def local_smg_destination(row: dict) -> str:
    """Return the canonical XP for one Local SMG account."""
    if row["person"] in {"Local SMG CA (Ter 8)", "Jaxson McBride"}:
        return (
            "Tatiana Montero"
            if row["acct"] in SOUTHERN_CA_LOCAL_SMG
            else "Eduardo Ruiz"
        )
    if row["person"] == "Luke Mulvaney":
        return "Luis Aguilar" if row["state"] == "TX" else "Carlos Torres"
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

    moved = []
    matched = set()
    for row in rows:
        old = row["newxp"]

        if old == "Nathan Williamson":
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
    page["rows"] = rows

    # Enterprise and Local SMG are separate books. Once every other rule has
    # run, apply the canonical nine-XP Local SMG cut. This is unconditional so
    # reruns converge after older per-account balancing overrides and after the
    # source PAGE has already been rewritten once.
    enterprise_xps = {r["newxp"] for r in rows if r.get("ent") and not r["alloc"]}
    offloaded = []
    for row in rows:
        if row["segment"] != "Local SMG":
            continue
        destination = local_smg_destination(row)
        if row["newxp"] != destination:
            offloaded.append((row["acct"], row["newxp"], destination))
            moved.append((row["acct"], row["newxp"], destination, row["person"]))
            row["newxp"] = destination

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
        if r["state"] not in {"ID", "ND"}
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
        "ashley_enterprise": ashley_enterprise,
        "carolina_countable": carolina_rows,
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
        "The proposed view removes account books from Jake Sager, Nathan "
        "Williamson, Savannah Lane, Kristen Murphy and Ashley Hill; the "
        "current view remains historical.",
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
        "The proposed view removes account books from Jake Sager, Nathan "
        "Williamson, Savannah Lane, Kristen Murphy and Ashley Hill; the current "
        "view remains historical.",
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
        "cap permits. Tatiana Montero holds Southern California, Eduardo Ruiz holds "
        "North/Central California, Luis Aguilar holds Texas, and Ricardo Castro "
        "holds the Southeast and Mid-Atlantic. California's 47 accounts force its "
        "placeholder AE seat to split; Luke Mulvaney's Texas account follows Luis "
        "while his New Jersey and Oregon accounts stay with Carlos Torres.",
    )
    source = source.replace(
        "Luke Mulvaney's three districts sit with Carlos Torres so Halena is not "
        "paired with that vertical.",
        "Luke Mulvaney's Texas district sits with Luis Aguilar; his New Jersey and "
        "Oregon districts stay with Carlos Torres.",
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
    print("Carolina countable consolidated accounts:")
    for row in result["carolina_countable"]:
        print(f"  {row['acct']} ${row['arr']:.0f}")


if __name__ == "__main__":
    main()
