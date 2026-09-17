#!/usr/bin/env python3
"""Wave 18 generator.

Builds data/wave18.json from field-level transcriptions made through the page
reader on 2026-09-17. Every registry row below was displayed in BOTH the
discovery query and the targeted cross-check query of the same City dataset.
Every licence read below was transcribed from an opened CSLB LicenseDetail page.
Platform evidence was transcribed from the displayed category/search pages.
Nothing was inferred beyond the displayed text; unread fields are absent.
"""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKED = "2026-09-17"
BASELINE = hashlib.sha256((ROOT / "data" / "research.json").read_bytes()).hexdigest()

CITY_A = ("https://data.sf.gov/resource/3pee-9qhc.json?%24select=firm_name%2Clicense1%2C"
          "firm_address%2Cfirm_zipcode%2Ccount%28%2A%29&%24group=firm_name%2Clicense1%2C"
          "firm_address%2Cfirm_zipcode&%24where=firm_zipcode+like+%2794122%25%27+AND+"
          "license1+is+not+null&%24order=license1&%24limit=200&%24offset=200")
CITY_A_X = ("https://data.sf.gov/resource/3pee-9qhc.json?%24select=distinct+firm_name%2C"
            "license1&%24where=license1+in%28%27750209%27%2C%27830655%27%2C%27819519%27%2C"
            "%27711115%27%2C%27730800%27%2C%27721644%27%2C%27847215%27%2C%27845353%27%2C"
            "%27719222%27%2C%27791127%27%2C%27685718%27%2C%27749150%27%2C%27871463%27%2C"
            "%27681955%27%2C%27686057%27%2C%27761394%27%2C%27754649%27%2C%27778667%27%2C"
            "%27880429%27%2C%27786487%27%2C%27738744%27%2C%27850582%27%2C%27866221%27%2C"
            "%27850016%27%2C%27866340%27%2C%27797155%27%2C%27795882%27%2C%27718999%27%2C"
            "%27707090%27%2C%27879073%27%2C%27887672%27%2C%27901734%27%2C%27765291%27%29"
            "&%24order=license1%2Cfirm_name&%24limit=200")
CITY_B = ("https://data.sf.gov/resource/k6kv-9kix.json?%24select=firm_name%2Clicense_number"
          "%2Caddress%2Czipcode%2Cphone%2Ccount%28%2A%29&%24group=firm_name%2Clicense_number"
          "%2Caddress%2Czipcode%2Cphone&%24where=zipcode+like+%2794122%25%27&%24order="
          "license_number&%24limit=200&%24offset=100")
CITY_B_X = ("https://data.sf.gov/resource/k6kv-9kix.json?%24select=distinct+firm_name%2C"
            "license_number&%24where=license_number+in%28%27348588%27%2C%27376048%27%2C"
            "%27446707%27%2C%27307912%27%2C%27315962%27%2C%27368898%27%2C%27398232%27%2C"
            "%27462311%27%2C%27415007%27%2C%27369977%27%29&%24order=license_number%2Cfirm_name&%24limit=200")
CSLB = "https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum="

REQ = {
    "plumbing": "unconfirmed",
    "drywall": "unconfirmed",
    "ceilingRestoration": "unconfirmed",
    "accessHatch": "unconfirmed",
    "outerSunsetDispatch": "unconfirmed",
    "seizedOverflowOutcome": "unconfirmed",
    "projectInsurance": "unconfirmed",
    "writtenRepairFirstScope": "unconfirmed",
}

# name, registry number, address as displayed, zip as displayed, count as
# displayed, extra registry flags
REG_A = [
    ("Westside Plastering", "750209", "1870 25th Av", "94122", "1", []),
    ("A Atlantiac Plastering Inc", "830655", "1240 14th Av", "94122-0000", "4",
     ["City registry spells the name \"Atlantiac\"; the CSLB page prints \"A ATLANTIC PLASTERING INC\". The spelling difference is published, not reconciled."]),
    ("E-Construction And Plumbing Co", "819519", "1268 10th Av", "94122-0000", "1",
     ["The CSLB page for this number prints \"AAA CONSTRUCTION AND PLUMBING CO\" with a Santa Clara address. Whether the City row and the regulator record describe one business is unresolved and stays flagged."]),
    ("Ron Chan Painting", "711115", "1819 - 34th Av", "94122-0000", "1", []),
    ("Carpentech Co", "730800", "1820 Noriega St", "94122-0000", "7", []),
    ("All Trades Contracting", "721644", "1415 44th Av", "94122-0000", "8", []),
    ("Sunset Improvements", "847215", "1567 37th Av", "94122-0000", "15", []),
    ("Ciganovich Constr****Bond Suspend******", "845353", "1636 16th Av", "94122-0000", "7",
     ["The City row itself carries a bond-suspension note in the firm name field; the CSLB page shows the licence expired 2014 with the contractor's bond cancelled 2007. No allegation beyond the displayed text is characterised."]),
    ("Winner Remodel & Const", "719222", "1430 20th Av", "94122-0000", "3",
     ["The CSLB page for this number prints \"BAK REMODEL & CONSTRUCTION\" at the same 1430 20th Avenue address. The name difference is published, not reconciled."]),
    ("Owens Design Build Inc", "791127", "1236 Kirkham St", "94122-0000", "18", []),
    ("Visual Building & Remodeling Inc", "685718", "1494 22nd Av", "94122-0000", "2", []),
    ("Morris Home Inc", "749150", "3539 Judah St", "94122-0000", "24",
     ["The CSLB page prints a historical disciplinary bond (effective 2002, cancelled 2004). A displayed bond line is not an adjudication and no allegation is inferred."]),
    ("Huff Construction Company Inc", "871463", "1527 43rd Ave", "94122-0000", "119",
     ["A second City row at the same number shows 1539 Taraval St Ste 204 with count 1."]),
    ("Baseline Homes", "681955", "638 Parnassus Av", "94122-0000", "18", []),
    ("Guilfoyle Construction", "686057", "1231 31st Av", "94122-0000", "29", []),
    ("Kelly & Gallagher Bldg Co", "761394", "1287 42nd Av", "94122-1208", "13", []),
    ("James Garcia Construction", "754649", "1617 45th Av", "94122-0000", "33", []),
    ("Maguire Construction", "778667", "4027 Irving Street", "94122-0000", "28", []),
    ("P J Hegarty Construction", "880429", "1834 26th Av", "94122-0000", "34", []),
    ("Brody Construction", "786487", "1606 46th Av", "94122-0000", "20", []),
    ("Carson Construction", "738744", "1823 48th Av", "94122-3921", "27", []),
    ("Aotearoa Construction", "850582", "1478 47th Av", "94122-0000", "29", []),
    ("Stellar Construction", "866221", "1557 11th Av", "94122-0000", "17", []),
    ("P J M Construction", "850016", "1630 46th Av", "94122-0000", "13", []),
    ("Patrick Keightley Construction", "866340", "1355 28th Av", "94122-0000", "19", []),
    ("Sean O'neill Construction", "797155", "1251 07th Av", "94122-0000", "12", []),
    ("Mcelroy Construction", "795882", "1384 29th Av", "94122-0000", "9", []),
    ("J & H Construction Co.", "718999", "2933 Moraga Av", "94122-0000", "11", []),
    ("Sun Shing Construction Co", "707090", "1635 23rd Ave", "94122-3310", "27", []),
    ("C & K Builders Inc", "879073", "1870 32nd Av", "94122-0000", "13", []),
    ("Hong's Custom Builders", "887672", "1859 42nd Av", "94122-0000", "6", []),
    ("Quest Builders Inc.", "901734", "1370 27th Av", "94122-0000", "3", []),
    ("Shamrock Builders Inc", "765291", "3201 Moraga St", "94122-0000", "1", []),
]

