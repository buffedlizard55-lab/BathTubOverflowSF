#!/usr/bin/env python3
"""Wave-6 follow-up patch: attach THIS SESSION's verification work to three
pre-existing entries instead of double-counting them as new records.

Run AFTER `python3 scripts/merge_wave6.py`.

What changes and why (all read directly or from cited indexed extracts,
2026-09-11):

- bernal-hill  — CSLB 995163 read directly: BERNAL HILL DRYWALL INC, 720
                 Anderson St, San Francisco 94110. Current and active, C-9
                 (Drywall) + B (General Building), expires 07/31/2028. This
                 closes the wave-1 gap flag "CSLB status/class for 995163 not
                 checked". The number printed on the company's own site footer
                 matches the regulator record exactly. Two indexed Yelp
                 ceiling-review excerpts and the official site are attached.
- meticulous   — Indexed Yelp ceiling-repair results carry a truncated
                 customer excerpt about repairing "a huge hole in my plaster
                 ceiling (old…". Task-adjacent finish evidence for a 1940s
                 building; the truncation is preserved, not completed.
- bay-area     — Indexed Yelp Sunset District plumbing results carry the
                 business portfolio caption "Install new bathtub with a valve
                 inside the wall". Attached as a clearly-labelled portfolio
                 caption, NOT as a customer review.

Rejected in this pass and therefore NOT attached anywhere:
- An indexed Yelp excerpt on the San Francisco "drywall repair service" page
  praises "Singh" while appearing on the Jose HandyMan Services listing. The
  reviewer name does not match the business name, which is the same index-text
  -bleed pattern flagged in wave 4 (SAFENEST / Mike's Water Damage). Attaching
  it would misattribute a review, so it is recorded in the discovery log only.

Fail-closed rules mirror merge_wave6.py: the license source must be government
kind on cslb.ca.gov and must carry the classification the declared trade needs;
a non-active license would require a hold flag; nothing is promoted to master;
review invariants (back-reference, length, exactTask=False) still hold.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "research.json"
DATE = "2026-09-11"
PREV = "2026-09-10"

TRADE_REQUIRES = {
    "plumbing": [{"C36"}],
    "drywall": [{"C-9"}, {"B"}],
    "finish": [{"C-9"}, {"C35"}, {"B"}],
}

data = json.loads(TARGET.read_text())
assert DATE in data["researchDates"], "run merge_wave6.py first"
sources = {s["id"]: s for s in data["sources"]}
biz = {b["id"]: b for b in data["businesses"]}
review_ids = {r["id"] for r in data["reviews"]}


def need_source(sid):
    assert sid in sources, f"source {sid} missing — run merge_wave6.py first"
    return sources[sid]


def gov_cslb(sid, number):
    s = need_source(sid)
    assert s["kind"] == "government" and "cslb.ca.gov" in s["url"], sid
    assert str(number) in s["url"], (sid, number)
    return sid


def attach_license(bid, lic, trade):
    b = biz[bid]
    assert b.get("license") is None, f"{bid} already has a license — refusing to overwrite"
    gov_cslb(lic["source"], lic["number"])
    assert lic["status"] == "active" and lic["expires"] > DATE
    assert lic["entity"] and lic["classes"]
    assert set(lic["classes"]) <= {"C36", "C-9", "C35", "C-4", "C10", "C16", "C20", "B", "A"}
    assert any(combo <= set(lic["classes"]) for combo in TRADE_REQUIRES[trade]), \
        f"{bid}: {lic['classes']} does not support trade {trade}"
    lic["checkedAt"] = DATE
    b["license"] = lic
    b["trade"] = trade
    b["checkedAt"] = DATE
    return b


def add_claim(bid, field, text, source, excerpt):
    need_source(source)
    assert text.strip() and excerpt.strip()
    biz[bid]["claims"].append({"field": field, "text": text, "source": source,
                               "excerpt": excerpt})


def replace_flag(bid, old_substring, new_flag):
    b = biz[bid]
    hits = [i for i, f in enumerate(b["flags"]) if old_substring in f["text"]]
    assert len(hits) == 1, (bid, old_substring, hits)
    for sid in new_flag["sources"]:
        need_source(sid)
    b["flags"][hits[0]] = new_flag


def add_review(r):
    assert r["id"] not in review_ids, r["id"]
    need_source(r["source"])
    b = biz[r["business"]]
    assert len(r["quote"]) < 500 and len(r["analysis"]) > 30, r["id"]
    assert r["exactTask"] is False
    assert r["checkedAt"] == DATE
    r.setdefault("identity", "indexed")
    r.setdefault("negative", False)
    r.setdefault("published", None)
    data["reviews"].append(r)
    review_ids.add(r["id"])
    b["reviewIds"].append(r["id"])
    b["checkedAt"] = DATE
    return r


# =========================================================================
# Bernal Hill Drywall — CSLB 995163 read directly; official site attached.
# =========================================================================
SITE_BH = ("BERNAL HILL DRYWALL INC \u00b7 720 ANDERSON ST \u00b7 SAN FRANCISCO, CA 94110 \u00b7 Business "
           "Phone Number:(415) 533-8274 \u2014 Entity Corporation \u2014 Issue Date 07/28/2014 \u2014 "
           "Expire Date 07/31/2028 \u2014 \u201cThis license is current and active.\u201d \u2014 C-9 - DRYWALL; "
           "B - GENERAL BUILDING \u2014 Contractor's Bond $25,000 eff 03/29/2023 \u2014 qualifying "
           "individual JERRY FRED CALDERON \u2014 workers compensation with ENDURANCE ASSURANCE "
           "CORPORATION eff 03/10/2026 exp 03/10/2027; classification code 5447 Wallboard "
           "Installation-high wage")

attach_license("bernal-hill", {
    "number": "995163", "status": "active", "entity": "BERNAL HILL DRYWALL INC",
    "expires": "2028-07-31", "classes": ["C-9", "B"], "source": 196,
}, "drywall")

b = biz["bernal-hill"]
b["website"] = "https://www.bernalhilldrywall.com/"
b["websiteSource"] = 188
b["phone"] = "415-533-8274"
b["phoneSource"] = 196
b["area"] = "sf"
b["areaText"] = ("CSLB records the business address as 720 Anderson St, San Francisco, CA 94110 "
                 "(Bernal Heights), and Yelp's indexed results state \u201cServing San Francisco and "
                 "the Surrounding Area\u201d. No Outer Sunset dispatch statement was found.")
b["gaps"] = [
    "No exact seized bathtub-overflow extraction outcome was verified.",
    "Outer Sunset dispatch is not stated by the business or the regulator; the CSLB base is "
    "Bernal Heights (94110).",
    "Drywall scope covers the patch/hatch phase only; a licensed C-36 plumber must own any pipe "
    "work.",
]
add_claim("bernal-hill", "License",
          "CSLB license 995163 read directly on 2026-09-11: current and active corporation "
          "BERNAL HILL DRYWALL INC holding C-9 (Drywall) and B (General Building), expiring "
          "07/31/2028, with a $25,000 contractor's bond effective 03/29/2023 and workers "
          "compensation effective 03/10/2026 classified 5447 Wallboard Installation-high wage.",
          196, SITE_BH)
add_claim("bernal-hill", "Drywall scope",
          "The company's own site describes drywall installation and finishing, patching, level "
          "4 and level 5 smooth finishes, custom textures matched to existing surfaces, and "
          "complete build-back after water, fire or mold remediation \u2014 the finish half of a "
          "ceiling opening. Site located through search extract; not retrieved directly.",
          188, "From small wall repairs to complete build-backs after water, mold or fire "
               "remediation, we deliver smooth, seamless results. Whether you need a level 5 "
               "smooth wall finish or custom textures to match your existing surfaces")
add_claim("bernal-hill", "Identity",
          "The license number published in the company's own site footer matches the CSLB record "
          "read directly, including the expiration date BBB reports for the same number. Site, "
          "regulator and directory agree on identity.",
          188, "cALL nOW FOR AN ESTIMATE 415-533-8274 \u00b7 Picture \u00b7 CALIFORNIA License #995163")
replace_flag("bernal-hill", "CSLB status/class for 995163 not checked", {
    "level": "notice",
    "text": "Wave-1 gap closed on 2026-09-11: CSLB 995163 was read directly and confirms an "
            "active C-9 (Drywall) + B (General Building) corporation. The drywall trade class "
            "expected in wave 1 is confirmed, and the record holds no C36 \u2014 so this business "
            "cannot lawfully self-perform the plumbing portion of the job.",
    "sources": [196, 48]})
add_review(dict(
    id="R66", business="bernal-hill", platform="Yelp",
    author="Not reliably resolved in extract", published=None,
    quote="I had some major patches on my ceiling that needed to be taken care of as well as "
          "floating out a few walls that previousl\u2026",
    analysis="Ceiling patching plus floating out walls is the closest finish-side task evidence "
             "attached to this entry. The excerpt is truncated in the indexed source and the "
             "truncation is preserved rather than completed; no rating, date or reviewer name "
             "was published in the extract, and Yelp's own page was not directly retrievable.",
    theme="Ceiling repair", source=179, access="blocked-with-search-extract", checkedAt=DATE,
    exactTask=False))
add_review(dict(
    id="R67", business="bernal-hill", platform="Yelp",
    author="Not reliably resolved in extract", published=None,
    quote="Jerry and his team did an excellent job with a drywall project we had. They hung "
          "drywall in the ceiling of a family room,\u2026",
    analysis="Confirms the business hangs ceiling drywall as a crew, and the reviewer names "
             "Jerry, which matches the CSLB qualifying individual JERRY FRED CALDERON \u2014 a weak "
             "but real identity corroboration. The excerpt is truncated in the indexed source; "
             "no rating or date was published in the extract.",
    theme="Ceiling repair", source=177, access="blocked-with-search-extract", checkedAt=DATE,
    exactTask=False))

# =========================================================================
# The Meticulous Handyman — plaster ceiling hole in an old building.
# =========================================================================
add_claim("meticulous", "Task-adjacent evidence",
          "Indexed Yelp ceiling-repair results carry a truncated customer excerpt describing "
          "repair of a large hole in an old plaster ceiling. Plaster (not drywall) ceilings are "
          "the expected construction in a 1940 building, so this is the most "
          "period-appropriate finish excerpt attached to a pre-existing entry this pass.",
          179, "I will definitely use their services again. I had them repair a huge hole in my "
               "plaster ceiling (old\u2026")
add_review(dict(
    id="R68", business="meticulous", platform="Yelp",
    author="Not reliably resolved in extract", published=None,
    quote="I will definitely use their services again. I had them repair a huge hole in my "
          "plaster ceiling (old\u2026",
    analysis="A large hole in an old plaster ceiling was repaired, and the customer says they "
             "would use the business again. The excerpt is truncated mid-parenthesis in the "
             "indexed source and is preserved that way; the word \u201chuge\u201d is the reviewer's. No "
             "cause, access method, framing or inspection detail is published, and a handyman "
             "scope is not a licensed plastering or drywall classification.",
    theme="Older-home experience", source=179, access="blocked-with-search-extract",
    checkedAt=DATE, exactTask=False))
biz["meticulous"]["trade"] = "finish"
biz["meticulous"]["gaps"].append(
    "Handyman finish work is not a licensed C-9 or C35 classification; confirm which entity and "
    "classification would contract for a ceiling patch.")

# =========================================================================
# Bay Area Plumbing — portfolio caption, explicitly NOT a customer review.
# =========================================================================
bay = biz["bay-area"]
bay["trade"] = "plumbing"
bay["checkedAt"] = DATE
add_claim("bay-area", "Task-adjacent evidence",
          "Indexed Yelp Sunset District plumbing results carry a BUSINESS PORTFOLIO CAPTION (not "
          "a customer review) reading \u201cInstall new bathtub with a valve inside the wall\u201d, "
          "listed under \u201cRemodeling a bathroom\u201d. In-wall tub valve work is adjacent to an "
          "overflow mechanism behind a wall. A caption published by the business is marketing "
          "evidence only and proves nothing about a seized linkage.",
          195, "Bay Area Plumbing 4.8 (173 reviews) Serving San Francisco and the Surrounding "
               "Area Emergency services Certified professionals \u2026 Install two new water heaters "
               "Remodeling a bathroom. Install new bathtub with a valve inside the wall See "
               "Portfolio 20 mins response time 66 locals recently requested a quote")
bay["gaps"].append(
    "The only in-wall tub evidence attached to this entry is a business-published portfolio "
    "caption from an indexed page, not a customer account, and it was not read on Yelp directly.")

# =========================================================================
# Final invariants (mirror merge_wave6.py).
# =========================================================================
assert data["master"] == []
assert not any(b_["master"] for b_ in data["businesses"])
assert not any(b_.get("exactMatch") or b_.get("insuranceVerified")
               or b_.get("scopeConfirmed") for b_ in data["businesses"])
ids = [r["id"] for r in data["reviews"]]
assert len(ids) == len(set(ids))
for r in data["reviews"]:
    assert sources.get(r["source"]), r["id"]
    assert len(r["quote"]) < 500 and len(r["analysis"]) > 30, r["id"]
    assert r["exactTask"] is False, r["id"]
    assert r["checkedAt"] in data["researchDates"], r["id"]
for b_ in data["businesses"]:
    assert b_["checkedAt"] in data["researchDates"], b_["id"]
    assert b_["claims"] and b_["claims"][0]["field"] == "Discovery", b_["id"]
    assert len(b_["gaps"]) >= 2, b_["id"]
    for c in b_["claims"]:
        assert c["source"] in sources, (b_["id"], c["source"])
    for f in b_["flags"]:
        assert f["sources"] and all(s in sources for s in f["sources"]), b_["id"]
    lic = b_.get("license")
    if lic:
        assert sources[lic["source"]]["kind"] == "government", b_["id"]
        assert "cslb.ca.gov" in sources[lic["source"]]["url"], b_["id"]
        assert lic["checkedAt"] == b_["checkedAt"], b_["id"]
        if lic["status"] == "active":
            assert lic["expires"] > lic["checkedAt"], b_["id"]
        else:
            # established convention in waves 1-5: a non-active license puts the
            # business-level status on "hold". Wave 6 additionally carries an
            # explicit hold flag. Either satisfies the fail-closed rule.
            assert b_["status"] in ("hold", "excluded") or any(
                f["level"] == "hold" for f in b_["flags"]), b_["id"]
    for rid in b_["reviewIds"]:
        r = next(x for x in data["reviews"] if x["id"] == rid)
        assert r["business"] == b_["id"], (b_["id"], rid)

TARGET.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
active = sum(1 for b_ in data["businesses"]
             if b_.get("license") and b_["license"]["status"] == "active")
print(f"patched research.json: {len(data['businesses'])} businesses, {len(data['sources'])} "
      f"sources, {len(data['reviews'])} reviews, {active} active license records")
