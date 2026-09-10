#!/usr/bin/env python3
"""Fix two wave-3 data-integrity issues in research.json without re-merging:
  1. ensure every business has a platformLinks array (wave-3 records omitted it)
  2. remove any leftover 'R??' placeholder reviewIds (de-nola, reactic)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "data" / "research.json"
d = json.loads(p.read_text())

fixed_pl, fixed_r = 0, 0
for b in d["businesses"]:
    if not isinstance(b.get("platformLinks"), list):
        b["platformLinks"] = []
        fixed_pl += 1
    before = len(b.get("reviewIds", []))
    b["reviewIds"] = [rid for rid in b.get("reviewIds", []) if rid != "R??"]
    fixed_r += before - len(b["reviewIds"])

# referential safety: every review id referenced must exist and map back
review_ids = {r["id"] for r in d["reviews"]}
for b in d["businesses"]:
    for rid in b["reviewIds"]:
        assert rid in review_ids, (b["id"], rid)
        assert next(r for r in d["reviews"] if r["id"] == rid)["business"] == b["id"]

p.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
print(f"platformLinks added to {fixed_pl} businesses; removed {fixed_r} placeholder reviewIds")