# name, registry number, address, zip, phone as displayed on the retained row,
# count, extra flags
REG_B = [
    ("Phil's Refrigeration", "348588", "1606 Noriega Street", "94122", "415-731-9143", "1",
     ["Appears in the plumbing-permit contact dataset although the name is refrigeration-named; trade is not inferred from the dataset membership."]),
    ("Russell Tile Company", "376048", "1601 21st Avenue", "94122-0000", "4156617803", "1",
     ["Registry rows at this number show counts of 1 and 2 for the same address/phone."]),
    ("Metrom Construction", "446707", "536 Judah Street", "94122", "415-661-7468", "1", []),
    ("Johnson Construction Co", "307912", "1746 26th Avenue", "94122", "415-253-6632", "2",
     ["A second City row at the same number reads \"Johnson Control/Nis, Inc.\" at the same address; counted once, alias published."]),
    ("Duncan  Construction", "315962", "1600 Noriega", "94122", "415-242-7010", "1",
     ["Registry rows at this number show two phone variants (415-242-7010, 415-479-6269); the displayed phone of the retained row is stored, the variant is noted."]),
    ("Wing On Construction Co", "368898", "1339 - 20th Avenue", "94122", "415-731-2551", "2", []),
    ("Fogarty Construction", "398232", "1659 41st Avenue", "94122", "415-664-7900", "1",
     ["Registry rows at this number show four phone variants; only the retained row's displayed phone is stored."]),
    ("Lau's Construction Co", "415007", "2121 Moraga Street", "94122", "415-731-7588", "1", []),
    ("Lotti Construction", "462311", "1463 28th Ave", "94122", "415-681-6334", "2", []),
    ("United Pacific Construction Company", "369977", "1582 27th Av", "94122-0000", "415-661-8390", "1",
     ["Registry rows at this number show two phone variants (415-661-8390, 415-731-3080); only the retained row's displayed phone is stored."]),
]

