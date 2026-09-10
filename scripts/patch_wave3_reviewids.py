#!/usr/bin/env python3
"""Patch reciprocal reviewIds for wave-3 reviews R34-R38 so the dataset's
referential-integrity test (each review's business must list it) holds.
This only adds review ids that were authored in wave3.json but not echoed
back onto the business record."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data" / "research.json"
d = json.loads(p.read_text())

add = {
    "toms-painters": "R34",
    "amadors-drywall": "R35",
    "swift-restoration": "R36",
    "fire-water-recovery": "R37",
    "gcd-restoration": "R38",
}
changed = 0
for b in d["businesses"]:
    if b["id"] in add and add[b["id"]] not in b["reviewIds"]:
        b["reviewIds"].append(add[b["id"]])
        changed += 1

# safety: every review must be referenced by its business
by_id = {b["id"]: b for b in d["businesses"]}
for r in d["reviews"]:
    assert r["id"] in {x for b in d["businesses"] for x in b["reviewIds"]}, r["id"]
    assert by_id[r["business"]]["reviewIds"].count(r["id"]) == 1

p.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
print(f"patched reciprocal reviewIds on {changed} businesses; total reviews {len(d['reviews'])}")
