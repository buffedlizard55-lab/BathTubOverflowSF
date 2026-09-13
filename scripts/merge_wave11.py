#!/usr/bin/env python3
"""Fail-closed merge for wave 11."""
from __future__ import annotations
import hashlib, json, re, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WAVE = ROOT / "data" / "wave11.json"
TARGET = ROOT / "data" / "research.json"
DATE = "2026-09-12"
STATUSES = {"active", "expired", "canceled", "inactive", "suspended", "revoked"}
NONACTIVE = STATUSES - {"active"}
KINDS = {"business", "community", "directory", "government", "platform", "testimonial"}
ACCESS = {"page", "search-extract", "blocked-with-search-extract", "redirect", "expired-site", "review-panel-unavailable"}
CLASSES = {"A", "B", "B-2", "C-2", "C-4", "C4", "C10", "C12", "C15", "C16", "C20", "C22", "C27", "C29", "C33", "C35", "C36", "C38", "C39", "C42", "C43", "C45", "C54", "D34", "D39", "D56", "C-7", "C-9"}
TRADES = {
    "plumbing": [["C36"]], "drywall": [["C-9"], ["B"]], "plaster": [["C35"], ["B"]],
    "finish": [["C-9"], ["C35"], ["B"]], "general": [["B"]], "engineering": [["A"]],
    "multi-trade": [["B", "C36"]], "masonry": [["C29"]], "tile": [["C54"]],
    "plumbing-and-drywall": [["C-9", "C36"]], "scope-exclusion": [["A"], ["B"], ["C12"], ["C20"], ["C27"], ["C39"], ["C43"], ["C45"]],
    "registry-lead": [],
}
SUFFIXES = {"and", "co", "company", "corp", "corporation", "dba", "inc", "incorporated", "llc", "the", "of"}

def core(name):
    s = unicodedata.normalize("NFKD", name)
    return " ".join(x for x in re.sub(r"[^a-zA-Z0-9]+", " ", s).lower().split() if x not in SUFFIXES)

def digits(value): return re.sub(r"\D", "", value or "")
def license_fact(number, entity, classes, status, expires, source):
    return {"number": number, "entity": entity, "classes": classes, "status": status, "expires": expires, "checkedAt": DATE, "source": source}
def c(field, text, source, excerpt): return {"field": field, "text": text, "source": source, "excerpt": excerpt}
def f(level, text, sources): return {"level": level, "text": text, "sources": sources}
def fail(msg): raise SystemExit("MERGE REFUSED: " + msg)

