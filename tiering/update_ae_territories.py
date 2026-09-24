#!/usr/bin/env python3
"""Publish tiering/ae_territories.csv into index.html.

index.html shows two state lists for every AE: the assigned territory, which
comes from this CSV, and the states the AE actually holds accounts in, which the
page derives from the accounts themselves. This script writes the first list and
checks it against the second, so a territory that has drifted from the book is
visible here rather than only on the page.

Idempotent: re-run after editing the CSV.

Run:  python3 tiering/update_ae_territories.py
"""

from __future__ import annotations

import csv
import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"
TERRITORIES = Path(__file__).resolve().parent / "ae_territories.csv"

BEGIN = "// BEGIN AE_TERRITORY"
END = "// END AE_TERRITORY"

USPS = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI",
    "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN",
    "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH",
    "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA",
    "WV", "WI", "WY",
}


def load_territories(path: Path) -> dict[str, dict]:
    body = "\n".join(
        line for line in path.read_text().splitlines() if not line.startswith("#")
    )
    territories: dict[str, dict] = {}
    for record in csv.DictReader(io.StringIO(body)):
        ae = (record["ae"] or "").strip()
        if not ae:
            continue
        if ae in territories:
            raise RuntimeError(f"Duplicate territory row for {ae!r}")
        states = [s.strip().upper() for s in (record["states"] or "").split(",")]
        states = [s for s in states if s]
        unknown = [s for s in states if s not in USPS]
        if unknown:
            raise RuntimeError(f"{ae!r} has unknown state codes: {', '.join(unknown)}")
        if len(set(states)) != len(states):
            raise RuntimeError(f"{ae!r} lists a state twice")
        territories[ae] = {
            "states": sorted(states),
            "note": (record["note"] or "").strip(),
        }
    return territories


def extract_page(source: str) -> dict:
    start = source.index("const PAGE = ") + len("const PAGE = ")
    return json.loads(source[start : source.index(";\nconst ROWS_ALL", start)])


def render_block(territories: dict[str, dict]) -> str:
    lines = [
        BEGIN,
        "// Generated from tiering/ae_territories.csv. Edit that file, then run",
        "// python3 tiering/update_ae_territories.py. Do not edit this block by hand.",
        "const AE_TERRITORY = {",
    ]
    for ae in sorted(territories):
        lines.append(f" {json.dumps(ae)}: {json.dumps(territories[ae])},")
    lines += ["};", END]
    return "\n".join(lines)


def main() -> None:
    territories = load_territories(TERRITORIES)
    source = HTML.read_text()
    rows = extract_page(source)["rows"]

    book: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        if row["state"]:
            book[row["person"]].add(row["state"])
        else:
            book.setdefault(row["person"], set())

    missing = sorted(set(book) - set(territories))
    if missing:
        raise RuntimeError(
            "AEs on the map with no row in ae_territories.csv: " + ", ".join(missing)
        )

    if BEGIN not in source or END not in source:
        raise RuntimeError(f"index.html is missing the {BEGIN} / {END} markers")
    source = re.sub(
        re.escape(BEGIN) + r".*?" + re.escape(END),
        lambda _: render_block(territories),
        source,
        count=1,
        flags=re.S,
    )
    HTML.write_text(source)

    mapped = [ae for ae, t in territories.items() if t["states"]]
    print(
        f"{len(territories)} AE rows, {len(mapped)} with a state territory, "
        f"{len(territories) - len(mapped)} without"
    )

    off_map = sorted(set(territories) - set(book))
    if off_map:
        print("in the CSV but holding no accounts on the map: " + ", ".join(off_map))

    unlisted = sorted(ae for ae in book if not territories[ae]["states"])
    if unlisted:
        print(f"no state territory on file ({len(unlisted)}):")
        for ae in unlisted:
            states = ", ".join(sorted(book[ae])) or "no accounts"
            print(f"  {ae}: accounts in {states}")

    open_territory = {
        ae: sorted(set(territories[ae]["states"]) - book[ae])
        for ae in book
        if territories[ae]["states"] and set(territories[ae]["states"]) - book[ae]
    }
    if open_territory:
        print(f"territory states with no account in the book ({len(open_territory)}):")
        for ae, states in sorted(open_territory.items()):
            print(f"  {ae}: {', '.join(states)}")

    outside = {
        ae: sorted(book[ae] - set(territories[ae]["states"]))
        for ae in book
        if territories[ae]["states"] and book[ae] - set(territories[ae]["states"])
    }
    if outside:
        print(f"accounts outside the listed territory ({len(outside)}):")
        for ae, states in sorted(outside.items()):
            print(f"  {ae}: {', '.join(states)}")


if __name__ == "__main__":
    sys.exit(main())
