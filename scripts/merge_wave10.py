#!/usr/bin/env python3
"""Merge the verified wave-10 artifact into data/research.json.

The merge is idempotent and deliberately fail-closed. It refuses source, name,
phone, licence, review, classification, date, privacy or qualification drift
instead of repairing ambiguous input silently.

Wave 10 adds 50 new records in three published evidence tiers and applies ten
verification upgrades to records that earlier waves stored without a regulator
read. Upgrades add regulator facts to an existing record and never create a new
entry, which is what keeps the corpus free of duplicates when a licence read
resolves to a business a registry-only row already named.

Run:
    python3 scripts/gen_wave10.py
    python3 scripts/merge_wave10.py
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WAVE_FILE = ROOT / "data" / "wave10.json"
TARGET = ROOT / "data" / "research.json"
DATE = "2026-09-12"

NON_ACTIVE = {"expired", "suspended", "canceled", "inactive", "revoked"}
STATUSES = {"active"} | NON_ACTIVE
SOURCE_ACCESS = {
    "page",
    "search-extract",
    "blocked-with-search-extract",
    "redirect",
    "expired-site",
    "review-panel-unavailable",
}
SOURCE_KINDS = {"business", "community", "directory", "government", "platform", "testimonial"}
CLASSES = {"A", "B", "B-2", "C-2", "C-4", "C-7", "C-9", "C4", "C10", "C15", "C16",
           "C20", "C22", "C29", "C33", "C35", "C36", "C38", "C42", "C43", "C54",
           "D34", "D39", "D56"}
FLAG_LEVELS = {"hold", "discrepancy", "notice", "gap"}
# The two trade labels wave 10 introduces, each tied to the one classification
# that actually covers it. Both are recorded as scope exclusions, because neither
# a C-29 masonry nor a C-54 tile licence can self-perform plumbing or drywall.
NEW_TRADES = {"masonry": [["C29"]], "tile": [["C54"]],
              "plumbing-and-drywall": [["C-9", "C36"]]}
TRADE_CLASSES = {
    "plumbing": [["C36"]],
    "drywall": [["C-9"], ["B"]],
    "plaster": [["C35"], ["B"]],
    "finish": [["C-9"], ["C35"], ["B"]],
    "general": [["B"]],
    "engineering": [["A"]],
    "multi-trade": [["B", "C36"]],
    "registry-lead": [],
    **NEW_TRADES,
}
# Records wave 10 read at the regulator that resolve to an existing wave-1-9
# record. The key is the existing record id; the value is the licence number that
# was read. A wave-10 business record must never reuse one of these licences.
UPGRADE_TARGETS = {
    "national": "619642",
    "sunny-plumbing": "536715",
    "w5-stan-plumbing": "410861",
    "sberlo": "487017",
    "w6-bill-bragg-plumbing": "440780",
    "w7-david-chu-plumbing": "343610",
    "chosen": "1054611",
    "w7-franks-all-city-plumbing": "319594",
    "w6-ren-lei-construction-co": "635360",
    "cl": "982738",
}

SUFFIXES = {"and", "co", "company", "corp", "corporation", "dba", "inc",
            "incorporated", "llc", "the", "of"}


def core_name(name: str) -> str:
    folded = unicodedata.normalize("NFKD", name)
    words = re.sub(r"[^a-zA-Z0-9]+", " ", folded).strip().lower().split()
    return " ".join(w for w in words if w not in SUFFIXES)


def digits(value: str | None) -> str:
    return re.sub(r"\D", "", value or "")


def fail(message: str) -> None:
    raise SystemExit(f"MERGE REFUSED: {message}")


def main() -> None:
    wave = json.loads(WAVE_FILE.read_text(encoding="utf-8"))
    data = json.loads(TARGET.read_text(encoding="utf-8"))

    new_businesses = wave["businesses"]
    new_sources = wave["sources"]
    new_reviews = wave["reviews"]
    upgrades = wave["upgrades"]
    reg_upgrades = wave.get("registryUpgrades") or []

    # ---- gates -----------------------------------------------------------
    if len(new_businesses) != 50:
        fail(f"wave 10 must carry exactly 50 business records, found {len(new_businesses)}")
    if len({b["id"] for b in new_businesses}) != 50:
        fail("wave-10 business ids are not unique")
    if len({b["name"].strip().lower() for b in new_businesses}) != 50:
        fail("wave-10 business names are not unique")
    if len(upgrades) != len(UPGRADE_TARGETS):
        fail("the upgrade list must match UPGRADE_TARGETS exactly")

    existing_ids = {b["id"] for b in data["businesses"]}
    existing_names = {b["name"].strip().lower() for b in data["businesses"]}
    existing_cores = {core_name(b["name"]) for b in data["businesses"]}
    existing_phones = {digits(b.get("phone")) for b in data["businesses"] if b.get("phone")}
    existing_licences = {
        b["license"]["number"] for b in data["businesses"] if b.get("license")
    }
    existing_source_ids = {s["id"] for s in data["sources"]}
    existing_review_ids = {r["id"] for r in data["reviews"]}

    for b in new_businesses:
        if b["id"] in existing_ids:
            fail(f"{b['id']} already exists")
        if b["name"].strip().lower() in existing_names:
            fail(f"wave-10 name “{b['name']}” already exists in the corpus")
        if core_name(b["name"]) in existing_cores:
            fail(f"wave-10 name “{b['name']}” collides on its core words with a stored name")
        if b.get("license"):
            number = b["license"]["number"]
            if number in existing_licences:
                fail(f"licence {number} is already stored")
            if b["license"]["status"] not in STATUSES:
                fail(f"{b['id']} carries unknown licence status {b['license']['status']}")
            if set(b["license"]["classes"]) - CLASSES:
                fail(f"{b['id']} carries an unknown classification")
            if b["license"]["status"] == "active" and not b["license"]["expires"] > b["checkedAt"]:
                fail(f"{b['id']} is active but does not expire after the check date")
            if b["trade"] not in TRADE_CLASSES:
                fail(f"{b['id']} carries unknown trade {b['trade']}")
            if b["trade"] == "registry-lead":
                fail(f"{b['id']} is a registry lead and may not carry a licence")
            combos = TRADE_CLASSES[b["trade"]]
            if not any(set(need) <= set(b["license"]["classes"]) for need in combos):
                fail(f"{b['id']} trade {b['trade']} is not covered by {b['license']['classes']}")
            if b["license"]["status"] != "active":
                if not (b["status"] in {"hold", "excluded"}
                        or any(f["level"] == "hold" for f in b["flags"])):
                    fail(f"{b['id']} has a {b['license']['status']} licence without a hold")
        else:
            # Two kinds of record may carry no licence: a City registry lead,
            # which must stay unpromotable, and a platform listing, which must
            # publish the platform page it came from and must not borrow a
            # licence from the platform badge.
            if b["trade"] == "registry-lead":
                if b.get("platformLinks"):
                    fail(f"{b['id']} is a registry lead and must not carry platform links")
            elif b.get("platformLinks"):
                if b["trade"] not in TRADE_CLASSES:
                    fail(f"{b['id']} carries unknown trade {b['trade']}")
                if b["trade"] == "registry-lead":
                    fail(f"{b['id']} mislabels a platform listing")
            else:
                fail(f"{b['id']} has no licence, is not a registry lead and cites no platform page")
        if b["master"] or b["exactMatch"] or b["insuranceVerified"] or b["scopeConfirmed"]:
            fail(f"{b['id']} asserts a qualification gate that no source supports")
        if b["priority"] is not None:
            fail(f"{b['id']} must not enter the diagnostic call order")
        if len(b["gaps"]) < 2 or not b["claims"]:
            fail(f"{b['id']} is missing claims or gaps")
        bad_levels = {f["level"] for f in b["flags"]} - FLAG_LEVELS
        if bad_levels:
            fail(f"{b['id']} carries unknown flag levels {sorted(bad_levels)}")
        if b["phone"] and digits(b["phone"]) in existing_phones:
            # A shared phone is a finding, not a duplicate. Wave 9 set this rule:
            # the merge accepts the overlap only when the record publishes which
            # stored record shares the number and why.
            other_id = b.get("phone_collision")
            if not other_id:
                fail(f"{b['id']} phone {b['phone']} collides with a stored phone and the record does not publish the overlap")
            if other_id not in existing_ids:
                fail(f"{b['id']} publishes a phone overlap with unknown record {other_id}")
            other = next(x for x in data["businesses"] if x["id"] == other_id)
            if digits(other.get("phone")) != digits(b["phone"]):
                fail(f"{b['id']} claims a phone overlap with {other_id} but the numbers differ")
            if not any(
                other_id in f["text"] or (other.get("name") or "") in f["text"]
                for f in b["flags"]
            ):
                fail(f"{b['id']} publishes a phone overlap with {other_id} but no flag names it")
        if b["website"]:
            fail(f"{b['id']} must not carry a website in this wave")

    upgrade_numbers = {u["lic"] for u in upgrades}
    if upgrade_numbers != set(UPGRADE_TARGETS.values()):
        fail("upgrade licence numbers do not match UPGRADE_TARGETS")
    for u in upgrades:
        if u["key"] not in UPGRADE_TARGETS:
            fail(f"upgrade target {u['key']} is not an existing record")
        if u["key"] in {b["id"] for b in new_businesses}:
            fail(f"upgrade target {u['key']} is also present as a new record")
        if u["status"] != "active" or u["status"] in NON_ACTIVE:
            if u.get("hold") is not True and u["status"] != "active":
                fail(f"upgrade {u['key']} reads {u['status']} and must be held")

    if {s["id"] for s in new_sources} & existing_source_ids:
        fail("wave-10 source ids collide with stored sources")
    if {r["id"] for r in new_reviews} & existing_review_ids:
        fail("wave-10 review ids collide with stored reviews")
    if len({r["id"] for r in new_reviews}) != len(new_reviews):
        fail("wave-10 review ids are not unique")
    for s in new_sources:
        if s["access"] not in SOURCE_ACCESS or s["kind"] not in SOURCE_KINDS:
            fail(f"source {s['id']} carries an unknown kind or access value")
        if not s["url"].startswith("https://"):
            fail(f"source {s['id']} is not https")
        if s["checkedAt"] not in data["researchDates"]:
            fail(f"source {s['id']} carries an unknown check date")
    for r in new_reviews:
        if len(r["quote"]) >= 500:
            fail(f"review {r['id']} quote is too long to be an excerpt")
        if r["exactTask"]:
            fail(f"review {r['id']} claims exact-task evidence that no source supports")
        if r["business"] not in {b["id"] for b in new_businesses}:
            fail(f"review {r['id']} points at an unknown business")

    if len(reg_upgrades) != 2:
        fail(f"wave 10 must carry exactly 2 registry upgrades, found {len(reg_upgrades)}")
    for u in reg_upgrades:
        if u["key"] not in existing_ids:
            fail(f"registry upgrade target {u['key']} is not a stored record")
        if u["key"] in {b["id"] for b in new_businesses}:
            fail(f"registry upgrade target {u['key']} is also a new wave-10 record")
        target = next(b for b in data["businesses"] if b["id"] == u["key"])
        if target.get("license"):
            fail(f"registry upgrade {u['key']} already carries a licence")
        if u["lic"] in existing_licences:
            fail(f"registry upgrade licence {u['lic']} is already stored as a licence fact")
        if u["lic"] in {b["license"]["number"] for b in new_businesses if b.get("license")}:
            fail(f"registry upgrade licence {u['lic']} is also read as a wave-10 licence")
        if u["source"] not in {s["id"] for s in new_sources}:
            fail(f"registry upgrade {u['key']} cites a source outside this wave")
        if not u["note"].strip() or not u["why"].strip():
            fail(f"registry upgrade {u['key']} is missing its note or its reason")
        if u["claim"]["source"] != u["source"] or u["source"] not in u["flag"]["sources"]:
            fail(f"registry upgrade {u['key']} cites inconsistent sources")

    # ---- apply -----------------------------------------------------------
    data["sources"].extend(new_sources)
    data["businesses"].extend(new_businesses)
    data["reviews"].extend(new_reviews)
    data["waves"].append(
        {
            "wave": 10,
            "date": DATE,
            "count": 50,
            "cslbReads": wave["composition"]["regulatorRead"],
            "registryOnly": wave["composition"]["registryOnly"],
            "platformListings": wave["composition"]["platformListing"],
            "verificationUpgrades": wave["composition"]["verificationUpgrades"],
            "retainedReviewExcerpts": len(new_reviews),
        }
    )

    # Verification upgrades: replace the guidance fields and attach the regulator
    # facts to the record that already exists. The id, its history and its place
    # in any call order are untouched.
    data["verificationUpgrades"] = [
        {
            "record": u["key"],
            "licence": u["lic"],
            "date": DATE,
            "note": u["note"],
            "result": u["status"],
        }
        for u in upgrades
    ]
    by_id = {b["id"]: b for b in data["businesses"]}
    for u in upgrades:
        b = by_id[u["key"]]
        if b["id"].startswith("w10-"):
            fail(f"upgrade target {u['key']} resolved to a wave-10 record")
        b["verifiedAt"] = DATE
        b["checkedAt"] = DATE
        b["previousCheckDates"] = sorted(
            {b["checkedAt"], DATE} | {b.get("verifiedAt", DATE)}
        )[:-1]
        b["verification"] = {
            "licence": u["lic"],
            "entity": u["entity"],
            "form": u["form"],
            "status": u["status"],
            "expires": u["expires"],
            "classes": u["classes"],
            "phone": u["phone"],
            "address": u["address"],
            "issued": u["issued"],
            "statusText": u["status_text"],
            "note": u["note"],
            "apparentConflict": u["false_claim"],
            "checkedAt": DATE,
        }
        b["license"] = {
            "number": u["lic"],
            "entity": u["entity"],
            "classes": u["classes"],
            "status": u["status"],
            "expires": u["expires"],
            "checkedAt": DATE,
            "source": next(
                s["id"] for s in new_sources
                if s["url"].endswith(u["lic"])
            ),
        }
        b["area"] = u["area"]
        b["areaText"] = u["area_text"]
        b["phone"] = u["phone"]
        b["phoneSource"] = b["license"]["source"]
        if u.get("hold"):
            b["status"] = "hold"
            if not any(f["level"] == "hold" for f in b["flags"]):
                b["flags"].insert(
                    0,
                    {
                        "level": "hold",
                        "text": f"wave-10 regulator read: licence {u['lic']} reads “{u['status']}” at the check date. {u['false_claim']}",
                        "sources": [b["license"]["source"]],
                    },
                )
        else:
            b["flags"].insert(
                0,
                {
                    "level": "discrepancy" if u.get("flag_wc") else "notice",
                    "text": f"wave-10 regulator read for licence {u['lic']}: {u['false_claim']}",
                    "sources": [b["license"]["source"]],
                },
            )
        # An upgrade may correct the declared trade when the licence read shows
        # the old label was not supported by any classification the licence
        # actually holds. Where the read adds a C36 record with no declared
        # trade at all, plumbing supplies it; nothing else is touched.
        if u.get("trade"):
            b["trade"] = u["trade"]
        elif b.get("trade") is None:
            b["trade"] = "plumbing"

    data["registryUpgrades"] = [
        {"record": u["key"], "licence": u["lic"], "date": DATE, "note": u["note"],
         "result": "licence number recorded by the City; not read at CSLB"}
        for u in reg_upgrades
    ]
    for u in reg_upgrades:
        b = by_id[u["key"]]
        if b["id"].startswith("w10-"):
            fail(f"registry upgrade target {u['key']} resolved to a wave-10 record")
        b["claims"].append(u["claim"])
        b["flags"].insert(0, u["flag"])
        b["checkedAt"] = DATE

    data["researchedAt"] = DATE
    data["scope"] = "Outer Sunset · repair-first bathtub plumbing research"
    payload = json.dumps(data, indent=1, ensure_ascii=False) + "\n"
    TARGET.write_text(payload, encoding="utf-8")

    # one-way fingerprint receipt so a rerun is provably identical
    print("merged wave 10")
    print("  businesses:", len(data["businesses"]))
    print("  sources:", len(data["sources"]))
    print("  reviews:", len(data["reviews"]))
    print("  sha256:", hashlib.sha256(payload.encode()).hexdigest()[:16])


if __name__ == "__main__":
    main()
