#!/usr/bin/env python3
"""Merge data/wave14.json into research.json with fail-closed gates."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "research.json"
WAVE = ROOT / "data" / "wave14.json"
DATE = "2026-09-16"
ALLOWED_CLASSES = {
    "A", "B", "B-2", "C-2", "C-4", "C4", "C-7", "C-9", "C-10", "C10",
    "C12", "C15", "C16", "C20", "C22", "C27", "C29", "C33", "C35",
    "C36", "C-36", "C38", "C39", "C42", "C43", "C45", "C51", "C54",
    "D06", "D34", "D39", "D56",
}
NON_ACTIVE = {"expired", "inactive", "revoked", "canceled", "suspended"}


def fail(message: str) -> None:
    raise SystemExit(f"wave 14 merge refused: {message}")


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

    if data["researchedAt"] != "2026-09-15" or len(data["businesses"]) != 643 or len(data["waves"]) != 13:
        fail("target is not the reviewed pre-wave-14 snapshot")
    if wave["wave"] != 14 or wave["date"] != DATE or len(businesses) != 50:
        fail("artifact identity/count mismatch")
    expected = {"cslbReads": 25, "registryOnly": 20, "platformListings": 5,
                "activeLicenses": 10, "nonActiveLicenses": 15,
                "retainedReviewExcerpts": 4, "verificationPasses": 3}
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
    data["waves"].append({"wave": 14, "date": DATE, "count": 50, **wave["composition"]})
    data["researchedAt"] = DATE
    data["researchDates"].append(DATE)

    data["methodology"]["passes"] += (
        " Pass 31 (wave 14, Sep 16 2026): 25 new CSLB detail pages opened and transcribed field by field, "
        "with each licence joined back to its official 94122 plumbing-contact row; 20 distinct building-contact "
        "rows and five current Thumbtack listings retained in separate registry-only and platform-only tiers. "
        "Pass 32: legal names, normalized cores, licence numbers and ten-digit phones compared with all 643 "
        "stored records; reissued entities and registry/regulator address, phone and name conflicts left as flags; "
        "Yelp, Thumbtack, Reddit, Google-indexed and BuildZoom evidence checked without reconstructing blocked text. "
        "Pass 33: status/classification and promotion-gate audit, review attribution, source-link and privacy checks, "
        "then Node, monitor, render and browser suites; no record promoted and the qualified master remains empty."
    )
    stored_licences = {str(b["license"]["number"]) for b in data["businesses"] if b.get("license")}
    cslb_pages = {
        re.search(r"LicNum=(\d+)", s["url"]).group(1)
        for s in data["sources"]
        if s["access"] == "page" and re.search(r"cslb\.ca\.gov.*LicenseDetail\.aspx\?LicNum=(\d+)", s["url"])
    }
    data["methodology"]["governmentSources"] = re.sub(
        r"^CSLB license detail pages read directly \([^)]*\)",
        f"CSLB license detail pages read directly ({len(cslb_pages)} distinct detail pages; {len(stored_licences)} stored licence numbers; 25 read in wave 14)",
        data["methodology"]["governmentSources"], count=1,
    )
    data["methodology"]["governmentSources"] += (
        " Wave 14 read 25 new CSLB pages and kept 20 additional building-registry numbers unpromoted. "
        "The wave's ten active and fifteen non-active regulator results remain separate from five platform listings; "
        "a registry number or platform badge never becomes a credential."
    )

    if len(data["businesses"]) != 693 or len(data["sources"]) != 621 or len(data["reviews"]) != 159 or len(data["waves"]) != 14:
        fail("post-merge totals are not 693/621/159/14")
    if data["master"] or any(b["master"] for b in data["businesses"]):
        fail("qualified master changed")

    TARGET.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("wave 14 merged: 50 businesses, 34 sources, 4 reviews")
    print(f"totals: {len(data['businesses'])} businesses · {len(data['sources'])} sources · {len(data['reviews'])} reviews · {len(data['waves'])} waves")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