def main():
    wave = json.loads(WAVE.read_text(encoding="utf-8"))
    data = json.loads(TARGET.read_text(encoding="utf-8"))
    bs, ss, rs, ups = wave["businesses"], wave["sources"], wave["reviews"], wave["upgrades"]
    if len(bs) != 50 or wave["composition"] != {"regulatorRead":42,"registryOnly":4,"platformListing":4,"verificationUpgrades":3}:
        fail("wave must contain exactly 50 records with 42/4/4 composition and three upgrades")
    if len({b["id"] for b in bs}) != 50 or len({b["name"].lower() for b in bs}) != 50: fail("wave IDs or names are not unique")
    old_ids = {b["id"] for b in data["businesses"]}
    old_names = {b["name"].strip().lower() for b in data["businesses"]}
    old_cores = {core(b["name"]) for b in data["businesses"]}
    old_phones = {digits(b.get("phone")) for b in data["businesses"] if b.get("phone")}
    old_lic = {b["license"]["number"] for b in data["businesses"] if b.get("license")}
    old_lic |= {u["licence"] for u in data.get("verificationUpgrades", [])}
    old_lic |= {u["licence"] for u in data.get("registryUpgrades", [])}
    old_sources = {s["id"] for s in data["sources"]}
    old_reviews = {r["id"] for r in data["reviews"]}
    for b in bs:
        if b["id"] in old_ids: fail(f"existing business id {b['id']}")
        if b["name"].strip().lower() in old_names or core(b["name"]) in old_cores: fail(f"name collision {b['name']}")
        if b["trade"] not in TRADES: fail(f"unknown trade {b['id']}")
        if len(b["claims"]) < 1 or len(b["gaps"]) < 2: fail(f"claims/gaps missing {b['id']}")
        for claim_obj in b["claims"]:
            if claim_obj["source"] not in {s["id"] for s in ss}: fail(f"claim source not in wave {b['id']}")
        for flag_obj in b["flags"]:
            if flag_obj["level"] not in {"hold", "discrepancy", "notice", "gap"}: fail(f"flag level {b['id']}")
            if not set(flag_obj["sources"]) <= {s["id"] for s in ss}: fail(f"flag source {b['id']}")
        if b["phone"] and digits(b["phone"]) in old_phones: fail(f"phone collision {b['id']}")
        if b.get("website"): fail(f"wave websites are not permitted {b['id']}")
        if b.get("license"):
            l = b["license"]
            if l["number"] in old_lic: fail(f"licence collision {b['id']}")
            if l["status"] not in STATUSES: fail(f"unknown licence status {b['id']}")
            if set(l["classes"]) - CLASSES: fail(f"unknown class {b['id']}")
            if l["status"] == "active" and not l["expires"] > DATE: fail(f"active licence not current after check {b['id']}")
            if not any(set(n) <= set(l["classes"]) for n in TRADES[b["trade"]]): fail(f"trade/class mismatch {b['id']}")
            if l["status"] != "active" and b["status"] not in {"hold", "excluded"} and not any(f["level"] == "hold" for f in b["flags"]): fail(f"non-active record not held {b['id']}")
            if l["source"] not in {s["id"] for s in ss}: fail(f"licence source {b['id']}")
            s = next(s for s in ss if s["id"] == l["source"])
            if s["kind"] != "government" or s["access"] != "page" or l["number"] not in s["url"]: fail(f"licence source is not a matching government page {b['id']}")
        elif b["trade"] == "registry-lead":
            if b.get("platformLinks"): fail(f"registry lead has platform link {b['id']}")
        elif not b.get("platformLinks"): fail(f"unlicensed non-lead has no platform link {b['id']}")
        if b["master"] or b["exactMatch"] or b["insuranceVerified"] or b["scopeConfirmed"] or b["priority"] is not None: fail(f"qualification asserted {b['id']}")
    if {s["id"] for s in ss} & old_sources or len({s["id"] for s in ss}) != len(ss): fail("source collision or duplicate")
    for s in ss:
        if s["kind"] not in KINDS or s["access"] not in ACCESS or not s["url"].startswith("https://") or s["checkedAt"] not in data["researchDates"]: fail(f"bad source metadata {s['id']}")
    if {r["id"] for r in rs} & old_reviews or len({r["id"] for r in rs}) != len(rs): fail("review collision or duplicate")
    for r in rs:
        if r["business"] not in {b["id"] for b in bs}: fail(f"review business {r['id']}")
        if len(r["quote"]) >= 500 or len(r["analysis"]) <= 30 or r["exactTask"] or r["platform"] == "Google": fail(f"review gate {r['id']}")
        if r["source"] not in {s["id"] for s in ss}: fail(f"review source {r['id']}")
    if {u["key"] for u in ups} != {"amx", "sugar-bear", "a1-plumbing"}: fail("upgrade target set")
    for u in ups:
        if u["key"] not in old_ids or u["source"] not in {s["id"] for s in ss}: fail(f"upgrade target/source {u['key']}")
        if u["status"] not in STATUSES or u["lic"] in old_lic: fail(f"upgrade licence {u['key']}")
        if u["status"] == "active" and not u["expires"] > DATE: fail(f"upgrade active expiry {u['key']}")
    data["sources"].extend(ss); data["businesses"].extend(bs); data["reviews"].extend(rs)
    data["waves"].append({"wave":11,"date":DATE,"count":50,"cslbReads":42,"registryOnly":4,"platformListings":4,"verificationUpgrades":3,"retainedReviewExcerpts":4})
    # Attach each regulator upgrade to the pre-existing record. Existing IDs and
    # discovery history are retained; the new CSLB fact is additive.
    for u in ups:
        b = next(b for b in data["businesses"] if b["id"] == u["key"])
        old_date = b.get("checkedAt")
        b["verifiedAt"] = DATE; b["checkedAt"] = DATE; b["previousCheckDates"] = [old_date] if old_date and old_date != DATE else []
        b["verification"] = {"licence":u["lic"],"entity":u["entity"],"form":u["form"],"status":u["status"],"expires":u["expires"],"classes":u["classes"],"phone":u["phone"],"address":u["address"],"issued":u["issued"],"statusText":u["status_text"],"note":u["note"],"apparentConflict":u["false_claim"],"checkedAt":DATE}
        b["license"] = license_fact(u["lic"], u["entity"], u["classes"], u["status"], u["expires"], u["source"])
        b["trade"] = "plumbing"; b["area"] = u["area"]; b["areaText"] = u["area_text"]; b["phone"] = u["phone"]; b["phoneSource"] = u["source"]
        b["claims"].append(c("Credential", f"CSLB detail page {u['lic']} was opened directly on {DATE}; it displays {u['entity']}, {', '.join(u['classes'])}, status {u['status']} and expiration {u['expires']}.", u["source"], f"License #{u['lic']} · {u['entity']} · {u['status']} · classes {', '.join(u['classes'])}"))
        b["claims"].append(c("Scope", "The regulator confirms C36 plumbing. Drywall service, Outer Sunset dispatch and exact-task experience remain unconfirmed.", u["source"], f"CSLB classes: {', '.join(u['classes'])}"))
        if u.get("hold") or u["status"] != "active":
            b["status"] = "hold"
            b["flags"].insert(0, f("hold", f"CSLB upgrade read shows licence {u['lic']} as {u['status']}; the record remains held.", [u["source"]]))
    data["verificationUpgrades"] = data.get("verificationUpgrades", []) + [{"record":u["key"],"licence":u["lic"],"date":DATE,"note":u["note"],"result":u["status"]} for u in ups]
    data["researchedAt"] = DATE
    data["scope"] = "Outer Sunset · repair-first bathtub plumbing research"
    # Keep the repository's neutral compliance position and add the three
    # verification passes without reproducing non-public project details.
    data["methodology"]["passes"] += " Pass 25 (wave 11, Sep 12 2026): adjacent-ZIP discovery pool queried from official SF DBI plumbing and building contact registries; 50 new records kept in regulator-read, registry-lead and platform-listing tiers; both required trades remain a hard qualification gate. Pass 26: line-by-line CSLB transcription and entity/phone/licence deduplication; non-active licences and classification mismatches held; source and privacy audit run. Pass 27: review attribution, source-link, area, trade-scope and promotion-gate audit; no record promoted and master remains empty."
    data["methodology"]["governmentSources"] += " Wave 11 read 42 additional CSLB detail pages, two complaint-disclosure pages and the official SF DBI plumbing/building contact registries for the adjacent 94112 pool. Registry leads remain unpromoted until the cited licence is read directly."
    payload = json.dumps(data, indent=1, ensure_ascii=False) + "\n"
    TARGET.write_text(payload, encoding="utf-8")
    print("merged wave 11", len(data["businesses"]), len(data["sources"]), len(data["reviews"]), hashlib.sha256(payload.encode()).hexdigest()[:16])

if __name__ == "__main__": main()
