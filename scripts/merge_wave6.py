#!/usr/bin/env python3
"""Merge wave 6 into data/research.json.

Generalises scripts/merge_wave.py for a mixed-trade wave. Wave 6 contains
plumbing (C36), drywall (C-9), lathing & plastering (C35), general building (B)
and general engineering (A) records, because the job needs plumbing AND
drywall/ceiling work. The old merge hard-required C36 on every license, which
would have forced a drywall record to be recorded without its verified
credential — a worse outcome than a trade-aware rule.

Fail-closed invariants (all checked BEFORE anything is written):

  * wave ids and names must not collide with any existing record
    (case-insensitive, across all 301 records after merge);
  * every claim, flag, website, phone, platform link and review must point at
    a source id that exists either in the merged dataset or in this wave;
  * a license may only come from a government source on cslb.ca.gov, must name
    a legal entity, must use classifications from a fixed allowed set, and must
    carry the classification that matches the record's declared trade;
  * an "active" license must expire after its own check date;
  * expired / canceled / suspended licenses must carry a booking hold flag;
  * nothing is promoted: master stays empty, exactMatch / insuranceVerified /
    scopeConfirmed stay absent or false on every record;
  * reviews keep unique ids, a business back-reference inside this wave, a
    quote under 500 characters, an analysis over 30 characters and
    exactTask=False.

The wave is dated 2026-09-11, a later snapshot than waves 1-5 (2026-09-10).
Records keep their own true check date; the dataset gains `researchDates` and
`waves` so no record's date is rewritten to make an assertion pass.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "research.json"

ALLOWED_ACCESS = {
    "page",
    "search-extract",
    "blocked-with-search-extract",
    "redirect",
    "expired-site",
    "review-panel-unavailable",
}
ALLOWED_KINDS = {"business", "community", "directory", "government", "platform", "testimonial"}

# CSLB classifications this project is willing to store, and the classification
# each declared trade must actually hold on the CSLB page that was read.
ALLOWED_CLASSES = {
    "C36", "C-9", "C35", "C-4", "C4", "C10", "C16", "C20", "C42", "D56", "B", "A",
}
TRADE_REQUIRES = {
    "plumbing": [{"C36"}],
    "drywall": [{"C-9"}, {"C-9", "B"}, {"B"}],
    "plaster": [{"C35"}, {"C35", "B"}, {"B"}],
    "finish": [{"C-9"}, {"C35"}, {"B"}, {"C-9", "B"}],
    "general": [{"B"}],
    "engineering": [{"A"}],
    "multi-trade": [{"B"}, {"C36"}, {"B", "C36"}],
}
NOT_ACTIVE = {"expired", "canceled", "cancelled", "suspended", "inactive", "revoked"}


def class_ok(trade, classes):
    """A record's declared trade must be supported by the classifications read."""
    cs = set(classes)
    if trade not in TRADE_REQUIRES:
        return False
    # every stored classification must be a real CSLB class we recognise
    if not cs <= ALLOWED_CLASSES:
        return False
    # at least one accepted combination must be fully present
    return any(combo <= cs for combo in TRADE_REQUIRES[trade])


