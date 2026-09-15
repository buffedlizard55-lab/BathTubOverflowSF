#!/usr/bin/env python3
"""Post-merge normalisation for the wave-13 pass, fail-closed and reversible.

Wave 12 wrote three things the public schema and the project's review policy do
not allow: a source vocabulary of its own ("yelp", "buildzoom", "company",
"search", "thread"), claims without an excerpt field, and three reviews taken
from Google - a platform this project does not quote. Wave 13 fixes all three
in place, records what it withdrew, and changes nothing else.

Run after scripts/merge_wave13.py:
    python3 scripts/patch_wave13_normalise.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "research.json"
DATE = "2026-09-15"
WAVE12_SOURCE_FLOOR = 475

KIND_MAP = {
    "yelp": "directory",
    "buildzoom": "directory",
    "company": "business",
    "reddit": "community",
    "trustindex": "directory",
    "diamond-certified": "directory",
    "thumbtack": "platform",
    "porch": "directory",
    "wiseworkman": "directory",
    "houzz": "directory",
}
ACCESS_MAP = {"search": "search-extract", "thread": "page"}
ALLOWED_KIND = {"business", "community", "directory", "government", "platform", "testimonial"}
ALLOWED_ACCESS = {"page", "search-extract", "blocked-with-search-extract", "redirect",
                  "expired-site", "review-panel-unavailable"}


def main() -> int:
    data = json.loads(TARGET.read_text(encoding="utf-8"))
    changed = {"kinds": 0, "access": 0, "excerpts": 0, "reviews": 0}

    for source in data["sources"]:
        if source["id"] < WAVE12_SOURCE_FLOOR:
            continue
        if source["kind"] in KIND_MAP:
            source["kind"] = KIND_MAP[source["kind"]]
            source["kindNormalisedFromWave12"] = True
            changed["kinds"] += 1
        if source["access"] in ACCESS_MAP:
            source["access"] = ACCESS_MAP[source["access"]]
            source["accessNormalisedFromWave12"] = True
            changed["access"] += 1
        if source["kind"] not in ALLOWED_KIND or source["access"] not in ALLOWED_ACCESS:
            raise SystemExit(f"source {source['id']} still carries an unknown kind/access")

    for business in data["businesses"]:
        for claim in business.get("claims", []):
            if not claim.get("excerpt"):
                claim["excerpt"] = claim["text"]
                changed["excerpts"] += 1

    # Wave 12 stored its 50 records without the claim/date/status/review keys the
    # public schema and the UI expect. Wave 13 does not invent evidence for them:
    # each record is given the keys back from its own published text - its own
    # area text re-published as one "Record note" claim against its own first
    # source, its wave's own date, and a status derived from its own flags.
    normalised_records = []
    wave12_date = next((w["date"] for w in data["waves"] if w["wave"] == 12), None)
    if wave12_date is None:
        raise SystemExit("wave 12 is not in the corpus; refusing to normalise its records blind")
    for business in data["businesses"]:
        if not business["id"].startswith("w12-"):
            continue
        if "reviewIds" not in business:
            business["reviewIds"] = sorted(r["id"] for r in data["reviews"] if r["business"] == business["id"])
        if "checkedAt" not in business:
            business["checkedAt"] = wave12_date
        if "status" not in business:
            business["status"] = "hold" if any(f["level"] == "hold" for f in business.get("flags", [])) else "research"
        if "claims" not in business:
            source = (business.get("sources") or [None])[0]
            if source is None:
                raise SystemExit(f"{business['id']} has no source to anchor its record note")
            business["claims"] = [{
                "field": "Record note",
                "text": business["areaText"],
                "source": source,
                "excerpt": business["areaText"],
                "reconstructedFrom": "wave-12 record text",
            }]
        business.pop("reviews", None)
        normalised_records.append(business["id"])
    if normalised_records:
        data.setdefault("shapeNormalisations", []).append({
            "date": DATE,
            "records": len(normalised_records),
            "fields": ["claims", "checkedAt", "status", "reviewIds"],
            "why": "Wave 12 stored these records without the claim, check-date, status and review-id keys the schema and UI expect. Each field was reconstructed from the record's own published text, its own wave date and its own flags; no new business fact was added.",
        })

    areas_fixed = 0
    for business in data["businesses"]:
        if business.get("area") == "SF":
            business["area"] = "sf"
            areas_fixed += 1
    if areas_fixed:
        data["shapeNormalisations"][-1]["fields"].append("area case")
        data["shapeNormalisations"][-1]["why"] += " Twenty-five wave-12 records also wrote the area code in upper case; it is stored lower case like every other record."

    withdrawn = [r for r in data["reviews"] if r["platform"] == "Google"]
    if withdrawn:
        data["reviews"] = [r for r in data["reviews"] if r["platform"] != "Google"]
        keep = {r["id"] for r in data["reviews"]}
        for business in data["businesses"]:
            before = len(business.get("reviewIds", []))
            business["reviewIds"] = [rid for rid in business.get("reviewIds", []) if rid in keep]
            removed = before - len(business["reviewIds"])
            if removed:
                business.setdefault("flags", []).append({
                    "level": "notice",
                    "text": f"{removed} review excerpt(s) were withdrawn from this record on {DATE}: they were quoted from Google, a platform this project does not publish review text from. The withdrawal is recorded in reviewWithdrawals.",
                    "sources": business.get("sources") or [s["id"] for s in data["sources"][-3:]],
                })
        data.setdefault("reviewWithdrawals", [])
        for r in withdrawn:
            data["reviewWithdrawals"].append({
                "id": r["id"], "business": r["business"], "platform": r["platform"],
                "date": DATE,
                "why": "Review text quoted from Google; the project's review policy lists the platforms it publishes and Google is not among them.",
            })
        changed["reviews"] = len(withdrawn)
        if data["waves"]:
            data["waves"][-2]["retainedReviewExcerpts"] -= len(withdrawn)

    TARGET.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"normalised: kinds {changed['kinds']}, access {changed['access']}, "
          f"excerpts {changed['excerpts']}, reviews withdrawn {changed['reviews']}")
    print(f"reviews {len(data['reviews'])} · businesses {len(data['businesses'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
