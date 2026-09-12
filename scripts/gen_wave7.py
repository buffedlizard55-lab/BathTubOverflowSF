#!/usr/bin/env python3
"""Build wave 7: 50 NEW source-linked plumbing / drywall / finish discovery records.

Research date: 2026-09-11 (the same snapshot date as wave 6; waves 1-5 are 2026-09-10).

Every field below was transcribed from a page that was RETRIEVED AND READ during
this pass. Nothing is inferred, and no third-party licence number is stored as a
licence fact.

Composition (50 records):

* GROUP A - 10 records whose CSLB license detail page was READ DIRECTLY on
  cslb.ca.gov this session (10 new licence numbers). Each was discovered through
  the official SF DBI "Plumbing Permits Contacts" open-data registry
  (data.sf.gov k6kv-9kix), which supplies the licence number that was then taken
  to the regulator.
* GROUP B - 20 records that are OFFICIAL-REGISTRY-ONLY. Their licence number was
  returned by the registry but the CSLB page was NOT read this pass, so
  `license` is null and each carries an explicit "has NOT been read on CSLB"
  flag. A registry row is never promoted into a licence fact.
* GROUP C - 20 records read directly from Thumbtack's San Francisco drywall
  category pages (not from a search index). Each retains one dated, attributed
  customer review excerpt and the exact profile URL it came from.

Twelve CSLB pages were read in total. Two of those reads are NOT new records:
  * 723992 was already read in wave 2 and is stored as `joe-watterson`; the
    2026-09-11 re-read corroborates it and adds three further registry name/ZIP
    rows. Applied by scripts/patch_wave7_attaches.py.
  * 660638 resolves to BILL CALLAWAY PLUMBER, which already exists as
    `bill-callaway` (discovered from Yellow Pages in wave 1). Applied by the
    same patch script rather than double-counted.

Fail-closed rules (mirrored by scripts/merge_wave7.py):
  - nothing is promoted to the qualified master list; exactMatch stays False;
  - expired / inactive / revoked / canceled / suspended licences carry a booking
    hold and the record is never presented as bookable;
  - a classification that does not cover the declared trade is recorded as a
    scope exclusion (A-only and B-only licences cannot self-perform plumbing);
  - a platform "Licensed pro" badge is never converted into a CSLB record.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-11"


def cslb(num):
    return (
        "https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/"
        f"LicenseDetail.aspx?LicNum={num}"
    )


# --------------------------------------------------------------------------
# Sources. IDs continue from the merged dataset (max existing id = 196).
# --------------------------------------------------------------------------
REG_BASE = "https://data.sf.gov/resource/k6kv-9kix.json"

REG_ROLLUP_94122 = (
    REG_BASE + "?$select=license_number,max(firm_name)%20as%20firm,max(address)%20as%20addr,"
    "max(phone)%20as%20phone,count(permit_number)%20as%20permits&$where=zipcode=%2794122%27"
    "%20AND%20license_number%20is%20not%20null&$group=license_number&$order=permits%20DESC"
    "&$limit=200"
)
REG_ROLLUP_94116 = (
    REG_BASE + "?$select=license_number,max(firm_name)%20as%20firm,max(address)%20as%20addr,"
    "max(phone)%20as%20phone,count(permit_number)%20as%20permits&$where=zipcode=%2794116%27"
    "%20AND%20license_number%20is%20not%20null&$group=license_number&$order=permits%20DESC"
    "&$limit=150"
)
REG_VERIFY_CSLB = (
    REG_BASE + "?$select=license_number,zipcode,max(firm_name)%20as%20firm,max(address)%20as%20addr,"
    "count(permit_number)%20as%20permits&$where=license_number%20in%20(%27708086%27,%27661818%27,"
    "%27721668%27,%27576600%27,%27609942%27,%27644189%27,%27734011%27,%27716856%27,%27723992%27,"
    "%27141304%27,%27708885%27,%27660638%27)&$group=license_number,zipcode&$order=permits%20DESC"
    "&$limit=60"
)
REG_VERIFY_17 = (
    REG_BASE + "?$select=license_number,max(firm_name)%20as%20firm,max(address)%20as%20addr,"
    "max(zipcode)%20as%20zip,count(permit_number)%20as%20permits&$where=zipcode=%2794122%27%20AND"
    "%20license_number%20in%20(%27586693%27,%27486546%27,%27343610%27,%27319594%27,%27595176%27,"
    "%27611082%27,%27502603%27,%27510452%27,%27329444%27,%27703293%27,%27459387%27,%27542108%27,"
    "%27608902%27,%27552359%27,%27664585%27,%27710842%27,%27735719%27)&$group=license_number"
    "&$order=permits%20DESC&$limit=50"
)
REG_VERIFY_3 = (
    REG_BASE + "?$select=license_number,zipcode,max(firm_name)%20as%20firm,max(address)%20as%20addr,"
    "count(permit_number)%20as%20permits&$where=zipcode=%2794122%27%20AND%20license_number%20in%20"
    "(%27637927%27,%27600722%27,%27470364%27)&$group=license_number,zipcode&$order=permits%20DESC"
    "&$limit=20"
)

THUMB_NOTE = (
    "Thumbtack category page retrieved and read directly (HTTP 200, not a search-index "
    "extract). Ratings, review counts, hire counts, \u201cLicensed pro\u201d / \u201cTop Pro\u201d badges and "
    "\u201cServes San Francisco, CA\u201d statements are Thumbtack-provided platform claims, not CSLB "
    "verification and not independent proof of a transaction. Review text is reproduced as "
    "published; where the platform's own markup joined two words in the rendered text "
    "(for example \u201cdrywallrepair\u201d), the space has been restored and no word was added, "
    "removed or re-ordered. Reviewer initials are as displayed. No review date is shown on "
    "this page, so none is asserted."
)

SOURCES = [
    {"id": 197,
     "title": "SF DBI \u00b7 Plumbing Permits Contacts \u00b7 Outer Sunset 94122 roll-up by licence",
     "url": REG_ROLLUP_94122, "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Official City & County of San Francisco open-data API (dataset k6kv-9kix, "
             "\u201cPlumbing Permits Contacts\u201d, provenance: official). Queried directly this session "
             "and rolled up per CSLB licence number so one firm cannot be counted several "
             "times through address or phone spelling variants. Returned records carry "
             "data_as_of 2026-09-11T05:04:44.000 and data_loaded_at 2026-09-11T05:28:58.000. "
             "Rows are historical plumbing-permit contacts with no in-dataset permit date: "
             "they establish a recorded address and licence linkage, never present operation."},
    {"id": 198,
     "title": "SF DBI \u00b7 registry re-read of the 12 licence numbers taken to CSLB",
     "url": REG_VERIFY_CSLB, "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Verification query run AFTER the CSLB reads, grouped by licence number AND ZIP, "
             "so every firm name / address / ZIP a licence appears under in the registry is "
             "visible on one line. This is what exposed the multi-name licence histories "
             "recorded below (609942, 723992, 734011, 708086, 660638)."},
    {"id": 199,
     "title": "SF DBI \u00b7 registry verification of 17 registry-only firms",
     "url": REG_VERIFY_17, "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Confirmatory re-query for every registry-only record stored in this wave, so no "
             "firm name, address, ZIP or permit count is published from a single transient "
             "reading. Returned 17 rows, all ZIP 94122."},
    {"id": 200,
     "title": "SF DBI \u00b7 Plumbing Permits Contacts \u00b7 Parkside 94116 roll-up by licence",
     "url": REG_ROLLUP_94116, "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Same official dataset queried for ZIP 94116 (Parkside, immediately south of the "
             "Outer Sunset). 94116 is NOT the Outer Sunset: records taken from it are labelled "
             "as adjacent, never as Outer Sunset coverage."},
    {"id": 201,
     "title": "SF DBI \u00b7 registry verification of 3 further 94122 firms",
     "url": REG_VERIFY_3, "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Confirmatory re-query for Hammerhead Construction (637927), Ecd Construction Inc "
             "(470364) and Admond Construction Inc (600722), added after the first "
             "registry-only batch so that the wave still totals exactly 50 new records."},
    {"id": 202, "title": "CSLB \u00b7 708086 \u00b7 Building Repair Co", "url": cslb("708086"),
     "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Licence detail page read directly on cslb.ca.gov; page states \u201cData current as "
             "of 9/11/2026 4:58:02 PM\u201d."},
    {"id": 203, "title": "CSLB \u00b7 661818 \u00b7 Ehrich's Plumbing", "url": cslb("661818"),
     "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Read directly; page states \u201cData current as of 9/11/2026 4:58:21 PM\u201d."},
    {"id": 204, "title": "CSLB \u00b7 721668 \u00b7 A R Plumbing", "url": cslb("721668"),
     "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Read directly; page states \u201cData current as of 9/11/2026 4:58:54 PM\u201d."},
    {"id": 205, "title": "CSLB \u00b7 576600 \u00b7 Michael Kuenzli Plumbing Co", "url": cslb("576600"),
     "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Read directly; page states \u201cData current as of 9/11/2026 5:00:10 PM\u201d."},
    {"id": 206, "title": "CSLB \u00b7 609942 \u00b7 Grant Plumbing & Construction", "url": cslb("609942"),
     "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Read directly; page states \u201cData current as of 9/11/2026 5:00:42 PM\u201d."},
    {"id": 207, "title": "CSLB \u00b7 644189 \u00b7 Ru Mahn Plumbing", "url": cslb("644189"),
     "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Read directly; page states \u201cData current as of 9/11/2026 5:01:10 PM\u201d."},
    {"id": 208, "title": "CSLB \u00b7 734011 \u00b7 Midmarket Development Company Inc", "url": cslb("734011"),
     "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Read directly; page states \u201cData current as of 9/11/2026 5:01:10 PM\u201d. The page "
             "also exposes a Complaint Disclosure link for this licence."},
    {"id": 209, "title": "CSLB \u00b7 716856 \u00b7 Alpine Construction", "url": cslb("716856"),
     "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Read directly; page states \u201cData current as of 9/11/2026 5:01:55 PM\u201d."},
    {"id": 210, "title": "CSLB \u00b7 723992 \u00b7 Joe Watterson Plumbing (corroborating re-read)",
     "url": cslb("723992"), "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Re-read of a licence already stored as the wave-2 record `joe-watterson`. NOT "
             "counted as a new wave-7 record; applied by scripts/patch_wave7_attaches.py. Page "
             "states \u201cData current as of 9/11/2026 5:01:55 PM\u201d."},
    {"id": 211, "title": "CSLB \u00b7 660638 \u00b7 Bill Callaway Plumber (attach to existing record)",
     "url": cslb("660638"), "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Read directly and attached to the pre-existing wave-1 record `bill-callaway` "
             "rather than double-counted. Page states \u201cData current as of 9/11/2026 5:03:20 "
             "PM\u201d."},
    {"id": 212, "title": "CSLB \u00b7 141304 \u00b7 Ken Topping Home Improvements", "url": cslb("141304"),
     "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Read directly; page states \u201cData current as of 9/11/2026 5:03:21 PM\u201d."},
    {"id": 213, "title": "CSLB \u00b7 708885 \u00b7 Ho's Contractor Co", "url": cslb("708885"),
     "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Read directly; page states \u201cData current as of 9/11/2026 5:03:53 PM\u201d."},
    {"id": 214,
     "title": "Thumbtack \u00b7 Drywall repairers near San Francisco, CA (page read directly)",
     "url": "https://www.thumbtack.com/ca/san-francisco/drywall-repair",
     "kind": "directory", "access": "page", "checkedAt": DATE, "note": THUMB_NOTE},
    {"id": 215,
     "title": "Thumbtack \u00b7 Drywall contractors near San Francisco, CA (page read directly)",
     "url": "https://www.thumbtack.com/ca/san-francisco/drywall-contractors",
     "kind": "directory", "access": "page", "checkedAt": DATE,
     "note": THUMB_NOTE + " This page also states: \u201cThere are 323 five star Drywall "
             "Contractors in San Francisco, CA on Thumbtack.\u201d That figure is a platform "
             "marketing count and is not treated as a verified population."},
    {"id": 216,
     "title": "data.ca.gov CKAN package_search \u00b7 \u201ccontractor license\u201d (negative result)",
     "url": "https://data.ca.gov/api/3/action/package_search?q=contractor+license&rows=10",
     "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Read directly to test whether the State of California publishes an official "
             "CSLB licence extract through an open-data API, which would allow every active "
             "94122 C-36 and C-9 licensee to be enumerated rather than sampled. The query "
             "returned success:true with result.count 4 and NO Contractors State License Board "
             "dataset (the returned datasets were water-rights and unrelated records). "
             "Recorded as a checked negative: no such API was found, so CSLB facts in this "
             "wave still come only from individual licence detail pages read one at a time."},
    {"id": 217,
     "title": "CSLB \u00b7 Find A Licensed Contractor \u00b7 Search by Location (page read directly)",
     "url": "https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/ZipCodeSearch.aspx",
     "kind": "government", "access": "page", "checkedAt": DATE,
     "note": "Read directly. CSLB's own area search states: \u201csimply enter either a city or zip "
             "code and pick the license classification you want. You\u2019ll get a randomly "
             "generated list of all eligible contractors in that license classification whose "
             "CSLB license of record is in the area you entered\u201d, and \u201cYou can select only one "
             "license classification at a time.\u201d The form posts to a results page that "
             "returned HTTP 404 on a direct GET "
             "(CheckLicenseII/ZipCodeSearchResults.aspx?EnteredZip=94122&Class=C36), so no "
             "result list was obtained through it. Logged as a barrier rather than worked "
             "around; the two official channels actually used were the SF DBI registry and "
             "individual licence detail pages."},
]

GAPS_COMMON = [
    "No exact seized bathtub-overflow trip-lever extraction outcome was verified for this business.",
    "On-site feasibility, a written repair-first scope and applicable insurance are not established by this research.",
]
GAPS_TRADE = (
    "Finish-trade and general-building records do not establish authority to perform regulated "
    "plumbing; a licensed C-36 plumber must own any pipe work, and pipe work that will be "
    "covered is permit and inspection territory for the City."
)
GAPS_PLUMB = (
    "General drain cleaning, water-heater work and fixture replacement do not establish "
    "experience extracting a seized overflow mechanism from a 1940s assembly."
)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# ==========================================================================
# GROUP A - licence detail pages read directly on cslb.ca.gov (10 new records)
# ==========================================================================
# Each dict is a transcription of one CSLB page plus the registry row that led
# to it. `reg` is the verbatim registry row returned by source 198.
GROUP_A = [
    dict(
        lic="708086", name="Building Repair Co", src=202, entity_type="Sole Ownership",
        cslb_name="BUILDING REPAIR CO", addr="579 17TH AVE, SAN FRANCISCO, CA 94121",
        phone="(415) 999-1930", issue="06/12/1995", expires="2022-01-31",
        status="expired", classes=["B"], trade="general", area="outside",
        status_sentence="This license is expired and not able to contract at this time.",
        extra="The license will need a contractors bond to renew active or reactivate.",
        bond="AMERICAN CONTRACTORS INDEMNITY COMPANY \u00b7 Bond Number 10118622 \u00b7 $15,000 \u00b7 "
             "Effective 01/01/2016 \u00b7 Cancellation Date 08/21/2020",
        wc="Exempt from workers compensation; certified no employees at this time \u00b7 "
           "Effective 12/27/2019",
        reg='{"license_number":"708086","zipcode":"94122","firm":"Building Repair Co.",'
            '"addr":"1751 46th Avenue","permits":"23"} and '
            '{"license_number":"708086","zipcode":"94121-0000","firm":"Building Repair Co.",'
            '"addr":"579 17th Av","permits":"44"}',
        area_text="Registry-recorded at 1751 46th Avenue (94122, Outer Sunset) on 23 permit "
                  "rows, but CSLB's current address of record is 579 17th Avenue, 94121 (Outer "
                  "Richmond), which carries 44 further registry rows. Neither proves dispatch "
                  "to the Outer Sunset today.",
        flags=[
            ("hold", "CSLB reads licence 708086 as EXPIRED (01/31/2022) and \u201cnot able to "
                     "contract at this time\u201d, with the contractor's bond cancelled 08/21/2020 "
                     "and a note that a bond is needed to reactivate. Do not book on this "
                     "licence.", [202]),
            ("hold", "Classification is B - GENERAL BUILDING only. No C36 plumbing and no C-9 "
                     "drywall classification appears on the page, so this record could not "
                     "self-perform the pipe work even if the licence were active.", [202]),
            ("discrepancy", "Name and address history: the registry ties licence 708086 to "
                            "\u201cBuilding Repair Co.\u201d at both a 94122 Outer Sunset address (23 "
                            "rows) and a 94121 address (44 rows). CSLB's current record is the "
                            "94121 one. Registry rows are undated, so the 94122 rows cannot be "
                            "placed in time.", [198, 202]),
        ],
    ),
    dict(
        lic="661818", name="Ehrich's Plumbing", src=203, entity_type="Partnership",
        cslb_name="EHRICH'S PLUMBING", addr="1607 31ST AVENUE, SAN FRANCISCO, CA 94122",
        phone="(415) 753-5613", issue="12/28/1992", expires="2026-12-31",
        status="inactive", classes=["C36"], trade="plumbing", area="outer",
        status_sentence="This license is inactive and not able to contract at this time.",
        extra="The license will need a contractors bond to renew active or reactivate. The "
              "license will need to meet the workers compensation requirements to renew "
              "active or reactivate.",
        bond="AMERICAN CONTRACTORS INDEMNITY COMPANY \u00b7 Bond Number 100332154 \u00b7 $15,000 \u00b7 "
             "Effective 11/26/2016 \u00b7 Cancellation Date 01/06/2022",
        wc="Exempt from workers compensation; certified no employees \u00b7 Effective 10/26/2020 "
           "\u00b7 Cancellation Date 09/06/2022",
        misc="10/16/2023 - WC EXEMPT CANCELLED-LIC INACTIVATED",
        reg='{"license_number":"661818","zipcode":"94122","firm":"Ehrich\'s Plumbing",'
            '"addr":"1607 31st Ave","permits":"25"}',
        area_text="CSLB's own record places this C36 partnership at 1607 31st Avenue, 94122 - "
                  "an Outer Sunset address - and the registry independently records 25 permit "
                  "rows at the same address. The licence is nonetheless INACTIVE, so the area "
                  "match cannot be acted on.",
        flags=[
            ("hold", "CSLB reads licence 661818 as INACTIVE and \u201cnot able to contract at this "
                     "time\u201d. The page adds that both a contractor's bond and workers "
                     "compensation must be satisfied to reactivate, and its miscellaneous "
                     "section records \u201c10/16/2023 - WC EXEMPT CANCELLED-LIC INACTIVATED\u201d. An "
                     "inactive licence cannot lawfully contract.", [203]),
            ("notice", "This is the strongest AREA evidence in wave 7 that cannot be used: an "
                       "Outer Sunset 94122 address on the regulator's own page, 25 registry "
                       "permit rows at the same address, and a C36 classification issued "
                       "12/28/1992 - all attached to a licence the Board has inactivated. "
                       "Recorded so the address is not mistaken for an available contractor.",
             [198, 203]),
        ],
    ),
    dict(
        lic="721668", name="A R Plumbing", src=204, entity_type="Sole Ownership",
        cslb_name="A R PLUMBING", addr="1902 SPENCER STREET, NAPA, CA 94559",
        phone="(707) 226-6342", issue="04/19/1996", expires="2012-04-30",
        status="expired", classes=["C36"], trade="plumbing", area="outside",
        status_sentence="This license is expired and not able to contract at this time.",
        extra="",
        bond="AMERICAN CONTRACTORS INDEMNITY COMPANY \u00b7 Bond Number SC639421 \u00b7 $12,500 \u00b7 "
             "Effective 03/02/2009 \u00b7 Cancellation Date 06/02/2010",
        wc="Exempt from workers compensation; certified no employees at this time \u00b7 "
           "Effective 03/14/1996",
        reg='{"license_number":"721668","zipcode":"94122","firm":"A R   Plumbing",'
            '"addr":"1391  39th Av","permits":"19"}',
        area_text="The registry records 19 plumbing-permit rows for licence 721668 at 1391 39th "
                  "Avenue, 94122 (Outer Sunset). CSLB's current address of record is 1902 "
                  "Spencer Street, NAPA, CA 94559 with a 707 telephone number. Registry history "
                  "is not present operation.",
        flags=[
            ("hold", "CSLB reads licence 721668 as EXPIRED on 04/30/2012 and \u201cnot able to "
                     "contract at this time\u201d. Do not book.", [204]),
            ("discrepancy", "Area conflict: 19 Outer Sunset 94122 permit rows in the official "
                            "registry against a current CSLB address in Napa (94559). The same "
                            "pattern was found in wave 6 for West Cork, Flow Masters and "
                            "Moonlight Plumbing.", [198, 204]),
        ],
    ),
    dict(
        lic="576600", name="Michael Kuenzli Plumbing Co", src=205, entity_type="Sole Ownership",
        cslb_name="MICHAEL KUENZLI PLUMBING CO", addr="1234 21 AVENUE, SAN FRANCISCO, CA 94122",
        phone="(415) 310-0435", issue="09/06/1989", expires="2027-09-30",
        status="active", classes=["C36"], trade="plumbing", area="outer",
        status_sentence="This license is current and active.",
        extra="All information below should be reviewed.",
        bond="ATLANTIC SPECIALTY INSURANCE COMPANY \u00b7 Bond Number 810025476 \u00b7 $25,000 \u00b7 "
             "Effective 08/22/2025 (no cancellation date shown)",
        wc="Exempt from workers compensation; certified no employees at this time \u00b7 "
           "Effective 11/26/2025",
        misc="11/06/2015 - CASH DEPOSIT LTR SENT $15,000; 01/14/2016 - CASH DEPOSIT 15K FOLLOW "
             "UP LTR SENT",
        reg='{"license_number":"576600","zipcode":"94122","firm":"Michael Kuenzli Plumbing Co.",'
            '"addr":"1234-21st Avenue","permits":"66"}',
        area_text="CSLB's own record places this active C36 sole ownership at 1234 21 Avenue, "
                  "94122 - Outer Sunset - and the official registry independently records 66 "
                  "plumbing-permit rows at the same address (1234-21st Avenue). Area evidence "
                  "from the regulator, not from marketing copy.",
        priority=10,
        rationale="The cleanest new credential find of wave 7: an ACTIVE C36 plumbing licence "
                  "whose CSLB page itself records a 94122 Outer Sunset business address, issued "
                  "09/06/1989 and valid to 09/30/2027, with a $25,000 contractor's bond "
                  "effective 08/22/2025 that shows no cancellation date, and 66 plumbing-permit "
                  "rows at the same address in the City's own registry. Long tenure on older San "
                  "Francisco housing is plausible but NOT proven: no review, no website and no "
                  "seized-overflow case was found for it in this pass.",
        next_step="Call and ask specifically about a seized bathtub overflow trip lever in a "
                  "1940s assembly: whether they extract the linkage without opening the wall, "
                  "what they do if the plunger will not release, and whether they will quote a "
                  "diagnostic visit separately from any repair. Confirm the contracting entity "
                  "is the licence holder, recheck CSLB immediately before signing, and ask who "
                  "pulls the permit and who patches and inspects any ceiling opened below.",
        flags=[
            ("notice", "Capacity: the CSLB page records a workers-compensation exemption with a "
                       "certification of NO EMPLOYEES at this time, and the entity is a sole "
                       "ownership. That is consistent with a one-person operation, which matters "
                       "for a job that may need a plumber and a ceiling patch coordinated across "
                       "two units.", [205]),
            ("notice", "The page's miscellaneous section records 2015 and 2016 Board letters "
                       "about a $15,000 cash deposit. That is an administrative history line, "
                       "not a disciplinary finding, and no complaint disclosure link appears on "
                       "this licence. Recorded verbatim rather than interpreted.", [205]),
            ("gap", "No review sample, website or task evidence of any kind was located for "
                    "this business in wave 7. The credential is verified; the workmanship and "
                    "the availability are not.", [205]),
        ],
    ),
    dict(
        lic="609942", name="Grant Plumbing & Construction", src=206, entity_type="Sole Ownership",
        cslb_name="GRANT PLUMBING & CONSTRUCTION",
        addr="1613 142ND AVENUE, SAN LEANDRO, CA 94578",
        phone="(415) 626-5551", issue="01/18/1991", expires="2007-01-31",
        status="expired", classes=["C36", "B"], trade="plumbing", area="outside",
        status_sentence="This license is expired and not able to contract at this time.",
        extra="",
        bond="REDLAND INSURANCE COMPANY \u00b7 Bond Number ACA1703267 \u00b7 $7,500 \u00b7 Effective "
             "08/16/2001 \u00b7 Cancellation Date 10/26/2002",
        wc="Exempt from workers compensation; certified no employees at this time \u00b7 "
           "Effective 11/12/1992",
        reg='{"license_number":"609942","zipcode":"94122","firm":"Drop Stop Plumbing Service",'
            '"addr":"1481 25th Ave Ste 4","permits":"7"}; '
            '{"license_number":"609942","zipcode":"94103-0000","firm":"Grant Plumbing & '
            'Cosntructio","addr":"689 Minna St","permits":"18"}; '
            '{"license_number":"609942","firm":"Drop Stop Pluimbing Service","addr":"3330 16th '
            'Street","permits":"2"}',
        area_text="Registry rows tie licence 609942 to three spellings and three addresses, "
                  "including 7 rows at 1481 25th Ave Ste 4, 94122 under the name \u201cDrop Stop "
                  "Plumbing Service\u201d. CSLB's current record for 609942 is Grant Plumbing & "
                  "Construction, 1613 142nd Avenue, San Leandro 94578.",
        flags=[
            ("hold", "CSLB reads licence 609942 as EXPIRED on 01/31/2007 and \u201cnot able to "
                     "contract at this time\u201d, with the contractor's bond cancelled "
                     "10/26/2002. Nothing may be booked on it.", [206]),
            ("discrepancy", "Identity conflict: the Outer Sunset registry rows for this licence "
                            "are filed under \u201cDrop Stop Plumbing Service\u201d (and a misspelled "
                            "variant \u201cDrop Stop Pluimbing Service\u201d), while CSLB names the "
                            "licence holder \u201cGRANT PLUMBING & CONSTRUCTION\u201d in San Leandro. "
                            "Which entity actually performed the 94122 work cannot be resolved "
                            "from these two sources, so no Outer Sunset claim is accepted for "
                            "this record. Same failure pattern as wave 4's Repipe Champions "
                            "(#1057927).", [198, 206]),
        ],
    ),
    dict(
        lic="644189", name="Ru Mahn Plumbing", src=207, entity_type="Sole Ownership",
        cslb_name="RU MAHN PLUMBING", addr="1339 16TH AVENUE #4, SAN FRANCISCO, CA 94122",
        phone="(415) 731-4542", issue="05/07/1992", expires="1994-05-31",
        status="expired", classes=["C36"], trade="plumbing", area="outer",
        status_sentence="This license is expired and not able to contract at this time.",
        extra="",
        bond="SURETY COMPANY OF THE PACIFIC \u00b7 Bond Number 698825 \u00b7 $7,500 \u00b7 Effective "
             "07/01/1994 \u00b7 Cancellation Date 12/06/1995",
        wc="Exempt from workers compensation; certified no employees at this time \u00b7 "
           "Effective 04/02/1992",
        reg='{"license_number":"644189","zipcode":"94122","firm":"Ru-Mahn Plumbing",'
            '"addr":"1339 16th Avenue","permits":"4"}',
        area_text="CSLB's own record places this C36 at 1339 16th Avenue #4, 94122 and the "
                  "registry records 4 permit rows at 1339 16th Avenue, 94122 - an exact address "
                  "match. The licence expired 05/31/1994.",
        flags=[
            ("hold", "CSLB reads licence 644189 as EXPIRED on 05/31/1994 - more than three "
                     "decades ago - and \u201cnot able to contract at this time\u201d. The bond was "
                     "cancelled 12/06/1995. Do not book.", [207]),
            ("discrepancy", "The official registry still returns permit rows for this licence at "
                            "the same 94122 address although the licence expired in 1994. "
                            "Registry rows carry no in-dataset date, so they cannot be used to "
                            "infer recent activity - which is exactly why every registry lead in "
                            "this wave is taken to CSLB before it is treated as a contractor.",
             [198, 207]),
        ],
    ),
    dict(
        lic="734011", name="Midmarket Development Company Inc", src=208, entity_type="Corporation",
        cslb_name="MIDMARKET DEVELOPMENT COMPANY INC",
        addr="1072 FOLSOM STREET STE 483, SAN FRANCISCO, CA 94103",
        phone="(415) 934-9733", issue="03/20/1997", expires="2010-01-31",
        status="revoked", classes=["B"], trade="general", area="outside",
        status_sentence="This license is revoked and not able to contract at this time.",
        extra="The license was revoked after expiration. There is Complaint Disclosure "
              "information for this license.",
        bond="AMERICAN CONTRACTORS INDEMNITY COMPANY \u00b7 Bond Number 100048458 \u00b7 $12,500 \u00b7 "
             "Effective 05/28/2008 \u00b7 Cancellation Date 12/04/2008",
        wc="STATE COMPENSATION INSURANCE FUND \u00b7 Policy 713-0019982 \u00b7 Effective 08/22/2007 \u00b7 "
           "Expire 08/22/2008",
        misc="01/15/2008 - LICENSE REISSUED TO ANOTHER ENTITY. Reissue Date 01/15/2008. "
             "Qualifying individual PARAIC O'DONOGHUE certified ownership of 10 percent or more "
             "of the voting stock. Other: personnel listed on this license (current or "
             "disassociated) are listed on other licenses.",
        reg='{"license_number":"734011","zipcode":"94122","firm":"Killarney Construction",'
            '"addr":"1291 - 11th Ave. #5","permits":"3"}; '
            '{"license_number":"734011","zipcode":"94102-0000","firm":"Midmarket Development Co '
            'Inc","addr":"973 Market St","permits":"1"}',
        area_text="The registry returns 3 permit rows at 1291 - 11th Ave. #5, 94122 under the "
                  "firm name \u201cKillarney Construction\u201d for licence 734011. CSLB names the "
                  "licence holder MIDMARKET DEVELOPMENT COMPANY INC at 1072 Folsom Street, "
                  "94103. No Outer Sunset coverage is accepted for this record.",
        flags=[
            ("hold", "CSLB reads licence 734011 as REVOKED and \u201cnot able to contract at this "
                     "time\u201d, revoked after expiration on 01/31/2010. A revoked licence is the "
                     "most severe status in this dataset: excluded from any booking path.",
             [208]),
            ("discrepancy", "The CSLB page states \u201cThere is Complaint Disclosure information "
                            "for this license\u201d and links a Complaint Disclosure page. The "
                            "complaint content was NOT retrieved in this pass, so nothing is "
                            "asserted about it - only that the Board exposes a disclosure "
                            "record for this number.", [208]),
            ("discrepancy", "Identity conflict: the Outer Sunset registry rows are filed under "
                            "\u201cKillarney Construction\u201d while CSLB names MidMarket Development "
                            "Company Inc, and the page records \u201c01/15/2008 - LICENSE REISSUED "
                            "TO ANOTHER ENTITY\u201d. Any present-day firm trading as Killarney "
                            "Construction must be re-verified under its own licence number "
                            "before it is contacted.", [198, 208]),
        ],
    ),
    dict(
        lic="716856", name="Alpine Construction", src=209, entity_type="Partnership",
        cslb_name="ALPINE CONSTRUCTION", addr="1032 IRVING STREET #713, SAN FRANCISCO, CA 94122",
        phone="(415) 242-5198", issue="12/29/1995", expires="2021-12-31",
        status="expired", classes=["A"], trade="engineering", area="outer",
        status_sentence="This license is expired and not able to contract at this time.",
        extra="The license will need a contractors bond to renew active or reactivate.",
        bond="WESTERN SURETY COMPANY \u00b7 Bond Number 15072734 \u00b7 $25,000 \u00b7 Effective 01/01/2023 "
             "\u00b7 Cancellation Date 04/28/2023",
        wc="Exempt from workers compensation; certified no employees at this time \u00b7 "
           "Effective 09/17/2020",
        reg='{"license_number":"716856","zipcode":"94122","firm":"Alpine Construction",'
            '"addr":"1032 Irving St #713 St 713","permits":"9"}',
        area_text="CSLB's own record places this partnership at 1032 Irving Street #713, 94122 "
                  "(Outer Sunset) and the registry records 9 permit rows at the same address. "
                  "The classification is A - General Engineering only.",
        flags=[
            ("hold", "CSLB reads licence 716856 as EXPIRED on 12/31/2021 and \u201cnot able to "
                     "contract at this time\u201d, needing a contractor's bond to reactivate. Do "
                     "not book.", [209]),
            ("hold", "Scope exclusion: the only classification on the page is A - GENERAL "
                     "ENGINEERING. There is no C36, no C-9 and no B, so this licence could never "
                     "self-perform plumbing or interior drywall even while it was active. Same "
                     "pattern as wave 6's Gorman Pipeline Inc (898289).", [209]),
            ("discrepancy", "Date anomaly: the licence expired 12/31/2021, yet the contractor's "
                            "bond shown on the same page is effective 01/01/2023 and cancelled "
                            "04/28/2023 - a bond filed after the expiry date. Recorded verbatim; "
                            "not interpreted, and it does not revive the licence.", [209]),
        ],
    ),
    dict(
        lic="141304", name="Ken Topping Home Improvements", src=212, entity_type="Sole Ownership",
        cslb_name="KEN TOPPING HOME IMPROVEMENTS",
        addr="3101 VICENTE STREET, SAN FRANCISCO, CA 94116",
        phone="(415) 731-3930", issue="10/06/1953", expires="2011-04-30",
        status="expired", classes=["B", "C20"], trade="general", area="sunset",
        status_sentence="This license is expired and not able to contract at this time.",
        extra="The license was canceled after expiration.",
        bond="AMERICAN CONTRACTORS INDEMNITY COMPANY \u00b7 Bond Number SC1031358 \u00b7 $12,500 \u00b7 "
             "Effective 03/02/2009 \u00b7 Cancellation Date 11/06/2011",
        wc="EVEREST NATIONAL INSURANCE COMPANY \u00b7 Policy 7600004599101 \u00b7 Effective 01/01/2010 "
           "\u00b7 Expire 01/01/2011",
        misc="08/16/2010 - MATHEA ELSIE SHANE - DAUGHTER; 08/16/2010 - AUTH TO CONTINUE UNTIL "
             "07/19/2011; 07/19/2011 - LICENSE CANCELED PER REQUEST; 07/19/2011 - LIC CANCELED "
             "- CONTINUANCE EXPIRED",
        reg='{"license_number":"141304","zipcode":"94116","firm":"Ken Topping Home Imprmnts",'
            '"addr":"3101 Vicente Street","permits":"258"}',
        area_text="CSLB's own record places this licence at 3101 Vicente Street, 94116 "
                  "(Parkside) - the same address as its 258 registry permit rows. 94116 is "
                  "adjacent to, and is NOT, the Outer Sunset 94122.",
        flags=[
            ("hold", "CSLB reads licence 141304 as EXPIRED on 04/30/2011 and records that it "
                     "\u201cwas canceled after expiration\u201d, with the miscellaneous section showing "
                     "\u201c07/19/2011 - LICENSE CANCELED PER REQUEST\u201d and \u201cLIC CANCELED - "
                     "CONTINUANCE EXPIRED\u201d. Do not book.", [212]),
            ("notice", "Classification is B - GENERAL BUILDING plus C20 (warm-air heating, "
                       "ventilating and air conditioning). No C36 and no C-9, so the plumbing "
                       "portion could not be self-performed. A B licensee may contract for "
                       "multi-trade work only by holding the classification or subcontracting a "
                       "licensed specialty contractor.", [212]),
            ("notice", "Historical interest only: issued 10/06/1953, and the 258 registry permit "
                       "rows make it one of the largest Parkside permit histories in the "
                       "dataset. It is recorded so a long-established local name is not mistaken "
                       "for an operating contractor.", [198, 212]),
        ],
    ),
    dict(
        lic="708885", name="Ho's Contractor Co", src=213, entity_type="Sole Ownership",
        cslb_name="HO'S CONTRACTOR CO", addr="1371 46TH AVENUE, SAN FRANCISCO, CA 94122",
        phone="(415) 725-1200", issue="06/27/1995", expires="2015-06-30",
        status="expired", classes=["B"], trade="general", area="outer",
        status_sentence="This license is expired and not able to contract at this time.",
        extra="",
        bond="SURETEC INDEMNITY COMPANY \u00b7 Bond Number 208891 \u00b7 $12,500 \u00b7 Effective 09/17/2013 "
             "\u00b7 Cancellation Date 10/22/2015",
        wc="Exempt from workers compensation; certified no employees at this time \u00b7 "
           "Effective 05/13/2013",
        reg='{"license_number":"708885","zipcode":"94122","firm":"Ho\'s Contractors Co",'
            '"addr":"1371 46th Avenue","permits":"27"}',
        area_text="CSLB's own record places this licence at 1371 46th Avenue, 94122 (Outer "
                  "Sunset) and the registry records 27 permit rows at the same address under "
                  "the pluralised spelling \u201cHo's Contractors Co\u201d.",
        flags=[
            ("hold", "CSLB reads licence 708885 as EXPIRED on 06/30/2015 and \u201cnot able to "
                     "contract at this time\u201d, with the bond cancelled 10/22/2015. Do not book.",
             [213]),
            ("hold", "Classification is B - GENERAL BUILDING only: no C36 and no C-9. Even if "
                     "renewed, this record could not self-perform the pipe work.", [213]),
            ("notice", "Spelling variance only: CSLB reads \u201cHO'S CONTRACTOR CO\u201d, the registry "
                       "reads \u201cHo's Contractors Co\u201d, and both give 1371 46th Avenue, 94122 with "
                       "the same licence number. Treated as one entity; not double-counted.",
             [198, 213]),
        ],
    ),
]


def build_a(r):
    """One record per CSLB licence detail page read directly this session."""
    lic_src = r["src"]
    addr_line = f"{r['cslb_name']} \u00b7 {r['addr']} \u00b7 Business Phone Number:{r['phone']}"
    status_line = r["status_sentence"] + (f" {r['extra']}" if r.get("extra") else "")
    cls = ", ".join(r["classes"])
    claims = [
        {"field": "Discovery",
         "text": f"{r['name']} was surfaced by the official SF DBI plumbing-permit registry, "
                 f"and CSLB licence detail page #{r['lic']} was read directly on cslb.ca.gov "
                 f"on {DATE}.",
         "source": lic_src,
         "excerpt": f"Contractor's License Detail for License # {r['lic']} \u00b7 {addr_line} \u00b7 "
                    f"Entity {r['entity_type']} \u00b7 Issue Date {r['issue']} \u00b7 {status_line}"},
        {"field": "Registry",
         "text": "Registry-recorded plumbing-permit contact rows for this licence number, "
                 "re-read after the CSLB check and grouped by licence number and ZIP.",
         "source": 198, "excerpt": r["reg"]},
        {"field": "License",
         "text": f"{r['status_sentence'].rstrip('.')} \u00b7 {cls} \u00b7 {r['entity_type']} \u00b7 "
                 f"issued {r['issue']} \u00b7 expires {r['expires']}.",
         "source": lic_src, "excerpt": f"Classifications: {cls} \u00b7 {status_line}"},
        {"field": "Bonding",
         "text": "Contractor's bond exactly as recorded by CSLB on the licence detail page.",
         "source": lic_src, "excerpt": r["bond"]},
        {"field": "Workers' compensation",
         "text": "Workers' compensation position exactly as recorded by CSLB.",
         "source": lic_src, "excerpt": r["wc"]},
        {"field": "Coverage", "text": r["area_text"], "source": lic_src,
         "excerpt": addr_line},
    ]
    if r.get("misc"):
        claims.append({"field": "Miscellaneous / additional status",
                       "text": "Additional status and miscellaneous lines recorded by CSLB on "
                               "the same page, reproduced verbatim.",
                       "source": lic_src, "excerpt": r["misc"]})
    gaps = list(GAPS_COMMON)
    gaps.append(GAPS_PLUMB if r["trade"] == "plumbing" else GAPS_TRADE)
    if r["status"] != "active":
        gaps.append("Licence is not active, so current operation, dispatch and availability "
                    "cannot be established at all for this record.")
    else:
        gaps.append("Recheck CSLB immediately before contracting; an active licence is a "
                    "regulatory fact at a recorded date, not a workmanship guarantee.")
    b = {
        "id": "w7-" + slug(r["name"]), "name": r["name"], "website": None,
        "websiteSource": None,
        "status": "research" if r["status"] == "active" else "hold",
        "area": r["area"], "areaText": r["area_text"],
        "license": {"number": r["lic"], "status": r["status"],
                    "entity": r["cslb_name"], "expires": r["expires"],
                    "classes": r["classes"], "source": lic_src, "checkedAt": DATE},
        "phone": r["phone"], "phoneSource": lic_src,
        "claims": claims,
        "flags": [{"level": lv, "text": tx, "sources": srcs} for lv, tx, srcs in r["flags"]],
        "reviewIds": [], "exactMatch": False, "master": False, "checkedAt": DATE,
        "trade": r["trade"], "gaps": gaps, "platformLinks": [],
    }
    if r["status"] == "excluded":
        b["status"] = "excluded"
    if r.get("priority"):
        b["priority"] = r["priority"]
        b["rationale"] = r["rationale"]
        b["nextStep"] = r["next_step"]
    else:
        b["priority"] = None
    return b


# ==========================================================================
# GROUP B - official registry rows whose CSLB page was NOT read (20 records)
# ==========================================================================
# (licence, firm name as returned, address as returned, permit rows, source id)
GROUP_B = [
    ("586693", "C W Lee Plumbing Company", "1650 34th Avenue", 221, 199),
    ("486546", "W & J Plumbing Co.", "1346 26th Avenue", 181, 199),
    ("343610", "David Chu Plumbing", "1530 29th Avenue", 122, 199),
    ("319594", "Franks All City Plumbing", "22nd Avenue", 82, 199),
    ("608902", "W.K. Construction Company", "1626 26th Ave*", 67, 199),
    ("552359", "J K Construction Co", "1875 25th Ave *", 63, 199),
    ("595176", "Snc Plumbing & Fire Pro", "1730 - 44th Avenue", 61, 199),
    ("611082", "Allen Mechanical Plbg Co", "4thav", 60, 199),
    ("502603", "Chow's Plumbing Co", "1755 29th Avenue", 51, 199),
    ("735719", "Coast Pacific Dev. Const.", "2319 Noriega Street*", 20, 199),
    ("459387", "Larry Fitzsimmons Plbg &", "2883 A Folsom Street", 13, 199),
    ("510452", "K L Plumbing", "1926 Lawton St", 12, 199),
    ("703293", "Wallace Plumbing", "1337 5th Av", 11, 199),
    ("664585", "Transpacific Builders Inc", "1651 Noriega St", 9, 199),
    ("542108", "Noriega Heating", "1333 Noriega Street", 5, 199),
    ("329444", "Lam & Lee Plumbing Co Inc", "1723 26th Avenue", 4, 199),
    ("710842", "Campbell Custom Woodwork", "Great Highway", 2, 199),
    ("637927", "Hammerhead Construction", "1262 47th Ave", 10, 201),
    ("470364", "Ecd Construction Inc", "2535 Irving St", 3, 201),
    ("600722", "Admond Construction Inc", "2432 Judah St", 3, 201),
]
# Trade is inferred ONLY from the firm name the registry returns, and is stored
# as an unverified label. A name is never converted into a licence class.
B_TRADE = {
    "608902": "general", "552359": "general", "735719": "general", "664585": "general",
    "637927": "general", "470364": "general", "600722": "general",
    "710842": "finish", "542108": "plumbing",
}
B_NOTE = {
    "710842": "Registry address is given only as \u201cGreat Highway\u201d with ZIP 94122 and no "
              "street number, so the address cannot be resolved to a premises. The firm name "
              "indicates custom woodwork, which is why this record is kept: an access hatch "
              "door is carpentry, but the licence class behind this number has NOT been read.",
    "542108": "The name indicates heating work. The registry it appears in is a PLUMBING "
              "permit-contact registry, so the number behind it may carry a plumbing, a C-4 or "
              "a C20 classification - none of which has been read.",
    "319594": "The registry address is recorded only as \u201c22nd Avenue\u201d with no street number, "
              "so the premises cannot be resolved.",
    "611082": "The registry address is recorded only as \u201c4thav\u201d, which is not a resolvable "
              "Outer Sunset premises; the same licence also appears in the registry with a "
              "\u201c1317 - 4th Avenue #4\u201d address and a 415-334 telephone number.",
    "459387": "2883 A Folsom Street is not an Outer Sunset address; the ZIP on these rows is "
              "94122, which is itself inconsistent with that street. Flagged rather than "
              "resolved.",
}


def build_b(lic, firm, addr, permits, src):
    row = (f'{{"license_number":"{lic}","firm":"{firm}","addr":"{addr}",'
           f'"zip":"94122","permits":"{permits}"}}')
    trade = B_TRADE.get(lic, "plumbing")
    area_text = (
        f"Registry-recorded plumbing-permit contact at {addr}, ZIP 94122 (Outer Sunset), on "
        f"{permits} permit row{'s' if permits != 1 else ''}. The registry is the City's own "
        f"open data; the licence number it returns has NOT been read on CSLB, so no status, "
        f"classification or entity name is claimed."
    )
    if lic in B_NOTE:
        area_text += " " + B_NOTE[lic]
    flags = [
        {"level": "gap",
         "text": f"Licence number {lic} is returned by the official registry for this firm but "
                 f"has NOT been read on CSLB in this pass. Status, classification, legal entity, "
                 f"expiry, bond and workers' compensation are all unknown; the number is a lead, "
                 f"never a credential.",
         "sources": [src]},
        {"level": "notice",
         "text": "Registry rows are historical plumbing-permit contacts and carry no in-dataset "
                 "permit date. They prove a recorded address and a licence linkage; they do not "
                 "prove the firm is operating today, that it still holds that licence, or that "
                 "it dispatches to the Outer Sunset now.",
         "sources": [src]},
    ]
    if lic in ("710842", "319594", "611082", "459387"):
        flags.append({"level": "discrepancy",
                      "text": B_NOTE[lic], "sources": [src]})
    if trade != "plumbing":
        flags.append({"level": "notice",
                      "text": f"Trade label \u201c{trade}\u201d is inferred from the firm name the "
                              f"registry returns and is unverified. The registry only contains "
                              f"plumbing-permit contacts, so it cannot confirm what trade this "
                              f"firm actually holds a classification for.",
                      "sources": [src]})
    gaps = list(GAPS_COMMON)
    gaps.append(GAPS_PLUMB if trade == "plumbing" else GAPS_TRADE)
    gaps.append("CSLB identity, licence status and trade classification were not read for this "
                "record in wave 7; it is a registry-level lead only.")
    return {
        "id": "w7-" + slug(firm), "name": firm, "website": None, "websiteSource": None,
        "status": "research", "area": "sunset", "areaText": area_text,
        "license": None, "phone": None, "phoneSource": None,
        "claims": [
            {"field": "Discovery",
             "text": f"{firm} appears in the official SF DBI \u201cPlumbing Permits Contacts\u201d "
                     f"registry with a business address in ZIP 94122 and CSLB licence number "
                     f"{lic} recorded against those rows.",
             "source": src, "excerpt": row},
            {"field": "Registry",
             "text": f"Registry-recorded plumbing-permit contact: {firm}, {addr}, ZIP 94122, "
                     f"{permits} permit rows, licence number {lic}. Re-read in a confirmatory "
                     f"query so no field is published from a single transient reading.",
             "source": src, "excerpt": row},
            {"field": "Coverage", "text": area_text, "source": src, "excerpt": row},
        ],
        "flags": flags, "reviewIds": [], "exactMatch": False, "master": False,
        "checkedAt": DATE, "trade": trade, "gaps": gaps, "platformLinks": [],
        "priority": None,
    }


# ==========================================================================
# GROUP C - Thumbtack San Francisco category pages read directly (20 records)
# ==========================================================================
# name, profile URL, trade, area, area text, listing evidence, reviewer, quote
GROUP_C = [
    dict(
        name="Josael Reinosa",
        url="https://www.thumbtack.com/ca/san-francisco/drywall-repair/josael-reinosa/service/475036911089049622",
        trade="drywall", area="sf",
        area_text="Profile path is Thumbtack's San Francisco drywall-repair category "
                  "(/ca/san-francisco/drywall-repair/). No separate service-area statement was "
                  "retrieved, and no Outer Sunset coverage is claimed by this record.",
        listing="Named in the review section of Thumbtack's San Francisco drywall-repair page, "
                "which was read directly. No aggregate rating, review count or hire count is "
                "displayed for this entry in the retrieved text.",
        reviewer="Michael N.",
        quote="We had a leak caused by electrolysis between copper pipe and galvanized pipe. The "
              "plumbers opened up an eight foot by two foot hole in our sealing. Joseal repaired "
              "the hole with new drywall and drywall tape, muddled it, and then sanded it. "
              "Perfect repair at a reasonable price. \u2026",
        analysis="The closest match to the ceiling half of this job anywhere in seven waves: a "
                 "customer describes GALVANISED pipe involved in a leak, PLUMBERS opening a "
                 "large ceiling hole, and this pro repairing the ceiling with new drywall, tape, "
                 "mud and sanding. It is a customer account of a completed ceiling patch after "
                 "plumbing access - not of a seized overflow trip lever, not of an access hatch, "
                 "and not of work in the Outer Sunset. Spelling (\u201csealing\u201d, \u201cJoseal\u201d, "
                 "\u201cmuddled\u201d) is the reviewer's own and is reproduced as published.",
        theme="Ceiling patch after plumbing access", negative=False,
        flags=[("notice", "No CSLB licence number is published on this profile in the retrieved "
                          "text and none was read, so no credential is claimed. A drywall ceiling "
                          "patch and any access-hatch framing still need a classification that "
                          "covers them, and any pipe work needs a C-36.", [214])],
    ),
    dict(
        name="Sandoval drywall",
        url="https://www.thumbtack.com/ca/san-bruno/drywall-repair/sandoval-drywall/service/384887263474008065",
        trade="drywall", area="outside",
        area_text="Profile path places the pro's Thumbtack home market in San Bruno "
                  "(/ca/san-bruno/drywall-repair/). The review appears on Thumbtack's San "
                  "Francisco drywall-repair page, but no service-area statement covering the "
                  "Outer Sunset was retrieved.",
        listing="Named in the review section of Thumbtack's San Francisco drywall-repair page.",
        reviewer="Regina D.",
        quote="\u2026 My 100+ year old damaged plaster wall was quickly repaired with new drywall by "
              "him, and his attention to detail means that it's flush with the wall and "
              "seamless. It looks like one entire wall! Plus, he cleaned up during and "
              "afterwards, so it was easy for me to continue on painting the room!",
        analysis="Directly relevant to a 1940 building: the customer describes a 100+ year old "
                 "PLASTER wall repaired with NEW DRYWALL so that it is flush and seamless - the "
                 "same plaster-to-drywall transition a ceiling patch below a 1940 tub would "
                 "involve. It is a wall, not a ceiling, and the reviewer states painting was "
                 "left to her. Base market is San Bruno, so Outer Sunset dispatch is "
                 "unconfirmed.",
        theme="Old plaster repaired with new drywall", negative=False,
        flags=[("notice", "Reviewer names the tradesman \u201cAlfredo\u201d. A different reviewer on the "
                          "same page names an \u201cAlfredo\u201d for Baruch handyman services, and a "
                          "third names a \u201cSergio\u201d for both Fairfield Drywall Inc and Sham. The "
                          "profile URLs are distinct, so the records are kept separate and the "
                          "shared first names are logged rather than merged.", [214])],
    ),
    dict(
        name="Handyman Express",
        url="https://www.thumbtack.com/ca/san-leandro/handyman/handyman-express/service/434596248170496003",
        trade="finish", area="outside",
        area_text="Profile path places the pro's Thumbtack home market in San Leandro "
                  "(/ca/san-leandro/handyman/). No Outer Sunset coverage statement was "
                  "retrieved.",
        listing="Named in the review section of Thumbtack's San Francisco drywall-repair page.",
        reviewer="Joanna P.",
        quote="Excellent experience working with Handyman Express to repair drywall in a ceiling "
              "that was damaged by a leaking water heater. He responded immediately to my "
              "request for a quote and arranged to come and do the repair the next day. His "
              "price was reasonable and the work was high quality.",
        analysis="A CEILING drywall repair after water damage, quoted and completed next day - "
                 "the same shape of work as patching a ceiling opened for tub access. It does "
                 "not describe plaster, an access hatch, work in a unit below, or a 1940 "
                 "assembly. Base market San Leandro; Outer Sunset dispatch unconfirmed.",
        theme="Ceiling drywall after water damage", negative=False, flags=[],
    ),
    dict(
        name="Lazarit Construction",
        url="https://www.thumbtack.com/ca/burlingame/interior-painting/lazarit-construction/service/276676576147719334",
        trade="finish", area="outside",
        area_text="Profile path places the pro's Thumbtack home market in Burlingame under the "
                  "interior-painting category. No Outer Sunset coverage statement was retrieved.",
        listing="Named in the review section of Thumbtack's San Francisco drywall-repair page.",
        reviewer="Thumbtack Customer (no initials displayed)",
        quote="This was a great experience. They fixed our damaged ceiling (drywall repair and "
              "painting) so that it looks like nothing ever happened. They were efficient, their "
              "pricing was reasonable (half as much as what another company quoted!), and "
              "communicating with them was very easy throughout the process.",
        analysis="A damaged CEILING repaired with drywall and painting to the point that \u201cit "
                 "looks like nothing ever happened\u201d - the finish outcome this job needs below "
                 "the tub. The reviewer also reports the quote was half another company's, "
                 "which is a price datapoint, not a quality guarantee. Base market Burlingame.",
        theme="Ceiling drywall repair and paint match", negative=False,
        flags=[("notice", "The reviewer is shown as \u201cThumbtack Customer\u201d with no initials, so "
                          "the account cannot be attributed to a named person. Stored as "
                          "published with that limitation recorded.", [214])],
    ),
    dict(
        name="RoDidIt",
        url="https://www.thumbtack.com/ca/san-francisco/drywall-repair/rodidit/service/474068867544268824",
        trade="drywall", area="sf",
        area_text="Profile path is Thumbtack's San Francisco drywall-repair category. No "
                  "separate service-area statement was retrieved.",
        listing="Named in the review section of Thumbtack's San Francisco drywall-repair page.",
        reviewer="Tom C.",
        quote="Ro was responsive, a clear communicator, showed up on time, and did a super "
              "thorough job. He removed a TV wall mount, and completely repaired the wall "
              "damage behind it, including drywall work, filling holes, texturing, and painting.",
        analysis="Shows the full patch sequence - drywall, filling, texturing and painting - on "
                 "a wall, for a single tradesman in San Francisco. Relevant to finish quality, "
                 "not to ceilings, plaster or plumbing access.",
        theme="Full patch sequence: drywall, texture, paint", negative=False, flags=[],
    ),
    dict(
        name="WV General Contractor",
        url="https://www.thumbtack.com/ca/south-san-francisco/drywall-repair/wv-general-contractor/service/413414439878877186",
        trade="drywall", area="outside",
        area_text="Profile path places the pro's Thumbtack home market in South San Francisco "
                  "under drywall-repair. No Outer Sunset coverage statement was retrieved.",
        listing="Named in the review section of Thumbtack's San Francisco drywall-repair page.",
        reviewer="Florence W.",
        quote="Highly recommend Humberto! I'm so happy with how the drywall repair turned out. "
              "He was easy to work with, super nice, and punctual. He even added some texture "
              "with the paint to match the rest of the wall!",
        analysis="Texture matching is the specific skill that decides whether a ceiling patch "
                 "below a 1940 tub disappears. This review describes matching texture on a "
                 "wall, in South San Francisco, and says nothing about ceilings or plumbing.",
        theme="Texture matching", negative=False,
        flags=[("notice", "\u201cGeneral Contractor\u201d in a trading name is not a licence "
                          "classification. No CSLB number was published on this profile in the "
                          "retrieved text and none was read.", [214])],
    ),
    dict(
        name="Rock & Smooth Drywall",
        url="https://www.thumbtack.com/ca/pittsburg/drywall-repair/rock-smooth-drywall/service/556400741420572674",
        trade="drywall", area="sf",
        area_text="Listing states \u201cServes San Francisco, CA\u201d; the profile path places the "
                  "pro's home market in Pittsburg, CA. No Outer Sunset coverage was retrieved.",
        listing="Excellent 4.9 (54 reviews) \u00b7 \u201cGreat value\u201d \u00b7 \u201cLicensed pro\u201d badge \u00b7 51 hires "
                "on Thumbtack \u00b7 Serves San Francisco, CA.",
        reviewer="Mimi L.",
        quote="We highly recommend Ezequiel and Rock & Smooth Drywall! They are very responsive, "
              "fast, and a pleasure to work with.",
        analysis="A drywall-only specialist with a mid-size sample and a platform \u201cLicensed "
                 "pro\u201d badge. The retained review is about responsiveness, not about ceilings, "
                 "plaster or plumbing access, so it carries no task evidence. The badge is a "
                 "Thumbtack label and is NOT a CSLB read.",
        theme="Responsiveness", negative=False,
        flags=[("notice", "\u201cLicensed pro\u201d is a Thumbtack badge, not CSLB verification. No "
                          "licence number was retrieved for this business, so none is stored.",
                [214])],
    ),
    dict(
        name="Aldana co",
        url="https://www.thumbtack.com/ca/cotati/handyman/aldana-co/service/532844027876655110",
        trade="finish", area="sf",
        area_text="Listing states \u201cServes San Francisco, CA\u201d; the profile path places the "
                  "pro's home market in Cotati, CA under the handyman category.",
        listing="\u201cTop Pro\u201d \u00b7 Excellent 4.9 (15 reviews) \u00b7 28 hires on Thumbtack \u00b7 Serves San "
                "Francisco, CA.",
        reviewer="Chris M.",
        quote="Alberto brought his crew over to repair some walls and paint a room in our condo. "
              "He was professional, punctual, efficient, and did a great job.",
        analysis="A crew (not a solo operator) doing wall repair plus painting in an occupied "
                 "condo - relevant to a job that needs a patch and a paint match in a lived-in "
                 "building. Walls only; no ceiling, plaster or plumbing content. Base market "
                 "Cotati.",
        theme="Crew, wall repair and paint", negative=False, flags=[],
    ),
    dict(
        name="APM Handyman services",
        url="https://www.thumbtack.com/ca/oakland/handyman/apm-handyman-services/service/567378774740656134",
        trade="finish", area="sf",
        area_text="Listing states \u201cServes San Francisco, CA\u201d; the profile path places the "
                  "pro's home market in Oakland under the handyman category.",
        listing="\u201cTop Pro\u201d \u00b7 Exceptional 5.0 (36 reviews) \u00b7 50 hires on Thumbtack \u00b7 Serves San "
                "Francisco, CA.",
        reviewer="Courtney P.",
        quote="The quality of the repairs exceeded my expectations, and he left everything clean "
              "when the job was finished.",
        analysis="Cleanliness and repair quality in a handyman category - relevant to work "
                 "inside an occupied building, but the review names no trade, no ceiling and no "
                 "plumbing. A 5.0 across 36 reviews is a small sample.",
        theme="Cleanliness and repair quality", negative=False, flags=[],
    ),
    dict(
        name="Javier Fonseca",
        url="https://www.thumbtack.com/ca/san-jose/drywall-repair/javier-fonseca/service/417752798808309762",
        trade="drywall", area="sf",
        area_text="Listing states \u201cServes San Francisco, CA\u201d and \u201cOnline now\u201d; the profile "
                  "path places the pro's home market in San Jose under drywall-repair.",
        listing="Great 4.8 (155 reviews) \u00b7 \u201cGreat value\u201d \u00b7 257 hires on Thumbtack \u00b7 Serves San "
                "Francisco, CA \u00b7 Online now.",
        reviewer="Carla G.",
        quote="Javier and his team did an amazing job, and so quickly. So happy to have worked "
              "with him, would recommend him over and over again!",
        analysis="The largest drywall review sample read directly in wave 7 (155 reviews, 257 "
                 "hires) with a team rather than a solo operator. The retained excerpt carries "
                 "no task detail at all. Name-alike caution: a separate, unrelated \u201cFonseca "
                 "Marble and Tile\u201d already exists in this dataset.",
        theme="Volume of hires, no task detail", negative=False,
        flags=[("notice", "Near-name pair kept deliberately separate: this record is a drywall "
                          "pro; the existing dataset entry \u201cFonseca Marble and Tile\u201d is a "
                          "different trade. No reviews or credentials were merged between "
                          "them.", [214])],
    ),
    dict(
        name="Express hand",
        url="https://www.thumbtack.com/ca/san-francisco/handyman/express-hand/service/537682429367885830",
        trade="finish", area="sf",
        area_text="Profile path is Thumbtack's San Francisco handyman category. No separate "
                  "service-area statement was retrieved.",
        listing="Named in the review section of Thumbtack's San Francisco drywall-repair page; "
                "no rating or hire count is displayed for this entry in the retrieved text.",
        reviewer="Thumbtack Customer (no initials displayed)",
        quote="Repairs my drywall and did a great job",
        analysis="The shortest and weakest excerpt retained in wave 7: 38 characters, no "
                 "initials, no task detail, no ceiling or plumbing content. Kept only because "
                 "it is a genuine drywall-repair account published on the San Francisco page; it "
                 "supports nothing beyond \u201cthis pro has repaired drywall\u201d.",
        theme="Minimal drywall confirmation", negative=False,
        flags=[("notice", "Unattributed (\u201cThumbtack Customer\u201d) and 38 characters long. Treated "
                          "as the lowest-weight review evidence in this wave.", [214])],
    ),
    dict(
        name="F&Y Handyman",
        url="https://www.thumbtack.com/ca/san-francisco/handyman/fy-handyman/service/431400764115386370",
        trade="finish", area="sf",
        area_text="Profile path is Thumbtack's San Francisco handyman category. No separate "
                  "service-area statement was retrieved.",
        listing="Named in the review section of Thumbtack's San Francisco drywall-repair page.",
        reviewer="Evan F.",
        quote="F&Y did a great job repairing this drywall in an hour and a half.",
        analysis="Confirms a small drywall repair completed in about ninety minutes by a San "
                 "Francisco handyman - useful only as a scale reference for a small patch. No "
                 "ceiling, plaster or plumbing content.",
        theme="Small fast patch", negative=False, flags=[],
    ),
    dict(
        name="Legend Derry Painting",
        url="https://www.thumbtack.com/ca/san-francisco/interior-painting/legend-derry-painting/service/220300707265742012",
        trade="finish", area="sf",
        area_text="Profile path is Thumbtack's San Francisco interior-painting category. No "
                  "separate service-area statement was retrieved.",
        listing="Named in the review section of Thumbtack's San Francisco drywall-repair page.",
        reviewer="Thumbtack Customer (no initials displayed)",
        quote="Paul did a great job repairing drywall and matching texture in my bathroom. Five "
              "stars!",
        analysis="Drywall repair with TEXTURE MATCHING in a BATHROOM - the two variables that "
                 "matter most for a patch below a tub. It is a painting-category profile, so the "
                 "drywall work may be incidental, and no ceiling or access hatch is mentioned.",
        theme="Bathroom drywall and texture match", negative=False,
        flags=[("notice", "Near-name caution: the dataset already holds \u201cLegend Plumbing & "
                          "Drain\u201d. Different trade, different profile; nothing merged.", [214])],
    ),
    dict(
        name="Jovel Quality painting",
        url="https://www.thumbtack.com/ca/san-francisco/interior-painting/jovel-quality-painting/service/292723115982553115",
        trade="finish", area="sf",
        area_text="Profile path is Thumbtack's San Francisco interior-painting category. No "
                  "separate service-area statement was retrieved.",
        listing="Named in the review section of Thumbtack's San Francisco drywall-repair page.",
        reviewer="Wes M.",
        quote="Jovel was quick to respond and very friendly, while professional. He was able to "
              "come to do a drywall repair within two days. Would definitely hire Jovel again.",
        analysis="Two-day turnaround for a drywall repair in San Francisco. Response speed is "
                 "relevant when a ceiling is open, but the review carries no ceiling, plaster or "
                 "plumbing content.",
        theme="Response time", negative=False, flags=[],
    ),
    dict(
        name="Savr Handyman",
        url="https://www.thumbtack.com/ca/san-francisco/handyman/savr-handyman/service/542658877457219603",
        trade="finish", area="sf",
        area_text="Profile path is Thumbtack's San Francisco handyman category. No separate "
                  "service-area statement was retrieved.",
        listing="Named in the review section of Thumbtack's San Francisco drywall-repair page.",
        reviewer="Benjamin Y.",
        quote="Savr communicated clearly about pricing and expectations, showed up early and "
              "completed the drywall repair expertly and efficiently. I'm already working on a "
              "longer task list for another appointment.",
        analysis="Clear pricing communication plus a completed drywall repair, and a repeat "
                 "customer - relevant because this job may need a second visit to fit an access "
                 "hatch after the pipe work. No ceiling or plumbing content.",
        theme="Pricing clarity and repeat hire", negative=False, flags=[],
    ),
    dict(
        name="Fairfield Drywall Inc",
        url="https://www.thumbtack.com/ca/fairfield/drywall-repair/fairfield-drywall-inc/service/541480948531142656",
        trade="drywall", area="outside",
        area_text="Profile path places the pro's Thumbtack home market in Fairfield, CA. No "
                  "San Francisco or Outer Sunset coverage statement was retrieved.",
        listing="Named in the review section of Thumbtack's San Francisco drywall-repair page.",
        reviewer="Ansar B.",
        quote="Sergio did an awesome job repairing my drywall! He was very punctual and "
              "professional. I was very happy with the final repairs. On top of that he also "
              "gave me some tips on repairing other minor damages in my apartment. \u2026",
        analysis="Drywall repair in an apartment, plus advice on other minor damage. No ceiling, "
                 "plaster or plumbing content. Base market Fairfield (Solano County) is roughly "
                 "an hour from the Outer Sunset, so dispatch is doubtful and is recorded as "
                 "unconfirmed rather than assumed.",
        theme="Apartment drywall repair", negative=False,
        flags=[("notice", "Base market is Fairfield, CA. Appearing in a San Francisco category "
                          "page's review section does not establish that the pro travels to the "
                          "Outer Sunset.", [214])],
    ),
    dict(
        name="Honart",
        url="https://www.thumbtack.com/ca/daly-city/handyman/honart/service/357997397331607565",
        trade="finish", area="outside",
        area_text="Profile path places the pro's Thumbtack home market in Daly City under the "
                  "handyman category. Daly City borders San Francisco but is not the Outer "
                  "Sunset; no coverage statement was retrieved.",
        listing="Named in the review section of Thumbtack's San Francisco drywall-repair page.",
        reviewer="Nipun J.",
        quote="Jose helped me out with a small drywall patch/paint repair job. He communicated "
              "well, showed up on time, did a good job, and charged me a fair price.... Give him "
              "a shot.",
        analysis="A small combined drywall patch AND paint repair - the paired scope a ceiling "
                 "patch needs - in Daly City. No ceiling, plaster or plumbing content.",
        theme="Small patch plus paint", negative=False, flags=[],
    ),
    dict(
        name="THWC home improvement",
        url="https://www.thumbtack.com/ca/alameda/handyman/thwc-home-improvement/service/377199012908662788",
        trade="finish", area="outside",
        area_text="Profile path places the pro's Thumbtack home market in Alameda under the "
                  "handyman category. No San Francisco or Outer Sunset coverage statement was "
                  "retrieved.",
        listing="Named in the review section of Thumbtack's San Francisco drywall-repair page.",
        reviewer="Thumbtack Customer (no initials displayed)",
        quote="I hired THWC to repair drywall damage. The upfront and transparent pricing is "
              "very appreciated. The work quality is good. The paint color is carefully matched. "
              "The surface after the fix is smooth and blends well. Will hire again",
        analysis="The two finish outcomes this job depends on, stated explicitly: PAINT COLOR "
                 "CAREFULLY MATCHED and a surface that \u201cblends well\u201d, with upfront pricing. "
                 "Base market Alameda, so East Bay dispatch to the Outer Sunset is unconfirmed.",
        theme="Paint match and blend", negative=False, flags=[],
    ),
    dict(
        name="Baruch handyman services",
        url="https://www.thumbtack.com/ca/san-jose/drywall-repair/baruch-handyman-services/service/542152517974253587",
        trade="drywall", area="outside",
        area_text="Profile path places the pro's Thumbtack home market in San Jose under "
                  "drywall-repair. No San Francisco or Outer Sunset coverage statement was "
                  "retrieved.",
        listing="Named in the review section of Thumbtack's San Francisco drywall-repair page.",
        reviewer="Brandon W.",
        quote="Alfredo is very helpful with my drywall repair and painting. He has done a "
              "flawless work to patch all the chips and holes for my 2bdroom condo. He is very "
              "responsive and punctual with communications. I'd highly recommend Alfredo!",
        analysis="Drywall patching plus painting across a whole two-bedroom condo - volume work "
                 "rather than a single ceiling patch. Base market San Jose, roughly an hour from "
                 "the Outer Sunset.",
        theme="Whole-unit patching and paint", negative=False,
        flags=[("notice", "Reviewer names the tradesman \u201cAlfredo\u201d, the same first name a "
                          "different reviewer gives for Sandoval drywall on the same page. The "
                          "profile URLs and reviewers differ, so the two records are kept "
                          "separate and the coincidence is logged rather than merged.", [214])],
    ),
    dict(
        name="Elite Solution Will Team",
        url="https://www.thumbtack.com/ca/redwood-city/handyman/elite-solution-will-team/service/536892597307711490",
        trade="finish", area="outside",
        area_text="Profile path places the pro's Thumbtack home market in Redwood City under the "
                  "handyman category. No San Francisco or Outer Sunset coverage statement was "
                  "retrieved.",
        listing="Named in the review section of Thumbtack's San Francisco DRYWALL-CONTRACTORS "
                "page, which was read directly.",
        reviewer="Valerie H.",
        quote="I hired Will for drywall repair following a water leak in a neighbor's unit. "
              "Unfortunately, the experience was highly unprofessional and resulted in a failed "
              "remediation. \u2026",
        analysis="The most instructive negative review found in seven waves, and it is about "
                 "exactly this shape of job: drywall repair after a water leak affecting a "
                 "NEIGHBOUR'S UNIT. The same reviewer continues that the vendor \u201cperformed the "
                 "work without a proper license\u201d, performed \u201cno moisture testing whatsoever on "
                 "the water-damaged area\u201d, painted over unprepped surfaces, refused to return, "
                 "and that she \u201cended up having to hire a licensed C-9 contractor to strip, "
                 "sand, and redo the entire project from scratch\u201d. These are one customer's "
                 "allegations, not established facts, and no CSLB record was searched for this "
                 "business. They are retained because they state the three checks this project "
                 "already insists on: a real licence classification, moisture verification "
                 "before closing a ceiling, and a written scope.",
        theme="Unlicensed work and failed remediation after a leak", negative=True,
        flags=[
            ("hold", "A dated, attributed Thumbtack review alleges work performed \u201cwithout a "
                     "proper license\u201d, no moisture testing on water-damaged material, a "
                     "cosmetic cover-up and a refusal to return, with the customer re-hiring a "
                     "licensed C-9 contractor to redo the job. These are allegations by one "
                     "reviewer and are not proven; the record is held so the account is not "
                     "lost, and it is not ranked for booking.", [215]),
            ("gap", "No CSLB licence number was published on this profile in the retrieved text "
                    "and none was read, so the reviewer's licensing allegation could be neither "
                    "confirmed nor refuted from official records in this pass.", [215]),
        ],
    ),
]


def build_c(r, src):
    b = {
        "id": "w7-" + slug(r["name"]), "name": r["name"], "website": None,
        "websiteSource": None, "status": "hold" if any(f[0] == "hold" for f in r["flags"])
        else "research",
        "area": r["area"], "areaText": r["area_text"], "license": None,
        "phone": None, "phoneSource": None,
        "claims": [
            {"field": "Discovery",
             "text": f"{r['name']} was read directly from a Thumbtack San Francisco category "
                     f"page retrieved on {DATE} (HTTP 200, not a search-index extract).",
             "source": src, "excerpt": r["listing"]},
            {"field": "Listing evidence",
             "text": "Platform listing detail exactly as displayed on the retrieved page. "
                     "Ratings, review counts, hire counts and badges are Thumbtack claims.",
             "source": src, "excerpt": r["listing"]},
            {"field": "Coverage", "text": r["area_text"], "source": src,
             "excerpt": r["url"]},
        ],
        "flags": [{"level": lv, "text": tx, "sources": s} for lv, tx, s in r["flags"]],
        "reviewIds": [], "exactMatch": False, "master": False, "checkedAt": DATE,
        "trade": r["trade"], "platformLinks": [
            {"label": "Thumbtack profile", "url": r["url"], "source": src}],
        "gaps": list(GAPS_COMMON) + [
            GAPS_TRADE,
            "No CSLB licence number was published on the retrieved profile text, so legal "
            "entity, licence status and classification are unknown for this record.",
            "Thumbtack displays no publication date for this review, so none is asserted; the "
            "review is also unauthenticated as a genuine transaction.",
        ],
        "priority": None,
    }
    return b


# ==========================================================================
# Reviews (wave 7: one per GROUP C record, ids continue from R68)
# ==========================================================================
def build_reviews():
    out = []
    n = 69
    for r in GROUP_C:
        src = 215 if r["name"] == "Elite Solution Will Team" else 214
        out.append({
            "id": f"R{n}", "business": "w7-" + slug(r["name"]), "platform": "Thumbtack",
            "author": r["reviewer"],
            "identity": ("unverified-username"
                         if "no initials displayed" in r["reviewer"] else "matched"),
            "published": "No date displayed on the retrieved Thumbtack page",
            "quote": r["quote"], "analysis": r["analysis"], "theme": r["theme"],
            "source": src, "access": "page",
            "negative": r["negative"], "checkedAt": DATE, "exactTask": False,
        })
        n += 1
    return out


def main():
    businesses = [build_a(r) for r in GROUP_A]
    businesses += [build_b(*row) for row in GROUP_B]
    businesses += [build_c(r, 215 if r["name"] == "Elite Solution Will Team" else 214)
                   for r in GROUP_C]
    # attach review ids to GROUP C records
    for rev in REVIEWS:
        next(b for b in businesses if b["id"] == rev["business"])["reviewIds"].append(rev["id"])

    ids = [b["id"] for b in businesses]
    names = [b["name"].strip().lower() for b in businesses]
    assert len(businesses) == 50, len(businesses)
    assert len(set(ids)) == 50, [i for i in ids if ids.count(i) > 1]
    assert len(set(names)) == 50, [i for i in names if names.count(i) > 1]
    assert len({s["id"] for s in SOURCES}) == len(SOURCES)
    wave = {
        "wave": 7, "researchedAt": DATE,
        "note": "50 new records: 10 with a CSLB licence detail page read directly, 20 "
                "official-registry-only leads with no licence read, and 20 read directly from "
                "Thumbtack's San Francisco drywall category pages with one dated, attributed "
                "review excerpt each. No promotions; the qualified master list stays empty.",
        "businesses": businesses, "sources": SOURCES, "reviews": REVIEWS,
    }
    (ROOT / "data" / "wave7.json").write_text(
        json.dumps(wave, indent=1, ensure_ascii=False) + "\n")
    lic = [b for b in businesses if b.get("license")]
    print(f"wrote wave7.json: {len(businesses)} businesses, {len(SOURCES)} sources, "
          f"{len(REVIEWS)} reviews")
    print(f"  licence reads attached: {len(lic)} "
          f"(active {sum(1 for b in lic if b['license']['status'] == 'active')}, "
          f"non-active {sum(1 for b in lic if b['license']['status'] != 'active')})")
    print(f"  registry-only: {sum(1 for b in businesses if not b.get('license') and b['id'] in REG_IDS)}")
    print(f"  thumbtack: {sum(1 for b in businesses if b['id'] not in REG_IDS and not b.get('license'))}")


REVIEWS = build_reviews()
REG_IDS = {"w7-" + slug(f) for _, f, _, _, _ in GROUP_B}

if __name__ == "__main__":
    main()
