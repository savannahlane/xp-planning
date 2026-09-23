#!/usr/bin/env python3
"""Apply the whole-team assignment corrections to index.html.

This script is intentionally narrow. It starts from the whole-team PAGE payload
that landed on main and changes only the proposed assignment (`newxp`):

* Jake Sager, Nathan Williamson, Savannah Lane, Kristen Murphy and Ashley Hill
  hold no proposed accounts.
* Ashley's seven current Enterprise accounts land with direct reports.
* Displaced Local SMG accounts move as whole AE groups to an XP who already
  works with that AE. This removes an XP↔AE edge instead of creating one.
* Carolina Prieto is labelled Team Lead, not Manager. She keeps the Kentucky
  and North Dakota enterprise agreements (two customers).

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

# Each destination already works with the AE in the main-branch proposal.
# Keeping an AE group intact removes the departing XP↔AE relationship without
# adding one for the recipient.
LOCAL_SMG_DESTINATION = {
    "Local SMG FL (Ter 4)": "Natalia Sanchez",
    "Jared Cummings": "David Treminio",
    "Caleb Fort Jr": "Kerrian Dailey",
    "Tommy Monaghan": "Carlos Torres",
    "Brittany Greer": "Marcy Castro",
    "Local SMG CA (Ter 8)": "Eduardo Ruiz",
    "John Meah": "Cody Nichols",
    "Kimberley Steelmann": "Andrés Pérez",
    "Amanda Brooks": "David Treminio",
    "Local SMG Ter 6 (TX/OK/AR)": "Kerrian Dailey",
    "Emery Herrschel": "Kerrian Dailey",
    "Jeffrey Johnson": "Andrés Pérez",
    "Luke Mulvaney": "Carlos Torres",
}

# Kentucky COT and North Dakota ITD are the billed parents of statewide
# enterprise agreements. Sister agency rows travel with them and do not
# consume a countable slot.
EA_PARENTS = {
    "Kentucky Commonwealth Office of Technology",
    "North Dakota Information Technology Department",
}

ENTERPRISE_SEGMENTS = {"State", "Local ENT"}


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


def apply_assignments(page: dict, overrides: dict[str, dict]) -> dict:
    rows = page["rows"]
    before_edges = proposed_edges(rows)
    carolina_countable = EA_PARENTS | {
        account
        for account, override in overrides.items()
        if override["xp"] == "Carolina Prieto"
    }

    # The open Pacific XP is an Ashley report. That preserves the coherent,
    # single-XP California State AE groups while satisfying the reporting rule.
    page["meta"]["Open XP2 (PT)"][0] = "Ashley Hill"
    page["meta"]["Carolina Prieto"] = ["—", "—", "Team Lead", "Not specified"]

    moved = []
    matched = set()
    for row in rows:
        old = row["newxp"]

        if row["segment"] == "Local SMG" and old in NO_BOOK:
            try:
                row["newxp"] = LOCAL_SMG_DESTINATION[row["person"]]
            except KeyError as exc:
                raise RuntimeError(
                    f"No destination for displaced AE group {row['person']!r}"
                ) from exc

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

        # Kentucky and North Dakota are statewide enterprise agreements, so the
        # sister agencies travel with the billed parent instead of consuming a
        # countable slot of their own.
        if row["state"] in {"KY", "ND"} and (
            old == "Carolina Prieto" or row["newxp"] == "Carolina Prieto"
        ):
            row["newxp"] = "Carolina Prieto"
            if row["acct"] not in carolina_countable:
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

    # Hard validations: fail loudly instead of publishing a subtly wrong map.
    for xp in NO_BOOK:
        assigned = [r["acct"] for r in rows if r["newxp"] == xp]
        if assigned:
            raise RuntimeError(f"{xp} still has proposed accounts: {assigned}")

    ashley_enterprise = [
        r for r in rows if r["cur"] == "Ashley Hill" and r.get("ent")
    ]
    bad = [r for r in ashley_enterprise if r["newxp"] not in ASHLEY_REPORTS]
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

    after_edges = proposed_edges(rows)
    return {
        "moved": moved,
        "removed": removed,
        "before_edges": before_edges,
        "after_edges": after_edges,
        "ashley_enterprise": ashley_enterprise,
        "carolina_countable": carolina_rows,
    }


def update_markup(source: str) -> str:
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

    if "enterprise agreements (two customers" not in source:
        source = source.replace(
            "Halena retains the broader Connecticut estate.</li>",
            "Halena retains the broader Connecticut estate.</li>\n"
            "      <li>Carolina Prieto keeps the Kentucky and North Dakota statewide "
            "enterprise agreements (two customers; sister agencies are allocated "
            "children), plus CHFS, Homeland Security and Transportation for Kentucky "
            "consolidation. She releases scattered local accounts to XPs who already "
            "work with those AEs. Glendale AZ is the exception: Conrad Taylor has no "
            "other book, so it goes to Colleen with her other Pacific SAM work.</li>\n"
            "      <li>Local SMG includes special districts except SAM territories. "
            "GLAVCD stays Enterprise with Colleen. Luke Mulvaney's three districts "
            "sit with Carlos Torres so Halena is not paired with that vertical.</li>",
        )

    source = source.replace(
        "Savannah Lane, Kristen Murphy and Ashley Hill carry no accounts in the "
        "proposed book.",
        "Jake Sager, Nathan Williamson, Savannah Lane, Kristen Murphy and Ashley "
        "Hill carry no accounts in the proposed book.",
    )
    source = source.replace(
        "The proposed view removes account books from Savannah Lane, Kristen "
        "Murphy and Ashley Hill; the current view remains historical.",
        "The proposed view removes account books from Jake Sager, Nathan "
        "Williamson, Savannah Lane, Kristen Murphy and Ashley Hill; the current "
        "view remains historical.",
    )
    source = source.replace(
        "enterprise agreements (two customers; sister agencies are allocated "
        "children) and releases the scattered local accounts",
        "enterprise agreements (two customers; sister agencies are allocated "
        "children), plus CHFS, Homeland Security and Transportation for Kentucky "
        "consolidation. She releases scattered local accounts",
    )
    source = source.replace(
        "Luke Mulvaney's three districts sit with one SMG XP so Halena is not "
        "paired with that vertical.",
        "Luke Mulvaney's three districts sit with Carlos Torres so Halena is not "
        "paired with that vertical.",
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
    print(
        "XP↔AE edges: "
        f"{len(result['before_edges'])} → {len(result['after_edges'])} "
        f"({len(result['after_edges']) - len(result['before_edges']):+d})"
    )
    for xp in sorted(NO_BOOK):
        print(f"{xp}: 0 proposed accounts")
    print("Ashley's Enterprise destinations:")
    for row in result["ashley_enterprise"]:
        print(f"  {row['acct']} → {row['newxp']}")
    print("Carolina countable consolidated accounts:")
    for row in result["carolina_countable"]:
        print(f"  {row['acct']} ${row['arr']:.0f}")


if __name__ == "__main__":
    main()
