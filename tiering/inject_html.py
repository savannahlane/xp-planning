#!/usr/bin/env python3
"""Fold the tiering output into index.html.

Adds per-account tier fields to the ROWS literal and writes a TERRITORIES literal
next to it. Idempotent: re-run after build_tiering.py to refresh the page.

Run:  python3 tiering/build_tiering.py && python3 tiering/inject_html.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"

TIER_KEYS = ("tier", "tlab", "tt", "ts", "gp", "cd")


def main():
    src = HTML.read_text()
    tiering = json.loads((ROOT / "tiering" / "tiering.json").read_text())
    by_key = {(a["account"], a["state"]): a for a in tiering["accounts"]}

    m = re.search(r"const ROWS = (\[.*?\]);\n", src, re.S)
    rows = json.loads(m.group(1))

    for r in rows:
        for k in TIER_KEYS:
            r.pop(k, None)
        a = by_key.get((r["acct"], r["state"]))
        if not a or a["tier"] is None:
            continue
        r["tier"] = a["tier"]
        r["tlab"] = a["tier_label"]
        r["tt"] = a["territory_tier"]
        r["ts"] = a["territory_score"]
        r["gp"] = a["growth_potential"]
        r["cd"] = a["capability_data"]

    terr = {}
    for ab, t in tiering["territories"].items():
        terr[ab] = {
            "name": t["state"],
            "sT": t["state_side_tier"], "sS": t["state_side_score"],
            "lT": t["local_side_tier"], "lS": t["local_side_score"],
            "posture": t["posture"], "rdf": t["rdf_pct"], "cycle": t["budget_cycle"],
            "itmod": t["it_mod_signal"], "grants": t["grant_env"], "cliff": t["arpa_cliff"],
            "access": t["purchasing_access"], "taxcap": t["tax_cap_pressure"],
            "conf": t["confidence"],
            "addr": t["addressable_over_100k"], "held": t["local_accounts_held"],
            "nState": t["in_book_state_accounts"], "nLocal": t["in_book_local_accounts"],
            "pop": t["population"], "popChg": t["pop_pct_chg"], "mig": t["dom_mig_per_1k"],
        }

    block = (
        "const ROWS = " + json.dumps(rows, separators=(", ", ": ")) + ";\n"
        + "const TERR = " + json.dumps(terr, separators=(", ", ": ")) + ";\n"
        + "const TIERMETA = " + json.dumps(tiering["weights"]["growth_load"],
                                           separators=(", ", ": ")) + ";\n"
        + "const TIERCUTS = " + json.dumps(tiering["cuts"], separators=(", ", ": ")) + ";\n"
    )

    # Replace ROWS plus any previously injected literals, so re-running is idempotent.
    start, end = m.span()
    tail = src[end:]
    tail = re.sub(r"^const (TERR|TIERMETA|TIERCUTS) = .*?;\n", "", tail, count=3, flags=re.S | re.M)
    HTML.write_text(src[:start] + block + tail)

    tiers = [r.get("tier") for r in rows if r.get("tier")]
    print(f"index.html: {len(tiers)} of {len(rows)} rows tiered, {len(terr)} territories")


if __name__ == "__main__":
    main()