# licence reads: number -> dict of displayed fields
LIC = {
    "750209": {
        "legalName": "WESTSIDE PLASTERING", "status": "suspended", "classes": ["C35"],
        "entity": "Sole Ownership", "issued": "1998-06-03", "expires": "2028-06-30",
        "address": "5 SOUTH KNOLL ROAD APT 9, MILL VALLEY, CA 94941",
        "phone": "(415) 378-5614", "sourceAsOf": "9/16/2026 6:00:24 PM (as displayed; timezone not supplied)",
        "statusExcerpt": "License is under suspension for the following reasons: License is under Contractors Bond Suspension.",
        "bond": "Contractor's Bond filed with HUDSON INSURANCE COMPANY, bond 30122776, $25,000, effective 06/18/2023, cancellation 09/01/2026.",
        "workersComp": "Workers compensation with PIE INSURANCE COMPANY (THE), policy 3969221, effective 04/17/2026, expire 04/17/2027; classification code 5485 - Plastering/Stucco Work-high wage.",
        "extra": [],
        "flags": [
            "CSLB prints a Contractors Bond Suspension; the displayed bond cancellation date is 09/01/2026. The licence cannot currently contract.",
            "C35 (LATHING AND PLASTERING) is the closest displayed classification to the drywall/plastering side of this project, but the suspension means the licence is not currently usable and no capability for this specific repair is established.",
            "CSLB prints a Mill Valley address while the City registry row shows 1870 25th Av, 94122; the address difference is published, not reconciled.",
        ],
    },
    "830655": {
        "legalName": "A ATLANTIC PLASTERING INC", "status": "inactive", "classes": ["C35"],
        "entity": "Corporation", "issued": "2004-01-07", "expires": "2028-01-31",
        "address": "172 JUANITA WAY, SAN FRANCISCO, CA 94127",
        "phone": "(415) 260-3425", "sourceAsOf": "9/16/2026 6:00:25 PM (as displayed; timezone not supplied)",
        "statusExcerpt": "This license is inactive and not able to contract at this time.",
        "bond": "Contractor's Bond filed with SURETEC INSURANCE COMPANY, bond 145581, $25,000, effective 01/01/2023, cancellation 04/25/2024.",
        "workersComp": "Workers compensation with STATE COMPENSATION INSURANCE FUND, policy 9018239, effective 07/13/2012, cancellation 02/07/2024.",
        "extra": [
            "Additional status: the licence will need to meet workers compensation requirements and a contractor's bond to renew active or reactivate.",
            "Qualifying individual PADRAIG JOSEPH DOWD certified 10 percent or more ownership (Bond of Qualifying Individual not required), effective 01/07/2004.",
        ],
        "flags": [
            "Inactive and not able to contract; reactivation would need bond and workers-compensation requirements per the displayed page.",
            "C35 (LATHING AND PLASTERING) is relevant to the drywall/plastering side, but an inactive licence supports no current hiring decision.",
            "CSLB prints 94127 while the City registry row shows 1240 14th Av, 94122; the address difference is published, not reconciled.",
        ],
    },
    "819519": {
        "legalName": "AAA CONSTRUCTION AND PLUMBING CO", "status": "suspended", "classes": ["B", "C36"],
        "entity": "Partnership", "issued": "2003-05-06", "expires": "2027-01-31",
        "address": "59 WASHINGTON STREET #177, SANTA CLARA, CA 95050",
        "phone": "(650) 630-0406", "sourceAsOf": "9/16/2026 6:00:25 PM (as displayed; timezone not supplied)",
        "statusExcerpt": "License is under suspension for the following reasons: License is under Contractors Bond Suspension.",
        "bond": "Contractor's Bond filed with BUSINESS ALLIANCE INSURANCE COMPANY, bond G150616819757, $25,000, effective 06/11/2025, cancellation 06/14/2026.",
        "workersComp": "Exempt from workers compensation; certified no employees at this time, effective 06/11/2025.",
        "extra": [],
        "flags": [
            "The City row names \"E-Construction And Plumbing Co\" at 1268 10th Av while CSLB prints \"AAA CONSTRUCTION AND PLUMBING CO\" in Santa Clara; the identity question is left flagged rather than resolved by assumption.",
            "B + C36 (PLUMBING) would be the strongest displayed trade match for the plumbing side, but the licence is under Contractors Bond Suspension and cannot currently contract.",
        ],
    },
    "711115": {
        "legalName": "YONG RONG CHEN", "status": "active", "classes": ["C33"],
        "entity": "Sole Ownership", "issued": "1995-08-14", "expires": "2027-08-31",
        "address": "1819 34TH AVENUE, SAN FRANCISCO, CA 94122",
        "phone": "(415) 753-1188", "sourceAsOf": "9/16/2026 6:00:25 PM (as displayed; timezone not supplied)",
        "statusExcerpt": "This license is current and active.",
        "bond": "Contractor's Bond filed with WESTERN SURETY COMPANY, bond 67411931, $25,000, effective 07/20/2025.",
        "workersComp": "Exempt from workers compensation; certified no employees at this time, effective 07/11/2025.",
        "extra": [],
        "flags": [
            "CSLB lists the licensee as sole owner YONG RONG CHEN while the City row names \"Ron Chan Painting\" at the same 34th Avenue address; treated as one displayed identity with the name difference published.",
            "C33 (PAINTING AND DECORATING) is adjacent to drywall finishing but is not a drywall or plumbing classification; neither required trade is established.",
            "The CSLB address (1819 34th Avenue, 94122) matches the City registry address.",
        ],
    },
    "730800": {
        "legalName": "YU OUYANG", "status": "active", "classes": ["B"],
        "entity": "Sole Ownership", "issued": "1996-12-24", "expires": "2027-08-31",
        "address": "526 FORESTER LANE S, MADERA, CA 93636",
        "phone": "(213) 800-2131", "sourceAsOf": "9/16/2026 6:00:41 PM (as displayed; timezone not supplied)",
        "statusExcerpt": "This license is current and active.",
        "bond": "Contractor's Bond filed with ATLANTIC SPECIALTY INSURANCE COMPANY, bond 800246004, $25,000, effective 02/07/2026.",
        "workersComp": "Exempt from workers compensation; certified no employees at this time, effective 08/07/2025.",
        "extra": [],
        "flags": [
            "CSLB prints a Madera address while the City row shows 1820 Noriega St, 94122; current Outer Sunset presence is not established by this read.",
            "B (GENERAL BUILDING) alone does not demonstrate the plumbing or drywall capability this project requires.",
        ],
    },
    "721644": {
        "legalName": "ALLTRADES", "status": "expired", "classes": ["B"],
        "entity": "Sole Ownership", "issued": "1996-04-18", "expires": "2013-07-31",
        "address": "P O BOX 99539, SAN DIEGO, CA 92169",
        "phone": "(618) 303-6001", "sourceAsOf": "9/16/2026 6:00:41 PM (as displayed; timezone not supplied)",
        "statusExcerpt": "This license is expired and not able to contract at this time.",
        "bond": "Contractor's Bond filed with SURETEC INSURANCE COMPANY, bond 101809, $12,500, effective 04/18/2011, cancellation 05/18/2013.",
        "workersComp": "Exempt from workers compensation; certified no employees at this time, effective 07/13/2011.",
        "extra": [],
        "flags": [
            "Expired since 2013-07-31 and not able to contract; CSLB prints the name ALLTRADES with a San Diego address.",
            "The City permit-contact rows for 1415 44th Av are historical; no current capability is established.",
        ],
    },
    "847215": {
        "legalName": "SUNSET IMPROVEMENTS", "status": "expired", "classes": ["B"],
        "entity": "Sole Ownership", "issued": "2004-09-20", "expires": "2018-09-30",
        "address": "1567-37TH AVENUE, SAN FRANCISCO, CA 94122",
        "phone": "(415) 564-0784", "sourceAsOf": "9/16/2026 6:00:42 PM (as displayed; timezone not supplied)",
        "statusExcerpt": "This license is expired and not able to contract at this time.",
        "bond": "Contractor's Bond filed with SURETEC INDEMNITY COMPANY, bond 225921, $15,000, effective 01/01/2016, cancellation 06/16/2018.",
        "workersComp": "Exempt from workers compensation; certified no employees at this time, effective 08/04/2016.",
        "extra": [],
        "flags": [
            "Expired since 2018-09-30 and not able to contract; the CSLB address matches the City row at 1567 37th Avenue.",
            "B classification and an expired licence establish neither required trade nor current availability.",
        ],
    },
    "845353": {
        "legalName": "CIGANOVICH CONSTRUCTION", "status": "expired", "classes": ["B"],
        "entity": "Sole Ownership", "issued": "2004-08-25", "expires": "2014-08-31",
        "address": "1636 16TH AVENUE, SAN FRANCISCO, CA 94122",
        "phone": "(415) 317-5336", "sourceAsOf": "9/16/2026 6:00:43 PM (as displayed; timezone not supplied)",
        "statusExcerpt": "This license is expired and not able to contract at this time.",
        "bond": "Contractor's Bond filed with SURETY COMPANY OF THE PACIFIC, bond 6336678, $12,500, effective 01/01/2007, cancellation 09/30/2007.",
        "workersComp": "Exempt from workers compensation; certified no employees at this time, effective 08/11/2004.",
        "extra": [],
        "flags": [
            "Expired since 2014-08-31; the City row's own \"Bond Suspend\" annotation is consistent with the displayed 2007 bond cancellation, but no further allegation is characterised.",
            "The CSLB address matches the City row at 1636 16th Avenue.",
        ],
    },
    "719222": {
        "legalName": "BAK REMODEL & CONSTRUCTION", "status": "inactive", "classes": ["B"],
        "entity": "Sole Ownership", "issued": "1996-02-23", "expires": "2030-02-28",
        "address": "1430 20TH AVENUE, SAN FRANCISCO, CA 94122",
        "phone": "(415) 601-3018", "sourceAsOf": "9/16/2026 6:00:54 PM (as displayed; timezone not supplied)",
        "statusExcerpt": "This license is inactive and not able to contract at this time.",
        "bond": "Contractor's Bond filed with AMERICAN CONTRACTORS INDEMNITY COMPANY, bond SC404316, $12,500, effective 03/02/2009, cancellation 04/02/2014.",
        "workersComp": "Exempt from workers compensation effective 02/06/1996, cancellation 03/01/2014.",
        "extra": ["Miscellaneous: 10/16/2023 - WC EXEMPT CANCELLED-LIC INACTIVATED."],
        "flags": [
            "Inactive and not able to contract; reactivation needs a contractor's bond and workers-compensation compliance per the displayed page.",
            "CSLB prints \"BAK REMODEL & CONSTRUCTION\" at the same 1430 20th Avenue address as the City row named \"Winner Remodel & Const\"; the name difference is published, not reconciled.",
        ],
    },
    "791127": {
        "legalName": "OWENS DESIGN BUILD INC", "status": "expired", "classes": ["B"],
        "entity": "Corporation", "issued": "2001-02-08", "expires": "2025-06-30",
        "address": "1236 KIRKHAM ST, SAN FRANCISCO, CA 94122",
        "phone": "(415) 260-1036", "sourceAsOf": "9/16/2026 6:00:55 PM (as displayed; timezone not supplied)",
        "statusExcerpt": "This license is expired and not able to contract at this time.",
        "bond": "Contractor's Bond filed with NORTH RIVER INSURANCE COMPANY (THE), bond 04CF614202, $25,000, effective 01/01/2023.",
        "workersComp": "Exempt from workers compensation; certified no employees at this time, effective 08/21/2023.",
        "extra": [
            "Reissue date 12/08/2010; qualifying individual DANIEL EDWARD OWENS certified 10 percent or more ownership, effective 12/08/2010.",
            "Additional status: the corporation's Secretary of State status must be returned to active before renewal or reactivation.",
            "Other: personnel listed on this license (current or disassociated) are listed on other licenses.",
        ],
        "flags": [
            "Expired 2025-06-30 and not able to contract; the CSLB address matches the City row at 1236 Kirkham St.",
            "Reactivation additionally requires the corporation's Secretary of State status to be active per the displayed page.",
        ],
    },
    "685718": {
        "legalName": "VISUAL BUILDING AND REMODELING INC", "status": "expired", "classes": ["B"],
        "entity": "Corporation", "issued": "1994-03-19", "expires": "2006-09-30",
        "address": "1494 22ND AVENUE, SAN FRANCISCO, CA 94122",
        "phone": "(415) 793-8101", "sourceAsOf": "9/16/2026 6:00:56 PM (as displayed; timezone not supplied)",
        "statusExcerpt": "This license is expired and not able to contract at this time.",
        "bond": "Contractor's Bond filed with SURETY COMPANY OF THE PACIFIC, bond 6329789, $12,500, effective 01/01/2007, cancellation 08/01/2008.",
        "workersComp": "Exempt from workers compensation; certified no employees at this time, effective 12/13/1999.",
        "extra": [
            "Reissue date 09/08/1998; qualifying individual HUNG TRUNG QUACH certified 10 percent or more ownership, effective 09/08/1998.",
            "Miscellaneous: 09/08/1998 - LICENSE REISSUED TO ANOTHER ENTITY.",
        ],
        "flags": [
            "Expired since 2006-09-30 and not able to contract; the CSLB address matches the City row at 1494 22nd Avenue.",
            "A displayed reissue note (1998, to another entity) is transcribed without interpretation.",
        ],
    },
    "749150": {
        "legalName": "MORRIS HOME INC", "status": "expired", "classes": ["B"],
        "entity": "Corporation", "issued": "1998-05-08", "expires": "2004-05-31",
        "address": "1030 VICENTE STREET, SAN FRANCISCO, CA 94116",
        "phone": "(415) 566-2210", "sourceAsOf": "9/16/2026 6:00:56 PM (as displayed; timezone not supplied)",
        "statusExcerpt": "This license is expired and not able to contract at this time.",
        "bond": "Contractor's Bond filed with GULF INSURANCE COMPANY, bond B36006519, $10,000, effective 01/01/2004, cancellation 03/06/2004.",
        "workersComp": "Exempt from workers compensation; certified no employees at this time, effective 04/10/1998.",
        "extra": [
            "Disciplinary Bond filed with GULF INSURANCE COMPANY, bond B34221724, $15,000, effective 03/27/2002, cancellation 03/27/2004.",
            "Qualifying individual MORRIS JIN KIM certified 10 percent or more ownership, effective 11/24/2003.",
        ],
        "flags": [
            "Expired since 2004-05-31 and not able to contract; CSLB prints 94116 while the City row shows 3539 Judah St, 94122.",
            "A historical disciplinary bond line is transcribed as displayed; it is not an adjudication and no allegation is characterised.",
        ],
    },
}

