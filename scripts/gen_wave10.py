#!/usr/bin/env python3
"""Build the wave-10 artifact (data/wave10.json) from directly-read sources.

Wave 10 is the tenth discovery pass. It adds 50 nonduplicate businesses in three
published evidence tiers and performs ten verification upgrades against records
that earlier waves had stored without a regulator read.

Evidence tiers, stated per record rather than smoothed over:

* **regulator-read (23)** — a CSLB ``LicenseDetail.aspx`` page was opened and
  transcribed field by field: legal entity, business form, address, phone, issue
  and expiry dates, status text, every displayed classification, the contractor's
  bond line, the workers'-compensation line and any Additional Status or
  Miscellaneous Information entries.
* **registry-lead (21)** — a City open-data permit registry records a firm name,
  address, phone and licence *number*. The licence number is deliberately NOT
  promoted into a licence fact, so these records carry ``license: null`` and the
  trade value ``registry-lead``, which no classification set can satisfy.
* **platform-listing (6)** — a Thumbtack category page was read directly. A
  platform rating, hire count or "Licensed pro" badge is a platform claim; it is
  never stored as a licence.

Discovery ran registry-first: the City's own plumbing and building permit contact
registries were grouped by licence number so every firm name, address and phone a
licence appears under in ZIP 94122 is visible. Candidates already present in
waves 1-9 were removed before selection.

Ten licence reads here resolve to records that earlier waves had already stored
*without* a regulator read. Those are published as verification upgrades rather
than as new entries, so the corpus gains evidence without gaining duplicates.

Run:
    python3 scripts/gen_wave10.py
    python3 scripts/merge_wave10.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "wave10.json"
DATE = "2026-09-12"

# --------------------------------------------------------------------------
# Sources 353-397. Every URL below was opened or returned by a search tool on
# the check date; nothing is reconstructed from memory.
# --------------------------------------------------------------------------
CSLB = "https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum="

CSLB_READ_ORDER = [
    "619642", "486122", "410861", "487017", "440780", "762214", "536715",
    "586693", "324708", "486546", "343610", "1054611", "319594", "635360",
    "856173", "604689", "863410", "489739", "797580", "546425", "834292",
    "869710", "443478", "595176", "782830", "950725", "917101", "803442",
    "652992", "943574", "982738", "917252", "804459",
]
# licence number -> source id, assigned in read order starting at 353
LIC_SRC = {num: 353 + i for i, num in enumerate(CSLB_READ_ORDER)}

CSLB_LEGAL_NAME = {
    "619642": "NATIONAL PLUMBING",
    "486122": "PLUMBWORKS INC",
    "410861": "STAN PLUMBING",
    "487017": "SBERLO PLUMBING INC",
    "440780": "BILL BRAGG PLUMBING",
    "762214": "ORAN PLUMBING CORP",
    "536715": "SUNNY'S PLUMBING INC",
    "586693": "LEE PLUMBING CO",
    "324708": "HAWK N LEE DESIGN & CONSTRUCTION COMPANY",
    "486546": "WINSON WAH LAU",
    "343610": "DAVID CHU PLUMBING",
    "1054611": "CHOSEN ROOTER & PLUMBING INC",
    "319594": "FRANKS ALL CITY PLUMBING CO",
    "635360": "REN LEI CONSTRUCTION CO INC",
    "856173": "H Y CONSTRUCTION INC",
    "604689": "M F CONSTRUCTION",
    "863410": "J & A STONE AND TILE INC",
    "489739": "TILE ARTS INC",
    "797580": "TERENCE MCMAHON CONSTRUCTION",
    "546425": "CONNOR DALY CORPORATION",
    "834292": "BRENDAN WATERS CONSTRUCTION INC",
    "869710": "URBAN BUILDER GENERAL CONTRACTING INC",
    "443478": "A & W CONTRACTORS",
    "595176": "SNC PLUMBING & FIRE PROTECTION INC",
    "782830": "BENJAMIN FRANKLIN PLUMBING",
    "950725": "SAN FRANCISCO DESIGN BUILD",
    "917101": "VECTOR CONSTRUCTION INC",
    "803442": "A W CONSTRUCTION COMPANY",
    "652992": "MR ROOTER PLUMBING",
    "943574": "JONES BROS CONSTRUCTION INC",
    "982738": "C & L PLUMBING INC",
    "917252": "SEDERAP'S DRYWALL INC",
    "804459": "HAMMERHOUSE CONSTRUCTION INC",
}

S_REG_PLUMB = 386
S_REG_BUILD = 387
S_PERMIT_PLUMB = 388
S_PERMIT_BUILD = 389
S_TT_DRYWALL = 390
S_TT_PLUMB = 391
S_REDDIT_ASK = 392
S_REDDIT_PLUM = 393
S_REDDIT_HI_STUCK = 394
S_REDDIT_HI_CANT = 395
S_PLBC = 396
S_REDDIT_DIY = 397
S_BUILDZOOM = 398
S_YELP_NEAR = 399
S_PROCORE = 400

SOURCES = [
    {
        "id": S_REG_PLUMB,
        "title": "SF DBI · Plumbing Permits Contacts · every licence with a 94122 firm address",
        "url": "https://data.sf.gov/resource/k6kv-9kix.json?%24select=license_number%2Cmax%28firm_name%29+as+firm%2Cmax%28address%29+as+addr%2Cmax%28phone%29+as+phone%2Ccount%28permit_number%29+as+permits&%24where=zipcode+like+%2794122%25%27+AND+license_number+is+not+null&%24group=license_number&%24order=permits+DESC&%24limit=300",
        "kind": "government",
        "access": "page",
        "note": "Official City & County of San Francisco open-data API (dataset k6kv-9kix, “Plumbing Permits Contacts”, provenance: official), queried directly and grouped by licence number so every firm name, address and phone a licence appears under in ZIP 94122 is visible. Registry rows are historical permit contacts: they establish a recorded address and a licence linkage, not current status, classification or availability. Phone values are reproduced exactly as the registry prints them, including malformed area codes.",
    },
    {
        "id": S_REG_BUILD,
        "title": "SF DBI · Building Permits Contacts · every licence1 with a 94122 firm ZIP",
        "url": "https://data.sf.gov/resource/3pee-9qhc.json?%24select=license1%2Cmax%28firm_name%29+as+firm%2Cmax%28firm_address%29+as+addr%2Cmax%28firm_zipcode%29+as+zip%2Ccount%28permit_number%29+as+permits&%24where=firm_zipcode+like+%2794122%25%27+AND+license1+is+not+null&%24group=license1&%24order=permits+DESC&%24limit=80",
        "kind": "government",
        "access": "page",
        "note": "Official City & County of San Francisco building-permit contact registry (dataset 3pee-9qhc, provenance: official), grouped by the licence1 column. Used for the drywall, ceiling and general-building side of the search, where the plumbing registry supplies no candidates. A contact row records who appears on a permit; it does not allocate the work described on a permit to a specific contact.",
    },
    {
        "id": S_PERMIT_PLUMB,
        "title": "SF DBI · completed 94122 plumbing permits in the current window",
        "url": "https://data.sf.gov/resource/a6aw-rudh.json?%24select=permit_number%2Cstatus%2Ccompleted_date%2Cdescription%2Cstreet_number%2Cstreet_name%2Cstreet_suffix%2Czipcode&%24where=zipcode%3D%2794122%27+AND+status%3D%27complete%27+AND+completed_date+%3E%3D+%272025-06-01T00%3A00%3A00.000%27&%24order=completed_date+DESC&%24limit=200",
        "kind": "government",
        "access": "page",
        "note": "Official plumbing-permit detail rows, newest completions first, so wave 10 works from current rather than archival plumbing activity in the Outer Sunset. A completed permit establishes a work location, a completion date and the words actually printed in the scope.",
    },
    {
        "id": S_PERMIT_BUILD,
        "title": "SF DBI · completed 94122 building permits naming drywall, sheetrock, ceiling or plaster work",
        "url": "https://data.sf.gov/resource/i98e-djp9.json?%24select=permit_number%2Cstatus%2Ccompleted_date%2Cdescription%2Cstreet_number%2Cstreet_name%2Cstreet_suffix%2Czipcode&%24where=zipcode%3D%2794122%27+AND+status%3D%27complete%27+AND+%28lower%28description%29+like+%27%25drywall%25%27+OR+lower%28description%29+like+%27%25sheetrock%25%27+OR+lower%28description%29+like+%27%25gyp%25%27+OR+lower%28description%29+like+%27%25ceiling%25%27+OR+lower%28description%29+like+%27%25plaster%25%27+OR+lower%28description%29+like+%27%25stucco%25%27%29&%24order=completed_date+DESC&%24limit=200",
        "kind": "government",
        "access": "page",
        "note": "Official building-permit detail rows filtered to finish work, so the drywall and ceiling side of the search is checked against the same City source rather than a directory. Descriptions support only the work words actually printed.",
    },
    {
        "id": S_TT_DRYWALL,
        "title": "Thumbtack · drywall repairers near San Francisco, CA (category page read directly)",
        "url": "https://www.thumbtack.com/ca/san-francisco/drywall-repair",
        "kind": "platform",
        "access": "page",
        "note": "The San Francisco drywall-repair category page was read directly. Ratings, review counts, hire counts and the “Licensed pro” badge are platform claims about a listing; none of them is a CSLB read. Review cards shown on a category page are attributed to the listing the page itself names, and their text is reproduced as published, including run-together words. A pro whose profile path points at another city keeps that path in the record.",
    },
    {
        "id": S_TT_PLUMB,
        "title": "Thumbtack · plumbers near San Francisco, CA (category page read directly)",
        "url": "https://www.thumbtack.com/ca/san-francisco/plumbers",
        "kind": "platform",
        "access": "page",
        "note": "The San Francisco plumber category page was read directly. Service-scope lines are quoted as printed for each listing. Two listings shown on this page are water-heater or repipe specialists, which is plumbing work but not the same task as freeing a seized overflow trip lever; that difference is recorded rather than blurred.",
    },
    {
        "id": S_REDDIT_ASK,
        "title": "r/askaplumber · “Trip Lever Bathtub old and broken”",
        "url": "https://www.reddit.com/r/askaplumber/comments/17curdh/trip_lever_bathtub_old_and_broken/",
        "kind": "community",
        "access": "search-extract",
        "note": "Community thread about a seized trip-lever linkage. Reached as a search-result extract on the check date, not as a direct page read. The thread names no business, so it can support the task description but never a contractor's experience claim.",
    },
    {
        "id": S_REDDIT_PLUM,
        "title": "r/Plumbing · “Stuck trip lever, old bathtub. Wouldn’t turn up or down, can’t pull out.”",
        "url": "https://www.reddit.com/r/Plumbing/comments/170tvds/stuck_trip_lever_old_bathtub_wouldnt_turn_up_or/",
        "kind": "community",
        "access": "search-extract",
        "note": "Thread in which a renter reports that penetrating oil, a steam pot and plunging all failed, and later reports that the waste and overflow had to be replaced through the drywall. Search-result extract; no business named.",
    },
    {
        "id": S_REDDIT_HI_STUCK,
        "title": "r/HomeImprovement · “Stuck plunger mechanism in bathtub drain”",
        "url": "https://www.reddit.com/r/HomeImprovement/comments/9l5s32/stuck_plunger_mechanism_in_bathtub_drain_pic/",
        "kind": "community",
        "access": "search-extract",
        "note": "Thread where a plumber on site confirms the obstruction is the mechanism itself and says access would require cutting through the wall. Search-result extract; no business named.",
    },
    {
        "id": S_REDDIT_HI_CANT,
        "title": "r/HomeImprovement · “Can’t remove trip-lever drain stopper in bathtub”",
        "url": "https://www.reddit.com/r/HomeImprovement/comments/esb5xg/cant_remove_triplever_drain_stopper_in_bathtub/",
        "kind": "community",
        "access": "search-extract",
        "note": "Thread describing a mechanism that is “all corrosion welded”, with a reply noting that freeing it is what penetrating oil is for and that over-application is a concern. Search-result extract; no business named.",
    },
    {
        "id": S_PLBC,
        "title": "plbg.com plumbing forum · “bathtub trip lever stopper stuck in overflow pipe”",
        "url": "https://www.plbg.com/forum/read.php?1,537511",
        "kind": "community",
        "access": "search-extract",
        "note": "Trade forum thread in which every poured product runs straight past a hollow brass stopper, and the advice converges on disassembling the overflow tube. Search-result extract; no business named.",
    },
    {
        "id": S_REDDIT_DIY,
        "title": "r/DIY · “Bath tub drain lever completely stuck”",
        "url": "https://www.reddit.com/r/DIY/comments/1bj07go/bath_tub_drain_lever_completely_stuck/",
        "kind": "community",
        "access": "search-extract",
        "note": "Thread recommending descaling before penetrating oil, and warning that oil and its smell are undesirable in a bathtub. Search-result extract; no business named.",
    },
    {
        "id": S_BUILDZOOM,
        "title": "BuildZoom · Sunny’s Plumbing Inc profile (no reviews on file)",
        "url": "https://www.buildzoom.com/contractor/sunnys-plumbing-inc",
        "kind": "directory",
        "access": "search-extract",
        "note": "Directory profile returned by search. It states “BuildZoom hasn't received any reviews for Sunny's Plumbing Inc” and lists both licence 536715 and a second licence, 524327. Absence of reviews is stored as a gap, never as a neutral or positive signal; the second licence number is recorded only as a directory-stated lead.",
    },
    {
        "id": S_YELP_NEAR,
        "title": "Yelp · “Best Things to Do near Sunny’s Plumbing in San Francisco, CA”",
        "url": "https://www.yelp.com/search?find_desc=Things+to+Do&find_near=sunnys-plumbing-san-francisco",
        "kind": "platform",
        "access": "search-extract",
        "note": "Quarantined as a source. The page’s JSON-LD carries an aggregateRating of 4.5 from 2603 reviews, but its own title shows it is a category page for attractions near the address, not the plumber’s own rating, and the business is not rated by it. The figure is therefore recorded as a rejected third-party derivation and is never rendered as a rating for the business.",
    },
    {
        "id": S_PROCORE,
        "title": "Procore Network · National Plumbing (San Francisco) company page",
        "url": "https://network.procore.com/p/national-plumbing-san-francisco",
        "kind": "directory",
        "access": "search-extract",
        "note": "Construction-network company page returned by search. It repeats the 1472 24th Ave address but prints a telephone number that differs from the one CSLB publishes for licence 619642; both readings are kept and the conflict is flagged rather than reconciled.",
    },
]

for _num, _sid in LIC_SRC.items():
    SOURCES.append(
        {
            "id": _sid,
            "title": f"CSLB · Contractor’s License Detail for licence {_num}",
            "url": f"{CSLB}{_num}",
            "kind": "government",
            "access": "page",
            "note": f"California Contractors State License Board licence-detail page for licence {_num}, opened directly and transcribed field by field on {DATE}. CSLB reports “Data current as of 9/12/2026” on the page. A licence status never establishes exact-task experience, current dispatch, or that the licensee will accept a particular job.",
        }
    )

for _s in SOURCES:
    _s.setdefault("checkedAt", DATE)

SOURCES.sort(key=lambda s: s["id"])

# --------------------------------------------------------------------------
# Wave-10 records. Tier A — a CSLB licence-detail page was read directly.
# --------------------------------------------------------------------------
TIER_A = [
    {
        "key": "plumbworks-inc-dba-chris-goodwin-plumbing",
        "name": "Plumbworks Inc dba Chris Goodwin Plumbing",
        "lic": "486122",
        "phone": "415-681-1309",
        "trade": "plumbing",
        "region": "outside",
        "entity": "Corporation",
        "issued": "01/28/1986",
        "reissued": "08/21/2003",
        "expires": "2021-06-29",
        "status": "canceled",
        "classes": ["C16", "C36"],
        "address": "494 Silver Ave Unit A, Half Moon Bay, CA 94019",
        "status_text": "This license is canceled and not able to contract.",
        "bond": "Contractor's Bond with SURETEC INSURANCE COMPANY, bond number 230408, amount $15,000, effective 07/01/2020, cancellation date 09/09/2022.",
        "wc": "Workers' compensation: exempt, certified no employees, effective 09/14/2020.",
        "misc": "Miscellaneous Information: 08/21/2003 LICENSE REISSUED TO ANOTHER ENTITY; 06/29/2021 LICENSE CANCELED PER REQUEST.",
        "registry": "The City plumbing-permit contact registry records licence 486122 as “Plumbworks Inc. /Chris Goodwin Plumbing” at 1663 48th Ave, ZIP 94122, across 944 permit rows, with the phone printed as 6811306 — a value with no area code.",
        "registry_flags": [
            ("discrepancy", "The registry prints the phone as “6811306” with no area code, while CSLB publishes (415) 681-1309. The registry value is stored as printed and not completed by assumption."),
            ("discrepancy", "The registry places this licence at 1663 48th Ave, ZIP 94122 — an Outer Sunset street — while CSLB places the licensee in Half Moon Bay, CA 94019. The 94122 value is a recorded permit-contact address, not a current business address."),
            ("notice", "944 recorded permit rows at a 94122 address is the second-largest single-firm count found in this pass, and it belongs to a licence that was canceled per request in 2021. Historic volume and current availability are different facts."),
        ],
        "area_text": "CSLB places the licensee at 494 Silver Ave Unit A, Half Moon Bay, CA 94019. The City plumbing registry separately records this licence at 1663 48th Ave, ZIP 94122 across 944 permit rows. Neither reading is a current Outer Sunset dispatch promise, and the licence is canceled.",
    },
    {
        "key": "lee-plumbing-co",
        "name": "Lee Plumbing Co",
        "lic": "586693",
        "phone": "415-681-9323",
        "trade": "plumbing",
        "region": "sf",
        "entity": "Sole Ownership",
        "issued": "01/24/1990",
        "reissued": "04/08/2025",
        "expires": "2027-04-30",
        "status": "active",
        "classes": ["C36"],
        "address": "2407 21st Avenue, San Francisco, CA 94116",
        "status_text": "This license is current and active.",
        "bond": "Contractor's Bond with WESTERN SURETY COMPANY, bond number 67399197, amount $25,000, effective 02/26/2025.",
        "wc": "Workers' compensation: exempt, certified no employees, effective 02/12/2025.",
        "misc": "Miscellaneous Information: 04/08/2025 LICENSE REISSUED TO A FAMILY MEMBER.",
        "registry": "The City plumbing-permit contact registry records licence 586693 as “C W Lee Plumbing Company” at 1650 34th Avenue, ZIP 94122, across 221 permit rows, with the phone printed as 415-689-9323.",
        "registry_flags": [
            ("discrepancy", "The registry name (“C W Lee Plumbing Company”, at 1650 34th Avenue) does not match the CSLB licensee name (“LEE PLUMBING CO”, at 2407 21st Avenue, 94116). Name and city both differ. The registry string is quoted as-read and the licence number, not the name, is what links the two readings."),
            ("discrepancy", "The registry prints 415-689-9323; CSLB publishes (415) 681-9323. Two digits are transposed. The CSLB value is stored; the registry value is flagged."),
            ("notice", "A separate, unrelated licence number 342141 is stored in earlier waves under the similar name “Lee’s Plumbing Co” (LEE’S PLUMBING CO, 94118, expired 1997). The two records share a surname pattern only; nothing here merges them."),
        ],
        "area_text": "CSLB places the licensee at 2407 21st Avenue, San Francisco 94116. The City plumbing registry separately records licence 586693 on 221 permit rows at 1650 34th Avenue, ZIP 94122, so there is recorded work in the Outer Sunset ZIP without a CSLB Outer Sunset address.",
    },
    {
        "key": "h-y-construction-inc",
        "name": "H Y Construction Inc",
        "lic": "856173",
        "phone": "415-812-5188",
        "trade": "general",
        "region": "outer",
        "entity": "Corporation",
        "issued": "03/23/2005",
        "expires": "2027-03-31",
        "status": "active",
        "classes": ["B"],
        "address": "1774 8th Avenue, San Francisco, CA 94122",
        "status_text": "This license is current and active.",
        "bond": "Contractor's Bond with WESTERN SURETY COMPANY, bond number 67629083, amount $25,000, effective 01/10/2026.",
        "wc": "Workers' compensation with STATE COMPENSATION INSURANCE FUND, policy 9048772, effective 03/11/2013, expires 03/11/2027; classification codes 5183, 5190 Electrical Wiring-low wage, 5482 — descriptions not displayed by the board.",
        "misc": "No Miscellaneous Information section is displayed for this licence.",
        "registry": "Both City registries record licence 856173 as “H Y Construction Inc.” at 1774 8th Av, ZIP 94122, with 98 plumbing permit-contact rows and 93 building permit rows, and the phone printed as 415-812-5188.",
        "registry_flags": [
            ("notice", "The registry phone 415-812-5188 matches the CSLB number exactly, and the street address matches on both readings. This is the cleanest identity agreement in the wave-10 set."),
            ("notice", "The licence holds B only; the registry rows are plumbing and building permit contacts, which a general contractor can appear on without performing plumbing."),
        ],
        "area_text": "CSLB places this licensee at 1774 8th Avenue, San Francisco 94122 — an Outer Sunset ZIP — with an active B classification and matching registry address and phone.",
    },
    {
        "key": "m-f-construction",
        "name": "M F Construction",
        "lic": "604689",
        "phone": "415-225-5709",
        "trade": "general",
        "region": "outer",
        "entity": "Sole Ownership",
        "issued": "10/15/1990",
        "expires": "2028-01-31",
        "status": "active",
        "classes": ["B"],
        "address": "1459 32nd Ave, San Francisco, CA 94122",
        "status_text": "This license is current and active.",
        "bond": "Contractor's Bond with JET INSURANCE COMPANY, bond number JT022550, amount $25,000, effective 09/30/2025.",
        "wc": "Workers' compensation: exempt, certified no employees, effective 12/08/2025.",
        "misc": "No Miscellaneous Information section is displayed for this licence.",
        "registry": "The City plumbing registry records licence 604689 as “M F Construction” at 1459 32nd Av, ZIP 94122 on 83 permit rows; the City building registry records the same licence at the same address on 179 permit rows. The phone prints as 415-225-5709 on both.",
        "registry_flags": [
            ("notice", "Address and phone agree across the regulator and both registries; the licence holds B only, so plumbing permit rows do not establish plumbing classification."),
            ("notice", "The licence is a sole ownership with a workers'-compensation exemption in force since 12/08/2025, which means no employees are certified. Capacity to staff a two-trade opening is unproven by this record."),
        ],
        "area_text": "CSLB places this licensee at 1459 32nd Ave, San Francisco 94122 — an Outer Sunset ZIP — with an active B classification and matching registry address and phone.",
    },
    {
        "key": "terence-mcmahon-construction",
        "name": "Terence McMahon Construction",
        "lic": "797580",
        "phone": "415-385-3304",
        "trade": "general",
        "region": "outer",
        "entity": "Corporation",
        "issued": "07/19/2001",
        "reissued": "07/29/2011",
        "expires": "2027-07-31",
        "status": "active",
        "classes": ["B"],
        "address": "1400 Irving Street, San Francisco, CA 94122",
        "status_text": "This license is current and active.",
        "bond": "Contractor's Bond with AMERICAN CONTRACTORS INDEMNITY COMPANY, bond number 100670309, amount $25,000, effective 01/01/2023.",
        "wc": "Workers' compensation with STATE COMPENSATION INSURANCE FUND, policy 9405736, effective 07/17/2026, expires 07/17/2027; classification codes 5432 Carpentry-high wage, 5403 Carpentry-low wage.",
        "misc": "Miscellaneous Information: 07/29/2011 LICENSE REISSUED TO ANOTHER ENTITY. Other: personnel listed on this license are listed on other licenses.",
        "registry": "The City building registry records licence 797580 as “Terence Mcmahon Construction” at 1400 Irving St, ZIP 94122, with 577 building permit rows — the second-highest count in the wave-10 building pull.",
        "registry_flags": [
            ("notice", "577 building permit rows at a 94122 firm address is the strongest volume evidence found on the finish side of this pass. Volume is not finish-quality evidence and is not treated as such."),
            ("notice", "The qualifying individual changed effective 05/23/2025 (ANDREW GEORGE BYRNE certified 10%+ ownership). A qualifying-individual change is a control change worth confirming at contact."),
        ],
        "area_text": "CSLB places this licensee at 1400 Irving Street, San Francisco 94122 — an Outer Sunset ZIP — with an active B classification, and the City building registry records 577 permit rows at the same address.",
    },
    {
        "key": "connor-daly-corporation",
        "name": "Connor Daly Corporation",
        "lic": "546425",
        "phone": "415-294-1804",
        "trade": "general",
        "region": "sf",
        "entity": "Corporation",
        "issued": "11/07/1988",
        "reissued": "11/20/2017",
        "expires": "2027-11-30",
        "status": "active",
        "classes": ["B"],
        "address": "289 Bungalow Ave, San Rafael, CA 94901",
        "status_text": "This license is current and active.",
        "bond": "Contractor's Bond with MERCHANTS BONDING COMPANY (MUTUAL), bond number 101698186, amount $25,000, effective 11/20/2025.",
        "wc": "Workers' compensation with BERKSHIRE HATHAWAY DIRECT INSURANCE COMPANY, policy N9WC025766, effective 10/09/2025, expires 10/09/2026; classification codes 540300 and 543200 — descriptions not displayed by the board.",
        "misc": "Miscellaneous Information: 05/11/2017 CONNOR DALY SON; 05/11/2017 AUTH TO CONTINUE UNTIL 11/27/2017; 09/08/2017 LICENSE REISSUED TO A FAMILY MEMBER; 11/20/2017 LICENSE REISSUED TO ANOTHER ENTITY.",
        "registry": "The City building registry records licence 546425 as “Connor Daly Corporation” at 1727 20th Av, ZIP 94122, across 215 building permit rows.",
        "registry_flags": [
            ("discrepancy", "The registry places this licence at 1727 20th Av, ZIP 94122; CSLB places the licensee at 289 Bungalow Ave, San Rafael 94901. The 94122 value is a recorded permit-contact address."),
            ("notice", "Four Miscellaneous Information entries between 05/11/2017 and 11/20/2017 record a son entry, an authorisation to continue, a reissue to a family member and then a reissue to another entity on the same licence number. The number alone does not identify one continuous operator over that period."),
        ],
        "area_text": "CSLB places the licensee at 289 Bungalow Ave, San Rafael 94901. The City building registry records this licence on 215 permit rows at 1727 20th Av, ZIP 94122, so 94122 work is recorded without a CSLB Outer Sunset address.",
    },
    {
        "key": "brendan-waters-construction-inc",
        "name": "Brendan Waters Construction Inc",
        "lic": "834292",
        "phone": "415-876-0658",
        "trade": "general",
        "region": "outer",
        "entity": "Corporation",
        "issued": "03/18/2004",
        "reissued": "11/15/2013",
        "expires": "2027-11-30",
        "status": "active",
        "classes": ["B"],
        "address": "1382 7th Avenue, San Francisco, CA 94122",
        "status_text": "This license is current and active.",
        "bond": "Contractor's Bond with AMERICAN CONTRACTORS INDEMNITY COMPANY, bond number 100234887, amount $25,000, effective 01/01/2023.",
        "wc": "Workers' compensation with NORGUARD INSURANCE COMPANY, policy BRWC722799, effective 02/12/2026, expires 02/12/2027; classification code 5432 Carpentry-high wage.",
        "misc": "Miscellaneous Information: 11/15/2013 LICENSE REISSUED TO ANOTHER ENTITY.",
        "registry": "The City building registry records licence 834292 as “Brendan Waters Construction Inc” at 1382 07th Av, ZIP 94122, across 210 building permit rows.",
        "registry_flags": [
            ("notice", "Regulator and registry agree on the street address and ZIP; the registry writes the street as “07th” and the regulator as “7th”."),
            ("notice", "The licence holds B only with a single carpentry workers'-compensation code. Nothing in this record establishes experience with a finished access hatch or with a plumbing repair behind a ceiling."),
        ],
        "area_text": "CSLB places this licensee at 1382 7th Avenue, San Francisco 94122 — an Outer Sunset ZIP — with an active B classification and a matching registry address.",
    },
    {
        "key": "urban-builder-general-contracting-inc",
        "name": "Urban Builder General Contracting Inc",
        "lic": "869710",
        "phone": "415-269-4916",
        "trade": "general",
        "region": "outer",
        "entity": "Corporation",
        "issued": "12/19/2005",
        "reissued": "11/26/2012",
        "expires": "2026-11-30",
        "status": "active",
        "classes": ["B"],
        "address": "1258 33rd Avenue, San Francisco, CA 94122",
        "status_text": "This license is current and active.",
        "bond": "Contractor's Bond with ATLANTIC SPECIALTY INSURANCE COMPANY, bond number 800211320, amount $25,000, effective 01/22/2026.",
        "wc": "Workers' compensation with EVEREST PREMIER INSURANCE COMPANY, policy 7600023509261, effective 08/03/2026, expires 08/03/2027; classification codes 5403 Carpentry-low wage, 5432 Carpentry-high wage.",
        "misc": "Miscellaneous Information: 11/26/2012 LICENSE REISSUED TO ANOTHER ENTITY.",
        "registry": "The City building registry records licence 869710 as “Urban Builder General Contracting Inc” at 1258 33rd Av, ZIP 94122, across 186 building permit rows.",
        "registry_flags": [
            ("notice", "Regulator and registry agree on the street address and ZIP. The licence expires 11/30/2026, roughly eleven weeks after the check date."),
            ("notice", "The workers'-compensation policy was replaced effective 08/03/2026, five weeks before the check date, so the coverage on file is current as displayed."),
        ],
        "area_text": "CSLB places this licensee at 1258 33rd Avenue, San Francisco 94122 — an Outer Sunset ZIP — with an active B classification and a matching registry address.",
    },
    {
        "key": "a-and-w-contractors",
        "name": "A & W Contractors",
        "lic": "443478",
        "phone": "415-665-3619",
        "trade": "general",
        "region": "outer",
        "entity": "Corporation",
        "issued": "07/22/1983",
        "expires": "2027-07-31",
        "status": "active",
        "classes": ["B"],
        "address": "1549 Noriega Street, San Francisco, CA 94122",
        "status_text": "This license is current and active.",
        "bond": "Contractor's Bond with NORTH RIVER INSURANCE COMPANY (THE), bond number 04CF629407, amount $25,000, effective 08/26/2024, CANCELLATION DATE 09/30/2026.",
        "wc": "Workers' compensation with STATE COMPENSATION INSURANCE FUND, policy 9367967, effective 05/01/2026, expires 05/01/2027; no classification codes are displayed for this licence.",
        "misc": "Other: personnel listed on this license (current or disassociated) are listed on other licenses.",
        "registry": "The City building registry records licence 443478 as “A & W Contractors” at 1549 Noriega St, ZIP 94122, across 219 building permit rows.",
        "registry_flags": [
            ("hold", "CSLB displays a CANCELLATION DATE of 09/30/2026 on the contractor’s bond while the licence still reads “current and active”. Under the board’s own published suspension mechanics a bond cancellation puts a licence into suspension, so this licence is likely to change status within weeks of the check date. Held pending a re-read rather than booked."),
            ("notice", "Address and ZIP agree between the regulator and the registry."),
        ],
        "area_text": "CSLB places this licensee at 1549 Noriega Street, San Francisco 94122 — an Outer Sunset ZIP — with an active B classification, but the contractor’s bond carries a cancellation date of 09/30/2026.",
    },
    {
        "key": "san-francisco-design-build",
        "name": "San Francisco Design Build",
        "lic": "950725",
        "phone": "415-349-0579",
        "trade": "general",
        "region": "outer",
        "entity": "Sole Ownership",
        "issued": "08/03/2010",
        "expires": "2028-08-31",
        "status": "active",
        "classes": ["B"],
        "address": "1560 Great Highway, Apt 1, San Francisco, CA 94122",
        "status_text": "This license is current and active.",
        "bond": "Contractor's Bond with BUSINESS ALLIANCE INSURANCE COMPANY, bond number G100724397934, amount $25,000, effective 01/01/2023.",
        "wc": "Workers' compensation with STATE COMPENSATION INSURANCE FUND, policy 9095613, effective 04/10/2014, expires 04/10/2027; classification code 5403 Carpentry-low wage.",
        "misc": "No Miscellaneous Information section is displayed for this licence.",
        "registry": "The City building registry records licence 950725 as “San Francisco Design Build” at 1560 Great Hy, ZIP 94122, across 129 building permit rows.",
        "registry_flags": [
            ("notice", "The 94122 address is a Great Highway residential unit, not a commercial shopfront. Regulator and registry agree on it."),
            ("notice", "The licence holds B only. Nothing read here establishes plumbing classification or a finished-access-hatch precedent."),
        ],
        "area_text": "CSLB places this licensee at 1560 Great Highway, Apt 1, San Francisco 94122 — an Outer Sunset ZIP — with an active B classification and a matching registry address.",
    },
    {
        "key": "vector-construction-inc",
        "name": "Vector Construction Inc",
        "lic": "917101",
        "phone": "415-812-6741",
        "trade": "general",
        "region": "outer",
        "entity": "Corporation",
        "issued": "06/06/2008",
        "expires": "2028-06-30",
        "status": "inactive",
        "classes": ["B", "C10"],
        "address": "3618 Ortega St, San Francisco, CA 94122",
        "status_text": "This license is inactive and not able to contract at this time.",
        "additional": "The license will need a contractors bond to renew active or reactivate. The license will need to meet the workers compensation requirements to renew active or reactivate.",
        "bond": "Contractor's Bond with AMERICAN CONTRACTORS INDEMNITY COMPANY, bond number 100047440, amount $25,000, effective 01/01/2023, cancellation date 07/01/2026.",
        "wc": "Workers' compensation: exempt, certified no employees, effective 06/25/2026, cancellation date 08/07/2026.",
        "misc": "Miscellaneous Information: 08/17/2026 WC EXEMPT CANCELLED-LIC INACTIVATED.",
        "registry": "The City building registry records licence 917101 as “Vector Construction Inc.” at 3618 Ortega St, ZIP 94122, across 125 building permit rows.",
        "registry_flags": [
            ("hold", "The licence was inactivated on 08/17/2026, twenty-six days before the check date, because the workers'-compensation exemption was cancelled on 08/07/2026. The registry still lists 125 building permit rows at this address, and a register-only check would have shown an address and a licence number with no hint that the licence cannot currently contract."),
        ],
        "area_text": "CSLB places this licensee at 3618 Ortega St, San Francisco 94122 — an Outer Sunset ZIP — but the licence is inactive and CSLB states it is not able to contract at this time.",
    },
    {
        "key": "a-w-construction-company",
        "name": "A W Construction Company",
        "lic": "803442",
        "phone": "415-613-9056",
        "trade": "general",
        "region": "outer",
        "entity": "Sole Ownership",
        "issued": "01/22/2002",
        "expires": "2028-01-31",
        "status": "suspended",
        "classes": ["B"],
        "address": "1201-32nd Avenue, San Francisco, CA 94122",
        "status_text": "License is under suspension for the following reasons: License is under suspension for failure to comply with Workers Comp.",
        "bond": "Contractor's Bond with PHILADELPHIA INDEMNITY INSURANCE COMPANY, bond number PB10163404994, amount $25,000, effective 01/01/2026.",
        "wc": "Workers' compensation with STATE COMPENSATION INSURANCE FUND, policy 9371673, effective 12/10/2024, cancellation date 02/18/2026; classification codes 5432 Carpentry-high wage, 5403 Carpentry-low wage.",
        "misc": "Miscellaneous Information: 11/06/2015 CASH DEPOSIT LTR SENT $15,000; 01/14/2016 CASH DEPOSIT 15K FOLLOW UP LTR SENT.",
        "registry": "The City building registry records licence 803442 as “A W Construction Company” at 1201 32nd Ave Av, ZIP 94122, across 160 building permit rows.",
        "registry_flags": [
            ("hold", "CSLB states the licence is suspended for failure to comply with workers'-compensation requirements, with the carrier cancellation dated 02/18/2026 — roughly seven months before the check date. The registry shows 160 building permit rows at a 94122 address and no indication of the suspension."),
            ("notice", "Two Miscellaneous Information entries from 2015 and 2016 record cash-deposit letters at the $15,000 level. They are reproduced as the board prints them and no conclusion is drawn from them."),
        ],
        "area_text": "CSLB places this licensee at 1201-32nd Avenue, San Francisco 94122 — an Outer Sunset ZIP — but the licence is under suspension for failure to comply with workers'-compensation requirements.",
    },
    {
        "key": "snc-plumbing-and-fire-protection-inc",
        "name": "SNC Plumbing & Fire Protection Inc",
        "lic": "595176",
        "phone": "415-282-0688",
        "trade": "plumbing",
        "region": "sf",
        "entity": "Corporation",
        "issued": "05/30/1990",
        "expires": "2012-04-19",
        "status": "canceled",
        "classes": ["C16", "C36"],
        "address": "1595 Fairfax Avenue Ste A, San Francisco, CA 94124",
        "status_text": "This license is canceled and not able to contract.",
        "bond": "Contractor's Bond with OLD REPUBLIC SURETY COMPANY, bond number GCL1154848, amount $12,500, effective 10/29/2007, cancellation date 12/04/2009.",
        "wc": "Workers' compensation with STATE COMPENSATION INSURANCE FUND, policy 571-0004312, effective 07/01/2008, cancellation date 07/01/2012.",
        "misc": "Miscellaneous Information: 04/19/2012 LICENSE CANCELED PER REQUEST.",
        "registry": "The City plumbing-permit contact registry records licence 595176 as “Snc Plumbing & Fire Pro” at “1730 - 44th Avenue”, ZIP 94122, across 159 permit rows, with the phone printed as 5501129.",
        "registry_flags": [
            ("discrepancy", "The registry prints the phone as 5501129 with no area code and truncates the firm name; CSLB publishes (415) 282-0688 for “SNC PLUMBING & FIRE PROTECTION INC”."),
            ("notice", "The registry address “1730 - 44th Avenue” is an Outer Sunset street while the licensee is at 94124, and the licence has been canceled since 2012. Historical 94122 work in a registry row is not current availability."),
        ],
        "area_text": "CSLB places the licensee at 1595 Fairfax Avenue Ste A, San Francisco 94124, with a licence canceled since 04/19/2012. The City plumbing registry records 159 permit rows at a 94122 street address.",
    },
    {
        "key": "benjamin-franklin-plumbing",
        "name": "Benjamin Franklin Plumbing",
        "lic": "782830",
        "phone": "415-454-9500",
        "trade": "plumbing",
        "region": "outside",
        "entity": "Partnership",
        "issued": "08/11/2000",
        "expires": "2006-08-31",
        "status": "expired",
        "classes": ["A", "C36"],
        "address": "517 Jacoby Street Suite C, San Rafael, CA 94901",
        "status_text": "This license is expired and not able to contract at this time.",
        "bond": "Contractor's Bond with AMERICAN CONTRACTORS INDEMNITY COMPANY, bond number 111942, amount $10,000, effective 01/01/2004, cancellation date 06/15/2006.",
        "wc": "Workers' compensation with TRUCK INSURANCE EXCHANGE, policy B19135970, effective 04/15/2006, expires 04/15/2007.",
        "misc": "Other: personnel listed on this license (current or disassociated) are listed on other licenses.",
        "registry": "The City plumbing-permit contact registry records licence 782830 as “Benjamin Franklin Plumbing” at 2255 Judah St, ZIP 94122, across 80 permit rows, with the phone printed as 415-564-0526.",
        "registry_flags": [
            ("discrepancy", "The registry places this licence at 2255 Judah St, ZIP 94122 with phone 415-564-0526; CSLB places the licensee at 517 Jacoby Street Suite C, San Rafael 94901 with (415) 454-9500. Address and phone both differ."),
            ("discrepancy", "The registry phone 415-564-0526 is one digit from the Judah Street shop number already stored against an unrelated licence in earlier waves. A near-match on a phone is recorded as a conflict, never as an identity match."),
            ("notice", "The licence number on a national brand name is not the brand. This 2006-expired partnership in San Rafael is a different legal entity from any current franchise of the same name, and nothing here is attributed to a franchise."),
        ],
        "area_text": "CSLB places the licensee at 517 Jacoby Street Suite C, San Rafael 94901 with a licence expired since 08/31/2006. The City plumbing registry records 80 permit rows at 2255 Judah St, ZIP 94122 under the same number.",
    },
    {
        "key": "hawk-n-lee-design-and-construction-company",
        "name": "Hawk N Lee Design & Construction Company",
        "lic": "324708",
        "phone": "415-823-1685",
        "trade": "multi-trade",
        "region": "outer",
        "entity": "Sole Ownership",
        "issued": "09/03/1976",
        "expires": "2026-12-31",
        "status": "active",
        "classes": ["A", "B", "C10", "C36"],
        "address": "1032 Irving Street #930, San Francisco, CA 94122",
        "status_text": "This license is current and active.",
        "bond": "Contractor's Bond with WESTERN SURETY COMPANY, bond number 67668182, amount $25,000, effective 01/01/2026.",
        "wc": "Workers' compensation: exempt, certified no employees, effective 11/13/2024.",
        "misc": "Other: personnel listed on this license (current or disassociated) are listed on other licenses.",
        "registry": "The City plumbing-permit contact registry records licence 324708 as “Hawk N Lee Co” at 1609 Noriega Street, ZIP 94122, across 198 permit rows, with the phone printed as 415-681-6328. The City building-permit registry records the same street address under the identifier CE28526, “Hwak N.Lee,P.E”.",
        "registry_flags": [
            ("discrepancy", "The registry prints the firm as “Hawk N Lee Co” at 1609 Noriega Street with phone 415-681-6328; CSLB prints “HAWK N LEE DESIGN & CONSTRUCTION COMPANY” at 1032 Irving Street #930 with (415) 823-1685. Name, street address and phone all differ."),
            ("notice", "The building registry’s “Hwak N.Lee,P.E” entry carries identifier CE28526, which is a professional-engineer registration format and not a contractor licence number. It is recorded as a separate credential type and is not treated as evidence about licence 324708."),
            ("notice", "Holding A, B, C10 and C36 on one licence is the broadest classification set found in this pass, and the licence expires 12/31/2026 — inside four months of the check date. A renewal re-read is required before any reliance."),
        ],
        "area_text": "CSLB itself places this licensee at 1032 Irving Street #930, San Francisco 94122 — an Outer Sunset ZIP — with A, B, C10 and C36 classifications and an active licence expiring 12/31/2026. The registry adds a second 94122 street address that CSLB does not print.",
    },
    {
        "key": "w-and-j-plumbing-co",
        "name": "Winson Wah Lau dba W & J Plumbing Co",
        "lic": "486546",
        "phone": "415-509-3732",
        "trade": "multi-trade",
        "region": "outer",
        "entity": "Sole Ownership",
        "issued": "02/04/1986",
        "expires": "2016-02-29",
        "status": "expired",
        "classes": ["B", "C36"],
        "address": "1346 26th Avenue, San Francisco, CA 94122",
        "status_text": "This license is expired and not able to contract at this time.",
        "bond": "Contractor's Bond with AMERICAN CONTRACTORS INDEMNITY COMPANY, bond number SC925562, amount $15,000, effective 01/01/2016, cancellation date 03/02/2016.",
        "wc": "Workers' compensation: exempt, certified no employees, effective 02/25/2016.",
        "misc": "No Miscellaneous Information section is displayed for this licence.",
        "registry": "The City plumbing-permit contact registry records licence 486546 as “W & J Plumbing Co.” at 1346 26th Avenue, ZIP 94122, across 181 permit rows, with the phone printed as 415-751-1801.",
        "registry_flags": [
            ("discrepancy", "The registry prints 415-751-1801; CSLB publishes (415) 509-3732. The CSLB value is stored; the registry value is flagged."),
            ("notice", "The address matches on both readings, and the licence has been expired since 02/29/2016 — more than ten years. The registry rows are historical."),
        ],
        "area_text": "CSLB places this licensee at 1346 26th Avenue, San Francisco 94122 — an Outer Sunset ZIP — with B and C36 classifications, but the licence expired 02/29/2016 and CSLB states it is not able to contract.",
    },
    {
        "key": "oran-plumbing-corp",
        "name": "Oran Plumbing Corp",
        "lic": "762214",
        "phone": "415-307-8198",
        "trade": "plumbing",
        "region": "sf",
        "entity": "Corporation",
        "issued": "04/27/1999",
        "reissued": "05/07/2014",
        "expires": "2028-05-31",
        "status": "active",
        "classes": ["C36"],
        "address": "95 El Plazuela St, San Francisco, CA 94127",
        "status_text": "This license is current and active.",
        "bond": "Contractor's Bond with AMERICAN CONTRACTORS INDEMNITY COMPANY, bond number 100242985, amount $25,000, effective 01/01/2023.",
        "wc": "Workers' compensation with STATE COMPENSATION INSURANCE FUND, policy 9093731, effective 03/27/2022, expires 03/27/2027; classification code 51871 Plumbing-high wage.",
        "misc": "Miscellaneous Information: 05/07/2014 LICENSE REISSUED TO ANOTHER ENTITY.",
        "registry": "The City plumbing-permit contact registry records licence 762214 as “Oran Plmbing Corp” at 2437 Ortega St, ZIP 94122, across 362 permit rows, with the phone printed as 415-806-5586.",
        "phone_collision": "w6-francis-john-burke",
        "registry_flags": [
            ("discrepancy", "The registry misspells the firm as “Oran Plmbing Corp”, places it at 2437 Ortega St, ZIP 94122 and prints 415-806-5586; CSLB prints “ORAN PLUMBING CORP” at 95 El Plazuela St, 94127, phone (415) 307-8198. Name, address and phone all differ."),
            ("notice", "362 permit rows is the largest count among the wave-10 registry rows that still resolves to an active C-36 licence, which makes the identity conflict worth resolving before contact rather than after."),
            ("discrepancy", "The CSLB phone for this licence, (415) 307-8198, is the same number the City plumbing registry already stores against a different record read in an earlier wave — the record held as “Francis John Burke” (w6-francis-john-burke), which sits at 2437 Ortega St, ZIP 94122. The regulator resolves the overlap rather than leaving it open: the CSLB page for licence 762214 names FRANCIS JOHN BURKE as the qualifying individual who owns 10 percent or more of the corporation. Two registry names, one address, one phone and one qualifying individual is recorded as an identity linkage between two records — as a linkage, never as a merge and never as a rating transfer."),
        ],
        "area_text": "CSLB places the licensee at 95 El Plazuela St, San Francisco 94127. The City plumbing registry records this active C-36 licence on 362 permit rows at 2437 Ortega St, ZIP 94122, with a different printed phone.",
    },
    {
        "key": "j-and-a-stone-and-tile-inc",
        "name": "J & A Stone and Tile Inc",
        "lic": "863410",
        "phone": "505-699-1298",
        "trade": "masonry",
        "region": "outside",
        "entity": "Corporation",
        "issued": "08/25/2005",
        "expires": "2027-08-31",
        "status": "active",
        "classes": ["C29"],
        "address": "3425 Gravenstein Highway South, Sebastopol, CA 95472",
        "status_text": "This license is current and active.",
        "bond": "Contractor's Bond with ATLANTIC SPECIALTY INSURANCE COMPANY, bond number 800049083, amount $25,000, effective 08/09/2025.",
        "wc": "Workers' compensation with STATE COMPENSATION INSURANCE FUND, policy 9389480, effective 10/24/2025, expires 10/24/2026; classification codes 874210, 534804, 881002 — descriptions not displayed by the board.",
        "misc": "No Miscellaneous Information section is displayed for this licence.",
        "registry": "The City plumbing-permit contact registry records licence 863410 as “J & A Stone And Tile Inc” at 1711 38th Ave, ZIP 94122, across 88 permit rows, with the phone printed as 5454735533.",
        "registry_flags": [
            ("hold", "The licence holds C29 Masonry only — no plumbing and no building classification — yet the City registry records it as a contact on 88 plumbing-permit rows at a 94122 address. Whatever the explanation, a masonry-only licence cannot self-perform plumbing or drywall, so this record is scope-excluded from both requirements."),
            ("discrepancy", "The registry phone 5454735533 has a North American area-code shape that is not a valid California area code, and CSLB publishes a 505 New Mexico number for the licensee. Both readings are stored as printed."),
        ],
        "area_text": "CSLB places the licensee at 3425 Gravenstein Highway South, Sebastopol 95472 with a C29 Masonry classification only. The City plumbing registry records 88 permit rows under this licence at 1711 38th Ave, ZIP 94122.",
        "excluded": True,
    },
    {
        "key": "tile-arts-inc",
        "name": "Tile Arts Inc",
        "lic": "489739",
        "phone": "415-305-7787",
        "trade": "tile",
        "region": "outside",
        "entity": "Corporation",
        "issued": "04/12/1986",
        "reissued": "05/26/2000",
        "expires": "2028-05-31",
        "status": "active",
        "classes": ["C54"],
        "address": "63 Tamalpais, Fairfax, CA 94930",
        "status_text": "This license is current and active.",
        "bond": "Contractor's Bond with ATLANTIC SPECIALTY INSURANCE COMPANY, bond number 800213380, amount $25,000, effective 10/12/2025.",
        "wc": "Workers' compensation with SECURITY NATIONAL INSURANCE COMPANY, policy SNS1648470, effective 06/06/2026, expires 06/06/2027; classification code 5348 Tile/Stone/Mosaic/Terrazzo Work.",
        "misc": "Miscellaneous Information: 05/26/2000 LICENSE REISSUED TO ANOTHER ENTITY. Other: personnel listed on this license are listed on other licenses.",
        "registry": "The City plumbing-permit contact registry records licence 489739 as “Tile Arts Inc” at 1374 29th Avenue, ZIP 94122, across 78 permit rows, with the phone printed as 4158767058.",
        "registry_flags": [
            ("hold", "The licence holds C54 Tile (ceramic and mosaic) only. It cannot self-perform plumbing or drywall, so it is scope-excluded from the two requirements even though it is the trade most likely to be needed if a tub surround has to be opened to reach an overflow."),
            ("discrepancy", "The registry places this licence at 1374 29th Avenue, ZIP 94122 with phone 4158767058; CSLB places the licensee at 63 Tamalpais, Fairfax 94930 with (415) 305-7787. Address and phone both differ."),
        ],
        "area_text": "CSLB places the licensee at 63 Tamalpais, Fairfax 94930 with a C54 Tile classification only. The City plumbing registry records 78 permit rows under this licence at 1374 29th Avenue, ZIP 94122.",
        "excluded": True,
    },
    {
        "key": "mr-rooter-plumbing",
        "name": "Mr Rooter Plumbing",
        "lic": "652992",
        "phone": "310-901-0528",
        "trade": "plumbing",
        "region": "outside",
        "entity": "Partnership",
        "issued": "08/26/1992",
        "expires": "2018-08-31",
        "status": "expired",
        "classes": ["C36"],
        "address": "30100 Town Center Dr Ste 0-425, Laguna Niguel, CA 92677",
        "status_text": "This license is expired and not able to contract at this time.",
        "bond": "Contractor's Bond with AMERICAN CONTRACTORS INDEMNITY COMPANY, bond number 122574, amount $15,000, effective 01/01/2016, cancellation date 07/31/2019.",
        "wc": "Workers' compensation: exempt, certified no employees, effective 07/22/2016.",
        "misc": "Other: personnel listed on this license (current or disassociated) are listed on other licenses.",
        "registry": "The City plumbing-permit contact registry records licence 652992 as “Mr. Rooter Pluming” at 2801 Judah St, ZIP 94122, across 72 permit rows, with the phone printed as 415-748-3004.",
        "registry_flags": [
            ("hold", "The registry phone 415-748-3004 is the same number already stored against an unrelated licence number in earlier waves, and the registry address 2801 Judah St is the same address stored with that other licence. Two licence numbers, one address, one phone: this is recorded as a collision, and no review, permit or job is attributed to either number on the strength of it."),
            ("discrepancy", "CSLB places licence 652992 in Laguna Niguel, 92677 — roughly 400 miles from the Outer Sunset — on a licence expired since 08/31/2018, while the registry records 72 permit rows at a 94122 address under it."),
            ("notice", "A third Mr. Rooter legal entity is already stored from an earlier wave under a different licence number. Franchise-style naming across several distinct licence numbers is the reason this project keys on licence number rather than on trade name."),
        ],
        "area_text": "CSLB places the licensee at 30100 Town Center Dr Ste 0-425, Laguna Niguel 92677 on a licence expired since 08/31/2018. The City plumbing registry records 72 permit rows at 2801 Judah St, ZIP 94122 under the same number, with a phone that collides with another stored licence.",
    },
    {
        "key": "jones-bros-construction-inc",
        "name": "Jones Bros Construction Inc",
        "lic": "943574",
        "phone": "415-341-7285",
        "trade": "general",
        "region": "outer",
        "entity": "Corporation",
        "issued": "02/17/2010",
        "expires": "2018-01-30",
        "status": "canceled",
        "classes": ["B"],
        "address": "1879 35th Avenue, San Francisco, CA 94122",
        "status_text": "This license is canceled and not able to contract.",
        "bond": "Contractor's Bond with HUDSON INSURANCE COMPANY, bond number 30009068, amount $15,000, effective 01/01/2016, cancellation date 12/08/2018.",
        "wc": "Workers' compensation with STATE COMPENSATION INSURANCE FUND, policy 9026317, effective 09/28/2012, expires 09/28/2016.",
        "misc": "Miscellaneous Information: 01/30/2018 SECRETARY OF STATE - DISSOLUTION. Other: personnel listed on this license are listed on other licenses.",
        "registry": "The City building registry records licence 943574 as “Jones Bros Construction Inc” at 1879 35th Av, ZIP 94122, across 84 building permit rows.",
        "phone_collision": "w9-jones-bros-construction-design-inc",
        "registry_flags": [
            ("hold", "This licence is canceled and the licensee was dissolved by the Secretary of State on 01/30/2018, yet the City building registry still lists 84 permit rows at a 94122 address under the number."),
            ("discrepancy", "The phone CSLB publishes for this cancelled licence, (415) 341-7285, is identical to the phone already stored against a different licence number in an earlier wave under a near-identical family name — the record held as “Jones Bros Construction & Design Inc” (w9-jones-bros-construction-design-inc). One phone, two licence numbers, two similar names: recorded as a collision and cross-referenced, not merged."),
        ],
        "area_text": "CSLB places this licensee at 1879 35th Avenue, San Francisco 94122 — an Outer Sunset ZIP — but the licence is canceled and the licensee was dissolved in 2018. Its published phone number is shared with a different stored licence.",
    },
    {
        "key": "sederap-s-drywall-inc",
        "name": "Sederap's Drywall Inc",
        "lic": "917252",
        "phone": "415-713-7765",
        "trade": "plumbing-and-drywall",
        "region": "sf",
        "entity": "Corporation",
        "issued": "06/09/2008",
        "expires": "2028-06-30",
        "status": "active",
        "classes": ["B", "C-9", "C10", "C36"],
        "address": "3469 Mission Street, San Francisco, CA 94110",
        "status_text": "This license is current and active.",
        "bond": "Contractor's Bond with BUSINESS ALLIANCE INSURANCE COMPANY, bond number G150206787520, amount $25,000, effective 02/05/2025.",
        "wc": "Workers' compensation: exempt, certified no employees, effective 06/08/2026.",
        "misc": "The qualifying individual, YERIS ALFRANCIS PAREDES ZUNIGA, certified that he or she owns 10 percent or more of the voting stock or membership interest of the company, so a Bond of Qualifying Individual is not required. Other: personnel listed on this license (current or disassociated) are listed on other licenses.",
        "registry": "The City building registry records licence 917252 as “Sederap's Drywall Inc.” with a 94110 firm ZIP across 113 permit rows, the largest drywall-named firm count found in the City contact registries, and the registry also carries a one-row variant string, “Sederaps Electric & Drywall”, under a separate contact line.",
        "registry_flags": [
            ("notice", "This is the only licence read in this wave whose classification set contains both a drywall class (C-9) and a plumbing class (C36) on one active licence, which is the combination this project's two required trades need from a single responsible contractor. C10 electrical and B general building are also on the licence."),
            ("discrepancy", "The registry carries two different strings for this licence — “Sederap's Drywall Inc.” and “Sederaps Electric & Drywall” — and CSLB prints the legal name in capitals with no apostrophe convention. The licence number, not the string, is what links the readings, and both are stored as-printed."),
            ("gap", "No City permit contact row in ZIP 94122 was found under this licence number in this pass, so Outer Sunset is not evidenced for this business. A classification set is a credential fact, never a statement about where the firm currently works."),
        ],
        "area_text": "CSLB places the licensee in San Francisco 94110 and states C-9 drywall, C36 plumbing, C10 electrical and B general building classifications on an active licence expiring 06/30/2028. The City contact registry also records the licence with a 94110 firm ZIP. No 94122 permit contact was found, so this record claims San Francisco coverage and does not claim Outer Sunset dispatch.",
    },
    {
        "key": "hammerhouse-construction-inc",
        "name": "Hammerhouse Construction Inc",
        "lic": "804459",
        "phone": "415-516-7399",
        "trade": "general",
        "region": "outer",
        "entity": "Corporation",
        "issued": "02/21/2002",
        "reissued": "07/11/2005",
        "expires": "2027-07-31",
        "status": "active",
        "classes": ["B"],
        "address": "19 Cerritos Avenue, San Francisco, CA 94127",
        "status_text": "This license is current and active.",
        "bond": "Contractor's Bond with ATLANTIC SPECIALTY INSURANCE COMPANY, bond number 800211800, amount $25,000, effective 11/09/2025.",
        "wc": "Workers' compensation with STATE COMPENSATION INSURANCE FUND, policy 9128603, effective 04/01/2015, expires 04/01/2027; classification codes 54031, 53481 and 51461 (Cabinet/Fixtures Installation). The board states it does not verify or investigate the accuracy of classification codes displayed.",
        "misc": "The qualifying individual, THOMAS WINT BUCCHIONI, certified that he or she owns 10 percent or more of the voting stock or membership interest of the company, so a Bond of Qualifying Individual is not required.",
        "registry": "The City plumbing-permit contact registry records licence 804459 as “Hammerhouse Construction” at 1250 Kirkham St, ZIP 94122, across 38 permit rows, with the phone printed as 4157530744 — the same ten digits CSLB publishes, printed without punctuation.",
        "registry_flags": [
            ("discrepancy", "The City plumbing registry places this licence at 1250 Kirkham St, ZIP 94122; CSLB places the licensee at 19 Cerritos Avenue, San Francisco 94127. The 94122 value is a recorded permit-contact address in the Outer Sunset, not the regulator-confirmed business address."),
            ("gap", "The licence carries the B general building classification only. A B licence may take a whole project and subcontract the trades, but it cannot self-perform plumbing or drywall, so both required trades would have to be subcontracted and named before any work begins."),
            ("notice", "The registry carries this general-building licence on 38 plumbing-permit contact rows, which is itself the pattern worth checking: a builder appearing as a contact on plumbing permits does not make the builder a plumber."),
        ],
        "area_text": "CSLB places the licensee at 19 Cerritos Avenue, San Francisco 94127 with an active B general building classification expiring 07/31/2027, and the City plumbing registry separately records this licence at 1250 Kirkham St, ZIP 94122 across 38 permit rows — an Outer Sunset address recorded by the City. Neither reading is a dispatch promise, and the B classification covers neither required trade directly.",
    },
]

# --------------------------------------------------------------------------
# Tier B — 14 registry-only leads. The licence NUMBER is recorded by the City,
# but no CSLB page was read, so no licence fact may be asserted.
# --------------------------------------------------------------------------
TIER_B = [
    {
        "key": "macro-builder-inc",
        "name": "Macro Builder Inc",
        "lic": "797077",
        "phone": "7863683",
        "trade_note": "plumbing-permit contact rows in the 94122 plumbing registry",
        "roof": "registry-row",
        "registry_rows": "2121 19th Av, ZIP 94122",
        "permits": 158,
        "second": "The City building registry separately records licence 797077 as “Macro Builder Inc” at 1883 19th Ave, ZIP 94122 on 123 permit rows.",
        "flags": [
            ("discrepancy", "The registry prints the phone as “7863683” with no area code, and the two registries give different street numbers for the same licence (2121 19th Av and 1883 19th Ave) in the same ZIP. Both readings are stored as printed."),
        ],
    },
    {
        "key": "tony-tiejun-hu",
        "name": "Tony Tiejun Hu",
        "lic": "792165",
        "phone": "451-517-8123",
        "trade_note": "plumbing-permit contact rows in the 94122 plumbing registry",
        "roof": "registry-row",
        "registry_rows": "1214 40th Av, ZIP 94122",
        "permits": 180,
        "second": "No second-registry row was matched to this licence number.",
        "flags": [
            ("discrepancy", "The registry prints the phone as “451-517-8123”. A 451 area code is not a Californian one and 415 is the surrounding one, so the value looks transposed — but a transposition is a hypothesis, not a reading, and the registry string is stored exactly as printed."),
            ("notice", "The firm name is a personal name with no business suffix, which is consistent with a sole-owner licence rather than a company. Nothing was read from CSLB, so no entity, classification or status is stated for this record."),
        ],
    },
    {
        "key": "danny-chen",
        "name": "Danny Chen",
        "lic": "893929",
        "phone": "4156719698",
        "trade_note": "plumbing-permit contact rows in the 94122 plumbing registry",
        "roof": "registry-row",
        "registry_rows": "1659 23rd Av, ZIP 94122",
        "permits": 141,
        "second": "No second-registry row was matched to this licence number.",
        "phone_collision": "w8-dc-plumbing-llc",
        "flags": [
            ("notice", "141 plumbing permit rows at a 94122 address is substantial recorded activity under this licence number. The registry is the only source read, so this record asserts a recorded contact and nothing more."),
            ("discrepancy", "The registry phone 4156719698 is the same number already stored against a different record for a licence that was read at the regulator — the record held as “DC Plumbing LLC” (w8-dc-plumbing-llc) — and the registry address for this row, 1659 23rd Av, is the same street address as that record. An individual name and a company name sharing one address and one phone is recorded as a probable identity linkage; it is not treated as proof, and no licence fact is borrowed from the other record."),
        ],
    },
    {
        "key": "d-s-management-inc-dba-metrocon-builders",
        "name": "D S Management Inc dba Metrocon Builders",
        "lic": "978867",
        "phone": "4153732989",
        "trade_note": "plumbing-permit contact rows in the 94122 plumbing registry",
        "roof": "registry-row",
        "registry_rows": "2004 Irving St, ZIP 94122",
        "permits": 131,
        "second": "The City building registry records licence 978867 as “Metrocon Builders” at 2004 Irving St, ZIP 94122 on 110 permit rows.",
        "flags": [
            ("discrepancy", "The two registries print different firm names for one licence number: “D S Management Inc Dba Metrocon Builders” in the plumbing registry and “Metrocon Builders” in the building registry. Both strings are stored as-read."),
        ],
    },
    {
        "key": "r-c-construction-co",
        "name": "R C Construction Co",
        "lic": "747801",
        "phone": "415-601-9273",
        "trade_note": "plumbing-permit contact rows in the 94122 plumbing registry",
        "roof": "registry-row",
        "registry_rows": "2037 Irving St #203, ZIP 94122",
        "permits": 108,
        "second": "The City building registry records licence 747801 as “C R Construction Co Inc” at 1687 26th Avenue, ZIP 94122 on 191 permit rows.",
        "flags": [
            ("discrepancy", "One licence number carries two firm names and two addresses across the two City registries: “R C Construction Co” at 2037 Irving St #203 and “C R Construction Co Inc” at 1687 26th Avenue. Because the initials are reversed between the readings, the registry values cannot resolve which string is intended, and neither is chosen."),
        ],
    },
    {
        "key": "w-j-l-construction-inc",
        "name": "W J L Construction Inc",
        "lic": "775086",
        "phone": "415-682-3919",
        "trade_note": "building-permit contact rows with a 94122 firm ZIP",
        "roof": "registry-row",
        "registry_rows": "1518 26th Av, ZIP 94122",
        "permits": 141,
        "second": "The City building registry records the same licence at the same address on 101 permit rows under the same name.",
        "flags": [
            ("notice", "Both registries agree on the firm name, the street address and the ZIP for this licence number, which makes this one of the cleaner identity rows in Tier B. No CSLB page was read, so the licence’s own status is unknown."),
        ],
    },
    {
        "key": "jason-liu-construction-company",
        "name": "Jason Liu Construction Company",
        "lic": "662067",
        "phone": "415-215-7987",
        "trade_note": "plumbing-permit contact rows in the 94122 plumbing registry",
        "roof": "registry-row",
        "registry_rows": "1495 40th Av, ZIP 94122",
        "permits": 74,
        "second": "The City building registry records licence 662067 as “Jason Liu Construction Company” at 1495 40th Av, ZIP 94122 on 89 permit rows.",
        "flags": [
            ("notice", "Name and address agree across both registries. A construction company appearing on plumbing permit rows is a general-contracting pattern; no classification was read."),
        ],
    },
    {
        "key": "samco-construction-inc",
        "name": "Samco Construction Inc",
        "lic": "899541",
        "phone": "4158280177",
        "trade_note": "plumbing-permit contact rows in the 94122 plumbing registry",
        "roof": "registry-row",
        "registry_rows": "1623 Noriega St, ZIP 94122",
        "permits": 76,
        "second": "The City building registry records licence 899541 as “Samco Construction Inc” at 1623 Noriega St, ZIP 94122 on 79 permit rows.",
        "flags": [
            ("notice", "Name, street and ZIP agree across the two registries, and the recorded volume is similar on both (76 and 79 rows). No CSLB page was read."),
        ],
    },
    {
        "key": "ireland-tile-and-stone-inc",
        "name": "Ireland Tile & Stone Inc",
        "lic": "897547",
        "phone": "4155710679",
        "trade_note": "plumbing-permit contact rows in the 94122 plumbing registry",
        "roof": "registry-row",
        "registry_rows": "1558 39th Avenue, ZIP 94122",
        "permits": 76,
        "second": "No second-registry row was matched to this licence number.",
        "flags": [
            ("notice", "A tile and stone firm is recorded as a plumbing-permit contact. Tile work is adjacent to this project only if a tub surround has to be opened, and the registry row does not say what this firm did on any permit."),
        ],
    },
    {
        "key": "d-construction-inc",
        "name": "D Construction Inc",
        "lic": "1024901",
        "phone": "4158168862",
        "trade_note": "plumbing-permit contact rows in the 94122 plumbing registry",
        "roof": "registry-row",
        "registry_rows": "1726 45th Av, ZIP 94122",
        "permits": 87,
        "second": "The City building registry records licence 1024901 as “D Construction Inc” at 1726 45th Av, ZIP 94122 on 107 permit rows.",
        "flags": [
            ("notice", "Name and address agree across both registries. 45th Avenue is in the Outer Sunset, but the registry ZIP is a firm address and this project does not treat a firm ZIP as proof of dispatch."),
        ],
    },
    {
        "key": "cht-properties-development",
        "name": "Cht Properties Development",
        "lic": "812058",
        "phone": "451-225-8086",
        "trade_note": "plumbing-permit contact rows in the 94122 plumbing registry",
        "roof": "registry-row",
        "registry_rows": "1449 Moraga St, ZIP 94122",
        "permits": 80,
        "second": "No second-registry row was matched to this licence number.",
        "flags": [
            ("discrepancy", "The registry prints the phone as “451-225-8086”. As with the other 451 values in this wave, a transposition to 415 is plausible but unproven, so the string is stored as printed."),
            ("notice", "The firm name suggests property development rather than a trade licence. No CSLB page was read, so no classification is asserted."),
        ],
    },
    {
        "key": "z-construction-company-inc",
        "name": "Z Construction Company Inc",
        "lic": "740407",
        "phone": "415-931-8718",
        "trade_note": "plumbing-permit contact rows in the 94122 plumbing registry",
        "roof": "registry-row",
        "registry_rows": "1226 28th Av, ZIP 94122",
        "permits": 76,
        "second": "The City building registry records licence 740407 as “Z Construction Company Inc” at 1226 28th Av, ZIP 94122 on 100 permit rows.",
        "flags": [
            ("notice", "Name and address agree across both registries. The 415-931-8718 number is printed in full with an area code, unlike several other Tier B rows."),
        ],
    },
    {
        "key": "c-g-adams-construction",
        "name": "C G Adams Construction",
        "lic": "777558",
        "phone": None,
        "trade_note": "building-permit contact rows with a 94122 firm ZIP",
        "roof": "registry-row",
        "registry_rows": "1487 45th Av, ZIP 94122",
        "permits": 139,
        "second": "No second-registry row was matched to this licence number, and the building registry carries no phone column in the projection used.",
        "flags": [
            ("notice", "139 building permit rows are recorded under this licence number at a 94122 firm address. The building registry prints no phone for the row, so this record carries no contact number at all rather than a number taken from somewhere else."),
        ],
    },
    {
        "key": "ht-construction-company",
        "name": "Ht Construction Company",
        "lic": "993020",
        "phone": None,
        "trade_note": "building-permit contact rows with a 94122 firm ZIP",
        "roof": "registry-row",
        "registry_rows": "1488 28th Av, ZIP 94122",
        "permits": 77,
        "second": "No second-registry row was matched to this licence number, and the building registry carries no phone column in the projection used.",
        "flags": [
            ("notice", "77 building permit rows are recorded under this licence number at a 94122 firm address. No phone is printed for the row, so the record carries none."),
        ],
    },
    {
        "key": "nicholas-spencer-firth-gen-contr",
        "name": "Nicholas Spencer Firth Gen Contr",
        "lic": "873895",
        "phone": None,
        "trade_note": "building-permit contact rows with a 94122 firm ZIP",
        "roof": "registry-row",
        "registry_rows": "1543 17th Av, ZIP 94122",
        "permits": 76,
        "second": "No second-registry row was matched to this licence number, and the building registry carries no phone column in the projection used.",
        "flags": [
            ("notice", "The registry name is an individual’s name with the abbreviation “Gen Contr” appended, so the row records a personal-name licensee rather than a company. No CSLB page was read, so no entity or classification is asserted."),
        ],
    },
    {
        "key": "john-woo-construction-llc",
        "name": "John Woo Construction llc",
        "lic": "765131",
        "phone": None,
        "trade_note": "building-permit contact rows with a 94122 firm ZIP",
        "roof": "registry-row",
        "registry_rows": "1326 11th Av, ZIP 94122",
        "permits": 68,
        "second": "No second-registry row was matched to this licence number, and the building registry carries no phone column in the projection used.",
        "flags": [
            ("notice", "The registry prints the entity as “llc” in lower case with no space before it. The string is stored as-read rather than normalised to “LLC”."),
        ],
    },
    {
        "key": "j-t-a-c-corp",
        "name": "J-T A C  Corp",
        "lic": "512826",
        "phone": None,
        "trade_note": "building-permit contact rows with a 94122 firm ZIP",
        "roof": "registry-row",
        "registry_rows": "1465 46th Av, ZIP 94122",
        "permits": 74,
        "second": "No second-registry row was matched to this licence number, and the building registry carries no phone column in the projection used.",
        "flags": [
            ("notice", "The registry prints the firm name with two spaces between “J-T A C” and “Corp”. The string is stored as-read, including the spacing."),
        ],
    },
    {
        "key": "l-g-construction-co-inc",
        "name": "L.G. Construction Co.,Inc",
        "lic": "656193",
        "phone": None,
        "trade_note": "building-permit contact rows with a 94122 firm ZIP",
        "roof": "registry-row",
        "registry_rows": "1032 Irving St, ZIP 94122",
        "permits": 73,
        "second": "No second-registry row was matched to this licence number, and the building registry carries no phone column in the projection used.",
        "flags": [
            ("notice", "The registry prints the firm as “L.G. Construction Co.,Inc” with no space after the final comma. The string is stored as-read."),
            ("notice", "Two wave-10 registry leads share the 1032 Irving St address under different licence numbers. A shared commercial street address is a documented overlap and not evidence that the two licence numbers belong to one operator."),
        ],
    },
    {
        "key": "chin-pang-construction-co",
        "name": "Chin Pang Construction Co",
        "lic": "442727",
        "phone": None,
        "trade_note": "building-permit contact rows with a 94122 firm ZIP",
        "roof": "registry-row",
        "registry_rows": "1526 40th Av, ZIP 94122",
        "permits": 142,
        "second": "No second-registry row was matched to this licence number, and the building registry carries no phone column in the projection used.",
        "flags": [
            ("hold", "The City registry prints this firm’s name as “Chin Pang Construction Co ***Check Id***”. The annotation is the City’s own unresolved identity warning on the row. Until the licence number is read at the regulator and the flag is resolved, this record is held and may not be promoted."),
            ("notice", "142 building permit rows at a 94122 firm address is a high count, which makes resolving the City’s own identity warning more valuable rather than less."),
        ],
    },
    {
        "key": "stewart-cheung-const",
        "name": "Stewart Cheung Const",
        "lic": "362539",
        "phone": "415-665-6391",
        "trade_note": "plumbing-permit contact rows with a 94122 firm address",
        "roof": "registry-row",
        "registry_rows": "1277 41st Ave, ZIP 94122",
        "permits": 52,
        "second": "The building registry was queried separately for this licence number and no second row was matched, so the plumbing reading is the only City row this record rests on.",
        "flags": [
            ("notice", "52 plumbing permit rows at a 94122 firm address is a mid-range count in this registry — enough to show the firm appears on City plumbing paperwork, not enough to say anything about current capacity."),
            ("notice", "The registry prints the name with the abbreviation “Const” rather than a spelled-out trade, so the string is stored as-read and the licence number, not the string, is what a future regulator read would resolve."),
        ],
    },
    {
        "key": "k-a-lau-construction",
        "name": "K A Lau Construction",
        "lic": "823195",
        "phone": "415-812-4776",
        "trade_note": "plumbing-permit contact rows with a 94122 firm address",
        "roof": "registry-row",
        "registry_rows": "1362 33rd Av, ZIP 94122",
        "permits": 51,
        "second": "The building registry was queried separately for this licence number and no second row was matched, so the plumbing reading is the only City row this record rests on.",
        "flags": [
            ("notice", "51 plumbing permit rows at a 94122 firm address on 33rd Avenue, inside the Outer Sunset. The count is recorded activity under a licence number, never a promise of availability."),
        ],
    },
    {
        "key": "x-t-construction-co",
        "name": "X T Construction Co.",
        "lic": "608799",
        "phone": "415-566-7080",
        "trade_note": "plumbing-permit contact rows with a 94122 firm address",
        "roof": "registry-row",
        "registry_rows": "1875 19th Avenue, ZIP 94122",
        "permits": 48,
        "second": "The building registry was queried separately for this licence number and no second row was matched, so the plumbing reading is the only City row this record rests on.",
        "flags": [
            ("notice", "48 plumbing permit rows at a 94122 firm address. The registry prints a full stop inside the firm name; the string is stored exactly as printed."),
            ("notice", "A construction firm appearing as a contact on plumbing permits is the pattern this project watches for: it records that the firm appears on the paperwork, not that it performed the plumbing described on it."),
        ],
    },
]

# --------------------------------------------------------------------------
# Tier C — 12 platform listings read directly on a Thumbtack category page.
# --------------------------------------------------------------------------
TT_DRY = "https://www.thumbtack.com/ca/san-francisco/drywall-repair"
TT_PLM = "https://www.thumbtack.com/ca/san-francisco/plumbers"

TIER_C = [
    {
        "key": "sham",
        "name": "Sham",
        "trade": "finish",
        "rating": "No rating shown on the category page",
        "hires": "No hire count shown",
        "scope": "Palo Alto interior-painting category",
        "path": "/ca/palo-alto/interior-painting/sham/service/485881297731002398",
        "badges": "None shown",
        "source": S_TT_DRYWALL,
        "review": {
            "author": "Thumbtack Customer",
            "quote": "I hired Sergio to repair some drywall holes that came with our condo when we purchased it. He was able to accommodate our schedule and the work was completed well and quickly.",
            "theme": "Drywall holes repaired on a buyer’s schedule",
        },
        "analysis": "The reviewer is attributed only as “Thumbtack Customer”, so the account cannot be tied to a named person, and the listing is a single first name. A single-word listing name is the weakest possible identity anchor, which is why the record carries a hold.",
        "hold": True,
    },
    {
        "key": "repipe-specialists-san-francisco-bay-area",
        "name": "Repipe Specialists - San Francisco Bay Area",
        "trade": "plumbing",
        "rating": "Good 4.4 (42)",
        "hires": "5 hires on Thumbtack",
        "scope": "Serves San Francisco, CA",
        "path": "/ca/daly-city/repiping-specialists/repipe-specialists-san-francisco-bay-area/service/479245870668922887",
        "badges": "Licensed pro",
        "source": S_TT_PLUMB,
        "review": {
            "author": "Michael McMillan",
            "quote": "Out came a team to start cutting out walls and ceiling to access the pipes that needed to be replaced. The workers did an excellent job putting up visqueen plastic sheeting to protect areas of the house that weren’t affected … About a week later, another team came to patch the holes, re-plaster and re-stucco",
            "theme": "Walls and ceiling opened, then patched and re-plastered",
            "long": True,
        },
        "analysis": "Of every review read for this wave, this is the only one that describes in sequence opening walls and a ceiling for plumbing access, protecting the rest of the house with visqueen, and then returning to patch, re-plaster and repaint — including the observation that the repairs were undetectable. Two caveats are recorded rather than smoothed away: the quotation is abridged, and the review describes a whole-house repipe, which is the opposite of a repair-first outcome. The listing describes repiping, so its core trade is replacement, not freeing a seized mechanism.",
    },
    {
        "key": "jose-garcia",
        "name": "Jose Garcia",
        "trade": "plumbing",
        "rating": "Exceptional 5.0 (326)",
        "hires": "465 hires on Thumbtack",
        "scope": "Serves San Francisco, CA",
        "path": "/ca/san-francisco/garbage-disposal-repair/jose-garcia/service/193254471336019178",
        "badges": "Great value; no licence badge shown",
        "source": S_TT_PLUMB,
        "review": {
            "author": "Pearl K.",
            "quote": "Jose was knowledgeable and professional. Will work with him again!",
            "theme": "Knowledgeable, repeat hire",
        },
        "analysis": "This is the highest review count and hire count of any wave-10 listing, and it is the same generic praise the project records for what it is: a signal about manner, not about a seized overflow. Notably, no “Licensed pro” badge is shown for this listing while two others on the same page carry one, which is the kind of absence this project stores as a gap rather than as a neutral fact. The listing name is a personal name with no business suffix, so a licence match at the regulator would require more than a name.",
    },
    {
        "key": "century-build-group-inc",
        "name": "Century Build Group, Inc.",
        "trade": "general",
        "rating": "5.0 (1)",
        "hires": "3 hires on Thumbtack",
        "scope": "Serves San Francisco, CA",
        "path": "/ca/burlingame/water-damage/century-build-group-inc/service/583088289085390853",
        "badges": "Licensed pro",
        "source": S_TT_PLUMB,
        "review": {
            "author": "Daniela L.",
            "quote": "I honestly didn’t know what to expect when we found water damage and mold in our home. It was stressful and a little scary. The team at Century Build group made the whole process so much easier than I thought it would be. They showed up on time, explained everything clearly, and treated our home with real care.",
            "theme": "Water damage and mold remediation with clear explanation",
        },
        "analysis": "Water-damage remediation is the closest listed trade to the “open a ceiling, then make it look like nothing happened” half of this project, and the review credits clear explanation, which is the behaviour most likely to produce a written stop point. The evidence base is one review from three hires, which is far too thin to weigh as a pattern, and the page shows no rating beyond that single entry.",
    },
    {
        "key": "canel-solutions",
        "name": "Canel Solutions",
        "trade": "drywall",
        "rating": "Excellent 4.9 (130)",
        "hires": "241 hires on Thumbtack",
        "scope": "Serves San Francisco, CA",
        "path": "/ca/richmond/vinyl-siding-repair/canel-solutions/service/511225757012983810",
        "badges": "Top Pro; In high demand",
        "source": S_TT_DRYWALL,
        "review": {
            "author": "Dena A.",
            "quote": "And finally, repaired another wall and ceiling that had been ripped out, replaced insulation, installed drywall, textured, and painted.",
            "theme": "Wall and ceiling rebuilt, textured and painted after being opened",
        },
        "analysis": "The review describes a wall and a ceiling that had already been ripped out being rebuilt, insulated, textured and painted — the finish-side sequence the fallback plan needs, told from the customer's side. Both limits are recorded rather than smoothed over: the review does not say how the rest of the room was protected while the ceiling was open, and it does not say whether the opening was left as a usable access hatch. The listing's profile path points at Richmond while the category page states that it serves San Francisco.",
    },
]

# --------------------------------------------------------------------------
# Verification upgrades: licences read here that resolve to records already in
# the corpus. These add regulator facts to an existing record; they are NOT new
# entries and are never counted toward the 50.
# --------------------------------------------------------------------------
UPGRADES = [
    {
        "key": "national",
        "name": "National Plumbing",
        "lic": "619642",
        "entity": "NATIONAL PLUMBING",
        "status": "active",
        "expires": "2027-05-31",
        "classes": ["C36"],
        "phone": "415-310-4928",
        "address": "1472 24TH AVENUE, SAN FRANCISCO, CA 94122",
        "form": "Sole Ownership",
        "issued": "05/18/1991",
        "status_text": "This license is current and active.",
        "area": "outer",
        "area_text": "CSLB itself places this licensee at 1472 24th Avenue, San Francisco 94122 — an Outer Sunset address — with an active C36 classification expiring 05/31/2027. The City plumbing registry records 1,036 permit rows under this licence at a 94122 firm address, the highest count found in this pass.",
        "false_claim": "A construction-network company page repeats the 1472 24th Ave address but prints +14157531618, and the City registry prints 451-753-1618 — a value whose area code does not exist in California. CSLB publishes (415) 310-4928. The CSLB reading is stored and both other values are flagged.",
        "note": "Earlier waves stored this business as a discovery-only record with coverage unconfirmed and no regulator read. Licence 619642 was read directly in wave 10 and the record is upgraded with the regulator facts; the ID and its history are unchanged.",
    },
    {
        "key": "sunny-plumbing",
        "name": "Sunny's Plumbing Inc",
        "lic": "536715",
        "entity": "SUNNY'S PLUMBING INC",
        "status": "active",
        "expires": "2028-07-31",
        "classes": ["C16", "C36"],
        "phone": "415-716-3817",
        "address": "1786 35TH AVENUE, SAN FRANCISCO, CA 94122",
        "form": "Corporation",
        "issued": "07/29/1988",
        "status_text": "This license is current and active.",
        "area": "outer",
        "area_text": "CSLB itself places this licensee at 1786 35th Avenue, San Francisco 94122 — an Outer Sunset address — with active C16 and C36 classifications. The address matches the value the City registry already stored against this record.",
        "false_claim": "The record’s stored phone, 415-665-1029, comes from the City registry; CSLB publishes (415) 716-3817. A search result for a Yelp page titled “Best Things to Do near Sunny’s Plumbing” carries an aggregate rating of 4.5 from 2,603 reviews, but that is the page’s attraction category and not this plumber’s rating; the figure is quarantined and never rendered as a business rating. A directory profile states it has received no reviews for this contractor at all, and lists a second licence number 524327 that was not read.",
        "note": "Earlier waves stored this business as a registry-only lead with no licence read. Licence 536715 was read directly in wave 10; the record is upgraded and the C16 fire-protection classification is added to the licence fact.",
    },
    {
        "key": "w5-stan-plumbing",
        "name": "Stan Plumbing",
        "lic": "410861",
        "entity": "STAN PLUMBING",
        "status": "suspended",
        "expires": "2027-08-31",
        "classes": ["C36"],
        "phone": "415-724-0724",
        "address": "1429 9TH AVE APT 3, SAN FRANCISCO, CA 94122",
        "form": "Sole Ownership",
        "issued": "08/25/1981",
        "status_text": "License is under suspension for the following reasons: License is under Contractors Bond Suspension.",
        "area": "outer",
        "area_text": "CSLB itself places this licensee at 1429 9th Ave Apt 3, San Francisco 94122, with a C36 classification — but the licence is under a contractor’s-bond suspension, with the bond cancellation dated 09/01/2026, eleven days before the check date.",
        "false_claim": "A registry-only reading showed this firm at an Inner Sunset address with no rating shown and no licence status. The licence status is now known and it is a suspension, which is exactly the fact a register-only check cannot surface.",
        "note": "Upgraded from a wave-5 registry lead. The regulator read converts an unverified guess into a documented suspension and the record is held.",
        "hold": True,
    },
    {
        "key": "chosen",
        "name": "Chosen Rooter & Plumbing",
        "lic": "1054611",
        "entity": "CHOSEN ROOTER & PLUMBING INC",
        "status": "active",
        "expires": "2028-06-30",
        "classes": ["C36"],
        "phone": "415-702-9919",
        "address": "338 N CANAL ST STE 12, SOUTH SAN FRANCISCO, CA 94080",
        "form": "Corporation",
        "issued": "06/12/2019 · reissued 06/11/2020",
        "status_text": "This license is current and active.",
        "area": "sf",
        "area_text": "CSLB places this licensee at 338 N Canal St Ste 12, South San Francisco 94080 with an active C36 classification expiring 06/30/2028. The City plumbing registry records 93 permit rows under this licence at 1850 23rd Ave, ZIP 94122.",
        "false_claim": "The earlier record said only that the business “explicitly says outer and inner Sunset”, with no phone and no licence. CSLB publishes (415) 702-9919 — the same number the registry prints — and the licence carries both plumbing workers’-compensation wage classes. The registry phone is the first exact agreement between a registry row and a regulator row found in this pass.",
        "note": "Upgraded from an early discovery-only record. Licence 1054611 was read directly in wave 10; identity, classification, status and phone are now regulator-backed.",
    },
    {
        "key": "w7-franks-all-city-plumbing",
        "name": "Franks All City Plumbing",
        "lic": "319594",
        "entity": "FRANKS ALL CITY PLUMBING CO",
        "status": "expired",
        "expires": "2018-10-31",
        "classes": ["C36"],
        "phone": "415-407-2140",
        "address": "2560 TURNBERRY DRIVE, SAN BRUNO, CA 94066",
        "form": "Sole Ownership",
        "issued": "04/27/1976",
        "status_text": "This license is expired and not able to contract at this time.",
        "area": "outside",
        "area_text": "CSLB places this licensee at 2560 Turnberry Drive, San Bruno 94066, with a licence expired since 10/31/2018 and a contractor’s bond cancelled 11/03/2018. The registry address stored against this record was “22nd Avenue” with no street number.",
        "false_claim": "The record previously said only that the licence number it returned “has NOT been read on CSLB”. It has now been read, and the licence expired more than seven years before the check date. The registry phone 415-661-2696 also disagrees with CSLB’s (415) 407-2140. An unread licence number can be an expired licence, and this read is what converts that possibility into a fact.",
        "note": "Upgraded from a wave-7 registry lead. The licence number the registry returned is now read: C36, expired 2018.",
        "hold": True,
    },
    {
        "key": "w6-ren-lei-construction-co",
        "name": "Ren Lei Construction Co",
        "lic": "635360",
        "trade": "general",
        "entity": "REN LEI CONSTRUCTION CO INC",
        "status": "active",
        "expires": "2028-01-31",
        "classes": ["B"],
        "phone": "415-238-1202",
        "address": "750 LAWTON STREET, SAN FRANCISCO, CA 94122",
        "form": "Corporation",
        "issued": "01/11/1992 · reissued 01/30/1996",
        "status_text": "This license is current and active.",
        "area": "outer",
        "area_text": "CSLB itself places this licensee at 750 Lawton Street, San Francisco 94122 — an Outer Sunset address — with an active B classification expiring 01/31/2028 and workers’-compensation codes that include plumbing-low wage.",
        "false_claim": "The record previously carried a registry address and a phone with no licence. CSLB now confirms the entity, the Outer Sunset address, the active B classification and the phone, which matches the stored value exactly. The licence is B only, so it can general-contract but cannot self-perform the plumbing or the drywall.",
        "note": "Upgraded from a wave-6 registry lead. Licence 635360 is now read; the stored phone is regulator-confirmed.",
    },
    {
        "key": "sberlo",
        "name": "Sberlo Plumbing Inc",
        "lic": "487017",
        "entity": "SBERLO PLUMBING INC",
        "status": "canceled",
        "expires": "2011-02-20",
        "classes": ["C36"],
        "phone": "415-664-9282",
        "address": "1663 12TH AVENUE, SAN FRANCISCO, CA 94122",
        "form": "Corporation",
        "issued": "02/13/1986",
        "status_text": "This license is canceled and not able to contract.",
        "area": "outer",
        "area_text": "CSLB places this licensee at 1663 12th Avenue, San Francisco 94122. The licence was canceled, and the board’s Miscellaneous Information records a Secretary of State dissolution on 02/20/2011.",
        "false_claim": "The registry phone 415-664-9282 matches the CSLB number exactly, so identity is not in question; the licence status is. The City registry still lists 517 permit rows under this number at an Outer Sunset address.",
        "note": "Upgraded from a registry lead stored in an earlier wave. The 94122 address the registry recorded is confirmed by CSLB, and the licence is canceled.",
        "hold": True,
    },
    {
        "key": "w6-bill-bragg-plumbing",
        "name": "Bill Bragg Plumbing",
        "lic": "440780",
        "entity": "BILL BRAGG PLUMBING",
        "status": "active",
        "expires": "2027-05-31",
        "classes": ["C36"],
        "phone": "415-894-7231",
        "address": "620A GUERRERO ST, SAN FRANCISCO, CA 94110",
        "form": "Sole Ownership",
        "issued": "05/31/1983",
        "status_text": "This license is current and active.",
        "area": "sf",
        "area_text": "CSLB places this licensee at 620A Guerrero St, San Francisco 94110 — the Mission, not the Sunset. The City plumbing registry records 470 permit rows under this licence at a 94122 PO-box address.",
        "false_claim": "The workers’-compensation line shows an expiry date of 09/01/2026, which is eleven days before the check date, while the licence still reads current and active and a new contractor’s bond took effect the same day. A workers’-compensation lapse can suspend a licence, so the registry-derived phone 415-661-1705 and the apparent coverage gap are both flagged.",
        "note": "Upgraded from a wave-6 registry lead. Identity is now regulator-confirmed and two new facts appear that the registry row could not show: a published San Francisco address in a different district, and a workers’-compensation expiry that has already passed.",
        "flag_wc": True,
    },
    {
        "key": "w7-david-chu-plumbing",
        "name": "David Chu Plumbing",
        "lic": "343610",
        "entity": "DAVID CHU PLUMBING",
        "status": "inactive",
        "expires": "2028-02-29",
        "classes": ["C36"],
        "phone": "415-269-3861",
        "address": "1530 29TH AVENUE, SAN FRANCISCO, CA 94122",
        "form": "Sole Ownership",
        "issued": "09/12/1977",
        "status_text": "This license is inactive and not able to contract at this time.",
        "area": "outer",
        "area_text": "CSLB places this licensee at 1530 29th Avenue, San Francisco 94122 — an Outer Sunset address — but the licence is inactive, with Additional Status noting it needs a contractor’s bond and must meet workers’-compensation requirements to reactivate.",
        "false_claim": "The registry showed 122 permit rows at this Outer Sunset address and a licence number with no status. The read now shows “inactive and not able to contract at this time”, recorded on 10/16/2023 as “WC EXEMPT CANCELLED-LIC INACTIVATED”, while the expiry date still reads 02/29/2028 — which is why an expiry date alone is never treated as proof of an active licence.",
        "note": "Upgraded from a wave-7 registry lead. The record’s licence status changes from unknown to inactive, and the record is held.",
        "hold": True,
    },
    {
        "key": "cl",
        "name": "C&L Plumbing Inc",
        "lic": "982738",
        "entity": "C & L PLUMBING INC",
        "status": "active",
        "expires": "2027-04-30",
        "classes": ["C36"],
        "phone": "415-609-2182",
        "address": "1516 MORAGA STREET, SAN FRANCISCO, CA 94122",
        "form": "Corporation",
        "issued": "04/15/2013",
        "status_text": "This license is current and active.",
        "area": "outer",
        "area_text": "CSLB places this licensee at 1516 Moraga Street, San Francisco 94122 — an Outer Sunset address — with an active C36 plumbing classification expiring 04/30/2027. The City plumbing registry records the same licence at the same address across 62 permit rows, so the regulator and the City agree on both where the firm is and where it has been recorded working.",
        "false_claim": "The stored record said only “Outer Sunset service not established”, with no licence, no classification, no phone and no trade. CSLB publishes licence 982738 as an active Corporation at an Outer Sunset address with C36 plumbing, and the City registry confirms the same address under the same number. The licence is plumbing only: nothing on the regulator page covers the drywall side.",
        "note": "Upgraded from the stored record “C&L Plumbing Inc”. Licence 982738 was read directly in wave 10; entity, form, address, phone, classification and status are now regulator-backed, and the address is inside the district.",
    },
]

# --------------------------------------------------------------------------
# Registry upgrades. These two firms were stored in earlier waves from indexed
# Yelp pages with no licence identity of any kind. Wave 10 found each of them in
# the City's own permit-contact registries under a licence number at a 94122
# firm address. The licence number is recorded as a lead and is deliberately NOT
# read at CSLB here, so no entity, classification, status or expiry is asserted.
# --------------------------------------------------------------------------
REGISTRY_UPGRADES = [
    {
        "key": "kh-construction",
        "name": "K&H Construction Development",
        "lic": "1079861",
        "rows": "145 Judah St 2, ZIP 94122",
        "permits": 68,
        "registry": "building",
        "note": "The stored record rests on an indexed Yelp contractor page listing K&H in the Outer Sunset with bathroom and kitchen remodels and no licence identity. The City building-permit contact registry records the firm name at 145 Judah St 2, ZIP 94122 — 145 Judah St is in the Outer Sunset — under licence number 1079861 across 68 building-permit rows.",
        "why": "A licence number recorded by the City is a lead, not a credential: it is published here so the next pass reads 1079861 at CSLB instead of searching for the firm again. Nothing about the number’s entity, classification, status or expiry is asserted, and the record’s existing gaps are not cleared.",
    },
    {
        "key": "oshaughnessy",
        "name": "O Shaughnessy Construction",
        "lic": "922762",
        "rows": "1414 20th Av, ZIP 94122",
        "permits": 71,
        "registry": "plumbing",
        "note": "The stored record rests on an indexed Yelp contractor page serving San Francisco with about 19 reviews and no licence identity. The City plumbing-permit contact registry records this firm name at 1414 20th Av, ZIP 94122 under licence number 922762 across 71 plumbing-permit rows.",
        "why": "The registry string carries an apostrophe (“O’shaughnessy Construction”) that the stored record does not, and the City row places the firm at a 94122 address. Both readings are kept visible rather than reconciled by assumption, and the licence number is a lead for the next regulator read, not a credential.",
    },
]

REVIEW_PLATFORM = "Thumbtack"


def build_reviews():
    reviews = []
    n = 129
    for rec in TIER_C:
        rv = rec["review"]
        reviews.append(
            {
                "id": f"R{n}",
                "business": f"w10-{rec['key']}",
                "platform": REVIEW_PLATFORM,
                "source": rec["source"],
                "author": rv["author"],
                "published": None,
                "checkedAt": DATE,
                "quote": rv["quote"],
                "theme": rv["theme"],
                "analysis": rec["analysis"],
                "exactTask": False,
                "negative": False,
                "access": "page",
                "identity": "matched",
                "platformUrl": rec["path"] if rec["path"].startswith("http") else f"https://www.thumbtack.com{rec['path']}",
            }
        )
        n += 1
    return reviews


def _cslb_claim(lic: str, field: str, text: str, excerpt: str):
    return {"field": field, "text": text, "source": LIC_SRC[lic], "excerpt": excerpt}


def build_registry_upgrades():
    """Turn a City-recorded licence number into evidence on an existing record."""
    out = []
    for rec in REGISTRY_UPGRADES:
        sid = S_REG_BUILD if rec["registry"] == "building" else S_REG_PLUMB
        out.append(
            {
                "key": rec["key"],
                "lic": rec["lic"],
                "source": sid,
                "note": rec["note"],
                "why": rec["why"],
                "claim": {
                    "field": "Registry evidence",
                    "text": rec["note"],
                    "source": sid,
                    "excerpt": f"license={rec['lic']} · {rec['rows']} · permits={rec['permits']}",
                },
                "flag": {
                    "level": "notice",
                    "text": f"wave-10 registry read: the City records licence number {rec['lic']} for this firm at {rec['rows']} across {rec['permits']} permit rows. The number is recorded, NOT read at CSLB, so no entity, classification, status or expiry is asserted and every earlier gap stands. {rec['why']}",
                    "sources": [sid],
                },
            }
        )
    return out


def build_tier_a():
    out = []
    for rec in TIER_A:
        lic = rec["lic"]
        sid = LIC_SRC[lic]
        classes = " · ".join(rec["classes"])
        issued_line = f"issued {rec['issued']}"
        if rec.get("reissued"):
            issued_line += f" · reissued {rec['reissued']}"
        excerpt = f"#{lic} · {CSLB_LEGAL_NAME[lic]} · {rec['status']} · {classes} · {issued_line} · expires {rec['expires']} · {rec['entity']}"
        claims = [
            _cslb_claim(
                lic,
                "Discovery",
                "The CSLB detail page was opened directly and transcribed line by line: legal entity, business form, address, phone, issue and reissue dates, expiry date, status text, every displayed classification, the contractor’s bond line, the workers’-compensation line, and any Additional Status or Miscellaneous Information entry.",
                excerpt,
            ),
            _cslb_claim(
                lic,
                "Credential",
                f"CSLB displays licence #{lic} as {rec['status']} with classification(s) {classes}. The page states: “{rec['status_text']}” A licence status never establishes exact-task experience.",
                f"{rec['status_text']} · {rec['address']} · business phone {rec['phone']}",
            ),
            _cslb_claim(
                lic,
                "Insurance & bond",
                "Bond and workers’-compensation lines were read on the regulator page rather than accepted from a directory. Displayed coverage is recorded as displayed; it has not been confirmed with the insurer for this project.",
                f"{rec['bond']} {rec['wc']}",
            ),
        ]
        if rec.get("additional"):
            claims.append(
                _cslb_claim(
                    lic,
                    "Additional status",
                    "The board’s Additional Status block is reproduced as printed, because it states what the licence would need before it could contract again.",
                    rec["additional"],
                )
            )
        claims.append(
            _cslb_claim(
                lic,
                "Miscellaneous",
                "The board’s Miscellaneous Information block is reproduced as printed. Entries such as reissues and dissolutions describe the licence number’s history, not the current operator’s work.",
                rec["misc"],
            )
        )
        claims.append(
            {
                "field": "Registry identity",
                "text": rec["registry"],
                "source": S_REG_PLUMB if "building registry" not in rec["registry"] or "plumbing" in rec["registry"] else S_REG_BUILD,
                "excerpt": rec["registry"],
            }
        )
        claims.append(
            {
                "field": "Coverage",
                "text": rec["area_text"],
                "source": sid,
                "excerpt": f"{rec['address']} · ZIP 94122 evidence recorded in the City permit registries",
            }
        )
        flags = [
            {"level": lvl, "text": txt, "sources": [sid, S_REG_PLUMB, S_REG_BUILD]}
            for lvl, txt in rec.get("registry_flags", [])
        ]
        if rec["status"] != "active":
            flags.insert(
                0,
                {
                    "level": "hold",
                    "text": f"CSLB reads this licence as {rec['status']}, so the business cannot contract on it at the check date. Held rather than presented as bookable; the {rec['status']} status is preserved rather than smoothed over.",
                    "sources": [sid],
                },
            )
        flags.append(
            {
                "level": "gap",
                "text": "No independent review corpus was retrievable for this licence in this pass, and no review is reconstructed to fill the gap.",
                "sources": [sid],
            }
        )
        out.append(
            {
                "id": f"w10-{rec['key']}",
                "name": rec["name"],
                "phone": rec["phone"],
                "phoneSource": sid,
                **({"phone_collision": rec["phone_collision"]} if rec.get("phone_collision") else {}),
                "website": None,
                "websiteSource": None,
                "trade": rec["trade"],
                "area": rec["region"],
                "areaText": rec["area_text"],
                "status": "excluded" if rec.get("excluded") else "research",
                "checkedAt": DATE,
                "claims": claims,
                "license": {
                    "number": lic,
                    "entity": CSLB_LEGAL_NAME[lic],
                    "classes": rec["classes"],
                    "status": rec["status"],
                    "expires": rec["expires"],
                    "checkedAt": DATE,
                    "source": sid,
                },
                "reviewIds": [],
                "platformLinks": [],
                "flags": flags,
                "gaps": [
                    "No source proves successful extraction of a seized bathtub overflow trip lever by this business.",
                    "No review or permit proves a small ceiling opening was converted into a finished, reusable access hatch by this business.",
                    "Project-specific liability and workers’-compensation coverage were not independently verified with the insurer.",
                    "Current Outer Sunset dispatch was not confirmed by this business in its own words.",
                    "No written repair-first scope or stop point was obtained from this business.",
                ],
                "priority": None,
                "rationale": rec["area_text"],
                "nextStep": "Re-read the CSLB page at the time of contact, then ask for a diagnostic-only, repair-first scope: examples involving a seized trip-lever plunger in an older galvanised waste-and-overflow assembly, the least invasive method, a written stop point before any hidden-pipe replacement, who patches and finishes any ceiling opening and whether it is left as a usable access hatch, current Outer Sunset dispatch, and project-specific insurance.",
                "exactMatch": False,
                "insuranceVerified": False,
                "scopeConfirmed": False,
                "master": False,
            }
        )
    return out


def build_tier_b():
    out = []
    for rec in TIER_B:
        flags = [
            {"level": lvl, "text": txt, "sources": [S_REG_PLUMB, S_REG_BUILD]}
            for lvl, txt in rec["flags"]
        ]
        flags.append(
            {
                "level": "hold",
                "text": f"Licence number {rec['lic']} is recorded by the City registry but has NOT been read on CSLB. This record therefore holds no legal entity, no classification, no licence status and no expiry date, and it can never reach the qualified master.",
                "sources": [S_REG_PLUMB, S_REG_BUILD],
            }
        )
        claims = [
            {
                "field": "Registry",
                "text": f"The official City open-data permit registry records licence number {rec['lic']} under the firm name “{rec['name']}” at {rec['registry_rows']} across {rec['permits']} {rec['trade_note']}. The registry is the City’s own open data, but this row establishes only a recorded firm name, address, phone and licence number. Re-read in a confirmatory query on the check date. The licence number is deliberately NOT promoted into a licence fact.",
                "source": S_REG_PLUMB,
                "excerpt": f"license_number={rec['lic']} · firm={rec['name']} · addr={rec['registry_rows']} · permits={rec['permits']}",
            },
            {
                "field": "Coverage",
                "text": f"{rec['registry_rows']} is a 94122 firm address in the City’s own permit-contact data. A firm ZIP is a recorded address, not a dispatch promise, and it is not a regulator-confirmed Outer Sunset place of business.",
                "source": S_REG_BUILD,
                "excerpt": f"{rec['registry_rows']} · permits={rec['permits']}",
            },
            {
                "field": "Second registry reading",
                "text": rec["second"],
                "source": S_REG_BUILD,
                "excerpt": rec["second"],
            },
        ]
        out.append(
            {
                "id": f"w10-{rec['key']}",
                "name": rec["name"],
                "phone": rec["phone"],
                "phoneSource": S_REG_PLUMB if rec["phone"] else None,
                **({"phone_collision": rec["phone_collision"]} if rec.get("phone_collision") else {}),
                "website": None,
                "websiteSource": None,
                "trade": "registry-lead",
                "area": "sunset",
                "areaText": f"Registry lead only. The City registry records licence {rec['lic']} at {rec['registry_rows']} with {rec['permits']} permit rows. ZIP 94122 is the Outer Sunset ZIP, but a registry firm address is not a CSLB-confirmed place of business and no CSLB page was read for this record.",
                "status": "research",
                "checkedAt": DATE,
                "claims": claims,
                "license": None,
                "reviewIds": [],
                "platformLinks": [],
                "flags": flags,
                "gaps": [
                    "No CSLB licence-detail page was read, so the legal entity, classification, status and expiry behind this licence number are all unknown.",
                    "No review corpus was retrieved for this firm, and none is invented to balance the record.",
                    "No source proves successful extraction of a seized bathtub overflow trip lever by this business.",
                    "No proof that this firm can or will perform both the plumbing and the drywall side of the work.",
                ],
                "priority": None,
                "rationale": "A registry lead with a recorded 94122 permit history and a licence number that has not been read at the regulator. Useful only for prioritising which licence numbers to read next.",
                "nextStep": f"Read CSLB licence {rec['lic']} directly, then compare the regulator’s entity, address and phone field by field against the registry row before any contact.",
                "exactMatch": False,
                "insuranceVerified": False,
                "scopeConfirmed": False,
                "master": False,
            }
        )
    return out


def build_tier_c():
    out = []
    for rec in TIER_C:
        url = rec["path"] if rec["path"].startswith("http") else f"https://www.thumbtack.com{rec['path']}"
        flags = [
            {
                "level": "hold" if rec.get("hold") else "notice",
                "text": "A platform rating, hire count or “Licensed pro” badge is a platform claim about a listing. It is not a CSLB read, so this record carries no licence, no classification and no licence status.",
                "sources": [rec["source"]],
            },
            {
                "level": "gap",
                "text": "No Outer Sunset dispatch statement was retrieved for this listing. The service-area text shown is quoted exactly as the category page prints it.",
                "sources": [rec["source"]],
            },
        ]
        if rec.get("hold"):
            flags.append(
                {
                    "level": "hold",
                    "text": "The listing name is a single word and the review is attributed only to a generic platform account, so the identity of the business behind this listing cannot be resolved. Held.",
                    "sources": [rec["source"]],
                }
            )
        out.append(
            {
                "id": f"w10-{rec['key']}",
                "name": rec["name"],
                "phone": None,
                "phoneSource": None,
                "website": None,
                "websiteSource": None,
                "trade": rec["trade"],
                "area": "sf" if "San Francisco" in rec["scope"] or "san-francisco" in rec["path"] else "outside",
                "areaText": f"The listing states “{rec['scope']}” on the Thumbtack San Francisco category page read directly, and its profile path is {rec['path']}. A listing statement is not a verified Outer Sunset dispatch and the path shows a different home market wherever one differs.",
                "status": "hold" if rec.get("hold") else "research",
                "checkedAt": DATE,
                "claims": [
                    {
                        "field": "Listing evidence",
                        "text": f"The Thumbtack category page read directly shows this listing at {rec['rating']}, with {rec['hires']} and badges “{rec['badges']}”. These are platform figures quoted as published; none was independently confirmed.",
                        "source": rec["source"],
                        "excerpt": f"{rec['name']} · {rec['rating']} · {rec['hires']} · badges: {rec['badges']}",
                    },
                    {
                        "field": "Review evidence",
                        "text": f"One review is shown for this listing on the category page. It is attributed to {rec['review']['author']} and its text is reproduced exactly as published.",
                        "source": rec["source"],
                        "excerpt": rec["review"]["quote"],
                    },
                ],
                "license": None,
                "reviewIds": [],
                "platformLinks": [{"label": "Thumbtack listing", "url": url, "source": rec["source"]}],
                "flags": flags,
                "gaps": [
                    "No CSLB licence page was read for this listing, and a platform badge is not a licence.",
                    "No source proves successful extraction of a seized bathtub overflow trip lever by this business.",
                    "No written repair-first scope or stop point was obtained from this business.",
                    "The retained review corpus for this listing is one excerpt, not a full corpus.",
                ],
                "priority": None,
                "rationale": rec["analysis"],
                "nextStep": "Treat this as a finish-side candidate only. Ask for a small ceiling patch precedent, whether the work can be left as a usable access hatch, how the rest of the room is protected while a ceiling is open, and current Outer Sunset dispatch. Do not rely on the platform badge as a licence.",
                "exactMatch": False,
                "insuranceVerified": False,
                "scopeConfirmed": False,
                "master": False,
            }
        )
    return out


def main():
    businesses = build_tier_a() + build_tier_b() + build_tier_c()
    assert len(businesses) == 50, len(businesses)
    assert len(build_registry_upgrades()) == 2, "registry upgrades"
    reviews = build_reviews()
    # link reviews back to their business records
    by_id = {b["id"]: b for b in businesses}
    for rv in reviews:
        by_id[rv["business"]]["reviewIds"].append(rv["id"])
    for rv in reviews:
        rv.pop("platformUrl", None)
    payload = {
        "wave": 10,
        "date": DATE,
        "note": (
            "Wave 10 adds 50 nonduplicate businesses in three evidence tiers: records whose CSLB "
            "licence-detail page was opened and transcribed field by field, registry-only leads whose "
            "City-recorded licence number was deliberately NOT promoted into a licence fact, and "
            "platform listings read directly. It also applies verification upgrades to records that "
            "earlier waves had stored without a regulator read; those are published separately and are "
            "never counted toward the 50. The upgrade list is the dedupe result: each licence read here "
            "that resolved to an already-stored business became evidence on that record instead of a "
            "duplicate entry."
        ),
        "composition": {
            "regulatorRead": sum(1 for b in businesses if b.get("license")),
            "registryOnly": sum(1 for b in businesses if b.get("trade") == "registry-lead"),
            "platformListing": sum(
                1 for b in businesses
                if not b.get("license") and b.get("trade") != "registry-lead"
            ),
            "verificationUpgrades": len(UPGRADES),
        },
        "sources": SOURCES,
        "businesses": businesses,
        "reviews": reviews,
        "upgrades": UPGRADES,
        "registryUpgrades": build_registry_upgrades(),
        "dedupeRejections": [
            {"name": "Magaña Time Handyman", "existing": "w5-maga-a-time-handyman", "why": "already stored from wave 5"},
            {"name": "Aldana co", "existing": "w7-aldana-co", "why": "already stored from wave 7"},
            {"name": "Jovel Quality painting", "existing": "w7-jovel-quality-painting", "why": "already stored from wave 7"},
            {"name": "Honart", "existing": "w7-honart", "why": "already stored from wave 7"},
            {"name": "Fairfield Drywall Inc", "existing": "w7-fairfield-drywall-inc", "why": "already stored from wave 7"},
            {"name": "Walty Handy Service Pro", "existing": "w5-walty-handy-service-pro", "why": "already stored from wave 5"},
            {"name": "Sandoval drywall", "existing": "w7-sandoval-drywall", "why": "already stored from wave 7"},
            {"name": "Lazarit Construction", "existing": "w7-lazarit-construction", "why": "already stored from wave 7"},
            {"name": "Handyman Express", "existing": "w7-handyman-express", "why": "already stored from wave 7"},
            {"name": "RoDidIt", "existing": "w7-rodidit", "why": "already stored from wave 7"},
            {"name": "Baruch handyman services", "existing": "w7-baruch-handyman-services", "why": "already stored from wave 7"},
            {"name": "THWC home improvement", "existing": "w7-thwc-home-improvement", "why": "already stored from wave 7"},
            {"name": "Savr Handyman", "existing": "w7-savr-handyman", "why": "already stored from wave 7"},
            {"name": "New Age Drywall Inc", "existing": "w5-new-age-drywall-inc", "why": "already stored from wave 5"},
            {"name": "Rock & Smooth Drywall", "existing": "w7-rock-smooth-drywall", "why": "already stored from wave 7"},
            {"name": "Dr. Drain Plumbing and Rooter", "existing": "dr-drain", "why": "already stored"},
            {"name": "AMX Plumbing", "existing": "amx", "why": "already stored, with a different licence number on record"},
            {"name": "Ocean Air Heating", "existing": "w6-ocean-air-heating", "why": "already stored from wave 6"},
            {"name": "Jones Bros Construction & Design Inc", "existing": "w9-jones-bros-construction-design-inc", "why": "already stored from wave 9; its surname sibling was read here instead"},
            {"name": "Abe's Plumbing", "existing": "w6-abe-s-plumbing", "why": "already stored from wave 6"},
            {"name": "National Plumbing", "existing": "national", "why": "already stored; licence 619642 read here became a verification upgrade"},
            {"name": "Sunny's Plumbing Inc", "existing": "sunny-plumbing", "why": "already stored; licence 536715 read here became a verification upgrade"},
            {"name": "Stan Plumbing", "existing": "w5-stan-plumbing", "why": "already stored; licence 410861 read here became a verification upgrade"},
            {"name": "Sberlo Plumbing Inc", "existing": "sberlo", "why": "already stored; licence 487017 read here became a verification upgrade"},
            {"name": "Bill Bragg Plumbing", "existing": "w6-bill-bragg-plumbing", "why": "already stored; licence 440780 read here became a verification upgrade"},
            {"name": "David Chu Plumbing", "existing": "w7-david-chu-plumbing", "why": "already stored; licence 343610 read here became a verification upgrade"},
            {"name": "Chosen Rooter & Plumbing", "existing": "chosen", "why": "already stored; licence 1054611 read here became a verification upgrade"},
            {"name": "Franks All City Plumbing", "existing": "w7-franks-all-city-plumbing", "why": "already stored; licence 319594 read here became a verification upgrade"},
            {"name": "Ren Lei Construction Co", "existing": "w6-ren-lei-construction-co", "why": "already stored; licence 635360 read here became a verification upgrade"},
            {"name": "C&L Plumbing Inc", "existing": "cl", "why": "already stored; licence 982738 read here became a verification upgrade"},
            {"name": "Josael Reinosa", "existing": "w7-josael-reinosa", "why": "already stored from wave 7 with the same review excerpt retained as R69; no second copy was published"},
            {"name": "K&H Construction Development", "existing": "kh-construction", "why": "already stored from wave 1-2; the City registry row became a registry upgrade on that record"},
            {"name": "O Shaughnessy Construction", "existing": "oshaughnessy", "why": "already stored; the City registry row became a registry upgrade on that record"},
        ],
        "taskEvidence": [
            {
                "source": S_REDDIT_ASK,
                "point": "A responder describes the linkage as probably seized from disuse, suggests penetrating oil down the overflow, and states that when it is completely seized the entire drain has to be replaced — a job needing a plumber at roughly $400–$600.",
            },
            {
                "source": S_REDDIT_PLUM,
                "point": "The original poster reports that penetrating oil, a steam pot and plunging all failed, that force risked fracturing old rusted pipe, and later that they bought a replacement assembly, went through the drywall, installed it and repaired the drywall.",
            },
            {
                "source": S_REDDIT_HI_STUCK,
                "point": "A plumber attending in person confirms the obstruction is the mechanism rather than a clog and states that cutting through the wall would be required.",
            },
            {
                "source": S_REDDIT_HI_CANT,
                "point": "The mechanism is described as corrosion-welded, with a responder noting that penetrating oil is the right tool, that over-application is undesirable, and that a drain wrench is needed if the assembly is replaced.",
            },
            {
                "source": S_PLBC,
                "point": "A trade forum explains that a poured product runs straight past a hollow brass stopper, which is why soaking often fails, and that disassembling the overflow tube is the fallback.",
            },
            {
                "source": S_REDDIT_DIY,
                "point": "Descaling is recommended ahead of penetrating oil, with the warning that oil and its smell are undesirable in a bathtub — a constraints point for a rental where the fixture stays in use during attempts.",
            },
        ],
        "falseClaimsRejected": [
            {
                "claim": "Yelp aggregate rating of 4.5 from 2,603 reviews presented as Sunny’s Plumbing’s rating.",
                "source": S_YELP_NEAR,
                "why": "The JSON-LD aggregate on that page belongs to a “Things to Do near …” attraction category, not to the plumber. Recorded as a rejected third-party derivation and never rendered.",
            },
            {
                "claim": "Telephone +14157531618 for National Plumbing.",
                "source": S_PROCORE,
                "why": "A construction-network page prints a number that disagrees with the regulator’s own record for licence 619642. The CSLB value is stored and the conflict is flagged.",
            },
            {
                "claim": "BuildZoom listing licence 524327 for Sunny’s Plumbing Inc alongside 536715.",
                "source": S_BUILDZOOM,
                "why": "Only 536715 was read at the regulator. The second number is stored as a directory-stated lead and no fact is attached to it.",
            },
            {
                "claim": "Thumbtack “Licensed pro” badges as licence evidence.",
                "source": S_TT_PLUMB,
                "why": "A badge is a platform claim. No wave-10 platform record carries a licence, a classification or a status.",
            },
        ],
    }
    OUT.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT} — {len(businesses)} businesses, {len(SOURCES)} sources, {len(reviews)} reviews")


if __name__ == "__main__":
    main()
