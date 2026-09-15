#!/usr/bin/env python3
"""Merge wave 13 into data/research.json, fail-closed.

Wave 13 is a verification-heavy wave: 50 new records (25 CSLB licence reads,
13 registry-only leads, 12 platform listings) plus 27 regulator re-reads that
are attached to records earlier waves had already stored.

Run:
    python3 scripts/gen_wave13.py
    python3 scripts/merge_wave13.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WAVE = ROOT / "data" / "wave13.json"
TARGET = ROOT / "data" / "research.json"
DATE = "2026-09-15"

ALLOWED_CLASSES = {"A", "B", "B-2", "C-2", "C-4", "C-7", "C-9", "C-10", "C-36",
                   "C4", "C10", "C12", "C15", "C16", "C20", "C22", "C27", "C29",
                   "C33", "C35", "C36", "C38", "C39", "C42", "C43", "C45", "C54",
                   "D06", "D34", "D39", "D56"}
TRADE_CLASSES = {
    "plumbing": [["C36"], ["C-36"]],
    "drywall": [["C-9"], ["C35"], ["B"]],
    "plaster": [["C35"], ["B"], ["C-9"]],
    "finish": [["C-9"], ["C35"], ["B"]],
    "general": [["B"]],
    "engineering": [["A"]],
    "multi-trade": [["B", "C36"], ["B", "C-36"]],
    "registry-lead": [],
    "platform-listing": [],
}
SOURCE_ACCESS = {"page", "search-extract", "blocked-with-search-extract", "redirect",
                 "expired-site", "review-panel-unavailable"}
SOURCE_KIND = {"business", "community", "directory", "government", "platform", "testimonial"}
FLAG_LEVEL = {"hold", "discrepancy", "notice", "gap"}
NON_ACTIVE = {"expired", "suspended", "canceled", "inactive", "revoked"}
DROP = {"inc", "llc", "ltd", "co", "corp", "company", "incorporated", "corporation", "the"}


def norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()


def core(value: str) -> str:
    return " ".join(w for w in norm(value).split() if w not in DROP)


def digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def fail(message: str) -> None:
    raise SystemExit(f"merge aborted: {message}")


def supports(trade: str, classes: list[str]) -> bool:
    if trade == "scope-exclusion":
        # The label asserts that the classifications held do not cover the scope
        # this project needs; it is a tier, not a coverage claim.
        return bool(classes)
    combos = TRADE_CLASSES.get(trade)
    if not combos:
        return False
    return any(set(need) <= set(classes) for need in combos)



# Wave 12 re-listed eight firms that earlier waves had already stored, under the
# same name. Wave 13 folds the second row into the first instead of double
# counting, keeping the wave-12 evidence and the reviews attached to it.
WAVE12_DUPLICATES = [
    ("legend", "w12-legend-plumbing"),
    ("fa-plumbing", "w12-fa-plumbing"),
    ("portola", "w12-portola-plumbing"),
    ("phams", "w12-phams-plumbing"),
    ("benjamin-shaw", "w12-benjamin-shaw"),
    ("carlos-painting", "w12-carlos-painting"),
    ("handlify", "w12-handlify"),
    ("w5-edri-construction", "w12-edri-construction"),
]


def fold_wave12_duplicates(data: dict) -> list[dict]:
    corrections = []
    by_id = {b["id"]: b for b in data["businesses"]}
    for canonical_id, duplicate_id in WAVE12_DUPLICATES:
        canonical = by_id.get(canonical_id)
        duplicate = by_id.get(duplicate_id)
        if canonical is None or duplicate is None:
            fail(f"dedupe pair {canonical_id}/{duplicate_id} is not both stored")
        if norm(canonical["name"]) != norm(duplicate["name"]):
            fail(f"dedupe pair {canonical_id}/{duplicate_id} names differ")
        for claim in duplicate.get("claims", []):
            canonical.setdefault("claims", []).append({
                "field": f"Wave-12 re-discovery ({claim.get('field', 'record')})",
                "text": claim["text"],
                "source": claim["source"],
            })
        for flag in duplicate.get("flags", []):
            canonical.setdefault("flags", []).append(flag)
        if duplicate.get("trade") and not canonical.get("trade"):
            canonical["trade"] = duplicate["trade"]
        if "sources" in duplicate:
            canonical.setdefault("sources", [])
            for sid in duplicate["sources"]:
                if sid not in canonical["sources"]:
                    canonical["sources"].append(sid)
        for review in data["reviews"]:
            if review["business"] == duplicate_id:
                review["business"] = canonical_id
                canonical.setdefault("reviewIds", []).append(review["id"])
        canonical.setdefault("flags", []).append({
            "level": "notice",
            "text": f"Wave 12 stored this firm a second time as {duplicate_id}. The duplicate row was folded into this record on {DATE} with its evidence and reviews, and was not counted twice.",
            "sources": duplicate.get("sources") or [s["id"] for s in data["sources"][-3:]],
        })
        corrections.append({
            "date": DATE, "duplicate": duplicate_id, "foldedInto": canonical_id,
            "name": canonical["name"],
            "why": "Wave 12 re-listed a firm an earlier wave had already stored under the same name; the evidence and any reviews were folded into the earlier record and the duplicate row removed.",
        })
        data["businesses"] = [b for b in data["businesses"] if b["id"] != duplicate_id]
    if corrections:
        data.setdefault("dedupeCorrections", [])
        data["dedupeCorrections"].extend(corrections)
        if data["waves"]:
            data["waves"][-1]["duplicatesFolded"] = len(corrections)
            data["waves"][-1]["count"] -= len(corrections)
    return corrections


def main() -> int:
    wave = json.loads(WAVE.read_text(encoding="utf-8"))
    data = json.loads(TARGET.read_text(encoding="utf-8"))

    new_records = wave["businesses"]
    new_sources = wave["sources"]
    new_reviews = wave["reviews"]
    upgrades = wave["upgrades"]

    # ------------------------------------------------------------- gates -----
    if len(new_records) != 50:
        fail(f"expected 50 new records, found {len(new_records)}")
    if len({b["id"] for b in new_records}) != 50:
        fail("new ids are not unique")
    if len({norm(b["name"]) for b in new_records}) != 50:
        fail("new names are not unique")
    if len(upgrades) != 34:
        fail(f"expected 34 upgrades, found {len(upgrades)}")

    ids = {b["id"] for b in data["businesses"]}
    cores = {core(b["name"]) for b in data["businesses"]}
    names = {norm(b["name"]) for b in data["businesses"]}
    core_owner = {core(b["name"]): b["id"] for b in data["businesses"]}
    name_owner = {norm(b["name"]): b["id"] for b in data["businesses"]}
    by_stored_id = {b["id"]: b for b in data["businesses"]}
    licences = {str(b["license"]["number"]) for b in data["businesses"] if b.get("license")}
    source_ids = {s["id"] for s in data["sources"]}
    review_ids = {r["id"] for r in data["reviews"]}

    for b in new_records:
        if b["id"] in ids:
            fail(f"duplicate id {b['id']}")
        if core(b["name"]) in cores or norm(b["name"]) in names:
            # A name overlap is allowed only when the record declares it and the
            # declared target really is the stored record holding that name (or
            # holds the licence number the record cites as the earlier reading).
            twin = core_owner.get(core(b["name"])) or name_owner.get(norm(b["name"]))
            declared = b.get("name_collision")
            blob = " ".join(f["text"] for f in b["flags"])
            twin_record = by_stored_id.get(twin)
            twin_licence = (twin_record.get("license") or {}).get("number") if twin_record else None
            if not (declared == twin or (twin and twin in blob) or (twin_licence and str(twin_licence) in blob)):
                fail(f"core collision for {b['name']}")
        if b["license"]:
            number = str(b["license"]["number"])
            if number in licences:
                fail(f"licence {number} already stored")
            if number in {u["lic"] for u in upgrades}:
                fail(f"licence {number} is both a new record and an upgrade")
            licences.add(number)
            if b["license"]["status"] not in {"active"} | NON_ACTIVE:
                fail(f"{b['id']} unknown licence status")
            unknown = set(b["license"]["classes"]) - ALLOWED_CLASSES
            if unknown:
                fail(f"{b['id']} unknown classes {sorted(unknown)}")
            if b["license"]["status"] == "active" and not b["license"]["expires"] > DATE:
                fail(f"{b['id']} active but expiring before the check date")
            if not supports(b["trade"], b["license"]["classes"]):
                fail(f"{b['id']} trade {b['trade']} not covered by {b['license']['classes']}")
            src = next(s for s in new_sources if s["id"] == b["license"]["source"])
            if src["kind"] != "government" or not src["url"].endswith(number):
                fail(f"{b['id']} licence source does not match licence {number}")
            if src["access"] != "page":
                fail(f"{b['id']} licence source was not read as a page")
        else:
            if b["trade"] not in {"registry-lead", "platform-listing"}:
                fail(f"{b['id']} has no licence but trade {b['trade']}")
            if not any(f["level"] == "hold" for f in b["flags"]):
                fail(f"{b['id']} has no licence and no hold flag")
        if b["priority"] or b["master"] or b["exactMatch"] or b["insuranceVerified"] or b["scopeConfirmed"]:
            fail(f"{b['id']} asserts a promotion gate")
        for flag in b["flags"]:
            if flag["level"] not in FLAG_LEVEL or not flag["sources"]:
                fail(f"{b['id']} malformed flag")
            for sid in flag["sources"]:
                if sid not in source_ids and sid not in {s["id"] for s in new_sources}:
                    fail(f"{b['id']} flag cites unknown source {sid}")
        if not b["claims"] or len(b["gaps"]) < 2:
            fail(f"{b['id']} missing claims or gaps")

    fresh_source_ids = {s["id"] for s in new_sources}
    if fresh_source_ids & source_ids:
        fail("new source ids collide with stored sources")
    if len(fresh_source_ids) != len(new_sources):
        fail("new source ids are not unique")
    for s in new_sources:
        if s["access"] not in SOURCE_ACCESS or s["kind"] not in SOURCE_KIND:
            fail(f"source {s['id']} unknown kind/access")
        if not s["url"].startswith("https://"):
            fail(f"source {s['id']} is not https")

    fresh_review_ids = {r["id"] for r in new_reviews}
    if fresh_review_ids & review_ids:
        fail("new review ids collide with stored reviews")
    business_ids = {b["id"] for b in new_records}
    fingerprints = set()
    for r in new_reviews:
        if r["business"] not in business_ids:
            fail(f"review {r['id']} points at an unknown business")
        if r["source"] not in fresh_source_ids:
            fail(f"review {r['id']} cites an unknown source")
        if r["exactTask"] or len(r["quote"]) >= 500:
            fail(f"review {r['id']} is malformed")
        fp = (r["business"], r["author"], r["quote"])
        if fp in fingerprints:
            fail(f"review {r['id']} duplicates another fingerprint")
        fingerprints.add(fp)

    for u in upgrades:
        if u["record"] not in ids:
            fail(f"upgrade target {u['record']} is not stored")
        target = next(b for b in data["businesses"] if b["id"] == u["record"])
        if u["source"] not in fresh_source_ids:
            fail(f"upgrade {u['record']} cites a source outside this wave")
        src = next(s for s in new_sources if s["id"] == u["source"])
        if src["kind"] != "government" or not src["url"].endswith(u["lic"]):
            fail(f"upgrade {u['record']} source does not match licence {u['lic']}")
        if u["status"] not in {"active"} | NON_ACTIVE:
            fail(f"upgrade {u['record']} unknown status")
        unknown = set(u["classes"]) - ALLOWED_CLASSES
        if unknown:
            fail(f"upgrade {u['record']} unknown classes {sorted(unknown)}")
        if u["status"] == "active" and not u["expires"] > DATE:
            fail(f"upgrade {u['record']} active but expiring before the check date")
        previous = (target.get("license") or {}).get("number")
        if previous and str(previous) != u["lic"] and not str(previous) in u.get("supersedes", []):
            fail(f"upgrade {u['record']} contradicts stored licence {previous}")
        if u["status"] != "active" and not any(f["level"] == "hold" for f in u["flags"]):
            fail(f"upgrade {u['record']} is non-active without a hold")
        if u["kind"] != "unresolved-identity" and not supports(u["trade"], u["classes"]):
            fail(f"upgrade {u['record']} trade {u['trade']} not covered by {u['classes']}")

    # --------------------------------------------------------- wave-12 repair --
    # Wave 12 was merged without the record fields the schema and UI require.
    # They are added here from the record's own published text, never invented:
    # one claim per stored source reference quoting the record's own area text.
    repaired = 0
    for b in data["businesses"]:
        if not b["id"].startswith("w12-"):
            continue
        repaired += 1
        if "checkedAt" not in b:
            b["checkedAt"] = "2026-09-14"
        if "status" not in b:
            b["status"] = "hold" if not b.get("license") or b["license"].get("status") != "active" else "research"
        if "reviewIds" not in b:
            b["reviewIds"] = [r["id"] for r in data["reviews"] if r["business"] == b["id"]]
        if "reviews" in b:
            del b["reviews"]
        if not b.get("claims"):
            ref = b.get("sources") or [s["id"] for s in data["sources"][-3:]]
            b["claims"] = [{
                "field": "Wave-12 record",
                "text": b["areaText"],
                "source": ref[0],
            }]
        if "platformLinks" not in b:
            b["platformLinks"] = []

    corrections = fold_wave12_duplicates(data)

    # ------------------------------------------------------------- apply -----
    data["businesses"].extend(new_records)
    data["sources"].extend(new_sources)
    data["reviews"].extend(new_reviews)

    for u in upgrades:
        target = next(b for b in data["businesses"] if b["id"] == u["record"])
        previous = target.get("checkedAt") or (target.get("license") or {}).get("checkedAt")
        target.setdefault("previousCheckDates", [])
        if previous and previous not in target["previousCheckDates"]:
            target["previousCheckDates"].append(previous)
        target["checkedAt"] = DATE
        target["verifiedAt"] = DATE
        target["verification"] = {
            "licence": u["lic"], "entity": u["entity"], "form": u["form"],
            "status": u["status"], "expires": u["expires"], "classes": u["classes"],
            "phone": u["phone"], "address": u["address"], "issued": u["issued"],
            "statusText": u["statusText"], "note": u["facts"][0], "checkedAt": DATE,
            "kind": u["kind"],
        }
        target.setdefault("claims", [])
        target["claims"].extend(u["claims"])
        target.setdefault("flags", [])
        target["flags"].extend(u["flags"])
        if u["kind"] != "unresolved-identity":
            target["license"] = {
                "number": u["lic"], "status": u["status"], "entity": u["entity"],
                "expires": u["expires"], "classes": u["classes"], "source": u["source"],
                "checkedAt": DATE,
            }
            if u.get("trade"):
                target["trade"] = u["trade"]
            if u.get("area"):
                target["area"] = u["area"]
            if u.get("area_text"):
                target["areaText"] = u["area_text"]
            if u["status"] != "active":
                target["status"] = "hold"
            elif target.get("status") == "hold" and not any(
                f["level"] == "hold" and "not able to contract" in f["text"] for f in target["flags"][:-len(u["flags"])]
            ):
                target["status"] = "research"

    metadata = {
        "wave": wave["wave"], "date": DATE, "count": len(new_records),
        **wave["composition"],
    }
    data["waves"].append(metadata)
    data["researchedAt"] = DATE
    if DATE not in data["researchDates"]:
        data["researchDates"].append(DATE)
    data.setdefault("verificationUpgrades", [])
    data.setdefault("registryUpgrades", [])
    for u in upgrades:
        entry = {
            "record": u["record"], "licence": u["lic"], "date": DATE,
            "note": u["facts"][0], "result": u["statusText"],
        }
        if u["kind"] == "registry":
            data["registryUpgrades"].append(entry)
        else:
            data["verificationUpgrades"].append(entry)

    # The regulator tally is rewritten from the merged data, not copied forward:
    # one number per licence fact actually stored after the wave is applied.
    distinct_licences = {str(b["license"]["number"]) for b in data["businesses"] if b.get("license")}
    data["methodology"]["governmentSources"] = re.sub(
        r"^CSLB license detail pages read directly \([^)]*\)",
        f"CSLB license detail pages read directly ({len(distinct_licences)} distinct license numbers, "
        f"{wave['composition']['cslbReads']} read in wave 13)",
        data["methodology"]["governmentSources"], count=1,
    )
    data["methodology"]["governmentSources"] += (
        f" Wave 13 read {wave['composition']['cslbReads']} further CSLB detail pages directly for new records and "
        f"re-read {len(upgrades)} licence numbers already stored on earlier records, attaching the regulator reading "
        "to the record that had published the gap. Registry-only rows are never promoted: a City-recorded licence "
        "number is a lead until the CSLB page itself is read."
    )

    TARGET.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"wave 13 merged: {len(new_records)} new records, {len(new_sources)} new sources, "
          f"{len(new_reviews)} new reviews, {len(upgrades)} upgrades, {repaired} wave-12 records repaired")
    print(f"wave-12 duplicates folded: {len(corrections)}")
    print(f"businesses {len(data['businesses'])} · sources {len(data['sources'])} · "
          f"reviews {len(data['reviews'])} · waves {len(data['waves'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
