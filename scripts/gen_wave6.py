#!/usr/bin/env python3
"""Build wave 6: 50 NEW source-linked plumbing / drywall / plaster discovery records.

Research date: 2026-09-11 (a separate snapshot date from waves 1-5, 2026-09-10).

Verification level of this wave is deliberately higher than waves 3-5:

* 22 of the 50 records carry a CSLB license detail page that was READ DIRECTLY
  this session on cslb.ca.gov (22 distinct license numbers). Every status,
  entity name, address, classification, bond, workers-compensation and
  miscellaneous line recorded below was transcribed from those pages.
* 38 of the 50 records were discovered through the OFFICIAL SF DBI open-data
  registry "Plumbing Permits Contacts" (dataset k6kv-9kix), queried directly by
  firm ZIP code (94122 Outer Sunset, 94116 Parkside) via the Socrata API. Each
  registry row is reproduced verbatim in the supporting excerpt.
* 12 of the 50 records are drywall / plaster / finish leads from indexed Yelp,
  Thumbtack, BBB, BuildZoom and Angi extracts plus business sites.
* 2 records carry BOTH a registry row and a direct CSLB read.

Fail-closed rules (mirrored by scripts/merge_wave6.py):
  - a registry row NEVER becomes a license fact. Registry-recorded license
    numbers stay inside attributed claims until CSLB is read directly.
  - a platform "Verified License" badge is NEVER converted into a CSLB record.
  - nothing is promoted to the qualified master list; exactMatch stays False.
  - expired / canceled / suspended licenses are recorded with a booking hold.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-11"

# --------------------------------------------------------------------------
# Sources. IDs continue from the merged dataset (max existing id = 149).
# --------------------------------------------------------------------------
REG_94122 = (
    "https://data.sf.gov/resource/k6kv-9kix.json?$select=firm_name,license_number,"
    "address,city,zipcode,phone,count(permit_number)&$where=zipcode%20like%20"
    "%2794122%25%27&$group=firm_name,license_number,address,city,zipcode,phone"
    "&$order=count(permit_number)%20DESC&$limit=60"
)
REG_94116 = (
    "https://data.sf.gov/resource/k6kv-9kix.json?$select=firm_name,license_number,"
    "address,city,zipcode,phone,count(permit_number)&$where=zipcode%20like%20"
    "%2794116%25%27&$group=firm_name,license_number,address,city,zipcode,phone"
    "&$order=count(permit_number)%20DESC&$limit=45"
)


def cslb(num):
    return f"https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum={num}"


SOURCES = [
    # --- official government side channels -------------------------------
    {"id": 150, "title": "SF DBI \u00b7 Plumbing Permits Contacts \u00b7 Outer Sunset 94122 firm query",
     "url": REG_94122, "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Official City & County of San Francisco open-data API (dataset k6kv-9kix, "
             "\u201cPlumbing Permits Contacts\u201d, provenance: official). Queried directly this "
             "session, grouped by firm name + CSLB number + recorded business address, ordered "
             "by permit-row count. Rows are historical plumbing-permit contacts and carry no "
             "in-dataset permit date: they establish a recorded address and license linkage, "
             "never present operation."},
    {"id": 151, "title": "SF DBI \u00b7 Plumbing Permits Contacts \u00b7 Parkside 94116 firm query",
     "url": REG_94116, "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Same official dataset queried for ZIP 94116 (Parkside / southern Outer Sunset "
             "border). Same limits: historical permit-contact rows, no in-dataset dates."},
    {"id": 152, "title": "SF DBI \u00b7 dataset metadata for k6kv-9kix",
     "url": "https://data.sf.gov/api/views/k6kv-9kix.json", "kind": "government",
     "access": "page", "checkedAt": DATE,
     "note": "Read directly to confirm the dataset identity used for firm discovery: name "
             "\u201cPlumbing Permits Contacts\u201d, description \u201cContacts of contractors for Plumbing "
             "Permits\u201d, category Housing and Buildings, provenance \u201cofficial\u201d, 511,862 rows, "
             "rowsUpdatedAt 2026 (data_as_of 2026-09-11T05:04:44 in returned records)."},
    {"id": 175, "title": "SF.gov / DBI \u00b7 Apply for a plumbing and mechanical permit",
     "url": "https://www.sf.gov/apply-plumbing-and-mechanical-permit", "kind": "government",
     "access": "page", "checkedAt": DATE,
     "note": "Official Department of Building Inspection service page, read directly this "
             "session. States that a permit is required before cutting into or replacing pipes "
             "\u2014particularly pipes that will be covered by a wall\u2014 points to the exemptions in "
             "San Francisco Plumbing Code Section 104.2, requires a City-registered licensed "
             "contractor for online applications, restricts owner-installer applications to "
             "stand-alone single-family dwellings, and requires inspection before pipes are "
             "covered."},
]

# --- 22 direct CSLB license detail reads (this session) --------------------
CSLB_READS = [
    (153, "900309", "West Cork Plumbing Inc"),
    (154, "966337", "Flow Masters Plumbing Inc"),
    (155, "947504", "Building Efficiency Inc"),
    (156, "998141", "Faherty Plumbing and Heating"),
    (157, "916617", "De Barra Plumbing"),
    (158, "859973", "Pro Plumbing"),
    (159, "885083", "Ros Plumbing LLC"),
    (160, "976543", "Moonlight Plumbing"),
    (161, "950265", "All-Point Solutions Plumbing Co"),
    (162, "812845", "B R Troika Incorporated dba Mr Rooter Plumbing"),
    (163, "898289", "Gorman Pipeline Inc"),
    (164, "1022789", "F C Company"),
    (165, "570753", "Ricky's Plumbing Company"),
    (166, "989225", "Parks Plumbing Inc"),
    (167, "820321", "Hegarty Plumbing"),
    (168, "665412", "Chen's Plumbing Inc"),
    (169, "837694", "Goodrich Plumbing Inc"),
    (170, "265709", "Ron Hogan Drywall"),
    (171, "1130530", "R S Dynamic Builders Inc"),
    (172, "839447", "Feng K Plumbing Co"),
    (173, "287477", "Asia Plumbing"),
    (174, "1057063", "Caledonia Plastering & Stucco Inc"),
]
for sid, num, who in CSLB_READS:
    SOURCES.append({
        "id": sid, "title": f"CSLB \u00b7 {num} \u00b7 {who}", "url": cslb(num),
        "kind": "government", "access": "page", "checkedAt": DATE,
        "note": "License detail page read directly on cslb.ca.gov on 2026-09-11. Page carries "
                "the CSLB disclaimer that a status check is database information only and that "
                "relevant data may not yet be entered."})

# --- directories, platforms and business sites ----------------------------
SOURCES += [
    {"id": 176, "title": "Yelp \u00b7 Outer Sunset \u201cDry Wall Repair\u201d results (indexed extract)",
     "url": "https://www.yelp.com/search?find_desc=Dry+Wall+Repair&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA",
     "kind": "directory", "access": "blocked-with-search-extract", "checkedAt": DATE,
     "note": "Indexed result page read through search extract; the full review corpus was not "
             "retrieved. Supplied SF Building Group and Mullican Remodeling. \u201cVerified "
             "License\u201d is a Yelp badge, not a CSLB record."},
    {"id": 177, "title": "Yelp \u00b7 Outer Sunset \u201cDrywall Installation\u201d results (indexed extract)",
     "url": "https://www.yelp.com/search?find_desc=Drywall+Installation&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA",
     "kind": "directory", "access": "blocked-with-search-extract", "checkedAt": DATE,
     "note": "Indexed result page. Contains a truncated ceiling-drywall review excerpt for "
             "Bernal Hill Drywall (applied to the pre-existing entry by the wave-6 patch, not "
             "double-counted here)."},
    {"id": 178, "title": "Yelp \u00b7 San Francisco \u201cdrywall repair service\u201d results (indexed extract)",
     "url": "https://www.yelp.com/search?find_desc=drywall+repair+service&find_loc=San+Francisco%2C+CA",
     "kind": "directory", "access": "blocked-with-search-extract", "checkedAt": DATE,
     "note": "Indexed result page; supplied NorthLine Drywall Repair, Rodas Drywall and "
             "Painting, and an unattributed Jose HandyMan Services excerpt that was REJECTED "
             "for the pre-existing entry (review text names a different person than the "
             "business \u2014 probable index text bleed)."},
    {"id": 179, "title": "Yelp \u00b7 San Francisco \u201cdrywall ceiling repair\u201d results (indexed extract)",
     "url": "https://www.yelp.com/search?find_desc=drywall+ceiling+repair&find_loc=San+Francisco%2C+CA",
     "kind": "directory", "access": "blocked-with-search-extract", "checkedAt": DATE,
     "note": "Indexed result page. Contains the truncated Bernal Hill ceiling-patch excerpt and "
             "a truncated Meticulous Handyman plaster-ceiling excerpt; both are applied to "
             "pre-existing entries by the wave-6 patch and are not double-counted here."},
    {"id": 180, "title": "Yelp \u00b7 drywall repair near-me index (indexed extract)",
     "url": "https://www.yelp.com/nearme/drywall-repair", "kind": "directory",
     "access": "blocked-with-search-extract", "checkedAt": DATE,
     "note": "Indexed near-me page listing review counts and stated service areas. Supplied "
             "Ezekiel's Drywall Services (San Jose) and JR Drywall (Emeryville); both are "
             "recorded as outside-area concerns."},
    {"id": 181, "title": "Thumbtack \u00b7 Caledonia Plastering & Stucco profile (indexed extract + page JSON-LD)",
     "url": "https://www.thumbtack.com/ca/san-francisco/drywall-repair/caledonia-plastering-stucco/service/281335206093636654",
     "kind": "platform", "access": "search-extract", "checkedAt": DATE,
     "note": "Indexed profile read through search extract. Page JSON-LD states "
             "addressLocality San Francisco, postalCode 94116, aggregateRating 4.875 from 56 "
             "reviews, and carries dated, named reviews used in this wave. Only the reviews "
             "actually present in the extract are retained; no complete corpus is claimed."},
    {"id": 182, "title": "Yelp \u00b7 Caledonia Plastering and Stucco business profile (indexed extract)",
     "url": "https://www.yelp.com/biz/caledonia-plastering-and-stucco-san-francisco-2",
     "kind": "directory", "access": "blocked-with-search-extract", "checkedAt": DATE,
     "note": "Indexed profile places the business at 1551 Judah St, San Francisco, CA 94122 and "
             "labels the neighbourhood \u201cOuter Sunset\u201d; owner listed as John C.; shows a Yelp "
             "\u201cVerified License\u201d badge (badge only, not regulator verification)."},
    {"id": 183, "title": "BBB \u00b7 Caledonia Plastering & Stucco Inc. profile (indexed extract)",
     "url": "https://www.bbb.org/us/ca/san-francisco/profile/insulation-contractors/caledonia-plastering-stucco-inc-1116-946248",
     "kind": "directory", "access": "search-extract", "checkedAt": DATE,
     "note": "Indexed BBB profile: 1551 Judah St, San Francisco, CA 94122-1717; NOT BBB "
             "Accredited; BBB records CSLB license 1057063 with expiration 8/31/2027; business "
             "started 2/24/2023; file opened 6/12/2023. BBB is a directory, not the regulator."},
    {"id": 184, "title": "BuildZoom \u00b7 Caledonia Plastering and Stucco (indexed extract)",
     "url": "https://www.buildzoom.com/contractor/caledonia-plastering-and-stucco",
     "kind": "directory", "access": "search-extract", "checkedAt": DATE,
     "note": "Third-party aggregator. Lists license #1057063, type Lathing And Plastering, "
             "status Active \u201cverified as of February 2026\u201d, employee John Martin Cullen, and "
             "reproduces SF DBI stucco permits tied to 1551 JUDAH STREET 94122. Treated as "
             "corroboration only; the CSLB page itself is the authority (source 174)."},
    {"id": 185, "title": "Yelp \u00b7 San Francisco stucco services results (indexed extract)",
     "url": "https://www.yelp.com/search?cflt=stucco&find_loc=San+Francisco,+CA",
     "kind": "directory", "access": "blocked-with-search-extract", "checkedAt": DATE,
     "note": "Indexed category page; supplied All About Plastering and Gray Lath and Plaster, "
             "and independently shows Caledonia at \u201c1551 Judah St \u00b7 Outer Sunset\u201d."},
    {"id": 186, "title": "Yelp \u00b7 San Francisco \u201cStucco Contractor\u201d results (indexed extract)",
     "url": "https://www.yelp.com/search?find_desc=Stucco+Contractor&find_loc=San+Francisco%2C+CA",
     "kind": "directory", "access": "blocked-with-search-extract", "checkedAt": DATE,
     "note": "Indexed result page; supplied Marcelino Plastering."},
    {"id": 187, "title": "Ron Hogan Drywall \u00b7 official San Francisco drywall page",
     "url": "https://ronhogandrywall.net/commercial-residential-drywall-contractor-san-francisco-ca/",
     "kind": "business", "access": "search-extract", "checkedAt": DATE,
     "note": "Company page located through search extract; not retrieved directly this pass. "
             "States CSLB #265709 and lists the Sunset District among neighbourhoods served. "
             "Marketing copy is a business claim, not independent proof of coverage."},
    {"id": 188, "title": "Bernal Hill Drywall \u00b7 official site",
     "url": "https://www.bernalhilldrywall.com/", "kind": "business",
     "access": "search-extract", "checkedAt": DATE,
     "note": "Company site located through search extract; not retrieved directly this pass. "
             "Footer states \u201cCALIFORNIA License #995163\u201d, which matches the CSLB record read "
             "directly this session (source 196). Used by the wave-6 patch to attach that "
             "license to the pre-existing Bernal Hill Drywall entry."},
    {"id": 189, "title": "New Line Drywall \u00b7 official site",
     "url": "https://newlinedrywall.com/", "kind": "business",
     "access": "search-extract", "checkedAt": DATE,
     "note": "Company site located through search extract; not retrieved directly this pass. "
             "Page JSON-LD lists areaServed including San Francisco and telephone "
             "+15107063145; copy describes patching walls or ceilings and hand-matching "
             "existing texture. No license number is published in the extract."},
    {"id": 190, "title": "RS Dynamic Builders \u00b7 San Francisco drywall repair services page",
     "url": "https://rsdynamicbuilders.com/drywall-repair-services-san-francisco/",
     "kind": "business", "access": "search-extract", "checkedAt": DATE,
     "note": "Company page located through search extract; not retrieved directly this pass. "
             "Describes ceiling drywall repair including water stains and sagging, water-damage "
             "ceiling repair, reinforcing lath and plaster in older homes, and a permit "
             "handling / code compliance section. Marketing copy only."},
    {"id": 191, "title": "RS Dynamic Builders \u00b7 About page (structured data)",
     "url": "https://rsdynamicbuilders.com/about/", "kind": "business",
     "access": "search-extract", "checkedAt": DATE,
     "note": "Page JSON-LD lists serviceArea including \u201cSunset\u201d and \u201cRichmond\u201d, aggregateRating "
             "5.0 from 5 reviews, and streetAddress \u201c123 Main Street\u201d, San Mateo 94401 \u2014 a "
             "placeholder-looking address that does not match the CSLB record."},
    {"id": 192, "title": "RS Dynamic Builders \u00b7 home page",
     "url": "https://rsdynamicbuilders.com/", "kind": "business",
     "access": "search-extract", "checkedAt": DATE,
     "note": "Company home page located through search extract. Publishes \u201cCSLB# 1130530\u201d, "
             "location San Mateo CA 94401 and phone +1 415 450 7338."},
    {"id": 193, "title": "Angi / HomeAdvisor \u00b7 San Francisco drywall repair pros (indexed extract)",
     "url": "https://www.homeadvisor.com/tloc/San-Francisco-CA/Drywall-Repair/",
     "kind": "directory", "access": "search-extract", "checkedAt": DATE,
     "note": "Indexed lead-generation page; supplied Dango Drywall Co, Corp and one customer "
             "excerpt. Lead-marketplace prescreening is not regulator verification."},
    {"id": 194, "title": "Angi / HomeAdvisor \u00b7 San Francisco drywall & plaster matching page (indexed extract)",
     "url": "https://www.homeadvisor.com/c.Drywall-Plaster.San_Francisco.CA.-12025.html",
     "kind": "directory", "access": "search-extract", "checkedAt": DATE,
     "note": "Indexed matching page. Named providers are hidden behind a quote form in the "
             "extract; only a popcorn-ceiling-removal customer excerpt was visible, and it is "
             "not attributable to a named business, so it produced NO wave-6 entry."},
    {"id": 195, "title": "Yelp \u00b7 Sunset District plumbing best-10 (indexed extract)",
     "url": "https://www.yelp.com/search?cflt=plumbing&find_loc=Sunset+District%2C+San+Francisco%2C+CA",
     "kind": "directory", "access": "blocked-with-search-extract", "checkedAt": DATE,
     "note": "Indexed category page for the Sunset District. Re-checked this session; used by "
             "the wave-6 patch to add one clearly-labelled business portfolio caption to a "
             "pre-existing entry. No new wave-6 business is drawn from it."},
    {"id": 196, "title": "CSLB \u00b7 995163 \u00b7 Bernal Hill Drywall Inc", "url": cslb("995163"),
     "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "License detail page read directly on cslb.ca.gov on 2026-09-11 and applied by "
             "the wave-6 patch to the pre-existing Bernal Hill Drywall entry rather than "
             "double-counted as a new record."},
]

SRC = {s["id"]: s for s in SOURCES}
CSLB_SRC = {num: sid for sid, num, _ in CSLB_READS}
CSLB_SRC["995163"] = 196

# --------------------------------------------------------------------------
# Direct CSLB reads, transcribed line by line from the pages named above.
# --------------------------------------------------------------------------
L = {
    "900309": dict(src=153, entity="WEST CORK PLUMBING INC",
                   addr="20 ROY CT, NOVATO, CA 94947", phone="(415) 845-3870",
                   status="active", expires="2027-08-31", classes=["C36"], etype="Corporation",
                   issued="07/17/2007", reissued="08/18/2009",
                   quote="WEST CORK PLUMBING INC \u00b7 20 ROY CT \u00b7 NOVATO, CA 94947 \u00b7 Business "
                         "Phone Number:(415) 845-3870 \u2014 Entity Corporation \u2014 Issue Date "
                         "07/17/2007 \u2014 Reissue Date 08/18/2009 \u2014 Expire Date 08/31/2027 \u2014 "
                         "\u201cThis license is current and active.\u201d \u2014 C36 - PLUMBING \u2014 Contractor's "
                         "Bond $25,000 eff 06/03/2024 \u2014 workers compensation with HARTFORD "
                         "CASUALTY INSURANCE COMPANY eff 05/08/2026 exp 05/08/2027 \u2014 Misc: "
                         "08/18/2009 LICENSE REISSUED TO ANOTHER ENTITY",
                   misc=["08/18/2009 - LICENSE REISSUED TO ANOTHER ENTITY"]),
    "966337": dict(src=154, entity="FLOW MASTERS PLUMBING INC",
                   addr="6169 MISSION ST, DALY CITY, CA 94014", phone="(415) 751-1933",
                   status="active", expires="2027-10-31", classes=["C36", "C16", "C20"],
                   etype="Corporation", issued="10/04/2011",
                   quote="FLOW MASTERS PLUMBING INC \u00b7 6169 MISSION ST \u00b7 DALY CITY, CA 94014 \u00b7 "
                         "Business Phone Number:(415) 751-1933 \u2014 Entity Corporation \u2014 Issue "
                         "Date 10/04/2011 \u2014 Expire Date 10/31/2027 \u2014 \u201cThis license is current "
                         "and active.\u201d \u2014 C36 - PLUMBING; C16 - FIRE PROTECTION; C20 - WARM-AIR "
                         "HEATING, VENTILATING AND AIR-CONDITIONING \u2014 Contractor's Bond $25,000 "
                         "eff 03/09/2025 \u2014 qualifying individual ALAN PATRICK MORAN \u2014 workers "
                         "compensation with SECURITY NATIONAL INSURANCE COMPANY eff 06/01/2026 "
                         "exp 06/01/2027",
                   misc=[]),
    "947504": dict(src=155, entity="BUILDING EFFICIENCY INC",
                   addr="2037 IRVING STREET, SUITE 213, SAN FRANCISCO, CA 94122",
                   phone="(415) 831-4535", status="active", expires="2028-05-31",
                   classes=["B", "C20", "C36", "C10"], etype="Corporation",
                   issued="05/18/2010",
                   quote="BUILDING EFFICIENCY INC \u00b7 2037 IRVING STREET \u00b7 SUITE 213 \u00b7 SAN "
                         "FRANCISCO, CA 94122 \u00b7 Business Phone Number:(415) 831-4535 \u2014 Entity "
                         "Corporation \u2014 Issue Date 05/18/2010 \u2014 Expire Date 05/31/2028 \u2014 "
                         "\u201cThis license is current and active.\u201d \u2014 B - GENERAL BUILDING; C20 - "
                         "WARM-AIR HEATING, VENTILATING AND AIR-CONDITIONING; C36 - PLUMBING; "
                         "C10 - ELECTRICAL \u2014 Certifications: ASB - ASBESTOS (For Bidding "
                         "Purposes Only) \u2014 Contractor's Bond $25,000 eff 01/01/2023 \u2014 workers "
                         "compensation with STATE COMPENSATION INSURANCE FUND eff 08/12/2014 "
                         "exp 08/12/2027; classification codes 55421 Sheet Metal Work-high "
                         "wage, 5479 Insulation Work, 51871 Plumbing-high wage",
                   misc=["12/14/2015 - CONTRACTOR HIS LETTER SENT"]),
    "998141": dict(src=156, entity="FAHERTY PLUMBING AND HEATING dba FAHERTY PLUMBING",
                   addr="4004 IRVING STREET, SAN FRANCISCO, CA 94122", phone="(415) 640-9626",
                   status="active", expires="2028-09-30", classes=["C36"], etype="Corporation",
                   issued="10/28/2014", reissued="09/10/2018",
                   quote="FAHERTY PLUMBING AND HEATING \u00b7 dba FAHERTY PLUMBING \u00b7 4004 IRVING "
                         "STREET \u00b7 SAN FRANCISCO, CA 94122 \u00b7 Business Phone Number:(415) "
                         "640-9626 \u2014 Entity Corporation \u2014 Issue Date 10/28/2014 \u2014 Reissue Date "
                         "09/10/2018 \u2014 Expire Date 09/30/2028 \u2014 \u201cThis license is current and "
                         "active.\u201d \u2014 C36 - PLUMBING \u2014 Contractor's Bond $25,000 eff 01/01/2023 "
                         "\u2014 qualifying individual DAVID GERALD FAHERTY \u2014 workers compensation "
                         "with MASSACHUSETTS BAY INSURANCE COMPANY eff 01/04/2026 exp "
                         "01/04/2027; classification code 51871 Plumbing-high wage",
                   misc=["09/10/2018 - LICENSE REISSUED TO ANOTHER ENTITY"]),
    "916617": dict(src=157, entity="DE BARRA PLUMBING",
                   addr="1511 39TH AVENUE, SAN FRANCISCO, CA 94122", phone="(415) 368-7992",
                   status="active", expires="2028-06-30", classes=["C36"],
                   etype="Sole Ownership", issued="06/03/2008",
                   quote="DE BARRA PLUMBING \u00b7 1511 39TH AVENUE \u00b7 SAN FRANCISCO, CA 94122 \u00b7 "
                         "Business Phone Number:(415) 368-7992 \u2014 Entity Sole Ownership \u2014 Issue "
                         "Date 06/03/2008 \u2014 Expire Date 06/30/2028 \u2014 \u201cThis license is current "
                         "and active.\u201d \u2014 C36 - PLUMBING \u2014 Contractor's Bond $25,000 with "
                         "NATIONWIDE MUTUAL INSURANCE COMPANY eff 02/12/2026 \u2014 workers "
                         "compensation with PIE INSURANCE COMPANY (THE) eff 02/23/2026 exp "
                         "02/23/2027; classification codes 51871 Plumbing-high wage, 51831 "
                         "Plumbing-low wage, 8810 Clerical Office Employees",
                   misc=[]),
    "859973": dict(src=158, entity="PRO PLUMBING",
                   addr="145 BARNEVELD AVE, SAN FRANCISCO, CA 94122", phone="(415) 994-3468",
                   status="expired", expires="2023-06-30", classes=["C36", "C16"],
                   etype="Sole Ownership", issued="06/04/2005",
                   quote="PRO PLUMBING \u00b7 145 BARNEVELD AVE \u00b7 SAN FRANCISCO, CA 94122 \u00b7 Business "
                         "Phone Number:(415) 994-3468 \u2014 Entity Sole Ownership \u2014 Issue Date "
                         "06/04/2005 \u2014 Expire Date 06/30/2023 \u2014 \u201cThis license is expired and "
                         "not able to contract at this time.\u201d \u2014 Additional status: needs a "
                         "contractors bond to renew or reactivate; may have a legal requirement "
                         "to meet; needs to meet workers compensation requirements \u2014 C36 - "
                         "PLUMBING; C16 - FIRE PROTECTION \u2014 Contractor's Bond $15,000 eff "
                         "01/01/2016 Cancellation Date 08/04/2017 \u2014 workers compensation "
                         "exempt, certified no employees, eff 06/22/2017 Cancellation Date "
                         "07/01/2019",
                   misc=["10/16/2023 - WC EXEMPT CANCELLED-LIC INACTIVATED"]),
    "885083": dict(src=159, entity="ROS PLUMBING LLC",
                   addr="1543 HILL ROAD, NOVATO, CA 94947", phone="(415) 505-2180",
                   status="active", expires="2027-02-28", classes=["C36", "C-4", "B"],
                   etype="Ltd Liability", issued="09/30/2006", reissued="02/13/2021",
                   quote="ROS PLUMBING LLC \u00b7 1543 HILL ROAD \u00b7 NOVATO, CA 94947 \u00b7 Business Phone "
                         "Number:(415) 505-2180 \u2014 Entity Ltd Liability \u2014 Issue Date 09/30/2006 "
                         "\u2014 Reissue Date 02/13/2021 \u2014 Expire Date 02/28/2027 \u2014 \u201cThis license is "
                         "current and active.\u201d \u2014 C36 - PLUMBING; C-4 - BOILER, HOT WATER "
                         "HEATING AND STEAM FITTING; B - GENERAL BUILDING \u2014 Contractor's Bond "
                         "$25,000 eff 04/08/2024 \u2014 LLC EMPLOYEE/WORKER BOND $100,000 eff "
                         "02/13/2021 \u2014 Liability Insurance Information: CUMIS SPECIALTY "
                         "INSURANCE COMPANY INC, Amount $1,000,000, eff 05/29/2026 exp "
                         "05/29/2027 \u2014 workers compensation with EVEREST PREMIER INSURANCE "
                         "COMPANY eff 02/04/2026 exp 02/04/2027",
                   misc=["02/13/2021 - LICENSE REISSUED TO ANOTHER ENTITY"]),
    "976543": dict(src=160, entity="MOONLIGHT PLUMBING",
                   addr="59164 WILMAR AVE, YUCCA VALLEY, CA 92284", phone="(415) 722-3623",
                   status="active", expires="2026-09-30", classes=["C36"],
                   etype="Sole Ownership", issued="09/12/2012",
                   quote="MOONLIGHT PLUMBING \u00b7 59164 WILMAR AVE \u00b7 YUCCA VALLEY, CA 92284 \u00b7 "
                         "Business Phone Number:(415) 722-3623 \u2014 Entity Sole Ownership \u2014 Issue "
                         "Date 09/12/2012 \u2014 Expire Date 09/30/2026 \u2014 \u201cThis license is current "
                         "and active.\u201d \u2014 C36 - PLUMBING \u2014 Contractor's Bond $25,000 eff "
                         "08/08/2023 \u2014 workers compensation exempt, certified no employees, "
                         "eff 08/11/2024",
                   misc=[]),
    "950265": dict(src=161, entity="ALL - POINT SOLUTIONS PLUMBING CO",
                   addr="1651 42ND AVENUE, SAN FRANCISCO, CA 94122", phone="(415) 818-2822",
                   status="suspended", expires="2028-07-31", classes=["C36"],
                   etype="Sole Ownership", issued="07/21/2010",
                   quote="ALL - POINT SOLUTIONS PLUMBING CO \u00b7 1651 42ND AVENUE \u00b7 SAN FRANCISCO, "
                         "CA 94122 \u00b7 Business Phone Number:(415) 818-2822 \u2014 Entity Sole "
                         "Ownership \u2014 Issue Date 07/21/2010 \u2014 Expire Date 07/31/2028 \u2014 "
                         "\u201cLicense is under suspension for the following reasons: License is "
                         "under Contractors Bond Suspension.\u201d \u2014 C36 - PLUMBING \u2014 Contractor's "
                         "Bond $25,000 with HUDSON INSURANCE COMPANY eff 01/01/2023 "
                         "Cancellation Date 09/01/2026 \u2014 workers compensation exempt, "
                         "certified no employees, eff 08/23/2026",
                   misc=[]),
    "812845": dict(src=162, entity="B R TROIKA INCORPORATED dba MR ROOTER PLUMBING",
                   addr="2341 JUDAH, SAN FRANCISCO, CA 94122", phone="(415) 520-1200",
                   status="expired", expires="2018-09-30", classes=["C36"],
                   etype="Corporation", issued="09/18/2002",
                   quote="B R TROIKA INCORPORATED \u00b7 dba MR ROOTER PLUMBING \u00b7 2341 JUDAH \u00b7 SAN "
                         "FRANCISCO, CA 94122 \u00b7 Business Phone Number:(415) 520-1200 \u2014 Entity "
                         "Corporation \u2014 Issue Date 09/18/2002 \u2014 Expire Date 09/30/2018 \u2014 "
                         "\u201cThis license is expired and not able to contract at this time.\u201d \u2014 "
                         "C36 - PLUMBING \u2014 Contractor's Bond $15,000 eff 03/14/2018 "
                         "Cancellation Date 05/10/2019 \u2014 workers compensation exempt, "
                         "certified no employees, eff 09/15/2016",
                   misc=[]),
    "898289": dict(src=163, entity="GORMAN PIPELINE INC",
                   addr="1518 27TH AVE, SAN FRANCISCO, CA 94122", phone="(415) 515-7713",
                   status="active", expires="2027-06-30", classes=["A"], etype="Corporation",
                   issued="06/11/2007",
                   quote="GORMAN PIPELINE INC \u00b7 1518 27TH AVE \u00b7 SAN FRANCISCO, CA 94122 \u00b7 "
                         "Business Phone Number:(415) 515-7713 \u2014 Entity Corporation \u2014 Issue "
                         "Date 06/11/2007 \u2014 Expire Date 06/30/2027 \u2014 \u201cThis license is current "
                         "and active.\u201d \u2014 A - GENERAL ENGINEERING (no C36 plumbing "
                         "classification shown) \u2014 Contractor's Bond $25,000 eff 01/01/2023 \u2014 "
                         "qualifying individual MARK OLIVER GORMAN \u2014 workers compensation with "
                         "STATE COMPENSATION INSURANCE FUND eff 12/01/2019 exp 12/01/2026; "
                         "classification codes 6307 Sewer Construction-low wage, 6308 Sewer "
                         "Construction-high wage, 8810 Clerical Office Employees",
                   misc=[]),
    "1022789": dict(src=164, entity="F C COMPANY",
                    addr="113 SAN DIEGO AVENUE, DALY CITY, CA 94014", phone="(415) 668-9423",
                    status="suspended", expires="2027-01-31", classes=["B", "C36"],
                    etype="Sole Ownership", issued="01/20/2017",
                    quote="F C COMPANY \u00b7 113 SAN DIEGO AVENUE \u00b7 DALY CITY, CA 94014 \u00b7 Business "
                          "Phone Number:(415) 668-9423 \u2014 Entity Sole Ownership \u2014 Issue Date "
                          "01/20/2017 \u2014 Expire Date 01/31/2027 \u2014 \u201cLicense is under suspension "
                          "for the following reasons: License is under Contractors Bond "
                          "Suspension.\u201d \u2014 B - GENERAL BUILDING; C36 - PLUMBING \u2014 Contractor's "
                          "Bond $25,000 with HUDSON INSURANCE COMPANY eff 01/01/2023 "
                          "Cancellation Date 09/01/2026 \u2014 workers compensation exempt, "
                          "certified no employees, eff 12/16/2024",
                    misc=[]),
    "570753": dict(src=165, entity="RICKY'S PLUMBING COMPANY",
                   addr="3550 CABRILLO STREET, SAN FRANCISCO, CA 94121",
                   phone="(415) 876-0333", status="canceled", expires="2005-06-30",
                   classes=["C36"], etype="Sole Ownership", issued="06/13/1989",
                   quote="RICKY'S PLUMBING COMPANY \u00b7 3550 CABRILLO STREET \u00b7 SAN FRANCISCO, CA "
                         "94121 \u00b7 Business Phone Number:(415) 876-0333 \u2014 Entity Sole Ownership "
                         "\u2014 Issue Date 06/13/1989 \u2014 Expire Date 06/30/2005 \u2014 \u201cThis license is "
                         "expired and not able to contract at this time.\u201d \u2014 Additional Status: "
                         "The license was canceled after expiration \u2014 C36 - PLUMBING \u2014 "
                         "Contractor's Bond $10,000 eff 01/01/2004 Cancellation Date "
                         "02/17/2005 \u2014 Misc: 09/16/2005 LICENSE CANCELLED PER REQUEST",
                   misc=["09/16/2005 - LICENSE CANCELLED PER REQUEST"]),
    "989225": dict(src=166, entity="PARKS PLUMBING INC",
                   addr="484 CULLEN DR, PACIFICA, CA 94044", phone="(415) 519-6695",
                   status="active", expires="2026-12-31", classes=["C36"], etype="Corporation",
                   issued="12/17/2013", reissued="12/01/2016",
                   quote="PARKS PLUMBING INC \u00b7 484 CULLEN DR \u00b7 PACIFICA, CA 94044 \u00b7 Business "
                         "Phone Number:(415) 519-6695 \u2014 Entity Corporation \u2014 Issue Date "
                         "12/17/2013 \u2014 Reissue Date 12/01/2016 \u2014 Expire Date 12/31/2026 \u2014 "
                         "\u201cThis license is current and active.\u201d \u2014 C36 - PLUMBING \u2014 "
                         "Contractor's Bond $25,000 eff 08/29/2025 \u2014 qualifying individual "
                         "WESLEY DAVIS PARKS \u2014 workers compensation with TECHNOLOGY INSURANCE "
                         "COMPANY INC eff 04/05/2026 exp 04/05/2027",
                   misc=[]),
    "820321": dict(src=167, entity="HEGARTY PLUMBING",
                   addr="P O BOX 27326, SAN FRANCISCO, CA 94127", phone="(415) 532-9255",
                   status="active", expires="2027-06-30", classes=["C36"],
                   etype="Sole Ownership", issued="06/02/2003",
                   quote="HEGARTY PLUMBING \u00b7 P O BOX 27326 \u00b7 SAN FRANCISCO, CA 94127 \u00b7 "
                         "Business Phone Number:(415) 532-9255 \u2014 Entity Sole Ownership \u2014 Issue "
                         "Date 06/02/2003 \u2014 Expire Date 06/30/2027 \u2014 \u201cThis license is current "
                         "and active.\u201d \u2014 C36 - PLUMBING \u2014 Contractor's Bond $25,000 eff "
                         "01/01/2023 \u2014 workers compensation with HARTFORD CASUALTY INSURANCE "
                         "COMPANY eff 04/08/2025 exp 04/08/2027; classification code 51871 "
                         "Plumbing-high wage",
                   misc=[]),
    "665412": dict(src=168, entity="CHEN'S PLUMBING INC",
                   addr="148 21ST AVE, SAN FRANCISCO, CA 94121-1206", phone="(415) 831-2661",
                   status="canceled", expires="2015-02-16", classes=["C16", "C36"],
                   etype="Corporation", issued="03/02/1993",
                   quote="CHEN'S PLUMBING INC \u00b7 148 21ST AVE \u00b7 SAN FRANCISCO, CA 94121-1206 \u00b7 "
                         "Business Phone Number:(415) 831-2661 \u2014 Entity Corporation \u2014 Issue "
                         "Date 03/02/1993 \u2014 Expire Date 02/16/2015 \u2014 \u201cThis license is canceled "
                         "and not able to contract.\u201d \u2014 C16 - FIRE PROTECTION; C36 - PLUMBING \u2014 "
                         "Contractor's Bond $12,500 eff 02/08/2012 Cancellation Date "
                         "04/04/2015 \u2014 Misc: 02/16/2015 SECRETARY OF STATE - DISSOLUTION",
                   misc=["02/16/2015 - SECRETARY OF STATE - DISSOLUTION"]),
    "837694": dict(src=169, entity="GOODRICH PLUMBING INC",
                   addr="265 KENSINGTON WAY, SAN FRANCISCO, CA 94127", phone="(415) 661-9138",
                   status="canceled", expires="2025-02-11", classes=["C36"],
                   etype="Corporation", issued="05/05/2004",
                   quote="GOODRICH PLUMBING INC \u00b7 265 KENSINGTON WAY \u00b7 SAN FRANCISCO, CA 94127 "
                         "\u00b7 Business Phone Number:(415) 661-9138 \u2014 Entity Corporation \u2014 Issue "
                         "Date 05/05/2004 \u2014 Expire Date 02/11/2025 \u2014 \u201cThis license is canceled "
                         "and not able to contract.\u201d \u2014 C36 - PLUMBING \u2014 Contractor's Bond "
                         "$25,000 eff 01/01/2023 Cancellation Date 04/04/2025 \u2014 workers "
                         "compensation with STATE COMPENSATION INSURANCE FUND eff 08/17/2012 "
                         "Cancellation Date 01/04/2025 \u2014 Misc: 02/11/2025 LICENSE CANCELED PER "
                         "REQUEST; 02/11/2025 SECRETARY OF STATE - DISSOLUTION",
                   misc=["02/11/2025 - LICENSE CANCELED PER REQUEST",
                         "02/11/2025 - SECRETARY OF STATE - DISSOLUTION"]),
    "265709": dict(src=170, entity="RON HOGAN DRYWALL",
                   addr="2380 PALMER CIRCLE, FAIRFIELD, CA 94534", phone="(925) 791-9099",
                   status="active", expires="2026-11-30", classes=["C-9"],
                   etype="Sole Ownership", issued="10/20/1970", reissued="11/17/2022",
                   quote="RON HOGAN DRYWALL \u00b7 2380 PALMER CIRCLE \u00b7 FAIRFIELD, CA 94534 \u00b7 "
                         "Business Phone Number:(925) 791-9099 \u2014 Entity Sole Ownership \u2014 Issue "
                         "Date 10/20/1970 \u2014 Reissue Date 11/17/2022 \u2014 Expire Date 11/30/2026 "
                         "\u2014 \u201cThis license is current and active.\u201d \u2014 C-9 - DRYWALL \u2014 "
                         "Contractor's Bond $25,000 eff 07/18/2025 \u2014 workers compensation with "
                         "STATE COMPENSATION INSURANCE FUND eff 02/12/2025 exp 02/12/2027; "
                         "classification codes 5447 Wallboard Installation-high wage, 5446 "
                         "Wallboard Installation-low wage \u2014 Misc: 11/04/2019 LICENSE CANCELED "
                         "PER REQUEST",
                   misc=["08/02/2004 - (SON) AUTH TO CONTINUE TIL (8-2-05)",
                         "01/31/2005 - LICENSE REISSUED TO ANOTHER ENTITY",
                         "11/04/2019 - LICENSE CANCELED PER REQUEST"]),
    "1130530": dict(src=171, entity="R S DYNAMIC BUILDERS INC",
                    addr="909 OCEAN VIEW AVE, SAN MATEO, CA 94401", phone="(650) 918-2317",
                    status="active", expires="2026-12-31", classes=["B"], etype="Corporation",
                    issued="12/16/2024",
                    quote="R S DYNAMIC BUILDERS INC \u00b7 909 OCEAN VIEW AVE \u00b7 SAN MATEO, CA 94401 "
                          "\u00b7 Business Phone Number:(650) 918-2317 \u2014 Entity Corporation \u2014 Issue "
                          "Date 12/16/2024 \u2014 Expire Date 12/31/2026 \u2014 \u201cThis license is current "
                          "and active.\u201d \u2014 B - GENERAL BUILDING (no C36 and no C-9 shown) \u2014 "
                          "Contractor's Bond $25,000 eff 12/03/2024 \u2014 qualifying individual "
                          "KAMALJIT SINGH \u2014 workers compensation exempt, certified no employees, "
                          "eff 12/11/2024",
                    misc=[]),
    "839447": dict(src=172, entity="FENG K PLUMBING CO",
                   addr="1654 23RD AVENUE, SAN FRANCISCO, CA 94122", phone="(415) 939-8822",
                   status="active", expires="2028-05-31", classes=["C36"],
                   etype="Sole Ownership", issued="05/28/2004",
                   quote="FENG K PLUMBING CO \u00b7 1654 23RD AVENUE \u00b7 SAN FRANCISCO, CA 94122 \u00b7 "
                         "Business Phone Number:(415) 939-8822 \u2014 Entity Sole Ownership \u2014 Issue "
                         "Date 05/28/2004 \u2014 Expire Date 05/31/2028 \u2014 \u201cThis license is current "
                         "and active.\u201d \u2014 C36 - PLUMBING \u2014 Contractor's Bond $25,000 with "
                         "ATLANTIC SPECIALTY INSURANCE COMPANY eff 09/01/2026 \u2014 workers "
                         "compensation exempt, certified no employees, eff 05/11/2026",
                   misc=[]),
    "287477": dict(src=173, entity="ASIA PLUMBING",
                   addr="1354 31ST AVE, SAN FRANCISCO, CA 94122", phone="(415) 731-8085",
                   status="expired", expires="2014-05-31", classes=["C16", "C36"],
                   etype="Partnership", issued="10/01/1973",
                   quote="ASIA PLUMBING \u00b7 1354 31ST AVE \u00b7 SAN FRANCISCO, CA 94122 \u00b7 Business "
                         "Phone Number:(415) 731-8085 \u2014 Entity Partnership \u2014 Issue Date "
                         "10/01/1973 \u2014 Expire Date 05/31/2014 \u2014 \u201cThis license is expired and "
                         "not able to contract at this time.\u201d \u2014 C16 - FIRE PROTECTION; C36 - "
                         "PLUMBING \u2014 Contractor's Bond $12,500 eff 06/20/2011 Cancellation "
                         "Date 07/24/2014 \u2014 workers compensation with MARKEL INSURANCE COMPANY "
                         "eff 02/01/2014 exp 02/01/2015",
                   misc=[]),
    "1057063": dict(src=174, entity="CALEDONIA PLASTERING & STUCCO INC",
                    addr="1551 JUDAH STREET, SAN FRANCISCO, CA 94122", phone="(415) 685-9910",
                    status="active", expires="2027-08-31", classes=["C35"],
                    etype="Corporation", issued="08/14/2019",
                    quote="CALEDONIA PLASTERING & STUCCO INC \u00b7 1551 JUDAH STREET \u00b7 SAN "
                          "FRANCISCO, CA 94122 \u00b7 Business Phone Number:(415) 685-9910 \u2014 Entity "
                          "Corporation \u2014 Issue Date 08/14/2019 \u2014 Expire Date 08/31/2027 \u2014 "
                          "\u201cThis license is current and active.\u201d \u2014 C35 - LATHING AND PLASTERING "
                          "\u2014 Contractor's Bond $25,000 with NORTH RIVER INSURANCE COMPANY "
                          "(THE) eff 07/22/2024 \u2014 qualifying individual JOHN MARTIN CULLEN \u2014 "
                          "workers compensation with AMERICAN CASUALTY COMPANY OF READING PA "
                          "eff 06/12/2026 exp 06/12/2027; classification codes 5484 "
                          "Plastering/Stucco Work-low wage, 5485 Plastering/Stucco Work-high "
                          "wage",
                    misc=[]),
    "995163": dict(src=196, entity="BERNAL HILL DRYWALL INC",
                   addr="720 ANDERSON ST, SAN FRANCISCO, CA 94110", phone="(415) 533-8274",
                   status="active", expires="2028-07-31", classes=["C-9", "B"],
                   etype="Corporation", issued="07/28/2014",
                   quote="BERNAL HILL DRYWALL INC \u00b7 720 ANDERSON ST \u00b7 SAN FRANCISCO, CA 94110 \u00b7 "
                         "Business Phone Number:(415) 533-8274 \u2014 Entity Corporation \u2014 Issue "
                         "Date 07/28/2014 \u2014 Expire Date 07/31/2028 \u2014 \u201cThis license is current "
                         "and active.\u201d \u2014 C-9 - DRYWALL; B - GENERAL BUILDING \u2014 Contractor's "
                         "Bond $25,000 eff 03/29/2023 \u2014 qualifying individual JERRY FRED "
                         "CALDERON \u2014 workers compensation with ENDURANCE ASSURANCE CORPORATION "
                         "eff 03/10/2026 exp 03/10/2027; classification code 5447 Wallboard "
                         "Installation-high wage",
                   misc=[]),
}

# --------------------------------------------------------------------------
# Official SF DBI registry rows, transcribed verbatim from sources 150 / 151.
# --------------------------------------------------------------------------
REG = {
    "West Cork Plumbing": dict(src=150, lic="900309", addr="1854 39th Av", zip="94122-0000",
                               phone=None, permits=523),
    "Flow Masters Plumbing Inc": dict(src=150, lic="966337", addr="1554 45th Avenue",
                                      zip="94122-0000", phone=None, permits=311),
    "Building Efficiency Inc": dict(src=150, lic="947504", addr="2037 Irving Street",
                                    zip="94122-0000", phone="4158314535", permits=252),
    "Faherty Plumbing": dict(src=150, lic="998141", addr="1295 41st Av", zip="94122-0000",
                             phone="4156409626", permits=176),
    "De Barra Plumbing": dict(src=150, lic="916617", addr="1511 39th Av", zip="94122-0000",
                              phone=None, permits=169),
    "Pro Plumbing": dict(src=150, lic="859973", addr="1814 40th Av", zip="94122-0000",
                         phone="4152908462", permits=239),
    "Ros Plumbing": dict(src=150, lic="885083", addr="1817 26th Av", zip="94122-0000",
                         phone=None, permits=156),
    "Moonlight Plumbing": dict(src=150, lic="976543", addr="1406 25th Av", zip="94122-0000",
                               phone=None, permits=123),
    "All Point Solutions Plumbing Co.": dict(src=150, lic="950265", addr="1651 42nd Av",
                                             zip="94122-0000", phone="4088814686", permits=114),
    "B R Troika Incorporated/Mr R": dict(src=150, lic="812845", addr="2801 Judah St",
                                         zip="94122-0000", phone="415-520-1200", permits=159),
    "Br Troika Inc. Dba Mr Rooter Plumbing": dict(src=150, lic="812845", addr="2801 Judah St",
                                                  zip="94122-0000", phone="4155201200",
                                                  permits=142),
    "Gorman Pipeline Inc": dict(src=150, lic="898289", addr="1518 27th Av", zip="94122-0000",
                                phone="4155157713", permits=239),
    "F C Company": dict(src=150, lic="1022789", addr="3638 Noriega St", zip="94122-0000",
                        phone="4159942499", permits=107),
    "Ricky's Plumbing Co": dict(src=150, lic="570753", addr="2727 Irving St", zip="94122",
                                phone="415-731-9766", permits=183),
    "Parks Plumbing Inc": dict(src=151, lic="989225", addr="2301 45th Av", zip="94116-0000",
                               phone=None, permits=159),
    "Hegarty Plumbing": dict(src=151, lic="820321", addr="2451 28th Av", zip="94116-0000",
                             phone="415-235-0119", permits=129),
    "Chen's Plumbing Inc": dict(src=151, lic="665412", addr="2127 - 34th Avenue",
                                zip="94116", phone="415-661-1758", permits=223),
    "Goodrich Plumbing Inc": dict(src=150, lic="837694", addr="1412 11th Av", zip="94122-0000",
                                  phone="4156612382", permits=233),
    "Ron Hogan Drywall": None,
    "R S Dynamic Builders Inc": None,
    "Caledonia Plastering & Stucco Inc": None,
    "Feng K. Plumbing Corp.": dict(src=150, lic="839447", addr="1654 23rd Av",
                                   zip="94122-0000", phone="4154180185", permits=344),
    "Feng K Plumbing Co": dict(src=150, lic="839447", addr="1654 23rd Av", zip="94122-0000",
                               phone="4157565869", permits=97),
    "Asia Plumbing": dict(src=150, lic="287477", addr="1354 31st Avenue *", zip="94122",
                          phone="415-731-8085", permits=280),
    "Ocean Air Heating": dict(src=150, lic="968927", addr="1859 42nd Av", zip="94122-0000",
                              phone=None, permits=244),
    "Bill Bragg Plumbing": dict(src=150, lic="440780", addr="Po Box 22073", zip="94122",
                                phone="415-661-1705", permits=234),
    "C T Construction & Plumb": dict(src=150, lic="533324", addr="1847  48th Av",
                                     zip="94122", phone="4152037178", permits=234),
    "Francis John Burke": dict(src=150, lic="762214", addr="2437 Ortega St", zip="94122-0000",
                               phone="4153078198", permits=175),
    "Hawk N Lee Co": dict(src=150, lic="324708", addr="1609  Noriega St", zip="94122",
                          phone="4156816325", permits=154),
    "Ren Lei Construction Co": dict(src=150, lic="635360", addr="750 Lawton St",
                                    zip="94122-0000", phone="4152381202", permits=153),
    "Abe's Plumbing": dict(src=150, lic="439862", addr="Po Box 22153", zip="94122",
                           phone="415-664-3939", permits=148),
    "City Plumbing Company": dict(src=150, lic="792165", addr="1214 40th Av", zip="94122-0000",
                                phone=None, permits=79),
    "Best Plumbing Choice": dict(src=151, lic="738608", addr="2138 17th Av", zip="94116-0000",
                                 phone="4157401940", permits=422),
    "O M P P Inc.": dict(src=151, lic="691287", addr="633 Taraval Street *", zip="94116",
                         phone="415-661-2050", permits=323),
    "L R Plumbing": dict(src=151, lic="771776", addr="2162 19th Av", zip="94116-0000",
                         phone="4153705325", permits=289),
    "Yao Star Construction": dict(src=151, lic="969667", addr="2223 42nd Avenue",
                                  zip="94116-0000", phone="4159879555", permits=240),
    "L C Plumbing & Fire Protection Inc": dict(src=151, lic="973837", addr="2470 27th Avenue",
                                               zip="94116-0000", phone="4158127596",
                                               permits=215),
    "J A Plumbing Inc": dict(src=151, lic="845259", addr="3444 Ulloa St", zip="94116-0000",
                             phone="4155665003", permits=173),
    "F - 1 Plumbing Services": dict(src=151, lic="801428", addr="2186 46th Av",
                                    zip="94116-0000", phone="4153055872", permits=152),
    "Excellent Plumbing Co": dict(src=151, lic="633153", addr="1355 33rd Av", zip="94116",
                                  phone="4158198992", permits=151),
}


def reg_excerpt(name):
    r = REG[name]
    if r is None:
        return None
    parts = [f'firm_name "{name}"', f'license_number "{r["lic"]}"', f'address "{r["addr"]}"',
             'city "San Francisco"', f'zipcode "{r["zip"]}"']
    if r["phone"]:
        parts.append(f'phone "{r["phone"]}"')
    parts.append(f'permit rows {r["permits"]}')
    return "; ".join(parts)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def gaps_for(trade):
    base = [
        "No exact seized bathtub-overflow trip-lever extraction outcome was verified for this "
        "business.",
        "On-site feasibility, written repair-first scope and applicable insurance are not "
        "established by this research.",
    ]
    if trade == "plumbing":
        base.append("Registry and license records prove legal identity and classification at a "
                    "recorded date; they never prove current dispatch to the Outer Sunset or "
                    "availability.")
    elif trade in ("drywall", "plaster", "finish"):
        base.append("Finish-trade records do not establish authority to perform regulated "
                    "plumbing; a licensed C-36 plumber must own any pipe work.")
    else:
        base.append("Multi-trade scope does not establish that this business will self-perform "
                    "both the plumbing and the ceiling/finish work under one contract.")
    return base


BUSINESSES = []
REVIEWS = []


def add(b):
    b.setdefault("platformLinks", [])
    b.setdefault("flags", [])
    b.setdefault("reviewIds", [])
    b["exactMatch"] = False
    b["master"] = False
    b["checkedAt"] = DATE
    b["status"] = b.get("status", "research")
    assert len(b["gaps"]) >= 2, b["id"]
    assert b["claims"] and b["claims"][0]["field"] == "Discovery", b["id"]
    BUSINESSES.append(b)


def norm_phone(p):
    """Normalise the CSLB-published '(415) 845-3870' form to '415-845-3870' so the
    site's tel: link is well formed. Digits and order are unchanged; the raw
    CSLB string is still preserved verbatim in the supporting excerpt."""
    if not p:
        return None
    return p.replace("(", "").replace(") ", "-").replace(") ", "-").strip()


def lic_obj(num):
    d = L[num]
    return {"number": num, "status": d["status"], "entity": d["entity"], "expires": d["expires"],
            "classes": d["classes"], "source": d["src"], "checkedAt": DATE}


# ==========================================================================
# GROUP A - 22 records carrying a CSLB page read directly this session.
# ==========================================================================
A = [
    # (name, lic, trade, area, priority, extra_claims, flags, rationale, nextStep)
    dict(name="Building Efficiency Inc", lic="947504", trade="multi-trade", area="outer",
         priority=7,
         areaText="CSLB itself records the business address as 2037 Irving Street, Suite 213, "
                  "San Francisco, CA 94122 \u2014 an Outer Sunset address held by the regulator, "
                  "not a marketing claim. The SF DBI registry independently records the same "
                  "firm at 2037 Irving Street with 252 permit rows.",
         extra=[dict(field="Registry", text="Official SF DBI plumbing-permit registry records "
                                            "this firm at 2037 Irving Street, 94122, with 252 "
                                            "permit rows \u2014 independent government corroboration "
                                            "of the CSLB address.", source=150,
                     excerpt=reg_excerpt("Building Efficiency Inc"))],
         flags=[],
         rationale="The only wave-6 record whose CSLB page shows a single corporation holding "
                   "B (General Building), C36 (Plumbing), C10 (Electrical) and C20 (HVAC) at an "
                   "Outer Sunset address, plus an ASB asbestos certification for bidding. That "
                   "combination is the closest credential match found to a job that may need "
                   "pipe work, a ceiling opening and a finish rebuild under one responsible "
                   "entity.",
         nextStep="Ask whether one contract covers the plumbing repair, ceiling opening, patch "
                  "and access panel, and which trade classification each part is billed under. "
                  "Request the entity name on the contract match BUILDING EFFICIENCY INC."),
    dict(name="Faherty Plumbing and Heating", lic="998141", trade="plumbing", area="outer",
         priority=8,
         areaText="CSLB records the business address as 4004 Irving Street, San Francisco, CA "
                  "94122 \u2014 an Outer Sunset address held by the regulator. The SF DBI registry "
                  "records the firm at 1295 41st Av, 94122, with 176 permit rows.",
         extra=[dict(field="Registry", text="Official SF DBI plumbing-permit registry records "
                                            "this firm at 1295 41st Av, 94122 with 176 permit "
                                            "rows and the same phone number the CSLB page "
                                            "publishes.", source=150,
                     excerpt=reg_excerpt("Faherty Plumbing"))],
         flags=[],
         rationale="Active C-36 corporation whose regulator-held address is on Irving Street in "
                   "the Outer Sunset, with a workers-compensation policy classified 51871 "
                   "Plumbing-high wage \u2014 evidence of employed plumbers rather than a no-employee "
                   "exemption. Longest expiry horizon in wave 6 (09/30/2028).",
         nextStep="Ask directly whether they have freed a seized tub trip-lever linkage in a "
                  "1940s galvanized system, and what access route they would try first."),
    dict(name="De Barra Plumbing", lic="916617", trade="plumbing", area="outer", priority=9,
         areaText="CSLB records the business address as 1511 39th Avenue, San Francisco, CA "
                  "94122 \u2014 an Outer Sunset address held by the regulator, matching the SF DBI "
                  "registry row at 1511 39th Av with 169 permit rows.",
         extra=[dict(field="Registry", text="Official SF DBI plumbing-permit registry records "
                                            "the identical 1511 39th Av, 94122 address with 169 "
                                            "permit rows.", source=150,
                     excerpt=reg_excerpt("De Barra Plumbing"))],
         flags=[],
         rationale="Active C-36 sole ownership at a regulator-held Outer Sunset address. Bond "
                   "effective 02/12/2026 and workers compensation effective 02/23/2026 are both "
                   "recent, and the workers-compensation classification list includes plumbing "
                   "high-wage, low-wage and clerical codes \u2014 consistent with a staffed local "
                   "shop. Sole ownership means one named individual is contractually "
                   "responsible.",
         nextStep="Confirm who physically attends the diagnostic visit and that the contracting "
                  "entity on any agreement is DE BARRA PLUMBING under license 916617."),
    dict(name="Caledonia Plastering & Stucco Inc", lic="1057063", trade="plaster", area="outer",
         priority=6,
         areaText="CSLB records the business address as 1551 Judah Street, San Francisco, CA "
                  "94122. Yelp's indexed profile labels the same address \u201cOuter Sunset\u201d, and "
                  "BBB records 1551 Judah St, San Francisco, CA 94122-1717.",
         extra=[
             dict(field="Registry cross-check", text="BBB records CSLB license 1057063 with "
                                                     "expiration 8/31/2027 for this business \u2014 "
                                                     "the same number and expiry read directly "
                                                     "on CSLB. BBB is a directory, not the "
                                                     "regulator; agreement between the two is "
                                                     "corroboration of identity only.",
                  source=183, excerpt="BBB records show a license number of 1057063 for this "
                                      "business, issued by Contractors State License Board. The "
                                      "expiration date of this license is 8/31/2027"),
             dict(field="Third-party aggregator", text="BuildZoom lists license #1057063, type "
                                                       "Lathing And Plastering, status Active "
                                                       "\u201cverified as of February 2026\u201d, employee "
                                                       "John Martin Cullen, and reproduces SF DBI "
                                                       "stucco permits tied to 1551 JUDAH STREET "
                                                       "94122. Aggregator data is corroboration "
                                                       "only.", source=184,
                  excerpt="Caledonia Plastering and Stucco, 1551 Judah St, San Francisco, CA "
                          "(Employee: John Martin Cullen) holds a Lathing And Plastering license "
                          "according to the California license board \u2026 License # 1057063 \u00b7 "
                          "Status Active"),
             dict(field="Drywall scope", text="Thumbtack's indexed profile places the business "
                                              "in San Francisco (postal code 94116 in page "
                                              "structured data) with an aggregate rating of "
                                              "4.875 across 56 reviews, and lists the service "
                                              "detail \u201cRepair / Touchup \u2022 Wall(s) \u2022 Ceiling(s) "
                                              "\u2022 Wood lath\u201d.", source=181,
                  excerpt="Details: Repair / Touchup \u2022 Wall(s) \u2022 Ceiling(s) \u2022 Wood lath \u2026 "
                          "\"addressLocality\":\"San Francisco\",\"postalCode\":\"94116\" \u2026 "
                          "\"aggregateRating\":{\"ratingValue\":4.875,\"reviewCount\":56}"),
         ],
         flags=[dict(level="discrepancy",
                    text="Address/ZIP discrepancy across sources: CSLB and Yelp record 1551 "
                         "Judah Street with ZIP 94122 (Outer Sunset), while the Thumbtack "
                         "profile's own structured data records postal code 94116 (Parkside). "
                         "Same street address, different ZIP. Not evidence of wrongdoing; "
                         "confirm the contracting address in writing.",
                    sources=[174, 182, 181]),
                dict(level="notice",
                    text="Classification is C35 (Lathing and Plastering) only. The CSLB page "
                         "shows no C-9 drywall and no C36 plumbing classification, so this "
                         "business cannot lawfully self-perform the plumbing portion and a "
                         "drywall-only patch may fall outside its classification.",
                    sources=[174])],
         rationale="The strongest finish-side match found in six waves: a regulator-verified "
                   "active C35 lathing-and-plastering corporation at a 94122 Judah Street "
                   "address that Yelp labels Outer Sunset, with named, dated Thumbtack reviews "
                   "describing ceiling-hole repair, veneer plaster over newly drywalled "
                   "ceilings, and lath-and-plaster work that \u201cpass the city inspection with no "
                   "problems\u201d. Correct trade for a 1940 building whose ceiling below may be "
                   "lath and plaster rather than drywall.",
         nextStep="Ask whether the ceiling below the tub is lath and plaster or drywall, whether "
                  "they install a framed access panel as part of the patch, and whether they "
                  "will coordinate behind a licensed C-36 plumber."),
    dict(name="Feng K Plumbing Co", lic="839447", trade="plumbing", area="outer",
         areaText="CSLB records the business address as 1654 23rd Avenue, San Francisco, CA "
                  "94122 \u2014 an Outer Sunset address held by the regulator. The SF DBI registry "
                  "records the same firm at 1654 23rd Av with 344 permit rows under the name "
                  "\u201cFeng K. Plumbing Corp.\u201d and 97 further rows as \u201cFeng K Plumbing Co\u201d.",
         extra=[dict(field="Registry", text="Official SF DBI plumbing-permit registry records "
                                            "this firm at 1654 23rd Av, 94122 with 344 permit "
                                            "rows \u2014 the fourth-highest count in that ZIP.",
                     source=150, excerpt=reg_excerpt("Feng K. Plumbing Corp."))],
         flags=[dict(level="discrepancy",
                    text="Entity-type and name mismatch: the registry row reads \u201cFeng K. "
                         "Plumbing Corp.\u201d while CSLB records \u201cFENG K PLUMBING CO\u201d as a Sole "
                         "Ownership under the same license number 839447. Confirm the exact "
                         "legal entity before signing anything.",
                    sources=[150, 172]),
                dict(level="discrepancy",
                    text="Three different published phone numbers for one license: registry rows "
                         "show 4154180185 and 4157565869, while CSLB publishes (415) 939-8822. "
                         "Use the CSLB number as the record of authority and confirm the others "
                         "verbally.",
                    sources=[150, 172]),
                dict(level="gap",
                    text="Workers compensation is exempt on a certified no-employees basis "
                         "(effective 05/11/2026). If no employees are covered, confirm in "
                         "writing who performs the work and how liability is insured.",
                    sources=[172])],
         rationale="Active C-36 sole ownership at a regulator-held Outer Sunset address with a "
                   "very high registry permit count and a contractor's bond effective "
                   "09/01/2026 \u2014 the freshest bond in wave 6. Held back from the call order by "
                   "the entity-name, phone and no-employee discrepancies above.",
         nextStep="Resolve the legal entity name and current phone with CSLB in hand before "
                  "requesting a diagnostic visit."),
    dict(name="West Cork Plumbing Inc", lic="900309", trade="plumbing", area="outside",
         areaText="The official SF DBI registry records \u201cWest Cork Plumbing\u201d at 1854 39th Av, "
                  "San Francisco 94122 with 523 permit rows \u2014 the highest count of any firm in "
                  "that ZIP. CSLB now records the business address as 20 Roy Ct, Novato, CA "
                  "94947, so Outer Sunset dispatch is unconfirmed.",
         extra=[dict(field="Registry", text="Official SF DBI plumbing-permit registry records "
                                            "this firm at an Outer Sunset address (1854 39th Av, "
                                            "94122) with 523 permit rows, more than any other "
                                            "firm in that ZIP.", source=150,
                     excerpt=reg_excerpt("West Cork Plumbing"))],
         flags=[dict(level="notice",
                    text="Address moved out of San Francisco: registry shows 1854 39th Av "
                         "(94122); CSLB now shows 20 Roy Ct, Novato (94947). CSLB also records "
                         "\u201c08/18/2009 - LICENSE REISSUED TO ANOTHER ENTITY\u201d. A long Outer "
                         "Sunset permit history does not establish present local dispatch.",
                    sources=[150, 153])],
         rationale="Active C-36 corporation with the deepest Outer Sunset plumbing-permit "
                   "history found in the official registry (523 rows), but its regulator-held "
                   "address is now in Novato.",
         nextStep="Ask whether the firm still dispatches to 94122 and which entity signs the "
                  "contract."),
    dict(name="Flow Masters Plumbing Inc", lic="966337", trade="plumbing", area="outside",
         areaText="Registry records \u201cFlow Masters Plumbing Inc\u201d at 1554 45th Avenue, San "
                  "Francisco 94122 with 311 permit rows. CSLB now records the business address "
                  "as 6169 Mission St, Daly City, CA 94014.",
         extra=[dict(field="Registry", text="Official SF DBI registry records an Outer Sunset "
                                            "address (1554 45th Avenue, 94122) with 311 permit "
                                            "rows.", source=150,
                     excerpt=reg_excerpt("Flow Masters Plumbing Inc"))],
         flags=[dict(level="notice",
                    text="Address moved out of San Francisco: registry 1554 45th Avenue (94122) "
                         "versus CSLB 6169 Mission St, Daly City (94014). CSLB also notes that "
                         "personnel listed on this license are listed on other licenses.",
                    sources=[150, 154])],
         rationale="Active corporation holding C36 plus C16 (fire protection) and C20 (HVAC) "
                   "with an Outer Sunset permit history, now based in Daly City.",
         nextStep="Confirm current dispatch to 94122 and whether the plumbing work is "
                  "self-performed under C36."),
    dict(name="Ros Plumbing LLC", lic="885083", trade="plumbing", area="outside",
         areaText="Registry records \u201cRos Plumbing\u201d at 1817 26th Av, San Francisco 94122 with "
                  "156 permit rows. CSLB now records 1543 Hill Road, Novato, CA 94947.",
         extra=[dict(field="Registry", text="Official SF DBI registry records an Outer Sunset "
                                            "address (1817 26th Av, 94122) with 156 permit rows.",
                     source=150, excerpt=reg_excerpt("Ros Plumbing"))],
         flags=[dict(level="notice",
                    text="Address moved out of San Francisco (registry 94122 versus CSLB "
                         "Novato 94947), and CSLB records \u201c02/13/2021 - LICENSE REISSUED TO "
                         "ANOTHER ENTITY\u201d, so historic registry rows may predate the current "
                         "LLC.", sources=[150, 159])],
         rationale="The only wave-6 CSLB page that publishes a Liability Insurance Information "
                   "block: $1,000,000 with CUMIS SPECIALTY INSURANCE COMPANY INC, effective "
                   "05/29/2026, expiring 05/29/2027. Also holds C36, C-4 (boiler/hot-water "
                   "heating) and B (General Building) plus a $100,000 LLC employee/worker bond. "
                   "Recorded liability cover is directly relevant where a ceiling below an "
                   "occupied unit will be opened.",
         nextStep="Ask for a certificate of insurance naming the property, and confirm whether "
                  "the B classification is used for the ceiling rebuild."),
    dict(name="Parks Plumbing Inc", lic="989225", trade="plumbing", area="outside",
         areaText="Registry records \u201cParks Plumbing Inc\u201d at 2301 45th Av, San Francisco 94116 "
                  "(Parkside, adjacent to the Outer Sunset) with 159 permit rows. CSLB now "
                  "records 484 Cullen Dr, Pacifica, CA 94044.",
         extra=[dict(field="Registry", text="Official SF DBI registry records a 94116 address "
                                            "(2301 45th Av) with 159 permit rows.", source=151,
                     excerpt=reg_excerpt("Parks Plumbing Inc"))],
         flags=[dict(level="gap",
                    text="License expires 12/31/2026 \u2014 inside four months of this snapshot. "
                         "Recheck CSLB status immediately before any booking.",
                    sources=[166])],
         rationale="Active C-36 corporation with a Parkside permit history and current "
                   "workers-compensation cover, now based in Pacifica.",
         nextStep="Recheck the license in December 2026 and confirm 94122 dispatch."),
    dict(name="Hegarty Plumbing", lic="820321", trade="plumbing", area="sf",
         areaText="CSLB records a San Francisco mailing address (P O Box 27326, San Francisco, "
                  "CA 94127) but no street location, so neighbourhood dispatch cannot be "
                  "established from the regulator. The registry records 2451 28th Av, 94116 with "
                  "129 permit rows.",
         extra=[dict(field="Registry", text="Official SF DBI registry records 2451 28th Av, "
                                            "94116 with 129 permit rows.", source=151,
                     excerpt=reg_excerpt("Hegarty Plumbing"))],
         flags=[dict(level="gap",
                    text="CSLB address is a post-office box only; no physical base is published "
                         "by the regulator, so Outer Sunset coverage is unverified.",
                    sources=[167])],
         rationale="Active C-36 sole ownership issued 06/02/2003 with a San Francisco mailing "
                   "address, workers compensation classified 51871 Plumbing-high wage, and a "
                   "Parkside permit history.",
         nextStep="Ask for the physical work base and confirm dispatch to 94122."),
    dict(name="Ron Hogan Drywall", lic="265709", trade="drywall", area="sunset",
         website="https://ronhogandrywall.net/commercial-residential-drywall-contractor-san-francisco-ca/",
         websiteSource=187,
         areaText="The company's own page states it serves San Francisco neighbourhoods "
                  "including the \u201cSunset District\u201d. CSLB records the business address as 2380 "
                  "Palmer Circle, Fairfield, CA 94534, so the Sunset statement is a business "
                  "claim rather than a regulator-held local address.",
         extra=[dict(field="Coverage", text="Company page names the Sunset District among the "
                                            "San Francisco neighbourhoods it says it serves, "
                                            "and publishes CSLB #265709 \u2014 the same number read "
                                            "directly on CSLB.", source=187,
                     excerpt="a licensed and insured expert (CSLB #265709) with over 30 years of "
                             "experience \u2026 renovations in neighborhoods like Noe Valley, Pacific "
                             "Heights, Mission District, Nob Hill, Sunset District, and Russian "
                             "Hill"),
                dict(field="Drywall scope", text="Company page describes drywall installation, "
                                                 "repair and finishing for San Francisco "
                                                 "residential work.", source=187,
                     excerpt="we specialize in high-quality drywall installation, repair, and "
                             "finishing tailored specifically to San Francisco\u2019s unique needs")],
         flags=[dict(level="gap",
                    text="License expires 11/30/2026 \u2014 inside three months of this snapshot. "
                         "Recheck CSLB before booking.", sources=[170]),
                dict(level="notice",
                    text="CSLB miscellaneous history shows \u201c11/04/2019 - LICENSE CANCELED PER "
                         "REQUEST\u201d followed by a reissue on 11/17/2022. The license is active "
                         "now; the gap in between is recorded so the history is visible.",
                    sources=[170]),
                dict(level="discrepancy",
                    text="Company page headline says \u201cSan Francisco CA 94103\u201d while CSLB "
                         "records Fairfield (94534). Marketing location text does not match the "
                         "regulator-held address.", sources=[187, 170])],
         rationale="Active C-9 (Drywall) sole ownership issued 10/20/1970 with wallboard "
                   "workers-compensation codes, whose own site claims Sunset District coverage. "
                   "C-9 is the correct classification for hanging and finishing a ceiling patch "
                   "and framing an access opening.",
         nextStep="Confirm current Sunset dispatch, and ask whether an access-panel frame is "
                  "installed as part of the ceiling patch."),
    dict(name="R S Dynamic Builders Inc", lic="1130530", trade="general", area="sunset",
         website="https://rsdynamicbuilders.com/", websiteSource=192,
         areaText="The company's About-page structured data lists a serviceArea including "
                  "\u201cSunset\u201d and \u201cRichmond\u201d. CSLB records the business address as 909 Ocean "
                  "View Ave, San Mateo, CA 94401, so Sunset coverage is a business claim only.",
         extra=[dict(field="Drywall scope", text="Company page describes ceiling drywall repair "
                                                 "including water stains and sagging, water "
                                                 "damage ceiling repair, and reinforcing lath "
                                                 "and plaster in older homes.", source=190,
                     excerpt="Ceiling drywall repair San Francisco (including water stains & "
                             "sagging) \u2026 Water damage repair ceiling SF \u2026 Structural Integrity "
                             "for Older Homes: Reinforcing lath and plaster or updating with "
                             "modern drywall while preserving your home's character"),
                dict(field="Coverage", text="About-page structured data lists a service area "
                                            "that includes Sunset and Richmond, and an "
                                            "aggregate rating of 5.0 from 5 reviews.",
                     source=191,
                     excerpt="\"serviceArea\":[{\"name\":\"San Francisco Bay Area\"},{\"name\":\"Mission "
                             "District\"},{\"name\":\"Noe Valley\"},{\"name\":\"Castro\"},{\"name\":"
                             "\"Sunset\"},{\"name\":\"Richmond\"}\u2026] \u2026 \"aggregateRating\":"
                             "{\"ratingValue\":\"5.0\",\"reviewCount\":\"5\"}")],
         flags=[dict(level="hold",
                    text="Scope hold: CSLB shows B (General Building) only \u2014 no C36 plumbing "
                         "and no C-9 drywall classification. A B licensee cannot self-perform "
                         "the plumbing portion of this job and must hold or subcontract the "
                         "correct trade licenses.", sources=[171]),
                dict(level="discrepancy",
                    text="Address conflict: the company's own About-page structured data gives "
                         "streetAddress \u201c123 Main Street\u201d, San Mateo 94401 \u2014 a placeholder-"
                         "looking value \u2014 while CSLB records 909 Ocean View Ave, San Mateo "
                         "94401.", sources=[191, 171]),
                dict(level="discrepancy",
                    text="Phone conflict: the site publishes +1 415 450 7338 while CSLB "
                         "publishes (650) 918-2317 for the same license.", sources=[192, 171]),
                dict(level="gap",
                    text="License was issued 12/16/2024, expires 12/31/2026, and workers "
                         "compensation is exempt on a certified no-employees basis. Very short "
                         "operating history under this license and no covered employees.",
                    sources=[171])],
         rationale="Recorded because its own copy addresses ceiling water damage and older-home "
                   "lath and plaster, but it fails a scope gate: B-only classification, a new "
                   "license, no covered employees, and two internal identity conflicts.",
         nextStep="If contacted at all, ask which license classifications cover the plumbing and "
                  "the drywall, and who the subcontractors are."),
    dict(name="Gorman Pipeline Inc", lic="898289", trade="engineering", area="outer",
         status="excluded",
         areaText="CSLB records the business address as 1518 27th Ave, San Francisco, CA 94122 "
                  "\u2014 an Outer Sunset address held by the regulator. The registry records the "
                  "same address with 239 permit rows.",
         extra=[dict(field="Registry", text="Official SF DBI registry records 1518 27th Av, "
                                            "94122 with 239 permit rows.", source=150,
                     excerpt=reg_excerpt("Gorman Pipeline Inc"))],
         flags=[dict(level="hold",
                    text="Scope exclusion: the CSLB page shows A (General Engineering) only, "
                         "with workers-compensation codes 6307/6308 Sewer Construction. There is "
                         "no C36 plumbing classification, so this firm cannot lawfully "
                         "self-perform an indoor bathtub-overflow repair.", sources=[163])],
         rationale="Included as an explicit scope exclusion rather than silently dropped: an "
                   "active, Outer Sunset-addressed pipeline contractor is a plausible search "
                   "result for \u201cplumbing near me\u201d but is the wrong classification for this "
                   "job.",
         nextStep="None for this scope. Relevant only if a building sewer or lateral problem is "
                  "separately diagnosed."),
    # ---- lapsed / suspended records: held, never hidden ----
    dict(name="All-Point Solutions Plumbing Co", lic="950265", trade="plumbing", area="outer",
         status="hold",
         areaText="CSLB records 1651 42nd Avenue, San Francisco, CA 94122 \u2014 an Outer Sunset "
                  "address held by the regulator. The registry records 1651 42nd Av with 114 "
                  "permit rows and a 408-area-code phone.",
         extra=[dict(field="Registry", text="Official SF DBI registry records 1651 42nd Av, "
                                            "94122 with 114 permit rows.", source=150,
                     excerpt=reg_excerpt("All Point Solutions Plumbing Co."))],
         flags=[dict(level="hold",
                    text="BOOKING HOLD \u2014 CSLB status at the time of reading: \u201cLicense is under "
                         "suspension \u2026 License is under Contractors Bond Suspension.\u201d The "
                         "contractor's bond with HUDSON INSURANCE COMPANY shows a cancellation "
                         "date of 09/01/2026. A suspended license cannot lawfully contract.",
                    sources=[161]),
                dict(level="discrepancy",
                    text="Registry phone is a 408 area code (4088814686) while CSLB publishes "
                         "(415) 818-2822 for the same 94122 address.", sources=[150, 161])],
         rationale="Recorded as a hold, not a candidate. The address is genuinely Outer Sunset, "
                   "which is why the suspension is worth surfacing rather than dropping.",
         nextStep="Do not book while suspended. If reconsidered later, re-read CSLB and ask the "
                  "bonding company to confirm bond status, as the CSLB page itself advises."),
    dict(name="F C Company", lic="1022789", trade="plumbing", area="outside", status="hold",
         areaText="Registry records \u201cF C Company\u201d at 3638 Noriega St, San Francisco 94122 "
                  "with 107 permit rows. CSLB records 113 San Diego Avenue, Daly City, CA 94014.",
         extra=[dict(field="Registry", text="Official SF DBI registry records 3638 Noriega St, "
                                            "94122 with 107 permit rows.", source=150,
                     excerpt=reg_excerpt("F C Company"))],
         flags=[dict(level="hold",
                    text="BOOKING HOLD \u2014 CSLB status at the time of reading: \u201cLicense is under "
                         "suspension \u2026 License is under Contractors Bond Suspension.\u201d Bond with "
                         "HUDSON INSURANCE COMPANY shows cancellation date 09/01/2026 \u2014 the "
                         "same surety and the same cancellation date recorded for All-Point "
                         "Solutions Plumbing (950265). Two unrelated firms losing bond cover on "
                         "one date is a pattern to verify, not assume.", sources=[164, 161])],
         rationale="Held. Notable only as part of the shared 09/01/2026 Hudson Insurance bond "
                   "cancellation pattern with another wave-6 firm.",
         nextStep="None while suspended."),
    dict(name="B R Troika Incorporated dba Mr Rooter Plumbing", lic="812845", trade="plumbing",
         area="outer", status="hold",
         areaText="CSLB records \u201c2341 JUDAH, SAN FRANCISCO, CA 94122\u201d \u2014 an Outer Sunset "
                  "address held by the regulator. Registry rows record the same license at 2801 "
                  "Judah St, 94122 under two name variants (\u201cB R Troika Incorporated/Mr R\u201d, "
                  "159 rows; \u201cBr Troika Inc. Dba Mr Rooter Plumbing\u201d, 142 rows).",
         extra=[dict(field="Registry", text="Official SF DBI registry records this license at "
                                            "2801 Judah St, 94122 under two different firm-name "
                                            "spellings, 159 and 142 permit rows respectively.",
                     source=150, excerpt=reg_excerpt("B R Troika Incorporated/Mr R")),
                dict(field="Identity", text="This is a separate legal entity from the Mr. Rooter "
                                            "franchise record already in this dataset (SDP "
                                            "Plumbing Inc, license 1016070). Both are held: "
                                            "812845 expired 09/30/2018 and 1016070 expired "
                                            "07/31/2024 per direct CSLB reads.", source=162,
                     excerpt="B R TROIKA INCORPORATED \u00b7 dba MR ROOTER PLUMBING \u00b7 2341 JUDAH \u00b7 "
                             "SAN FRANCISCO, CA 94122 \u2014 Expire Date 09/30/2018 \u2014 \u201cThis license "
                             "is expired and not able to contract at this time.\u201d")],
         flags=[dict(level="hold",
                    text="BOOKING HOLD \u2014 license expired 09/30/2018 and CSLB states it is \u201cnot "
                         "able to contract at this time\u201d. Bond cancelled 05/10/2019; workers "
                         "compensation exempt with no employees.", sources=[162]),
                dict(level="discrepancy",
                    text="Street-number conflict on the same street: CSLB says 2341 Judah, the "
                         "registry says 2801 Judah St. Combined with two registry spellings of "
                         "the firm name, identity resolution for the Judah Street Mr. Rooter "
                         "operation is unresolved.", sources=[162, 150]),
                dict(level="notice",
                    text="Corroborates and extends an existing wave-1 irregularity: the Mr. "
                         "Rooter brand in San Francisco is now linked to two separately lapsed "
                         "C36 licenses (812845 expired 2018; 1016070 expired 07/31/2024). A "
                         "live franchise website and a large review count are still not a "
                         "license.", sources=[162])],
         rationale="Added as an entity-resolution record, not as a candidate. It strengthens the "
                   "existing Mr. Rooter flag with a second, independent lapsed license at a "
                   "Judah Street address.",
         nextStep="None. Do not treat brand advertising as evidence of a current license."),
    dict(name="Pro Plumbing", lic="859973", trade="plumbing", area="sunset", status="hold",
         areaText="CSLB records \u201c145 BARNEVELD AVE, SAN FRANCISCO, CA 94122\u201d. The registry "
                  "records \u201cPro Plumbing\u201d at 1814 40th Av, 94122 with 239 permit rows and a "
                  "second row with phone 4159943468 (111 rows).",
         extra=[dict(field="Registry", text="Official SF DBI registry records 1814 40th Av, "
                                            "94122 with 239 permit rows, plus a further 111 rows "
                                            "under the same license with a different phone "
                                            "number.", source=150,
                     excerpt=reg_excerpt("Pro Plumbing"))],
         flags=[dict(level="hold",
                    text="BOOKING HOLD \u2014 CSLB: \u201cThis license is expired and not able to "
                         "contract at this time\u201d (expire date 06/30/2023), with additional "
                         "status noting bond, legal and workers-compensation requirements must "
                         "be met to renew, and \u201c10/16/2023 - WC EXEMPT CANCELLED-LIC "
                         "INACTIVATED\u201d.", sources=[158]),
                dict(level="discrepancy",
                    text="Address/ZIP conflict inside CSLB itself: the street is given as 145 "
                         "Barnevelt Ave with ZIP 94122, while the registry address is 1814 40th "
                         "Av (94122). Barneveld Avenue is not an Outer Sunset street, so the "
                         "CSLB ZIP for this record looks inconsistent. Flagged for manual "
                         "review.", sources=[158, 150]),
                dict(level="notice",
                    text="Near-name caution: this record is separate from the pre-existing "
                         "\u201cPro Plumbing & Fire Sprinkler\u201d entry in this dataset. They were not "
                         "merged.", sources=[158])],
         rationale="Held. A long-standing 40th Avenue plumbing firm whose license has been "
                   "inactivated since 2023 \u2014 exactly the kind of neighbourhood shop that still "
                   "appears in directory results.",
         nextStep="None while expired."),
    dict(name="Moonlight Plumbing", lic="976543", trade="plumbing", area="outside",
         status="hold",
         areaText="Registry records \u201cMoonlight Plumbing\u201d at 1406 25th Av, San Francisco 94122 "
                  "with 123 permit rows. CSLB now records 59164 Wilmar Ave, Yucca Valley, CA "
                  "92284 \u2014 roughly 450 road miles from the Outer Sunset.",
         extra=[dict(field="Registry", text="Official SF DBI registry records 1406 25th Av, "
                                            "94122 with 123 permit rows.", source=150,
                     excerpt=reg_excerpt("Moonlight Plumbing"))],
         flags=[dict(level="hold",
                    text="BOOKING HOLD \u2014 CSLB address is Yucca Valley (92284) while the "
                         "business phone remains a 415 number, and the license expires "
                         "09/30/2026, nineteen days after this snapshot. Workers compensation "
                         "is exempt with no employees.", sources=[160]),
                dict(level="discrepancy",
                    text="Registry rows record two different 415 phone numbers for the same "
                         "license (4157223623 and, in a second row, none) while CSLB publishes "
                         "(415) 722-3623.", sources=[150, 160])],
         rationale="Held. Illustrates why registry presence is not present operation: an Outer "
                   "Sunset permit history, a San Francisco phone number and a desert mailing "
                   "address on the same active license.",
         nextStep="None. If the name resurfaces, re-read CSLB after 09/30/2026."),
    dict(name="Asia Plumbing", lic="287477", trade="plumbing", area="outer", status="hold",
         areaText="CSLB records 1354 31st Ave, San Francisco, CA 94122 \u2014 an Outer Sunset "
                  "address held by the regulator. The registry records the same address with 280 "
                  "permit rows plus 158 further rows.",
         extra=[dict(field="Registry", text="Official SF DBI registry records 1354 31st Avenue, "
                                            "94122 with 280 permit rows (and 158 more under a "
                                            "second phone formatting) \u2014 one of the deepest "
                                            "permit histories in the ZIP.", source=150,
                     excerpt=reg_excerpt("Asia Plumbing"))],
         flags=[dict(level="hold",
                    text="BOOKING HOLD \u2014 CSLB: \u201cThis license is expired and not able to "
                         "contract at this time\u201d, expire date 05/31/2014, partnership entity, "
                         "bond cancelled 07/24/2014. A license issued 10/01/1973 with a very "
                         "large local permit history has been lapsed for over a decade.",
                    sources=[173])],
         rationale="Held. Kept visible because a firm with 438 registry permit rows at an Outer "
                   "Sunset address can still appear in neighbourhood recommendations long after "
                   "its license lapsed.",
         nextStep="None while expired."),
    dict(name="Chen's Plumbing Inc", lic="665412", trade="plumbing", area="sunset",
         status="hold",
         areaText="Registry records \u201cChen's Plumbing Inc\u201d at 2127 - 34th Avenue, San "
                  "Francisco 94116 with 223 permit rows. CSLB records 148 21st Ave, San "
                  "Francisco, CA 94121-1206.",
         extra=[dict(field="Registry", text="Official SF DBI registry records 2127 - 34th "
                                            "Avenue, 94116 with 223 permit rows.", source=151,
                     excerpt=reg_excerpt("Chen's Plumbing Inc"))],
         flags=[dict(level="hold",
                    text="BOOKING HOLD \u2014 CSLB: \u201cThis license is canceled and not able to "
                         "contract\u201d, expire date 02/16/2015, with \u201c02/16/2015 - SECRETARY OF "
                         "STATE - DISSOLUTION\u201d. The corporate entity no longer exists.",
                    sources=[168])],
         rationale="Held. A dissolved corporation is not a bookable contractor regardless of "
                   "how its old permit history looks.",
         nextStep="None."),
    dict(name="Goodrich Plumbing Inc", lic="837694", trade="plumbing", area="sunset",
         status="hold",
         areaText="Registry records \u201cGoodrich Plumbing Inc\u201d at 1412 11th Av, San Francisco "
                  "94122 with 233 permit rows. CSLB records 265 Kensington Way, San Francisco, "
                  "CA 94127.",
         extra=[dict(field="Registry", text="Official SF DBI registry records 1412 11th Av, "
                                            "94122 with 233 permit rows.", source=150,
                     excerpt=reg_excerpt("Goodrich Plumbing Inc"))],
         flags=[dict(level="hold",
                    text="BOOKING HOLD \u2014 CSLB: \u201cThis license is canceled and not able to "
                         "contract\u201d with \u201c02/11/2025 - LICENSE CANCELED PER REQUEST\u201d and "
                         "\u201c02/11/2025 - SECRETARY OF STATE - DISSOLUTION\u201d. Bond cancelled "
                         "04/04/2025 and workers compensation cancelled 01/04/2025.",
                    sources=[169])],
         rationale="Held. Recently dissolved (2025), so historic neighbourhood familiarity does "
                   "not translate into a bookable contractor.",
         nextStep="None."),
    dict(name="Ricky's Plumbing Company", lic="570753", trade="plumbing", area="sunset",
         status="hold",
         areaText="Registry records \u201cRicky's Plumbing Co\u201d at 2727 Irving St, San Francisco "
                  "94122 with 183 permit rows. CSLB records 3550 Cabrillo Street, San "
                  "Francisco, CA 94121.",
         extra=[dict(field="Registry", text="Official SF DBI registry records an Outer Sunset "
                                            "corridor address (2727 Irving St, 94122) with 183 "
                                            "permit rows.", source=150,
                     excerpt=reg_excerpt("Ricky's Plumbing Co"))],
         flags=[dict(level="hold",
                    text="BOOKING HOLD \u2014 CSLB: expired 06/30/2005, \u201cThe license was canceled "
                         "after expiration\u201d and \u201c09/16/2005 - LICENSE CANCELLED PER REQUEST\u201d. "
                         "Lapsed for more than twenty years.", sources=[165])],
         rationale="Held. Demonstrates that permit-registry history reaches back decades and "
                   "must never be read as current availability.",
         nextStep="None."),
]

for spec in A:
    num = spec["lic"]
    d = L[num]
    bid = "w6-" + slug(spec["name"])
    claims = [dict(field="Discovery",
                   text=f"{spec['name']} was surfaced by this pass and its CSLB license detail "
                        f"page was read directly on cslb.ca.gov on {DATE}.",
                   source=d["src"], excerpt=d["quote"])]
    claims += spec["extra"]
    claims.append(dict(
        field="License",
        text=("Current and active \u00b7 " if d["status"] == "active" else
              "Not active at the time of reading \u00b7 ") + " \u00b7 ".join(d["classes"]) +
             f" \u00b7 {d['etype']} \u00b7 expires {d['expires']}.",
        source=d["src"], excerpt=d["quote"]))
    if d["misc"]:
        claims.append(dict(field="Status", text="CSLB miscellaneous history lines: " +
                           "; ".join(d["misc"]) + ".", source=d["src"], excerpt=d["quote"]))
    b = dict(id=bid, name=spec["name"], website=spec.get("website"),
             websiteSource=spec.get("websiteSource"), area=spec["area"],
             areaText=spec["areaText"], license=lic_obj(num),
             phone=norm_phone(d["phone"]),
             phoneSource=d["src"], claims=claims, flags=spec["flags"],
             trade=spec["trade"], gaps=gaps_for(spec["trade"]))
    if spec.get("priority"):
        b["priority"] = spec["priority"]
        b["rationale"] = spec["rationale"]
        b["nextStep"] = spec["nextStep"]
    elif spec.get("rationale"):
        b["rationale"] = spec["rationale"]
        b["nextStep"] = spec["nextStep"]
    if spec.get("status"):
        b["status"] = spec["status"]
    add(b)

# ==========================================================================
# GROUP B - 16 registry-only records (no CSLB read yet: fail-closed).
# ==========================================================================
B = [
    ("Ocean Air Heating", 150, "94122", "multi-trade",
     "Registry records \u201cOcean Air Heating\u201d at 1859 42nd Av, San Francisco 94122-0000 with "
     "244 permit rows \u2014 an Outer Sunset address, but the name suggests a heating trade."),
    ("Bill Bragg Plumbing", 150, "94122", "plumbing",
     "Registry records \u201cBill Bragg Plumbing\u201d at Po Box 22073, San Francisco 94122 with 234 "
     "permit rows plus 218 further rows under a second phone formatting."),
    ("C T Construction & Plumb", 150, "94122", "multi-trade",
     "Registry records \u201cC T Construction & Plumb\u201d at 1847  48th Av, San Francisco 94122 with "
     "234 permit rows and a second block of 81 rows under phone 4156681618."),
    ("Francis John Burke", 150, "94122", "plumbing",
     "Registry records \u201cFrancis John Burke\u201d at 2437 Ortega St, San Francisco 94122-0000 with "
     "175 permit rows \u2014 an individually named licensee on an Outer Sunset street."),
    ("Hawk N Lee Co", 150, "94122", "plumbing",
     "Registry records \u201cHawk N Lee Co\u201d at 1609  Noriega St, San Francisco 94122 with 154 "
     "permit rows."),
    ("Ren Lei Construction Co", 150, "94122", "multi-trade",
     "Registry records \u201cRen Lei Construction Co\u201d at 750 Lawton St, San Francisco 94122-0000 "
     "with 153 permit rows."),
    ("Abe's Plumbing", 150, "94122", "plumbing",
     "Registry records \u201cAbe's Plumbing\u201d at Po Box 22153, San Francisco 94122 with 148 permit "
     "rows."),
    ("City Plumbing Company", 150, "94122", "plumbing",
     "Registry records \u201cCity Plumbing Company\u201d at 1214 40th Av, San Francisco 94122-0000 with "
     "79 permit rows."),
    ("Best Plumbing Choice", 151, "94116", "plumbing",
     "Registry records \u201cBest Plumbing Choice\u201d at 2138 17th Av, San Francisco 94116-0000 with "
     "422 permit rows \u2014 the highest count found in the 94116 query."),
    ("O M P P Inc.", 151, "94116", "plumbing",
     "Registry records \u201cO M P P Inc.\u201d at 633 Taraval Street, San Francisco 94116 with 323 "
     "permit rows plus 161 further rows."),
    ("L R Plumbing", 151, "94116", "plumbing",
     "Registry records \u201cL R Plumbing\u201d at 2162 19th Av, San Francisco 94116-0000 with 289 "
     "permit rows."),
    ("Yao Star Construction", 151, "94116", "multi-trade",
     "Registry records \u201cYao Star Construction\u201d at 2223 42nd Avenue, San Francisco 94116-0000 "
     "with 240 permit rows."),
    ("L C Plumbing & Fire Protection Inc", 151, "94116", "plumbing",
     "Registry records \u201cL C Plumbing & Fire Protection Inc\u201d at 2470 27th Avenue, San "
     "Francisco 94116-0000 with 215 permit rows."),
    ("J A Plumbing Inc", 151, "94116", "plumbing",
     "Registry records \u201cJ A Plumbing Inc\u201d at 3444 Ulloa St, San Francisco 94116-0000 with 173 "
     "permit rows plus 115 further rows at 2241 28th Av."),
    ("F - 1 Plumbing Services", 151, "94116", "plumbing",
     "Registry records \u201cF - 1 Plumbing Services\u201d at 2186 46th Av, San Francisco 94116-0000 "
     "with 152 permit rows."),
    ("Excellent Plumbing Co", 151, "94116", "plumbing",
     "Registry records \u201cExcellent Plumbing Co\u201d at 1355 33rd Av, San Francisco 94116 with 151 "
     "permit rows plus 137 further rows at 2438 35th Ave."),
]

for name, src, zc, trade, areatext in B:
    r = REG[name]
    ex = reg_excerpt(name)
    claims = [
        dict(field="Discovery",
             text=f"{name} appears in the official SF DBI \u201cPlumbing Permits Contacts\u201d open "
                  f"dataset queried directly by firm ZIP on {DATE}.", source=src, excerpt=ex),
        dict(field="Registry",
             text="Registry-recorded CSLB number " + r["lic"] + " and recorded business address "
                  + r["addr"] + ", San Francisco " + r["zip"] + ", with " + str(r["permits"]) +
                  " plumbing-permit contact rows. This is a registry-recorded value, not an "
                  "independently read license record.", source=src, excerpt=ex),
    ]
    flags = [dict(level="gap",
                  text="Registry-recorded license number " + r["lic"] +
                       " has NOT been read on CSLB in this pass. Registry rows are historical "
                       "permit contacts with no in-dataset dates; they never establish that a "
                       "license is current, that the firm still operates, or that it dispatches "
                       "to the Outer Sunset today.", sources=[src])]
    if zc == "94116":
        flags.append(dict(level="notice",
                          text="Recorded address is in ZIP 94116 (Parkside), which borders the "
                               "Outer Sunset but is not 94122. Treat coverage as adjacent, not "
                               "confirmed.", sources=[src]))
    if r["addr"].lower().startswith("po box"):
        flags.append(dict(level="gap",
                          text="Registry address is a post-office box, so no physical base in "
                               "the neighbourhood is established.", sources=[src]))
    b = dict(id="w6-" + slug(name), name=name, website=None, websiteSource=None,
             area=("sunset" if zc == "94122" else "sunset"), areaText=areatext,
             license=None, phone=r["phone"], phoneSource=src, claims=claims, flags=flags,
             trade=trade, gaps=gaps_for(trade))
    add(b)

# ==========================================================================
# GROUP C - 12 drywall / plaster / finish leads from indexed extracts.
# ==========================================================================
C = [
    dict(name="SF Building Group", src=176, area="unknown", trade="general",
         evidence="5.0 (2 reviews); appears in Yelp's sponsored results for \u201cDry Wall Repair\u201d "
                  "near Outer Sunset, San Francisco with a \u201cVerified License\u201d badge and free "
                  "estimates; response time about 10 mins; 26 locals recently requested a "
                  "consultation.",
         note="Appears on Yelp's Outer Sunset dry-wall-repair results page; the indexed extract "
              "carries no explicit service-area statement and no license number, so coverage "
              "and credentials are unconfirmed.",
         flags=[dict(level="notice",
                    text="\u201cVerified License\u201d is a Yelp badge, not a CSLB record. No license "
                         "number appears in the extract and none was read this pass.",
                    sources=[176]),
                dict(level="gap",
                    text="Two reviews is a very small sample and cannot characterise "
                         "performance in either direction.", sources=[176])]),
    dict(name="Mullican Remodeling", src=176, area="unknown", trade="general",
         evidence="Labelled \u201cNew on Yelp\u201d in the sponsored results for \u201cDry Wall Repair\u201d near "
                  "Outer Sunset, San Francisco, with a \u201cVerified License\u201d badge and free "
                  "estimates; no rating or review count shown in the extract.",
         note="Appears on Yelp's Outer Sunset dry-wall-repair results page as a new listing with "
              "no review sample in the extract.",
         flags=[dict(level="gap",
                    text="No review sample and no license number in the extract; \u201cNew on Yelp\u201d "
                         "means the profile history is short, not that the business is new.",
                    sources=[176])]),
    dict(name="ABR PRO Painting", src=176, area="sf", trade="finish",
         evidence="4.8 (49 reviews); \u201cServing San Francisco and the Surrounding Area\u201d; "
                  "\u201cVerified License\u201d badge; discounts available and free estimates; listed "
                  "under \u201cWall finish repair\u201d in Yelp's Outer Sunset dry-wall-repair results "
                  "and categorised as Painters, General Contractors, Drywall Installation & "
                  "Repair.",
         note="Indexed extract states San Francisco coverage; a customer excerpt describes "
              "patching a new section of drywall alongside painting.",
         extra=[dict(field="Relevant quote",
                    text="An indexed customer excerpt describes scope growth that included "
                         "patching new drywall \u2014 adjacent to, but not the same as, closing a "
                         "ceiling opening after plumbing work.", source=176,
                    excerpt="when we needed to increase the scope to paint an extra room and "
                            "patch a new section of drywall.")],
         flags=[dict(level="notice",
                    text="Painting-led business: drywall patching is advertised as part of a "
                         "painting scope. Confirm a C-9 or B classification for ceiling work "
                         "before relying on it.", sources=[176])]),
    dict(name="NorthLine Drywall Repair", src=178, area="sf", trade="drywall",
         evidence="Listed in Yelp's San Francisco \u201cdrywall repair service\u201d results with the "
                  "neighbourhood label \u201cBayview-Hunters Point\u201d, an offer \u201c$50 OFF Cutter "
                  "Cleaning\u201d, a 10 mins response time and 447 locals recently requesting a "
                  "quote; no rating or review count shown in the extract.",
         note="Indexed extract places the business in Bayview-Hunters Point, San Francisco; no "
              "Outer Sunset coverage statement and no rating sample appear.",
         flags=[dict(level="gap",
                    text="No rating or review count in the extract, and the base is on the "
                         "opposite side of the city from the Outer Sunset. Coverage is "
                         "unconfirmed.", sources=[178])]),
    dict(name="Rodas Drywall and Painting", src=178, area="unknown", trade="drywall",
         evidence="5.0 (38 reviews); \u201c12 years in business\u201d; \u201cBeat or match prices\u201d; listed "
                  "under \u201cDrywall repair\u201d in Yelp's San Francisco drywall-repair-service "
                  "results; 1 day response time and 69 locals recently requested a quote.",
         note="Indexed extract gives a strong small-sample rating and a stated 12-year operating "
              "history but no explicit service area and no license number.",
         extra=[dict(field="Relevant quote",
                    text="An indexed customer excerpt describes interior painting, new door "
                         "installation and stair work \u2014 finish scope, not a ceiling opening "
                         "behind plumbing.", source=178,
                    excerpt="Rodas painted the interior of our home and did a great job. He "
                            "installed new doors too. Did some work on our stairs which made it "
                            "brand new")],
         flags=[dict(level="gap",
                    text="\u201cBeat or match prices\u201d is a marketing offer. Price competition is not "
                         "evidence of capability on a constrained ceiling repair.",
                    sources=[178])]),
    dict(name="New Line Drywall", src=189, area="sf", trade="drywall",
         website="https://newlinedrywall.com/", websiteSource=189,
         evidence="Company site describes sheetrock repair, drywall installation, taping and "
                  "Level 5 smooth finish across San Jose, San Francisco, Oakland and the Bay "
                  "Area; page structured data lists areaServed including San Francisco and "
                  "telephone +15107063145.",
         note="Business-site claim of San Francisco coverage, including patching ceilings and "
              "hand-matching existing texture.",
         extra=[dict(field="Drywall scope",
                    text="Company copy describes patching affected areas on walls or ceilings "
                         "and matching existing texture so the repair is not visible \u2014 the "
                         "finish half of a ceiling-opening job.", source=189,
                    excerpt="we patch the affected area on walls or ceilings, match your "
                            "existing texture, and restore the surface without leaving a trace"),
                dict(field="Coverage",
                    text="Page structured data lists an area served that includes San Francisco.",
                    source=189,
                    excerpt="\"areaServed\":[{\"name\":\"San Francisco\"},{\"name\":\"Oakland\"},"
                            "{\"name\":\"San Jose\"},{\"name\":\"Fremont\"},{\"name\":\"Palo Alto\"}]")],
         flags=[dict(level="gap",
                    text="No license number is published in the extract, so no CSLB read was "
                         "possible this pass. A telephone with a 510 area code and Bay Area "
                         "cities listed first suggest the base is east of San Francisco.",
                    sources=[189])]),
    dict(name="Ezekiel's Drywall Services", src=180, area="outside", trade="drywall",
         evidence="Listed in Yelp's drywall-repair near-me index as \u201cServing San Jose and the "
                  "Surrounding Area\u201d with 109 reviews and categories Drywall Installation & "
                  "Repair, Stucco Services, Painters.",
         note="Indexed extract states a San Jose service base; Outer Sunset coverage is not "
              "stated.",
         flags=[dict(level="notice",
                    text="Outside-area concern: San Jose is roughly 50 road miles from the Outer "
                         "Sunset. Recorded so the sample size is visible, not as a local "
                         "candidate.", sources=[180])]),
    dict(name="JR Drywall", src=180, area="outside", trade="drywall",
         evidence="Listed in Yelp's drywall-repair near-me index as \u201cServing Emeryville and the "
                  "Surrounding Area\u201d with 35 reviews, category Drywall Installation & Repair.",
         note="Indexed extract states an Emeryville service base; Outer Sunset coverage is not "
              "stated.",
         flags=[dict(level="notice",
                    text="Outside-area concern: Emeryville is across the bay. Recorded for "
                         "completeness of the drywall sample only.", sources=[180])]),
    dict(name="Dango Drywall Co, Corp", src=193, area="sf", trade="drywall",
         evidence="Named on Angi / HomeAdvisor's San Francisco drywall-repair matching page, "
                  "with a customer excerpt describing a next-day scheduling turnaround and a "
                  "quote about half the competition's.",
         note="Lead-marketplace listing for San Francisco drywall repair; the marketplace is not "
              "the regulator and prescreening claims are not verified here.",
         extra=[dict(field="Relevant quote",
                    text="An indexed customer excerpt describes rapid scheduling and a low "
                         "quote. Speed and price are not evidence of capability on a ceiling "
                         "opening above an occupied unit.", source=193,
                    excerpt="They accomodated my work request 1 day after I listed a job on "
                            "Angi. They quoted a price that was half that of the competititon "
                            "and were able to accomodate my work request on a weekend day")],
         flags=[dict(level="notice",
                    text="Angi / HomeAdvisor is a paid lead marketplace; BBB customer reviews of "
                         "the platform itself record widespread complaints about lead quality "
                         "and billing. A listing here is discovery only.", sources=[193])]),
    dict(name="All About Plastering", src=185, area="unknown", trade="plaster",
         evidence="4.8 (34 reviews); \u201cVerified License\u201d badge; free estimates; responds in "
                  "about 6 hrs; listed in Yelp's San Francisco stucco-services results "
                  "alongside Caledonia Plastering and Stucco.",
         note="Indexed stucco/plaster category result; no service-area statement and no license "
              "number in the extract.",
         flags=[dict(level="notice",
                    text="\u201cVerified License\u201d is a Yelp badge. Plastering classification (C35) "
                         "was not read on CSLB this pass.", sources=[185])]),
    dict(name="Gray Lath and Plaster", src=185, area="unknown", trade="plaster",
         evidence="Listed in Yelp's San Francisco stucco-services sponsored results with free "
                  "estimates; no rating, review count or service-area statement appears in the "
                  "extract.",
         note="Trade name is directly relevant to a 1940 building (wood lath and plaster "
              "ceilings), but the indexed extract carries no evidence beyond the listing.",
         flags=[dict(level="gap",
                    text="No rating sample, no service area and no license number in the "
                         "extract. Name relevance is not evidence of capability.",
                    sources=[185])]),
    dict(name="Marcelino Plastering", src=186, area="unknown", trade="plaster",
         evidence="4.9 (40 reviews); \u201cVerified License\u201d badge; free estimates; responds in "
                  "about 1 day; listed in Yelp's San Francisco \u201cStucco Contractor\u201d results.",
         note="Indexed stucco-contractor result with a solid small-sample rating; no "
              "service-area statement and no license number in the extract.",
         flags=[dict(level="notice",
                    text="\u201cVerified License\u201d is a Yelp badge, not CSLB verification. Stucco is "
                         "exterior scope; interior ceiling plaster work is not established.",
                    sources=[186])]),
]

for spec in C:
    claims = [dict(field="Discovery",
                   text=f"{spec['name']} appears in the cited indexed result with the "
                        f"attributed details below.", source=spec["src"],
                   excerpt=spec["evidence"])]
    claims.append(dict(field="Coverage", text=spec["note"], source=spec["src"],
                       excerpt=spec["evidence"]))
    claims += spec.get("extra", [])
    b = dict(id="w6-" + slug(spec["name"]), name=spec["name"],
             website=spec.get("website"), websiteSource=spec.get("websiteSource"),
             area=spec["area"], areaText=spec["note"], license=None, phone=None,
             phoneSource=None, claims=claims, flags=spec["flags"], trade=spec["trade"],
             gaps=gaps_for(spec["trade"]))
    add(b)

# ==========================================================================
# Reviews: only text actually present in an indexed extract, with author and
# date exactly as published. Nothing is completed, paraphrased or inferred.
# ==========================================================================
REVIEWS = [
    dict(id="R60", business="w6-caledonia-plastering-stucco-inc", platform="Thumbtack",
         author="Tom S.", published="Jun 2, 2018",
         quote="Quick to respond, fair price, explained the work clearly. job well done. John "
               "took care of the hole in the ceiling and cleaned up after. Thank you. Definitely "
               "will call again if there's a need for plastering job.",
         analysis="Closest finish-side task evidence in wave 6: a hole in a ceiling was made "
                  "good by this business, with the work explained beforehand and the site cleaned "
                  "afterwards. It does not say what created the hole, whether plumbing was "
                  "involved, whether an access panel was framed, or how the texture was matched.",
         theme="Ceiling repair", source=181, access="search-extract", identity="indexed",
         negative=False, exactTask=False),
    dict(id="R61", business="w6-caledonia-plastering-stucco-inc", platform="Thumbtack",
         author="Joe M.", published="Jul 26, 2018",
         quote="John did a great job repairing our ceiling plaster with minimal hassle",
         analysis="Ceiling plaster repair described as low-disruption. Supports capability on "
                  "plaster ceilings in occupied homes; \u201cminimal hassle\u201d is a customer's "
                  "characterisation, not a measured dust, noise or access outcome.",
         theme="Ceiling repair", source=181, access="search-extract", identity="indexed",
         negative=False, exactTask=False),
    dict(id="R62", business="w6-caledonia-plastering-stucco-inc", platform="Thumbtack",
         author="Karl W.", published="Dec 12, 2016",
         quote="John did a great job adding a veneer plaster to a newly drywalled ceiling. He "
               "was easy to communicate with, friendly, and took great care of the space. The "
               "finish of the ceiling was amazing, he truly is a pro. Highly recommended.",
         analysis="Shows veneer plaster applied over new drywall on a ceiling \u2014 the exact "
                  "combination needed when a modern drywall patch meets an older plaster "
                  "ceiling. \u201cTook great care of the space\u201d is relevant to working above an "
                  "occupied unit but is one customer's account.",
         theme="Finish work", source=181, access="search-extract", identity="indexed",
         negative=False, exactTask=False),
    dict(id="R63", business="w6-caledonia-plastering-stucco-inc", platform="Thumbtack",
         author="John L.", published="Nov 12, 2018",
         quote="John did great work patching several interior and exterior holes made by an "
               "electrician. He took extra care to set up and clean up to avoid making a mess. I "
               "would recommend.",
         analysis="Patching holes left behind by another trade, with deliberate set-up and "
                  "clean-up. That is the same coordination pattern as closing an opening made "
                  "for a plumber, and the containment comment is the most relevant detail in "
                  "wave 6 for work above an occupied unit.",
         theme="Clean work", source=181, access="search-extract", identity="indexed",
         negative=False, exactTask=False),
    dict(id="R64", business="w6-caledonia-plastering-stucco-inc", platform="Thumbtack",
         author="Eric S.", published="Jan 27, 2019",
         quote="Really great work repairing our plaster wall around a heater. Almost doesn't "
               "needs painting",
         analysis="Repair around an existing penetration with a finish close enough that "
                  "painting was nearly unnecessary. Supports finish-matching skill on plaster; "
                  "the excerpt is a wall, not a ceiling, and the reviewer's grammar is "
                  "reproduced as published.",
         theme="Finish work", source=181, access="search-extract", identity="indexed",
         negative=False, exactTask=False),
    dict(id="R65", business="w6-caledonia-plastering-stucco-inc", platform="Thumbtack",
         author="Not reliably resolved in extract", published=None,
         quote="His lath and plaster pass the city inspection with no problems.",
         analysis="The single most compliance-relevant sentence found in wave 6: a customer "
                  "states that this business's lath and plaster work passed city inspection. It "
                  "is an unattributed excerpt with no visible date, it does not name the "
                  "inspection type, and a customer's account of an inspection is not an official "
                  "inspection record. Treated as a lead to raise with the business, not as "
                  "proof.",
         theme="Permit & inspection", source=181, access="search-extract",
         identity="indexed", negative=False, exactTask=False),
]
for r in REVIEWS:
    r["checkedAt"] = DATE
    assert len(r["quote"]) < 500 and len(r["analysis"]) > 30, r["id"]

# link every review to its business (two-way reference, checked again on merge)
_by_id = {b["id"]: b for b in BUSINESSES}
for r in REVIEWS:
    assert r["id"] not in _by_id[r["business"]]["reviewIds"], r["id"]
    _by_id[r["business"]]["reviewIds"].append(r["id"])

# --------------------------------------------------------------------------
wave = {
    "wave": 6,
    "researchedAt": DATE,
    "note": "50 new records: 22 with a CSLB license detail page read directly this session, "
            "16 registry-only leads held fail-closed, 12 drywall/plaster/finish leads from "
            "indexed extracts. Nothing promoted to the qualified master list.",
    "businesses": BUSINESSES,
    "sources": SOURCES,
    "reviews": REVIEWS,
}

ids = [b["id"] for b in BUSINESSES]
names = [b["name"].lower() for b in BUSINESSES]
assert len(BUSINESSES) == 50, f"expected 50 records, got {len(BUSINESSES)}"
assert len(set(ids)) == 50, "duplicate ids inside wave 6"
assert len(set(names)) == 50, "duplicate names inside wave 6"
src_ids = {s["id"] for s in SOURCES}
assert len(src_ids) == len(SOURCES), "duplicate source ids"
assert max(src_ids) <= 196 and min(src_ids) >= 150
for b in BUSINESSES:
    for c in b["claims"]:
        assert c["source"] in src_ids, (b["id"], c["source"])
        assert c["text"].strip() and c["excerpt"].strip(), b["id"]
    for f in b["flags"]:
        assert f["sources"] and all(s in src_ids for s in f["sources"]), b["id"]
    if b.get("website"):
        assert b["websiteSource"] in src_ids, b["id"]
    if b.get("phone"):
        assert b["phoneSource"] in src_ids, b["id"]
    if b.get("license"):
        assert b["license"]["source"] in src_ids, b["id"]
        assert SRC[b["license"]["source"]]["kind"] == "government", b["id"]
        assert "cslb.ca.gov" in SRC[b["license"]["source"]]["url"], b["id"]
for r in REVIEWS:
    assert r["business"] in set(ids), r["id"]
    assert r["source"] in src_ids, r["id"]

(ROOT / "data" / "wave6.json").write_text(
    json.dumps(wave, indent=1, ensure_ascii=False) + "\n")
active = sum(1 for b in BUSINESSES if b.get("license") and b["license"]["status"] == "active")
print(f"wrote wave6.json: {len(BUSINESSES)} businesses, {len(SOURCES)} sources, "
      f"{len(REVIEWS)} reviews | {len(L)-1} CSLB reads in wave, {active} active, "
      f"{sum(1 for b in BUSINESSES if b.get('license') and b['license']['status']!='active')} "
      f"not active")