# Platform / community records ---------------------------------------------
THUMB_PLUMBERS = "https://www.thumbtack.com/ca/san-francisco/plumbers/"
THUMB_DRYWALL = "https://www.thumbtack.com/ca/san-francisco/drywall-contractors"
THUMB_PLASTER = "https://www.thumbtack.com/ca/san-francisco/plastering"
THUMB_CEILING = "https://www.thumbtack.com/ca/san-francisco/ceiling-repair-companies"
REPIPE_PROFILE = "https://www.thumbtack.com/ca/daly-city/repiping-specialists/repipe-specialists-san-francisco-bay-area/service/479245870668922887"
YELP_DW_OS = "https://www.yelp.com/search?find_desc=Dry+Wall+Repair&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA"
YELP_DW_INSTALL_OS = "https://www.yelp.com/search?find_desc=Drywall+Installation&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA"
YELP_DW_SF = "https://www.yelp.com/search?find_desc=drywall+repair+service&find_loc=San+Francisco%2C+CA"
YELP_NEARME = "https://www.yelp.com/nearme/drywall-repair"
REDDIT_SSF = "https://www.reddit.com/r/SouthSanFrancisco/comments/1df11w7/plumber_recommendations_for_ssf/"
REDDIT_ASKSF = "https://www.reddit.com/r/AskSF/comments/jcy9dl/can_you_recommend_a_plumber/"

