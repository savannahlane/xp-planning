#!/usr/bin/env python3
"""Apply the whole-team assignment corrections to index.html.

This script is intentionally narrow. It starts from the whole-team PAGE payload
that landed on main and changes only the proposed assignment (`newxp`):

* Savannah Lane, Kristen Murphy and Ashley Hill hold no proposed accounts.
* Ashley's seven current Enterprise accounts land with direct reports.
* Displaced Local SMG accounts move as whole AE groups to an XP who already
  works with that AE. This removes an XP↔AE edge instead of creating one.
* Carolina Prieto is labelled Team Lead, not Manager.

The current-assignment (`cur`) field is historical and is not rewritten.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"

NO_BOOK = {"Savannah Lane", "Kristen Murphy", "Ashley Hill"}
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
    "Kimberley Steelmann": "Jake Sager",
    "Amanda Brooks": "David Treminio",
    "Local SMG Ter 6 (TX/OK/AR)": "Kerrian Dailey",
    "Emery Herrschel": "Jake Sager",
    "Jeffrey Johnson": "Andrés Pérez",
}


def extract_page(source: str) -> tuple[dict, int, int]:
    start = source.index("const PAGE = ") + len("const PAGE = ")
    end = source.index(";\nconst ROWS_ALL", start)
    return json.loads(source[start:end]), start, end


def proposed_edges(rows: list[dict]) -> set[tuple[str, str]]:
    return {(r["newxp"], r["person"]) for r in rows if r.get("newxp")}


def apply_assignments(page: dict) -> dict:
    rows = page["rows"]
    before_edges = proposed_edges(rows)

    # The open Pacific XP is an Ashley report. That preserves the coherent,
    # single-XP California State AE groups while satisfying the reporting rule.
    page["meta"]["Open XP2 (PT)"][0] = "Ashley Hill"
    page["meta"]["Carolina Prieto"] = ["—", "—", "Team Lead", "Not specified"]

    moved = []
    for row in rows:
        old = row["newxp"]

        if row["segment"] == "Local SMG" and old in NO_BOOK:
            try:
                row["newxp"] = LOCAL_SMG_DESTINATION[row["person"]]
            except KeyError as exc:
                raise RuntimeError(
                    f"No destination for displaced AE group {row['person']!r}"
                ) from exc

        # This is the one Ashley Enterprise account that main sent outside her
        # reporting line. Halena keeps the other 39 Stephanie DelSignore rows;
        # the hold on the broader Connecticut estate is otherwise unchanged.
        if row["acct"] == "Connecticut Public Utilities Regulatory Authority [PURA],":
            row["newxp"] = "Steffany Amador"

        if row["newxp"] != old:
            moved.append((row["acct"], old, row["newxp"], row["person"]))

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

    after_edges = proposed_edges(rows)
    return {
        "moved": moved,
        "before_edges": before_edges,
        "after_edges": after_edges,
        "ashley_enterprise": ashley_enterprise,
    }


def update_markup(source: str) -> str:
    source = source.replace(
        "<title>XP ↔ AE alignment, Enterprise</title>",
        "<title>XP ↔ AE alignment, US team</title>",
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
        "The proposed view removes account books from Savannah Lane, Kristen "
        "Murphy and Ashley Hill; the current view remains historical.",
    )

    if "When those three books were removed" not in source:
        source = source.replace(
            "<li>Account counts exclude Allocated child records (they carry $0 and "
            "travel with the parent). ARR is the export's converted ARR.</li>",
            "<li>Account counts exclude Allocated child records (they carry $0 and "
            "travel with the parent). ARR is the export's converted ARR.</li>\n"
            "      <li>Savannah Lane, Kristen Murphy and Ashley Hill carry no accounts "
            "in the proposed book. Ashley's current Enterprise accounts route only "
            "to her reports; Carolina Prieto is a Team Lead, not a manager.</li>\n"
            "      <li>When those three books were removed, each displaced Local SMG "
            "AE group moved intact to an XP who already works with that AE. This "
            "strictly reduces coordination fan-out without creating a new relationship. "
            "The exception is Connecticut PURA: Ashley's reporting-line rule requires "
            "one additional Stephanie DelSignore relationship for Steffany while "
            "Halena retains the broader Connecticut estate.</li>",
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
    result = apply_assignments(page)

    source = source[:start] + json.dumps(page, separators=(", ", ": ")) + source[end:]
    source = update_markup(source)
    HTML.write_text(source)

    moved = result["moved"]
    print(f"moved {len(moved)} proposed account records")
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


if __name__ == "__main__":
    main()
