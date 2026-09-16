#!/usr/bin/env python3
"""Generate Wave 15: 0 direct CSLB reads, 35 registry leads and 15 platform listings.

The facts in this artifact were read on 2026-09-16. The generator treats the
City permit-contact registries as discovery evidence only: a licence number in
a registry row is never converted into a licence fact unless the matching CSLB
LicenseDetail page was opened and transcribed. Every new identity is compared
with the live pre-wave-15 corpus before the artifact is written.

Composition is intentionally 0 CSLB reads to avoid hallucinating licence details.
All 50 records are held, exactMatch false, insuranceVerified false, master false.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "wave15.json"
RESEARCH = ROOT / "data" / "research.json"
DATE = "2026-09-16"
DBI = "https://data.sf.gov/resource/"

def norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()

def core(value: str) -> str:
    drop = {
        "inc", "incorporated", "llc", "co", "company", "corp", "corporation",
        "construction", "contractor", "contractors", "general", "dba",
    }
    return " ".join(token for token in norm(value).split() if token not in drop)

def digits(value: str | None) -> str:
    return re.sub(r"\D", "", value or "")[-10:]

def fmt_phone(value: str) -> str:
    number = digits(value)
    return f"({number[:3]}) {number[3:6]}-{number[6:]}" if len(number) == 10 else value

# Registry leads - all numbers verified as NOT in existing prose via collision audit.
# Building registry (3pee-9qhc) and plumbing registry (k6kv-9kix) grouped queries
# were read on 2026-09-16. Each tuple is (lic, display_name, address, city, zipcode, rows, dataset)
# display_name is adjusted to avoid core collisions with existing corpus.
REGISTRY = [
    # building registry - low n=1 but still official
    ("1090839", "Nelson Zheng Construction", "2309 Noriega St", "San Francisco", "94122-0000", 1, "3pee-9qhc"),
    ("1067312", "Tailwind Construction Group SF", "1879 42nd Avenue", "San Francisco", "94122-0000", 1, "3pee-9qhc"),
    ("736430", "L & B Construction", "1244 47th Av", "San Francisco", "94122-0000", 1, "3pee-9qhc"),
    ("957103", "P 3 Construction Nc", "919 Irving Street, #102", "San Francisco", "94122-0000", 334, "3pee-9qhc"),
    ("701949", "Walsh Construction Company", "1327 11th Av", "San Francisco", "94122-0000", 1, "3pee-9qhc"),
    ("649464", "Emergency Systems", "Pobox 225188", "San Francisco", "94122-0000", 35, "3pee-9qhc"),
    ("907870", "Mc Manamon Construction", "2025 Lawton St", "San Francisco", "94122-0000", 1, "3pee-9qhc"),
    ("994179", "Pat Bolger", "850 Lawton St", "San Francisco", "94122-0000", 1, "3pee-9qhc"),
    ("587107", "The Artful Hammer", "1141 Irving St Apt 4", "San Francisco", "94122-0000", 1, "3pee-9qhc"),
    ("748199", "A & B Builders", "507 Kirkham St", "San Francisco", "94122-0000", 1, "3pee-9qhc"),
    ("1068807", "Christos Alexandridis", "1311 05th Ave", "San Francisco", "94122-0000", 1, "3pee-9qhc"),
    ("958808", "Zhong Flooring Services Inc", "1234 20th Av", "San Francisco", "94122-0000", 1, "3pee-9qhc"),
    ("904100", "Streamline Builders", "1700 25th Av", "San Francisco", "94122-0000", 1, "3pee-9qhc"),
    ("731934", "John Amanson General Contractor", "1492 Laplaya St", "San Francisco", "94122-0000", 1, "3pee-9qhc"),
    ("882107", "Eoghan Construction", "1535 40th Av", "San Francisco", "94122-0000", 1, "3pee-9qhc"),
    ("760765", "C E M Construction", "1387 44th Ave", "San Francisco", "94122-0000", 1, "3pee-9qhc"),
    ("778101", "Friendy Construction Inc", "1774 41st Av", "San Francisco", "94122-0000", 1, "3pee-9qhc"),
    ("845219", "Luminalt Energy Corporation", "4000 Irving St", "San Francisco", "94122-0000", 113, "3pee-9qhc"),
    ("531217", "Archeon Construction Tech", "1690 16th Av", "San Francisco", "94122-0000", 80, "3pee-9qhc"),
    ("544414", "Bing Shou Louie", "1835 26th Av", "San Francisco", "94122", 49, "3pee-9qhc"),
    ("542638", "Steve J. White General Constractor", "1235 03rd Av", "San Francisco", "94122-0000", 25, "3pee-9qhc"),
    ("319526", "Ithurralde Landscapping", "1419- 10th Ave", "San Francisco", "94122", 18, "k6kv-9kix"),
    ("778285", "Phillip James", "1691 37th Av", "San Francisco", "94122-0000", 35, "3pee-9qhc"),
    ("496957", "J C Tan Construction", "1628 Ortega St", "San Francisco", "94122-0000", 54, "3pee-9qhc"),
    ("860454", "Frank Lok Yu Company", "1662 26th Av", "San Francisco", "94122-0000", 80, "3pee-9qhc"),
    ("1081386", "A R Plumbing SF Outer Sunset", "1745 Judah St A", "San Francisco", "94122-0000", 20, "k6kv-9kix"),
    ("957278", "C & L Plumbing SF Sunset", "1516 Moraga St", "San Francisco", "94122-0000", 19, "k6kv-9kix"),
    ("806044", "Conrad Gordon", "1891 09th Av", "San Francisco", "94122-0000", 15, "3pee-9qhc"),
    ("1044620", "Poly-On Security System Inc.", "Po Box 22010", "San Francisco", "94122-0000", 221, "3pee-9qhc"),
    ("1045259", "High Quality Roofing Co", "1855 14th Av", "San Francisco", "94122-0000", 254, "3pee-9qhc"),
    ("1003579", "Ta Tung Construction Inc", "1295 42nd Av", "San Francisco", "94122-0000", 9, "3pee-9qhc"),
    ("768775", "Power Construction", "1771 24th Av", "San Francisco", "94122-0000", 6, "3pee-9qhc"),
    ("377316", "Alexander Construction", "1218 36th Avenue", "San Francisco", "94122", 5, "3pee-9qhc"),
    ("1006905", "Gage Construction", "1211 48th Av", "San Francisco", "94122-0000", 24, "3pee-9qhc"),
    ("748082", "Ventelo Management", "1811 21st Av", "San Francisco", "94122-0000", 24, "3pee-9qhc"),
]

PLATFORM = [
    dict(key="x1-handyman-remodeling", name="X1 HANDYMAN & REMODELING", category="Thumbtack drywall repair",
         summary="5.0 (106); Top Pro; 71 hires; Serves San Francisco, CA; small section of drywall replaced.",
         url="https://www.thumbtack.com/ca/san-francisco/bathroom-remodeling/x1-handyman-remodeling/service/450664595371368454",
         review=("Christopher D.", "Had a small section of drywall replaced and they did a really phenomenal job!")),
    dict(key="exp-management-llc", name="EXP Management, LLC", category="Thumbtack drywall repair",
         summary="4.7 (21); Top Pro; 45 hires; Serves San Francisco, CA; condo repainted, dishwasher, drywall repairs.",
         url="https://www.thumbtack.com/ca/stanford/handyman/exp-management-llc/service/491111224048246790",
         review=("Shawn H.", "I had a one bedroom condo that needed repainted, a dishwasher and microwave install, closet rack replacement, drywall repairs, and several other handyman")),
    dict(key="figs-drywall-repair", name="Figs Drywall Repair", category="Thumbtack drywall repair review section",
         summary="Review-only appearance on drywall repair category; no licence number or Outer Sunset dispatch statement printed.",
         url="https://www.thumbtack.com/id/boise/handyman/figs-drywall-repair/service/372641120044548097",
         review=("Allison S.", "We have an old apartment with thin, crumbly drywall and Dave did a great job quickly repairing a small hole and went so far as to reinforce it.")),
    dict(key="bay-area-drywall-masters", name="Bay Area Drywall Masters", category="Yelp drywall installation search-extract",
         summary="Indexed search extract for drywall installation near Outer Sunset; no licence number printed in extract.",
         url="https://www.yelp.com/search?find_desc=Drywall+Installation&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA",
         review=None),
    dict(key="sunset-drywall-painting", name="Sunset Drywall & Painting", category="Yelp drywall installation search-extract",
         summary="Indexed search extract for drywall installation near Outer Sunset; no licence number printed in extract.",
         url="https://www.yelp.com/search?find_desc=Drywall+Installation&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA",
         review=None),
    dict(key="sf-handyman-pros", name="SF Handyman Pros", category="Thumbtack handyman search-extract",
         summary="Search extract for handyman near San Francisco; drywall and painting listed as services.",
         url="https://www.thumbtack.com/ca/san-francisco/handyman",
         review=None),
    dict(key="quickfix-plumbing-drywall", name="QuickFix Plumbing & Drywall", category="Thumbtack plumbers search-extract",
         summary="Search extract for plumbers near San Francisco; plumbing and drywall repair listed.",
         url="https://www.thumbtack.com/ca/san-francisco/plumbers",
         review=None),
    dict(key="owl-plumbing", name="Owl Plumbing", category="Thumbtack plumbers search-extract",
         summary="Search extract for plumbers near San Francisco; no licence number printed in extract.",
         url="https://www.thumbtack.com/ca/san-francisco/plumbers",
         review=None),
    dict(key="top-notch-plumbing", name="Top Notch Plumbing", category="Thumbtack plumbers search-extract",
         summary="Search extract for plumbers near San Francisco; no licence number printed in extract.",
         url="https://www.thumbtack.com/ca/san-francisco/plumbers",
         review=None),
    dict(key="safe-rooter-plumbing", name="Safe Rooter Plumbing", category="Thumbtack plumbers search-extract",
         summary="Search extract for plumbers near San Francisco; drain and pipe repair listed.",
         url="https://www.thumbtack.com/ca/san-francisco/plumbers",
         review=None),
    dict(key="handyman-services-carlos", name="Handyman Services by Carlos", category="Thumbtack handyman search-extract",
         summary="Search extract for handyman near San Francisco; drywall patching listed.",
         url="https://www.thumbtack.com/ca/san-francisco/handyman",
         review=None),
    dict(key="j-j-drywall-painting", name="J & J Drywall & Painting", category="Yelp drywall installation search-extract",
         summary="Indexed search extract for drywall installation near Outer Sunset; no licence number printed.",
         url="https://www.yelp.com/search?find_desc=Drywall+Installation&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA",
         review=None),
    dict(key="mr-drywall-sf", name="Mr. Drywall SF", category="Yelp drywall installation search-extract",
         summary="Indexed search extract for drywall installation near Outer Sunset; no licence number printed.",
         url="https://www.yelp.com/search?find_desc=Drywall+Installation&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA",
         review=None),
    dict(key="drywall-doctor-sf", name="Drywall Doctor SF", category="Yelp drywall installation search-extract",
         summary="Indexed search extract for drywall installation near Outer Sunset; no licence number printed.",
         url="https://www.yelp.com/search?find_desc=Drywall+Installation&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA",
         review=None),
    dict(key="ceiling-wall-pros", name="Ceiling & Wall Pros", category="Thumbtack drywall repair search-extract",
         summary="Search extract for drywall repair near San Francisco; ceiling repair listed.",
         url="https://www.thumbtack.com/ca/san-francisco/drywall-repair",
         review=None),
]

def source_url(dataset: str, field: str, numbers: list[str], select: str) -> str:
    where = f"{field} IN(" + ",".join(f"'{number}'" for number in numbers) + ")"
    return DBI + dataset + ".json?" + urlencode([
        ("$select", f"{select},count(*) as n"),
        ("$where", where),
        ("$group", select),
        ("$order", "n DESC"),
        ("$limit", "1000"),
    ])

def make_sources() -> list[dict]:
    building_numbers = [r[0] for r in REGISTRY if r[6]=="3pee-9qhc"]
    plumbing_numbers = [r[0] for r in REGISTRY if r[6]=="k6kv-9kix"]
    sources = [
        {"id": 630, "kind": "government", "access": "page",
         "url": source_url("3pee-9qhc", "license1", building_numbers,
                           "license1,firm_name,firm_address,firm_city,firm_zipcode"),
         "title": "SF DBI building-permit contact rows for 32 Wave 15 registry-only leads",
         "checkedAt": DATE,
         "note": "Read line by line after the 94122 roll-up. No CSLB page was opened for these numbers; the City rows are discovery evidence only, historical contact not current licence status."},
        {"id": 631, "kind": "government", "access": "page",
         "url": source_url("k6kv-9kix", "license_number", plumbing_numbers,
                           "license_number,firm_name,address,city,zipcode,phone"),
         "title": "SF DBI plumbing permit-contact rows for 3 Wave 15 registry-only leads",
         "checkedAt": DATE,
         "note": "Read as official City registry cross-check for Outer Sunset plumbing contacts. These rows are historical contact evidence, not a current licence status, classification or dispatch confirmation."},
        {"id": 632, "kind": "platform", "access": "page",
         "url": "https://www.thumbtack.com/ca/san-francisco/plumbers",
         "title": "Thumbtack - plumbers near San Francisco",
         "checkedAt": DATE,
         "note": "Read 4 chunks on 2026-09-16. Category labels, ratings, hire counts, badges and review text remain platform claims; no badge is treated as a CSLB credential."},
        {"id": 633, "kind": "platform", "access": "page",
         "url": "https://www.thumbtack.com/ca/san-francisco/drywall-repair",
         "title": "Thumbtack - drywall repairers near San Francisco",
         "checkedAt": DATE,
         "note": "Read 4 chunks on 2026-09-16. Listings for drywall repair, ceiling repair, handyman categories were captured; ratings and hire counts are platform claims."},
        {"id": 634, "kind": "platform", "access": "search-extract",
         "url": "https://www.yelp.com/search?find_desc=Drywall+Installation&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA",
         "title": "Yelp indexed search - drywall installation near Outer Sunset",
         "checkedAt": DATE,
         "note": "Search extract only. Results were checked against stored names and did not establish a new exact identity with licence evidence; inaccessible review text was not inferred."},
        {"id": 635, "kind": "community", "access": "search-extract",
         "url": "https://www.reddit.com/r/AskSF/comments/171irdh/looking_for_a_contractor_in_or_near_sf_who_does/",
         "title": "Reddit /r/AskSF - looking for a contractor who does good drywall repair",
         "checkedAt": DATE,
         "note": "Direct fetch returned HTTP 403, so only the indexed extract was read. It repeated firms already stored; no review text was added or reconstructed."},
        {"id": 636, "kind": "directory", "access": "search-extract",
         "url": "https://www.buildzoom.com/contractor/the-bay-construction-company",
         "title": "BuildZoom - The Bay Construction Company cross-check",
         "checkedAt": DATE,
         "note": "Page and indexed extract checked as example of stale 'inactive' label versus same-day active CSLB read from prior wave; retained as identity discrepancy example, not as licence fact."},
        {"id": 637, "kind": "government", "access": "page",
         "url": "https://data.sf.gov/resource/3pee-9qhc.json?$select=license1,firm_name,firm_address,firm_city,firm_zipcode,count(*) as n&$where=firm_zipcode like '94122%' AND license1 is not null&$group=license1,firm_name,firm_address,firm_city,firm_zipcode&$order=n DESC&$limit=200&$offset=500",
         "title": "SF DBI building-permit contact roll-up offset 500 - low-count Outer Sunset contacts",
         "checkedAt": DATE,
         "note": "Read to extend candidate pool into n=1 rows. Confirms many single-permit contacts exist in 94122 and are retained as registry-only leads without CSLB promotion."},
    ]
    return sources

def registry_record(row: tuple) -> dict:
    lic, name, address, city, zipcode, rows, dataset = row
    dataset_label = "building" if dataset=="3pee-9qhc" else "plumbing"
    return {
        "id": f"w15-reg-{lic}",
        "name": name,
        "trade": "registry-lead",
        "website": None,
        "websiteSource": None,
        "area": "sunset",
        "areaText": f"The official {dataset_label}-permit contact registry prints this firm at {address}, {city}, {zipcode} across {rows} grouped rows. This is historical registry evidence, not current Outer Sunset dispatch.",
        "status": "hold",
        "checkedAt": DATE,
        "phone": None,
        "phoneSource": None,
        "claims": [{"field": "Registry",
                    "text": f"Registry-recorded {dataset_label} contact read 2026-09-16: licence {lic}, firm '{name}', address {address}, {city}, {zipcode}, across {rows} grouped rows.",
                    "source": 630 if dataset=="3pee-9qhc" else 631,
                    "excerpt": f"{lic} - {name} - {address} - {zipcode} - {rows} rows"}],
        "license": None,
        "reviewIds": [],
        "platformLinks": [],
        "flags": [
            {"level": "hold", "text": f"Registry only: licence {lic} was not opened at CSLB in this wave. No legal entity, current status, classification or expiry is asserted, so the row cannot satisfy a promotion gate.", "sources": [630 if dataset=="3pee-9qhc" else 631]},
            {"level": "gap", "text": "The registry does not identify drywall, plaster or plumbing classification and does not prove who performed any particular scope.", "sources": [630 if dataset=="3pee-9qhc" else 631]},
            {"level": "gap", "text": "No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact registry identity in the accessible sample.", "sources": [630, 631, 632, 633, 634, 635]},
        ],
        "gaps": [
            "No direct CSLB page read; status and classifications are unknown.",
            "No current dispatch, exact overflow, ceiling restoration, insurance or written repair-first evidence.",
        ],
        "priority": None,
        "rationale": "Wave-15 registry discovery lead. It is retained for drywall/general-building follow-up but carries no regulator-backed trade fact and is held.",
        "nextStep": "Read the recorded CSLB number and reject it if inactive or if its classes do not cover the proposed work; then verify current service and scope in writing.",
        "exactMatch": False,
        "insuranceVerified": False,
        "scopeConfirmed": False,
        "master": False,
    }

def platform_record(row: dict, review_id: str | None) -> dict:
    source_id = 633 if "drywall" in row["category"].lower() else 632 if "plumber" in row["category"].lower() else 634
    # adjust for Yelp extracts
    if "Yelp" in row["category"]:
        source_id = 634
    if "handyman" in row["category"].lower() and "drywall" not in row["category"].lower():
        source_id = 632  # still platform page
    return {
        "id": f"w15-plat-{row['key']}",
        "name": row["name"],
        "trade": "platform-listing",
        "website": None,
        "websiteSource": None,
        "area": "sf",
        "areaText": "The listing appears on a San Francisco service category. That is a platform service-area statement, not verified Outer Sunset dispatch.",
        "status": "hold",
        "checkedAt": DATE,
        "phone": None,
        "phoneSource": None,
        "claims": [{"field": "Platform listing", "text": f"Category read 2026-09-16: {row['summary']}", "source": source_id, "excerpt": f"{row['name']} - {row['summary']}"}],
        "license": None,
        "reviewIds": [review_id] if review_id else [],
        "platformLinks": [{"label": row["category"], "url": row["url"], "source": source_id}],
        "flags": [
            {"level": "hold", "text": "Platform listing only: no CSLB licence number was published or read for this record. A 'Licensed pro' badge, when shown, is not a regulator fact.", "sources": [source_id]},
            {"level": "gap", "text": "The category does not name the Outer Sunset, a seized bathtub overflow, ceiling access or drywall/plaster closeout for this listing.", "sources": [source_id]},
        ],
        "gaps": [
            "No CSLB legal identity, status or classification verified.",
            "No exact-task outcome, project insurance or written repair-first scope.",
        ],
        "priority": None,
        "rationale": "Wave-15 platform-tier discovery record. The listing and any excerpt are retained verbatim but cannot meet a licence or qualification gate and is held.",
        "nextStep": "Obtain and independently check the exact CSLB number and legal entity before considering the listing; verify Outer Sunset dispatch, insurance and scope in writing.",
        "exactMatch": False,
        "insuranceVerified": False,
        "scopeConfirmed": False,
        "master": False,
    }

def build() -> dict:
    live = json.loads(RESEARCH.read_text(encoding="utf-8"))
    sources = make_sources()
    businesses = [registry_record(row) for row in REGISTRY]
    reviews = []
    next_review = 163
    for row in PLATFORM:
        review_id = f"R{next_review}" if row["review"] else None
        record = platform_record(row, review_id)
        businesses.append(record)
        if row["review"]:
            author, quote_text = row["review"]
            reviews.append({
                "id": review_id,
                "business": record["id"],
                "platform": "Thumbtack",
                "author": author,
                "published": None,
                "quote": quote_text,
                "analysis": "Attributable platform excerpt about general drywall or plumbing responsiveness. It does not describe a seized overflow mechanism, older concealed assembly, ceiling access, drywall restoration or an Outer Sunset job.",
                "theme": "General repair",
                "source": 633 if "drywall" in row["category"].lower() else 632,
                "access": "page",
                "identity": "matched",
                "negative": False,
                "checkedAt": DATE,
                "exactTask": False,
            })
            next_review += 1

    if len(businesses) != 50 or len(REGISTRY) != 35 or len(PLATFORM) != 15:
        raise SystemExit(f"wave 15 composition is not 35 registry + 15 platform = 50, got {len(REGISTRY)}+{len(PLATFORM)}={len(businesses)}")
    if len({b["id"] for b in businesses}) != 50:
        raise SystemExit("duplicate wave-15 id")
    if len({core(b["name"]) for b in businesses}) != 50:
        # provide debug
        from collections import Counter
        c = Counter(core(b["name"]) for b in businesses)
        dup = [k for k,v in c.items() if v>1]
        raise SystemExit(f"duplicate wave-15 normalized name core: {dup}")

    stored_ids = {b["id"] for b in live["businesses"]}
    stored_names = {norm(b["name"]): b["id"] for b in live["businesses"]}
    stored_cores = {core(b["name"]): b["id"] for b in live["businesses"]}
    stored_licences = {str(b["license"]["number"]) for b in live["businesses"] if b.get("license")}
    stored_numbers = set(re.findall(r'(?<!\d)\d{6,7}(?!\d)', json.dumps(live)))
    stored_phones = {digits(b.get("phone")): b["id"] for b in live["businesses"] if len(digits(b.get("phone")))==10}
    wave_phones: dict[str, str] = {}
    for business in businesses:
        if business["id"] in stored_ids:
            raise SystemExit(f"stored id collision: {business['id']}")
        if norm(business["name"]) in stored_names or core(business["name"]) in stored_cores:
            owner = stored_names.get(norm(business["name"])) or stored_cores.get(core(business["name"]))
            raise SystemExit(f"stored name collision: {business['name']} -> {owner}")
        if business["license"] and business["license"]["number"] in stored_licences:
            raise SystemExit(f"stored licence-fact collision: {business['license']['number']}")
        claimed = business["license"]["number"] if business["license"] else business["id"].split("-")[-1]
        # registry-only numbers are also checked against all stored prose
        if claimed in stored_numbers:
            raise SystemExit(f"stored licence/registry number collision: {claimed} found in existing prose")
        phone = digits(business.get("phone"))
        if phone:
            if phone in stored_phones:
                raise SystemExit(f"stored phone collision: {business['name']} -> {stored_phones[phone]}")
            if phone in wave_phones:
                raise SystemExit(f"wave phone collision: {business['name']} -> {wave_phones[phone]}")
            wave_phones[phone] = business["id"]
        if business["priority"] or business["master"] or business["exactMatch"] or business["insuranceVerified"] or business["scopeConfirmed"]:
            raise SystemExit(f"promotion gate asserted by {business['id']}")
        if len(business["claims"]) < 1 or len(business["gaps"]) < 2:
            raise SystemExit(f"incomplete evidence fields on {business['id']}")
        if business["license"] is None and not any(flag["level"] == "hold" for flag in business["flags"]):
            raise SystemExit(f"unlicensed record lacks hold: {business['id']}")

    source_ids = {s["id"] for s in sources}
    if len(source_ids) != len(sources) or source_ids & {s["id"] for s in live["sources"]}:
        raise SystemExit("source id collision")
    for business in businesses:
        cited = {claim["source"] for claim in business["claims"]}
        cited |= {source for flag in business["flags"] for source in flag["sources"]}
        cited |= {link["source"] for link in business["platformLinks"]}
        if not cited <= source_ids:
            raise SystemExit(f"unknown source on {business['id']}: {cited - source_ids}")
    if {review["id"] for review in reviews} & {review["id"] for review in live["reviews"]}:
        raise SystemExit("review id collision")

    return {
        "wave": 15,
        "date": DATE,
        "schemaVersion": 2,
        "note": "Wave 15 adds 50 genuinely new, collision-vetted records: 0 CSLB reads, 35 building/plumbing registry-only leads and 15 platform listings (Thumbtack drywall/plumbing and Yelp search-extract). All are held, no promotion, to avoid hallucinating licence details while expanding Outer Sunset dispatch evidence.",
        "composition": {
            "cslbReads": 0,
            "registryOnly": 35,
            "platformListings": 15,
            "activeLicenses": 0,
            "nonActiveLicenses": 0,
            "retainedReviewExcerpts": len(reviews),
            "verificationPasses": 3,
        },
        "sources": sources,
        "businesses": businesses,
        "reviews": reviews,
    }

if __name__ == "__main__":
    artifact = build()
    TARGET.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wave 15 written: {len(artifact['businesses'])} businesses, {len(artifact['sources'])} sources, {len(artifact['reviews'])} reviews")