PLATFORM = [
    {
        "id": "w18-drain-geeks", "name": "Drain Geeks", "source": "thumbtack-plumbers",
        "platformEvidence": {
            "platform": "Thumbtack",
            "categoryUrl": THUMB_PLUMBERS,
            "profileUrl": "https://www.thumbtack.com/ca/san-francisco/drain-cleaning/drain-geeks/service/578628100619091977",
            "rating": "4.9", "reviewCount": 9, "hires": 8,
            "services": "Plumbing Drain Repair, Plumbing Pipe Repair, Water Heater Installation or Replacement, Sink or Faucet Installation or Replacement",
            "serves": "Serves San Francisco, CA (as displayed)",
            "badges": "No Top Pro or Licensed pro badge was displayed on the read category card; absence of a badge is recorded, not interpreted.",
        },
        "reviews": ["w18-r01"],
        "flags": [
            "Platform listing only: no CSLB read, no licence fact. Thumbtack's own page says platform presence is not licence verification.",
            "Outer Sunset dispatch is not established; the card displays \"Serves San Francisco, CA\" without a neighbourhood.",
            "No license badge observed on the read card, unlike several neighbouring cards; this is recorded as displayed, not as a negative finding.",
        ],
    },
    {
        "id": "w18-handy-teddy", "name": "Handy Teddy", "source": "thumbtack-plumbers",
        "platformEvidence": {
            "platform": "Thumbtack",
            "categoryUrl": THUMB_PLUMBERS,
            "profileUrl": "https://www.thumbtack.com/ca/sausalito/drain-cleaning/handy-teddy/service/507518044058312709",
            "rating": None, "reviewCount": None, "hires": None,
            "services": "Listed in the San Francisco plumbers category reviews section (drain-cleaning profile path).",
            "serves": "Profile path shows Sausalito; San Francisco service is not confirmed by the read page.",
            "badges": "No rating, badge or hire count was displayed in the read review-section card.",
        },
        "reviews": ["w18-r02"],
        "flags": [
            "Only one short attributed quote was displayed in the read section; rating and hire count were not displayed there.",
            "Profile path is Sausalito-based; Outer Sunset dispatch is unconfirmed.",
            "Platform listing only: no CSLB read, no licence fact.",
        ],
    },
    {
        "id": "w18-jc-plumbing", "name": "JC PLUMBING", "source": "thumbtack-plumbers",
        "platformEvidence": {
            "platform": "Thumbtack",
            "categoryUrl": THUMB_PLUMBERS,
            "profileUrl": None,
            "rating": None, "reviewCount": None, "hires": None,
            "services": "Plumbing (category reviews section).",
            "serves": "San Francisco category page (as displayed)",
            "badges": "No badge or rating was displayed in the read review-section card.",
        },
        "reviews": ["w18-r04"],
        "flags": [
            "The displayed quote is truncated at a page-chunk boundary after \"patient and thorough\"; the remainder was not read and is not reconstructed.",
            "No profile page was opened; only the category reviews-section card was read.",
            "Platform listing only: no CSLB read, no licence fact.",
        ],
    },
    {
        "id": "w18-robert-insulation-drywall", "name": "Robert Insulation & Drywall",
        "source": "yelp-drywall-sf",
        "platformEvidence": {
            "platform": "Yelp",
            "categoryUrl": YELP_DW_SF,
            "profileUrl": None,
            "rating": "4.5", "reviewCount": 15, "hires": None,
            "services": "Drywall repair (Yelp \"Drywall repair\" service tag displayed); \"Verified License\" label displayed.",
            "serves": "San Francisco search results (search-extract)",
            "badges": "Verified License label displayed in the search extract; the licence itself was not read at CSLB.",
        },
        "reviews": ["w18-r05"],
        "flags": [
            "Yelp evidence is a search-extract only; the business page was not opened (Yelp blocks automated reads). Rating and quote come from the extract text as displayed.",
            "\"Verified License\" is a platform label, not a CSLB read; no licence number was displayed.",
            "Outer Sunset dispatch is not established by the search extract.",
        ],
    },
    {
        "id": "w18-bendana-drywall", "name": "Bendana Drywall", "source": "yelp-drywall-sf",
        "platformEvidence": {
            "platform": "Yelp",
            "categoryUrl": YELP_DW_SF,
            "profileUrl": None,
            "rating": "5.0", "reviewCount": 1, "hires": None,
            "services": "Drywall repair (service tag displayed); \"Verified License\", \"Certified professionals\", \"Established in 2004\" labels displayed.",
            "serves": "San Francisco search results (search-extract)",
            "badges": "Verified License label displayed in the search extract; the licence itself was not read at CSLB.",
        },
        "reviews": ["w18-r06"],
        "flags": [
            "Single-review 5.0 rating: thin evidence base; treat as discovery-level only.",
            "Yelp evidence is a search-extract only; the quote is truncated in the extract and was not completed by assumption.",
            "Outer Sunset dispatch is not established by the search extract.",
        ],
    },
    {
        "id": "w18-ma-drywall-restoration", "name": "M A Drywall & Restoration",
        "source": "yelp-drywall-sf",
        "platformEvidence": {
            "platform": "Yelp",
            "categoryUrl": YELP_DW_SF,
            "profileUrl": None,
            "rating": "5.0", "reviewCount": 1, "hires": None,
            "services": "Drywall repair (service tag displayed); \"8 years in business\" and \"Offers commercial services\" labels displayed.",
            "serves": "San Francisco search results (search-extract)",
            "badges": "No Verified License label was displayed on this card.",
        },
        "reviews": ["w18-d01"],
        "flags": [
            "The retained text is the business's own description from the search extract, not a customer review; no customer review excerpt was read for this card.",
            "Single-review 5.0 rating: thin evidence base; treat as discovery-level only.",
            "Yelp evidence is a search-extract only; the business page was not opened.",
        ],
    },
    {
        "id": "w18-handyman-can", "name": "The Handyman Can", "source": "yelp-nearme",
        "platformEvidence": {
            "platform": "Yelp",
            "categoryUrl": YELP_NEARME,
            "profileUrl": None,
            "rating": None, "reviewCount": 80, "hires": None,
            "services": "Handyman, Furniture Assembly, Drywall Installation & Repair (category tags displayed).",
            "serves": "San Francisco and the Surrounding Area (as displayed in extract)",
            "badges": "No licence label was displayed on this card.",
        },
        "reviews": [],
        "flags": [
            "No review excerpt was displayed for this card in the read extract; the record holds category tags only.",
            "Handyman category with drywall tag: plumbing capability is not displayed, and this project needs both trades confirmed.",
            "Yelp evidence is a search-extract only; the business page was not opened.",
        ],
    },
]

