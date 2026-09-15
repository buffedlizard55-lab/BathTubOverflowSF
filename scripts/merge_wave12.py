#!/usr/bin/env python3
"""Merge Wave 12 into the master research.json."""
import json

# Load existing data
with open("data/research.json") as f:
    research = json.load(f)

# Load wave 12
with open("data/wave12.json") as f:
    wave = json.load(f)

# Merge businesses
existing_ids = {b["id"] for b in research["businesses"]}
added = 0
for b in wave["businesses"]:
    if b["id"] not in existing_ids:
        research["businesses"].append(b)
        existing_ids.add(b["id"])
        added += 1

# Merge sources
existing_source_ids = {s["id"] for s in research["sources"]}
for s in wave["sources"]:
    if s["id"] not in existing_source_ids:
        research["sources"].append(s)
        existing_source_ids.add(s["id"])

# Merge reviews
existing_review_ids = {r["id"] for r in research["reviews"]}
for r in wave["reviews"]:
    if r["id"] not in existing_review_ids:
        research["reviews"].append(r)
        existing_review_ids.add(r["id"])

# Update metadata
research["researchedAt"] = wave["date"]
if "waves" not in research:
    research["waves"] = []
research["waves"].append({
    "wave": wave["wave"],
    "date": wave["date"],
    "count": wave["composition"]["platformListings"] + wave["composition"]["cslbReads"] + wave["composition"].get("buildZoomReads", 0),
    "cslbReads": wave["composition"]["cslbReads"],
    "buildZoomReads": wave["composition"].get("buildZoomReads", 0),
    "platformListings": wave["composition"]["platformListings"],
    "retainedReviewExcerpts": wave["composition"]["retainedReviewExcerpts"],
})

# Update wave count in business list
# Recount
print(f"Wave 12 merged: {added} new businesses added")
print(f"Total businesses: {len(research['businesses'])}")
print(f"Total sources: {len(research['sources'])}")
print(f"Total reviews: {len(research['reviews'])}")
print(f"Total waves: {len(research['waves'])}")

with open("data/research.json", "w") as f:
    json.dump(research, f, indent=2, ensure_ascii=False)

print("research.json updated.")
