#!/usr/bin/env python3
"""Wave-7 follow-up patch: attach THIS SESSION's verification work to
pre-existing entries instead of double-counting them as new records, and
correct one wave-6 review attribution that a direct page read disproved.

Run AFTER `python3 scripts/merge_wave7.py`.

What changes, and the evidence for each change (all read directly 2026-09-11):

bill-callaway (wave 1)
    CSLB 660638 read directly: BILL CALLAWAY PLUMBER, 3141 Balboa St, San
    Francisco 94121, Sole Ownership, issued 12/08/1992, EXPIRED 12/31/2014,
    class C36 only. Contractor's bond $12,500 (Old Republic Surety, eff
    01/13/2008) CANCELLED 03/09/2012; workers' compensation exemption eff
    11/23/1992. The registry re-query returns 170 permit rows at 3141 Balboa
    (94121) and 7 rows at 1850 42nd Avenue (94122), the two 94122 rows using
    the exact CSLB entity name "Bill Callaway Plumber". The wave-1 record had
    no licence read at all; it now carries one, is placed on hold because the
    licence expired eleven years ago, and its area is narrowed to the 94122
    address the City's own registry records.

joe-watterson (wave 2)
    CSLB 723992 re-read: still CURRENT AND ACTIVE, C36, expires 06/30/2028,
    JOE WATTERSON PLUMBING, 3653 Folsom Street 94110, bond $25,000
    (Philadelphia Indemnity, eff 04/26/2025, no cancellation), workers'
    compensation exemption with no employees eff 05/19/2026. The registry
    re-query resolves the wave-2 name-history flag: licence 723992 appears
    under two firm names and four ZIPs — "Joe Watterson Plumbing" at 384
    Somerset St 94134 (194 rows), 3653 Folsom St 94110 (53 rows), 2186 46th Av
    94116 (5 rows) and Po Box 415 94996 (5 rows), and "Slemish Plumbing" at
    2186 46th Av 94116 (164+46+36+22+1 = 269 rows). NO 94122 row exists for
    this licence, so Outer Sunset coverage stays unconfirmed and the record is
    not moved to area "outer".

w6-caledonia-plastering-stucco-inc (wave 6, was call 06)
    Thumbtack's own profile page read directly. It shows "Plastering • 94116",
    Excellent 4.9 (56 reviews), Hired 65 times, Top Pro 2018/2019/2020 only, a
    background check on John Cullen, NO licence in its Credentials section, and
    a services list of plastering and stucco only — no drywall service. For the
    queried service and ZIP the page displayed "Sorry this pro can't do your
    job, but we know other pros who can." The default review list shows five
    reviews dated 2016-2018 and nothing later. Thumbtack's San Francisco
    drywall-contractors category page, read directly, publishes a long negative
    review by "Jay D." against this same profile slug alleging refused
    corrections, a covered-over bathroom exhaust, and cash payment.
    Consequence: the record is REMOVED from the diagnostic call order, placed
    on hold, and calls 06-09 are renumbered. The active C35 licence at a 94122
    CSLB address is unchanged and still recorded.

    CORRECTION: wave 6 stored review R60 as author "Tom S.", published
    "Jun 2, 2018", carrying the quote "Quick to respond, fair price … John took
    care of the hole in the ceiling …". The direct profile read shows that quote
    belongs to Vipada W., Oct 5, 2017, and that Tom S.'s Jun 2, 2018 review is a
    different text about exterior stucco on a backyard structure. R60's author,
    date, source, access and identity are corrected in place; Tom S.'s actual
    review is added as R98 so nothing is silently dropped; the mis-pairing is
    flagged on the record.

w5-new-age-drywall-inc (wave 5)
    Profile page read directly: Excellent 4.9 (237 reviews), Hired 455 times,
    current Top Pro 2021-2025, background checked, "License verified", 6
    employees, 6 years in business, "Serves Redwood City, CA". Credentials
    state "License type: C9 – Drywall / License state: CA / License verified on
    10/29/2020" and a background check on Jaime Lombera, but NO CSLB licence
    number is published anywhere in the retrieved text, so no CSLB page could be
    read and the licence field stays empty. Four reviews attached, three of them
    about ceilings and one specifically about a bathroom ceiling hole patched
    and textured to match. Area narrowed from "sf" to "outside" because the
    direct read states a Redwood City home market.

w5-figs-drywall-repair-paint, w5-maga-a-time-handyman, w5-walty-handy-service-pro
    (wave 5) Each gains the directly-read Thumbtack review and profile URL.
    Figs' profile path is /id/boise/handyman/ (Idaho) although its review is
    published on Thumbtack's San Francisco drywall-repair page, and the listing
    name is "Figs Drywall Repair" without the "& Paint" the wave-5 record
    stored; Walty's profile path is /ca/san-pablo/moving-companies/ (Contra
    Costa County, moving category) although its retained review is drywall
    patching. Both are flagged and moved to area "outside".

Rejected in this pass and therefore NOT attached anywhere:
    SAFENEST Restoration (Zachary S.) appears in the same directly-read review
    section with a drywall-patching review, but the record was excluded in wave
    4 on an index-text-bleed identity problem; a category-page review is not
    enough to reopen it.

Fail-closed rules mirror merge_wave7.py: a licence may only come from a
government cslb.ca.gov page; a non-active licence must carry a hold flag; a
platform "license verified" badge never populates the licence field; nothing is
promoted to master; review invariants (back-reference, <500 characters,
exactTask false) still hold.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "research.json"
DATE = "2026-09-11"
PREV = "2026-09-10"

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
NOT_ACTIVE = {"expired", "suspended", "canceled", "inactive", "revoked"}
FORBIDDEN = ("rent control", "in-law unit", "without a permit", "no permit",
             "unpermitted", "discreet", "do not disclose")

data = json.loads(TARGET.read_text())
assert any(b["id"].startswith("w7-") for b in data["businesses"]), "run merge_wave7.py first"
assert DATE in data["researchDates"]
assert not any(s["id"] >= 218 for s in data["sources"]), "patch already applied — refusing to duplicate"
assert not ({"R89", "R90", "R91", "R92", "R93", "R94", "R95", "R96", "R97", "R98"}
            & {r["id"] for r in data["reviews"]}), "patch already applied"
compliance_before = json.dumps(data["compliance"], sort_keys=True, ensure_ascii=False)

sources = {s["id"]: s for s in data["sources"]}
biz = {b["id"]: b for b in data["businesses"]}
reviews = {r["id"]: r for r in data["reviews"]}


def need_source(sid):
    assert sid in sources, f"source {sid} missing"
    return sources[sid]


# =========================================================================
# New sources read directly in this pass.
# =========================================================================
NEW_SOURCES = [
    {"id": 218,
     "title": "Thumbtack · New Age Drywall Inc · pro page (page read directly)",
     "url": "https://www.thumbtack.com/ca/redwood-city/drywall-repair/new-age-drywall-inc/service/404118804346175490",
     "kind": "platform", "access": "page", "checkedAt": DATE,
     "note": "Pro profile retrieved and read directly (HTTP 200). Page shows: header “Drywall "
             "Repair and Texturing • 94063”; “Excellent 4.9 (237)”; “Top Pro”; “Responds in about "
             "2 hours”; Overview “Current Top Pro / Hired 455 times / Serves Redwood City, CA / "
             "Background checked / License verified / 6 employees / 6 years in business”; Top Pro "
             "badges 2021, 2022, 2023, 2024, 2025; payment via Apple Pay, Cash, Check and Venmo; "
             "services offered include “Patch damaged drywall”, “Replace one or more sheets of "
             "drywall”, “Fill in cracks”, “Remove popcorn texture”; “Read reviews that mention: "
             "work・141, drywall・96, wall・38, repair・36, ceiling・29, paint・29, patching・23, "
             "texture・17, hole・13, dry・10”; Credentials “License type: C9 – Drywall / License "
             "state: CA / License verified on 10/29/2020” and “Background Check: Jaime Lombera”. "
             "NO CSLB licence number is published anywhere in the retrieved text, so no CSLB page "
             "could be read from it and the licence field is left empty. “License verified” and "
             "“Background checked” are Thumbtack-side badges, not CSLB verification, and the "
             "credential date shown is 10/29/2020. Review dates and “Hired on Thumbtack” markers "
             "are as displayed. Star distribution as displayed: 5★ 96%, 4★ 2%, 3★ 0%, 2★ 1%, "
             "1★ 1%. Where the platform's own markup joined two words in the rendered text (for "
             "example “drywallrepair”), the space has been restored and no word was added, "
             "removed or re-ordered."},
    {"id": 219,
     "title": "Thumbtack · Caledonia Plastering & Stucco · pro page (page read directly)",
     "url": "https://www.thumbtack.com/ca/san-francisco/drywall-repair/caledonia-plastering-stucco/service/281335206093636654",
     "kind": "platform", "access": "page", "checkedAt": DATE,
     "note": "Pro profile retrieved and read directly (HTTP 200). Page shows: header “Plastering • "
             "94116”; “Excellent 4.9 (56)”; select-a-service options “Stucco Application / "
             "Plastering / Stucco Repair”; the message “Sorry this pro can’t do your job, but we "
             "know other pros who can.” with a link to instant results for zipCode=94116 (this "
             "message is specific to the service and ZIP queried, not a general statement about "
             "every job); Overview “Hired 65 times / Background checked”; Top Pro badges 2018, "
             "2019 and 2020 only; “Ask this pro about their preferred payment method”; services "
             "offered “Restoration of existing plaster, Repair or touchup of existing plaster, "
             "Plastering for new construction, Skim-coating, +1 more” with NO drywall service "
             "listed; star distribution 5★ 93%, 4★ 5%, 3★ 0%, 2★ 0%, 1★ 2% of 56 reviews; "
             "“Read reviews that mention: stucco・11, plaster・9, walls・6, ceiling・5, repair・5, "
             "hole・4”; Credentials section contains only “Background Check: John Cullen” and NO "
             "licence entry. The default “Most relevant” review list displays five reviews dated "
             "Dec 12 2016, Oct 5 2017, Jan 16 2018, May 20 2018 and Jun 2 2018, and no review "
             "dated later than Jun 2, 2018. The negative review by “Jay D.” is NOT in that "
             "default list; it was read on Thumbtack's San Francisco drywall-contractors category "
             "page (source 215) under this same profile slug, where no review date is displayed."},
    {"id": 220,
     "title": "SF DBI · registry re-query of licence 723992 by firm name, address and ZIP",
     "url": "https://data.sf.gov/resource/k6kv-9kix.json?$select=firm_name,address,zipcode,"
            "count(permit_number)%20as%20permits&$where=license_number=%27723992%27"
            "&$group=firm_name,address,zipcode&$order=permits%20DESC",
     "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Official City & County of San Francisco open-data API (dataset k6kv-9kix, “Plumbing "
             "Permits Contacts”, provenance: official), queried directly and grouped so that every "
             "firm name, address and ZIP this licence appears under is visible on its own line. "
             "Returned 9 rows: Joe Watterson Plumbing / 384 Somerset St / 94134-0000 / 194; "
             "Slemish Plumbing / 2186  46th / 94116 / 164; Joe Watterson Plumbing / 3653 Folsom St "
             "/ 94110-0000 / 53; Slemish Plumbing / 2186  46th Av / 94116 / 46; Slemish Plumbing / "
             "2186 46th Ave / 94116 / 36; Slemish Plumbing / 2186 46th Av / 94116 / 22; Joe "
             "Watterson Plumbing / 2186  46th Av / 94116 / 5; Joe Watterson Plumbing / Po Box 415 "
             "St / 94996-0000 / 5; Slemish Plumbing / 2186  46th Ave / 94116 / 1. No row carries "
             "ZIP 94122. Registry rows are historical permit contacts with no in-dataset dates."},
    {"id": 221,
     "title": "SF DBI · registry re-query of licence 660638 by firm name, address and ZIP",
     "url": "https://data.sf.gov/resource/k6kv-9kix.json?$select=firm_name,address,zipcode,"
            "count(permit_number)%20as%20permits&$where=license_number=%27660638%27"
            "&$group=firm_name,address,zipcode&$order=permits%20DESC",
     "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Official City & County of San Francisco open-data API (dataset k6kv-9kix), queried "
             "directly and grouped by firm name, address and ZIP. Returned 5 rows: Bill Callaway "
             "Plumbing / 3141 Balboa St / 94121 / 111; Bill Callaway Plumbing / 3141 Balboa / "
             "94121 / 56; Bill Callaway Plumber / 1850 42nd Avenue / 94122 / 4; Bill Callaway "
             "Plumber / 3141 Balboa St / 94121 / 3; Bill Callaway Plumbing / 1850 42nd Ave / "
             "94122 / 3. Totals 170 rows at 94121 and 7 rows at 94122; the two 94122 rows use the "
             "exact CSLB entity name “Bill Callaway Plumber”. Registry rows are historical permit "
             "contacts with no in-dataset dates and never establish present operation."},
]
for s in NEW_SOURCES:
    assert s["id"] not in sources, s["id"]
    assert s["access"] == "page" and s["checkedAt"] == DATE, s["id"]
    assert re.match(r"^https://", s["url"]) and " " not in s["url"], s["id"]
    sources[s["id"]] = s
data["sources"].extend(NEW_SOURCES)


# =========================================================================
# Helpers.
# =========================================================================
def add_claim(bid, field, text, source, excerpt):
    need_source(source)
    assert text.strip() and excerpt.strip(), (bid, field)
    assert not any(c["field"] == field and c["source"] == source and c["text"] == text
                   for c in biz[bid]["claims"]), f"duplicate claim {bid}/{field}"
    biz[bid]["claims"].append({"field": field, "text": text, "source": source, "excerpt": excerpt})


def add_flag(bid, level, text, srcs):
    assert level in {"hold", "notice", "gap", "discrepancy"}, level
    for s in srcs:
        need_source(s)
    assert text.strip() and len(text) > 40, (bid, level)
    biz[bid]["flags"].append({"level": level, "text": text, "sources": list(srcs)})


def add_link(bid, label, url, source):
    need_source(source)
    assert not any(p["url"] == url for p in biz[bid]["platformLinks"]), (bid, url)
    biz[bid]["platformLinks"].append({"label": label, "url": url, "source": source})


def add_review(rid, bid, author, published, quote, analysis, theme, source,
               access="page", identity="matched", negative=False):
    assert rid not in reviews, rid
    assert bid in biz, bid
    need_source(source)
    assert len(quote) < 500, f"{rid} quote is {len(quote)} chars"
    assert len(analysis) > 30, rid
    assert quote.strip() and author.strip(), rid
    fp = (bid, author, quote[:60])
    for r in data["reviews"]:
        assert (r["business"], r["author"], r["quote"][:60]) != fp, f"{rid} duplicates {r['id']}"
    r = {"id": rid, "business": bid, "platform": "Thumbtack", "author": author,
         "published": published, "quote": quote, "analysis": analysis, "theme": theme,
         "source": source, "access": access, "identity": identity, "negative": negative,
         "exactTask": False, "checkedAt": DATE}
    reviews[rid] = r
    data["reviews"].append(r)
    biz[bid]["reviewIds"].append(rid)
    return r


# =========================================================================
# 1. bill-callaway — CSLB 660638 read directly, attached to the wave-1 record.
# =========================================================================
b = biz["bill-callaway"]
assert b.get("license") is None, "refusing to overwrite an existing licence read"
assert sources[211]["kind"] == "government" and "LicNum=660638" in sources[211]["url"]
b["license"] = {"number": "660638", "status": "expired", "entity": "BILL CALLAWAY PLUMBER",
                "expires": "2014-12-31", "classes": ["C36"], "source": 211, "checkedAt": DATE}
b["trade"] = "plumbing"
b["status"] = "hold"
b["checkedAt"] = DATE
b["area"] = "outer"
b["areaText"] = (
    "The City's own permit registry records this licence at 1850 42nd Avenue, San Francisco "
    "94122 — an Outer Sunset address — on 7 permit rows, two of them under the exact CSLB entity "
    "name “Bill Callaway Plumber”. The CSLB licence page itself records 3141 Balboa St, San "
    "Francisco 94121 (Outer Richmond), where 170 further permit rows sit, and the wave-1 discovery "
    "listing was a Yellow Pages Outer Sunset plumber directory. The licence expired on 12/31/2014, "
    "so this address history documents where the business was, not where it works now."
)
add_claim("bill-callaway", "License",
          "EXPIRED · C36 (Plumbing) only · sole ownership · issued 12/08/1992 · expired "
          "12/31/2014 · CSLB address 3141 Balboa St, San Francisco 94121 · phone (415) 751-6082. "
          "The page states the licence is expired and the holder is not able to contract.",
          211,
          "BILL CALLAWAY PLUMBER; 3141 BALBOA, SAN FRANCISCO, CA 94121; Sole Ownership; "
          "issue 12/08/1992; expire 12/31/2014; EXPIRED; class C36 - PLUMBING; "
          "“Data current as of 9/11/2026 5:03:20 PM”")
add_claim("bill-callaway", "Bonding",
          "The contractor's bond of record is cancelled: $12,500 with Old Republic Surety, "
          "effective 01/13/2008, cancelled 03/09/2012. No replacement bond is shown.",
          211,
          "bond: OLD REPUBLIC SURETY $12,500 eff 01/13/2008 CANCELLED 03/09/2012")
add_claim("bill-callaway", "Workers' compensation",
          "Workers' compensation exemption effective 11/23/1992. An exemption means no policy is "
          "on file with the Board; it is not evidence of coverage for anyone working on a job.",
          211, "WC exempt eff 11/23/1992")
add_claim("bill-callaway", "Registry",
          "Registry re-query grouped by firm name, address and ZIP returns 170 permit rows at "
          "3141 Balboa (94121) and 7 rows at 1850 42nd Avenue (94122). The two 94122 rows are "
          "filed under “Bill Callaway Plumber”, the exact CSLB entity name, and three under “Bill "
          "Callaway Plumbing”. Registry rows are historical permit contacts with no in-dataset "
          "dates.",
          221,
          "Bill Callaway Plumbing / 3141 Balboa St / 94121 / 111; Bill Callaway Plumbing / "
          "3141 Balboa / 94121 / 56; Bill Callaway Plumber / 1850 42nd Avenue / 94122 / 4; "
          "Bill Callaway Plumber / 3141 Balboa St / 94121 / 3; Bill Callaway Plumbing / "
          "1850 42nd Ave / 94122 / 3")
add_claim("bill-callaway", "Coverage", b["areaText"], 221,
          "Bill Callaway Plumber / 1850 42nd Avenue / 94122 / 4 permits")
add_flag("bill-callaway", "hold",
         "CSLB reads licence 660638 as EXPIRED on 12/31/2014, and the page states the holder is "
         "not able to contract. The contractor's bond of record was cancelled on 03/09/2012 and "
         "workers' compensation is exempt. This business cannot be engaged as a licensed C-36 "
         "plumbing contractor on the strength of this record, and a Yellow Pages directory listing "
         "does not revive an expired licence.",
         [211])
add_flag("bill-callaway", "discrepancy",
         "Three different addresses attach to this one business across three sources: the CSLB "
         "licence page records 3141 Balboa St 94121 (Outer Richmond); the City's permit registry "
         "records 1850 42nd Avenue 94122 (Outer Sunset) on 7 rows and 3141 Balboa on 170 rows; the "
         "wave-1 discovery listing placed the business in an Outer Sunset plumber directory. The "
         "94122 rows are recorded under the exact CSLB entity name, which is why the area label "
         "follows them, but the regulator's own address of record is 94121 and the licence is "
         "expired, so no current Outer Sunset dispatch is established.",
         [211, 221, 2])
b["gaps"] = [
    "Licence 660638 expired on 12/31/2014; whether the business still operates, and under what "
    "name or licence, is not established by any source in this dataset.",
    "No exact seized bathtub-overflow trip-lever extraction outcome was verified for this "
    "business, and no customer review of any kind is retained.",
    "The registry's 94122 rows carry no in-dataset dates, so they cannot show that any work at "
    "1850 42nd Avenue happened recently.",
    "On-site feasibility, a written repair-first scope and applicable insurance are unconfirmed.",
    "Re-check CSLB before any contact; if a current licence exists it will be under a different "
    "number or entity and must be read separately.",
]

# =========================================================================
# 2. joe-watterson — CSLB 723992 re-read plus the registry name history.
# =========================================================================
b = biz["joe-watterson"]
assert b["license"]["number"] == "723992" and b["license"]["status"] == "active"
assert b["license"]["source"] == 60 and b["license"]["checkedAt"] == PREV
assert sources[210]["kind"] == "government" and "LicNum=723992" in sources[210]["url"]
# A genuine re-read on 2026-09-11: the licence field now cites the later page.
b["license"].update({"source": 210, "checkedAt": DATE, "expires": "2028-06-30",
                     "entity": "JOE WATTERSON PLUMBING"})
b["checkedAt"] = DATE
b["trade"] = "plumbing"
b["areaText"] = (
    "CSLB records the licence address as 3653 Folsom Street, San Francisco 94110 (Bernal Heights / "
    "Mission). The City's permit registry records this licence at 2186 46th Avenue 94116 — Parkside, "
    "in the Sunset district — on 269 rows under the former firm name “Slemish Plumbing” plus 5 rows "
    "under “Joe Watterson Plumbing”, and at 384 Somerset St 94134 (194 rows) and Po Box 415 94996 "
    "(5 rows). No registry row carries ZIP 94122, so Outer Sunset dispatch is not established by "
    "any official record read here."
)
add_claim("joe-watterson", "License",
          "Re-read directly on 2026-09-11 after the wave-2 read of 2026-09-10: the licence is "
          "still CURRENT AND ACTIVE, class C36 (Plumbing) only, sole ownership, issued 06/14/1996, "
          "expires 06/30/2028, licensee JOE WATTERSON PLUMBING at 3653 Folsom Street, San "
          "Francisco 94110, phone (415) 525-0132. Two independent reads on two dates agree.",
          210,
          "JOE WATTERSON PLUMBING; 3653 FOLSOM STREET, SAN FRANCISCO, CA 94110; Sole Ownership; "
          "issue 06/14/1996; expire 06/30/2028; “This license is current and active”; "
          "class C36 - PLUMBING; “Data current as of 9/11/2026 5:01:55 PM”")
add_claim("joe-watterson", "Bonding",
          "Contractor's bond $25,000 with Philadelphia Indemnity, effective 04/26/2025, with no "
          "cancellation shown on the page — the current $25,000 statutory amount.",
          210, "bond: PHILADELPHIA INDEMNITY $25,000 eff 04/26/2025 (no cancellation)")
add_claim("joe-watterson", "Workers' compensation",
          "Workers' compensation exemption with no employees, effective 05/19/2026. An exemption is "
          "not coverage: if any worker is brought onto the job, certificate of insurance must be "
          "requested directly.",
          210, "WC exempt, no employees, eff 05/19/2026")
add_claim("joe-watterson", "Registry cross-check",
          "Registry re-query grouped by firm name, address and ZIP resolves the wave-2 name-history "
          "flag: licence 723992 appears under TWO firm names and FOUR ZIPs — “Joe Watterson "
          "Plumbing” at 384 Somerset St 94134 (194 rows), 3653 Folsom St 94110 (53 rows), 2186 46th "
          "Av 94116 (5 rows) and Po Box 415 94996 (5 rows), and “Slemish Plumbing” at 2186 46th "
          "Avenue 94116 (269 rows across five address spellings). The 94110 row matches the CSLB "
          "address of record exactly. No 94122 row exists.",
          220,
          "Joe Watterson Plumbing / 384 Somerset St / 94134-0000 / 194; Slemish Plumbing / "
          "2186  46th / 94116 / 164; Joe Watterson Plumbing / 3653 Folsom St / 94110-0000 / 53; "
          "Slemish Plumbing / 2186  46th Av / 94116 / 46; Slemish Plumbing / 2186 46th Ave / "
          "94116 / 36; Slemish Plumbing / 2186 46th Av / 94116 / 22; Joe Watterson Plumbing / "
          "2186  46th Av / 94116 / 5; Joe Watterson Plumbing / Po Box 415 St / 94996-0000 / 5; "
          "Slemish Plumbing / 2186  46th Ave / 94116 / 1")
add_claim("joe-watterson", "Coverage", b["areaText"], 220,
          "Slemish Plumbing / 2186  46th / 94116 / 164 permits (no 94122 row returned)")
add_flag("joe-watterson", "notice",
         "Corroborating re-read: CSLB 723992 was read on 2026-09-10 and again on 2026-09-11, and "
         "both reads show the same active C36 licence, the same 94110 licensee address and the same "
         "06/30/2028 expiry. The licence field now cites the later read; the earlier one is "
         "preserved as a claim so the two dates remain separately traceable.",
         [60, 210])
add_flag("joe-watterson", "discrepancy",
         "Name history remains unresolved as an identity matter even after the grouped re-query: "
         "the same licence number carries both “Slemish Plumbing” and “Joe Watterson Plumbing” in "
         "the City's registry, at four different ZIPs (94134, 94116, 94110, 94996). CSLB shows only "
         "JOE WATTERSON PLUMBING at 94110. A rename, a buy-out or a shared licence number would all "
         "produce this pattern, and nothing read here distinguishes them. Confirm the operating "
         "name in writing before booking.",
         [220, 210, 48])
add_flag("joe-watterson", "gap",
         "No registry row and no CSLB address places this licence in 94122. The record stays at "
         "area “Sunset / citywide stated” on the strength of the 94116 Parkside permit history "
         "only; Outer Sunset dispatch must be asked about directly and is not inferred.",
         [220, 210])
b["gaps"] = [
    "No exact seized bathtub-overflow trip-lever extraction outcome was verified for this "
    "business, and no customer review of any kind is retained.",
    "Which legal name the business trades under today — Slemish Plumbing or Joe Watterson "
    "Plumbing — is not resolved by any source read here.",
    "Outer Sunset (94122) dispatch coverage is not established by CSLB or by the permit registry.",
    "On-site feasibility, a written repair-first scope and applicable insurance are unconfirmed; "
    "the workers' compensation entry is an exemption, not a policy.",
]

# =========================================================================
# 3. Caledonia — direct profile read, negative review, attribution correction,
#    removal from the diagnostic call order.
# =========================================================================
CID = "w6-caledonia-plastering-stucco-inc"
b = biz[CID]
assert b["priority"] == 6, "expected Caledonia at call 06"
r60 = reviews["R60"]
assert r60["business"] == CID and r60["author"] == "Tom S." and r60["published"] == "Jun 2, 2018"
assert r60["quote"].startswith("Quick to respond, fair price")

# 3a. Correct R60 in place: the direct read shows this quote is Vipada W.'s.
r60.update({"author": "Vipada W.", "published": "Oct 5, 2017", "source": 219,
            "access": "page", "identity": "matched"})
r60["analysis"] = (
    "Corrected attribution. The wave-6 row paired this quote with the author “Tom S.” and the date "
    "“Jun 2, 2018” from an indexed extract; the profile page read directly on 2026-09-11 shows the "
    "quote belongs to Vipada W., dated Oct 5, 2017, and that Tom S.'s Jun 2, 2018 review is a "
    "different text about exterior stucco on a backyard structure (retained as R98). On its own "
    "terms this is close finish-side evidence: a hole in a ceiling was made good, the work was "
    "explained beforehand and the site was cleaned afterwards. It does not say what created the "
    "hole, whether plumbing was involved, whether an access panel was framed, or how the texture "
    "was matched."
)

add_review("R98", CID, "Tom S.", "Jun 2, 2018",
           "John Cullen of Caledonia Plastering did outstanding exterior stucco and interior "
           "plaster work for my backyard structure - beautiful wall finish, very uniform and flat, "
           "tightly finished and good to see. He worked his schedule around to get to me quickly, "
           "working on Saturdays. If I have more stucco or plaster work I will definitely check "
           "with him again.",
           "The review wave 6 had mis-paired with R60's quote, restored here under its own author "
           "and date so the correction is auditable rather than a silent deletion. Substantively it "
           "is exterior stucco and a backyard structure — the least relevant trade direction in "
           "this record's sample — though it does show weekend scheduling and a 2018 transaction.",
           "Exterior stucco", 219)

add_review("R89", CID, "Jay D.", None,
           "For all the hard work John does, and some of it fairly good, he is an emotionally "
           "volatile fellow … I also had to agree to pay him in cash so apparently he doesn't "
           "report it to "
           "the IRS. … he moved an electrician's towel-warmer wire in the bathroom and covered up a "
           "square bathroom exhaust with plaster all the way to the small round hole in the middle. "
           "First he refused to fix either. … he took to calling me names, accused me of being "
           "drunk, instead of simply owning up to the mistakes",
           "A long, specific, first-person negative account published by Thumbtack on its San "
           "Francisco drywall-contractors category page against this exact profile slug. Ellipses "
           "mark omitted text, including some of the reviewer's own descriptive asides; nothing "
           "that is reproduced was re-worded. The allegations that matter for this job are "
           "a bathroom exhaust covered with plaster, an electrician's wire moved, corrections "
           "refused on the first request, and a request for cash payment. The tax statement is the "
           "reviewer's inference (“apparently”), not a finding, and is reproduced only because it "
           "bears on how payment would be documented. No date is displayed for this review on the "
           "page it was read from, and it does not appear in the profile's default review list, "
           "which shows five reviews from 2016-2018. One review is not a pattern: the profile's own "
           "distribution is 93% five-star of 56, with 2% one-star.",
           "Negative review / corrections refused", 215, negative=True)

add_review("R90", CID, "Jennifer H.", "Jan 16, 2018",
           "Update: We hired John again to replace a portion of old wall plaster that had to be "
           "removed due to cracking and water damage. He did a great job filling it in and making "
           "it match the rest of the wall. Can’t recommend him enough! … 110 years of paint, "
           "wallpaper, and attempts at removing both had left the walls and ceilings wrecked. He "
           "removed the old ceiling moldings and applied new plaster to all surfaces.",
           "The strongest trade-direction evidence in this record and the reason the licence read "
           "was worth keeping: a repeat customer describes old plaster removed after WATER DAMAGE "
           "and made to match, in a building with 110 years of paint and wallpaper — the same "
           "lath-and-plaster fabric a 1940 Outer Sunset house has. Ellipses mark omitted text. It "
           "is wall and ceiling plaster, not a bathtub overflow access, and it is dated 2018.",
           "Old plaster / water damage", 219)

add_claim(CID, "Platform",
          "Profile page read directly on 2026-09-11: “Excellent 4.9 (56)”, “Hired 65 times”, "
          "“Background checked”, Top Pro badges for 2018, 2019 and 2020 only, payment method "
          "“Ask this pro about their preferred payment method”, and a Credentials section that "
          "contains a background check on John Cullen and NO licence entry. The profile header "
          "reads “Plastering • 94116” and the services offered are restoration of existing plaster, "
          "repair or touchup of existing plaster, plastering for new construction and skim-coating "
          "— no drywall service is listed.",
          219,
          "“Plastering • 94116”; “Excellent 4.9 (56)”; “Hired 65 times”; “Background checked”; "
          "Top Pro 2020, 2019, 2018; “Restoration of existing plaster / Repair or touchup of "
          "existing plaster / Plastering for new construction / Skim-coating”; "
          "“Background Check: John Cullen”")
add_claim(CID, "Availability",
          "For the service and ZIP queried, the profile page displayed Thumbtack's own message "
          "“Sorry this pro can’t do your job, but we know other pros who can.” linking to instant "
          "results for ZIP 94116. That message is specific to the queried service and ZIP — it is "
          "not a general statement that the business has closed — but it is the platform's own "
          "answer for a plastering enquiry in the profile's stated ZIP as of 2026-09-11.",
          219,
          "“Sorry this pro can’t do your job, but we know other pros who can.” with a link to "
          "thumbtack.com/instant-results/?category_pk=152405715933127031&zipCode=94116")
add_claim(CID, "Review sample",
          "The profile's default “Most relevant” review list displays five reviews, dated Dec 12 "
          "2016, Oct 5 2017, Jan 16 2018, May 20 2018 and Jun 2 2018, and no review dated later "
          "than Jun 2, 2018. Review counts by star as displayed: 5★ 93%, 4★ 5%, 3★ 0%, 2★ 0%, "
          "1★ 2%. The negative review by “Jay D.” read on the category page is not in that default "
          "list and carries no displayed date.",
          219,
          "“Vipada W. Oct 5, 2017 • Hired on Thumbtack”; “Karl W. Dec 12, 2016 • Hired on "
          "Thumbtack”; “Jennifer H. Jan 16, 2018 • Hired on Thumbtack”; “Guillaume R. May 20, 2018 "
          "• Hired on Thumbtack”; “Tom S. Jun 2, 2018 • Hired on Thumbtack”; 5★ 93%, 4★ 5%, 3★ 0%, "
          "2★ 0%, 1★ 2%")
add_flag(CID, "hold",
         "Removed from the diagnostic call order on 2026-09-11 and placed on hold. A directly-read "
         "Thumbtack review by “Jay D.” against this profile alleges that corrections were refused, "
         "that a bathroom exhaust was covered with plaster, that an electrician's wire was moved, "
         "and that payment was requested in cash. The same direct read shows the platform answering "
         "“Sorry this pro can’t do your job” for a plastering enquiry in the profile's own stated "
         "ZIP 94116, no displayed review later than Jun 2, 2018, Top Pro status ending in 2020, no "
         "licence in the profile's Credentials section, and a services list with no drywall entry. "
         "Refusing to correct a covered-over bathroom exhaust is the specific failure mode this job "
         "cannot absorb, so the record is held even though the C35 licence is active and the 4.9 "
         "rating across 56 reviews is unchanged.",
         [215, 219, 174])
add_flag(CID, "discrepancy",
         "Review attribution corrected. Wave 6 stored R60 as “Tom S.”, published “Jun 2, 2018”, "
         "from an indexed extract, carrying the quote “Quick to respond, fair price … John took "
         "care of the hole in the ceiling …”. The profile page read directly shows that quote under "
         "Vipada W., Oct 5, 2017, and shows Tom S.'s Jun 2, 2018 review as a separate text about "
         "exterior stucco on a backyard structure. R60's author, date, source, access and identity "
         "have been corrected in place and Tom S.'s real review is retained as R98. This is the "
         "same extract-bleed pattern flagged in wave 4 (SAFENEST / Mike's Water Damage) and wave 6 "
         "(“Singh” on the Jose HandyMan listing), now confirmed by direct read rather than "
         "suspected from index text.",
         [219, 181])
add_flag(CID, "discrepancy",
         "Service ZIP on the platform profile is 94116 (header “Plastering • 94116”), while CSLB "
         "records the licence address as 1551 Judah Street 94122 and Yelp records the same. 94116 "
         "is Parkside, adjacent to but not the Outer Sunset. The area label stays “outer” because "
         "the regulator's own licence page carries the 94122 address, but the platform's stated "
         "service ZIP does not corroborate it.",
         [219, 174])
b["priority"] = None
b["status"] = "hold"
b["rationale"] = (
    "Was call 06 on the wave-6 basis (active C35 licence whose CSLB page records a 94122 address, "
    "4.9 across 56 reviews, dated ceiling and plaster work in buildings of this era). Removed from "
    "the call order on 2026-09-11 after the profile was read directly: a published negative review "
    "alleges refused corrections and a bathroom exhaust covered with plaster, the platform answered "
    "“Sorry this pro can’t do your job” for a plastering enquiry in the profile's own ZIP 94116, no "
    "review is displayed later than Jun 2, 2018, and the services list contains no drywall entry."
)
b["nextStep"] = (
    "Do not call for this job while the hold stands. If the plaster evidence is wanted anyway, "
    "first ask in writing whether the business is currently taking plaster work at 94122, request "
    "the C35 licence status directly from CSLB rather than from the platform profile, and put any "
    "correction obligation and payment method in the written scope before work starts."
)
b["checkedAt"] = DATE
b["gaps"] = list(dict.fromkeys(b["gaps"] + [
    "Whether the business is currently accepting plaster work at 94122 is unresolved: the profile's "
    "stated service ZIP is 94116 and the platform returned “this pro can’t do your job” for that "
    "query.",
    "The negative review read on the category page carries no displayed date, so it cannot be "
    "placed in the timeline of the 2016-2018 reviews shown on the profile.",
]))

# =========================================================================
# 4. New Age Drywall — profile page read directly, four reviews attached.
# =========================================================================
NID = "w5-new-age-drywall-inc"
b = biz[NID]
assert b.get("license") is None
b["trade"] = "drywall"
b["checkedAt"] = DATE
b["area"] = "outside"
b["areaText"] = (
    "The profile page read directly states “Serves Redwood City, CA” and its URL path is "
    "/ca/redwood-city/drywall-repair/, with a header ZIP of 94063 — roughly 25 miles south of the "
    "Outer Sunset. The wave-5 record stored area “SF / Bay Area stated” from a San Francisco "
    "category listing; the direct read narrows that to an outside-area concern. New Age does appear "
    "in Thumbtack's San Francisco drywall-repair AND drywall-contractors category pages, both read "
    "directly, and several retained reviews describe San Francisco jobs, but no statement covering "
    "94122 was retrieved."
)
add_review("R91", NID, "Colin I.", None,
           "A great licensed pro! Did a great job patching the drywall hole in the bathroom ceiling "
           "and texturing it to match the surrounding areas. They did not paint and were upfront "
           "about this. I would highly recommend them to anyone in need of repairing or replacing "
           "drywall.",
           "The single most task-adjacent drywall review in seven waves: a hole in a BATHROOM "
           "CEILING patched and textured to match the surrounding area, with the scope limit "
           "(painting excluded) stated up front rather than discovered afterwards. That is the "
           "exact shape of the ceiling half of this job once a tub overflow has been opened. "
           "“Licensed pro” is the reviewer's own wording, not a CSLB fact; no date is displayed for "
           "this review on the category page it was read from.",
           "Bathroom ceiling patch", 214)
add_review("R92", NID, "Tuan T.", "Jan 8, 2026",
           "New Age Dry Wall did an excellent job patching a ceiling our plumber had to cut into to "
           "fix a leak. They provided a very competitive price, were communicative throughout the "
           "process, showed up on time, and worked fast. The repair was done quickly and correctly, "
           "and the ceiling looks great again. Couldn’t have asked for anything more — highly "
           "recommend!",
           "Dated 8 January 2026 and marked “Hired on Thumbtack”, so it is recent and transactional "
           "rather than legacy: a PLUMBER cut into a ceiling to fix a leak and this business made "
           "the ceiling good. That is precisely the two-trade sequence this job would follow if the "
           "overflow has to be opened. It does not say whether plumbing and drywall were coordinated "
           "by one party, whether an access panel was framed for future entry, or how the texture "
           "was matched to 1940s stock.",
           "Ceiling patch after plumbing access", 218)
add_review("R93", NID, "Ray P.", None,
           "Jaime and his partner did an excellent job repairing the drywall in my ceiling. They "
           "were very professional and friendly and, as an added bonus, even nailed the trim back "
           "in my kitchen. I highly recommend New Age Drywall. Thanks again for the great work!",
           "A second ceiling repair, plus trim reinstated without being asked — relevant because a "
           "ceiling opening below a 1940 tub often disturbs moulding or trim that has to go back. "
           "No date is displayed for this review on the category page it was read from, and the "
           "cause of the ceiling damage is not stated.",
           "Ceiling repair / trim reinstated", 214)
add_review("R94", NID, "Winston P.", None,
           "… Jaime and his crew were extremely responsive to my messages and questions, punctual, "
           "and they’re probably the cleanest drywaller I’ve ever worked with. Probably the most "
           "communicative drywaller or contractor I’ve ever worked with two, which is wonderful. I "
           "will be hiring him again for some more work and he’ll be the first person I call for any "
           "additional drywall (and stucco) work I have in the future.",
           "Written by a reviewer who describes working for a contractor doing building maintenance "
           "and patching drywall himself, so the comparison is informed rather than casual. "
           "Cleanliness and communication are the two attributes that matter most when ceiling work "
           "happens above an occupied floor. Ellipses mark the omitted opening; the spelling "
           "“worked with two” is as published. No date is displayed on the category page.",
           "Cleanliness / communication", 215)
add_claim(NID, "Platform",
          "Profile page read directly on 2026-09-11: “Excellent 4.9 (237)”, “Hired 455 times”, "
          "current Top Pro with badges for 2021-2025, “Background checked”, “License verified”, "
          "6 employees, 6 years in business, “Responds in about 2 hours”, “Serves Redwood City, "
          "CA”, payments by Apple Pay, Cash, Check and Venmo. Services offered include “Patch "
          "damaged drywall”, “Replace one or more sheets of drywall”, “Fill in cracks” and “Remove "
          "popcorn texture”. Review-topic counts as displayed: ceiling・29, patching・23, "
          "texture・17, hole・13.",
          218,
          "“Excellent 4.9 (237)”; “Current Top Pro”; “Hired 455 times”; “Serves Redwood City, CA”; "
          "“Background checked”; “License verified”; “6 employees”; “6 years in business”; Top Pro "
          "2025, 2024, 2023, 2022, 2021; “Patch damaged drywall”; “Replace one or more sheets of "
          "drywall”; “ceiling・29”, “patching・23”, “texture・17”, “hole・13”")
add_claim(NID, "Credentials note",
          "The profile's Credentials section states “License type: C9 – Drywall”, “License state: "
          "CA”, “License verified on 10/29/2020” and “Background Check: Jaime Lombera”. NO CSLB "
          "licence number is published anywhere in the retrieved text, so no CSLB page could be "
          "read and the licence field is deliberately left empty. “License verified” is a "
          "Thumbtack-side badge whose displayed verification date is 10/29/2020, nearly six years "
          "before this read; it is not a CSLB status check and does not show whether the licence is "
          "current today.",
          218,
          "“License type: C9 – Drywall”; “License state: CA”; “License verified on 10/29/2020”; "
          "“Background Check: Jaime Lombera”; “View credential details”")
add_claim(NID, "Coverage", b["areaText"], 218, "“Serves Redwood City, CA”; header “Drywall Repair and Texturing • 94063”")
add_link(NID, "Thumbtack profile (read directly)",
         "https://www.thumbtack.com/ca/redwood-city/drywall-repair/new-age-drywall-inc/service/404118804346175490",
         218)
add_flag(NID, "gap",
         "No CSLB licence number is published on the profile, so no CSLB page could be read and no "
         "licence status, class, bond or workers' compensation entry is verified for this record. "
         "The platform's “License verified” badge carries a displayed verification date of "
         "10/29/2020 and is not a substitute for a regulator read. Ask for the CSLB number and read "
         "it on cslb.ca.gov before booking.",
         [218])
add_flag(NID, "notice",
         "Area label narrowed from “SF / Bay Area stated” to “Outside-area concern” on the strength "
         "of the direct profile read, which states “Serves Redwood City, CA” and sits at URL path "
         "/ca/redwood-city/ with header ZIP 94063. The business still appears in Thumbtack's San "
         "Francisco drywall-repair and drywall-contractors category pages, both read directly, so "
         "San Francisco work is plausible — but Outer Sunset dispatch is a question to ask, not a "
         "fact on file.",
         [218, 214, 215])
b["gaps"] = [
    "No CSLB licence number was published, so licence status, classification, bond and workers' "
    "compensation are all unverified for this record.",
    "No exact seized bathtub-overflow trip-lever extraction outcome was verified; the retained "
    "evidence is drywall ceiling patching, including one bathroom ceiling and one ceiling a plumber "
    "had cut into.",
    "Outer Sunset (94122) dispatch coverage is not established: the profile states a Redwood City "
    "home market.",
    "On-site feasibility, a written repair-first scope and applicable insurance are unconfirmed.",
]

# =========================================================================
# 5-7. Figs, Magaña and Walty — wave-5 records, review and profile URL attached.
# =========================================================================
FID = "w5-figs-drywall-repair-paint"
b = biz[FID]
b["checkedAt"] = DATE
b["area"] = "outside"
b["areaText"] = (
    "The profile URL published alongside this business's review on Thumbtack's San Francisco "
    "drywall-repair page is /id/boise/handyman/figs-drywall-repair/ — Boise, IDAHO, not "
    "California. The wave-5 record stored area “SF / Bay Area stated” from the San Francisco "
    "category listing; the direct read of that listing shows the profile path is out of state, so "
    "the label is narrowed to an outside-area concern. The reviewer describes “an old apartment”, "
    "which does not by itself place the job in San Francisco."
)
add_review("R95", FID, "Allison S.", None,
           "We have an old apartment with thin, crumbly drywall and Dave did a great job quickly "
           "repairing a small hole and went so far as to reiforce it.",
           "Task-adjacent in the useful direction: thin, crumbly drywall in an OLD apartment, a "
           "small hole repaired and reinforced rather than merely filled — the condition a 1940 "
           "building's ceiling stock is often in. The spelling “reiforce” is as published. No date "
           "is displayed for this review, and it says nothing about plumbing, ceilings or texture "
           "matching.",
           "Old building / small hole reinforced", 214)
add_claim(FID, "Listing evidence",
          "Named in the review section of Thumbtack's San Francisco drywall-repair page, read "
          "directly, as “Figs Drywall Repair” — WITHOUT the “& Paint” the wave-5 record stored. The "
          "profile link published beside the review is a Boise, Idaho path under the handyman "
          "category. No rating, review count or hire count is displayed for this entry in the "
          "retrieved text.",
          214,
          "“Figs Drywall Repair” … review by “Allison S.” … link "
          "https://www.thumbtack.com/id/boise/handyman/figs-drywall-repair/service/372641120044548097")
add_link(FID, "Thumbtack profile (Boise, ID path)",
         "https://www.thumbtack.com/id/boise/handyman/figs-drywall-repair/service/372641120044548097",
         214)
add_flag(FID, "discrepancy",
         "Out-of-state profile path. The review is published on Thumbtack's San Francisco "
         "drywall-repair category page, but the profile URL beside it is /id/boise/handyman/ — "
         "Boise, Idaho, under the handyman rather than drywall category. The stored name “Figs "
         "Drywall Repair & Paint” also does not match the listing name “Figs Drywall Repair”. Either "
         "the platform is surfacing a distant profile in a San Francisco result set, or two "
         "similarly named businesses have been conflated; nothing read here distinguishes them, so "
         "no San Francisco coverage is inferred.",
         [214])
b["gaps"] = [
    "Whether this is a San Francisco business at all is unresolved: the profile URL published "
    "beside its review is a Boise, Idaho path.",
    "No CSLB licence number was published and none was read, so licence status and classification "
    "are unverified.",
    "No exact seized bathtub-overflow trip-lever extraction outcome was verified for this business.",
    "On-site feasibility, a written repair-first scope and applicable insurance are unconfirmed.",
]

MID = "w5-maga-a-time-handyman"
b = biz[MID]
b["checkedAt"] = DATE
add_review("R96", MID, "Priyam m.", None,
           "I had him for a small drywall repair. He finished the job as promised and his "
           "workmanship was good. I plan on using him on future projects as well",
           "A small drywall repair completed as promised, with repeat intent. Thin but genuine "
           "task-adjacent evidence for the patch half of this job; it says nothing about ceilings, "
           "plaster, texture matching or plumbing access, and no date is displayed for it. The "
           "published text renders “drywall repair” as one joined word; the space has been restored "
           "and no word was added or re-ordered.",
           "Small drywall repair", 214)
add_claim(MID, "Listing evidence",
          "Named in the review section of Thumbtack's San Francisco drywall-repair page, read "
          "directly, as “Magaña Time handyman” with a San Francisco profile path under the handyman "
          "category. No rating, review count or hire count is displayed for this entry in the "
          "retrieved text.",
          214,
          "“Magaña Time handyman” … review by “Priyam m.” … link "
          "https://www.thumbtack.com/ca/san-francisco/handyman/maga-time-handyman/service/450414062583914508")
add_link(MID, "Thumbtack profile (read directly)",
         "https://www.thumbtack.com/ca/san-francisco/handyman/maga-time-handyman/service/450414062583914508",
         214)
add_flag(MID, "notice",
         "The profile path is /ca/san-francisco/handyman/, so the platform places this pro in San "
         "Francisco, but under the HANDYMAN category rather than drywall, and the stored name "
         "capitalisation differs from the listing (“Magaña Time handyman”). A handyman classification "
         "is not a CSLB classification: in California work exceeding $500 in combined labour and "
         "materials requires an appropriate licence, and none was published or read for this record.",
         [214])

WID = "w5-walty-handy-service-pro"
b = biz[WID]
b["checkedAt"] = DATE
b["area"] = "outside"
b["areaText"] = (
    "The profile URL published beside this business's review on Thumbtack's San Francisco "
    "drywall-repair page is /ca/san-pablo/moving-companies/walty-handy-service-pro/ — San Pablo in "
    "Contra Costa County, roughly 20 miles north-east of the Outer Sunset, and filed under the "
    "MOVING COMPANIES category. The wave-5 record stored area “SF / Bay Area stated” from the San "
    "Francisco category listing; the direct read narrows that to an outside-area concern."
)
add_review("R97", WID, "Erika M.", None,
           "Walty did a great job patching / repairing drywall for a client of mine! He was "
           "extremely communicative and did a great job with the circumstances he was given. Thank "
           "you!",
           "Drywall patching, with communication singled out. Note the reviewer writes “for a client "
           "of mine”, so this is likely a property manager, agent or contractor relaying a job "
           "rather than an occupant describing their own home — relevant because the person who "
           "would authorise access and approve a ceiling patch here is not the person quoted. "
           "“With the circumstances he was given” also implies constrained site conditions without "
           "saying what they were. No date is displayed; the published text renders “repairing "
           "drywall” as one joined word and the space has been restored.",
           "Drywall patching / third-party reviewer", 214)
add_claim(WID, "Listing evidence",
          "Named in the review section of Thumbtack's San Francisco drywall-repair page, read "
          "directly, as “Walty Handy Service Pro”, with the profile link published beside the review "
          "pointing at a San Pablo, CA path under the moving-companies category. No rating, review "
          "count or hire count is displayed for this entry in the retrieved text.",
          214,
          "“Walty Handy Service Pro” … review by “Erika M.” … link "
          "https://www.thumbtack.com/ca/san-pablo/moving-companies/walty-handy-service-pro/service/348368959797469193")
add_link(WID, "Thumbtack profile (San Pablo, CA path)",
         "https://www.thumbtack.com/ca/san-pablo/moving-companies/walty-handy-service-pro/service/348368959797469193",
         214)
add_flag(WID, "discrepancy",
         "Category and location mismatch. The retained review is about drywall patching and appears "
         "on Thumbtack's San Francisco drywall-repair page, but the profile URL published beside it "
         "is /ca/san-pablo/moving-companies/ — a Contra Costa County town under a MOVING COMPANIES "
         "category. A drywall repair review attached to a moving-company profile in another city "
         "does not establish San Francisco drywall work, so no coverage is inferred and the area "
         "label is narrowed.",
         [214])
b["gaps"] = [
    "Whether this business performs drywall work in San Francisco at all is unresolved: its profile "
    "path is a San Pablo moving-companies listing.",
    "No CSLB licence number was published and none was read, so licence status and classification "
    "are unverified.",
    "The only retained review is written by someone describing a job done “for a client of mine”, "
    "not by an occupant of the property.",
    "On-site feasibility, a written repair-first scope and applicable insurance are unconfirmed.",
]

# =========================================================================
# 8. Renumber the diagnostic call order after Caledonia's removal.
# =========================================================================
RENUMBER = {
    "w6-building-efficiency-inc": (7, 6),
    "w6-faherty-plumbing-and-heating": (8, 7),
    "w6-de-barra-plumbing": (9, 8),
    "w7-michael-kuenzli-plumbing-co": (10, 9),
}
for bid, (old, new) in RENUMBER.items():
    assert biz[bid]["priority"] == old, (bid, biz[bid]["priority"], old)
    biz[bid]["priority"] = new
k = biz["w7-michael-kuenzli-plumbing-co"]
assert k["license"]["status"] == "active" and k["area"] == "outer" and "94122" in k["areaText"]
# Kuenzli's stored rationale never names its own call number, so nothing there
# needs rewording; only the ordering metadata changes.

short = sorted((b for b in data["businesses"] if b.get("priority")), key=lambda x: x["priority"])
assert [b["priority"] for b in short] == [1, 2, 3, 4, 5, 6, 7, 8, 9], [b["priority"] for b in short]
for b_ in short:
    assert b_["license"] and b_["license"]["status"] == "active", b_["id"]
    assert b_["license"]["checkedAt"] == b_["checkedAt"], b_["id"]
    assert any(combo <= set(b_["license"]["classes"]) for combo in TRADE_REQUIRES[b_.get("trade") or "plumbing"]), b_["id"]
    assert b_["rationale"] and b_["nextStep"], b_["id"]
    if b_["priority"] > 5:
        assert b_["area"] == "outer" and "94122" in b_["areaText"], b_["id"]
        assert re.search(r"SAN FRANCISCO|INC|CO|PLUMBING|STUCCO", b_["license"]["entity"], re.I), b_["id"]

# =========================================================================
# 9. Methodology: record the correction and the call-order change.
# =========================================================================
m = data["methodology"]
assert "Pass 13" in m["passes"]
m["passes"] = m["passes"].rstrip() + (
    " Pass 14 (wave 7 follow-up, Sep 11 2026): direct reads of two Thumbtack pro profiles and two "
    "grouped registry re-queries, applied to seven PRE-EXISTING records rather than counted as new "
    "rows — an expired C-36 licence attached to a wave-1 record, a corroborating CSLB re-read and a "
    "resolved name history on a wave-2 record, a wave-6 shortlisted record removed from the call "
    "order and held on a directly-read negative review plus the platform's own “this pro can't do "
    "your job” response, four dated drywall-ceiling reviews attached to a wave-5 record whose "
    "platform C-9 credential carries no readable CSLB number, and three wave-5 records given their "
    "verbatim reviews and out-of-area profile paths. One wave-6 review attribution was corrected in "
    "place after a direct read disproved it, and the review it had been mis-paired with was "
    "restored under its real author."
)
def rewrite_ranking(old, new):
    assert old in m["ranking"], f"ranking text drifted, cannot rewrite: {old[:60]!r}"
    m["ranking"] = m["ranking"].replace(old, new, 1)

rewrite_ranking("Calls 06-09 were added in wave 6", "Calls 06-08 were added in wave 6")
rewrite_ranking(
    "Call 10 was added in wave 7 on that same strict basis",
    "Call 09 was added in wave 7 on that same strict basis")
rewrite_ranking(
    "Call 06 additionally carries a directly-read negative Thumbtack review alleging refused "
    "corrections and undisclosed cash payment; that review is attached to the record and the "
    "caveat is repeated in its call rationale rather than being averaged away.",
    "Wave 6's Caledonia Plastering & Stucco was call 06 and has been REMOVED from the call order "
    "and placed on hold: its profile, read directly, published a negative review alleging refused "
    "corrections, a bathroom exhaust covered with plaster and a request for cash payment, answered "
    "“this pro can't do your job” for a plastering enquiry in its own stated ZIP 94116, showed no "
    "review later than 2018 and listed no drywall service. Its active C-35 licence at a 94122 CSLB "
    "address is still recorded on the held row, and calls 06-09 were renumbered accordingly. A "
    "4.9 rating across 56 reviews is not treated as cancelling out a specific, directly-read "
    "allegation about corrections refused in a bathroom.")
assert "Call 10" not in m["ranking"] and "Calls 06-09" not in m["ranking"]

# =========================================================================
# Final invariants (mirror merge_wave7.py).
# =========================================================================
assert data["master"] == []
assert not any(b_["master"] for b_ in data["businesses"])
assert not any(b_.get("exactMatch") or b_.get("insuranceVerified") or b_.get("scopeConfirmed")
               for b_ in data["businesses"])
assert json.dumps(data["compliance"], sort_keys=True, ensure_ascii=False) == compliance_before
ids = [b_["id"] for b_ in data["businesses"]]
assert len(ids) == len(set(ids))
sids = [s["id"] for s in data["sources"]]
assert len(sids) == len(set(sids))
rids = [r["id"] for r in data["reviews"]]
assert len(rids) == len(set(rids))
fp = {}
for r in data["reviews"]:
    key = (r["business"], r["author"], r["quote"][:60])
    assert key not in fp, f"duplicate review content: {r['id']} vs {fp[key]}"
    fp[key] = r["id"]
for r in data["reviews"]:
    assert sources.get(r["source"]), r["id"]
    assert len(r["quote"]) < 500 and len(r["analysis"]) > 30, r["id"]
    assert r["exactTask"] is False, r["id"]
    assert r["checkedAt"] in data["researchDates"], r["id"]
    assert r["identity"] in {"indexed", "matched", "unverified-username", "company-published"}, r["id"]
for b_ in data["businesses"]:
    assert b_["checkedAt"] in data["researchDates"], b_["id"]
    assert b_["claims"] and b_["claims"][0]["field"] == "Discovery", b_["id"]
    assert len(b_["gaps"]) >= 2, b_["id"]
    blob = json.dumps(b_, ensure_ascii=False).lower()
    for phrase in FORBIDDEN:
        assert phrase not in blob, f"{b_['id']} contains forbidden phrase {phrase!r}"
    for c in b_["claims"]:
        assert c["source"] in sources, (b_["id"], c["source"])
        assert c["text"].strip() and c["excerpt"].strip(), b_["id"]
    for f in b_["flags"]:
        assert f["level"] in {"hold", "notice", "gap", "discrepancy"}, b_["id"]
        assert f["sources"] and all(s in sources for s in f["sources"]), b_["id"]
    for p in b_["platformLinks"]:
        assert p["source"] in sources and p["url"].startswith("https://"), b_["id"]
    if b_["phone"]:
        assert b_["phoneSource"] in sources, b_["id"]
    lic = b_.get("license")
    if lic:
        s_ = sources[lic["source"]]
        assert s_["kind"] == "government" and "cslb.ca.gov" in s_["url"], b_["id"]
        assert str(lic["number"]) in s_["url"], b_["id"]
        assert lic["status"] in {"active"} | NOT_ACTIVE, b_["id"]
        assert lic["checkedAt"] == b_["checkedAt"], b_["id"]
        assert set(lic["classes"]) <= ALLOWED_CLASSES, b_["id"]
        if lic["status"] == "active":
            assert lic["expires"] > lic["checkedAt"], b_["id"]
        else:
            assert b_["status"] in ("hold", "excluded") or any(
                f["level"] == "hold" for f in b_["flags"]), b_["id"]
        if b_.get("trade"):
            assert any(combo <= set(lic["classes"]) for combo in TRADE_REQUIRES[b_["trade"]]), \
                f"{b_['id']}: {lic['classes']} does not support trade {b_['trade']}"
    for rid in b_["reviewIds"]:
        assert reviews[rid]["business"] == b_["id"], (b_["id"], rid)
for b_ in (biz[t] for t in ("bill-callaway", "joe-watterson", CID, NID, FID, MID, WID)):
    assert b_["checkedAt"] == DATE, b_["id"]

TARGET.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
active = sum(1 for b_ in data["businesses"] if b_.get("license") and b_["license"]["status"] == "active")
inactive = sum(1 for b_ in data["businesses"] if b_.get("license") and b_["license"]["status"] in NOT_ACTIVE)
print(f"patched research.json: {len(data['businesses'])} businesses, {len(data['sources'])} sources, "
      f"{len(data['reviews'])} reviews")
print(f"  licence records: {active} active, {inactive} non-active")
print("  call order: " + ", ".join("%02d %s" % (b_["priority"], b_["name"]) for b_ in short))
print(f"  held after patch: Caledonia (was call 06), bill-callaway (expired 660638)")