def main(wave_path=None):
    wave_path = Path(wave_path or (ROOT / "data" / "wave6.json"))
    data = json.loads(TARGET.read_text())
    wave = json.loads(wave_path.read_text())
    wdate = wave["researchedAt"]

    # ---- idempotence guard -------------------------------------------------
    existing_ids = {b["id"] for b in data["businesses"]}
    if existing_ids & {b["id"] for b in wave["businesses"]}:
        sys.exit(f"REFUSING: {wave_path.name} is already merged into research.json")

    src_ids = {s["id"] for s in data["sources"]}
    wave_src_ids = {s["id"] for s in wave["sources"]}
    assert not src_ids & wave_src_ids, "wave reuses an existing source id"
    valid = src_ids | wave_src_ids

    existing_names = {b["name"].strip().lower() for b in data["businesses"]}
    new_ids = [b["id"] for b in wave["businesses"]]
    new_names = [b["name"].strip().lower() for b in wave["businesses"]]
    assert len(new_ids) == len(set(new_ids)), "duplicate ids inside wave"
    assert len(new_names) == len(set(new_names)), "duplicate names inside wave"
    dupes = existing_names & set(new_names)
    assert not dupes, f"wave reuses an existing business name: {sorted(dupes)}"

    # ---- per-record invariants --------------------------------------------
    for b in wave["businesses"]:
        bid = b["id"]
        assert b["claims"] and b["claims"][0]["field"] == "Discovery", bid
        assert len(b["gaps"]) >= 2, bid
        assert b["checkedAt"] == wdate, bid
        assert b["master"] is False and b["exactMatch"] is False, bid
        assert not b.get("insuranceVerified") and not b.get("scopeConfirmed"), bid
        assert b.get("trade") in TRADE_REQUIRES, f"{bid}: unknown trade"
        for c in b["claims"]:
            assert c["source"] in valid, (bid, c["source"])
            assert c["excerpt"].strip() and c["text"].strip(), bid
        if b.get("website"):
            assert b["websiteSource"] in valid, bid
            assert b["website"].startswith("https://"), bid
        if b.get("phone"):
            assert b["phoneSource"] in valid, bid
        for f in b.get("flags", []):
            assert f["sources"] and all(s in valid for s in f["sources"]), bid
            assert f["level"] in {"hold", "gap", "notice", "discrepancy"}, bid
        for p in b.get("platformLinks", []):
            assert p["source"] in valid, bid
        lic = b.get("license")
        if lic:
            assert lic["source"] in valid, bid
            lic_src = next(s for s in data["sources"] + wave["sources"]
                           if s["id"] == lic["source"])
            assert lic_src["kind"] == "government", bid
            assert "cslb.ca.gov" in lic_src["url"], bid
            assert str(lic["number"]) in lic_src["url"], f"{bid}: source/url number mismatch"
            assert lic["entity"], bid
            assert lic["checkedAt"] == wdate, bid
            assert lic["classes"], bid
            assert class_ok(b["trade"], lic["classes"]), \
                f"{bid}: classes {lic['classes']} do not support trade {b['trade']}"
            if lic["status"] == "active":
                assert lic["expires"] > wdate, f"{bid}: active but expires {lic['expires']}"
            else:
                assert lic["status"] in NOT_ACTIVE, f"{bid}: unknown license status"
                assert any(f["level"] == "hold" for f in b["flags"]), \
                    f"{bid}: non-active license without a booking hold"

    existing_reviews = {r["id"] for r in data["reviews"]}
    new_bid = set(new_ids)
    for r in wave["reviews"]:
        assert r["id"] not in existing_reviews, r["id"]
        assert r["business"] in new_bid, r["id"]
        assert r["source"] in valid, r["id"]
        assert len(r["quote"]) < 500 and len(r["analysis"]) > 30, r["id"]
        assert r["exactTask"] is False, r["id"]
        assert r["checkedAt"] == wdate, r["id"]

    for s in wave["sources"]:
        assert s["access"] in ALLOWED_ACCESS, s["id"]
        assert s["kind"] in ALLOWED_KINDS, s["id"]
        assert s["checkedAt"] == wdate, s["id"]
        assert s["url"].startswith("https://"), s["id"]
        assert s["title"].strip(), s["id"]

    # ---- merge -------------------------------------------------------------
    data["businesses"].extend(wave["businesses"])
    data["sources"].extend(wave["sources"])
    data["reviews"].extend(wave["reviews"])

    # ---- dataset-level metadata (never rewrites an older record's date) -----
    prior_dates = data.get("researchDates") or [data["researchedAt"]]
    dates = sorted(set(prior_dates) | {wdate})
    data["researchDates"] = dates
    data["researchedAt"] = dates[-1]

    prior_waves = data.get("waves") or [
        {"wave": 1, "date": "2026-09-10", "count": None},
        {"wave": 2, "date": "2026-09-10", "count": 50},
        {"wave": 3, "date": "2026-09-10", "count": 51},
        {"wave": 4, "date": "2026-09-10", "count": 50},
        {"wave": 5, "date": "2026-09-10", "count": 50},
    ]
    if prior_waves[0]["count"] is None:
        prior_waves[0]["count"] = len(existing_ids) - sum(w["count"] for w in prior_waves[1:])
    prior_waves.append({"wave": wave["wave"], "date": wdate, "count": len(new_ids),
                        "cslbReads": sum(1 for s in wave["sources"]
                                         if s["kind"] == "government"
                                         and "cslb.ca.gov" in s["url"])})
    data["waves"] = prior_waves
    assert sum(w["count"] for w in data["waves"]) == len(data["businesses"]), \
        "wave counts no longer add up to the directory total"

    data["methodology"]["passes"] = (
        "Pass 1 (wave 1, Sep 10 2026): 50-entry discovery pool. "
        "Pass 2 (wave 2, Sep 10 2026): 50 new entries from Yellow Pages page reads, indexed "
        "Yelp/Thumbtack/Reddit extracts, Reddit recommendation threads and the official SF DBI "
        "permit-firm registry (data.sf.gov k6kv-9kix), with 20 direct CSLB license page reads. "
        "Pass 3: entity resolution and de-duplication (name-alike firms kept separate; identity "
        "conflicts flagged). "
        "Pass 4: targeted review sampling with provenance labels. "
        "Pass 5: structural audits (tests), fail-closed master admission, final site build. "
        "Pass 6 (wave 6, Sep 11 2026): 50 new entries discovered through the official SF DBI "
        "\u201cPlumbing Permits Contacts\u201d open-data API queried directly by firm ZIP (94122 Outer "
        "Sunset, 94116 Parkside), plus indexed Yelp/Thumbtack/BBB/BuildZoom/Angi extracts for "
        "the drywall and plaster trades. 22 CSLB license detail pages read directly. "
        "Pass 7: line-by-line re-verification of every wave-6 field against the page it cites, "
        "entity resolution against all pre-existing records, and rejection logging. "
        "Pass 8: classification-versus-scope audit \u2014 each license's CSLB classification list "
        "compared with the work it would lawfully cover, plus suspension, cancellation, bond "
        "cancellation, workers-compensation-exemption and near-expiry detection. "
        "Pass 9: compliance verification against the official City & County of San Francisco "
        "permit service page, dataset-level date/wave bookkeeping, structural tests and the "
        "final site build."
    )
    data["methodology"]["ranking"] = (
        "Editorial diagnostic-call order, not star averages and not a guarantee. Calls 01-05 "
        "carry adjacent task evidence, primary-source area coverage and direct CSLB checks from "
        "waves 1-2. Calls 06-09 were added in wave 6 on a stricter basis: each is an active "
        "license whose CSLB page itself records a 94122 Outer Sunset business address, and "
        "each holds the classification its trade requires (C35 lathing & plastering, B+C36 "
        "general building/plumbing, C36 plumbing)."
    )
    data["methodology"]["governmentSources"] = (
        "CSLB license detail pages read directly (59 distinct license numbers across waves 1, 2, "
        "4 and 6); the official SF DBI \u201cPlumbing Permits Contacts\u201d open-data registry "
        "(data.sf.gov dataset k6kv-9kix, provenance: official) queried directly by firm ZIP and "
        "by firm name, including its dataset metadata record; and the official SF.gov / "
        "Department of Building Inspection plumbing & mechanical permit service page. Registry "
        "rows are historical permit contacts without in-dataset dates: they prove a recorded "
        "address and license linkage, never present operation."
    )

    # ---- verified compliance facts (official City source) ------------------
    data["compliance"] = {
        "jurisdiction": "City & County of San Francisco \u00b7 Department of Building Inspection",
        "sourceId": 175,
        "checkedAt": wdate,
        "position": (
            "This project researches credentials and reviews. It does not plan, sequence, "
            "recommend or assist work that avoids a required permit or inspection, and it does "
            "not rank contractors by willingness to work outside DBI requirements. The official "
            "City rules below are reproduced so the scope decision is made against the actual "
            "regulation rather than an assumption."
        ),
        "facts": [
            "You need a permit before cutting into or replacing pipes, particularly pipes that "
            "will be covered by a wall or buried in the ground.",
            "Exemptions are listed in San Francisco Plumbing Code Section 104.2 (Exempt Work), "
            "linked from the same official page.",
            "You must be a licensed contractor registered with the City of San Francisco to "
            "apply for a plumbing or mechanical permit online.",
            "Only owner-installers of stand-alone single family dwellings may apply for a "
            "plumbing or mechanical permit to do the work themselves.",
            "Before covering pipes, you must have it inspected.",
            "Permit fees depend on the scope of work; DBI publishes a plumbing/mechanical fee "
            "schedule.",
            "Plumbing permits can be applied for online through DBI's Plumbing Permitting and "
            "Inspection Scheduling system, or in person at Permit Services, DBI, 49 South Van "
            "Ness Avenue, 2nd floor, San Francisco, CA 94103, Monday to Friday 9:00am to 5:00pm.",
            "General permitting questions: 628-652-3200 or dbicustomerservice@sfgov.org.",
        ],
        "officialLinks": [
            {"label": "Apply for a plumbing and mechanical permit (SF.gov / DBI)",
             "url": "https://www.sf.gov/apply-plumbing-and-mechanical-permit", "sourceId": 175},
            {"label": "Plumbing Permitting and Inspection Scheduling system (DBI)",
             "url": "https://dbiweb02.sfgov.org/dbi_plumbing/", "sourceId": 175},
            {"label": "Register as a City-licensed contractor (SF.gov)",
             "url": "https://www.sf.gov/register-city-licensed-contractor/", "sourceId": 175},
            {"label": "DBI plumbing / mechanical permit fee schedule (PDF)",
             "url": "https://www.sf.gov/documents/44100/Table_1A-C_-_Plumbing_Mechanical_2026.pdf",
             "sourceId": 175},
            {"label": "Schedule and pay for an inspection (SF.gov)",
             "url": "https://www.sf.gov/schedule-and-pay-your-inspection/", "sourceId": 175},
        ],
        "notRetrieved": [
            {"label": "San Francisco Plumbing Code Section 104.2 \u2014 Exempt Work",
             "url": "https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_building/0-0-0-85830",
             "note": "Referenced by the official SF.gov permit page. The code text was NOT "
                     "retrieved in this pass, so no exemption is quoted or asserted here. Read "
                     "the section directly, or ask DBI, before deciding that any part of a scope "
                     "is exempt."},
        ],
        "why": (
            "Two verified facts make this relevant rather than theoretical. First, the City rule "
            "turns on whether pipes are cut into or replaced and then covered \u2014 which is the "
            "definition of concealed work. Second, wave 6 found a customer review stating that "
            "one Outer Sunset plastering firm's lath and plaster work \u201cpass the city inspection "
            "with no problems\u201d: contractors who work inside the permit system treat inspection "
            "as normal, and that is a question worth asking any candidate."
        ),
    }

    # ---- final invariants --------------------------------------------------
    assert data["master"] == []
    assert not any(b["master"] for b in data["businesses"])
    assert not any(b.get("insuranceVerified") or b.get("scopeConfirmed")
                   or b.get("exactMatch") for b in data["businesses"])
    all_names = [b["name"].strip().lower() for b in data["businesses"]]
    assert len(all_names) == len(set(all_names)), "duplicate business name after merge"
    all_ids = [b["id"] for b in data["businesses"]]
    assert len(all_ids) == len(set(all_ids)), "duplicate business id after merge"
    sids = [s["id"] for s in data["sources"]]
    assert len(sids) == len(set(sids)), "duplicate source id after merge"
    rid = [r["id"] for r in data["reviews"]]
    assert len(rid) == len(set(rid)), "duplicate review id after merge"
    smap = {s["id"]: s for s in data["sources"]}
    bmap = {b["id"]: b for b in data["businesses"]}
    for b in data["businesses"]:
        assert b["checkedAt"] in data["researchDates"], b["id"]
        for c in b["claims"]:
            assert c["source"] in smap, b["id"]
        if b.get("license"):
            assert smap[b["license"]["source"]]["kind"] == "government", b["id"]
            assert b["license"]["checkedAt"] == b["checkedAt"], b["id"]
            if b["license"]["status"] == "active":
                assert b["license"]["expires"] > b["license"]["checkedAt"], b["id"]
        for rev_id in b["reviewIds"]:
            assert rev_id in {x["id"] for x in data["reviews"]}, (b["id"], rev_id)
    for r in data["reviews"]:
        assert r["business"] in bmap, r["id"]
        assert r["id"] in bmap[r["business"]]["reviewIds"], r["id"]
        assert r["source"] in smap, r["id"]
        assert r["checkedAt"] in data["researchDates"], r["id"]
    for k in ("propertyAddress", "occupants", "privateNotes", "accessInstructions"):
        assert k not in data, k
        for b in data["businesses"]:
            assert k not in b, (b["id"], k)
    for s in data["sources"]:
        assert s["access"] in ALLOWED_ACCESS and s["checkedAt"] in data["researchDates"], s["id"]

    data["schemaVersion"] = 2
    TARGET.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    active = sum(1 for b in data["businesses"]
                 if b.get("license") and b["license"]["status"] == "active")
    cslb = len({s["url"] for s in data["sources"]
                if "cslb.ca.gov" in s["url"] and s["access"] == "page"})
    print(f"merged {wave_path.name}: +{len(new_ids)} businesses, +{len(wave['sources'])} "
          f"sources, +{len(wave['reviews'])} reviews")
    print(f"research.json now: {len(data['businesses'])} businesses, {len(data['sources'])} "
          f"sources, {len(data['reviews'])} reviews | {active} active licenses | "
          f"{cslb} distinct CSLB pages read | dates {data['researchDates']}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
