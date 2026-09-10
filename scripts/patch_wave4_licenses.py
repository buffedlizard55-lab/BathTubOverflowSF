#!/usr/bin/env python3
"""Wave-4 follow-up patch: attach THIS SESSION's direct CSLB reads to three
pre-existing entries, and two task-relevant business-site reads to existing
entries. Run AFTER scripts/merge_wave.py data/wave4.json.

What changes and why (all verified this session, 2026-09-10):
- magic      — CSLB 698806 read directly: MAGIC PLUMBING dba MAGIC PLUMBING
               HEATING & COOLING, SF 94114. Active C36+C20, exp 03/31/2027.
               Its prior "needs primary-source checks" flag is updated to
               record the completed registry step.
- rooter-247 — CSLB 954813 read directly: 24/7 ROOTER AND PLUMBING SERVICES
               INC dba A & R PLUMBING, SF 94124. Active C36(+D56,+A),
               exp 11/30/2026 — near-term expiry flagged for recheck.
- ab         — CSLB 876212 read directly: A B PLUMBING, 12909 Skyline Blvd,
               OAKLAND 94619. Active C36, exp 04/30/2028. Oakland record
               address plus a bond cancellation date (10/03/2026) and a
               no-employees workers-comp exemption are flagged for review.
- heises     — Its official drain page (source 106) publishes dated check-ins
               of cabled shower/tub drains and tub-stopper work in SF. Added
               as a task-adjacent claim plus one clearly-labeled
               company-published excerpt (R59).
- five-star  — Its repiping page (source 131) markets galvanized replacement
               naming the Sunset; added as a business-claim (registry caveat
               on 996627 reissue already flagged in wave 2).
- chosen     — Its repiping page (source 132) markets PEX replacement of
               galvanized/copper; added as a business-claim.

Fail-closed rules mirror merge_wave.py: license sources must be government
kind with a cslb.ca.gov URL and class C36; nothing is promoted to master;
review invariants (business back-reference, length, exactTask=False) hold.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "research.json"
RESEARCHED = "2026-09-10"

data = json.loads(TARGET.read_text())
assert data["researchedAt"] == RESEARCHED
sources = {s["id"]: s for s in data["sources"]}
biz = {b["id"]: b for b in data["businesses"]}
reviews = {r["id"] for r in data["reviews"]}


def license_source(sid):
    s = sources[sid]
    assert s["kind"] == "government" and "cslb.ca.gov" in s["url"], sid
    return sid


def attach_license(bid, lic):
    b = biz[bid]
    lic_source = license_source(lic["source"])
    assert lic["source"] == lic_source
    assert "C36" in lic["classes"]
    assert lic["status"] == "active" and lic["expires"] > RESEARCHED
    lic["checkedAt"] = RESEARCHED
    assert b.get("license") is None, f"{bid} already has a license — refusing to overwrite"
    b["license"] = lic
    return b


def add_claim(bid, field, text, source, excerpt):
    assert source in sources
    biz[bid]["claims"].append({"field": field, "text": text,
                               "source": source, "excerpt": excerpt})


def add_flag(bid, level, text, srcs):
    for s in srcs:
        assert s in sources
    biz[bid]["flags"].append({"level": level, "text": text, "sources": srcs})


def set_phone(bid, phone, source):
    assert source in sources
    b = biz[bid]
    assert b.get("phone") in (None, phone), f"{bid} phone conflict: {b.get('phone')}"
    b["phone"] = phone
    b["phoneSource"] = source


# ---- Magic Plumbing (698806) ----
attach_license("magic", {
    "number": "698806", "status": "active",
    "entity": "MAGIC PLUMBING · dba MAGIC PLUMBING HEATING & COOLING",
    "expires": "2027-03-31", "classes": ["C36", "C20"], "source": 101,
})
add_claim("magic", "License",
          "Current and active · C36, C20",
          101, "This license is current and active.")
set_phone("magic", "(415) 441-2255", 101)
magic_flags = biz["magic"]["flags"]
assert len(magic_flags) == 1 and magic_flags[0]["level"] in ("notice", "gap"), magic_flags
magic_flags[0]["text"] = (
    "Registry step completed 09/10/2026: direct CSLB read confirms #698806, active "
    "C36+C20 under MAGIC PLUMBING (SF 94114). Remaining unverified: current service "
    "menu, exact seized-overflow experience and area dispatch — the earlier "
    "'directory-linked website' caution applies to those, not to legal identity."
)
magic_flags[0]["sources"] = sorted(set(magic_flags[0]["sources"]) | {101})

# ---- 24-7 Rooter & Plumbing (954813) ----
attach_license("rooter-247", {
    "number": "954813", "status": "active",
    "entity": "24 / 7 ROOTER AND PLUMBING SERVICES INC · dba A & R PLUMBING",
    "expires": "2026-11-30", "classes": ["C36", "D56", "A"], "source": 102,
})
add_claim("rooter-247", "License",
          "Current and active · C36, D56, A",
          102, "This license is current and active.")
set_phone("rooter-247", "(415) 586-6851", 102)
add_flag("rooter-247", "notice",
         "License #954813 expires 11/30/2026 — about twelve weeks after this research "
         "snapshot. Renewals typically post near expiry; re-read the CSLB record before booking.",
         [102])

# ---- AB Plumbing (876212) ----
attach_license("ab", {
    "number": "876212", "status": "active",
    "entity": "A B PLUMBING",
    "expires": "2028-04-30", "classes": ["C36"], "source": 103,
})
add_claim("ab", "License",
          "Current and active · C36",
          103, "This license is current and active.")
set_phone("ab", "(415) 333-5566", 103)
add_flag("ab", "notice",
         "Direct CSLB read places A B Plumbing (#876212) at 12909 Skyline Blvd, OAKLAND "
         "94619, while its marketing and the older SF review corpus emphasize San "
         "Francisco. Confirm the current physical base and Outer Sunset dispatch before "
         "relying on the historic review sample.",
         [103, 127])
add_flag("ab", "notice",
         "CSLB shows the contractor's bond with a cancellation date of 10/03/2026 "
         "(Jet Insurance #JT034371) and a workers'-comp exemption ('no employees'); "
         "verify bond continuity and who actually performs the work.",
         [103])

# ---- Heise's Plumbing: company-published tub-drain check-ins ----
add_claim("heises", "Task-adjacent evidence",
          "The company's drain page publishes dated 2026 check-ins describing shower and "
          "tub drains cleared by cabling and tub-stopper repositioning at San Francisco "
          "residences.",
          106, "Heises Plumbing cleared blockages from shower and tub drains at a San "
               "Francisco residence by cabling the lines.")
assert "R59" not in reviews
data["reviews"].append({
    "id": "R59", "business": "heises", "platform": "Business site",
    "author": "Heise's Plumbing (self-reported check-in)",
    "published": "Page carries Feb–Mar 2026 check-in dates",
    "quote": "Heises Plumbing in San Francisco, CA cleared a residential bathtub drain "
             "using a hand crank. They tested the drain by filling and emptying the tub "
             "to confirm proper flow.",
    "analysis": "Business-reported check-in (not a customer account) of a San Francisco "
                "bathtub-drain service with flow verification — adjacent to the target "
                "task but not a seized trip-lever extraction behind a wall.",
    "theme": "Tub-adjacent service", "source": 106, "access": "search-extract",
    "identity": "company-published", "negative": False,
    "checkedAt": RESEARCHED, "exactTask": False,
})
biz["heises"]["reviewIds"].append("R59")
reviews.add("R59")

# ---- 5 Star Plumbing & Rooter: repipe claim (registry caveat already flagged) ----
add_claim("five-star", "Repipe capability",
          "Company repiping page markets galvanized-steel replacement and partial "
          "repipes, naming the Sunset among the older San Francisco neighborhoods it serves.",
          131, "replacing aging galvanized steel, corroded copper, or deteriorated pipe "
               "systems… older neighborhoods like the Mission, Noe Valley, Richmond, Sunset")

# ---- Chosen Rooter & Plumbing: repipe claim ----
add_claim("chosen", "Repipe capability",
          "Company house-repiping page offers PEX replacement of outdated copper or "
          "galvanized steel pipes — the last-resort path if the overflow drain line itself fails.",
          132, "Replacement of outdated copper or galvanized steel pipes with PEX")

# ---- final invariants (mirror merge_wave.py) ----
assert data["master"] == []
assert not any(b["master"] for b in data["businesses"])
assert not any(b.get("exactMatch") for b in data["businesses"])
ids = [r["id"] for r in data["reviews"]]
assert len(ids) == len(set(ids))
for r in data["reviews"]:
    assert sources.get(r["source"])
    assert len(r["quote"]) < 500 and len(r["analysis"]) > 30, r["id"]
    assert r["exactTask"] is False
for b in data["businesses"]:
    for rid in b["reviewIds"]:
        r = next(x for x in data["reviews"] if x["id"] == rid)
        assert r["business"] == b["id"]

TARGET.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
active = sum(1 for b in data["businesses"]
             if b.get("license") and b["license"].get("status") == "active")
print(f"patched research.json: {len(data['businesses'])} businesses, "
      f"{len(data['sources'])} sources, {len(data['reviews'])} reviews, "
      f"{active} active license records")
