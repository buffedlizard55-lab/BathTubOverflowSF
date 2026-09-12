#!/usr/bin/env python3
"""Build data/wave9.json: the ninth verification wave (50 new research records).

Wave 9 deliberately splits its evidence into two tiers, and the split is stated
on every record rather than smoothed over:

  1. ``cslb_read``  -- 17 records whose CSLB LicenseDetail page was opened and
     transcribed field by field on 2026-09-12 (entity, business form, address,
     phone, issue/expiry dates, status text, every classification, bond,
     workers-compensation and liability lines, and any Additional Status line).
  2. ``registry_only`` -- 33 records that surfaced from the City's own open
     permit registries (``k6kv-9kix`` plumbing-permit contacts, ``3pee-9qhc``
     building-permit contacts, ``i98e-djp9``/``a6aw-rudh`` permit details) and
     whose registry-recorded license number was NOT read on CSLB in this pass.
     For those records ``license`` stays ``null`` and the trade is recorded as
     ``registry-lead``: a channel-derived lead, never a classification claim.

Review evidence is attached only where the platform page itself establishes the
business identity. Category-page quotes and community threads whose author or
subject cannot be tied to a specific licensee are stored as sources and are
never converted into a review.

Run:
    python3 scripts/gen_wave9.py
    python3 scripts/merge_wave9.py
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "wave9.json"
DATE = "2026-09-12"

# --------------------------------------------------------------- source ids
SRC_FIRM94122 = 306  # k6kv-9kix: distinct license+firm rows with firm ZIP 94122
SRC_B_DRYWALL = 307  # i98e-djp9: completed 94122 drywall/ceiling/plaster permits
SRC_P_RECENT = 308  # a6aw-rudh: completed 94122 plumbing permits, recent window
SRC_B_JOIN_1 = 309  # 3pee-9qhc: contact join, drywall permit batch 1
SRC_B_JOIN_2 = 310  # 3pee-9qhc: contact join, drywall permit batch 2
SRC_P_JOIN = 311  # k6kv-9kix: contact join, recent plumbing permits
SRC_B_FIRM94122 = 312  # 3pee-9qhc: contractor contacts, firm ZIP 94122
SRC_P_PERMITS_A = 313  # k6kv-9kix: permit numbers for registry licenses, set A
SRC_P_PERMITS_B = 314  # k6kv-9kix: permit numbers for registry licenses, set B
SRC_P_PERMITS_C = 315  # k6kv-9kix: permit numbers for registry licenses, set C
SRC_P_FIRMADDR = 316  # k6kv-9kix: firm-address confirmation for CSLB 94122 firms

CSLB_FIRST = 317  # 317..333 LicenseDetail pages, 334 complaint disclosure
DISCLOSURE_1017991 = 334

YELP_INNOVATION = 335
CYLEX_INNOVATION = 336
YELP_DISCOUNT = 337
HOMEADVISOR_SMELLY = 338
SERVICEAGENT_SMELLY = 339
BUILDZOOM_COIT = 340
BUILDZOOM_YU = 341
BUILDZOOM_HJ = 342
YELP_KEVEL = 343
ANGI_KEVEL = 344
THUMBTACK_SF_DRYWALL = 345
THUMBTACK_CEILING = 346
THUMBTACK_SSF_DRYWALL = 347
REDDIT_TRIP_LEVER = 348
REDDIT_ACCESS_BELOW = 349
REDDIT_1940S_TUB = 350
REDDIT_SHEETROCK = 351
REDDIT_SF_PRICING = 352

CSLB_URL = "https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum="
DISCLOSURE_URL = (
    "https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/ComplaintDisclosure.aspx?LicNum="
)
SODA = "https://data.sf.gov/resource/"


def soda(dataset: str, select: str, where: str, order: str = "", limit: int = 200) -> str:
    parts = [f"$select={select}", f"$where={where}", f"$limit={limit}"]
    if order:
        parts.append(f"$order={order}")
    return SODA + f"{dataset}.json?" + "&".join(parts)


# --------------------------------------------------------------- CSLB reads
# Every value below was transcribed from the CSLB LicenseDetail page named in
# the source table on 2026-09-12. Nothing is inferred from a directory.
READS: dict[str, dict] = {
    "1002370": dict(
        name="Charles Lakamp",
        entity="CHARLES LAKAMP",
        addr="13560 Terrace Drive, Sonora, CA 95370",
        phone="415-902-4457",
        form="Sole Ownership",
        issued="03/25/2015",
        expires="2027-03-31",
        status="inactive",
        classes=["B"],
        status_text="This license is inactive and not able to contract at this time.",
        extra=(
            "Additional status: needs a contractors bond and must meet workers compensation "
            "requirements to renew active or reactivate. Bond OLD REPUBLIC SURETY GCL5942138 "
            "$25,000 eff 01/01/2023, CANCELLATION 04/08/2023. WC exempt eff 03/23/2021, "
            "CANCELLATION 04/01/2023. Misc 10/16/2023: WC EXEMPT CANCELLED-LIC INACTIVATED."
        ),
        registry=(
            "k6kv-9kix lists this license against a firm address of 536 Judah St, San Francisco "
            "94122-0000, phone 4156999385, on plumbing-permit rows PP20150413689, PP20150501234, "
            "PP20150722524 and PP20170313701."
        ),
        registry_excerpt=(
            '{"license_number":"1002370","addr":"536 Judah St","zip":"94122-0000",'
            '"phone":"4156999385","permits":"PP20150413689,PP20150501234,PP20150722524,PP20170313701"}'
        ),
        registry_source=SRC_FIRM94122,
        trade="general",
        area="sunset",
    ),
    "1140051": dict(
        name="American Plumbing and Trenchless LLC",
        entity="AMERICAN PLUMBING AND TRENCHLESS LLC",
        addr="310 Cimarron Drive, Vallejo, CA 94589",
        phone="707-639-7405",
        form="Ltd Liability",
        issued="07/08/2025",
        expires="2027-07-31",
        status="active",
        classes=["C36"],
        status_text="This license is current and active.",
        extra=(
            "Bond AMERICAN CONTRACTORS INDEMNITY 100966404 $25,000 eff 06/10/2025. LLC "
            "Employee/Worker Bond 100966483 $100,000 eff 06/10/2025. BQI not required: JOSEPH "
            "JOHN GARIN owns 10%+. WC EXEMPT (no employees) eff 06/10/2025. Liability insurance "
            "ATEGRITY SPECIALTY 01CPKP201760340 $2,000,000 eff 06/10/2026 exp 06/10/2027."
        ),
        permit=(
            "PP20260810750",
            "2026-08-31",
            "601 Moraga St, San Francisco 94122",
            "install of two way clean out behind the sidewalk, install two cast iron wye fittings "
            "and branch lines for storm drains and adu sewer connections. new storm and sewer "
            "lines approx 25' in length. underground work to be completed.",
        ),
        permit_contact_source=SRC_P_JOIN,
        permit_detail_source=SRC_P_RECENT,
        registry="k6kv-9kix firm phone 7076397405 matches the CSLB phone exactly.",
        registry_excerpt='{"permit_number":"PP20260810750","license_number":"1140051","phone":"7076397405"}',
        registry_source=SRC_P_JOIN,
        trade="plumbing",
        area="sunset",
    ),
    "830368": dict(
        name="Garzac Plumbing",
        entity="GARZAC PLUMBING",
        addr="23743 Industrial Blvd Ste K, Hayward, CA 94545",
        phone="510-581-5005",
        form="Sole Ownership",
        issued="12/31/2003",
        expires="2027-12-31",
        status="active",
        classes=["C36"],
        status_text="This license is current and active.",
        extra=(
            "Bond NORTH RIVER INSURANCE 04CF617773 $25,000 eff 03/08/2023. WC STATE COMPENSATION "
            "INSURANCE FUND 9242676 eff 12/13/2018, CANCELLATION DATE 09/11/2026. WC class 51871 "
            "Plumbing-high wage. No liability-insurance section displayed."
        ),
        permit=(
            "PW20260303050",
            "2026-09-02",
            "4115 Irving St, San Francisco 94122",
            "modify existing gas line to stove and install shut off valve into the cabinet and "
            "point of connection behind the stove. install gas line for fireplace insert. modify "
            "existing sink, drain inlet inside wall and lower it for garbage disposal installation.",
        ),
        permit_contact_source=SRC_P_JOIN,
        permit_detail_source=SRC_P_RECENT,
        registry="k6kv-9kix firm zipcode 94545-0000, phone 5105815005 (matches CSLB).",
        registry_excerpt='{"permit_number":"PW20260303050","license_number":"830368","zipcode":"94545-0000","phone":"5105815005"}',
        registry_source=SRC_P_JOIN,
        trade="plumbing",
        area="sunset",
    ),
    "786183": dict(
        name="Smelly Mel's Plumbing Inc",
        entity="SMELLY MEL'S PLUMBING INC",
        addr="300 Shaw Road, South San Francisco, CA 94080",
        phone="415-758-6237",
        form="Corporation",
        issued="10/20/2000",
        expires="2026-10-31",
        status="active",
        classes=["A", "C36", "B", "C16"],
        status_text="This license is current and active.",
        extra=(
            "Bond SWISS RE CORPORATE SOLUTIONS AMERICA 2382614 $25,000 eff 07/01/2026. BQI not "
            "required: MICHAEL ANTHONY ALLEN (eff 06/06/2016) and TRAVIS MARSHALL ALLEN (eff "
            "06/09/2016) each own 10%+. WC EVEREST PREMIER 7600023644251 eff 10/27/2025 exp "
            "10/27/2026; WC classes 8810 Clerical, 5183/5187 Description Unavailable. Other: "
            "personnel listed on this license are listed on other licenses."
        ),
        permit=(
            "PW20260706215",
            "2026-08-27",
            "1941 Irving St, San Francisco 94122",
            "replace the sewer lateral from the excavated area to the curb, utilizing the "
            "trenchless pipe bursting method.",
        ),
        permit2=(
            "PW20260721658",
            "2026-08-27",
            "1945 Irving St, San Francisco 94122",
            "sewer repair",
        ),
        permit_contact_source=SRC_P_JOIN,
        permit_detail_source=SRC_P_RECENT,
        registry=(
            "k6kv-9kix firm phone 6507382030 CONFLICTS with the CSLB phone (415) 758-6237 read on "
            "the same date."
        ),
        registry_excerpt='{"permit_number":"PW20260706215","license_number":"786183","phone":"6507382030"}',
        registry_source=SRC_P_JOIN,
        trade="multi-trade",
        area="sunset",
    ),
    "1051988": dict(
        name="Yu Plumbing Inc",
        entity="YU PLUMBING INC",
        addr="148 San Diego Ave, Daly City, CA 94014",
        phone="415-613-4676",
        form="Corporation",
        issued="04/04/2019",
        expires="2027-04-30",
        status="active",
        classes=["C36"],
        status_text="This license is current and active.",
        extra=(
            "Bond JET INSURANCE JT035570 $25,000 eff 08/05/2026. BQI not required: RONG BIN BEN "
            "YU owns 10%+ eff 04/04/2019. WC MARKEL MWC026779401 eff 08/20/2026 exp 08/20/2027; "
            "WC classes 51871 Plumbing-high wage, 51831 Plumbing-low wage. No liability-insurance "
            "section displayed."
        ),
        permit=(
            "PW20260802933",
            "2026-09-10",
            "1315 06th Av, San Francisco 94122",
            "replace 4 inch sewer pipes, approximately 15 feet and house trap.",
        ),
        permit_contact_source=SRC_P_JOIN,
        permit_detail_source=SRC_P_RECENT,
        registry="k6kv-9kix firm zipcode 94014-0000, phone 4156134676 (matches CSLB).",
        registry_excerpt='{"permit_number":"PW20260802933","license_number":"1051988","zipcode":"94014-0000","phone":"4156134676"}',
        registry_source=SRC_P_JOIN,
        trade="plumbing",
        area="sunset",
    ),
    "1097098": dict(
        name="H&J Plumbing Inc",
        entity="H&J PLUMBING INC",
        addr="39 1st Avenue, Daly City, CA 94014",
        phone="510-388-8126",
        form="Corporation",
        issued="09/28/2022",
        expires="2028-09-30",
        status="active",
        classes=["C36"],
        status_text="This license is current and active.",
        extra=(
            "Bond NORTH RIVER INSURANCE 04CF632805 $25,000 eff 09/22/2025. BQI not required: HONG "
            "CUI owns 10%+ eff 09/28/2022. WC SECURITY NATIONAL TES4728771 eff 01/03/2026 exp "
            "01/03/2027; WC classes 5187 Description Unavailable, 51831 Plumbing-low wage. Other: "
            "personnel listed on other licenses. No liability-insurance section displayed."
        ),
        permit=(
            "PW20260803947",
            "2026-08-18",
            "1639 33rd Av, San Francisco 94122",
            "replace house trap and sewer line. replace 1inch water inlet copper pipe.",
        ),
        permit_contact_source=SRC_P_JOIN,
        permit_detail_source=SRC_P_RECENT,
        registry=(
            "k6kv-9kix firm phone 4158198126 CONFLICTS with the CSLB phone (510) 388-8126 read on "
            "the same date."
        ),
        registry_excerpt='{"permit_number":"PW20260803947","license_number":"1097098","phone":"4158198126"}',
        registry_source=SRC_P_JOIN,
        trade="plumbing",
        area="sunset",
    ),
    "1140843": dict(
        name="Discount Plumbing Rooter Services LLC",
        entity="DISCOUNT PLUMBING ROOTER SERVICES LLC",
        addr="1325 Howard Ave Bldg 710, Burlingame, CA 94010",
        phone="650-991-2100",
        form="Ltd Liability",
        issued="07/22/2025",
        expires="2027-07-31",
        status="active",
        classes=["C36", "A"],
        status_text="This license is current and active.",
        extra=(
            "Bond LEXINGTON NATIONAL L2842122142 $25,000 eff 06/09/2025. LLC Employee/Worker Bond "
            "L2842132142 $100,000 eff 06/09/2025. BQI FILED (not waived): DANIEL CHAVEZ "
            "L2777752142 $25,000 eff 02/01/2026; MARY ABIGAIL ABAD DELA CRUZ L3504082142 $25,000 "
            "eff 08/13/2026. WC A I U INSURANCE 020396018 eff 04/01/2025 exp 04/01/2027. Liability "
            "NATIONAL UNION FIRE OF PITTSBURGH PA 9952707 $2,000,000 eff 04/01/2026 exp 04/01/2027. "
            "Other: personnel listed on other licenses."
        ),
        permit=(
            "PW20260813237",
            "2026-08-21",
            "1367 28th Av, San Francisco 94122",
            "sewer line replacement",
        ),
        permit2=(
            "PW20260818349",
            "2026-08-27",
            "644 Judah St, San Francisco 94122",
            "sewer lateral replacement",
        ),
        permit_contact_source=SRC_P_JOIN,
        permit_detail_source=SRC_P_RECENT,
        registry=(
            "k6kv-9kix firm phone 6509912164 CONFLICTS with the CSLB phone (650) 991-2100 read on "
            "the same date."
        ),
        registry_excerpt='{"permit_number":"PW20260813237","license_number":"1140843","phone":"6509912164"}',
        registry_source=SRC_P_JOIN,
        trade="plumbing",
        area="sunset",
    ),
    "1026009": dict(
        name="Speedy Serrano Plumbing",
        entity="SPEEDY SERRANO PLUMBING",
        addr="30 Salada Ave, Pacifica, CA 94044",
        phone="650-898-3007",
        form="Partnership",
        issued="04/21/2017",
        expires="2027-04-30",
        status="active",
        classes=["C36"],
        status_text="This license is current and active.",
        extra=(
            "Bond ATLANTIC SPECIALTY 800273683 $25,000 eff 09/01/2026. WC EXEMPT (no employees) "
            "eff 03/17/2025. Other: personnel listed on other licenses. No liability-insurance "
            "section displayed."
        ),
        permit=(
            "PP20260107698",
            "2026-09-09",
            "1350 44th Av, San Francisco 94122",
            "new plumbing lines, sewer, vents water for 1 new laundry room, 1 new kitchen, 1 new "
            "restroom. underground work to be completed.",
        ),
        permit_contact_source=SRC_P_JOIN,
        permit_detail_source=SRC_P_RECENT,
        registry="k6kv-9kix firm zipcode 94044-0000, phone 6508983007 (matches CSLB).",
        registry_excerpt='{"permit_number":"PP20260107698","license_number":"1026009","zipcode":"94044-0000","phone":"6508983007"}',
        registry_source=SRC_P_JOIN,
        trade="plumbing",
        area="sunset",
    ),
    "1013565": dict(
        name="Innovation Plumbing and Rooter",
        entity="INNOVATION PLUMBING AND ROOTER",
        addr="828 Crescent Ave, San Francisco, CA 94110",
        phone="415-424-8419",
        form="Sole Ownership",
        issued="04/30/2016",
        expires="2028-04-30",
        status="active",
        classes=["C36", "B"],
        status_text="This license is current and active.",
        extra=(
            "Bond JET INSURANCE JT014978 $25,000 eff 03/01/2025. WC EXEMPT (no employees) eff "
            "03/30/2026. No liability-insurance section displayed. This license holds BOTH C-36 "
            "plumbing and B general building."
        ),
        permit=(
            "202510288289",
            "2026-01-20",
            "1678 48th Av, San Francisco 94122",
            "relocate washer and dryer machine from basement to inside basement. install (n) drain "
            "line and water line, move the (e) receptacle. install (n) exhaust bent pipe and "
            "replace a section of drywall apprx. 2x4'",
        ),
        permit_contact_source=SRC_B_JOIN_1,
        permit_detail_source=SRC_B_DRYWALL,
        registry="3pee-9qhc permit 202510288289 firm_zipcode 94110-0000, role contractor.",
        registry_excerpt='{"permit_number":"202510288289","license1":"1013565","firm_zipcode":"94110-0000","role":"contractor"}',
        registry_source=SRC_B_JOIN_1,
        trade="multi-trade",
        area="sunset",
    ),
    "1112261": dict(
        name="Ct Plumbing & Fire Protection",
        entity="CT PLUMBING & FIRE PROTECTION",
        addr="1847 48th Ave, San Francisco, CA 94122",
        phone="415-203-7178",
        form="Sole Ownership",
        issued="11/03/2023",
        expires="2027-11-30",
        status="active",
        classes=["C36", "C16"],
        status_text="This license is current and active.",
        extra=(
            "Bond JET INSURANCE JT005902 $25,000 eff 10/16/2023. WC EXEMPT (no employees) eff "
            "10/14/2025. No liability-insurance section displayed. The CSLB page itself records a "
            "94122 Outer Sunset business address."
        ),
        registry=(
            "k6kv-9kix returns this license against firm address ZIP 94122, matching the CSLB "
            "business address 1847 48th Ave, San Francisco 94122."
        ),
        registry_excerpt='{"license_number":"1112261","addr":"1847 48th Ave","zip":"94122-0000","phone":"4152037178"}',
        registry_source=SRC_P_FIRMADDR,
        trade="plumbing",
        area="outer",
    ),
    "1028917": dict(
        name="Euro Plumbing Inc dba General Contractor",
        entity="EURO PLUMBING INC dba GENERAL CONTRACTOR",
        addr="720 Pine Street, San Francisco, CA 94108",
        phone="415-509-9577",
        form="Corporation",
        issued="07/13/2017",
        expires="2021-07-31",
        status="expired",
        classes=["B"],
        status_text="This license is expired and not able to contract at this time.",
        extra=(
            "NO C-36 CLASSIFICATION - B ONLY. Bond HUDSON 30027886 $15,000 eff 06/28/2018 "
            "CANCELLED 07/30/2022. BQI waived GEORGE KVESELADZE eff 07/13/2017. WC exempt eff "
            "06/05/2019. Other: personnel listed on other licenses."
        ),
        registry=(
            "k6kv-9kix lists a firm at 1523 32nd Av 94122 under BOTH 'Euro Plumbing Inc, General "
            "Contractor' and 'E P I General Contractor', phone 4155099527, on PLUMBING permit rows."
        ),
        registry_excerpt=(
            '{"license_number":"1028917","firm":"Euro Plumbing Inc, General  Contractor",'
            '"addr":"1523 32nd Av","zip":"94122-0000","phone":"4155099527"}'
        ),
        registry_source=SRC_FIRM94122,
        trade="general",
        area="sunset",
    ),
    "658767": dict(
        name="Euro Plastering",
        entity="EURO PLASTERING",
        addr="330 Ortega Street, San Francisco, CA 94122",
        phone="415-661-6651",
        form="Sole Ownership",
        issued="11/18/1992",
        expires="2000-11-30",
        status="expired",
        classes=["C35"],
        status_text="This license is expired and not able to contract at this time.",
        extra=(
            "C35 LATHING AND PLASTERING. Bond MARKEL AMERICAN 97461342 $7,500 eff 09/15/1997 "
            "CANCELLED 09/23/1999. WC exempt eff 10/19/1992."
        ),
        registry="3pee-9qhc lists this license with firm_zipcode 94122-0000, role contractor.",
        registry_excerpt='{"license1":"658767","firm_name":"Euro Plastering","firm_zipcode":"94122-0000","role":"contractor"}',
        registry_source=SRC_B_FIRM94122,
        trade="plaster",
        area="outer",
    ),
    "373337": dict(
        name="Lam Pui Electrical & Plumbing Inc",
        entity="LAM PUI ELECTRICAL & PLUMBING INC",
        addr="2900 Yorba St, San Francisco, CA 94116",
        phone="415-298-8369",
        form="Corporation",
        issued="04/05/1979",
        expires="2010-04-30",
        status="expired",
        classes=["B", "C10", "C36"],
        status_text="This license is expired and not able to contract at this time.",
        extra=(
            "Reissue Date 04/06/2006. Misc 04/06/2006: LICENSE REISSUED TO ANOTHER ENTITY. Bond "
            "ACIC SC1041094 $12,500 eff 03/02/2009 CANCELLED 05/03/2012. BQI waived PUI LEUNG LAM "
            "eff 04/06/2006. WC State Fund 713-0029175 eff 06/23/2008 CANCELLED 04/12/2010."
        ),
        registry=(
            "k6kv-9kix 94122 rows for this license use SIX different firm-name spellings: Lam Pui / "
            "Pui Lam / Lam Pui Elec And Plumbing / Lam Pui Electrical & Plbg / Lam Pui Electrical & "
            "Plumbin / Pui Lam Electrical."
        ),
        registry_excerpt=(
            '{"license_number":"373337","zip":"94122-0000","firm_variants":"Lam Pui | Pui Lam | '
            'Lam Pui Elec And Plumbing | Lam Pui Electrical & Plbg | Lam Pui Electrical & Plumbin '
            '| Pui Lam Electrical"}'
        ),
        registry_source=SRC_FIRM94122,
        trade="multi-trade",
        area="sunset",
    ),
    "1017991": dict(
        name="San Francisco Remodel",
        entity="SAN FRANCISCO REMODEL",
        addr="3411 Clearfield Ave, Richmond, CA 94803",
        phone="510-367-4934",
        form="Sole Ownership",
        issued="09/07/2016",
        expires="2028-09-30",
        status="active",
        classes=["B"],
        status_text="This license is current and active.",
        extra=(
            "ADDITIONAL STATUS: 'There is Complaint Disclosure information for this license.' The "
            "disclosure page was read directly: Complaint # N A 2025 2297, Date 06/23/2026, Status "
            "LETTER OF ADMONISHMENT ISSUED. CSLB disclaimer: any complaint listed is only an "
            "allegation of a probable violation and does not affect the status of the license at "
            "this time. Bond WESTERN SURETY 66985288 $25,000 eff 07/29/2024. WC exempt eff "
            "08/06/2026. B only, no C-36."
        ),
        permit=(
            "202407247180",
            "2025-11-05",
            "1461 43rd Av, San Francisco 94122",
            "repair 80 sqft of drywall inside the house on 2nd fl across from kitchen. repair "
            "plumbing in-kind in kitchen under sink. replace valve of hot/cold water & p-trap. "
            "replace 2 light switches on 1st fl.",
        ),
        permit_contact_source=SRC_B_JOIN_1,
        permit_detail_source=SRC_B_DRYWALL,
        registry="3pee-9qhc permit 202407247180 firm_zipcode 94803-0000, role contractor.",
        registry_excerpt='{"permit_number":"202407247180","license1":"1017991","firm_zipcode":"94803-0000","role":"contractor"}',
        registry_source=SRC_B_JOIN_1,
        trade="general",
        area="sunset",
    ),
    "1120735": dict(
        name="KNB Tile and Stone Inc dba KNB Remodeling",
        entity="KNB TILE AND STONE INC dba KNB REMODELING",
        addr="2670 Debbie Place, San Carlos, CA 94070",
        phone="650-274-5086",
        form="Corporation",
        issued="05/14/2024",
        expires="2028-05-31",
        status="active",
        classes=["B-2", "B"],
        status_text="This license is current and active.",
        extra=(
            "Holds B-2 RESIDENTIAL REMODELING plus B GENERAL BUILDING. Bond NATIONWIDE MUTUAL "
            "7901332180 $25,000 eff 07/13/2026. BQI waived THIAGO MARQUES SILVANO eff 08/29/2025. "
            "WC UNITED FIRE & CASUALTY 10174050015 eff 04/26/2025 exp 04/26/2027, class 13021 "
            "Description Unavailable. No C-36."
        ),
        permit=(
            "PP20260731567",
            "2026-08-27",
            "75 Aloha Av, San Francisco 94122",
            "replace tub in same location upgrade plumbing up to code as needed",
        ),
        permit_contact_source=SRC_P_JOIN,
        permit_detail_source=SRC_P_RECENT,
        registry="k6kv-9kix firm zipcode 94070-0000, phone 6502745086 (matches CSLB).",
        registry_excerpt='{"permit_number":"PP20260731567","license_number":"1120735","zipcode":"94070-0000","phone":"6502745086"}',
        registry_source=SRC_P_JOIN,
        trade="general",
        area="sunset",
    ),
    "342141": dict(
        name="Lee's Plumbing Co",
        entity="LEE'S PLUMBING CO",
        addr="217 Willard North, San Francisco, CA 94118",
        phone="415-221-3554",
        form="Sole Ownership",
        issued="08/17/1977",
        expires="1997-09-30",
        status="expired",
        classes=["C36"],
        status_text="This license is expired and not able to contract at this time.",
        extra=(
            "Bond SURETY COMPANY OF THE PACIFIC 464321 $5,000 eff 01/01/1980 CANCELLED 12/15/1985. "
            "Workers compensation: 'There was no workers comp information found for this license.'"
        ),
        registry=(
            "k6kv-9kix lists license 342141 under the firm name 'L & L Plumbing Inc.' with a 94122 "
            "address, while the CSLB licensee for 342141 is LEE'S PLUMBING CO at 94118."
        ),
        registry_excerpt='{"license_number":"342141","firm":"L & L Plumbing Inc.","zip":"94122-0000"}',
        registry_source=SRC_FIRM94122,
        trade="plumbing",
        area="sunset",
    ),
    "341277": dict(
        name="Coit Construction",
        entity="COIT CONSTRUCTION",
        addr="2180 Bryant St 212, San Francisco, CA 94110",
        phone="415-640-4808",
        form="Sole Ownership",
        issued="08/08/1977",
        expires="2027-09-30",
        status="active",
        classes=["B", "C36"],
        status_text="This license is current and active.",
        extra=(
            "B GENERAL BUILDING + C36 PLUMBING on one license, issued 1977. Bond ACIC SC464290 "
            "$25,000 eff 01/01/2023. WC exempt eff 09/13/2025. No liability-insurance section "
            "displayed."
        ),
        permit=(
            "202407176666",
            "2025-06-24",
            "1201 08th Av, San Francisco 94122",
            "unit #3: kitchen and bathroom remodel in kind. installation of approx. 700 sq ft of "
            "5/8 type sheetrock.",
        ),
        permit_contact_source=SRC_B_JOIN_2,
        permit_detail_source=SRC_B_DRYWALL,
        registry=(
            "k6kv-9kix lists a 94122 firm address; 3pee-9qhc permit 202407176666 lists "
            "firm_zipcode 94114; the CSLB business address is 94110 - three ZIP variants."
        ),
        registry_excerpt='{"permit_number":"202407176666","license1":"341277","firm_zipcode":"94114-0000","role":"contractor"}',
        registry_source=SRC_B_JOIN_2,
        trade="multi-trade",
        area="sunset",
    ),
}

VERIFIED_ORDER = [
    "1140051",
    "830368",
    "786183",
    "1051988",
    "1097098",
    "1140843",
    "1026009",
    "1013565",
    "1112261",
    "341277",
    "1017991",
    "1120735",
    "1002370",
    "1028917",
    "658767",
    "373337",
    "342141",
]

# ------------------------------------------------- registry-only cohort (33)
# Tier 2. No CSLB page was opened for these licenses in wave 9, so ``license``
# stays null and the registry number is published only as a lead.
#
# kind "addr"  = row came from the plumbing-permit-contact registry filtered on
#                firm ZIP 94122 (SRC_FIRM94122), with permit numbers confirmed by
#                a second registry query (SRC_P_PERMITS_A/B/C).
# kind "pjoin" = row came from joining completed 94122 plumbing permits to their
#                recorded contacts (SRC_P_JOIN + SRC_P_RECENT).
# kind "bjoin" = row came from joining completed 94122 building permits whose
#                scope names drywall/sheetrock/ceiling/plaster work to their
#                recorded contacts (SRC_B_JOIN_1/2 + SRC_B_DRYWALL).
REGISTRY: list[dict] = [
    dict(number="1015230", name="Buteo Builders Inc", kind="addr",
         addr="1894 48th Ave", phone="415-519-0735",
         permits=["PP20210127971", "PP20180228229", "PP20171117466", "PP20170119297", "PP20161216513"],
         permits_src=SRC_P_PERMITS_A),
    dict(number="1016488", name="Kilb's Construction Inc", kind="addr",
         addr="1430 28th Av", phone="415-867-0054",
         permits=["PP20260612582", "PP20260225598", "PP20220516889", "PP20210816701"],
         permits_src=SRC_P_PERMITS_A,
         note=("The registry prints this firm name with a literal annotation, "
               "'Kilb's Construction Inc***Check Id***', which the City has not resolved.")),
    dict(number="1018406", name="Jones Bros Construction & Design Inc", kind="addr",
         addr="2636 Judah St 233", phone="415-341-7285",
         permits=["PM20220712886", "PP20180911723", "PP20180730539"],
         permits_src=SRC_P_PERMITS_A),
    dict(number="1021221", name="Kevel Home Performance", kind="addr",
         addr="2115 Judah St", phone="415-213-5545",
         permits=["PW20260723711", "PMW20260617769", "PMW20260611635", "PMW20260531295", "PMW20260413083"],
         permits_src=SRC_P_PERMITS_A),
    dict(number="1024196", name="Wnc Construction Inc", kind="addr",
         addr="3524 Lawton St", phone="415-819-6338",
         permits=["PP20250813113", "PP20250804895", "PM20250804896", "PP20190903012"],
         permits_src=SRC_P_PERMITS_B),
    dict(number="1027247", name="Richbay Construction", kind="addr",
         addr="1743 28th Ave", phone="415-999-5428",
         permits=["PP20250507130", "PP20250328352", "PP20231025729", "PP20231005376"],
         permits_src=SRC_P_PERMITS_B),
    dict(number="1033146", name="Block 12 Construction", kind="addr",
         addr="1770 26th Av", phone="415-261-4413",
         permits=["PP20220614415", "PP20210922456", "PP20201207207"],
         permits_src=SRC_P_PERMITS_B,
         note=("The registry carries two firm names against this one license number, "
               "'Block 12 Construction' and 'Shaun Ryan Construction'.")),
    dict(number="1039289", name="Sunset Builders Llc", kind="addr",
         addr="2309 Noriega St 388", phone="415-640-2268",
         permits=["PP20260225596", "PP20251121978", "PP20251105663", "PP20251017295",
                  "PP20250922817", "PM20260225597"],
         permits_src=SRC_P_PERMITS_C),
    dict(number="1047605", name="Sunset Remodeling And Design Inc", kind="addr",
         addr="1343 31st Av", phone="925-323-6527",
         permits=["PP20260721350", "PP20260106669", "PP20250714419", "PP20240523991"],
         permits_src=SRC_P_PERMITS_C),
    dict(number="1106329", name="Excalibur Water Heaters Inc", kind="pjoin",
         firm_zip="94595-0000", phone=None,
         permit=("PW20260821465", "2026-08-31", "1439 18th Av, San Francisco 94122",
                 "new water heater")),
    dict(number="1059891", name="Zhongwei Construction", kind="pjoin",
         firm_zip="94134-0000", phone="415-812-6691",
         permit=("PP20251119948", "2026-08-28", "1627 10th Av, San Francisco 94122",
                 "remodel two existing bathrooms on second floor including shower pan installation.")),
    dict(number="960561", name="Chl Construction Company", kind="pjoin",
         firm_zip="94121-0000", phone="415-297-8897",
         permit=("PP20260210330", "2026-08-26", "1775 37th Av, San Francisco 94122",
                 "3 bathroom, 1 kitchen, laundry room and 1 bar sink. underground plumbing")),
    dict(number="893710", name="Elux Construction Inc", kind="pjoin",
         firm_zip="94131-0000", phone="415-609-2028",
         permit=("PP20260219496", "2026-09-09", "1451 27th Av, San Francisco 94122",
                 "1/f remodel add 1 bathroom, 1 laundry room and 1 wet bar")),
    dict(number="805968", name="Flmc Development Corp dba Adamo Campagna", kind="pjoin",
         firm_zip="94044-0000", phone="415-310-8937",
         permit=("PP20260320064", "2026-09-03", "1847 47th Av, San Francisco 94122",
                 "install plumbing for new bathroom at g/f, move gas line for forced air unit, "
                 "new on demand water heater. underground plumbing.")),
    dict(number="1113396", name="Anova Build Inc", kind="pjoin",
         firm_zip="94502-0000", phone="510-993-4700",
         permit=("PP20260414498", "2026-08-25", "1882 41st Av, San Francisco 94122",
                 "first floor: remodel bathroom, shower pan and convert family room to "
                 "kitchennete per plan. repair and replace floor drain at rear yard.")),
    dict(number="872779", name="All Bay Cities Construction", kind="pjoin",
         firm_zip="94132-0000", phone="415-716-7023",
         permit=("PP20260420601", "2026-08-31", "1845 Irving St, San Francisco 94122",
                 "add new ada bathroom, water heater, floor sink, fountain")),
    dict(number="1059074", name="Vij Construction Inc", kind="pjoin",
         firm_zip="94801-0000", phone="415-694-1061",
         permit=("PP20260706008", "2026-09-03", "1268 15th Av, San Francisco 94122",
                 "replacing new vanity, shower valve, kitchen faucet, work in kitchen & bathroom.")),
    dict(number="851213", name="328 Construction", kind="pjoin",
         firm_zip="94015-0000", phone="415-828-3668",
         permit=("PW20260816284", "2026-08-31", "1356 34th Av, San Francisco 94122",
                 "replace the downspout roof drain pipe from the roof to the existing connection "
                 "above the ground")),
    dict(number="1108989", name="Gagne Rossie Enterprises Inc", kind="bjoin",
         firm_zip="94949-0000", phone=None,
         permit=("202501228824", "2025-09-02", "1270 11th Av, San Francisco 94122",
                 "interior demolition for fire/water damage mitigation: plaster, drywall, "
                 "flooring. replacement by others. no wall demolition or wall construction.")),
    dict(number="752768", name="Zhou's International Inc.", kind="bjoin",
         firm_zip="94118-3821", phone=None,
         permit=("202407055910", "2026-02-12", "1354 29th Av, San Francisco 94122",
                 'replace sheetrock in living, dining, and bedroom. in kind 5/8" type x gyp.')),
    dict(number="1035618", name="Gendros Construction", kind="bjoin",
         firm_zip="94561-0000", phone=None,
         permit=("202309146617", "2026-07-21", "1270 La Playa, San Francisco 94122",
                 "repair all floors where all interior finish including walls and ceiling are "
                 "removed due to smoke & water damage during fire on the 3/f. repair the exterior "
                 "walls, including stucco, architectural motifs, windows")),
    dict(number="812877", name="Sean M O'Reilly", kind="bjoin",
         firm_zip="94127-0000", phone=None,
         permit=("202603127447", "2026-04-17", "1464 La Playa, San Francisco 94122",
                 "unit 308: replace dryrot framing and drywall inside unit. to comply with nov "
                 "202649630 #2. all work is interior.")),
    dict(number="1087651", name="All Property Tech Llc.", kind="bjoin",
         firm_zip="94545-0000", phone=None,
         permit=("202506128626", "2025-11-18", "1855 27th Av, San Francisco 94122",
                 "replace framing of 2/f between garage and living room (~40 sqft). replace "
                 "damaged drywall. replace flooring. no exterior work. work inkind")),
    dict(number="1106767", name="Wtam Builder", kind="bjoin",
         firm_zip="94530-0000", phone=None,
         permit=("202408027842", "2025-11-07", "1438 39th Av, San Francisco 94122",
                 'remove interior drywall in living room & insulate w/ safe & rockwool insulation '
                 'for sound dampening. replace drywall w/ 5/8"')),
    dict(number="1020870", name="Zamora Construction", kind="bjoin",
         firm_zip="95376-0000", phone=None,
         permit=("202508132992", "2026-03-03", "1607 44th Av, San Francisco 94122",
                 "demolition of drywall to install insulation throughout house and replace drywall "
                 "due to poor condition. replace 3 windows.")),
    dict(number="1004147", name="Kevin Lin Construction Inc", kind="bjoin",
         firm_zip="94132-0000", phone=None,
         permit=("202509054630", "2026-03-13", "2923 Lawton St, San Francisco 94122",
                 "remodel kitchen @ 2nd floor. replace sheetrock @ 2nd floor.")),
    dict(number="1111917", name="Mars Construction And Remodeling", kind="bjoin",
         firm_zip="94521-0000", phone=None,
         permit=("202512030860", "2026-02-17", "2722 Judah St, San Francisco 94122",
                 "bathroom remodel w/ removal of partition non-load bearing walls, doors (e) "
                 "shower enclosure, vanity, toilet & closet. relocation of vanity, large showers, "
                 "(n) toilet, washer&dryer. (n) tile vanity, lights mirrors, plumbing fixtures, "
                 "paint, gfci outlets, ceiling fan w/ humidity sensor.")),
    dict(number="1111133", name="Boman Design & Construction Inc", kind="bjoin",
         firm_zip="94134-0000", phone=None,
         permit=("202512051101", "2026-02-18", "1336 10th Av, San Francisco 94122",
                 "rear structure: remodel bathroom at rear building 1336a 10th ave, sf, ca 94122, "
                 "replace toilet, vanity ceiling light, shower using existing electrical & "
                 "plumbing, in kind"),
         note=("The registry prints the firm name as 'Boman Deign & Construction Inc' "
               "('Deign'), which does not match the spelled-out design word used elsewhere.")),
    dict(number="613489", name="Lin's Builder", kind="bjoin",
         firm_zip="94134-0000", phone=None,
         permit=("202502180456", "2025-07-18", "2407 Judah St, San Francisco 94122",
                 "relocate mop sink, (2) hand sinks, grease trap, (1) floor sink, and water heater "
                 "in commercial kitchen. provide minor changes to commercial kitchen ceiling "
                 "framing.")),
    dict(number="1101204", name="Csq Inc", kind="bjoin",
         firm_zip="94080-0000", phone=None,
         permit=("202510298498", "2026-05-18", "1809 Irving St, San Francisco 94122",
                 "interior tenant improvement, demolition sf non structural partitions, new "
                 "partitions, light fixtures, ceiling assemblies, millwork, plumbing, door "
                 "assemblies and finishes. mep under separate permit")),
    dict(number="1078252", name="Plus One Construction Inc", kind="bjoin",
         firm_zip="94015-0000", phone=None,
         permit=("202602105651", "2026-04-24", "1309 09th Av, San Francisco 94122",
                 "repaint dining area wall and ceiling. replace dining floor tiles. "
                 "(no plumbing and electrical).")),
    dict(number="685246", name="David Rodriguez Construction", kind="bjoin",
         firm_zip="94605-0000", phone=None,
         permit=("202011098549", "2025-09-05", "1363 35th Av, San Francisco 94122",
                 '2/f: remodel (e) kitchen & bathroom and add 1 bathroom & laundry; infill (e) '
                 'lightwells; rebuild (e) interior stairs up to code from 2/f to ground; 2 new '
                 'bedrooms, 2 bathrooms and media room on g/f; replace (e) sheetrock with new '
                 '5/8in type x, new electrical wiring & fixtures.')),
    dict(number="1114615", name="Blue Sky Building", kind="bjoin",
         firm_zip="94134-0000", phone=None,
         permit=("201710110865", "2026-03-31", "1719 33rd Av, San Francisco 94122",
                 'horizontal & vertical addition with a new adu proposed, adu on the lower level. '
                 'all windows to be replaced, minor excavation at lower level to maintain 9\'-0" '
                 'floor to ceiling in living space')),
]


# --------------------------------------------------------------- source table
def q(dataset: str, select: str, where: str, order: str = "", limit: int = 200,
      group: str = "") -> str:
    """Build a SODA query URL in the same encoded form the earlier waves used."""
    from urllib.parse import urlencode

    parts: list[tuple[str, str]] = [("$select", select), ("$where", where)]
    if group:
        parts.append(("$group", group))
    if order:
        parts.append(("$order", order))
    parts.append(("$limit", str(limit)))
    return SODA + dataset + ".json?" + urlencode(parts)


def inlist(numbers: list[str]) -> str:
    return "(" + ",".join(f"'{n}'" for n in numbers) + ")"


ADDR_PERMITS = [p for r in REGISTRY if r["kind"] == "addr" for p in r["permits"]]
PJOIN_PERMITS = [r["permit"][0] for r in REGISTRY if r["kind"] == "pjoin"]
BJOIN_PERMITS = [r["permit"][0] for r in REGISTRY if r["kind"] == "bjoin"]
BJOIN_1 = BJOIN_PERMITS[:8]
BJOIN_2 = BJOIN_PERMITS[8:]
PJOIN_CONTACTS = PJOIN_PERMITS + [
    "PP20260810750", "PW20260303050", "PW20260706215", "PW20260802933",
    "PW20260803947", "PW20260813237", "PP20260107698", "PP20260731567",
]

P_SELECT = "permit_number,license_number,firm_name,address,city,zipcode,phone"
D_SELECT = ("permit_number,status,completed_date,description,street_number,"
            "street_name,street_suffix,zipcode")
C_SELECT = "permit_number,firm_name,license1,role,firm_address,firm_city,firm_zipcode"

CSLB_NOTES = {
    "1140051": "Active C-36 read directly: Vallejo business address, LLC form, both contractor and LLC worker bonds displayed, WC exempt (no employees), and a $2,000,000 Ategrity liability policy effective 06/10/2026-06/10/2027. Liability coverage is displayed but has not been independently verified against the insurer.",
    "830368": "Active C-36 read directly. The page still says current and active but displays State Fund workers-compensation policy 9242676 with CANCELLATION DATE 09/11/2026 - one day before this research date. No liability-insurance section is displayed.",
    "786183": "Active license read directly with FOUR classifications: A, C-36, B and C-16. Bond effective 07/01/2026, WC Everest Premier effective 10/27/2025 expiring 10/27/2026. License expiry 2026-10-31 is inside seven weeks of the research date.",
    "1051988": "Active C-36 read directly: Daly City corporation, bond effective 08/05/2026, WC Markel effective 08/20/2026 expiring 08/20/2027. No liability-insurance section displayed.",
    "1097098": "Active C-36 read directly: Daly City corporation, bond effective 09/22/2025, WC Security National effective 01/03/2026 expiring 01/03/2027. No liability-insurance section displayed.",
    "1140843": "Active C-36 plus A read directly. Both a qualifying-individual bond and a filed (not waived) BQI for two individuals are displayed, plus WC and a $2,000,000 liability policy effective 04/01/2026-04/01/2027.",
    "1026009": "Active C-36 read directly: Pacifica partnership, bond effective 09/01/2026, WC exempt (no employees). No liability-insurance section displayed.",
    "1013565": "Active license read directly holding BOTH C-36 plumbing and B general building - the only verified wave-9 record besides Coit Construction and Lam Pui whose classifications cover plumbing and building work on one license. WC exempt (no employees); no liability-insurance section displayed.",
    "1112261": "Active C-36 plus C-16 fire protection read directly. The CSLB page itself records 1847 48th Ave, San Francisco, CA 94122 - an Outer Sunset business address confirmed by the regulator rather than by a directory. WC exempt (no employees).",
    "1028917": "Read directly and found EXPIRED 2021-07-31, with B only and NO C-36 classification, yet the City registry places this license on plumbing-permit contact rows. Bond cancelled 07/30/2022.",
    "658767": "Read directly and found EXPIRED 2000-11-30. C-35 lathing and plastering only. Bond cancelled 09/23/1999. The CSLB business address is 330 Ortega Street, San Francisco 94122 - inside the Outer Sunset - but the license has been expired for 26 years.",
    "373337": "Read directly and found EXPIRED 2010-04-30 with B, C-10 and C-36. The page shows Reissue Date 04/06/2006 and the misc note '04/06/2006 LICENSE REISSUED TO ANOTHER ENTITY', so the number no longer identifies the original contractor. Bond cancelled 05/03/2012; WC cancelled 04/12/2010.",
    "1017991": "Active B-only license read directly. The page carries the Additional Status line 'There is Complaint Disclosure information for this license', and the disclosure page was read: Complaint # N A 2025 2297 dated 06/23/2026 with status LETTER OF ADMONISHMENT ISSUED. CSLB states a listed complaint is only an allegation of a probable violation and does not affect license status.",
    "1120735": "Active license read directly holding B-2 RESIDENTIAL REMODELING plus B GENERAL BUILDING. B-2 is a real CSLB classification that this dataset's allowed-class list did not previously contain; it has been added rather than silently mapped onto B. No C-36.",
    "342141": "Read directly and found EXPIRED 1997-09-30, C-36 only, bond cancelled 12/15/1985, and the page states 'There was no workers comp information found for this license.' The CSLB licensee is LEE'S PLUMBING CO at 217 Willard North, San Francisco 94118.",
    "341277": "Active license read directly holding B GENERAL BUILDING and C-36 PLUMBING on one license, issued 08/08/1977. WC exempt effective 09/13/2025; no liability-insurance section displayed.",
    "1002370": "Read directly and found INACTIVE: the page states the license is not able to contract and still needs a contractors bond and workers-compensation compliance to reactivate. Bond cancellation 04/08/2023 and WC-exempt cancellation 04/01/2023 are both displayed. Displayed expiry is 2027-03-31 but an expiry date on an inactive license is not permission to contract.",
}


def src(sid: int, title: str, url: str, kind: str, access: str, note: str) -> dict:
    return {"id": sid, "title": title, "url": url, "kind": kind,
            "access": access, "checkedAt": DATE, "note": note}


SOURCES: list[dict] = [
    src(SRC_FIRM94122,
        "SF DBI · Plumbing Permits Contacts · every licence with a 94122 firm address",
        q("k6kv-9kix",
          "license_number,max(firm_name) as firm,max(address) as addr,max(phone) as phone,"
          "count(permit_number) as permits",
          "zipcode like '94122%' AND license_number is not null",
          order="permits DESC", limit=500, group="license_number"),
        "government", "page",
        "Official City & County of San Francisco open-data API (dataset k6kv-9kix, "
        "\u201cPlumbing Permits Contacts\u201d, provenance: official), queried directly and grouped by "
        "licence number so every firm name, address and phone a licence appears under in ZIP 94122 "
        "is visible. Rows already stored in waves 1-8 were removed before wave-9 candidate "
        "selection. Registry rows are historical permit contacts: they establish a recorded "
        "address and a licence linkage, not current status, classification or availability."),
    src(SRC_B_DRYWALL,
        "SF DBI · completed 94122 building permits naming drywall, sheetrock, ceiling or plaster work",
        q("i98e-djp9", D_SELECT,
          "zipcode='94122' AND status='complete' AND (lower(description) like '%drywall%' OR "
          "lower(description) like '%sheetrock%' OR lower(description) like '%gyp%' OR "
          "lower(description) like '%ceiling%' OR lower(description) like '%plaster%' OR "
          "lower(description) like '%stucco%')",
          order="completed_date DESC", limit=200),
        "government", "page",
        "Official building-permit detail rows. Each retained row was confirmed complete with a "
        "94122 work location before use. Descriptions support only the work words actually "
        "printed; a permit never identifies which contact performed which task."),
    src(SRC_P_RECENT,
        "SF DBI · completed 94122 plumbing permits in the recent window",
        q("a6aw-rudh", D_SELECT,
          "zipcode='94122' AND status='complete' AND completed_date >= '2025-06-01T00:00:00.000'",
          order="completed_date DESC", limit=200),
        "government", "page",
        "Official plumbing-permit detail rows, newest completions first, so wave 9 works from "
        "current rather than archival plumbing activity in the Outer Sunset."),
    src(SRC_B_JOIN_1,
        "SF DBI · building-permit contact join, drywall-scope permit batch 1",
        q("3pee-9qhc", C_SELECT, "permit_number in " + inlist(BJOIN_1), limit=200),
        "government", "page",
        "Official building-permit contact rows for the first batch of completed 94122 "
        "drywall/ceiling-scope permits. Extra contacts can exist on a permit; claims use only the "
        "selected licence/permit pair and never infer that every contact performed every task."),
    src(SRC_B_JOIN_2,
        "SF DBI · building-permit contact join, drywall-scope permit batch 2",
        q("3pee-9qhc", C_SELECT, "permit_number in " + inlist(BJOIN_2), limit=200),
        "government", "page",
        "Second batch of the same official contact join, kept separate because a single wide query "
        "truncates and would have hidden rows behind one prolific firm."),
    src(SRC_P_JOIN,
        "SF DBI · plumbing-permit contact join for recent completed 94122 permits",
        q("k6kv-9kix", P_SELECT, "permit_number in " + inlist(PJOIN_CONTACTS), limit=200),
        "government", "page",
        "Official plumbing-permit contact rows for the recent completed 94122 permits. This is the "
        "join that supplies licence number, firm name, firm address, firm ZIP and phone for both "
        "verified and registry-only wave-9 records."),
    src(SRC_B_FIRM94122,
        "SF DBI · Building Permit Contacts · contractor rows with firm ZIP 94122",
        q("3pee-9qhc",
          "license1,firm_name,firm_address,firm_city,firm_zipcode,role,count(permit_number) as permits",
          "firm_zipcode like '94122%' AND license1 is not null",
          order="permits DESC", limit=500, group="license1,firm_name,firm_address,firm_city,firm_zipcode,role"),
        "government", "page",
        "Official building-permit contact dataset used to find contractors whose own business "
        "address sits in ZIP 94122. Licence numbers returned here are leads: none was promoted "
        "into a licence fact without a CSLB page read."),
    src(SRC_P_PERMITS_A,
        "SF DBI · permit numbers for registry licences, set A (94122 firm addresses)",
        q("k6kv-9kix", "permit_number,license_number",
          "license_number in " + inlist(["1015230", "1016488", "1018406", "1021221"])
          + " AND zipcode like '94122%'",
          order="license_number,permit_number DESC", limit=60),
        "government", "page",
        "Compact confirmatory query returning only permit_number and licence_number, newest first, "
        "so each registry-only record publishes real permit identifiers instead of a bare count."),
    src(SRC_P_PERMITS_B,
        "SF DBI · permit numbers for registry licences, set B (94122 firm addresses)",
        q("k6kv-9kix", "permit_number,license_number",
          "license_number in " + inlist(["1024196", "1027247", "1033146"])
          + " AND zipcode like '94122%'",
          order="license_number,permit_number DESC", limit=60),
        "government", "page",
        "Second compact confirmatory query. Sets are split into small licence batches because a "
        "single wide query was consumed by one very prolific firm and silently dropped the rest."),
    src(SRC_P_PERMITS_C,
        "SF DBI · permit numbers for registry licences, set C (94122 firm addresses)",
        q("k6kv-9kix", "permit_number,license_number",
          "license_number in " + inlist(["1039289", "1047605"]) + " AND zipcode like '94122%'",
          order="license_number,permit_number DESC", limit=60),
        "government", "page",
        "Third compact confirmatory query, covering the two Sunset-named 94122 firms with heavy "
        "2025-2026 plumbing-permit activity."),
    src(SRC_P_FIRMADDR,
        "SF DBI · firm-address confirmation for licences whose CSLB address is already 94122",
        q("k6kv-9kix", "license_number,firm_name,address,zipcode,phone",
          "license_number in " + inlist(["1112261", "658767"]), limit=50),
        "government", "page",
        "Used to cross-check the two wave-9 licences whose CSLB page itself records a 94122 "
        "business address. Agreement between regulator and City registry is what earns those "
        "records the Outer Sunset area label."),
]

for index, number in enumerate(VERIFIED_ORDER):
    r = READS[number]
    SOURCES.append(src(
        CSLB_FIRST + index,
        f"CSLB license detail #{number} · {r['name']}",
        CSLB_URL + number, "government", "page",
        "California Contractors State License Board detail page opened directly on 2026-09-12 and "
        "transcribed field by field: legal entity, business form, mailing address, phone, issue "
        "and expiry dates, status text, every displayed classification, bond, workers-compensation "
        "and liability lines, and any Additional Status line. " + CSLB_NOTES[number],
    ))

SOURCES.append(src(
    DISCLOSURE_1017991,
    "CSLB complaint disclosure for license #1017991 · San Francisco Remodel",
    DISCLOSURE_URL + "1017991", "government", "page",
    "Opened directly after the license page displayed the Additional Status line 'There is "
    "Complaint Disclosure information for this license.' The page lists Complaint # N A 2025 2297, "
    "date 06/23/2026, status LETTER OF ADMONISHMENT ISSUED, together with CSLB's own statement "
    "that any complaint listed is only an allegation of a probable violation and does not affect "
    "the status of the license at this time. Recorded as an allegation, never as a finding.",
))

SOURCES += [
    src(YELP_INNOVATION,
        "Yelp · Innovation Plumbing and Rooter (San Francisco)",
        "https://www.yelp.com/biz/innovation-plumbing-and-rooter-san-francisco",
        "platform", "search-extract",
        "Search-extract read only; Yelp blocks direct page fetches in this environment. The "
        "extract shows a 1.0-star aggregate from exactly one review and an unclaimed listing. The "
        "single review's text, date and author could NOT be retrieved, so no review record is "
        "attached and the 1.0-star figure is published as an unverified aggregate signal only."),
    src(CYLEX_INNOVATION,
        "Cylex · Innovation Plumbing and Rooter directory listing",
        "https://www.cylex.us.com/ca/san-francisco/innovation-plumbing-and-rooter.html",
        "directory", "search-extract",
        "Third-party directory extract. Checked for an independent review corpus for license "
        "1013565; it carries contact data and no attributable customer reviews, so it supports "
        "identity only and is never used for a rating."),
    src(YELP_DISCOUNT,
        "Yelp · Discount Plumbing Rooter Services (San Francisco)",
        "https://www.yelp.com/biz/discount-plumbing-rooter-services-san-francisco-2",
        "platform", "search-extract",
        "Search-extract read only. The extract shows a 4.5-star aggregate across roughly 1,300 "
        "reviews, and the only review text reachable is JSON-LD photo-caption metadata rather than "
        "a dated customer review. Per this project's quarantine rule, caption metadata is stored "
        "as a source and is NOT converted into a review record."),
    src(HOMEADVISOR_SMELLY,
        "HomeAdvisor/Angi · Smelly Mel's Plumbing Htg rated page",
        "https://www.homeadvisor.com/rated.SmellyMelsPlumbingHtg.7558800.html",
        "platform", "search-extract",
        "Rated page extract showing a 3.8 of 5 aggregate from 8 reviews plus three individually "
        "attributable reviews with author initial, month/year, star value and project cost band. "
        "Identity is matched to CSLB license 786183 by exact corporate name and South San "
        "Francisco location, and by the CSLB phone (415) 758-6237 appearing on a directory "
        "restatement of the same business. Aggregate scores are never blended with other "
        "platforms."),
    src(SERVICEAGENT_SMELLY,
        "ServiceAgent directory · Smelly Mel's Plumbing",
        "https://serviceagent.ai/plumber/california/south-san-francisco/smelly-mel-s-plumbing",
        "directory", "search-extract",
        "Third-party directory restating a 4.8 of 5 'Google' score from 243 reviews. The "
        "restatement could not be confirmed on Google itself, so it is recorded as an unverified "
        "third-party claim and is never presented as an official Google rating. Useful for one "
        "thing only: it prints (415) 758-6237, which matches the CSLB phone exactly and supports "
        "the identity match used for the HomeAdvisor reviews."),
    src(BUILDZOOM_COIT,
        "BuildZoom · Coit Construction profile",
        "https://www.buildzoom.com/contractor/coit-construction",
        "directory", "search-extract",
        "Directory extract for license 341277. It states the profile 'hasn't received any "
        "reviews', lists 43 permits, and prints a 763 Noe St, San Francisco 94114 address - a "
        "third ZIP variant alongside CSLB 94110 and registry 94122. Absence of reviews is recorded "
        "as a gap, never as a positive signal."),
    src(BUILDZOOM_YU,
        "BuildZoom · Yu Pluming Inc profile (name printed as 'Yu Pluming')",
        "https://www.buildzoom.com/contractor/yu-pluming-inc",
        "directory", "search-extract",
        "Directory extract for license 1051988. The profile title misspells the business as 'Yu "
        "Pluming' and states no reviews have been received. The same page links an INACTIVE "
        "'Y&L Plumbing Inc' (license 1041444, expired 2018) at the same 148 San Diego Ave address, "
        "which is an entity-confusion risk. No record was created for 1041444."),
    src(BUILDZOOM_HJ,
        "BuildZoom · H&J Plumbing Inc profile",
        "https://www.buildzoom.com/contractor/h-j-plumbing-inc",
        "directory", "search-extract",
        "Directory extract for license 1097098. States no reviews have been received and lists 9 "
        "sewer-lateral permits plus house-trap permit PP20250207423, corroborating the CSLB read "
        "and the retained 94122 house-trap replacement."),
    src(YELP_KEVEL,
        "Yelp · Kevel Home Performance (3624 Ortega St, San Francisco 94122)",
        "https://www.yelp.com/biz/kevel-home-performance-san-francisco",
        "platform", "search-extract",
        "Search-extract read only. Shows 3624 Ortega St, San Francisco 94122 and (415) 213-5545, "
        "matching the City registry row for license 1021221 exactly on both address and phone - "
        "that is what makes the retained reviews safely attributable. Aggregate 5.0 stars from 32 "
        "reviews. Two snapshots disagree on whether the listing is claimed or unclaimed, and the "
        "categories shown are HVAC, energy and insulation rather than plumbing or drywall."),
    src(ANGI_KEVEL,
        "Angi · Kevel Home Performance reviews",
        "https://www.angi.com/companylist/us/ca/san-francisco/kevel-home-performance-reviews.htm",
        "platform", "search-extract",
        "Angi rated-page extract: 5.0 of 5 from 1 review, reviewer Ian H., June 2014, and a "
        "printed note that the business does not offer free estimates. A single 2014 review is "
        "historical context, not current performance evidence."),
    src(THUMBTACK_SF_DRYWALL,
        "Thumbtack · San Francisco drywall repair category page",
        "https://www.thumbtack.com/ca/san-francisco/drywall-repair",
        "platform", "search-extract",
        "Category page, not a business page. It contains an on-point account of patching a "
        "bathroom ceiling hole and texturing to match, but the extract does not establish which "
        "licensed business performed it, so it is stored as a source only and is NOT attributed to "
        "any record or converted into a review."),
    src(THUMBTACK_CEILING,
        "Thumbtack · ceiling drywall repair category page",
        "https://www.thumbtack.com/k/ceiling-drywall-repair/near-me",
        "platform", "search-extract",
        "Category page quoting a customer describing a pro 'installing a panel for a hole in our "
        "ceiling'. Unattributable to any wave-9 licensee, so it stays a source and supports the "
        "general finding that ceiling-hole patching is a routinely offered small job."),
    src(THUMBTACK_SSF_DRYWALL,
        "Thumbtack · South San Francisco drywall repair category page",
        "https://www.thumbtack.com/ca/south-san-francisco/drywall-repair",
        "platform", "search-extract",
        "Category page with JSON-LD aggregate data for one named pro (4.677 of 5 from 31 reviews). "
        "That pro is not a wave-9 candidate and the page is not a verified business profile, so "
        "the aggregate is quarantined here rather than attached to a record."),
    src(REDDIT_TRIP_LEVER,
        "Reddit r/Plumbing · stuck bathtub overflow trip lever thread",
        "https://www.reddit.com/r/Plumbing/comments/170tvds/",
        "community", "search-extract",
        "Community thread on a stuck trip lever where penetrating oil and steam both failed, one "
        "reply states the work 'went thru the drywall', and another describes an old pipe "
        "crumbling when disturbed. Directly on-task for the repair-first question, but it names no "
        "business, so it is task evidence and never review evidence."),
    src(REDDIT_ACCESS_BELOW,
        "Reddit r/askaplumber · accessing a tub drain from behind and below",
        "https://www.reddit.com/r/askaplumber/comments/1pbycaf/",
        "community", "search-extract",
        "Community thread describing access 'from behind and below' through a downstairs "
        "neighbour's ceiling, galvanized rust debris in the drain, and an endoscope inspection "
        "before cutting. Relevant to the access-hatch question; unattributable to any business."),
    src(REDDIT_1940S_TUB,
        "Reddit r/HomeImprovement · 1940s tub overflow gasket thread",
        "https://www.reddit.com/r/HomeImprovement/comments/20ozpm/",
        "community", "search-extract",
        "Community thread about a 1940s-era tub with an odd 1 3/8 inch pipe where the poster "
        "ultimately hired a plumber. Supports the age-of-house context for galvanized systems; "
        "names no business."),
    src(REDDIT_SHEETROCK,
        "Reddit r/Plumbing · trip lever screws and sheetrock repair thread",
        "https://www.reddit.com/r/Plumbing/comments/1gkjesd/",
        "community", "search-extract",
        "Community thread in which a reply frames the necessary sheetrock work as 'sheetrock "
        "isn't hard', i.e. the finish patch is the minor part of the job. Task evidence only."),
    src(REDDIT_SF_PRICING,
        "Reddit r/sanfrancisco · San Francisco home-service pricing complaints",
        "https://www.reddit.com/r/sanfrancisco/comments/1i7vp0g/",
        "community", "search-extract",
        "Community thread on San Francisco service pricing and marketplace behaviour. Retained "
        "because it explains why this project verifies licensing and insurance itself instead of "
        "trusting a marketplace ranking. No business is named or rated."),
]

SOURCE_IDS = [s["id"] for s in SOURCES]
assert SOURCE_IDS == list(range(306, 353)), SOURCE_IDS
assert len({s["id"] for s in SOURCES}) == len(SOURCES)


# --------------------------------------------------------------- builders
def slug(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def claim(field: str, text: str, sid: int, excerpt: str) -> dict:
    return {"field": field, "text": text, "source": sid, "excerpt": excerpt}


def flag(level: str, text: str, *sources: int) -> dict:
    return {"level": level, "text": text, "sources": list(sources)}


def link(label: str, url: str, sid: int) -> dict:
    return {"label": label, "url": url, "source": sid}


def tail(gaps: list[str]) -> list[str]:
    """Gaps every wave-9 record shares: the exact task was never proven."""
    return gaps + [
        "No source proves successful extraction of this exact seized bathtub overflow trip lever.",
        "No written repair-first stop point or authorization boundary was obtained from this business.",
        "Project-specific liability and workers-compensation coverage were not independently verified.",
    ]


REGISTRY_GAP = (
    "Registry licence number {number} is printed by the City's own open data but was NOT read on "
    "CSLB in this pass. Status, classification, legal entity, expiry, bond and workers' "
    "compensation are all unknown; the number is a lead, never a credential."
)
REGISTRY_NOTICE = (
    "Registry rows are historical permit contacts. They prove a recorded firm address, a licence "
    "linkage and a permit identifier; they do not prove the firm is operating today, that it still "
    "holds that licence, or that it dispatches to the Outer Sunset now."
)
REGISTRY_TRADE_NOTICE = (
    "The trade label on this record is 'registry lead'. It names only the official City registry "
    "channel that surfaced the row and is deliberately not a classification claim: no CSLB page "
    "was read, so no C-36, C-9, C-35 or B is asserted."
)

BUSINESSES: list[dict] = []

# ---------------------------------------------------- tier 1: CSLB-read rows
AREA_OVERRIDE = {
    "1002370": (
        "The City registry places a 94122 firm address (536 Judah St) and a 415 phone against this "
        "licence, while CSLB records the licensee in Sonora, CA 95370. The registry rows are "
        "historical plumbing-permit contacts from 2015-2017; current Outer Sunset dispatch is "
        "unconfirmed and the licence is inactive."
    ),
    "1028917": (
        "The City registry places this licence at 1523 32nd Av, ZIP 94122 on plumbing-permit rows, "
        "while CSLB records 720 Pine Street, San Francisco 94108. Both readings are published; the "
        "conflict is unresolved and the licence expired in 2021."
    ),
    "373337": (
        "The City registry prints 94122 rows for this licence under six name variants, while CSLB "
        "records 2900 Yorba St, San Francisco 94116 and states the licence was reissued to another "
        "entity in 2006. No current Outer Sunset coverage can be claimed from this row."
    ),
    "342141": (
        "The City registry lists licence 342141 under 'L & L Plumbing Inc.' with a 94122 address, "
        "while the CSLB licensee is LEE'S PLUMBING CO at 217 Willard North, San Francisco 94118. "
        "The name and address conflict is unresolved and the licence expired in 1997."
    ),
}

for index, number in enumerate(VERIFIED_ORDER):
    r = READS[number]
    sid = CSLB_FIRST + index
    active = r["status"] == "active"
    classes = ", ".join(r["classes"])
    permit = r.get("permit")
    claims = [
        claim(
            "Discovery",
            "The CSLB detail page was opened directly and transcribed line by line: legal entity, "
            "business form, address, phone, issue and expiry dates, status text, every displayed "
            "classification, bond, workers-compensation and liability lines, and any Additional "
            "Status line.",
            sid,
            f"#{number} · {r['entity']} · {r['status']} · {classes} · issued {r['issued']} · "
            f"expires {r['expires']} · {r['form']}",
        ),
        claim(
            "Credential",
            f"CSLB displays licence #{number} as {r['status']} with classification(s) {classes}. "
            f"The page states: '{r['status_text']}' A licence status never establishes "
            "exact-task experience.",
            sid,
            f"{r['status_text']} · {r['addr']} · {r['phone']}",
        ),
        claim(
            "Insurance & bond",
            "Bond, workers-compensation and liability lines were read on the regulator page rather "
            "than accepted from a directory. Displayed coverage is recorded as displayed; it has "
            "not been confirmed with the insurer for this project.",
            sid,
            r["extra"],
        ),
    ]
    if permit:
        pid, completed, paddr, scope = permit
        claims.append(claim(
            "Permit linkage",
            f"The official City permit-contact dataset associates licence #{number} with permit "
            f"{pid}. A contact row identifies who was recorded on the permit; it does not allocate "
            "every task on a multi-contact permit.",
            r["permit_contact_source"],
            f'{{"permit_number":"{pid}","license_number":"{number}"}}',
        ))
        claims.append(claim(
            "Permit scope",
            f"Permit {pid} is recorded complete on {completed} at {paddr}. The printed scope is "
            "quoted verbatim and supports only the work words actually shown.",
            r["permit_detail_source"],
            f'{{"permit_number":"{pid}","status":"complete","completed_date":"{completed}",'
            f'"address":"{paddr}","description":"{scope}"}}',
        ))
        if r.get("permit2"):
            pid2, completed2, paddr2, scope2 = r["permit2"]
            claims.append(claim(
                "Permit scope",
                f"A second completed 94122 permit, {pid2} ({completed2}) at {paddr2}, is recorded "
                "against the same licence in the same window.",
                r["permit_detail_source"],
                f'{{"permit_number":"{pid2}","status":"complete","completed_date":"{completed2}",'
                f'"address":"{paddr2}","description":"{scope2}"}}',
            ))
    claims.append(claim(
        "Registry identity",
        r["registry"],
        r["registry_source"],
        r["registry_excerpt"],
    ))

    flags: list[dict] = []
    top_status = "research"

    if r["area"] == "outer":
        area_text = (
            f"CSLB itself records the business at {r['addr']} in ZIP 94122 and the City registry "
            "agrees. A regulator-read Outer Sunset address is the strongest local evidence "
            "available in this dataset, but it is not a scheduling promise."
        )
        claims.append(claim(
            "Coverage",
            f"The CSLB page records the business address as {r['addr']}, inside ZIP 94122, and the "
            "official City registry returns the same licence against a 94122 firm address.",
            sid,
            f"{r['addr']} · {r['registry_excerpt']}",
        ))
    elif number in AREA_OVERRIDE:
        area_text = AREA_OVERRIDE[number]
        claims.append(claim(
            "Coverage",
            "Registry and regulator readings disagree about this licence's San Francisco address. "
            "Both are published and the conflict is left open rather than resolved by assumption.",
            r["registry_source"],
            r["registry_excerpt"],
        ))
    elif permit:
        area_text = (
            f"A completed official permit places work at {permit[2]} in ZIP 94122; CSLB records the "
            f"business at {r['addr']}. Neither reading is a current Outer Sunset dispatch promise."
        )
        claims.append(claim(
            "Coverage",
            f"Completed permit {permit[0]} at {permit[2]} places verified work inside ZIP 94122, "
            f"while the CSLB business address is {r['addr']}.",
            r["permit_detail_source"],
            f'{{"permit_number":"{permit[0]}","completed_date":"{permit[1]}","zipcode":"94122"}}',
        ))
    else:
        area_text = (
            f"CSLB records the business at {r['addr']}, outside ZIP 94122. Local evidence for this "
            "record is registry-level only and current Outer Sunset dispatch is unconfirmed."
        )
        claims.append(claim(
            "Coverage",
            "No completed 94122 work-location permit was selected for this licence in this pass; "
            "the only local reading is the registry row.",
            r["registry_source"],
            r["registry_excerpt"],
        ))

    # --- per-licence irregularities, each tied to the page that showed it
    if not active:
        top_status = "hold"
        flags.append(flag(
            "hold",
            f"CSLB displays licence #{number} as {r['status']} (displayed expiry {r['expires']}). "
            "Do not book under a non-active licence; retain only as historical permit and identity "
            "context.",
            sid,
        ))
    if number == "1002370":
        flags.append(flag(
            "discrepancy",
            "The City registry prints a 94122 firm address (536 Judah St) and phone 415-699-9385 "
            "while CSLB records Sonora, CA 95370 and 415-902-4457. Both readings are published; "
            "neither is treated as the current one.",
            sid, SRC_FIRM94122,
        ))
        flags.append(flag(
            "notice",
            "A displayed expiry of 2027-03-31 on an INACTIVE licence is not permission to "
            "contract: CSLB also states a contractors bond and workers-compensation compliance are "
            "still required to reactivate.",
            sid,
        ))
    if number == "830368":
        top_status = "hold"
        flags.append(flag(
            "hold",
            "CSLB still says current and active but displays State Fund workers-compensation policy "
            "9242676 with CANCELLATION DATE 09/11/2026 - the day before this research date. "
            "Recheck coverage directly before any contact or scope discussion.",
            sid,
        ))
    if number == "786183":
        flags.append(flag(
            "discrepancy",
            "The official plumbing-permit registry prints phone 650-738-2030 while CSLB prints "
            "(415) 758-6237 for the same licence on the same date. Confirm the contracting entity "
            "and the number to call before contact.",
            sid, SRC_P_JOIN,
        ))
        flags.append(flag(
            "notice",
            "Displayed licence expiry 2026-10-31 falls within seven weeks of this research date. "
            "Recheck status at the time of any contact.",
            sid,
        ))
        flags.append(flag(
            "notice",
            "A third-party directory restates a 4.8 of 5 'Google' score from 243 reviews. That "
            "restatement could not be confirmed on Google itself and is never presented here as an "
            "official Google rating.",
            SERVICEAGENT_SMELLY,
        ))
        flags.append(flag(
            "discrepancy",
            "One retained HomeAdvisor review (Michael N., October 2009) displays 1.0 of 5 stars "
            "while its text reads as satisfied. Both the star value and the words are preserved "
            "exactly as published and neither is treated as established.",
            HOMEADVISOR_SMELLY,
        ))
    if number == "1051988":
        flags.append(flag(
            "discrepancy",
            "BuildZoom prints the business name as 'Yu Pluming Inc'. The CSLB legal entity is YU "
            "PLUMBING INC, so the directory spelling is treated as an error and never as a second "
            "business.",
            sid, BUILDZOOM_YU,
        ))
        flags.append(flag(
            "notice",
            "The same directory page links an INACTIVE 'Y&L Plumbing Inc' (licence 1041444, expired "
            "2018) at the same 148 San Diego Ave address. Entity confusion is a live risk here; no "
            "record was created for 1041444 and no evidence from it is used.",
            BUILDZOOM_YU,
        ))
        flags.append(flag(
            "gap",
            "BuildZoom states this profile 'hasn't received any reviews', and no other independent "
            "review corpus was retrievable in this pass. Absence of reviews is recorded as a gap, "
            "never as a positive signal.",
            BUILDZOOM_YU,
        ))
    if number == "1097098":
        flags.append(flag(
            "discrepancy",
            "The official plumbing-permit registry prints phone 415-819-8126 while CSLB prints "
            "(510) 388-8126 for the same licence on the same date.",
            sid, SRC_P_JOIN,
        ))
        flags.append(flag(
            "gap",
            "BuildZoom states this profile 'hasn't received any reviews'. Its permit data "
            "corroborates the CSLB read (9 sewer laterals and house-trap permit PP20250207423) but "
            "adds no customer evidence.",
            BUILDZOOM_HJ,
        ))
    if number == "1140843":
        flags.append(flag(
            "discrepancy",
            "The official plumbing-permit registry prints phone 650-991-2164 while CSLB prints "
            "(650) 991-2100 for the same licence on the same date.",
            sid, SRC_P_JOIN,
        ))
        flags.append(flag(
            "gap",
            "Yelp shows a 4.5-star aggregate across roughly 1,300 reviews, but the only review text "
            "reachable in this environment is JSON-LD photo-caption metadata. Caption metadata is "
            "quarantined as a source and is not converted into a review record, so no review is "
            "attached to this record.",
            YELP_DISCOUNT,
        ))
    if number == "1140051":
        flags.append(flag(
            "notice",
            "The CSLB business address is Vallejo, CA 94589. The 94122 evidence is one completed "
            "permit, not a local office; confirm current dispatch and travel policy before contact.",
            sid,
        ))
        flags.append(flag(
            "gap",
            "No independent review corpus was retrievable for this licence in this pass.",
            sid,
        ))
    if number == "1026009":
        flags.append(flag(
            "notice",
            "The CSLB business address is Pacifica, CA 94044, and CSLB shows workers' compensation "
            "exempt (no employees). A no-employee filing is common for a small partnership but "
            "means on-site labour and coverage should be confirmed directly.",
            sid,
        ))
        flags.append(flag(
            "gap",
            "No independent review corpus was retrievable for this licence in this pass.",
            sid,
        ))
    if number == "1013565":
        top_status = "hold"
        flags.append(flag(
            "hold",
            "Yelp shows a 1.0-star aggregate from exactly ONE review on an unclaimed listing, and "
            "the review text, date and author could not be retrieved in this environment. The only "
            "independent public signal for this licence is negative and unverifiable, so the record "
            "is held rather than presented as a lead until the review can be read directly.",
            sid, YELP_INNOVATION,
        ))
        flags.append(flag(
            "notice",
            "This is the strongest trade coverage verified in wave 9: one active licence holding "
            "both C-36 plumbing and B general building, and a completed 94122 permit whose printed "
            "scope combines new drain and water lines with replacing a section of drywall "
            "approximately 2x4 feet. That combination is exactly the plumbing-plus-finish pattern "
            "this research is looking for, and it is still not proof of exact-task experience.",
            sid, SRC_B_DRYWALL,
        ))
        flags.append(flag(
            "gap",
            "Cylex and Yelp were both checked for an independent review corpus; Cylex carries no "
            "attributable customer reviews and Yelp's single review text is unreachable.",
            CYLEX_INNOVATION, YELP_INNOVATION,
        ))
    if number == "1112261":
        claims.append(claim(
            "Relationship",
            "The CSLB-read business address (1847 48th Ave, San Francisco 94122) and phone "
            "(415) 203-7178 are IDENTICAL to the address and phone already stored in this dataset "
            "for registry-only record w6-c-t-construction-plumb, 'C T Construction & Plumb', whose "
            "registry licence number is 533324 on 234 plumbing-permit rows. Two different licence "
            "numbers are therefore recorded at one location under two different firm names, and "
            "registry licence 533324 has never been read on CSLB. Whether this is a re-licensing, a "
            "shared office or a registry error is unresolved and is published as unresolved.",
            sid,
            '{"cslb":"1112261 · CT PLUMBING & FIRE PROTECTION · 1847 48TH AVE · SAN FRANCISCO 94122 '
            '· (415) 203-7178","registry":"533324 · C T Construction & Plumb · 1847  48th Av · '
            'San Francisco · 94122 · 4152037178 · 234 permit rows"}',
        ))
        flags.append(flag(
            "discrepancy",
            "Same address and same phone as stored record w6-c-t-construction-plumb, but a "
            "different licence number: CSLB reads 1112261 (CT PLUMBING & FIRE PROTECTION, active "
            "C-36 + C-16, issued 2023) while the City registry row carries 533324 (C T Construction "
            "& Plumb, 234 permit rows, never read on CSLB). Confirm which licence is the "
            "contracting party before any contact. This is the one documented phone overlap in "
            "wave 9 and it is cross-referenced on both sides rather than deduplicated silently.",
            sid, SRC_FIRM94122,
        ))
        flags.append(flag(
            "notice",
            "This is the only wave-9 record where the regulator itself, not a directory, places the "
            "business inside ZIP 94122 (1847 48th Ave). CSLB also shows C-36 plus C-16 fire "
            "protection and workers' compensation exempt (no employees).",
            sid, SRC_P_FIRMADDR,
        ))
        flags.append(flag(
            "gap",
            "No completed 94122 permit was selected for this licence in the strict join, and no "
            "independent review corpus was retrievable in this pass. Local evidence is the "
            "regulator-read business address plus registry rows.",
            sid, SRC_P_FIRMADDR,
        ))
    if number == "1028917":
        flags.append(flag(
            "notice",
            "The City registry places this licence on PLUMBING permit contact rows, but CSLB shows "
            "B only and NO C-36. Any pipe work would require a properly licensed plumbing "
            "contractor, and this licence is expired in any case.",
            sid, SRC_FIRM94122,
        ))
        flags.append(flag(
            "discrepancy",
            "Four conflicts on one licence: registry name appears as both 'Euro Plumbing Inc, "
            "General Contractor' and 'E P I General Contractor'; CSLB address 94108 versus registry "
            "94122; registry phone 415-509-9527 versus CSLB (415) 509-9577; and bond cancelled "
            "07/30/2022.",
            sid, SRC_FIRM94122,
        ))
        flags.append(flag(
            "notice",
            "Wave 8 rejected this licence number because the regulator's business name did not "
            "match the discovery identity. Wave 9 opened the page and resolved the question "
            "directly: the licence expired 2021-07-31 and holds no C-36. It is therefore stored as "
            "a documented hold instead of being silently dropped.",
            sid,
        ))
    if number == "658767":
        flags.append(flag(
            "notice",
            "CSLB records 330 Ortega Street, San Francisco 94122 - inside the Outer Sunset - with "
            "C-35 lathing and plastering only and no plumbing classification. The licence expired "
            "2000-11-30, so this is historical local identity, not an available contractor.",
            sid, SRC_B_FIRM94122,
        ))
    if number == "373337":
        flags.append(flag(
            "notice",
            "CSLB shows Reissue Date 04/06/2006 and the misc note '04/06/2006 LICENSE REISSUED TO "
            "ANOTHER ENTITY'. The number therefore no longer identifies the original contractor, "
            "and every registry row carrying it is ambiguous about which entity performed the work.",
            sid, SRC_FIRM94122,
        ))
        flags.append(flag(
            "discrepancy",
            "The registry prints SIX different firm-name spellings against this one licence number, "
            "and CSLB's address is 94116 rather than the registry's 94122.",
            sid, SRC_FIRM94122,
        ))
    if number == "1017991":
        flags.append(flag(
            "notice",
            "CSLB carries an Additional Status line pointing to complaint disclosure information. "
            "The disclosure page was read directly: Complaint # N A 2025 2297, dated 06/23/2026, "
            "status LETTER OF ADMONISHMENT ISSUED. CSLB states that any complaint listed is only an "
            "allegation of a probable violation and does not affect the status of the licence at "
            "this time. It is recorded as an allegation, never as a finding.",
            sid, DISCLOSURE_1017991,
        ))
        flags.append(flag(
            "notice",
            "The completed 94122 permit scope includes 'repair plumbing in-kind in kitchen under "
            "sink. replace valve of hot/cold water & p-trap', but CSLB shows B only and no C-36. "
            "Identify the properly licensed plumbing contractor for any pipe work.",
            sid, SRC_B_DRYWALL,
        ))
        flags.append(flag(
            "gap",
            "No independent review corpus was retrievable for this licence in this pass; the "
            "disclosure record is the only adverse public signal found and it is an allegation.",
            DISCLOSURE_1017991,
        ))
    if number == "1120735":
        flags.append(flag(
            "notice",
            "CSLB shows B-2 RESIDENTIAL REMODELING alongside B GENERAL BUILDING. B-2 is a real, "
            "distinct CSLB classification; it was added to this dataset's allowed-classification "
            "list rather than silently mapped onto B, because a residential-remodelling licence "
            "does not carry the same scope as a general building licence.",
            sid,
        ))
        flags.append(flag(
            "notice",
            "The completed 94122 permit PP20260731567 reads 'replace tub in same location upgrade "
            "plumbing up to code as needed' - a bathtub replacement - yet the licence holds no "
            "C-36. A properly licensed plumbing contractor must be identified for any pipe work, "
            "and that is precisely the coordination this project would need.",
            sid, SRC_P_RECENT,
        ))
        flags.append(flag(
            "gap",
            "No independent review corpus was retrievable for this licence in this pass.",
            sid,
        ))
    if number == "342141":
        flags.append(flag(
            "discrepancy",
            "The City registry lists licence 342141 under the firm name 'L & L Plumbing Inc.' with "
            "a 94122 address, while the CSLB licensee for that number is LEE'S PLUMBING CO at 217 "
            "Willard North, San Francisco 94118. Name and address both conflict; the row is "
            "published as-read and left unresolved.",
            sid, SRC_FIRM94122,
        ))
        flags.append(flag(
            "notice",
            "CSLB states 'There was no workers comp information found for this license' and shows "
            "the bond cancelled 12/15/1985.",
            sid,
        ))
    if number == "341277":
        flags.append(flag(
            "notice",
            "One active licence has held B GENERAL BUILDING and C-36 PLUMBING since 08/08/1977, "
            "which is the multi-trade combination this project needs. That makes coordination "
            "worth investigating, not proven.",
            sid,
        ))
        flags.append(flag(
            "discrepancy",
            "Three ZIP variants for one business: CSLB 94110 (2180 Bryant St 212), the plumbing "
            "permit registry 94122, and the building permit contact row plus BuildZoom 94114 (763 "
            "Noe St). Confirm the current contracting address before contact.",
            sid, SRC_B_JOIN_2, BUILDZOOM_COIT,
        ))
        flags.append(flag(
            "gap",
            "BuildZoom states this profile 'hasn't received any reviews' while listing 43 permits. "
            "No independent customer review was retrievable for this licence in this pass.",
            BUILDZOOM_COIT,
        ))

    if r["trade"] == "plumbing":
        rationale = (
            f"{'Active' if active else 'Historical'} C-36 licence read directly on CSLB, plus a "
            "completed 94122 permit or a regulator-read 94122 address. Useful for a "
            "diagnostic-plumber comparison on a seized overflow, but no retained source proves the "
            "mechanism was freed without opening finishes."
        )
        next_step = (
            "Read the CSLB page again at the time of contact, then ask for a diagnostic-only, "
            "repair-first scope: examples involving stuck trip-lever and plunger assemblies in "
            "1940s galvanized systems, the least invasive method, a written stop point before any "
            "hidden-pipe replacement, who patches any ceiling opening they create, current Outer "
            "Sunset dispatch, and project-specific insurance."
            if active else
            "Do not book under this non-active licence. Keep only as historical permit and identity "
            "context, and locate a currently active C-36 entity."
        )
        gaps = [
            "Drywall or ceiling restoration and a finished reusable access hatch are not confirmed "
            "under this plumbing-only scope.",
            "No review or permit proves a small ceiling opening was converted into a finished "
            "access hatch by this business.",
        ]
    elif r["trade"] == "multi-trade":
        rationale = (
            f"{'Active' if active else 'Historical'} licence read directly on CSLB holding both "
            "plumbing and building classifications, with 94122 permit evidence. That is the "
            "single-source coordination pattern this project needs, and it is still not proof of "
            "exact-task experience or finish quality."
        )
        next_step = (
            "Ask who will diagnose the seized overflow, who performs the plumbing versus the finish "
            "work, whether a small code-compliant access hatch can be framed and finished to match "
            "the surrounding ceiling, the written repair-first stop point, permit responsibility, "
            "current Outer Sunset dispatch and project-specific insurance."
            if active else
            "Do not book under this non-active licence. Retain only as historical evidence of a "
            "combined plumbing-and-building scope."
        )
        gaps = [
            "No review proves a small ceiling opening was converted into a finished reusable access "
            "hatch.",
            "Current crew assignments, subcontractors and Outer Sunset availability are unknown.",
        ]
    elif r["trade"] == "plaster":
        rationale = (
            "Historical C-35 lathing and plastering licence read directly on CSLB, with the "
            "regulator itself recording an Outer Sunset business address at 330 Ortega Street. "
            "Relevant only as evidence that a finish trade operated inside 94122; the licence "
            "expired in 2000."
        )
        next_step = (
            "Do not contact under this licence. Retain as historical evidence for the finish-trade "
            "question, and identify a currently active C-9, C-35 or B entity for any ceiling patch "
            "or access hatch."
        )
        gaps = [
            "The licence expired 2000-11-30 and CSLB shows the bond cancelled in 1999, so no "
            "current contractor is identified by this record.",
            "No current entity, phone or address continuity was established for this business.",
        ]
    else:  # general
        rationale = (
            f"{'Active' if active else 'Historical'} B-classification licence read directly on "
            "CSLB, plus 94122 evidence. Supports a restoration or remodelling-estimate lead only; "
            "it does not establish plumbing self-performance or exact finish matching."
        )
        next_step = (
            "Ask for examples of small occupied-home ceiling openings, substrate and texture "
            "matching, dust containment, framing and finishing a reusable access hatch, which "
            "active C-36 plumber they coordinate with, permit responsibility, current Outer Sunset "
            "dispatch and project-specific insurance."
            if active else
            "Do not book under this non-active licence. Retain only as historical identity and "
            "permit context."
        )
        gaps = [
            "No source proves a small plumbing-access opening was finished as a reusable access "
            "hatch by this business.",
            "No active C-36 plumbing coordination is established by this record.",
        ]

    BUSINESS = {
        "id": f"w9-{slug(r['name'])}",
        "name": r["name"],
        "phone": r["phone"],
        "phoneSource": sid,
        "website": None,
        "websiteSource": None,
        "trade": r["trade"],
        "area": r["area"],
        "areaText": area_text,
        "status": top_status,
        "checkedAt": DATE,
        "claims": claims,
        "license": {
            "number": number,
            "entity": r["entity"],
            "classes": r["classes"],
            "status": r["status"],
            "expires": r["expires"],
            "checkedAt": DATE,
            "source": sid,
        },
        "reviewIds": [],
        "platformLinks": [],
        "flags": flags,
        "gaps": tail(gaps),
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
BY_LICENSE["1013565"]["platformLinks"] = [
    link("Yelp profile (1.0 stars, 1 review, unclaimed)",
         "https://www.yelp.com/biz/innovation-plumbing-and-rooter-san-francisco", YELP_INNOVATION),
    link("Cylex directory listing",
         "https://www.cylex.us.com/ca/san-francisco/innovation-plumbing-and-rooter.html",
         CYLEX_INNOVATION),
]
BY_LICENSE["1140843"]["platformLinks"] = [
    link("Yelp profile (4.5 stars, ~1,300 reviews)",
         "https://www.yelp.com/biz/discount-plumbing-rooter-services-san-francisco-2",
         YELP_DISCOUNT),
]
BY_LICENSE["786183"]["platformLinks"] = [
    link("HomeAdvisor/Angi rated page (3.8 of 5, 8 reviews)",
         "https://www.homeadvisor.com/rated.SmellyMelsPlumbingHtg.7558800.html", HOMEADVISOR_SMELLY),
    link("ServiceAgent directory restatement (unverified Google score)",
         "https://serviceagent.ai/plumber/california/south-san-francisco/smelly-mel-s-plumbing",
         SERVICEAGENT_SMELLY),
]
BY_LICENSE["341277"]["platformLinks"] = [
    link("BuildZoom profile (43 permits, no reviews)",
         "https://www.buildzoom.com/contractor/coit-construction", BUILDZOOM_COIT),
]
BY_LICENSE["1051988"]["platformLinks"] = [
    link("BuildZoom profile, name printed as 'Yu Pluming' (no reviews)",
         "https://www.buildzoom.com/contractor/yu-pluming-inc", BUILDZOOM_YU),
]
BY_LICENSE["1097098"]["platformLinks"] = [
    link("BuildZoom profile (no reviews; sewer-lateral permit history)",
         "https://www.buildzoom.com/contractor/h-j-plumbing-inc", BUILDZOOM_HJ),
]
BY_LICENSE["1112261"]["gaps"].insert(
    0,
    "The relationship between CSLB licence 1112261 and registry licence 533324 at the same 1847 "
    "48th Ave address and phone is unresolved, and 533324 has never been read on CSLB.",
)


# ------------------------------------------- tier 2: registry-only rows (33)
for r in REGISTRY:
    number = r["number"]
    kind = r["kind"]
    if kind == "addr":
        contact_source, detail_source = SRC_FIRM94122, r["permits_src"]
        excerpt = (
            f'{{"license_number":"{number}","firm":"{r["name"]}","addr":"{r["addr"]}",'
            f'"zip":"94122","phone":"{r["phone"].replace("-", "")}",'
            f'"permits":"{",".join(r["permits"])}"}}'
        )
        discovery = (
            f"The official SF DBI \u201cPlumbing Permits Contacts\u201d registry returns licence number "
            f"{number} against a firm address of {r['addr']} in ZIP 94122, with permit rows "
            f"{', '.join(r['permits'][:3])}{' and others' if len(r['permits']) > 3 else ''}."
        )
        area_text = (
            f"Registry-recorded plumbing-permit contact at {r['addr']}, ZIP 94122 (Outer Sunset), on "
            f"{len(r['permits'])} permit rows. The registry is the City's own open data, but licence "
            f"number {number} has NOT been read on CSLB, so no status, classification or legal "
            "entity is claimed and current dispatch is unconfirmed."
        )
        coverage = (
            f"The City's plumbing-permit contact registry records this firm's own business address "
            f"in ZIP 94122 on {len(r['permits'])} permit rows, including "
            f"{r['permits'][0]}. A recorded 94122 business address is local presence evidence, not "
            "a promise to take this job."
        )
        rationale = (
            f"The City's own plumbing-permit registry places this firm's business address inside ZIP "
            f"94122 and ties licence number {number} to {len(r['permits'])} plumbing-permit rows, "
            f"the most recent being {r['permits'][0]}. That is genuine local presence evidence from "
            "an official source and nothing more: no regulator page was read and no exact-task "
            "experience is shown."
        )
        next_step = (
            f"Read CSLB licence #{number} directly (status, classification, legal entity, expiry, "
            "bond, workers' compensation) before any contact. Then ask for repair-first diagnostic "
            "examples on stuck trip levers in 1940s galvanized systems, the least invasive method, "
            "a written stop point before hidden-pipe replacement, who patches any ceiling opening, "
            "current Outer Sunset dispatch and project-specific insurance."
        )
        gaps = [
            "Permit descriptions were not read for these registry rows, so the scope of work "
            "behind each permit number is unknown.",
            "Whether this firm performs its own plumbing or subcontracts it is not established.",
        ]
        phone_source = SRC_FIRM94122
    elif kind == "pjoin":
        pid, completed, paddr, scope = r["permit"]
        contact_source, detail_source = SRC_P_JOIN, SRC_P_RECENT
        excerpt = (
            f'{{"permit_number":"{pid}","license_number":"{number}",'
            f'"firm_name":"{r["name"]}","zipcode":"{r["firm_zip"]}"'
            + (f',"phone":"{r["phone"].replace("-", "")}"' if r["phone"] else "")
            + "}"
        )
        discovery = (
            f"The official plumbing-permit contact dataset associates licence number {number} "
            f"({r['name']}) with completed permit {pid} at {paddr}."
        )
        area_text = (
            f"A completed official plumbing permit places work at {paddr} on {completed}; the "
            f"registry records this firm's own address in ZIP {r['firm_zip'][:5]}. Licence number "
            f"{number} was NOT read on CSLB in this pass, so classification, status and current "
            "Outer Sunset dispatch are unconfirmed."
        )
        coverage = (
            f"Completed permit {pid} ({completed}) at {paddr} places verified plumbing work inside "
            f"ZIP 94122 while the recorded firm address is ZIP {r['firm_zip'][:5]}."
        )
        rationale = (
            f"A completed 94122 plumbing permit ({pid}, {completed}) names licence number {number} "
            f"as the permit contact, with the printed scope '{scope[:90]}'. Official, dated and "
            "local - but a contact row does not allocate every task on a permit, and no CSLB page "
            "was read for this licence."
        )
        next_step = (
            f"Read CSLB licence #{number} directly before any contact, then ask for repair-first "
            "diagnostic examples on seized trip levers in 1940s galvanized systems, the least "
            "invasive method, a written stop point before hidden-pipe replacement, who patches any "
            "ceiling opening they create, current Outer Sunset dispatch and project-specific "
            "insurance."
        )
        gaps = [
            "The permit-contact row does not establish who performed which task on the permit.",
            "No drywall, ceiling or finish capability is established by a plumbing-permit row.",
        ]
        phone_source = SRC_P_JOIN if r["phone"] else None
    else:  # bjoin
        pid, completed, paddr, scope = r["permit"]
        contact_source = SRC_B_JOIN_1 if pid in BJOIN_1 else SRC_B_JOIN_2
        detail_source = SRC_B_DRYWALL
        excerpt = (
            f'{{"permit_number":"{pid}","license1":"{number}","firm_name":"{r["name"]}",'
            f'"role":"contractor","firm_zipcode":"{r["firm_zip"]}"}}'
        )
        discovery = (
            f"The official building-permit contact dataset records licence number {number} "
            f"({r['name']}) as a contact on permit {pid}, whose printed scope names drywall, "
            f"sheetrock, ceiling or plaster work at {paddr}."
        )
        area_text = (
            f"A completed official building permit whose printed scope names drywall, sheetrock, "
            f"ceiling or plaster work places that work at {paddr} on {completed}; the recorded firm "
            f"address is ZIP {r['firm_zip'][:5]}. Licence number {number} was NOT read on CSLB in "
            "this pass, so classification, status and current Outer Sunset dispatch are "
            "unconfirmed."
        )
        coverage = (
            f"Completed permit {pid} ({completed}) at {paddr} places finish-side work inside ZIP "
            f"94122 while the recorded firm address is ZIP {r['firm_zip'][:5]}."
        )
        rationale = (
            f"A completed 94122 building permit ({pid}, {completed}) whose printed scope names "
            f"drywall, sheetrock, ceiling or plaster work records licence number {number} as a "
            "contact. That supports a restoration-estimate lead only; it establishes neither "
            "plumbing self-performance nor exact finish matching."
        )
        next_step = (
            f"Read CSLB licence #{number} directly before any contact, then ask for examples of "
            "small occupied-home ceiling openings, substrate and texture matching, dust "
            "containment, framing and finishing a reusable access hatch, which active C-36 plumber "
            "they coordinate with, permit responsibility, current Outer Sunset dispatch and "
            "project-specific insurance."
        )
        gaps = [
            "No plumbing capability is established by a building-permit contact row.",
            "The permit-contact row does not establish who performed which task on the permit.",
        ]
        phone_source = None

    claims = [
        claim("Discovery", discovery, contact_source, excerpt),
        claim(
            "Registry",
            "Registry-recorded evidence re-read in a second query so no field is published from a "
            "single transient reading. The City dataset is official; the licence number it returns "
            "is a lead.",
            detail_source if kind != "addr" else r["permits_src"],
            excerpt,
        ),
        claim("Coverage", coverage, contact_source, excerpt),
    ]
    if kind != "addr":
        pid, completed, paddr, scope = r["permit"]
        claims.append(claim(
            "Permit scope",
            f"Permit {pid} is recorded complete on {completed} at {paddr}. The printed scope is "
            "quoted verbatim and supports only the work words actually shown.",
            detail_source,
            f'{{"permit_number":"{pid}","status":"complete","completed_date":"{completed}",'
            f'"address":"{paddr}","description":"{scope}"}}',
        ))

    flags = [
        flag("gap", REGISTRY_GAP.format(number=number), contact_source, detail_source),
        flag("notice", REGISTRY_NOTICE, contact_source),
        flag("notice", REGISTRY_TRADE_NOTICE, contact_source),
    ]
    if r.get("note"):
        flags.append(flag("discrepancy", r["note"], contact_source))
    if not r["phone"]:
        flags.append(flag(
            "gap",
            "The registry row read for this record carries no phone number, so no contact channel "
            "is established by this research.",
            contact_source,
        ))
    if number == "1021221":
        claims.append(claim(
            "Review identity",
            "Yelp prints 3624 Ortega St, San Francisco 94122 and (415) 213-5545 for Kevel Home "
            "Performance, matching the City registry row for this licence on both address and "
            "phone. That double match is what makes the retained reviews safely attributable to "
            "this record.",
            YELP_KEVEL,
            '{"address":"3624 Ortega St","zip":"94122","phone":"(415) 213-5545","rating":"5.0","reviews":"32"}',
        ))
        claims.append(claim(
            "Angi record",
            "Angi shows a 5.0 of 5 aggregate from a single review (Ian H., June 2014) and prints "
            "that this business does not offer free estimates.",
            ANGI_KEVEL,
            '{"rating":"5.0","reviews":"1","reviewer":"Ian H.","date":"June 2014","free_estimates":"no"}',
        ))
        flags.append(flag(
            "notice",
            "Yelp categories for this business are HVAC, energy and insulation - NOT plumbing or "
            "drywall. The registry rows are plumbing and water-heater permits. Trade coverage for "
            "this project is therefore unverified in both directions and must be confirmed by a "
            "CSLB read before contact.",
            YELP_KEVEL, contact_source,
        ))
        flags.append(flag(
            "discrepancy",
            "Two Yelp snapshots of the same listing disagree on whether the business is claimed or "
            "unclaimed. Both readings are recorded; neither is treated as authoritative.",
            YELP_KEVEL,
        ))
        flags.append(flag(
            "notice",
            "Angi prints that this business does not offer free estimates, which matters for a "
            "diagnostic-first approach.",
            ANGI_KEVEL,
        ))
    if number == "1039289":
        flags.append(flag(
            "notice",
            "This registry row is unusually active: six permit numbers returned in the 94122 firm "
            "window, all from 2025-2026. Activity is not qualification - no CSLB page was read and "
            "no review corpus was retrievable.",
            r["permits_src"],
        ))
    if number == "1111133":
        flags.append(flag(
            "notice",
            "The retained permit scope is a bathroom remodel that replaces a toilet, vanity and "
            "shower 'using existing electrical & plumbing, in kind' - in-kind replacement, which is "
            "the closest published analogue in wave 9 to a like-for-like overflow or fixture repair.",
            detail_source,
        ))

    # The no-regulator-read gap is published in the plain gap list as well as in
    # the flag list, so it survives any UI that renders only one of them.
    gaps.insert(
        0,
        f"Registry licence number {number} was NOT read on CSLB in this pass, so its status, "
        "classification, legal entity, expiry, bond and workers' compensation are all unknown.",
    )

    business = {
        "id": f"w9-{slug(r['name'])}",
        "name": r["name"],
        "phone": r["phone"],
        "phoneSource": phone_source,
        "website": None,
        "websiteSource": None,
        "trade": "registry-lead",
        "area": "sunset",
        "areaText": area_text,
        "status": "research",
        "checkedAt": DATE,
        "claims": claims,
        "license": None,
        "reviewIds": [],
        "platformLinks": [],
        "flags": flags,
        "gaps": tail(gaps),
        "priority": None,
        "rationale": rationale,
        "nextStep": next_step,
        "exactMatch": False,
        "insuranceVerified": False,
        "scopeConfirmed": False,
        "master": False,
    }
    if number == "1021221":
        business["platformLinks"] = [
            link("Yelp profile (5.0 stars, 32 reviews; 3624 Ortega St 94122)",
                 "https://www.yelp.com/biz/kevel-home-performance-san-francisco", YELP_KEVEL),
            link("Angi rated page (5.0 of 5, 1 review)",
                 "https://www.angi.com/companylist/us/ca/san-francisco/kevel-home-performance-reviews.htm",
                 ANGI_KEVEL),
        ]
    BUSINESSES.append(business)

BY_ID = {b["id"]: b for b in BUSINESSES}

# ------------------------------------------------------------------ reviews
REVIEWS: list[dict] = []


def review(business_id: str, rid: str, platform: str, source: int, author: str,
           published: str | None, quote: str, theme: str, analysis: str, *,
           negative: bool = False, identity: str = "matched") -> None:
    REVIEWS.append({
        "id": rid,
        "business": business_id,
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
        "access": "search-extract",
        "identity": identity,
    })


SMELLY = "w9-smelly-mel-s-plumbing-inc"
KEVEL = "w9-kevel-home-performance"

review(
    SMELLY, "R122", "HomeAdvisor", HOMEADVISOR_SMELLY, "Gordon M.", None,
    "We hired Smelly Mel's to install new main sewer line and replace all drainage pipes. The "
    "customer service was first-rate and very responsive. The work performed was done with the "
    "highest degree of professionalism and done quickly. I'm extremely pleased with the quality "
    "of the work.",
    "Whole-system drainage replacement",
    "Dated October 2010 with a project cost band of about $5,000 and 5.0 of 5 stars. Replacing a "
    "main sewer line and all drainage pipes is heavy in-wall work on an older house, which is "
    "adjacent to this project's galvanized-pipe risk but is the opposite of a repair-first "
    "outcome. It says nothing about freeing a seized overflow trip lever or about finishing a "
    "ceiling opening.",
)
review(
    SMELLY, "R123", "HomeAdvisor", HOMEADVISOR_SMELLY, "Bill H.", None,
    "Travis was very knowledgeable and shared ideas based on his experience.",
    "Diagnostic knowledge",
    "Dated August 2010, 4.0 of 5 stars, cost band about $5,000. Short but relevant in one respect: "
    "it credits named diagnostic judgement rather than price. CSLB lists Travis Marshall Allen as "
    "a 10%+ owner of licence 786183, which supports - without proving - that the reviewer met a "
    "principal. No task detail is given.",
)
review(
    SMELLY, "R124", "HomeAdvisor", HOMEADVISOR_SMELLY, "Michael N.", None,
    "The work was done well. There were a few small issues, related to delays in cleanup. I would "
    "use Smelly Mel's use.",
    "Cleanup delays; star/text mismatch",
    "Displayed as 1.0 of 5 stars for an October 2009 job in the $10,000 band, while the retained "
    "text reads as satisfied apart from cleanup delays. The star value and the words disagree, so "
    "both are preserved exactly as published and neither is treated as established. The extract "
    "also ends mid-phrase ('I would use Smelly Mel's use'), which is recorded rather than "
    "silently repaired.",
    negative=True,
)
review(
    KEVEL, "R125", "Yelp", YELP_KEVEL, "David K.", None,
    "The pricing for the work was very reasonable and the work well-done, and our tenants loved "
    "working with Jeff and Brian.",
    "Work in a tenant-occupied rental",
    "One of the Yelp 'review highlight' excerpts for a 5.0-star listing with 32 reviews. The only "
    "detail that matters here is the setting: work performed while tenants were in place, with the "
    "tenants naming the crew. For a rental property this is closer to the real constraint than a "
    "quality score is - dust control, scheduling around occupants and leaving the unit usable. No "
    "plumbing or drywall task is named.",
)
review(
    KEVEL, "R126", "Yelp", YELP_KEVEL, "Chris Y.", None,
    "You are not going to find a better, more meticulous and professional team than Jeff and the "
    "gang at Kevel.",
    "Workmanship care",
    "A second Yelp highlight excerpt. 'Meticulous' is the word most relevant to finish matching "
    "after a small ceiling opening, but the excerpt names no task, no substrate and no texture "
    "match, so it cannot support a drywall or access-hatch claim on its own.",
)
review(
    KEVEL, "R127", "Yelp", YELP_KEVEL, "Abby D.", None,
    "We had a great experience working with Kevel on an energy audit and related upgrades this "
    "winter and spring.",
    "Energy audit and upgrades",
    "A third Yelp highlight excerpt, and it names the trade this business actually works in: "
    "energy audits and upgrades. That is consistent with the Yelp categories (HVAC, energy, "
    "insulation) and inconsistent with the plumbing-permit registry rows, which is exactly why the "
    "trade-coverage flag on this record stays open.",
)
review(
    KEVEL, "R128", "Angi", ANGI_KEVEL, "Ian H.", None,
    "Brian was great to work with from the start. Very insightful with several ideas on how to "
    "make our home more comfortable by adding a whole house fan, attic exhausts and insulation",
    "Whole-house fan, attic exhausts and insulation",
    "The single Angi review, dated June 2014, 5.0 of 5. It describes ceiling and attic work - a "
    "whole-house fan and attic exhausts require cutting ceiling openings - but it is twelve years "
    "old and names no plumbing, no drywall patching and no access hatch. Historical context only.",
)

for rv in REVIEWS:
    BY_ID[rv["business"]]["reviewIds"].append(rv["id"])

# ------------------------------------------------------------------ checks
def norm_name(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def core_name(value: str) -> str:
    suffixes = {"and", "co", "company", "corp", "corporation", "dba", "inc",
                "incorporated", "llc", "the"}
    return " ".join(t for t in norm_name(value).split() if t not in suffixes)


def norm_phone(value):
    digits = re.sub(r"\D", "", value or "")
    return digits[-10:] if len(digits) >= 10 else digits


assert len(BUSINESSES) == 50, len(BUSINESSES)
assert len(REGISTRY) == 33 and len(READS) == 17
assert len({b["id"] for b in BUSINESSES}) == 50
assert all(b["claims"][0]["field"] == "Discovery" for b in BUSINESSES)
assert all(len(b["gaps"]) >= 4 for b in BUSINESSES)
assert not any(b["master"] or b["exactMatch"] or b["insuranceVerified"] or b["scopeConfirmed"]
               for b in BUSINESSES)
assert all(b["priority"] is None for b in BUSINESSES)
assert len(REVIEWS) == 7
assert len({rv["id"] for rv in REVIEWS}) == 7
assert len({re.sub(r"[^a-z0-9]+", " ", rv["quote"].lower()).strip() for rv in REVIEWS}) == 7

# Collision pre-flight against the merged 401-record baseline, so a drift is
# reported here instead of failing the merge.
# CSLB licence 1112261 (CT Plumbing & Fire Protection) reads the same business
# address and the same phone as stored registry-only record
# w6-c-t-construction-plumb, which carries a DIFFERENT registry licence number
# (533324). Both readings are published and cross-referenced; the overlap is
# never resolved by assumption and never deduplicated silently.
DOCUMENTED_PHONE_OVERLAP = {"4152037178"}

data = json.loads((ROOT / "data" / "research.json").read_text())
prior_names = {norm_name(b["name"]) for b in data["businesses"]}
prior_cores = {core_name(b["name"]) for b in data["businesses"]}
prior_phones = {norm_phone(b.get("phone")) for b in data["businesses"] if norm_phone(b.get("phone"))}
prior_licenses = {str(b["license"]["number"]) for b in data["businesses"] if b.get("license")}
prior_ids = {b["id"] for b in data["businesses"]}
problems: list[str] = []
seen_cores: dict[str, str] = {}
seen_phones: dict[str, str] = {}
seen_licenses: dict[str, str] = {}
for b in BUSINESSES:
    if b["id"] in prior_ids:
        problems.append(f"id collision: {b['id']}")
    if norm_name(b["name"]) in prior_names:
        problems.append(f"name collision: {b['name']}")
    core = core_name(b["name"])
    if core in prior_cores:
        problems.append(f"core collision: {b['name']}")
    if core in seen_cores:
        problems.append(f"intra-wave core collision: {b['name']} vs {seen_cores[core]}")
    seen_cores[core] = b["name"]
    phone = norm_phone(b["phone"])
    if phone:
        if phone in prior_phones and phone not in DOCUMENTED_PHONE_OVERLAP:
            problems.append(f"phone collision: {b['name']} {phone}")
        if phone in DOCUMENTED_PHONE_OVERLAP:
            # The overlap is only acceptable when the record publishes it.
            assert any(
                f["level"] == "discrepancy" and "w6-c-t-construction-plumb" in f["text"]
                for f in b["flags"]
            ), f"documented overlap not flagged: {b['name']}"
            assert any(c["field"] == "Relationship" for c in b["claims"]), b["name"]
        if phone in seen_phones:
            problems.append(f"intra-wave phone collision: {b['name']} vs {seen_phones[phone]}")
        seen_phones[phone] = b["name"]
    if b["license"]:
        num = str(b["license"]["number"])
        if num in prior_licenses:
            problems.append(f"license collision: {num} ({b['name']})")
        if num in seen_licenses:
            problems.append(f"intra-wave license collision: {num}")
        seen_licenses[num] = b["name"]
if problems:
    print("COLLISION PRE-FLIGHT FAILED:")
    for p in problems:
        print("  -", p)
    raise SystemExit(1)

payload = {
    "wave": 9,
    "date": DATE,
    "composition": {
        "businesses": len(BUSINESSES),
        "cslbPagesRead": len(READS),
        "activeLicenses": sum(1 for b in BUSINESSES if b["license"] and b["license"]["status"] == "active"),
        "nonActiveLicenses": sum(1 for b in BUSINESSES if b["license"] and b["license"]["status"] != "active"),
        "registryOnlyRecords": sum(1 for b in BUSINESSES if not b["license"]),
        "multiTradeVerified": sum(
            1 for b in BUSINESSES
            if b["license"] and {"B", "C36"} <= set(b["license"]["classes"])
        ),
        "completedPermits94122": sum(
            1 for b in BUSINESSES
            if any(c["field"] == "Permit scope" for c in b["claims"])
        ),
        "holdsRaised": sum(1 for b in BUSINESSES if b["status"] == "hold"),
        "retainedReviewExcerpts": len(REVIEWS),
        "unattributedCategoryExcerpts": 3,
        "communityTaskThreadsRead": 5,
        "discrepancyFlags": sum(
            1 for b in BUSINESSES for f in b["flags"] if f["level"] == "discrepancy"
        ),
    },
    "sources": SOURCES,
    "businesses": BUSINESSES,
    "reviews": REVIEWS,
}

OUT.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n")
print(
    f"wrote {OUT.relative_to(ROOT)}: {len(BUSINESSES)} businesses "
    f"({payload['composition']['cslbPagesRead']} CSLB reads + "
    f"{payload['composition']['registryOnlyRecords']} registry-only), "
    f"{len(SOURCES)} sources, {len(REVIEWS)} review excerpts"
)
print(json.dumps(payload["composition"], indent=1))
