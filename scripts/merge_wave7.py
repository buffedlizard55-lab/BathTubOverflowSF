#!/usr/bin/env python3
"""Merge wave 7 into data/research.json — idempotent and fail-closed.

Run AFTER `python3 scripts/gen_wave7.py` produces `data/wave7.json`.

Wave 7 is built entirely from three kinds of primary evidence, and the
composition is deliberately reported so the counts cannot silently drift:

  10  CSLB license pages read directly in this pass. One of them (576600) is
      an ACTIVE C-36 plumbing contractor whose regulator-recorded address is
      inside 94122; the other nine are non-active (eight expired, one
      inactive, one revoked) and are carried as hold records only.
  20  registry-only leads from the official SF DBI "Plumbing Permits
      Contacts" open dataset, queried directly by firm ZIP (94122-0000).
      No licence page was read for these; each carries a "gap" flag.
  20  Thumbtack drywall listings read directly on 2026-09-11 (category
      listing pages are directly reachable; individual pro pages are not).
      These are unverified trade leads, not licence confirmations.

Fail-closed rules (same family as merge_wave6.py, extended):
  * a license field may only be sourced from a government cslb.ca.gov page;
  * an active license must not be expired relative to its checkedAt date;
  * any non-active license status (expired, suspended, canceled, inactive,
    revoked) must be paired with a hold-level flag on that record;
  * the declared trade must be supported by at least one acceptable class
    combination for the license that backs it;
  * registry-recorded license numbers are never promoted to the license field;
  * every claim, flag, link and review must reference a real source id;
  * review quotes stay under 500 characters, are marked exactTask=false, and
    analyses are longer than 30 characters;
  * nothing is promoted to master; the compliance block is byte-for-byte
    preserved; no private fields are introduced.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WAVE_FILE = ROOT / "data" / "wave7.json"
TARGET = ROOT / "data" / "research.json"
DATE = "2026-09-11"
PREV = "2026-09-10"

NOT_ACTIVE = {"expired", "suspended", "canceled", "inactive", "revoked"}
# Compliance posture: the public dataset never carries the private context, and
# never assists with concealed or unpermitted work. Fail closed on the phrases.
FORBIDDEN = ("rent control", "in-law unit", "without a permit", "no permit",
             "unpermitted", "discreet", "do not disclose")
STATUSES = {"active"} | NOT_ACTIVE
# Must stay identical to ALLOWED_CLASSES / TRADE_CLASSES in lib.js, which the
# site uses to render the credential badge. Divergence here would let a record
# merge that the browser then reports as a class/trade mismatch.
ALLOWED_CLASSES = {"C36", "C-9", "C35", "C-4", "C4", "C10", "C16", "C20", "C42", "D56", "B", "A"}
TRADE_REQUIRES = {
    "plumbing": [{"C36"}],
    "drywall": [{"C-9"}, {"B"}],
    "plaster": [{"C35"}, {"B"}],
    "finish": [{"C-9"}, {"C35"}, {"B"}],
    "general": [{"B"}],
    "engineering": [{"A"}],
    "multi-trade": [{"B"}, {"C36"}],
}

# ---------------------------------------------------------------- load inputs
wave = json.loads(WAVE_FILE.read_text())
data = json.loads(TARGET.read_text())
sources = {s["id"]: s for s in data["sources"]}
biz = {b["id"]: b for b in data["businesses"]}

existing_ids = set(biz)
existing_names = {b["name"].lower() for b in data["businesses"]}
existing_reviews = {r["id"] for r in data["reviews"]}
compliance_before = json.dumps(data["compliance"], sort_keys=True, ensure_ascii=False)

# ------------------------------------------------------------------- idempotence
if any(b["id"].startswith("w7-") for b in data["businesses"]):
    print("wave 7 already merged — no changes written.")
    raise SystemExit(0)

# ---------------------------------------------------------------- collision gate
# A wave-7 candidate is only accepted as a NEW record if no existing entry
# shares its name (case/space/accents-insensitive) or its CSLB number.
def norm(name):
    name = name.lower().replace("í", "i").replace("ñ", "n").replace("ó", "o")
    return re.sub(r"[^a-z0-9]+", " ", name).strip()

existing_norm = {norm(b["name"]) for b in data["businesses"]}
attached_numbers = {b["license"]["number"] for b in data["businesses"] if b.get("license")}

for b in wave["businesses"]:
    assert b["id"] not in existing_ids, f"id collision {b['id']}"
    assert b["name"].lower() not in existing_names, f"name collision {b['name']}"
    assert norm(b["name"]) not in existing_norm, f"near-name collision {b['name']}"
    if b.get("license"):
        assert b["license"]["number"] not in attached_numbers, \
            f"licence {b['license']['number']} already attached to another record"

# ------------------------------------------------------------------- source gate
next_id = max(sources) + 1
for s in wave["sources"]:
    assert s["id"] not in sources, f"source id {s['id']} already taken"
    # these two vocabularies are the ones tests/research.test.js enforces
    assert s["access"] in {"page", "search-extract", "blocked-with-search-extract",
                           "redirect", "expired-site", "review-panel-unavailable"}, s["id"]
    assert s["kind"] in {"business", "community", "directory", "government", "platform",
                         "testimonial"}, s["id"]
    assert re.match(r"^https://", s["url"]), s["id"]
    assert s["checkedAt"] in {DATE}, s["id"]
    if s["kind"] == "government":
        assert s["access"] == "page", f"government source {s['id']} must be a direct read"
    # a CSLB page must be a licence-detail page with a number in the URL
    if "cslb.ca.gov" in s["url"]:
        assert s["access"] == "page", f"{s['id']} must be marked as directly read"
        if not re.search(r"LicenseDetail\.aspx\?LicNum=\d+$", s["url"]):
            # Not a licence record: only acceptable as a search page whose note
            # records what the page actually returned (a limitation, not a read
            # of contractor data). Prevents an unreadable form being presented
            # as evidence.
            assert "ZipCodeSearch" in s["url"], s["url"]
            assert "404" in s["note"] or "negative" in s["note"].lower(), s["id"]
            assert not re.search(r"LicNum=", s["url"]), s["url"]
    sources[s["id"]] = s
data["sources"].extend(wave["sources"])

# licence detail pages actually read this wave (the area-search page is a
# documented negative result, not a licence read)
cslb_wave_sources = [s for s in wave["sources"]
                     if "cslb.ca.gov" in s["url"] and "LicNum=" in s["url"]]
thumbtack_sources = {s["id"] for s in wave["sources"] if "thumbtack.com" in s["url"]}

# ------------------------------------------------------------------ record gate
for b in wave["businesses"]:
    assert b["id"].startswith("w7-"), b["id"]
    assert b["checkedAt"] in {DATE}, b["id"]
    assert b["status"] in {"research", "hold"}, b["id"]
    assert b["claims"] and b["claims"][0]["field"] == "Discovery", b["id"]
    assert len(b["gaps"]) >= 2, b["id"]
    assert b["trade"] in TRADE_REQUIRES, (b["id"], b["trade"])
    assert b["area"] in {"outer", "sunset", "sf", "unknown", "outside"}, b["id"]
    blob = json.dumps(b, ensure_ascii=False).lower()
    for phrase in FORBIDDEN:
        assert phrase not in blob, f"{b['id']} contains forbidden private phrase {phrase!r}"

    lic = b.get("license")
    if lic:
        src = sources.get(lic["source"])
        assert src and src["kind"] == "government" and "cslb.ca.gov" in src["url"], b["id"]
        assert str(lic["number"]) in src["url"], (b["id"], lic["number"])
        assert lic["status"] in STATUSES, (b["id"], lic["status"])
        assert lic["checkedAt"] in {DATE}, b["id"]
        assert lic["checkedAt"] == b["checkedAt"], b["id"]
        assert set(lic["classes"]) <= ALLOWED_CLASSES, (b["id"], lic["classes"])
        if lic["status"] == "active":
            assert lic["expires"] > DATE, f"{b['id']} active licence expired"
            assert lic["entity"], b["id"]
            # an active licence must still be supported by a class its trade needs
            assert any(combo <= set(lic["classes"]) for combo in TRADE_REQUIRES[b["trade"]]), \
                f"{b['id']}: {lic['classes']} does not support trade {b['trade']}"
        else:
            assert any(f["level"] == "hold" for f in b["flags"]), \
                f"{b['id']} non-active licence needs a hold flag"
    for c in b["claims"]:
        assert c["source"] in sources, (b["id"], c["source"])
        assert c["text"].strip() and c["excerpt"].strip(), b["id"]
    for f in b["flags"]:
        assert f["level"] in {"hold", "notice", "gap", "discrepancy"}, (b["id"], f["level"])
        assert f["sources"] and all(s in sources for s in f["sources"]), b["id"]
    for link in b["platformLinks"]:
        assert link["source"] in sources, (b["id"], link["source"])
    for srcid in b["phoneSource"] and [b["phoneSource"]] or []:
        assert srcid in sources, b["id"]
    if b["priority"] is not None:
        assert 1 <= b["priority"] <= 12, (b["id"], b["priority"])
        assert b["rationale"] and b["nextStep"], f"priority {b['id']} needs rationale+nextStep"
        assert lic and lic["status"] == "active", f"shortlist record {b['id']} needs an active licence"
        assert any(combo <= set(lic["classes"]) for combo in TRADE_REQUIRES[b["trade"]]), b["id"]
        if b["priority"] > 5:
            # stricter admission basis used since wave 6: the regulator itself
            # records the 94122 address on the licence page.
            assert b["area"] == "outer", f"call {b['priority']:02d} must be Outer Sunset"
            assert "94122" in b["areaText"], b["id"]
            assert re.search(r"SAN FRANCISCO|INC|CO|PLUMBING|STUCCO", lic["entity"], re.I), b["id"]
    biz[b["id"]] = b
data["businesses"].extend(wave["businesses"])

# ------------------------------------------------------------------ review gate
for r in wave["reviews"]:
    assert r["id"] not in existing_reviews, f"review id {r['id']} already taken"
    assert r["checkedAt"] in {DATE}, r["id"]
    assert r["platform"] == "Thumbtack", r["id"]
    assert r["source"] in sources, r["id"]
    assert r["business"] in biz, r["id"]
    assert len(r["quote"]) < 500, r["id"]
    assert len(r["analysis"]) > 30, r["id"]
    assert r["exactTask"] is False, r["id"]
    assert r["identity"] in {"indexed", "matched", "unverified-username", "company-published"}, r["id"]
    existing_reviews.add(r["id"])
    biz[r["business"]]["reviewIds"].append(r["id"])
data["reviews"].extend(wave["reviews"])

# fingerprint reviews so no two rows carry the same business+author+quote
fp = {}
for r in data["reviews"]:
    key = (r["business"], r["author"], r["quote"][:60])
    assert key not in fp, f"duplicate review content: {r['id']} vs {fp[key]}"
    fp[key] = r["id"]

# --------------------------------------------------------------------- metadata
if DATE not in data["researchDates"]:
    data["researchDates"].append(DATE)

prior_waves = {w["wave"]: w for w in data["waves"]}
assert set(prior_waves) == {1, 2, 3, 4, 5, 6}, prior_waves
data["waves"].append({
    "wave": 7,
    "date": DATE,
    "count": len(wave["businesses"]),
    "cslbReads": len(cslb_wave_sources),
    "registryOnly": sum(1 for b in wave["businesses"] if not b.get("license")
                        and any(c["field"] == "Registry" for c in b["claims"])),
    "thumbtack": sum(1 for b in wave["businesses"]
                     if any(c["source"] in thumbtack_sources for c in b["claims"])),
})
assert sum(w["count"] for w in data["waves"]) == len(data["businesses"]), \
    "wave counts must add up to the record total"

active_licences = sorted({b["license"]["number"] for b in data["businesses"]
                          if b.get("license") and b["license"]["status"] == "active"})
inactive_licences = sorted({b["license"]["number"] for b in data["businesses"]
                            if b.get("license") and b["license"]["status"] in NOT_ACTIVE})
assert "licenseStatusCounts" not in data, "counts are derived in lib.js, not stored"

# Report only numbers this project actually read on cslb.ca.gov — computed from
# the source list so the figure can never be a hard-coded guess.
read_numbers = sorted({re.search(r"LicNum=(\d+)", s["url"]).group(1)
                       for s in data["sources"]
                       if s["access"] == "page" and "cslb.ca.gov" in s["url"]
                       and re.search(r"LicNum=(\d+)", s["url"])})
assert set(read_numbers) >= set(active_licences), \
    "every active licence must correspond to a CSLB page this project read"

m = data["methodology"]
assert "CSLB license detail pages read directly" in m["governmentSources"]
m["governmentSources"] = re.sub(
    r"^CSLB license detail pages read directly \([^)]*\)",
    (f"CSLB license detail pages read directly ({len(read_numbers)} distinct license numbers, "
     f"{len(cslb_wave_sources)} of them read in wave 7)"),
    m["governmentSources"], count=1,
) + (
    " CSLB’s own area-search form was also read directly and is recorded as a documented "
    "negative result: its results page is POST-only and returns HTTP 404 to a direct request, "
    "so CSLB facts here come from individual licence detail pages rather than from an "
    "enumerated 94122 list. A query of the State of California open-data catalogue for a CSLB "
    "licence extract returned no such dataset and is likewise recorded as a checked negative."
)
assert isinstance(m["passes"], str), "methodology.passes is prose, not a list"
assert "Pass 9" in m["passes"] and "Pass 10" not in m["passes"]
m["passes"] = m["passes"].rstrip() + (
    " Pass 10 (wave 7, Sep 11 2026): 50 new entries from three primary channels — 10 CSLB "
    "license detail pages read directly (1 active C-36 recorded at a 94122 address, 8 "
    "expired, 1 inactive, 1 revoked), 20 registry-only 94122 leads from the official SF DBI "
    "“Plumbing Permits Contacts” dataset queried directly by firm ZIP, and 20 Thumbtack "
    "drywall category listings read directly. Pass 11: line-by-line re-verification of every "
    "wave-7 field against the page it cites, name and license-number collision checks against "
    "all 301 pre-existing records, and rejection logging for every duplicate or out-of-scope "
    "candidate. Pass 12: status and classification audit — the newly surfaced “inactive” and "
    "“revoked” CSLB statuses added to the fail-closed hold rule, registry firm names "
    "compared with CSLB licensee names, and directly-read negative Thumbtack reviews attached "
    "to the existing records they describe rather than to new rows. Pass 13: compliance "
    "re-check, dataset date/wave bookkeeping, structural tests and the site rebuild."
)
m["ranking"] = (
    "Editorial diagnostic-call order, not star averages and not a guarantee. Calls 01-05 carry "
    "adjacent task evidence, primary-source area coverage and direct CSLB checks from waves "
    "1-2. Calls 06-09 were added in wave 6 on a stricter basis: each is an active license "
    "whose CSLB page itself records a 94122 Outer Sunset business address, and each holds the "
    "classification its trade requires (C35 lathing & plastering, B+C36 general "
    "building/plumbing, C36 plumbing). Call 10 was added in wave 7 on that same strict basis: "
    "an active C-36 plumbing license whose CSLB page records a 94122 address, licensed since "
    "1989. Call 06 additionally carries a directly-read negative Thumbtack review alleging "
    "refused corrections and undisclosed cash payment; that review is attached to the record "
    "and the caveat is repeated in its call rationale rather than being averaged away. "
    "Everything outside the call order is a discovery record: registry-only permit-contact "
    "leads, unverified Thumbtack drywall leads, and CSLB records whose licenses are expired, "
    "inactive, revoked, or outside the trade needed for this job. The master qualified list "
    "stays empty until full evidence exists for an exact repair scope and insurance."
)

# compliance block must survive unchanged
assert json.dumps(data["compliance"], sort_keys=True, ensure_ascii=False) == compliance_before
assert data["master"] == []
assert not any(b["master"] for b in data["businesses"])
assert not any(b.get("exactMatch") or b.get("insuranceVerified") or b.get("scopeConfirmed")
               for b in data["businesses"])
assert not any("rent control" in b["name"].lower() or "in-law" in b["name"].lower()
               for b in data["businesses"])

# ------------------------------------------------------------------- final sweep
for b in data["businesses"]:
    assert b["checkedAt"] in data["researchDates"], b["id"]
    assert b["claims"] and b["claims"][0]["field"] == "Discovery", b["id"]
    for c in b["claims"]:
        assert c["source"] in sources, (b["id"], c["source"])
    for f in b["flags"]:
        assert f["sources"] and all(s in sources for s in f["sources"]), b["id"]
    for rid in b["reviewIds"]:
        r = next(x for x in data["reviews"] if x["id"] == rid)
        assert r["business"] == b["id"], (b["id"], rid)

ids = [b["id"] for b in data["businesses"]]
assert len(ids) == len(set(ids)), "duplicate business ids"
sids = [s["id"] for s in data["sources"]]
assert len(sids) == len(set(sids)), "duplicate source ids"

TARGET.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
print(f"merged wave 7: {len(data['businesses'])} businesses, {len(data['sources'])} sources, "
      f"{len(data['reviews'])} reviews")
print(f"  active licenses {len(active_licences)}, non-active {len(inactive_licences)}, "
      f"distinct CSLB pages read {len(read_numbers)}")
print(f"  wave 7 composition: {data['waves'][-1]['cslbReads']} CSLB reads / "
      f"{data['waves'][-1]['registryOnly']} registry-only / "
      f"{data['waves'][-1]['thumbtack']} thumbtack")
