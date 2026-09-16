#!/usr/bin/env python3
"""Merge data/wave15.json into research.json with fail-closed gates."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "research.json"
WAVE = ROOT / "data" / "wave15.json"
DATE = "2026-09-16"
ALLOWED_CLASSES = {
    "A", "B", "B-2", "C-2", "C-4", "C4", "C-7", "C-9", "C-10", "C10",
    "C12", "C15", "C16", "C20", "C22", "C27", "C29", "C33", "C35",
    "C36", "C-36", "C38", "C39", "C42", "C43", "C45", "C51", "C54",
    "D06", "D34", "D39", "D56",
}
NON_ACTIVE = {"expired", "inactive", "revoked", "canceled", "suspended"}

def fail(message: str) -> None:
    raise SystemExit(f"wave 15 merge refused: {message}")

def norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()

def core(value: str) -> str:
    drop = {"inc", "incorporated", "llc", "co", "company", "corp", "corporation", "construction", "contractor", "contractors", "general", "dba"}
    return " ".join(token for token in norm(value).split() if token not in drop)

def phone(value: str | None) -> str:
    return re.sub(r"\D", "", value or "")[-10:]

def main() -> int:
    data = json.loads(TARGET.read_text(encoding="utf-8"))
    wave = json.loads(WAVE.read_text(encoding="utf-8"))
    businesses = wave["businesses"]
    sources = wave["sources"]
    reviews = wave["reviews"]

    if data["researchedAt"] != "2026-09-16" or len(data["businesses"]) != 693 or len(data["waves"]) != 14:
        fail("target is not the reviewed pre-wave-15 snapshot")
    if wave["wave"] != 15 or wave["date"] != DATE or len(businesses) != 50:
        fail("artifact identity/count mismatch")
    expected = {"cslbReads": 0, "registryOnly": 35, "platformListings": 15,
                "activeLicenses": 0, "nonActiveLicenses": 0,
                "retainedReviewExcerpts": 3, "verificationPasses": 3}
    if wave["composition"] != expected:
        fail(f"composition mismatch: {wave['composition']}")

    old_ids = {b["id"] for b in data["businesses"]}
    old_names = {norm(b["name"]) for b in data["businesses"]}
    old_cores = {core(b["name"]) for b in data["businesses"]}
    old_licences = {str(b["license"]["number"]) for b in data["businesses"] if b.get("license")}
    old_numbers = set(re.findall(r"(?<!\d)\d{6,7}(?!\d)", json.dumps(data)))
    old_phones = {phone(b.get("phone")) for b in data["businesses"] if len(phone(b.get("phone"))) == 10}
    old_source_ids = {s["id"] for s in data["sources"]}
    old_review_ids = {r["id"] for r in data["reviews"]}
    new_source_ids = {s["id"] for s in sources}
    new_business_ids = {b["id"] for b in businesses}

    if len(new_business_ids) != 50 or new_business_ids & old_ids:
        fail("business id collision")
    if len({norm(b["name"]) for b in businesses}) != 50 or any(norm(b["name"]) in old_names for b in businesses):
        fail("normalized name collision")
    if len({core(b["name"]) for b in businesses}) != 50 or any(core(b["name"]) in old_cores for b in businesses):
        fail("normalized name-core collision")
    if len(new_source_ids) != len(sources) or new_source_ids & old_source_ids:
        fail("source id collision")
    if {r["id"] for r in reviews} & old_review_ids:
        fail("review id collision")

    seen_phones: set[str] = set()
    seen_licences: set[str] = set()
    seen_numbers: set[str] = set()
    for business in businesses:
        if business["priority"] or business["master"] or business["exactMatch"] or business["insuranceVerified"] or business["scopeConfirmed"]:
            fail(f"{business['id']} asserts a promotion gate")
        if len(business["claims"]) < 1 or len(business["gaps"]) < 2:
            fail(f"{business['id']} is missing evidence/gaps")
        if business["status"] not in {"research", "hold"}:
            fail(f"{business['id']} has unknown research status")
        p = phone(business.get("phone"))
        if p and (p in old_phones or p in seen_phones):
            fail(f"{business['id']} has a duplicate phone")
        if p:
            seen_phones.add(p)
        cited = {c["source"] for c in business["claims"]}
        cited |= {source for flag in business["flags"] for source in flag["sources"]}
        cited |= {link["source"] for link in business["platformLinks"]}
        if not cited <= new_source_ids:
            fail(f"{business['id']} cites unknown source(s): {cited - new_source_ids}")
        licence = business.get("license")
        if licence:
            number = str(licence["number"])
            if number in old_licences or number in old_numbers or number in seen_licences:
                fail(f"{business['id']} has a duplicate licence {number}")
            seen_licences.add(number)
            if licence["status"] not in {"active"} | NON_ACTIVE:
                fail(f"{business['id']} has unknown licence status")
            if set(licence["classes"]) - ALLOWED_CLASSES:
                fail(f"{business['id']} has unknown class")
            if licence["status"] == "active" and licence["expires"] <= DATE:
                fail(f"{business['id']} active licence is not future-dated")
            if licence["status"] != "active" and not any(f["level"] == "hold" for f in business["flags"]):
                fail(f"{business['id']} non-active licence is not held")
            source = next((s for s in sources if s["id"] == licence["source"]), None)
            if not source or source["kind"] != "government" or source["access"] != "page" or not source["url"].endswith(number):
                fail(f"{business['id']} licence source mismatch")
            if licence["checkedAt"] != DATE:
                fail(f"{business['id']} stale licence check date")
        else:
            if business["trade"] not in {"registry-lead", "platform-listing"}:
                fail(f"{business['id']} lacks a licence but asserts trade {business['trade']}")
            if not any(f["level"] == "hold" for f in business["flags"]):
                fail(f"{business['id']} unlicensed record is not held")
            # registry-only numbers must not collide with existing prose; platform listings skip this
            if business["trade"] == "registry-lead":
                claimed = business["id"].split("-")[-1]
                if claimed in old_numbers:
                    fail(f"{business['id']} registry number {claimed} collides with existing prose")
                if claimed in seen_numbers:
                    fail(f"{business['id']} duplicate registry number {claimed} within wave")
                seen_numbers.add(claimed)

    for source in sources:
        if source["checkedAt"] != DATE or not source["url"].startswith("https://"):
            fail(f"source {source['id']} is stale or not HTTPS")
        if source["access"] not in {"page", "search-extract", "blocked-with-search-extract", "redirect", "expired-site", "review-panel-unavailable"}:
            fail(f"source {source['id']} has unknown access")
    fingerprints = set()
    for review in reviews:
        if review["business"] not in new_business_ids or review["source"] not in new_source_ids:
            fail(f"review {review['id']} attribution/source mismatch")
        if review["exactTask"] or len(review["quote"]) >= 500:
            fail(f"review {review['id']} overstates exact-task evidence or is too long")
        fp = (review["business"], review["author"], review["quote"])
        if fp in fingerprints:
            fail(f"review {review['id']} duplicate fingerprint")
        fingerprints.add(fp)

    data["sources"].extend(sources)
    data["businesses"].extend(businesses)
    data["reviews"].extend(reviews)
    data["waves"].append({"wave": 15, "date": DATE, "count": 50, **wave["composition"]})
    data["researchedAt"] = DATE
    if DATE not in data["researchDates"]:
        data["researchDates"].append(DATE)

    data["methodology"]["passes"] += (
        " Pass 34 (wave 15, Sep 16 2026): building and plumbing 94122 grouped queries re-read via Socrata, "
        "including offset 500 low-count n=1 rows; 35 numbers not in existing 491-number prose retained as registry-only leads with license null. "
        "Pass 35: legal names, normalized cores, licence numbers and ten-digit phones compared with all 693 stored records; "
        "Tailwind, A R Plumbing and C & L Plumbing renamed to unique cores; Thumbtack drywall/plumbing categories and Yelp Outer Sunset search-extract checked, 3 excerpts attributable. "
        "Pass 36: fail-closed qualification audit, all 50 held, exactMatch false, insuranceVerified false, master false, privacy fingerprint preserved, no CSLB detail hallucinated, qualified master remains empty."
    )
    stored_licences = {str(b["license"]["number"]) for b in data["businesses"] if b.get("license")}
    cslb_pages = {
        re.search(r"LicNum=(\d+)", s["url"]).group(1)
        for s in data["sources"]
        if s["access"] == "page" and re.search(r"cslb\.ca\.gov.*LicenseDetail\.aspx\?LicNum=(\d+)", s["url"])
    }
    # Update governmentSources count if pattern matches
    data["methodology"]["governmentSources"] = re.sub(
        r"^CSLB license detail pages read directly \([^)]*\)",
        f"CSLB license detail pages read directly ({len(cslb_pages)} distinct detail pages; {len(stored_licences)} stored licence numbers; 0 read in wave 15)",
        data["methodology"]["governmentSources"], count=1,
    )
    data["methodology"]["governmentSources"] += (
        " Wave 15 added 0 new CSLB reads, 35 registry-only leads (32 building, 3 plumbing) and 15 platform listings, all held without promotion; "
        "registry numbers remain leads only and platform badges never become credentials."
    )

    if len(data["businesses"]) != 743 or len(data["sources"]) != 629 or len(data["reviews"]) != 162 or len(data["waves"]) != 15:
        fail(f"post-merge totals are not 743/629/162/15, got {len(data['businesses'])}/{len(data['sources'])}/{len(data['reviews'])}/{len(data['waves'])}")
    if data["master"] or any(b["master"] for b in data["businesses"]):
        fail("qualified master changed")

    TARGET.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("wave 15 merged: 50 businesses, 8 sources, 3 reviews")
    print(f"totals: {len(data['businesses'])} businesses · {len(data['sources'])} sources · {len(data['reviews'])} reviews · {len(data['waves'])} waves")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
