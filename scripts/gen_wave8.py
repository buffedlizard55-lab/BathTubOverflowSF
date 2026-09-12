#!/usr/bin/env python3
"""Generate wave 8: 50 new, collision-checked plumbing/restoration records.

Research snapshot: 2026-09-12.

Composition
-----------
* 23 plumbing-primary records (13 active, 10 non-active/historical)
* 27 general-building/restoration records (all active)
* 50 distinct CSLB detail pages read directly
* 17 completed plumbing permits in work-location ZIP 94122
* 27 completed building permits in work-location ZIP 94122
* one additional historical building permit for Frank J O'Brien

The City permit sources are split deliberately: contact datasets establish the
license-to-permit linkage; permit datasets establish location, completion date,
and scope. A permit is historical work evidence, never a current dispatch
promise or a workmanship endorsement. Review text is retained only where the
business identity can be matched without relying on a similar name alone.
Nothing in this wave is promoted to the qualified master list.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-12"
OUT = ROOT / "data" / "wave8.json"


def cslb(number: str) -> str:
    return (
        "https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/"
        f"LicenseDetail.aspx?LicNum={number}"
    )


def disclosure(number: str) -> str:
    return (
        "https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/"
        f"ComplaintDisclosure.aspx?LicType=LIC&LicNum={number}"
    )


def soda(dataset: str, select: str, where: str, order: str = "", limit: int = 200) -> str:
    query = {"$select": select, "$where": where, "$limit": str(limit)}
    if order:
        query["$order"] = order
    return f"https://data.sf.gov/resource/{dataset}.json?{urlencode(query)}"


# Source IDs continue from the wave-7 merged maximum (221).
P_CONTACTS = 222
P_DETAILS = 223
P_HISTORICAL = 224
B_CONTACTS = 225
B_DETAILS = 226
B_OBRIEN = 227
CSLB_FIRST = 228

# Public business/platform sources. Their IDs are fixed so claims stay stable.
FLOW_SITE, FLOW_YELP = 278, 279
HOLLAND_YELP, HOLLAND_JUDYS = 280, 281
PANHANDLE_BUILDZOOM = 282
AXION_SITE, AXION_NEXTDOOR, AXION_YELP = 283, 284, 285
PROCARE_SITE, PROCARE_BIRDEYE, PROCARE_YAHOO = 286, 287, 288
BAYMETRO_SITE, BAYMETRO_GUILD, BAYMETRO_YELP = 289, 290, 291
BRUS_SITE, BRUS_YELP, BRUS_YAHOO = 292, 293, 294
BOLD_SITE = 295
HARGENS_SITE, HARGENS_YELP, HARGENS_NEXTDOOR, HARGENS_BUILDZOOM = 296, 297, 298, 299
SAFESTEP_BBB, SAFESTEP_CONSUMER = 300, 301
CHEN_DISCLOSURE, SHEK_DISCLOSURE, GERSON_DISCLOSURE = 302, 303, 304
SF_CODE_104_2 = 305


# Completed plumbing permit selections. These were selected only after joining
# the permit-contact rows by permit number and checking work-location ZIP 94122.
P_PERMITS = {
    "817607": ("PP20190501385", "2019-05-06", "replacement of main sewer"),
    "887553": ("PW20240812801", "2024-08-16", "replace sewer lateral and water-main services"),
    "902830": ("PW20190501695", "2019-08-26", "install bypass backflow on existing fire-service backflow"),
    "1028751": ("PW20241212759", "2025-05-07", "remodel bathroom and kitchen and add a bathroom"),
    "498866": ("PW20260320521", "2026-09-02", "half-bath/powder-room and roof-drain work"),
    "957727": ("PW20221005482", "2022-10-14", "reopened final for kitchen waterlines and bathroom-sink waste line"),
    "975509": ("PW20250331196", "2025-04-08", "replace 25 feet of sewer pipe and a house trap"),
    "1122605": ("PP20260813825", "2026-08-18", "house-trap replacement and possible main-line spot repair"),
    "814802": ("PP20080528027", "2008-10-15", "four new bathrooms, water piping, tubs and shower fixtures"),
    "1115284": ("PW20240627846", "2024-09-26", "repair sewer line and house trap"),
    "488896": ("PP20230517004", "2023-05-30", "legalization work in a kitchen area"),
    "581431": ("PP20120124951", "2012-06-21", "new kitchen, bathroom, powder-room, laundry and gas-line plumbing"),
    "900145": ("PP20110207859", "2011-04-19", "commercial sinks, grease trap, floor drain and gas line"),
    "942224": ("PP20100621871", "2010-06-21", "new sewer in the street"),
    "811534": ("PP20080125460", "2008-02-21", "kitchen remodel"),
    "406739": ("PP20101004304", "2010-10-12", "kitchen, bathroom and laundry-room water-pipe work"),
    "667361": ("PP20100930251", "2011-03-01", "gas line and ground-floor kitchen/bathroom remodeling"),
}

# Completed building-permit selections. Scope text is conservatively condensed
# from the official description; the source URL exposes the complete field.
B_PERMITS = {
    "850352": ("202605181462", "2026-08-14", "fire-damage framing and drywall repair"),
    "361402": ("202603318629", "2026-06-24", "remove plaster ceiling and install drywall"),
    "1090249": ("202603318559", "2026-09-08", "water-damage drywall, tape, texture and paint"),
    "1002753": ("202603308518", "2026-07-10", "new drywall, tape and smooth finish"),
    "1082165": ("202603258250", "2026-05-13", "tub work and drywall patching"),
    "1119854": ("202603187849", "2026-06-30", "tub relocation, new drywall and insulation"),
    "1141495": ("202603026793", "2026-09-03", "drain/supply, bathroom, framing and drywall work"),
    "1142594": ("202602045258", "2026-07-17", "in-kind drywall and roof-ceiling repair"),
    "1022801": ("202601133757", "2026-03-30", "old/new sheetrock and small framing work"),
    "944813": ("202512151795", "2026-01-02", "wall and ceiling sheetrock"),
    "1064544": ("202512081247", "2026-03-10", "ceiling drywall replacement"),
    "1132400": ("202511260567", "2026-01-02", "remediation with drywall removal and replacement"),
    "1018292": ("202511250390", "2026-01-28", "water-damage drywall on walls and ceilings"),
    "855109": ("202507140728", "2025-12-05", "bath remodel with wall/ceiling drywall removal and replacement"),
    "937457": ("202506027697", "2025-09-02", "approximately 1,600 square feet of drywall"),
    "1008141": ("202505196742", "2026-06-04", "bathroom work and sheetrock"),
    "773300": ("202505075931", "2025-08-21", "kitchen sheetrock with plumbing/electrical work"),
    "1072943": ("202504174635", "2025-05-16", "framing to cover duct and drywall"),
    "697522": ("202501077889", "2025-05-07", "bathroom rebuild with plumbing, drywall and tile"),
    "701864": ("202412187085", "2025-02-11", "mold/damaged sheetrock and repair after plumbing leakage"),
    "592325": ("202411124782", "2025-02-06", "water-damage drywall repair and plumbing-leak repair"),
    "900156": ("202411054443", "2025-07-22", "bathroom/kitchen work and wall/ceiling sheetrock"),
    "1108341": ("202605141289", "2026-08-19", "exploratory ceiling demolition for design drawings"),
    "1057565": ("202408239341", "2025-03-21", "sheetrock, bathroom and insulation work"),
    "1031942": ("202410012093", "2025-03-31", "multiple-bathroom remodel work"),
    "754201": ("202512111572", "2026-07-30", "wall/ceiling demolition and patching after electrical work"),
    "998906": ("202412126731", "2025-09-15", "kitchen/bathroom work and sheetrock"),
}


def row(
    number: str,
    name: str,
    phone: str,
    address: str,
    form: str,
    classes: list[str],
    expires: str,
    trade: str,
    *,
    status: str = "active",
    outer: bool = False,
    website: str | None = None,
    website_source: int | None = None,
) -> dict:
    return {
        "number": number,
        "name": name,
        "phone": phone,
        "address": address,
        "form": form,
        "classes": classes,
        "expires": expires,
        "trade": trade,
        "license_status": status,
        "outer": outer,
        "website": website,
        "websiteSource": website_source,
    }


# Final collision-vetted cohort. Oran Plumbing #762214 and New Golden State
# Plumbing #778200 were rejected before this list because their license numbers
# already occur in the merged dataset. Euro Plumbing #1028917 was also rejected
# because the regulator's business name did not match the discovery identity.
CANDIDATES = [
    row("817607", "Holland Plumbing Works", "415-205-1235", "2072 15th Avenue, San Francisco, CA 94116", "Corporation", ["C36"], "2027-02-28", "plumbing"),
    row("887553", "Glenn's Plumbing", "415-290-1749", "1460 41st Avenue, San Francisco, CA 94122", "Sole Ownership", ["C36"], "2026-11-30", "plumbing", outer=True),
    row("902830", "R E M Boiler and Plumbing", "415-216-3247", "1495 7th Avenue #2, San Francisco, CA 94122", "Sole Ownership", ["C-4", "C36"], "2027-08-31", "plumbing"),
    row("1028751", "Panhandle Plumbing", "415-240-1983", "2114 44th Avenue, San Francisco, CA 94116", "Sole Ownership", ["C36"], "2027-07-31", "plumbing", outer=True),
    row("791342", "Impressive Plumbing", "415-797-0246", "PO Box 5311, Hercules, CA 94547", "Sole Ownership", ["C36"], "2027-02-28", "plumbing"),
    row("498866", "O'Connor Plumbing & Fire Protection Inc", "650-344-4424", "360 Swift Avenue, South San Francisco, CA 94080", "Corporation", ["C16", "C36"], "2028-04-30", "plumbing"),
    row("957727", "Flow Form Plumbing", "415-294-1588", "5885 Scarborough Drive, Oakland, CA 94611", "Sole Ownership", ["C36"], "2028-08-31", "plumbing", website="https://flowformplumbing.blogspot.com/p/flow-form-plumbing.html", website_source=FLOW_SITE),
    row("975509", "L & Y Plumbing", "415-823-2649", "1349 48th Avenue, San Francisco, CA 94122", "Partnership", ["C36"], "2028-08-31", "plumbing", outer=True),
    row("1122605", "Axion Plumbing", "415-672-0249", "930 Ortega Street, San Francisco, CA 94122", "Corporation", ["C36"], "2028-06-30", "plumbing", website="https://axionplumbing.com/", website_source=AXION_SITE),
    row("814802", "Chen's Construction and Mechanical Inc", "415-710-8777", "396 Forbes Boulevard Suite C, South San Francisco, CA 94080", "Corporation", ["A", "B", "C10", "C16", "C20", "C36", "C38"], "2028-07-31", "plumbing"),
    row("1115284", "DC Plumbing LLC", "415-671-9698", "1659 23rd Avenue, San Francisco, CA 94122", "Ltd Liability", ["C36"], "2028-01-31", "plumbing", outer=True),
    row("343837", "Frank J O'Brien", "415-987-5903", "1579 35th Avenue, San Francisco, CA 94122", "Sole Ownership", ["B", "C10", "C36"], "2027-01-31", "multi-trade", outer=True),
    row("488896", "Peter So Company", "415-205-0625", "1570 46th Avenue, San Francisco, CA 94122", "Sole Ownership", ["B", "C36"], "2028-03-31", "multi-trade", outer=True),
    row("306841", "Shek's Plumbing", "415-271-9837", "1323 21st Avenue, San Francisco, CA 94122", "Sole Ownership", ["C36"], "2006-07-24", "plumbing", status="revoked"),
    row("581431", "Le's Plumbing & Construction Co", "415-377-3470", "1662 Great Highway, San Francisco, CA 94122", "Sole Ownership", ["C36", "B"], "2027-09-30", "multi-trade", status="suspended", outer=True),
    row("693052", "Applied Plumbing Company", "415-759-8247", "1334 39th Avenue, San Francisco, CA 94122", "Sole Ownership", ["C36"], "2012-06-30", "plumbing", status="expired", outer=True),
    row("900145", "Morrison Plumbing", "415-728-4343", "965 Alice Lane #3, Menlo Park, CA 94025", "Sole Ownership", ["C36"], "2025-07-31", "plumbing", status="expired"),
    row("811534", "Walsemann Mechanical", "415-531-4540", "1618 46th Avenue, San Francisco, CA 94122", "Sole Ownership", ["C36"], "2008-08-31", "plumbing", status="expired", outer=True),
    row("667361", "City Construction Inc", "415-509-5025", "3649 Lawton Street #622, San Francisco, CA 94122", "Corporation", ["B", "C10", "C36"], "2015-04-30", "multi-trade", status="expired", outer=True),
    row("942224", "Tully Plumbing", "415-425-2065", "1436 Ingalls Street, San Francisco, CA 94124", "Sole Ownership", ["C36"], "2030-01-31", "plumbing", status="inactive"),
    row("908590", "Almo Plumbing", "415-374-3071", "1554 45th Avenue, San Francisco, CA 94122", "Sole Ownership", ["C36"], "2028-01-31", "plumbing", status="inactive", outer=True),
    row("406739", "Polytec Construction Company Inc", "415-751-5197", "2470 35th Avenue, San Francisco, CA 94116", "Corporation", ["B", "C16", "C20", "C38", "C36", "A", "C10"], "2013-03-23", "multi-trade", status="canceled"),
    row("520892", "Meridian Plumbing Company Inc", "415-531-0109", "1245 27th Avenue, San Francisco, CA 94122", "Corporation", ["C16", "C36"], "2011-10-28", "plumbing", status="canceled"),
    row("850352", "Bay Metro Corporation", "415-626-4067", "2339 Third Street #5, San Francisco, CA 94107", "Corporation", ["B", "C36"], "2026-11-30", "multi-trade", website="https://www.baymetrocorp.com/", website_source=BAYMETRO_SITE),
    row("361402", "Sarris Construction", "415-621-1281", "131 Fillmore Street, San Francisco, CA 94117", "Sole Ownership", ["B"], "2028-07-31", "general"),
    row("1090249", "Pro-Care Restoration Inc", "510-807-2473", "23673 Connecticut Street Suite 10, Hayward, CA 94545", "Corporation", ["B", "C22"], "2028-04-30", "general", website="https://www.pro-carerestoration.com/", website_source=PROCARE_SITE),
    row("1002753", "Buck Construction", "415-370-0996", "2820 Kirkham Street, San Francisco, CA 94122", "Sole Ownership", ["B"], "2027-04-30", "general", outer=True),
    row("1082165", "Safe Step Walk In Tub LLC", "714-373-8545", "520 Royal Parkway Suite 100, Nashville, TN 37214", "Ltd Liability", ["B"], "2027-10-31", "general"),
    row("1119854", "Raxe Construction Inc", "925-232-1325", "330 Hillsdale Drive, Pittsburg, CA 94565", "Corporation", ["B"], "2028-04-30", "general"),
    row("1141495", "Brus Box Contractor Works", "415-608-4090", "643 Sylvan Street #2, Daly City, CA 94014", "Corporation", ["B"], "2027-08-31", "general", website="https://brusbox.us/", website_source=BRUS_SITE),
    row("1142594", "O'Neil Engineering Inc", "415-309-0186", "1534 Plaza Lane #307, Burlingame, CA 94010", "Corporation", ["A", "B"], "2027-08-31", "general"),
    row("1022801", "Precise Construcion", "510-472-8438", "420 Pendleton Way, Oakland, CA 94621", "Sole Ownership", ["B"], "2027-01-31", "general"),
    row("944813", "Solid Design Construction", "415-988-3844", "1691 40th Avenue, San Francisco, CA 94122", "Sole Ownership", ["B"], "2028-03-31", "general", outer=True),
    row("1064544", "Kelun Construction", "415-602-6515", "1220 Tasman Drive Space 428, Sunnyvale, CA 94089", "Corporation", ["B"], "2028-03-31", "general"),
    row("1132400", "RPRW Inc dba James Macmillan", "415-250-8453", "200 Bolinas Road Apartment 49, Fairfax, CA 94930", "Corporation", ["B"], "2027-01-31", "general"),
    row("1018292", "Bold Restoration Inc", "510-315-7056", "2114 Adams Avenue, San Leandro, CA 94577", "Corporation", ["B", "C-2", "D39", "C33"], "2026-11-30", "general", website="https://boldrestoration.com/", website_source=BOLD_SITE),
    row("855109", "Yong Hong Construction Inc", "510-723-0088", "27688 Industrial Boulevard, Hayward, CA 94545", "Corporation", ["B"], "2027-02-28", "general"),
    row("937457", "Cleanair Image Inc dba Servpro of Belmont / San Carlos", "650-591-4137", "PO Box 422, San Carlos, CA 94070", "Corporation", ["B"], "2027-09-30", "general"),
    row("1008141", "Blue Wood Construction Inc", "415-860-6303", "745 Vienna Street, San Francisco, CA 94112", "Corporation", ["B", "C-7", "C10", "C36"], "2027-10-31", "multi-trade"),
    row("773300", "Constantine Construction", "415-613-3734", "736 Kansas Street, San Francisco, CA 94107", "Sole Ownership", ["B", "C36"], "2028-01-31", "multi-trade"),
    row("1072943", "BAA General Builder", "415-317-7069", "3149 Vicente Street, San Francisco, CA 94116", "Corporation", ["B", "C36"], "2028-01-31", "multi-trade"),
    row("697522", "Kobliska Construction", "415-819-6976", "581 Pennsylvania Avenue, San Francisco, CA 94107", "Sole Ownership", ["B"], "2026-10-31", "general"),
    row("701864", "Spotlight Construction Groups Inc", "415-716-4962", "543 Campbell Avenue, San Francisco, CA 94134", "Corporation", ["B", "D34"], "2027-06-30", "general"),
    row("592325", "Hargens Inc", "650-876-1801", "483 Victory Avenue, South San Francisco, CA 94080", "Corporation", ["B", "C33", "C43", "C20", "C36"], "2028-04-30", "multi-trade", website="https://www.hargensinc.com/", website_source=HARGENS_SITE),
    row("900156", "Simply Building Inc", "415-606-1406", "6170 Skyline Boulevard, Burlingame, CA 94010", "Corporation", ["B", "C36", "C15"], "2028-04-30", "multi-trade"),
    row("1108341", "Gerson Construction Inc", "415-713-5181", "355 Hale Street, San Francisco, CA 94134", "Corporation", ["B"], "2027-08-31", "general"),
    row("1057565", "Alpha Construction & Solutions Inc", "415-828-9984", "350 Wheeler Avenue, San Francisco, CA 94134", "Corporation", ["B", "C10", "C36"], "2027-08-31", "multi-trade"),
    row("1031942", "Winwin Construction Inc", "415-828-3918", "1258 36th Avenue, San Francisco, CA 94122", "Corporation", ["B"], "2027-10-31", "general", outer=True),
    row("754201", "Wolfe Painting Co", "415-235-6227", "190 Alexander Avenue, Daly City, CA 94014", "Sole Ownership", ["C33", "B"], "2026-09-30", "general"),
    row("998906", "Yong and Zhuo Construction Inc", "415-254-9978", "1882 Donner Avenue, San Francisco, CA 94124", "Corporation", ["B"], "2026-12-31", "general"),
]

assert len(CANDIDATES) == 50
assert len({r["number"] for r in CANDIDATES}) == 50
assert sum(r["trade"] in {"plumbing", "multi-trade"} for r in CANDIDATES[:23]) == 23
assert sum(r["license_status"] == "active" for r in CANDIDATES) == 40

plumbing_permit_ids = [v[0] for v in P_PERMITS.values()]
building_permit_ids = [v[0] for v in B_PERMITS.values()]
plumbing_numbers = [r["number"] for r in CANDIDATES[:23]]
building_numbers = [r["number"] for r in CANDIDATES[23:]]

SOURCES = [
    {
        "id": P_CONTACTS,
        "title": "SF DBI · plumbing permit-contact mappings for selected wave-8 licenses",
        "url": soda(
            "k6kv-9kix",
            "permit_number,license_number,firm_name,address,city,zipcode,phone",
            "license_number in (" + ",".join(f"'{n}'" for n in plumbing_numbers) + ") and permit_number in (" + ",".join(f"'{p}'" for p in plumbing_permit_ids) + ")",
            "license_number,permit_number",
            100,
        ),
        "kind": "government",
        "access": "page",
        "checkedAt": DATE,
        "note": "Official SF DBI Plumbing Permits Contacts query. It establishes only the historical permit-contact/license linkage; it does not state current CSLB status, present dispatch coverage, or workmanship.",
    },
    {
        "id": P_DETAILS,
        "title": "SF DBI · selected completed plumbing permits in work-location ZIP 94122",
        "url": soda(
            "a6aw-rudh",
            "permit_number,status,completed_date,description,street_number,street_name,street_suffix,zipcode",
            "permit_number in (" + ",".join(f"'{p}'" for p in plumbing_permit_ids) + ")",
            "permit_number",
            100,
        ),
        "kind": "government",
        "access": "page",
        "checkedAt": DATE,
        "note": "Official plumbing-permit rows selected after the contact join. Each retained row was checked for completed status and work-location ZIP 94122. Scope descriptions are historical facts, not proof of exact trip-lever skill.",
    },
    {
        "id": P_HISTORICAL,
        "title": "SF DBI · historical 94122 permit-contact rows for Impressive Plumbing and Almo Plumbing",
        "url": soda(
            "k6kv-9kix",
            "permit_number,license_number,firm_name,address,city,zipcode,phone",
            "license_number in ('791342','908590') and zipcode like '94122%'",
            "license_number",
            50,
        ),
        "kind": "government",
        "access": "page",
        "checkedAt": DATE,
        "note": "Historical contractor-contact ZIP evidence only. The strict completed-work-location join did not return a selected completed 94122 permit for either license.",
    },
    {
        "id": B_CONTACTS,
        "title": "SF DBI · building-permit contact mappings for 27 restoration licenses and Frank J O'Brien",
        "url": soda(
            "3pee-9qhc",
            "permit_number,firm_name,license1,role,firm_address,firm_city,firm_zipcode",
            "license1 in (" + ",".join(f"'{n}'" for n in building_numbers + ["343837"]) + ") and permit_number in (" + ",".join(f"'{p}'" for p in building_permit_ids + ["200408040636"]) + ")",
            "license1,permit_number",
            200,
        ),
        "kind": "government",
        "access": "page",
        "checkedAt": DATE,
        "note": "Official building-permit contact rows. Extra contacts can exist on a permit; claims use only the selected license/permit pair and do not infer that every contact performed every task.",
    },
    {
        "id": B_DETAILS,
        "title": "SF DBI · selected completed restoration permits in work-location ZIP 94122",
        "url": soda(
            "i98e-djp9",
            "permit_number,status,completed_date,description,street_number,street_name,street_suffix,zipcode",
            "permit_number in (" + ",".join(f"'{p}'" for p in building_permit_ids) + ")",
            "permit_number",
            100,
        ),
        "kind": "government",
        "access": "page",
        "checkedAt": DATE,
        "note": "Official building-permit details checked for complete status and work-location ZIP 94122. Descriptions support only the work words actually shown.",
    },
    {
        "id": B_OBRIEN,
        "title": "SF DBI · Frank J O'Brien building permit 200408040636",
        "url": soda(
            "i98e-djp9",
            "permit_number,status,completed_date,description,street_number,street_name,street_suffix,zipcode",
            "permit_number='200408040636'",
            limit=10,
        ),
        "kind": "government",
        "access": "page",
        "checkedAt": DATE,
        "note": "Official historical building-permit detail for a 94122 kitchen remodel. It is retained as local-work evidence only and does not establish present availability or the requested repair skill.",
    },
]

# One directly read CSLB source per candidate. Source notes preserve the exact
# business form, address, phone, status, classifications, and displayed expiry.
for index, r in enumerate(CANDIDATES):
    sid = CSLB_FIRST + index
    classes = ", ".join(r["classes"])
    SOURCES.append({
        "id": sid,
        "title": f"CSLB · {r['number']} · {r['name']}",
        "url": cslb(r["number"]),
        "kind": "government",
        "access": "page",
        "checkedAt": DATE,
        "note": (
            f"License detail page read directly. Business name {r['name']}; {r['form']}; "
            f"address {r['address']}; phone {r['phone']}; status {r['license_status']}; "
            f"classifications {classes}; displayed expiry {r['expires']}. Bond and workers-"
            "compensation sections were also read, but they do not verify project-specific coverage."
        ),
    })

SOURCES.extend([
    {"id": FLOW_SITE, "title": "Flow Form Plumbing · historical business page", "url": "https://flowformplumbing.blogspot.com/p/flow-form-plumbing.html", "kind": "business", "access": "page", "checkedAt": DATE, "note": "Business-hosted page identifies C. Alec Miller, phone 415-294-1588 and service/repair work in San Francisco. The exact phone matches the current CSLB record; the page is visibly legacy material and is not treated as a current dispatch promise."},
    {"id": FLOW_YELP, "title": "Yelp · Flow Form Plumbing indexed profile", "url": "https://www.yelp.com/biz/flow-form-plumbing-san-francisco-3", "kind": "platform", "access": "search-extract", "checkedAt": DATE, "note": "Direct Yelp access returned an access barrier; the indexed profile supplied exact name, phone, San Francisco service-area text, business specialty, photos and short review highlights. The 53-review corpus was not read."},
    {"id": HOLLAND_YELP, "title": "Yelp · Holland Plumbing Works indexed profile", "url": "https://www.yelp.com/biz/holland-plumbing-works-san-francisco", "kind": "platform", "access": "search-extract", "checkedAt": DATE, "note": "Indexed profile matches the CSLB business by exact name, phone and San Francisco location. One short review excerpt was accessible; the 13-review corpus was not read."},
    {"id": HOLLAND_JUDYS, "title": "Judy's Book · Holland Plumbing Works · Citysearch-fed reviews", "url": "https://www.judysbook.com/Holland-Plumbing-Works-BtoB~Plumbing-Contractors-sanfrancisco-r29770409.htm", "kind": "directory", "access": "page", "checkedAt": DATE, "note": "Direct page read. Exact name and phone match, and both displayed Citysearch-fed reviews were read. One task-adjacent 2011 shower-handle mechanism account is selected below; the other concerns a water heater. These old syndicated accounts do not establish current availability."},
    {"id": PANHANDLE_BUILDZOOM, "title": "BuildZoom · Panhandle Plumbing", "url": "https://www.buildzoom.com/contractor/panhandle-plumbing-san-francisco-ca", "kind": "directory", "access": "page", "checkedAt": DATE, "note": "Profile matches exact name, phone, address and license 1028751. One dated review is shown. BuildZoom's score and license summary are not substituted for the direct CSLB read."},
    {"id": AXION_SITE, "title": "Axion Plumbing · official site", "url": "https://axionplumbing.com/", "kind": "business", "access": "page", "checkedAt": DATE, "note": "Business-hosted site markets leak detection and pipe repair and prints 415-286-3451. CSLB prints a different business phone, 415-672-0249; both are preserved as a discrepancy rather than reconciled by assumption."},
    {"id": AXION_NEXTDOOR, "title": "Nextdoor · Axion Plumbing recommendations", "url": "https://nextdoor.com/pages/axion-plumbing-san-francisco-ca/", "kind": "platform", "access": "search-extract", "checkedAt": DATE, "note": "Indexed profile prints license 1122605, address 930 Ortega Street, website and public phone, safely tying two displayed recommendations to this entity. The full Nextdoor corpus was not read."},
    {"id": AXION_YELP, "title": "Yelp · Axion Plumbing indexed result", "url": "https://www.yelp.com/search?find_desc=axion&find_loc=San+Francisco%2C+CA", "kind": "platform", "access": "search-extract", "checkedAt": DATE, "note": "Search extract located the San Francisco Axion Plumbing profile and one short highlight. It is retained as a platform link only because the spelling in the quote says Axiom and a complete review was not exposed."},
    {"id": PROCARE_SITE, "title": "Pro-Care Restoration · official site", "url": "https://www.pro-carerestoration.com/", "kind": "business", "access": "page", "checkedAt": DATE, "note": "Official site matches CSLB phone and business name; markets water, fire, mold, structural repair and complete restoration, and explicitly lists San Francisco County in its service area."},
    {"id": PROCARE_BIRDEYE, "title": "Birdeye · Pro-Care Restoration · Google-republished reviews", "url": "https://reviews.birdeye.com/pro-care-restoration-inc-171673259657633", "kind": "platform", "access": "page", "checkedAt": DATE, "note": "Direct page read. It labels five rows as Google reviews. Two pairs carry verbatim duplicate text under different author labels; each duplicated text is retained only once and the irregularity is flagged. This is not the original Google review panel."},
    {"id": PROCARE_YAHOO, "title": "Yahoo Local · Pro-Care Restoration · Yelp-fed excerpts", "url": "https://local.yahoo.com/info-235468637-procare-restoration-hayward/", "kind": "platform", "access": "page", "checkedAt": DATE, "note": "Direct page read. Exact phone and official website match the business. Yahoo exposes four dated Yelp-fed excerpts, all retained with truncation made explicit; the complete Yelp reviews were not retrieved."},
    {"id": BAYMETRO_SITE, "title": "Bay Metro Corporation · official site", "url": "https://www.baymetrocorp.com/", "kind": "business", "access": "page", "checkedAt": DATE, "note": "Official site matches CSLB business name, San Francisco address and phone and describes restoration/reconstruction and remodeling work."},
    {"id": BAYMETRO_GUILD, "title": "GuildQuality · Bay Metro Corporation", "url": "https://www.guildquality.com/profile/bay-metro-corporation", "kind": "platform", "access": "search-extract", "checkedAt": DATE, "note": "Profile identity matches CSLB by exact business name, street address and phone. Three dated San Francisco excerpts were accessible in the search result; direct page markup did not expose the individual text. The full survey corpus is incomplete."},
    {"id": BAYMETRO_YELP, "title": "Yelp · Bay Metro Corporation indexed profile", "url": "https://www.yelp.com/biz/bay-metro-corporation-san-francisco", "kind": "platform", "access": "search-extract", "checkedAt": DATE, "note": "Indexed profile matches the legal name and San Francisco identity and exposes three review highlights. It is retained as a manual-inspection link; those highlights are not duplicated into the selected review sample."},
    {"id": BRUS_SITE, "title": "BrusBox · official site", "url": "https://brusbox.us/", "kind": "business", "access": "page", "checkedAt": DATE, "note": "Official site matches CSLB phone and markets San Francisco-area bathroom remodeling, plumbing and repairs. The CSLB record carries B only, not C-36; plumbing self-performance therefore remains unverified."},
    {"id": BRUS_YELP, "title": "Yelp · Brus Box Contractor Works indexed profile", "url": "https://www.yelp.com/biz/brus-box-contractor-works-san-francisco", "kind": "platform", "access": "search-extract", "checkedAt": DATE, "note": "Indexed profile matches exact name and phone and lists bathtub repair, drain repair and plumbing among platform-verified services. The full 62-review corpus was not read."},
    {"id": BRUS_YAHOO, "title": "Yahoo Local · Brus Box Contractor Works · Yelp-fed excerpts", "url": "https://local.yahoo.com/info-232677711-brus-box-contractor-works-san-francisco/", "kind": "platform", "access": "page", "checkedAt": DATE, "note": "Direct page read. Exact business name and phone match; five Yelp-fed excerpts were visible and three task-adjacent excerpts were retained. Text remains truncated and is not a complete Yelp corpus."},
    {"id": BOLD_SITE, "title": "Bold Restoration · official site", "url": "https://boldrestoration.com/", "kind": "business", "access": "page", "checkedAt": DATE, "note": "Business-hosted site markets damage restoration. Its claims are retained separately from the direct CSLB record and selected official permit."},
    {"id": HARGENS_SITE, "title": "Hargens Inc · official site", "url": "https://www.hargensinc.com/", "kind": "business", "access": "page", "checkedAt": DATE, "note": "Official site matches current CSLB Victory Avenue address and phone. It describes water/fire-damage building repair and carries two business-hosted testimonials; one restoration account is retained as a testimonial, not independent review evidence."},
    {"id": HARGENS_YELP, "title": "Yelp · Hargens indexed profile", "url": "https://www.yelp.com/biz/hargens-south-san-francisco-2", "kind": "platform", "access": "search-extract", "checkedAt": DATE, "note": "Indexed page matches exact name, phone and South San Francisco identity; it exposes three short review highlights and markets remodeling, disaster recovery and plumbing. The complete 21-review corpus was not read."},
    {"id": HARGENS_NEXTDOOR, "title": "Nextdoor · Hargens Inc", "url": "https://nextdoor.com/pages/hargens-inc-south-san-francisco-ca/", "kind": "platform", "access": "search-extract", "checkedAt": DATE, "note": "Indexed profile matches exact phone and business identity. Its generated summary mentions rebuilding after a fire-suppression leak and later bathroom remodeling, but no underlying named excerpt was safely attributable, so it is a platform link only."},
    {"id": HARGENS_BUILDZOOM, "title": "BuildZoom · Hargens Inc", "url": "https://www.buildzoom.com/contractor/hargens-inc", "kind": "directory", "access": "search-extract", "checkedAt": DATE, "note": "Third-party profile matches license 592325 and phone and shows relevant permits. Official SF permit data, not BuildZoom's score, supports the permit claims in this dataset."},
    {"id": SAFESTEP_BBB, "title": "BBB · national Safe Step Walk-In Tub profile · rejected review corpus", "url": "https://www.bbb.org/us/tn/nashville/profile/walk-in-bathtubs/safe-step-walk-in-tub-0573-37032409/customer-reviews", "kind": "directory", "access": "search-extract", "checkedAt": DATE, "note": "Checked for review attribution but rejected: the indexed national profile did not expose enough contractor-license/entity continuity to attach its reviews to California license 1082165."},
    {"id": SAFESTEP_CONSUMER, "title": "ConsumerAffairs · Safe Step Walk-In Tubs · rejected review corpus", "url": "https://www.consumeraffairs.com/homeowners/safe-step-walk-in-tubs.html", "kind": "platform", "access": "search-extract", "checkedAt": DATE, "note": "National product/company corpus checked and rejected for this record because individual California contracting-entity attribution could not be established safely."},
    {"id": CHEN_DISCLOSURE, "title": "CSLB · complaint disclosure · license 814802", "url": disclosure("814802"), "kind": "government", "access": "page", "checkedAt": DATE, "note": "Official disclosure page read directly. A disclosure exists; the record preserves that fact without treating an allegation or unresolved matter as a proven finding."},
    {"id": SHEK_DISCLOSURE, "title": "CSLB · complaint/disciplinary disclosure · license 306841", "url": disclosure("306841"), "kind": "government", "access": "page", "checkedAt": DATE, "note": "Official disclosure page read directly and considered alongside the revoked license status. This record is historical and held from booking."},
    {"id": GERSON_DISCLOSURE, "title": "CSLB · pending citation disclosure · license 1108341", "url": disclosure("1108341"), "kind": "government", "access": "page", "checkedAt": DATE, "note": "Official page read directly. It says disciplinary action is pending in the form of a citation and warns that no conclusion should be assumed before the legal process is complete."},
    {"id": SF_CODE_104_2, "title": "San Francisco Plumbing Code §104.2 · Exempt Work", "url": "https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_building/0-0-0-85830", "kind": "government", "access": "page", "checkedAt": DATE, "note": "Official current code page read directly. Section 104.2 lists narrow exempt-work categories tied to whether work requires cutting into or removing piping or traps. Applicability to a particular scope is not inferred."},
])

assert len(SOURCES) == 84
assert len({s["id"] for s in SOURCES}) == len(SOURCES)
assert min(s["id"] for s in SOURCES) == 222 and max(s["id"] for s in SOURCES) == 305


def slug(value: str) -> str:
    value = value.lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def claim(field: str, text: str, sid: int, excerpt: str) -> dict:
    return {"field": field, "text": text, "source": sid, "excerpt": excerpt}


def flag(level: str, text: str, *sources: int) -> dict:
    return {"level": level, "text": text, "sources": list(sources)}


BUSINESSES: list[dict] = []
for index, r in enumerate(CANDIDATES):
    number = r["number"]
    sid = CSLB_FIRST + index
    lic_status = r["license_status"]
    active = lic_status == "active"
    classes = ", ".join(r["classes"])
    claims = [
        claim(
            "Discovery",
            "The CSLB detail page was read directly; legal identity, business form, address, phone, status, classifications and displayed expiry were transcribed line by line.",
            sid,
            f"#{number} · {r['name']} · {lic_status} · {classes} · expires {r['expires']}",
        ),
        claim(
            "Credential",
            f"CSLB displays license #{number} as {lic_status} with classification(s) {classes}. A registry status does not establish exact-task experience.",
            sid,
            f"{r['form']} · {r['address']} · {r['phone']}",
        ),
    ]

    permit = None
    permit_contact_source = None
    permit_detail_source = None
    if number in P_PERMITS:
        permit = P_PERMITS[number]
        permit_contact_source, permit_detail_source = P_CONTACTS, P_DETAILS
    elif number in B_PERMITS:
        permit = B_PERMITS[number]
        permit_contact_source, permit_detail_source = B_CONTACTS, B_DETAILS
    elif number == "343837":
        permit = ("200408040636", "2004-09-13", "kitchen remodel")
        permit_contact_source, permit_detail_source = B_CONTACTS, B_OBRIEN

    if permit:
        pid, completed, scope = permit
        claims.append(claim(
            "Permit linkage",
            f"The official permit-contact dataset associates license #{number} with permit {pid}; this identifies the permit contact but does not allocate every task on a multi-contact permit.",
            permit_contact_source,
            f"{'license1' if permit_contact_source == B_CONTACTS else 'license_number'} {number} · permit_number {pid}",
        ))
        claims.append(claim(
            "Coverage",
            "The selected official permit row records completed historical work in work-location ZIP 94122. This is concrete local-work evidence, not confirmation of current dispatch to a new address.",
            permit_detail_source,
            f"{pid} · complete · {completed} · ZIP 94122",
        ))
        claims.append(claim(
            "Permit scope",
            f"The official description records {scope}. It supports only that historical scope and does not prove the requested trip-lever or access-hatch technique.",
            permit_detail_source,
            f"{pid} · {scope}",
        ))
        area = "outer" if r["outer"] else "sunset"
        area_text = (
            f"CSLB records an Outer Sunset-area business address ({r['address']}); a completed 94122 permit is also retained. Neither is a current scheduling promise."
            if r["outer"]
            else "A completed official permit places historical work in ZIP 94122; current Outer Sunset dispatch remains to be confirmed."
        )
    elif number in {"791342", "908590"}:
        claims.append(claim(
            "Coverage",
            "The official plumbing contact dataset records historical contractor-contact ZIP 94122, but no completed 94122 work-location permit was selected in the strict join.",
            P_HISTORICAL,
            f"license_number {number} · historical contact ZIP 94122",
        ))
        area = "outer" if r["outer"] else "sunset"
        area_text = "Historical permit-contact ZIP evidence only; current Outer Sunset dispatch and completed local work remain unconfirmed."
    elif r["outer"]:
        claims.append(claim(
            "Coverage",
            "CSLB records the business at a west-side San Francisco address. A business address is useful local evidence but not a promise to accept this project.",
            sid,
            r["address"],
        ))
        area = "outer"
        area_text = f"CSLB records {r['address']}; current dispatch must still be confirmed."
    else:
        claims.append(claim(
            "Coverage",
            "No current Outer Sunset service statement or completed local permit was retained for this record.",
            sid,
            r["address"],
        ))
        area = "unknown"
        area_text = "Current Outer Sunset dispatch is not verified."

    flags: list[dict] = []
    top_status = "research"
    if not active:
        top_status = "hold"
        flags.append(flag(
            "hold",
            f"Do not book under license #{number}: CSLB displays status {lic_status}. Retained only for historical identity and permit evidence.",
            sid,
        ))

    # Record-specific official and identity irregularities.
    if number == "814802":
        flags.append(flag("notice", "CSLB links complaint-disclosure information. The disclosure was read; no allegation is converted into a proven finding.", sid, CHEN_DISCLOSURE))
        flags.append(flag("discrepancy", "The 2008 permit-contact row uses an earlier firm name and predates CSLB's 2020 reissue to the current corporation. It proves license-number history, not that the current entity performed that work.", sid, P_CONTACTS, P_DETAILS))
    if number == "306841":
        flags.append(flag("hold", "CSLB displays a revoked license and a related public disclosure. This is not a bookable record.", sid, SHEK_DISCLOSURE))
    if number == "1108341":
        top_status = "hold"
        flags.append(flag("hold", "CSLB says a citation is pending and expressly cautions against assuming a conclusion before the legal process is complete. Hold for resolution and recheck.", sid, GERSON_DISCLOSURE))
    if number == "1122605":
        flags.append(flag("discrepancy", "CSLB lists 415-672-0249 while the official site and matched Nextdoor profile list 415-286-3451. Confirm the contracting entity before contact.", sid, AXION_SITE, AXION_NEXTDOOR))
    if number == "498866":
        flags.append(flag("notice", "CSLB shows the license reissued to another entity on 2026-04-02. Confirm that the current corporation—not a predecessor—is the contracting party and recheck the selected permit chronology.", sid, P_CONTACTS, P_DETAILS))
    if number == "1090249":
        flags.append(flag("discrepancy", "The direct Birdeye page repeats two review texts under different author labels. Duplicate text is deduplicated rather than counted twice.", PROCARE_BIRDEYE))
        flags.append(flag("notice", "A Yahoo/Yelp-fed excerpt alleges unfair ownership-level business practices. It is preserved as an allegation, not treated as established fact.", PROCARE_YAHOO))
        flags.append(flag("discrepancy", "CSLB, Birdeye and Yahoo display different Hayward street addresses while exact business name, phone/website evidence supports continuity. Confirm the current contracting address.", sid, PROCARE_BIRDEYE, PROCARE_YAHOO))
    if number == "1082165":
        flags.append(flag("gap", "National Safe Step review corpora were checked but rejected: California contracting-entity continuity was insufficient for safe attribution. No national review is attached here.", SAFESTEP_BBB, SAFESTEP_CONSUMER))
    if number == "1141495":
        top_status = "hold"
        flags.append(flag("hold", "CSLB still says active but displays workers-compensation expiry 2026-08-15, before this research date. Recheck coverage directly before any contact or scope discussion.", sid))
        flags.append(flag("notice", "The business markets plumbing and bathtub repair, but CSLB lists B only and no C-36. Require identification of the properly licensed plumbing contractor/subcontractor for pipe work.", sid, BRUS_SITE, BRUS_YELP))
    if number == "1132400":
        top_status = "hold"
        flags.append(flag("hold", "CSLB still says active but displays workers-compensation cancellation 2026-08-26. Recheck current coverage and status before considering the firm.", sid))
    if number == "754201":
        top_status = "hold"
        flags.append(flag("hold", "License expiry is 2026-09-30 and CSLB displays workers-compensation cancellation scheduled for 2026-09-19. Hold for a fresh regulator and insurance check.", sid))
    if number == "1119854":
        flags.append(flag("notice", "The displayed workers-compensation policy expires on the research date, 2026-09-12. Treat project coverage as unverified and recheck before contact.", sid))
    if number == "592325":
        flags.append(flag("discrepancy", "The current CSLB/official-site address is 483 Victory Avenue; Yelp/Nextdoor index an older 205 Utah Avenue address. Exact phone and name support continuity, but confirm the current entity/address.", sid, HARGENS_SITE, HARGENS_YELP, HARGENS_NEXTDOOR))

    if r["trade"] == "plumbing":
        rationale = (
            f"{'Active C-36' if active else 'Historical C-36 record'} plus source-linked local evidence. "
            "Useful for a diagnostic-plumber comparison, but no retained source proves a seized bathtub overflow linkage was freed without opening finishes."
        )
        next_step = (
            "Ask for a diagnostic-only, repair-first scope: examples involving stuck trip-lever/plunger assemblies and older galvanized systems; the least invasive method; a written stop point before hidden-pipe replacement; current Outer Sunset dispatch; and project-specific insurance."
            if active else
            "Do not book under this non-active license. Keep only as historical permit/identity context and locate a currently active C-36 entity."
        )
        gaps = [
            "No source proves successful extraction of this exact seized bathtub overflow mechanism.",
            "No written repair-first stop point or authorization boundary was obtained.",
            "Project-specific liability and workers-compensation coverage were not independently verified.",
            "Drywall/ceiling restoration and a finished access hatch are not confirmed under this plumbing scope.",
        ]
    elif r["trade"] == "multi-trade":
        rationale = (
            f"{'Active' if active else 'Historical'} license classifications include both B and C-36, and the record carries local permit evidence. "
            "That makes coordination worth investigating, not proven: exact mechanism work, finish quality and current staffing remain unknown."
        )
        next_step = (
            "Ask who will diagnose the overflow, who will perform any plumbing and finish work, whether a small code-compliant access hatch can be framed and finished, the repair-first stop point, permit responsibility, current service area and project-specific insurance."
            if active else
            "Do not book under this non-active license. Retain only as historical evidence."
        )
        gaps = [
            "No exact seized trip-lever extraction case was verified.",
            "No review proves a small ceiling opening was converted into a finished reusable access hatch.",
            "Current crew assignments, subcontractors and Outer Sunset availability are unknown.",
            "Project-specific insurance and a written repair-first scope remain unverified.",
        ]
    else:
        rationale = (
            "Active B-classification read plus a completed 94122 permit with relevant drywall, ceiling, bathroom, water-damage or exploratory-access wording. "
            "This supports a restoration-estimate lead only; it does not establish plumbing self-performance or exact finish matching."
        )
        next_step = (
            "Ask for examples of small occupied-home ceiling openings, substrate/texture matching, dust containment, framing and finishing a reusable access hatch, coordination with an active C-36 plumber, permit responsibility, current Outer Sunset dispatch and project-specific insurance."
        )
        gaps = [
            "No source proves work on this exact overflow mechanism.",
            "No source proves a small plumbing-access opening was finished as a reusable access hatch.",
            "Current Outer Sunset availability and minimum job size remain unconfirmed.",
            "Project-specific insurance, finish-matching method and plumber coordination remain unverified.",
        ]

    BUSINESS = {
        "id": f"w8-{slug(r['name'])}",
        "name": r["name"],
        "phone": r["phone"],
        "phoneSource": sid,
        "website": r["website"],
        "websiteSource": r["websiteSource"],
        "trade": r["trade"],
        "area": area,
        "areaText": area_text,
        "status": top_status,
        "checkedAt": DATE,
        "claims": claims,
        "license": {
            "number": number,
            "entity": r["name"].upper(),
            "classes": r["classes"],
            "status": lic_status,
            "expires": r["expires"],
            "checkedAt": DATE,
            "source": sid,
        },
        "reviewIds": [],
        "platformLinks": [],
        "flags": flags,
        "gaps": gaps,
        "priority": None,
        "rationale": rationale,
        "nextStep": next_step,
        "exactMatch": False,
        "insuranceVerified": False,
        "scopeConfirmed": False,
        "master": False,
    }
    BUSINESSES.append(BUSINESS)

BY_LICENSE = {b["license"]["number"]: b for b in BUSINESSES}

# Business/site capability claims and platform links are added only to the
# entity whose phone, license, website, or exact identity established continuity.
def add_claim(number: str, field: str, text: str, sid: int, excerpt: str) -> None:
    BY_LICENSE[number]["claims"].append(claim(field, text, sid, excerpt))


def add_link(number: str, label: str, url: str, sid: int) -> None:
    BY_LICENSE[number]["platformLinks"].append({"label": label, "url": url, "source": sid})


add_claim("957727", "Repair-first capability", "The indexed Yelp business description says Flow Form services plumbing fixtures from very old to modern; a photo caption describes replacing an old tub/shower valve with a cover plate that avoided tile work. This is business/profile content, not an overflow-trip-lever result.", FLOW_YELP, "Service and Repair of all Plumbing Fixtures from very old to modern · old tub/shower valve · eliminating need for tile work")
add_link("957727", "Yelp profile", "https://www.yelp.com/biz/flow-form-plumbing-san-francisco-3", FLOW_YELP)
add_link("817607", "Yelp profile", "https://www.yelp.com/biz/holland-plumbing-works-san-francisco", HOLLAND_YELP)
add_link("817607", "Judy's Book excerpts", "https://www.judysbook.com/Holland-Plumbing-Works-BtoB~Plumbing-Contractors-sanfrancisco-r29770409.htm", HOLLAND_JUDYS)
add_link("1028751", "BuildZoom profile", "https://www.buildzoom.com/contractor/panhandle-plumbing-san-francisco-ca", PANHANDLE_BUILDZOOM)
add_claim("1122605", "Service scope", "The official site markets leak detection and pipe repair. It does not mention overflow trip-lever extraction or galvanized assemblies.", AXION_SITE, "Leak Detection & Pipe Repair")
add_link("1122605", "Nextdoor profile", "https://nextdoor.com/pages/axion-plumbing-san-francisco-ca/", AXION_NEXTDOOR)
add_link("1122605", "Yelp search result", "https://www.yelp.com/search?find_desc=axion&find_loc=San+Francisco%2C+CA", AXION_YELP)
add_claim("1090249", "Restoration and coverage", "The official site markets water, fire and mold restoration, structural repair and complete restoration, and lists San Francisco County among areas served.", PROCARE_SITE, "complete restoration · Areas We Serve · San Francisco County")
add_link("1090249", "Birdeye review page", "https://reviews.birdeye.com/pro-care-restoration-inc-171673259657633", PROCARE_BIRDEYE)
add_link("1090249", "Yahoo/Yelp excerpts", "https://local.yahoo.com/info-235468637-procare-restoration-hayward/", PROCARE_YAHOO)
add_claim("850352", "Restoration scope", "The official Bay Metro site describes restoration/reconstruction and remodeling; CSLB separately lists B and C-36. Exact small access-hatch work is not stated.", BAYMETRO_SITE, "restoration · reconstruction · remodeling")
add_link("850352", "GuildQuality profile", "https://www.guildquality.com/profile/bay-metro-corporation", BAYMETRO_GUILD)
add_link("850352", "Yelp profile", "https://www.yelp.com/biz/bay-metro-corporation-san-francisco", BAYMETRO_YELP)
add_claim("1141495", "Marketed service scope", "The official site and indexed Yelp profile market San Francisco-area bathroom remodeling, plumbing, bathtub repair and drain repair. CSLB lists B only, so a C-36 plumber must be identified for pipe work.", BRUS_SITE, "Bathroom Remodeling and Enhancements · Plumbing Services · bathtub repair · drain repair")
add_link("1141495", "Yelp profile", "https://www.yelp.com/biz/brus-box-contractor-works-san-francisco", BRUS_YELP)
add_link("1141495", "Yahoo/Yelp excerpts", "https://local.yahoo.com/info-232677711-brus-box-contractor-works-san-francisco/", BRUS_YAHOO)
add_claim("1018292", "Restoration scope", "The official site markets damage restoration. The selected City permit, not the marketing page, supplies the specific wall/ceiling drywall evidence.", BOLD_SITE, "damage restoration")
add_claim("592325", "Cross-trade scope", "The official site describes water/fire-damage building repair; CSLB independently lists B, C-36, C-33, C-43 and C-20. This is strong coordination direction but not exact-task proof.", HARGENS_SITE, "repair commercial and residential buildings from water damage · rebuilding")
add_link("592325", "Yelp profile", "https://www.yelp.com/biz/hargens-south-san-francisco-2", HARGENS_YELP)
add_link("592325", "Nextdoor profile", "https://nextdoor.com/pages/hargens-inc-south-san-francisco-ca/", HARGENS_NEXTDOOR)
add_link("592325", "BuildZoom profile", "https://www.buildzoom.com/contractor/hargens-inc", HARGENS_BUILDZOOM)


REVIEWS: list[dict] = []


def review(number: str, platform: str, source: int, author: str, published: str | None, quote: str, theme: str, analysis: str, *, access: str, negative: bool = False, identity: str = "matched") -> None:
    rid = f"R{99 + len(REVIEWS)}"
    REVIEWS.append({
        "id": rid,
        "business": BY_LICENSE[number]["id"],
        "platform": platform,
        "source": source,
        "author": author,
        "published": published,
        "checkedAt": DATE,
        "quote": quote,
        "theme": theme,
        "analysis": analysis,
        "exactTask": False,
        "negative": negative,
        "access": access,
        "identity": identity,
    })
    BY_LICENSE[number]["reviewIds"].append(rid)


review("957727", "Yelp", FLOW_YELP, "Diana S.", None, "He replaced our kitchen faucet and worked on our very old faucets in the tub and the shower.", "Older tub fixtures", "Task-adjacent evidence for work on old tub/shower fixtures. It does not say the overflow linkage was stuck, describe galvanized pipe, or prove that finishes were preserved.", access="search-extract")
review("817607", "Yelp", HOLLAND_YELP, "Indexed reviewer", None, "I've called Patrick on many occasions in relation to troubles with my plumbing. He is responsive, trustworthy, and punctual. He fixes the problem with reasonable prices.", "Repeat plumbing service", "A repeat-customer account tied by exact phone and name. It is generic plumbing evidence, not an overflow mechanism or difficult-access case.", access="search-extract")
review("817607", "Citysearch via Judy's Book", HOLLAND_JUDYS, "Maureen McGinley", "2011-07-20", "the shower handle mechanism came out ... Pat insisted on coming right over and quickly, professionally and most important, pleasantly fixed the problem", "Shower-handle mechanism repair", "The closest Holland account concerns a shower-control handle mechanism, not a bathtub overflow/trip-lever assembly. It does not describe hidden piping, galvanized material, finish preservation, or current availability.", access="page")
review("1028751", "BuildZoom", PANHANDLE_BUILDZOOM, "Colin M.", "2024-07-15", "Chris is the best! Highly recommend for projects both large and small.", "Small-project willingness", "The only directly displayed review suggests willingness to handle varied project sizes. It gives no task details, so it cannot establish diagnostic technique or finish quality.", access="page")
review("1122605", "Nextdoor", AXION_NEXTDOOR, "J. N.", None, "I recently used Axion Plumbing for issues in my bathroom and kitchen... Ramon was highly knowledgeable, quickly diagnosing and efficiently resolving everything without leaving a mess.", "Bathroom diagnosis", "Relevant to bathroom diagnosis and clean work, but it is an excerpt with no exact problem, publication year, or proof of overflow-trip-lever experience.", access="search-extract")
review("1122605", "Nextdoor", AXION_NEXTDOOR, "A. L.", None, "Russ is a consummate professional who explains things incredibly clearly and is a master plumber.", "Communication", "Supports a customer account of clear explanations. The platform wording does not verify a statutory master-plumber credential, and no exact repair scope is described.", access="search-extract")
review("1090249", "Google via Birdeye", PROCARE_BIRDEYE, "Anonymous (duplicate text also labeled Vince R. Jr.)", None, "ProCare was very detailed and with intelligent workmanship attacked a very devasting building condition. The crew was very hardworking, responsible, & respectful.", "Complex restoration", "A Google-attributed text republished by Birdeye. Because the same words appear under another author label, it is counted once and flagged; it supports only a customer account of broad restoration work.", access="page")
review("1090249", "Google via Birdeye", PROCARE_BIRDEYE, "Susan (duplicate text also labeled Anonymous)", None, "I had mold discovered behind the tile in my bathroom. Jesse from Pro-care was very responsive... It was a one day job and the crew was excellent and mold re-test was negative for any residual mold.", "Bathroom remediation", "Task-adjacent bathroom remediation and behind-tile access. The duplicate author labeling prevents independent counting, and the account does not establish plumbing or ceiling finish work.", access="page")
review("1090249", "Google via Birdeye", PROCARE_BIRDEYE, "Sudhakar", None, "Though they were busy, they accommodated our request in 1 day, worked over the weekend, did the thorough restoration job in our house kitchen, bath and bed rooms.", "Multi-room restoration", "Supports a republished customer account of kitchen/bath/bedroom restoration and scheduling. It does not identify materials, plumbing responsibility, or an access hatch.", access="page")
review("1090249", "Yelp via Yahoo", PROCARE_YAHOO, "Iris W.", "2026-08-10", "Daisy and team have helped us with three separate projects (summer 2025, winter 2025, summer 2026) and we've been really happy with the results each time. Pro Care came highly recommended to us by...", "Repeat restoration work", "A dated, truncated Yelp-fed excerpt visible on Yahoo. It suggests repeat use but does not reveal the project scopes or exact finish outcome.", access="page")
review("1090249", "Yelp via Yahoo", PROCARE_YAHOO, "Luke S.", "2025-01-10", "Highly recommend Pro-Care Restoration. Our complex needed some mitigation work done after a unit-to unit leak which was complicated by some health issues of one resident. The crew sensitively...", "Leak mitigation", "Task-adjacent mitigation after a leak and a customer account of sensitivity. The excerpt is truncated and does not prove reconstruction, plumbing work, or current Outer Sunset coverage.", access="page")
review("1090249", "Yelp via Yahoo", PROCARE_YAHOO, "juan w.", "2025-05-31", "Jesse helped u me with mold remediation at my condo. He is very professional and reasonable. They did a great job. I am very glad to work with them!", "Mold remediation", "A short dated remediation account. It concerns mold, not drywall finish quality, plumbing repair, or the requested overflow mechanism.", access="page")
review("1090249", "Yelp via Yahoo", PROCARE_YAHOO, "A J.", "2025-12-22", "BEWARE -- unfair business practices at the ownership level. The owner, Jesse, is very aggressive and unreasonable. Their team started remediation work but approached with numerous incorrect...", "Business-practices allegation", "A negative, truncated Yelp-fed allegation preserved for balance. It is not independently substantiated and must not be treated as a factual finding; the full review was not retrieved.", access="page", negative=True)
review("850352", "GuildQuality", BAYMETRO_GUILD, "Betty L.", "2024-12-04", "They were professional, and Manny was very reliable. He always showed up on time and repaired things.", "Repair reliability", "Dated third-party survey excerpt tied by exact name/address/phone. It supports reliability in unspecified repairs, not bathtub plumbing or finish matching.", access="search-extract")
review("850352", "GuildQuality", BAYMETRO_GUILD, "Joann T.", "2024-10-16", "Manny did well coordinating things with the contractors. He was available to talk anytime and was very kind. As the project manager, he made sure everything was done correctly and made some good recommendations.", "Trade coordination", "Relevant to coordination across contractors, which may matter if plumbing and restoration are separate. It does not identify those trades or independently verify technical outcomes.", access="search-extract")
review("850352", "GuildQuality", BAYMETRO_GUILD, "Anne B.", "2022-12-13", "Manny was fantastic and they did a great job. I would work with them again.", "Repeat intent", "A positive but generic dated excerpt. It adds no exact-task, access-hatch, plumbing, or material evidence.", access="search-extract")
review("1141495", "Yelp via Yahoo", BRUS_YAHOO, "Greg C.", "2024-01-22", "We hired Brus Box to replace our kitchen faucet and install an electric bidet seat, including a new power outlet. The business owner, Andrew, was very communicative and came out himself for the...", "Fixture and cross-trade work", "A task-adjacent, truncated account involving a plumbing fixture and electrical work. CSLB lists B only, so it does not establish lawful C-36 self-performance or overflow expertise.", access="page")
review("1141495", "Yelp via Yahoo", BRUS_YAHOO, "Delairen B.", "2025-10-12", "They removed & replaced all the insulation in our attic and cleaned up & repaired some loose wiring for us so that we could use the attic for some...", "Opening/restoration work", "Shows a customer account of removing/replacing building material and coordinating wiring. It is truncated, concerns an attic, and does not establish drywall or plumbing scope.", access="page")
review("1141495", "Yelp via Yahoo", BRUS_YAHOO, "Edward F.", "2023-03-04", "The job was to replace a toilet that was potentially having leaking issues. They selected an affordable toilet from Home...", "Plumbing fixture replacement", "A truncated fixture-replacement account. It is relevant only as a lead; it does not identify the licensed plumbing performer or a repair-first alternative.", access="page")
review("592325", "Business site", HARGENS_SITE, "Kirk Stratton", None, "My family and I are very grateful and I want to thank you and your company for your professionalism and for rebuilding our home in a timely manner.", "Restoration testimonial", "Business-hosted testimonial supporting a broad rebuilding account. It is not independent review evidence and says nothing about small access openings or exact finish matching.", access="page", identity="company-published")
review("592325", "Yelp", HARGENS_YELP, "Debra R.", None, "I would not have gotten anything near this without Tom's and Pompeu's professional experience and guidance.", "Project guidance", "A short indexed highlight suggesting guidance on an unspecified project. It is too incomplete to establish restoration quality or task fit.", access="search-extract")
review("592325", "Yelp", HARGENS_YELP, "Kathleen D.", None, "Hargen's employees are total pros and really nice to work with.", "Crew conduct", "A brief positive crew account. No scope, date or exact technical outcome is exposed in the indexed highlight.", access="search-extract")
review("592325", "Yelp", HARGENS_YELP, "Paintchip D.", None, "Two weeks later, some are just now starting to return my call or still working on getting me a quote.", "Response-time concern", "A negative-leaning indexed highlight about delayed callbacks/quotes. Context and date are unavailable, so it is a caution rather than a verified current performance finding.", access="search-extract", negative=True)

assert len(REVIEWS) == 23
assert REVIEWS[0]["id"] == "R99" and REVIEWS[-1]["id"] == "R121"
assert len({r["id"] for r in REVIEWS}) == len(REVIEWS)
assert all(len(r["quote"]) < 500 and not r["exactTask"] for r in REVIEWS)

# Review quote uniqueness is global within this wave after case/space folding.
def review_fingerprint(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()

assert len({review_fingerprint(r["quote"]) for r in REVIEWS}) == len(REVIEWS)

# Every record remains fail-closed.
assert not any(b["master"] or b["exactMatch"] or b["insuranceVerified"] or b["scopeConfirmed"] for b in BUSINESSES)
assert all(b["claims"][0]["field"] == "Discovery" for b in BUSINESSES)
assert all(len(b["gaps"]) >= 4 for b in BUSINESSES)

payload = {
    "wave": 8,
    "date": DATE,
    "composition": {
        "businesses": len(BUSINESSES),
        "plumbingPrimary": 23,
        "restorationPrimary": 27,
        "activeLicenses": 40,
        "nonActiveLicenses": 10,
        "cslbPagesRead": 50,
        "completedPlumbingPermits94122": len(P_PERMITS),
        "completedRestorationPermits94122": len(B_PERMITS),
        "retainedReviewExcerpts": len(REVIEWS),
    },
    "sources": SOURCES,
    "businesses": BUSINESSES,
    "reviews": REVIEWS,
}

OUT.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n")
print(
    f"wrote {OUT.relative_to(ROOT)}: {len(BUSINESSES)} businesses, "
    f"{len(SOURCES)} sources, {len(REVIEWS)} review excerpts"
)