REVIEWS = [
    {
        "id": "w18-r01", "entry": "w18-drain-geeks", "platform": "Thumbtack",
        "attribution": "Meredith N. (as displayed on the category card)",
        "source": "thumbtack-plumbers", "access": "page", "checkedAt": CHECKED,
        "kind": "review",
        "excerpt": ("We needed to replace our failing water heater and Patrick was incredibly quick to respond! "
                    "He was able to order a replacement take, coordinate delivery and installation all in one day. "
                    "We were so pleased with his quick turnaround, excellent service and professionalism. He expertly "
                    "handled the installation--calling in colleagues to help him lift the very large tank into position--"
                    "and was very thorough in cleaning the work site and leaving things completely tidy after the job was "
                    "completed. He is very courteous and personable and we felt very fortunate to have found him to help "
                    "with our plumbing issues on short notice. He will be our first call the next time we have any plumbing "
                    "issues in need of professional assistance!"),
        "note": "Water-heater replacement account. Not a seized-overflow account; exact-task gate remains unconfirmed.",
    },
    {
        "id": "w18-r02", "entry": "w18-handy-teddy", "platform": "Thumbtack",
        "attribution": "Michael L. (as displayed on the category card)",
        "source": "thumbtack-plumbers", "access": "page", "checkedAt": CHECKED,
        "kind": "review",
        "excerpt": "Very honest plumber. Thank you Teddy.",
        "note": "Short character endorsement; no task detail, no location detail.",
    },
    {
        "id": "w18-r04", "entry": "w18-jc-plumbing", "platform": "Thumbtack",
        "attribution": "Duncan C. (as displayed on the category card)",
        "source": "thumbtack-plumbers", "access": "page", "checkedAt": CHECKED,
        "kind": "review",
        "truncatedEnd": True,
        "excerpt": "Plumber was patient and thorough",
        "note": "Quote ends at the read page boundary; the remainder was not read and is not reconstructed.",
    },
    {
        "id": "w18-r05", "entry": "w18-robert-insulation-drywall", "platform": "Yelp",
        "attribution": "Reviewer initials/name not fully displayed in the search extract",
        "source": "yelp-drywall-sf", "access": "search-extract", "checkedAt": CHECKED,
        "kind": "review",
        "truncatedEnd": True,
        "excerpt": ("Superb work!! Robert and his crew (Milton) resurfaced some textured walls and new Sheetrock to "
                    "level 5 surface throughout my small condo"),
        "note": "Yelp search-extract; the extract itself cuts the quote. Drywall/ceiling-adjacent work described.",
    },
    {
        "id": "w18-r06", "entry": "w18-bendana-drywall", "platform": "Yelp",
        "attribution": "Reviewer name not displayed in the search extract",
        "source": "yelp-drywall-sf", "access": "search-extract", "checkedAt": CHECKED,
        "kind": "review",
        "truncatedEnd": True,
        "excerpt": "These guys rock - I had a great experience with Fabio's team",
        "note": "Yelp search-extract; the extract cuts the quote.",
    },
    {
        "id": "w18-d01", "entry": "w18-ma-drywall-restoration", "platform": "Yelp",
        "attribution": "Business's own description (not a customer review)",
        "source": "yelp-drywall-sf", "access": "search-extract", "checkedAt": CHECKED,
        "kind": "business-description",
        "excerpt": ("M.A Drywall & Restoration Co is your go-to solution for all home and business repairs whether "
                    "it's a small home fix or a large commercial restoration"),
        "note": "Self-description displayed in the Yelp search extract; treated as a business claim, not a customer account.",
    },
]

