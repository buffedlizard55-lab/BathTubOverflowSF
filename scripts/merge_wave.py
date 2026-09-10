#!/usr/bin/env python3
"""Merge a research wave file (e.g. data/wave2.json) into data/research.json.

Fail-closed: refuses to run if any structural invariant would break.
Never edits wave-1 records; never promotes anything to the qualified master.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "research.json"
ALLOWED_ACCESS = {
    "page",
    "search-extract",
    "blocked-with-search-extract",
    "redirect",
    "expired-site",
    "review-panel-unavailable",
}


def main(wave_paths):
    data = json.loads(TARGET.read_text())
    before = len(data["businesses"])
    for wave_path in wave_paths:
        wave = json.loads(Path(wave_path).read_text())
        src_ids = {s["id"] for s in data["sources"]}
        wave_src_ids = {s["id"] for s in wave["sources"]}
        assert not src_ids & wave_src_ids, "wave reuses an existing source id"
        valid = src_ids | wave_src_ids
        # invariants, checked before anything is written
        new_ids = [b["id"] for b in wave["businesses"]]
        old_ids = {b["id"] for b in data["businesses"]}
        assert len(new_ids) == len(set(new_ids)), "duplicate ids inside wave"
        assert not old_ids & set(new_ids), "wave reuses an existing business id"
        for b in wave["businesses"]:
            assert b["claims"] and b["claims"][0]["field"] == "Discovery", b["id"]
            assert len(b["gaps"]) >= 2, b["id"]
            assert b["checkedAt"] == data["researchedAt"], b["id"]
            assert b["master"] is False and b["exactMatch"] is False, b["id"]
            for c in b["claims"]:
                assert c["source"] in valid, (b["id"], c["source"])
                assert c["excerpt"].strip() and c["text"].strip(), b["id"]
            if b.get("website"):
                assert b["websiteSource"] in valid, b["id"]
            if b.get("phone"):
                assert b["phoneSource"] in valid, b["id"]
            if b.get("license"):
                lic = b["license"]
                assert lic["source"] in valid, b["id"]
                assert data["sources"] + wave["sources"]  # guard exists
                lic_src = next(
                    s for s in list(data["sources"]) + list(wave["sources"])
                    if s["id"] == lic["source"]
                )
                assert lic_src["kind"] == "government", b["id"]
                assert "cslb.ca.gov" in lic_src["url"], b["id"]
                assert "C36" in lic["classes"], b["id"]
                assert lic["entity"], b["id"]
                assert lic["checkedAt"] == data["researchedAt"], b["id"]
            for f in b.get("flags", []):
                assert f["sources"], b["id"]
        existing_reviews = {r["id"] for r in data["reviews"]}
        for r in wave["reviews"]:
            assert r["id"] not in existing_reviews, r["id"]
            assert r["business"] in set(new_ids), r["id"]
            assert r["source"] in valid, r["id"]
            assert len(r["quote"]) < 500 and len(r["analysis"]) > 30, r["id"]
            assert r["exactTask"] is False, r["id"]
        for s in wave["sources"]:
            assert s["access"] in ALLOWED_ACCESS, s["id"]
            assert s["checkedAt"] == data["researchedAt"], s["id"]
        # merge
        data["businesses"].extend(wave["businesses"])
        data["sources"].extend(wave["sources"])
        data["reviews"].extend(wave["reviews"])
        print(
            f"merged {wave_path}: +{len(wave['businesses'])} businesses, "
            f"+{len(wave['sources'])} sources, +{len(wave['reviews'])} reviews"
        )
    assert data["master"] == []
    assert not any(b["master"] for b in data["businesses"])
    assert not any(b.get("insuranceVerified") or b.get("scopeConfirmed") or b.get("exactMatch") for b in data["businesses"])
    data["schemaVersion"] = 2
    TARGET.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print(f"research.json now: {len(data['businesses'])} businesses, "
          f"{len(data['sources'])} sources, {len(data['reviews'])} reviews (schema v{data['schemaVersion']})")


if __name__ == "__main__":
    main(sys.argv[1:] or [str(ROOT / "data" / "wave2.json")])