SOURCES = [
    {"id": "city-a", "url": CITY_A, "kind": "government", "access": "page", "checkedAt": CHECKED,
     "coverage": "Entire four-chunk response read. Building-permit contact rows grouped by firm name, license1, address and ZIP for firm ZIP prefix 94122, ordered by license1, offset 200. Rows with no firm_name were not retained.",
     "note": "Field-level transcription through the page reader; not a raw download. Firm ZIP is the contact ZIP, not a project ZIP."},
    {"id": "city-a-crosscheck", "url": CITY_A_X, "kind": "government", "access": "page", "checkedAt": CHECKED,
     "coverage": "Entire targeted response read: 33 name/number pairs for the 33 building-contact records retained in this wave.",
     "note": "Independent second read of the same dataset; each retained building-contact pair appears in both queries."},
    {"id": "city-b", "url": CITY_B, "kind": "government", "access": "page", "checkedAt": CHECKED,
     "coverage": "Entire four-chunk response read. Plumbing-permit contact rows grouped by firm name, license_number, address, ZIP and phone for ZIP prefix 94122, ordered by license_number, offset 100.",
     "note": "Field-level transcription through the page reader; not a raw download. Alias rows at the same number were consolidated and noted per record."},
    {"id": "city-b-crosscheck", "url": CITY_B_X, "kind": "government", "access": "page", "checkedAt": CHECKED,
     "coverage": "Entire targeted response read: 11 name/number rows for the 10 plumbing-contact records retained (one alias row at 307912).",
     "note": "Independent second read of the same dataset; each retained plumbing-contact number appears in both queries."},
]

for num in sorted(LIC):
    SOURCES.append({
        "id": f"cslb-{num}", "url": f"{CSLB}{num}", "kind": "government", "access": "page",
        "checkedAt": CHECKED,
        "coverage": "License detail page opened and transcribed field by field: business information, entity, issue/reissue and expiry dates, status text, classifications, bond and workers' compensation lines as printed.",
        "note": "CSLB status is a point-in-time regulator read, not a capability assessment.",
    })

SOURCES += [
    {"id": "thumbtack-plumbers", "url": THUMB_PLUMBERS, "kind": "platform", "access": "page", "checkedAt": CHECKED,
     "coverage": "Live category page read through the page reader in four chunks: pro cards, badges, hire counts and the displayed review excerpts.",
     "note": "Platform content, not licence verification. Names already stored in the corpus were not re-counted; only new identities became records."},
    {"id": "thumbtack-drywall", "url": THUMB_DRYWALL, "kind": "platform", "access": "page", "checkedAt": CHECKED,
     "coverage": "First content chunk read: all four displayed drywall pro cards with ratings, hire counts and excerpts; remaining chunks are FAQ/nav boilerplate and were not used.",
     "note": "Every displayed drywall pro name was already stored in the corpus, so this page produced no new wave-18 records."},
    {"id": "thumbtack-plastering", "url": THUMB_PLASTER, "kind": "platform", "access": "page", "checkedAt": CHECKED,
     "coverage": "First content chunk read: the four displayed plastering pro cards with ratings, hire counts and excerpts.",
     "note": "Every displayed name was already stored in the corpus; no new wave-18 records."},
    {"id": "thumbtack-ceiling", "url": THUMB_CEILING, "kind": "platform", "access": "page", "checkedAt": CHECKED,
     "coverage": "First content chunk read: all six displayed ceiling-repair pro cards.",
     "note": "Every displayed name was already stored in the corpus; no new wave-18 records."},
    {"id": "thumbtack-repipe-profile", "url": REPIPE_PROFILE, "kind": "platform", "access": "search-extract", "checkedAt": CHECKED,
     "coverage": "Profile description and review text as returned in a search extract; the profile page itself was not opened.",
     "note": ("Galvanized-pipe repipe accounts; the business is already stored in the corpus as "
              "w10-repipe-specialists-san-francisco-bay-area, so this evidence is published as a fold, not a new record.")},
    {"id": "yelp-drywall-outer-sunset", "url": YELP_DW_OS, "kind": "platform", "access": "search-extract", "checkedAt": CHECKED,
     "coverage": "Yelp search results for dry wall repair near Outer Sunset as returned in a search extract; business pages not opened.",
     "note": "Yelp blocks automated page reads; extract is the access mode, stated on every record that uses it."},
    {"id": "yelp-drywall-install-outer-sunset", "url": YELP_DW_INSTALL_OS, "kind": "platform", "access": "search-extract", "checkedAt": CHECKED,
     "coverage": "Yelp search results for drywall installation near Outer Sunset as returned in a search extract.",
     "note": "Same access limitation as the other Yelp extracts."},
    {"id": "yelp-drywall-sf", "url": YELP_DW_SF, "kind": "platform", "access": "search-extract", "checkedAt": CHECKED,
     "coverage": "Yelp city-wide drywall repair service search extract; supplies the Robert Insulation & Drywall, Bendana Drywall and M A Drywall & Restoration cards.",
     "note": "Ratings, labels and quotes are exactly as displayed in the extract."},
    {"id": "yelp-nearme", "url": YELP_NEARME, "kind": "platform", "access": "search-extract", "checkedAt": CHECKED,
     "coverage": "Yelp near-me drywall repair extract; supplies The Handyman Can card (category tags and review count only).",
     "note": "No excerpt was displayed for the retained card."},
    {"id": "reddit-ssf-thread", "url": REDDIT_SSF, "kind": "community", "access": "search-extract", "checkedAt": CHECKED,
     "coverage": "Thread text as returned in a search extract; direct fetch returned HTTP 403.",
     "note": "Named plumbers in the thread (Everlast, Gomez, Crusader, an individual handyman) are all already stored in the corpus; no new records were created from this thread."},
    {"id": "reddit-asksf-thread", "url": REDDIT_ASKSF, "kind": "community", "access": "search-extract", "checkedAt": CHECKED,
     "coverage": "Thread text as returned in a search extract; direct fetch not attempted after the 403 pattern was observed.",
     "note": "Named plumbers (Pipeline Plumbing, A-1 Plumbing, Ace on Taraval) are already stored in the corpus."},
    {"id": "context-trip-lever", "url": "https://www.jaspector.com/wiki/trip-lever-drain/", "kind": "context", "access": "search-extract", "checkedAt": CHECKED,
     "coverage": "Technical description of trip-lever overflow drains: linkage rod, plunger, corrosion and stuck-in-tube failure modes, and adjustment before replacement.",
     "note": "Background mechanism context only; not business evidence."},
    {"id": "context-diy-thread", "url": "https://www.doityourself.com/forum/toilets-sinks-showers-dishwashers-tubs-garbage-disposals/570507-replacing-bathtub-drain-lever-no-screw-holes-screws-rusted-off.html", "kind": "context", "access": "search-extract", "checkedAt": CHECKED,
     "coverage": "Forum thread about rusted-off overflow plate screws; replies describe drilling/tapping options and note overflow replacement needs access from behind or below the tub.",
     "note": "Community DIY context only; not business evidence."},
]


def reg_entry(name, num, addr, zipc, source_id, xcheck_id, observed, extra_flags, context):
    return {
        "id": f"w18-{num}",
        "name": name,
        "registryLicenseNumber": num,
        "source": source_id,
        "crosscheckSource": xcheck_id,
        "observedFields": observed,
        "discoveryContext": context,
        "status": "hold",
        "master": False,
        "requirements": dict(REQ),
        "reviews": [],
        "flags": [
            "Historical City permit-contact lead only. The registry row proves a recorded name/number with a 94122 contact address; it does not prove the licence is current, that either required trade is offered, or that the firm still operates.",
            "No attributable business review was read for this record in this session. Missing reviews are neither positive nor negative evidence.",
            "Both required services (plumbing and drywall/ceiling restoration), Outer Sunset dispatch, a seized-overflow outcome, project insurance and a written repair-first scope remain unconfirmed.",
        ] + extra_flags,
    }


def main():
    entries = []
    transcription = []
    ctx_a = ("Building-permit contact query filtered to firm ZIP prefix 94122 (offset 200, ordered by license1). "
             "The ZIP is the firm contact ZIP, not a work location. Confirmed again in the targeted cross-check query.")
    ctx_b = ("Plumbing-permit contact query filtered to ZIP prefix 94122 (offset 100, ordered by license_number). "
             "The ZIP is the firm contact ZIP, not a work location. Confirmed again in the targeted cross-check query.")

    for name, num, addr, zipc, count, extra in REG_A:
        observed = {"firm_name": name, "license1": num, "firm_address": addr,
                    "firm_zipcode": zipc, "count": count}
        transcription.append({"firm_name": name, "license": num, "dataset": "3pee-9qhc"})
        entry = reg_entry(name, num, addr, zipc, "city-a", "city-a-crosscheck", observed, extra, ctx_a)
        if num in LIC:
            lic = LIC[num]
            entry["licenseCheck"] = {
                "legalName": lic["legalName"], "number": num, "status": lic["status"],
                "classes": lic["classes"], "entity": lic["entity"], "issued": lic["issued"],
                "expires": lic["expires"], "address": lic["address"], "phone": lic["phone"],
                "checkedAt": CHECKED, "sourceAsOf": lic["sourceAsOf"],
                "url": f"{CSLB}{num}", "statusExcerpt": lic["statusExcerpt"],
                "bond": lic["bond"], "workersComp": lic["workersComp"],
                "additional": lic["extra"],
            }
            entry["flags"] = lic["flags"] + entry["flags"]
        entries.append(entry)

    for name, num, addr, zipc, phone, count, extra in REG_B:
        observed = {"firm_name": name, "license_number": num, "address": addr,
                    "zipcode": zipc, "phone": phone, "count": count}
        transcription.append({"firm_name": name, "license": num, "dataset": "k6kv-9kix"})
        entries.append(reg_entry(name, num, addr, zipc, "city-b", "city-b-crosscheck", observed, extra, ctx_b))

    for p in PLATFORM:
        entries.append({
            "id": p["id"], "name": p["name"], "trade": "platform-lead",
            "license": None, "source": p["source"], "crosscheckSource": None,
            "platformEvidence": p["platformEvidence"],
            "discoveryContext": ("Platform/community listing read on 2026-09-17. Platform presence, badges and ratings "
                                 "are not licence verification and not capability verification."),
            "status": "hold", "master": False,
            "requirements": dict(REQ),
            "reviews": p["reviews"],
            "flags": p["flags"],
        })

    wave = {
        "schemaVersion": 1,
        "wave": 18,
        "checkedAt": CHECKED,
        "stage": "discovery-only",
        "baselineSha256": BASELINE,
        "note": ("50 new discovery records, not 50 verified businesses or qualified matches: 43 City registry "
                 "records (12 with direct CSLB reads - 2 active, 2 suspended, 2 inactive, 6 expired - and 31 "
                 "registry-only) plus 7 platform/community listings. Five review excerpts and one business "
                 "self-description were retained with source links. One further account was folded into a record "
                 "the corpus already stores (see dedupeFolds). The 793-record research corpus and the empty "
                 "qualified master are unchanged."),
        "dedupeFolds": [
            {
                "name": "Repipe Specialists - San Francisco Bay Area",
                "storedAs": "w10-repipe-specialists-san-francisco-bay-area",
                "reason": ("The Thumbtack category page and search extracts displayed this business, but the corpus "
                           "already stores it under the same profile URL. No parallel record was created."),
                "evidence": ("A displayed customer account (read mid-sentence on the category page fragment, truncated "
                             "start marked) describes cutting out walls and ceiling to access pipes, then patching, "
                             "re-plastering, re-stuccoing and painting with undetectable results - the destructive-access "
                             "fallback path with full restoration, relevant to this project's contingency but not to the "
                             "repair-first attempt."),
                "sources": ["thumbtack-plumbers", "thumbtack-repipe-profile"],
            },
        ],
        "sources": SOURCES,
        "sourceTranscription": transcription,
        "entries": entries,
        "reviews": REVIEWS,
        "passes": {
            "pass1": ("Transcribed every retained registry row from the opened City responses (all four chunks of each "
                      "discovery query) and every licence field from the opened CSLB pages; unread fields were left absent."),
            "pass2": ("Compared all 50 candidate names, stripped name cores, ids and registry numbers against the 793-record "
                      "corpus and the 50 wave-17 records before writing any record; known collisions were excluded. Each "
                      "registry number was then re-read in a targeted cross-check query of the same dataset."),
            "pass3": ("Fail-closed audit: all 50 records held, every requirement gate unconfirmed, master false for all, "
                      "no promotion, no private project context in any field. These are three checks by one agent, not "
                      "three independent reviewers."),
        },
    }
    out = ROOT / "data" / "wave18.json"
    out.write_text(json.dumps(wave, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {out} ({len(entries)} entries, {len(SOURCES)} sources, {len(REVIEWS)} retained excerpts)")


if __name__ == "__main__":
    main()
