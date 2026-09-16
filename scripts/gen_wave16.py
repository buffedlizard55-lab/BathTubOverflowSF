#!/usr/bin/env python3
"""Generate Wave 16: 25 direct CSLB reads, 10 registry leads and 15 platform/community listings.

Everything here was read on 2026-09-16. Three evidence tiers stay separate:

* 25 licence pages opened at cslb.ca.gov and transcribed field by field, each
  with the City permit-contact row that produced the number;
* 10 City of San Francisco building-permit contact rows in ZIP 94122 that carry
  no licence number at all, stored as registry-only leads; and
* 15 platform or community listings read today (Thumbtack category pages, Yelp
  search extracts, Reddit threads).

No record is promoted, no priority is assigned, insuranceVerified, scopeConfirmed,
exactMatch and master stay false for all 50.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "wave16.json"
RESEARCH = ROOT / "data" / "research.json"
DATE = "2026-09-16"

CSLB = "https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum="
PLUMB_QUERY = (
    "https://data.sf.gov/resource/k6kv-9kix.json?%24select=firm_name%2Clicense_number"
    "%2Caddress%2Czipcode%2Cphone%2Ccount%28%2A%29&%24group=firm_name%2Clicense_number"
    "%2Caddress%2Czipcode%2Cphone&%24where=zipcode+like+%2794122%25%27&"
    "%24order=license_number&%24limit=60"
)
BUILD_QUERY = (
    "https://data.sf.gov/resource/3pee-9qhc.json?%24select=firm_name%2Clicense1"
    "%2Cfirm_address%2Cfirm_zipcode%2Ccount%28%2A%29&%24group=firm_name%2Clicense1"
    "%2Cfirm_address%2Cfirm_zipcode&%24where=firm_zipcode+like+%2794122%25%27+AND"
    "+license1+is+not+null&%24order=license1&%24limit=60"
)
NULL_QUERY = (
    "https://data.sf.gov/resource/3pee-9qhc.json?%24select=firm_name%2Cfirm_address"
    "%2Cfirm_zipcode%2Ccount%28%2A%29&%24group=firm_name%2Cfirm_address%2Cfirm_zipcode"
    "&%24where=firm_zipcode+like+%2794122%25%27+AND+license1+is+null+AND+%28firm_name+like"
    "+%27%25Construc%25%27+OR+firm_name+like+%27%25Build%25%27+OR+firm_name+like"
    "+%27%25Plumb%25%27+OR+firm_name+like+%27%25Drywall%25%27+OR+firm_name+like"
    "+%27%25Remodel%25%27+OR+firm_name+like+%27%25Handyman%25%27+OR+firm_name+like"
    "+%27%25Repair%25%27%29&%24order=count+DESC&%24limit=40"
)

# ---------------------------------------------------------------------------
# Tier A: 25 licence pages read directly at CSLB on 2026-09-16.
# registry = the City permit-contact row that surfaced the number, quoted as read
# (source index below: 663 = plumbing contact registry, 664 = building contact registry).
# ---------------------------------------------------------------------------
CSLB_READS = [
    dict(
        lic="1000783", name="Thomas Engel", entity="Sole Ownership",
        addr="1492 36TH AVE, SAN FRANCISCO, CA 94122", phone="(415) 652-3133",
        issued="02/04/2015", expires="02/28/2027", status="active", classes=["B"],
        address="1492 36th Ave", rows="8 grouped rows",
        bond="Merchants Bonding Company (Mutual) bond 101723325, $25,000, effective 01/08/2026",
        wc="exempt from workers compensation; certified no employees, effective 01/11/2025",
        area="sunset", registry=664, notes=[],
    ),
    dict(
        lic="1003699", name="Kenneth Chou", entity="Sole Ownership",
        addr="1430 28TH AVENUE, SAN FRANCISCO, CA 94122", phone="(415) 867-0054",
        issued="05/15/2015", expires="05/31/2027", status="inactive", classes=["B"],
        address="1430 28th Av", rows="10 grouped plumbing rows and 9 grouped building rows",
        bond="Western National Mutual Insurance Company bond W70424746752, $15,000, effective 04/10/2017, cancellation date 04/11/2018",
        wc="State Compensation Insurance Fund policy 9156653, effective 04/09/2016, cancellation date 02/26/2018",
        area="sunset", registry=663,
        notes=[
            "CSLB additional status: the licence will need a contractors bond to renew active or reactivate, and will need to meet the workers compensation requirements.",
        ],
    ),
    dict(
        lic="1006197", name="Reichart Construction", entity="Sole Ownership",
        addr="1540 GREAT HIGHWAY 14, SAN FRANCISCO, CA 94122", phone="(415) 410-6694",
        issued="08/06/2015", expires="08/31/2027", status="active", classes=["B"],
        address="1540 La Playa", rows="2 grouped plumbing rows, 14 and 4 grouped building rows",
        bond="Nationwide Mutual Insurance Company bond 7901259666, $25,000, effective 07/09/2025",
        wc="exempt from workers compensation; certified no employees, effective 08/02/2025",
        area="sunset", registry=663,
        notes=[
            "The City registry prints 1540 La Playa while the CSLB page prints 1540 Great Highway 14 for the same licence and the same ZIP.",
        ],
    ),
    dict(
        lic="1008172", name="Nbay Construction", entity="Corporation",
        addr="2636 JUDAH STREET #233, SAN FRANCISCO, CA 94122", phone="(415) 341-7285",
        issued="10/15/2015", expires="09/18/2023", status="canceled", classes=["B"],
        address="2636 Judah St 233", rows="16 grouped plumbing rows and 22 grouped building rows",
        bond="Hudson Insurance Company bond 30007841, $15,000, effective 01/01/2016, cancellation date 02/05/2022",
        wc="State Compensation Insurance Fund policy 9157965, effective 09/28/2016, cancellation date 02/22/2022",
        area="sunset", registry=663,
        notes=[
            "CSLB miscellaneous information records 09/18/2023 SECRETARY OF STATE - DISSOLUTION.",
            "The qualifying individual CHUN ZHONG certified ownership of 10 percent or more; CSLB notes personnel listed on this licence are listed on other licences.",
        ],
    ),
    dict(
        lic="1009077", name="Zarin Gollogly Design & Build", entity="Sole Ownership",
        addr="1622 24TH AVENUE, SAN FRANCISCO, CA 94122", phone="(415) 377-0300",
        issued="11/18/2015", expires="11/30/2025", status="expired", classes=["B"],
        address="1622 24th Avenue and 1622 24th Avenue S", rows="10 and 2 grouped building rows",
        bond="Old Republic Surety Company bond GCL5926879, $25,000, effective 01/01/2023",
        wc="Endurance Assurance Corporation policy EAW0000167800, effective 07/05/2024, expire 07/05/2025",
        area="sunset", registry=664,
        notes=[
            "The licence expiry date 11/30/2025 has passed by the read date, so the CSLB status line reads expired and not able to contract.",
        ],
    ),
    dict(
        lic="1009112", name="Zhuo Zhang Construction Inc", entity="Corporation",
        addr="1452 47TH AVENUE, SAN FRANCISCO, CA 94122", phone="(415) 307-0177",
        issued="11/19/2015", expires="11/30/2027", status="active", classes=["B"],
        address="1452 47th Avenue and 1452 7th Avenue", rows="7 plumbing and 27 building rows for 47th Avenue; 9 plumbing and 2 building rows for 7th Avenue",
        bond="Western Surety Company bond 67225016, $25,000, effective 11/16/2024",
        wc="State Compensation Insurance Fund policy 9336701, effective 04/14/2023, expire 04/14/2027; classification codes 5432 carpentry-high wage and 5140 electrical wiring-high wage",
        area="sunset", registry=663,
        notes=[
            "The City registry stores both 1452 47th Avenue and 1452 7th Avenue against this licence; the CSLB page prints 1452 47th Avenue.",
        ],
    ),
    dict(
        lic="1014452", name="Riley Remodeling and Consulting Inc", entity="Corporation",
        addr="1032 IRVING STREET #436, SAN FRANCISCO, CA 94122", phone="(415) 725-1525",
        issued="05/23/2016", expires="05/31/2028", status="active", classes=["B"],
        address="1032 Irving Street #436", rows="2 grouped plumbing rows and 6 grouped building rows",
        bond="Merchants Bonding Company (Mutual) bond 101846030, $25,000, effective 04/18/2026",
        wc="exempt from workers compensation; certified no employees, effective 04/18/2026",
        area="sunset", registry=663,
        notes=[
            "The qualifying individual RICHARD LEROY RILEY certified ownership of 10 percent or more.",
        ],
    ),
    dict(
        lic="1018105", name="Chris William Construction Inc", entity="Corporation",
        addr="1245 LAWTON STREET, SAN FRANCISCO, CA 94122", phone="(415) 917-9928",
        issued="09/12/2016", expires="09/30/2026", status="active", classes=["B", "C10"],
        address="1245 Lawton St", rows="1 grouped plumbing row",
        bond="Business Alliance Insurance Company bond G80809416767, $25,000, effective 01/01/2023",
        wc="exempt from workers compensation; certified no employees, effective 09/23/2024",
        area="sunset", registry=663,
        notes=[
            "Two qualifying individuals are listed: DAVID TD NGUYEN (effective 09/12/2016) and JOHNNY NGUYEN (effective 08/18/2022).",
            "C10 is electrical; the licence carries no plumbing or drywall classification.",
        ],
    ),
    dict(
        lic="1021804", name="Hybrid City Construction Inc", entity="Corporation",
        addr="251 FAXON AVENUE, SAN FRANCISCO, CA 94112", phone="(415) 812-1117",
        issued="12/15/2016", expires="12/31/2026", status="suspended", classes=["B"],
        address="251 Faxon Av", rows="6 grouped plumbing rows and 16 grouped building rows",
        bond="Hudson Insurance Company bond 30119677, $25,000, effective 09/19/2023, cancellation date 09/01/2026",
        wc="Benchmark Insurance Company policy 99WCGC00009821500, effective 08/05/2026, expire 08/05/2027; classification codes 5403 carpentry-low wage and 5432 carpentry-high wage",
        area="sf", registry=663,
        notes=[
            "CSLB status line reads: License is under suspension for the following reasons: License is under Contractors Bond Suspension.",
            "The CSLB address ZIP is 94112 while the City registry row prints 94122; the CSLB phone is (415) 812-1117 while the City row prints (415) 971-8890.",
        ],
    ),
    dict(
        lic="1023648", name="New City Construction Company", entity="Sole Ownership",
        addr="2309 NORIEGA ST STE 99, SAN FRANCISCO, CA 94122", phone="(415) 509-5025",
        issued="02/10/2017", expires="06/30/2028", status="active", classes=["B", "C10", "C36"],
        address="2309 Noriega St", rows="1 grouped plumbing row",
        bond="American Contractors Indemnity Company bond 100864589, $25,000, effective 06/17/2024",
        wc="exempt from workers compensation; certified no employees, effective 05/02/2026",
        area="sunset", registry=663,
        notes=[
            "CSLB miscellaneous information records 10/16/2023 WC EXEMPT CANCELLED-LIC INACTIVATED.",
            "The closest new single-licence B plus C36 (plumbing) read of this wave at a 94122 address; held anyway because no attributable review, ceiling-restoration or written repair-first evidence was joined to it.",
        ],
    ),
    dict(
        lic="1024550", name="Silver Lining Design Build Co", entity="Corporation",
        addr="1125 LAWTON STREET, SAN FRANCISCO, CA 94122", phone="(303) 819-3086",
        issued="03/10/2017", reissued="10/30/2018", expires="10/31/2028", status="active",
        classes=["B"], address="1125 Lawton St", rows="1 grouped plumbing row and 7 grouped building rows",
        bond="Atlantic Specialty Insurance Company bond 800273117, $25,000, effective 09/01/2026",
        wc="exempt from workers compensation; certified no employees, effective 09/08/2026",
        area="sunset", registry=663,
        notes=[
            "CSLB reissue date 10/30/2018 with miscellaneous information LICENSE REISSUED TO ANOTHER ENTITY.",
            "The qualifying individual CARL BEN SAVITZ certified ownership of 10 percent or more.",
        ],
    ),
    dict(
        lic="1029195", name="Fly Cloud Construction Inc", entity="Corporation",
        addr="1254 18TH AVE 3, SAN FRANCISCO, CA 94122", phone="(415) 879-6118",
        issued="07/24/2017", reissued="06/23/2023", expires="06/30/2027", status="active",
        classes=["B"], address="1254 18th Av", rows="10 grouped building rows",
        bond="American Contractors Indemnity Company bond 100754712, $25,000, effective 06/23/2023",
        wc="exempt from workers compensation; certified no employees, effective 05/09/2025",
        area="sunset", registry=664,
        notes=[
            "CSLB reissue date 06/23/2023 with miscellaneous information LICENSE REISSUED TO ANOTHER ENTITY.",
            "The City registry row prints phone (415) 350-9953 for this licence; the CSLB page prints (415) 879-6118.",
        ],
    ),
    dict(
        lic="1033149", name="D-Finity Construction Inc", entity="Corporation",
        addr="1440 A 25TH AVE, SAN FRANCISCO, CA 94122", phone="(415) 806-5888",
        issued="11/20/2017", expires="10/29/2024", status="revoked", classes=["B"],
        address="1440 25th Av A", rows="16 grouped plumbing rows and 21 grouped building rows",
        bond="Hudson Insurance Company bond 30049985, $25,000, effective 01/01/2023, cancellation date 09/07/2024",
        wc="exempt from workers compensation; certified no employees, effective 04/03/2024",
        area="sunset", registry=663,
        notes=[
            "CSLB status line reads: This license is revoked and not able to contract at this time.",
            "The CSLB page also links complaint disclosure and states there is complaint disclosure information for this licence. The complaint page itself was not opened in this wave, so no allegation is characterised here.",
            "The qualifying individual DAVID SIUMAN TANG certified ownership of 10 percent or more.",
        ],
    ),
    dict(
        lic="1033503", name="Shelter Cove Construction", entity="Partnership",
        addr="1210 47TH AVE, SAN FRANCISCO, CA 94122", phone="(415) 640-3970",
        issued="12/01/2017", expires="12/31/2021", status="expired", classes=["B"],
        address="1210 47th Av", rows="9 grouped building rows",
        bond="Navigators Insurance Company bond NAV00011485, $15,000, effective 11/10/2019, cancellation date 11/11/2021",
        wc="State Compensation Insurance Fund policy 9231998, effective 05/22/2019, expire 05/22/2022",
        area="sunset", registry=664,
        notes=[
            "The licence expiry date 12/31/2021 has passed by the read date.",
            "A second licence, 1082812, is also printed as Shelter Cove Construction at 1210 47th Av in the City registry; it was not read in this wave and is not stored.",
        ],
    ),
    dict(
        lic="1035799", name="Actually Design Build", entity="Sole Ownership",
        addr="1429 46TH AVENUE, SAN FRANCISCO, CA 94122", phone="(415) 243-6701",
        issued="02/12/2018", expires="02/28/2030", status="inactive", classes=["B"],
        address="1359 48th Av", rows="21 grouped building rows; a separate row prints 1429 46th Ave",
        bond="Suretec Insurance Company bond 138346, $25,000, effective 01/01/2023, cancellation date 01/28/2023",
        wc="exempt from workers compensation; effective 01/13/2020, cancellation date 03/01/2022",
        area="sunset", registry=664,
        notes=[
            "CSLB status is inactive and not able to contract; the additional status notes a contractors bond and workers compensation are needed to reactivate.",
            "The City registry row prints 1359 48th Av while the CSLB page prints 1429 46th Avenue.",
            "CSLB miscellaneous information records 10/16/2023 WC EXEMPT CANCELLED-LIC INACTIVATED.",
        ],
    ),
    dict(
        lic="1044915", name="Slick Construction Inc", entity="Corporation",
        addr="1422 16TH AVE, SAN FRANCISCO, CA 94122", phone="(415) 940-9199",
        issued="09/27/2018", reissued="09/26/2019", expires="09/30/2027", status="active",
        classes=["B"], address="1422 16th Av", rows="11 grouped building rows",
        bond="Atlantic Specialty Insurance Company bond 800209324, $25,000, effective 09/26/2025",
        wc="American Casualty Company of Reading PA policy WC8035983569, effective 09/08/2026, expire 09/08/2027; classification codes 5432 carpentry-high wage and 5403 carpentry-low wage",
        area="sunset", registry=664,
        notes=[
            "CSLB reissue date 09/26/2019 with miscellaneous information LICENSE REISSUED TO ANOTHER ENTITY.",
            "The qualifying individual NICHOLAS GERARD COLEMAN certified ownership of 10 percent or more.",
        ],
    ),
    dict(
        lic="1047639", name="B&K Construction Inc", entity="Corporation",
        addr="1759 33RD AVENUE, SAN FRANCISCO, CA 94122", phone="(415) 990-9431",
        issued="12/07/2018", expires="12/31/2026", status="active", classes=["B"],
        address="1759 1759 33rd Av", rows="3 grouped plumbing rows and 3 grouped building rows",
        bond="Atlantic Specialty Insurance Company bond 800210107, $25,000, effective 09/05/2025",
        wc="State Compensation Insurance Fund policy 9241920, effective 01/15/2019, expire 01/15/2027; classification codes 54031, 51831 plumbing-low wage and 52011 concrete-cement work-sidewalks-low wage",
        area="sunset", registry=663,
        notes=[
            "The CSLB classifications page lists B only, while the workers compensation classification codes include 51831 plumbing-low wage. The mismatch is recorded, not resolved.",
            "The qualifying individual BO ZHONG LIANG certified ownership of 10 percent or more.",
        ],
    ),
    dict(
        lic="1048032", name="Jakobson Construction Inc", entity="Corporation",
        addr="PO BOX 470253, SAN FRANCISCO, CA 94147", phone="(415) 875-0690",
        issued="12/18/2018", expires="12/31/2026", status="active", classes=["B"],
        address="1675 08th Av", rows="10 grouped building rows",
        bond="Western Surety Company bond 67292353, $25,000, effective 12/23/2024",
        wc="National Liability and Fire Insurance Company policy N9WC668123, effective 04/28/2026, expire 04/28/2027",
        area="sf", registry=664,
        notes=[
            "The CSLB business address is a PO box in ZIP 94147 while the City registry row prints 1675 08th Av, 94122. No service-area claim is inferred from either.",
            "The qualifying individual MIKAEL JAKOBSON certified ownership of 10 percent or more.",
        ],
    ),
    dict(
        lic="1048617", name="Jian Hua Construction", entity="Sole Ownership",
        addr="1719 42ND AVENUE, SAN FRANCISCO, CA 94122", phone="(415) 760-8817",
        issued="01/04/2019", expires="01/31/2027", status="active", classes=["B"],
        address="1719 42nd St", rows="1 grouped plumbing row and 2 grouped building rows",
        bond="Western Surety Company bond 66864390, $25,000, effective 03/15/2024",
        wc="exempt from workers compensation; certified no employees, effective 12/06/2024",
        area="sunset", registry=663,
        notes=[
            "The City registry row prints 1719 42nd St while the CSLB page prints 1719 42ND AVENUE.",
        ],
    ),
    dict(
        lic="1048687", name="Yan Construction", entity="Sole Ownership",
        addr="1433 7TH AVENUE, SAN FRANCISCO, CA 94122", phone="(415) 867-5797",
        issued="01/07/2019", expires="01/31/2027", status="active", classes=["B"],
        address="1433 07th Ave", rows="2 grouped building rows",
        bond="Merchants Bonding Company (Mutual) bond 101320809, $25,000, effective 10/30/2024",
        wc="exempt from workers compensation; certified no employees, effective 01/14/2025",
        area="sunset", registry=664,
        notes=[
            "The City registry row for this licence prints the malformed ZIP 941222; the CSLB page prints 94122.",
        ],
    ),
    dict(
        lic="1053452", name="CMAC Construction LLC", entity="Ltd Liability",
        addr="704 CHERRY STREET, NOVATO, CA 94945", phone="(415) 680-6036",
        issued="05/13/2019", reissued="05/24/2023", expires="05/31/2027", status="active",
        classes=["B"], address="1295 41st Av", rows="1 grouped plumbing row and 13 grouped building rows",
        bond="Merchants Bonding Company (Mutual) bond 101889415, $25,000, effective 05/24/2026; LLC Employee/Worker Bond with Great American Insurance Company, bond 4906454, $100,000, effective 05/24/2023",
        wc="Everest Premier Insurance Company policy 7600028319261, effective 07/31/2026, expire 07/31/2027; classification codes 5432 carpentry-high wage, 5403 carpentry-low wage and 5484 plastering-stucco work-low wage",
        area="outside", registry=663,
        liability="Gotham Insurance Company policy GL202600040991, amount $2,000,000, effective 02/24/2026, expiration 02/24/2027",
        notes=[
            "CSLB reissue date 05/24/2023 with miscellaneous information LICENSE REISSUED TO ANOTHER ENTITY.",
            "The CSLB business address is in Novato while the City registry row prints 1295 41st Av, 94122.",
            "This is the only record of the 25 direct reads in this wave whose CSLB page prints a liability-insurance line, and it is still held: the address, the past 94122 permit rows and the absence of attributable reviews leave area and task evidence open.",
        ],
    ),
    dict(
        lic="1070288", name="Basset Engineering", entity="Corporation",
        addr="2354 MARKET ST, SAN FRANCISCO, CA 94114", phone="(415) 930-2385",
        issued="10/26/2020", expires="10/31/2028", status="active", classes=["A"],
        address="P.O.Box 22095", rows="3 grouped building rows",
        bond="Great Midwest Insurance Company bond GM222619, $25,000, effective 12/13/2023",
        wc="An employee service group holds the workers compensation insurance; policy C58905495, effective 06/01/2025, expire 06/01/2027",
        area="sf", registry=664,
        notes=[
            "The classification is A - GENERAL ENGINEERING, not B and not C36, so it does not cover either trade this project needs.",
            "The qualifying individual SHANE JOSEPH MCCARTHY certified ownership of 10 percent or more; CSLB notes personnel listed on this licence are listed on other licences.",
        ],
    ),
    dict(
        lic="1074425", name="Dmsquare Construction 2 Inc", entity="Corporation",
        addr="2715 OTIS DRIVE, ALAMEDA, CA 94501", phone="(415) 806-6687",
        issued="04/01/2021", expires="04/30/2027", status="active", classes=["B"],
        address="571 Edinburgh St", rows="4 grouped plumbing rows",
        bond="Western Surety Company bond 72347495, $25,000, effective 01/01/2023",
        wc="exempt from workers compensation; certified no employees, effective 04/03/2025",
        area="outside", registry=663,
        notes=[
            "The CSLB business address is in Alameda while the City registry row prints 571 Edinburgh St, 94122.",
            "The qualifying individual DAN VI FUNG certified ownership of 10 percent or more.",
        ],
    ),
    dict(
        lic="1090715", name="Dreamsky Construction", entity="Sole Ownership",
        addr="1685 19TH AVENUE, SAN FRANCISCO, CA 94122", phone="(415) 350-9953",
        issued="04/26/2022", expires="04/30/2028", status="active", classes=["B"],
        address="1685 19th Av", rows="7 grouped plumbing rows and 8 grouped building rows",
        bond="Atlantic Specialty Insurance Company bond 800233214, $25,000, effective 03/16/2026",
        wc="exempt from workers compensation; certified no employees, effective 03/06/2026",
        area="sunset", registry=663,
        notes=[
            "The City registry prints (415) 350-9953 for both this licence and Fly Cloud Construction (1029195). The CSLB pages print (415) 350-9953 for this licence and (415) 879-6118 for 1029195, so the shared registry phone is a City-row irregularity, not a shared CSLB phone.",
        ],
    ),
    dict(
        lic="1092217", name="Sound Build", entity="Corporation",
        addr="1798 GREAT HWY APT 3, SAN FRANCISCO, CA 94122", phone="(415) 672-2485",
        issued="06/01/2022", expires="06/30/2028", status="active", classes=["B", "C-2"],
        address="1798 Great Hwy Apt 3", rows="1 grouped plumbing row and 9 grouped building rows",
        bond="Western Surety Company bond 67695089, $25,000, effective 03/01/2026; the CSLB page links a Bond of Qualifying Individual history",
        wc="Norguard Insurance Company policy SOWC762069, effective 02/27/2026, expire 02/27/2027; classification codes 5432 carpentry-high wage, 5403 carpentry-low wage and 9011",
        area="sunset", registry=663,
        notes=[
            "C-2 is insulation and acoustical; the licence carries no plumbing or drywall classification.",
            "The qualifying individual BRIAN WARD VEIT is effective 05/26/2026.",
        ],
    ),
]

# ---------------------------------------------------------------------------
# Tier B: 10 City of San Francisco 94122 building-permit contact rows with no
# licence number in the row. Name, address and row count only.
# ---------------------------------------------------------------------------
REGISTRY_LEADS = [
    ("eky-builder", "Eky Builder Inc.", "4525 Lincoln Way, Suite# A", "26"),
    ("s-and-j-constructions", "S & J Constructions Inc", "1846 - 33rd Avenue", "32"),
    ("property-specialists", "Property Specialists", "1516 23rd Ave", "20"),
    ("x-tean-design-construction", "X Tean Design & Construction", "2099 Irving Street Ste 205", "3"),
    ("woods-construction", "Woods Construction", "2625 Judah St#2", "2"),
    ("friendly-construction", "Friendly Construction", "1774 41st Ave", "1"),
    ("hegarty-construction", "Hegarty Construction", "1834 26th Ave", "1"),
    ("seastar-construction", "Seastar Construction", "1439 23rd Ave", "1"),
    ("cg-adams-construction", "Cg Adams Construction", "1487 45th Ave", "1"),
    ("mark-huff-construction", "Mark Huff Construction, Inc.", "1527 43rd Ave", "1"),
]

# ---------------------------------------------------------------------------
# Tier C: 15 platform or community listings read on 2026-09-16.
# source: 666 Thumbtack plumbers, 667 Thumbtack drywall repair,
#         668 Thumbtack bathroom remodeling, 669-674 Yelp search extracts,
#         675-678 Reddit threads.
# ---------------------------------------------------------------------------
PLATFORM = [
    dict(
        slug="ace-on-taraval", name="Ace on Taraval", trade="platform-listing",
        area="sunset", platform="Reddit", source=676,
        url="https://www.reddit.com/r/AskSF/comments/jcy9dl/can_you_recommend_a_plumber/",
        label="Reddit thread",
        listing="Community thread mention read 2026-09-16: a commenter replies to a request for a plumber with 'Ace on Taraval has treated us great'. Taraval Street runs through the Sunset, but the listing itself is not read, no licence is published and no scope is stated.",
        text="Community thread mention: 'Ace on Taraval has treated us great'. No licence, address, classification or scope is published in the thread.",
        theme="Neighborhood plumber mention",
        review="R166", author="City_Goat",
        quote="Ace on Taraval has treated us great",
    ),
    dict(
        slug="legend-plumbing-and-drain", name="Legend Plumbing and Drain", trade="platform-listing",
        area="sf", platform="Yelp", source=672,
        url="https://www.yelp.com/search?find_desc=24+Hour+Plumbers&find_loc=Outer+Sunset,+San+Francisco,+CA&start=120",
        label="Yelp 24-hour plumbers near Outer Sunset",
        listing="Search extract read 2026-09-16: 'Legend Plumbing and Drain 5.0 (14 reviews) Verified License'. The same search shows a second card 'Legend Plumbing & Drain 5.0 (20 reviews) Verified License'; the two cards carry different review counts and are not merged here.",
        text="Platform card: 5.0 (14 reviews) and a 'Verified License' badge. A second card for the near-identical name shows 5.0 (20 reviews).",
        theme="Duplicate platform cards",
    ),
    dict(
        slug="friendly-plumbing", name="Friendly Plumbing", trade="platform-listing",
        area="sf", platform="Yelp", source=674,
        url="https://www.yelp.com/search?find_desc=Sewer+Line+Repair&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA",
        label="Yelp sewer line repair near Outer Sunset",
        listing="Search extract read 2026-09-16: 'Friendly Plumbing 5.0 (15 reviews) Verified License - Sewer repair' with an excerpt about replacing a leaky fixture. Yelp did not serve the page directly (HTTP 403 on 2026-09-16), so only the search extract is retained.",
        text="Platform card: 5.0 (15 reviews), 'Verified License', sewer-repair category and an attributable excerpt beginning 'Highly recommend! Friendly Plumbing had completed two services for my house replaced my leaky'.",
        theme="Sewer repair",
        review="R167", author="Yelp reviewer (name not shown in extract)",
        quote="Highly recommend! Friendly Plumbing had completed two services for my house replaced my leaky",
    ),
    dict(
        slug="water-heater-boys", name="Water Heater Boys", trade="platform-listing",
        area="sf", platform="Thumbtack", source=666,
        url="https://www.thumbtack.com/ca/san-francisco/plumbers",
        label="Thumbtack San Francisco plumbers category",
        listing="Category read 2026-09-16: 5.0 (13), Top Pro, 27 hires, water-heater installation and replacement. No licence number is published on the category card.",
        text="Platform card: 5.0 (13); Top Pro; 27 hires; water heater installation or replacement; 'Serves San Francisco, CA'.",
        theme="Water heater",
        review="R168", author="Jon D.",
        quote="I was bracing myself for days without hot showers and the hassle of finding a reliable plumber. Then I stumbled upon Water Heater Boys.",
    ),
    dict(
        slug="magic-plumbing-heating-cooling", name="Magic Plumbing Heating Cooling", trade="platform-listing",
        area="sf", platform="Thumbtack", source=666,
        url="https://www.thumbtack.com/ca/san-francisco/repiping-specialists/magic-plumbing-heating-cooling/service/588097039016427524",
        label="Thumbtack San Francisco plumbers category",
        listing="Category read 2026-09-16: the card states licensed technicians and lists repiping, drain and water-heater work; no rating or licence number is exposed in the extract that was read.",
        text="Platform card: repiping list, drain clearing and water-heater installs; the card states 'Our licensed technicians handle everything from leaky faucets and clogged drains to full repipes'. No licence number is published.",
        theme="Repiping and drains",
    ),
    dict(
        slug="ja-emmanuel-construction", name="J.A. Emmanuel Construction", trade="platform-listing",
        area="sf", platform="Reddit", source=675,
        url="https://www.reddit.com/r/AskSF/comments/171irdh/looking_for_a_contractor_in_or_near_sf_who_does/",
        label="Reddit thread",
        listing="Community thread read 2026-09-16 asking for a contractor who does good drywall repair in or near San Francisco; one commenter recommends this firm from direct experience and says drywall work was involved. No licence, address or scope is published.",
        text="Community thread: 'I didn't ask him to work on dry wall specifically (although he redid several walls in my house and so there must have been dry wall work involved), but I had a great experience with J.A. Emmanuel Construction.'",
        theme="Drywall repair referral",
        review="R169", author="lessachu",
        quote="I didn't ask him to work on dry wall specifically (although he redid several walls in my house and so there must have been dry wall work involved), but I had a great experience with J.A. Emmanuel Construction.",
    ),
    dict(
        slug="sederap", name="Sederap", trade="platform-listing",
        area="sf", platform="Reddit", source=675,
        url="https://www.reddit.com/r/AskSF/comments/171irdh/looking_for_a_contractor_in_or_near_sf_who_does/",
        label="Reddit thread",
        listing="Community thread read 2026-09-16: a commenter who had not hired the firm says it appears licensed and insured and has done drywall work nearby. A second-hand, unverified mention.",
        text="Community thread: 'haven't used them myself, but a friend almost did - i'd check out sederap since theyre licensed, insured, and looks like they've done a lot of drywall work nearby.'",
        theme="Unused second-hand referral",
        review="R170", author="No-Doubt9029",
        quote="haven't used them myself, but a friend almost did - i'd check out sederap since theyre licensed, insured, and looks like they've done a lot of drywall work nearby",
    ),
    dict(
        slug="c-max-construction", name="C Max Construction", trade="platform-listing",
        area="sf", platform="Reddit", source=678,
        url="https://www.reddit.com/r/sanfrancisco/comments/1aj2hy6/general_contractor_recommendations/",
        label="Reddit thread",
        listing="Community thread read 2026-09-16 recommending general contractors in San Francisco. The recommending username matches the firm name, so the comment reads as self-promotion and is flagged rather than treated as independent review evidence.",
        text="Community thread: 'C Max Construction - reasonable prices & excellent customer service, skillful craftmanship!' posted by the username cmaxconstruction.",
        theme="Self-recommendation",
        review="R171", author="cmaxconstruction",
        quote="C Max Construction - reasonable prices & excellent customer service, skillful craftmanship!",
        self_promo=True,
    ),
    dict(
        slug="cameron-bryce-construction", name="Cameron Bryce Construction", trade="platform-listing",
        area="sf", platform="Reddit", source=678,
        url="https://www.reddit.com/r/sanfrancisco/comments/1aj2hy6/general_contractor_recommendations/",
        label="Reddit thread",
        listing="Community thread read 2026-09-16: a shortlist of three names posted in one comment with no detail about the work, the licence, the address or any scope.",
        text="Community thread: 'Cameron Bryce Construction / Dreamt Design and Build / Kiely Construction'.",
        theme="Bare name list",
        review="R172", author="pandabearak",
        quote="Cameron Bryce Construction Dreamt Design and Build Kiely Construction",
    ),
    dict(
        slug="eduardo-jose-paz-garcia-painting", name="Eduardo & Jose's Paz Garcia's Painting",
        trade="platform-listing", area="sf", platform="Thumbtack", source=667,
        url="https://www.thumbtack.com/ca/berkeley/interior-painting/eduardo-joses-paz-garcias-painting/service/220902047590138914",
        label="Thumbtack San Francisco drywall repair category",
        listing="Category read 2026-09-16: 4.4 (137), Top Pro, 151 hires, 'In high demand', appears on the San Francisco drywall-repair category and its review excerpt is about painting. No licence number is published.",
        text="Platform card: 4.4 (137); Top Pro; 151 hires; drywall-repair category; retained excerpt is about a paint job, not about drywall repair.",
        theme="Painting in a drywall category",
        review="R173", author="KARLOS G.",
        quote="Fantastic paint job. High quality work and very responsiveness",
        mismatch=True,
    ),
    dict(
        slug="economy-plumbing-sewer-drain", name="Economy Plumbing Sewer & Drain",
        trade="platform-listing", area="sf", platform="Yelp", source=672,
        url="https://www.yelp.com/search?find_desc=24+Hour+Plumbers&find_loc=Outer+Sunset,+San+Francisco,+CA&start=120",
        label="Yelp 24-hour plumbers near Outer Sunset",
        listing="Search extract read 2026-09-16: 'Economy Plumbing Sewer & Drain 3.5 (149 reviews)' with a price-comparison excerpt. No licence badge is shown on the card, unlike neighbouring cards that print 'Verified License'.",
        text="Platform card: 3.5 (149 reviews); the retained excerpt compares an estimate against other quotes.",
        theme="Price comparison",
        review="R174", author="Yelp reviewer (name not shown in extract)",
        quote="Franco came out in person within 30 minutes of calling him and gave me an estimate that was $500 cheaper than the next cheapest quote.",
    ),
    dict(
        slug="lemus-construction", name="Lemus Construction", trade="platform-listing",
        area="sf", platform="Yelp", source=673,
        url="https://yelp.com/search?find_desc=Construction&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA",
        label="Yelp construction near Outer Sunset",
        listing="Search extract read 2026-09-16: 'Lemus Construction 4.8 (21 reviews) Serving San Francisco and the Surrounding Area' with an excerpt about a design approval and an engineer. No licence badge is shown on the card.",
        text="Platform card: 4.8 (21 reviews); the retained excerpt is about design approval with the city and an engineer.",
        theme="Design approval",
        review="R175", author="Yelp reviewer (name not shown in extract)",
        quote="getting a design approved by both an engineer and the city, we hired Jose from Lemus Construction.",
    ),
    dict(
        slug="five-star-plumbing-rooter", name="Five Star Plumbing & Rooter", trade="platform-listing",
        area="sf", platform="Yelp", source=672,
        url="https://www.yelp.com/search?find_desc=24+Hour+Plumbers&find_loc=Outer+Sunset,+San+Francisco,+CA&start=120",
        label="Yelp 24-hour plumbers near Outer Sunset",
        listing="Search extract read 2026-09-16: 'Five Star Plumbing & Rooter 4.9 (89 reviews) Verified License'. No review text is exposed for this card in the extract, so no excerpt is retained.",
        text="Platform card: 4.9 (89 reviews) with a 'Verified License' badge and free estimates.",
        theme="Verified-licence badge only",
    ),
    dict(
        slug="precise-plumbing-drain", name="Precise Plumbing & Drain", trade="platform-listing",
        area="sf", platform="Yelp", source=672,
        url="https://www.yelp.com/search?find_desc=24+Hour+Plumbers&find_loc=Outer+Sunset,+San+Francisco,+CA&start=120",
        label="Yelp 24-hour plumbers near Outer Sunset",
        listing="Search extract read 2026-09-16: 'Precise Plumbing & Drain 5.0 (11 reviews)' with free consultations. No licence badge and no review text appear on the card.",
        text="Platform card: 5.0 (11 reviews); free consultations; no licence badge shown.",
        theme="Sparse card",
    ),
    dict(
        slug="antormen", name="ANT\u00d6RMEN", trade="platform-listing",
        area="sf", platform="Thumbtack", source=668,
        url="https://www.thumbtack.com/ca/san-francisco/general-contractors/antrmen/service/549741754129948686",
        label="Thumbtack San Francisco bathroom remodeling category",
        listing="Category read 2026-09-16: 5.0 (40), Top Pro, 10 hires, 'Licensed pro' badge, Serves San Francisco. The retained excerpt mentions vents and ducting for a range hood and a bathroom fan, not a drain assembly or ceiling access.",
        text="Platform card: 5.0 (40); Top Pro; 10 hires; 'Licensed pro' badge; excerpt about ventilation work.",
        theme="Ventilation, not drains",
        mismatch=True,
    ),
]

SOURCES = []
for index, read in enumerate(CSLB_READS):
    SOURCES.append(
        dict(
            id=638 + index,
            kind="government",
            access="page",
            url=f"{CSLB}{read['lic']}",
            title=f"CSLB licence detail for {read['lic']} ({read['name']})",
            checkedAt=DATE,
            note=(
                "Opened and transcribed field by field on 2026-09-16: business information, entity, issue and "
                "expiry dates, status line, classifications, bonding and workers compensation lines."
            ),
        )
    )

SOURCES.extend(
    [
        dict(
            id=663, kind="government", access="page", url=PLUMB_QUERY,
            title="SF DBI plumbing-permit contact rows grouped for ZIP 94122",
            checkedAt=DATE,
            note=(
                "Official City permit-contact registry, read 2026-09-16 and grouped by firm, licence number, address, "
                "ZIP and phone for 94122. Registry rows are discovery evidence: a number in a row is not a licence fact."
            ),
        ),
        dict(
            id=664, kind="government", access="page", url=BUILD_QUERY,
            title="SF DBI building-permit contact rows grouped for ZIP 94122",
            checkedAt=DATE,
            note=(
                "Official City permit-contact registry, read 2026-09-16 and grouped by firm, licence number and address "
                "for 94122. Used only to surface licence numbers for direct CSLB reads."
            ),
        ),
        dict(
            id=665, kind="government", access="page", url=NULL_QUERY,
            title="SF DBI building-permit contact rows in 94122 with no licence number recorded",
            checkedAt=DATE,
            note=(
                "Official City rows whose licence field is empty, filtered to firm names containing construction, "
                "builder, plumbing, drywall, remodel, handyman or repair. These rows support a firm name, an address "
                "and a row count and nothing else."
            ),
        ),
        dict(
            id=666, kind="platform", access="page", url="https://www.thumbtack.com/ca/san-francisco/plumbers",
            title="Thumbtack San Francisco plumbers category",
            checkedAt=DATE,
            note=(
                "Category page read 2026-09-16. Ratings, badges, hire counts and reviewer excerpts are the platform's "
                "own presentation; a badge is not a regulator fact and no licence number is published for the cards "
                "retained in this wave."
            ),
        ),
        dict(
            id=667, kind="platform", access="page", url="https://www.thumbtack.com/ca/san-francisco/drywall-repair",
            title="Thumbtack San Francisco drywall-repair category",
            checkedAt=DATE,
            note=(
                "Category page read 2026-09-16. Most attributable names on this page were already stored by earlier "
                "waves; only names that did not collide with the existing corpus were retained."
            ),
        ),
        dict(
            id=668, kind="platform", access="page", url="https://www.thumbtack.com/ca/san-francisco/bathroom-remodeling",
            title="Thumbtack San Francisco bathroom-remodeling category",
            checkedAt=DATE,
            note=(
                "Category page read 2026-09-16. Cards are shown for the platform's own 'bathroom remodeler' category, "
                "which can include ventilation, painting and tile work rather than the drain assembly at issue here."
            ),
        ),
        dict(
            id=669, kind="directory", access="blocked-with-search-extract",
            url="https://www.yelp.com/search?find_desc=Handyman&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA",
            title="Yelp handyman search near Outer Sunset",
            checkedAt=DATE,
            note=(
                "Yelp returned HTTP 403 to a direct read on 2026-09-16, so only the search extract is retained. Every "
                "name quoted from this source is labelled a search extract, never a read review panel."
            ),
        ),
        dict(
            id=670, kind="directory", access="blocked-with-search-extract",
            url="https://www.yelp.com/search?find_desc=Drywall+Installation&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA",
            title="Yelp drywall installation near Outer Sunset",
            checkedAt=DATE,
            note=(
                "Search extract retained after the direct read was blocked. The names on this page were all already "
                "present in the corpus, so no new record was created from them and the page is cited only as the "
                "cross-check that produced no additions."
            ),
        ),
        dict(
            id=671, kind="directory", access="blocked-with-search-extract",
            url="https://www.yelp.com/search?cflt=plumbing&find_loc=outer+sunset%2C+san+francisco%2C+ca",
            title="Yelp plumbing search near Outer Sunset",
            checkedAt=DATE,
            note=(
                "Search extract retained after the direct read was blocked. Retained cards include a plumbing supply "
                "house with an Outer Sunset street address; supply counters are not contractors and are not stored as "
                "contracting records."
            ),
        ),
        dict(
            id=672, kind="directory", access="blocked-with-search-extract",
            url="https://www.yelp.com/search?find_desc=24+Hour+Plumbers&find_loc=Outer+Sunset,+San+Francisco,+CA&start=120",
            title="Yelp 24-hour plumbers near Outer Sunset (later results page)",
            checkedAt=DATE,
            note=(
                "Search extract retained after the direct read was blocked. This page prints a 'Verified License' "
                "badge without a licence number, so the badge is recorded as platform wording only."
            ),
        ),
        dict(
            id=673, kind="directory", access="blocked-with-search-extract",
            url="https://yelp.com/search?find_desc=Construction&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA",
            title="Yelp construction search near Outer Sunset",
            checkedAt=DATE,
            note="Search extract retained after the direct read was blocked on 2026-09-16.",
        ),
        dict(
            id=674, kind="directory", access="blocked-with-search-extract",
            url="https://yelp.com/search?find_desc=Sewer+Line+Repair&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA",
            title="Yelp sewer line repair search near Outer Sunset",
            checkedAt=DATE,
            note="Search extract retained after the direct read was blocked on 2026-09-16.",
        ),
        dict(
            id=675, kind="community", access="search-extract",
            url="https://www.reddit.com/r/AskSF/comments/171irdh/looking_for_a_contractor_in_or_near_sf_who_does/",
            title="r/AskSF thread: contractor in or near SF who does good drywall repair",
            checkedAt=DATE,
            note=(
                "Thread read 2026-09-16 through the search extract; the thread body and comments are quoted as shown "
                "and no username is treated as a verified identity."
            ),
        ),
        dict(
            id=676, kind="community", access="search-extract",
            url="https://www.reddit.com/r/AskSF/comments/jcy9dl/can_you_recommend_a_plumber/",
            title="r/AskSF thread: can you recommend a plumber?",
            checkedAt=DATE,
            note=(
                "Thread read 2026-09-16 through the search extract. Community answers are opinions about businesses, "
                "not credential evidence, and each named firm still needs a regulator read."
            ),
        ),
        dict(
            id=677, kind="community", access="search-extract",
            url="https://www.reddit.com/r/AskSF/comments/1sejkq2/recommendations_for_a_general_contractor_or/",
            title="r/AskSF thread: recommendations for a general contractor or design-build firm",
            checkedAt=DATE,
            note=(
                "Thread read 2026-09-16 through the search extract. One comment notes that Sunset homes tend to hide "
                "surprises once they are opened up; that is a neighbourhood sentiment, not evidence about any firm."
            ),
        ),
        dict(
            id=678, kind="community", access="search-extract",
            url="https://www.reddit.com/r/sanfrancisco/comments/1aj2hy6/general_contractor_recommendations/",
            title="r/sanfrancisco thread: general contractor recommendations",
            checkedAt=DATE,
            note=(
                "Thread read 2026-09-16 through the search extract. One recommendation is posted by a username that "
                "matches the firm name and is retained as flagged self-promotion."
            ),
        ),
        dict(
            id=679, kind="community", access="search-extract",
            url="https://www.reddit.com/r/askaplumber/comments/17curdh/trip_lever_bathtub_old_and_broken/",
            title="r/askaplumber thread: trip lever bathtub old and broken",
            checkedAt=DATE,
            note=(
                "Practitioner thread read 2026-09-16 through the search extract. Retained as task evidence about how "
                "a seized trip-lever linkage is approached and about the replace-the-drain option, not as a review of "
                "any business in this dataset."
            ),
        ),
        dict(
            id=680, kind="community", access="search-extract",
            url="https://www.reddit.com/r/HomeImprovement/comments/esb5xg/cant_remove_triplever_drain_stopper_in_bathtub/",
            title="r/HomeImprovement thread: can't remove trip-lever drain stopper in bathtub",
            checkedAt=DATE,
            note=(
                "Thread read 2026-09-16 through the search extract. Retained as task evidence about a linkage that "
                "will not budge after penetrating oil and about when the assembly has to be changed out."
            ),
        ),
        dict(
            id=681, kind="community", access="search-extract",
            url="https://www.reddit.com/r/HomeImprovement/comments/tsd5cx/plummer_said_i_dont_do_drywall/",
            title="r/HomeImprovement thread: plumber said I don't do drywall",
            checkedAt=DATE,
            note=(
                "Thread read 2026-09-16 through the search extract. Two replies make the point that a plumbing "
                "opening is normally closed out by a separate drywall trade and that a screw-in access panel is the "
                "usual answer for a spot that may need to be reopened."
            ),
        ),
    ]
)

EXISTING = json.loads(RESEARCH.read_text(encoding="utf-8"))


def ten_digits(value: str | None) -> str:
    return re.sub(r"\D", "", value or "")[-10:]


# A phone number is stored at most once in this dataset. Where CSLB prints a
# number that an earlier record already carries, the number is left unstored and
# the collision is flagged rather than merged.
STORED_PHONES = {
    ten_digits(b.get("phone"))
    for b in EXISTING["businesses"]
    if len(ten_digits(b.get("phone"))) == 10
}


def iso(printed: str) -> str:
    """CSLB prints MM/DD/YYYY; the dataset stores ISO dates."""
    month, day, year = printed.split("/")
    return f"{year}-{month}-{day}"


BUSINESSES = []
for index, read in enumerate(CSLB_READS):
    source_id = 638 + index
    registry_id = read["registry"]
    classes = " + ".join(read["classes"])
    record = {
        "id": f"w16-{read['lic']}",
        "name": read["name"],
        "trade": read.get("trade") or (
            "multi-trade" if "C36" in read["classes"]
            else "engineering" if read["classes"] == ["A"]
            else "general"
        ),
        "website": None,
        "websiteSource": None,
        "area": read["area"],
        "areaText": (
            f"City permit-contact registry row in ZIP 94122 for licence {read['lic']} "
            f"({read['address']}, {read['rows']}); CSLB business address on the same licence is {read['addr']}. "
            "The registry row is historical permit-contact evidence and the CSLB address is a mailing address, "
            "so neither proves current Outer Sunset dispatch."
        ),
        "status": "hold",
        "checkedAt": DATE,
        "phone": read["phone"],
        "phoneSource": source_id,
        "claims": [
            {
                "field": "Discovery",
                "text": (
                    f"Registry-recorded permit contact read 2026-09-16: licence {read['lic']}, "
                    f"{read['address']}, San Francisco 94122, across {read['rows']}. The number was then opened at CSLB."
                ),
                "source": registry_id,
                "excerpt": f"{read['lic']} - {read['name']} - {read['address']} - 94122 - {read['rows']}",
            },
            {
                "field": "License",
                "text": (
                    f"CSLB page read 2026-09-16: {'current and active' if read['status'] == 'active' else read['status']} "
                    f"with classification {classes}; issue date {read['issued']}, expire date {read['expires']}; "
                    f"business address as printed {read['addr']}."
                ),
                "source": source_id,
                "excerpt": f"Contractor's License Detail for License # {read['lic']}",
            },
            {
                "field": "Bonding",
                "text": f"CSLB bonding line read 2026-09-16: {read['bond']}.",
                "source": source_id,
                "excerpt": read["bond"],
            },
            {
                "field": "Workers compensation",
                "text": f"CSLB workers compensation line read 2026-09-16: {read['wc']}.",
                "source": source_id,
                "excerpt": read["wc"],
            },
        ],
        "license": {
            "number": read["lic"],
            "status": read["status"],
            "entity": read["entity"],
            "expires": iso(read["expires"]),
            "classes": read["classes"],
            "source": source_id,
            "checkedAt": DATE,
        },
        "reviewIds": [],
        "platformLinks": [],
        "flags": [],
        "gaps": [],
        "priority": None,
        "rationale": (
            f"Wave-16 direct regulator read. Licence {read['lic']} was opened and transcribed at CSLB on 2026-09-16 "
            "after the City permit-contact row surfaced the number. The record is held: no attributable review of a "
            "seized overflow or a ceiling opening, no project insurance confirmation and no written repair-first scope "
            "were joined to it."
        ),
        "nextStep": (
            "Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset "
            "dispatch, project insurance and a written repair-first scope with a stop-and-review point."
        ),
        "exactMatch": False,
        "insuranceVerified": False,
        "scopeConfirmed": False,
        "master": False,
    }
    if read["status"] == "active":
        record["flags"].append(
            {
                "level": "hold",
                "text": (
                    f"Active licence {read['lic']} ({classes}) read directly at CSLB, but the promotion gates for "
                    "Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are "
                    "not satisfied, so the record stays out of the qualified master."
                ),
                "sources": [source_id],
            }
        )
    else:
        record["flags"].append(
            {
                "level": "hold",
                "text": (
                    f"CSLB status for licence {read['lic']} was read as {read['status']}. A licence that is not current "
                    "and active cannot be contracted on, so the record is held and never promoted."
                ),
                "sources": [source_id],
            }
        )
    if read.get("liability"):
        record["claims"].append(
            {
                "field": "Liability insurance",
                "text": f"CSLB liability line read 2026-09-16: {read['liability']}.",
                "source": source_id,
                "excerpt": read["liability"],
            }
        )
    if ten_digits(read["phone"]) in STORED_PHONES:
        record["phone"] = None
        record["phoneSource"] = None
        record["flags"].append(
            {
                "level": "discrepancy",
                "text": (
                    f"CSLB prints {read['phone']} for licence {read['lic']}, but the same ten digits are already "
                    "stored against a different record in this dataset. The number is left unstored so two licence "
                    "identities are not merged by a shared phone line."
                ),
                "sources": [source_id, registry_id],
            }
        )
    for note in read["notes"]:
        level = "hold" if ("suspension" in note or "revoked" in note or "not able to contract" in note
                           or "inactive" in note) else "discrepancy" if (
            "prints" in note or "differs" in note or "while" in note or "irregularity" in note
        ) else "note"
        record["flags"].append({"level": level, "text": note, "sources": [source_id, registry_id]})
    record["flags"].append(
        {
            "level": "gap",
            "text": (
                "No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence "
                "identity in the evidence read on 2026-09-16."
            ),
            "sources": [source_id, registry_id, 666, 667, 669, 672],
        }
    )
    record["gaps"] = [
        "No review or job record describes a seized bathtub overflow linkage on this exact licence.",
        "No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.",
        "No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.",
    ]
    BUSINESSES.append(record)

for slug, name, address, rows in REGISTRY_LEADS:
    BUSINESSES.append(
        {
            "id": f"w16-reg-{slug}",
            "name": name,
            "trade": "registry-lead",
            "website": None,
            "websiteSource": None,
            "area": "sunset",
            "areaText": (
                f"The official building-permit contact registry prints this firm at {address}, San Francisco, 94122 "
                f"across {rows} grouped rows. This is historical registry evidence, not current Outer Sunset dispatch."
            ),
            "status": "hold",
            "checkedAt": DATE,
            "phone": None,
            "phoneSource": None,
            "claims": [
                {
                    "field": "Registry",
                    "text": (
                        f"Registry-recorded building contact read 2026-09-16: firm '{name}', address {address}, "
                        f"ZIP 94122, across {rows} grouped rows. The rows carry no licence number."
                    ),
                    "source": 665,
                    "excerpt": f"{name} - {address} - 94122 - {rows} rows - licence field empty",
                }
            ],
            "license": None,
            "reviewIds": [],
            "platformLinks": [],
            "flags": [
                {
                    "level": "hold",
                    "text": (
                        "Registry only: the City row records no licence number and no CSLB page was opened, so no legal "
                        "entity, status, classification or expiry is asserted."
                    ),
                    "sources": [665],
                },
                {
                    "level": "gap",
                    "text": (
                        "The registry does not say which trade was performed under these permit rows, and a permit "
                        "contact row is not proof that a given firm performed a given scope."
                    ),
                    "sources": [665],
                },
                {
                    "level": "gap",
                    "text": (
                        "No attributable Yelp, Thumbtack, Reddit or directory review was matched to this registry "
                        "identity in the evidence read on 2026-09-16."
                    ),
                    "sources": [665, 666, 667, 669, 672],
                },
            ],
            "gaps": [
                "No licence number in the City row and no direct CSLB read, so status and classification are unknown.",
                "No current dispatch, exact overflow, ceiling-restoration, insurance or written repair-first evidence.",
            ],
            "priority": None,
            "rationale": (
                "Wave-16 registry-tier discovery record. A firm name, an Outer Sunset address and a row count are "
                "retained as a lead so the licence can be looked up later; nothing about licensing or scope is assumed."
            ),
            "nextStep": (
                "Look the firm up at CSLB and match the legal name and address before any contact; then verify dispatch, "
                "insurance and scope in writing."
            ),
            "exactMatch": False,
            "insuranceVerified": False,
            "scopeConfirmed": False,
            "master": False,
        }
    )

for item in PLATFORM:
    review_ids = [item["review"]] if item.get("review") else []
    record = {
        "id": f"w16-plat-{item['slug']}",
        "name": item["name"],
        "trade": "platform-listing",
        "website": None,
        "websiteSource": None,
        "area": item["area"],
        "areaText": (
            "The listing appears in a search or category scoped to Outer Sunset or San Francisco. That is a platform "
            "service-area statement, not verified Outer Sunset dispatch."
            if item["area"] == "sunset"
            else "The listing appears in a San Francisco service category. That is a platform service-area statement, "
            "not verified Outer Sunset dispatch."
        ),
        "status": "hold",
        "checkedAt": DATE,
        "phone": None,
        "phoneSource": None,
        "claims": [
            {
                "field": "Community thread" if item["platform"] == "Reddit" else "Platform listing",
                "text": f"{item['listing']}",
                "source": item["source"],
                "excerpt": f"{item['name']} - {item['text']}",
            }
        ],
        "license": None,
        "reviewIds": review_ids,
        "platformLinks": [{"label": item["label"], "url": item["url"], "source": item["source"]}],
        "flags": [
            {
                "level": "hold",
                "text": (
                    "Platform or community listing only: no CSLB licence number was published or read for this record. "
                    "A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact."
                ),
                "sources": [item["source"]],
            },
            {
                "level": "gap",
                "text": (
                    "Nothing in the listing names a seized bathtub overflow linkage, a concealed 1940s-era assembly, a "
                    "ceiling opening, drywall closeout or an installed access hatch."
                ),
                "sources": [item["source"]],
            },
            {
                "level": "gap",
                "text": (
                    "No Outer Sunset address, dispatch radius, project insurance or written repair-first scope was "
                    "confirmed for this listing on 2026-09-16."
                ),
                "sources": [item["source"]],
            },
        ],
        "gaps": [
            "No CSLB legal identity, status or classification verified.",
            "No exact-task outcome, project insurance or written repair-first scope.",
        ],
        "priority": None,
        "rationale": (
            "Wave-16 platform-tier discovery record. The listing and any excerpt are retained verbatim but a listing "
            "cannot meet a licence or qualification gate, so the record is held."
        ),
        "nextStep": (
            "Obtain the exact CSLB number and legal entity, check both at CSLB, then verify Outer Sunset dispatch, "
            "insurance and scope in writing."
        ),
        "exactMatch": False,
        "insuranceVerified": False,
        "scopeConfirmed": False,
        "master": False,
    }
    if item.get("self_promo"):
        record["flags"].append(
            {
                "level": "discrepancy",
                "text": (
                    "The recommending username matches the firm name, so the comment reads as self-promotion and is not "
                    "treated as independent review evidence."
                ),
                "sources": [item["source"]],
            }
        )
    if item.get("mismatch"):
        record["flags"].append(
            {
                "level": "discrepancy",
                "text": (
                    "The retained excerpt does not describe the category the card appears in; the excerpt is quoted "
                    "exactly as published and is not read as evidence of the missing scope."
                ),
                "sources": [item["source"]],
            }
        )
    BUSINESSES.append(record)

REVIEWS = []
for item in PLATFORM:
    if not item.get("review"):
        continue
    REVIEWS.append(
        {
            "id": item["review"],
            "business": f"w16-plat-{item['slug']}",
            "platform": item["platform"],
            "author": item["author"],
            "published": None,
            "quote": item["quote"],
            "analysis": (
                "Attributable excerpt about general repair or responsiveness. It does not describe a seized overflow "
                "linkage, an original concealed assembly, a ceiling opening, drywall closeout or an Outer Sunset job, "
                "so it is retained without any exact-task credit."
            ),
            "theme": item["theme"],
            "source": item["source"],
            "access": "search-extract" if item["platform"] in {"Yelp", "Reddit"} else "page",
            "identity": "unverified-username" if item["platform"] == "Reddit" else "indexed",
            "negative": False,
            "checkedAt": DATE,
            "exactTask": False,
        }
    )


def main() -> int:
    data = json.loads(RESEARCH.read_text(encoding="utf-8"))
    old_names = {re.sub(r"[^a-z0-9]+", " ", b["name"].lower()).strip() for b in data["businesses"]}
    drop = {"inc", "incorporated", "llc", "co", "company", "corp", "corporation", "construction",
            "contractor", "contractors", "general", "dba"}
    old_cores = {
        " ".join(t for t in re.sub(r"[^a-z0-9]+", " ", b["name"].lower()).strip().split() if t not in drop)
        for b in data["businesses"]
    }
    collisions = [
        b["name"] for b in BUSINESSES
        if re.sub(r"[^a-z0-9]+", " ", b["name"].lower()).strip() in old_names
        or " ".join(
            t for t in re.sub(r"[^a-z0-9]+", " ", b["name"].lower()).strip().split() if t not in drop
        ) in old_cores
    ]
    if collisions:
        raise SystemExit(f"wave 16 name collisions before writing: {collisions}")
    if len(BUSINESSES) != 50 or len({b["id"] for b in BUSINESSES}) != 50:
        raise SystemExit("wave 16 must carry exactly 50 unique records")

    active = [b for b in BUSINESSES if b.get("license") and b["license"]["status"] == "active"]
    non_active = [b for b in BUSINESSES if b.get("license") and b["license"]["status"] != "active"]
    composition = {
        "cslbReads": len(CSLB_READS),
        "registryOnly": len(REGISTRY_LEADS),
        "platformListings": len(PLATFORM),
        "activeLicenses": len(active),
        "nonActiveLicenses": len(non_active),
        "retainedReviewExcerpts": len(REVIEWS),
        "verificationPasses": 3,
    }
    artifact = {
        "wave": 16,
        "date": DATE,
        "schemaVersion": 2,
        "note": (
            "Wave 16 adds 50 genuinely new, collision-vetted records: 25 direct CSLB licence reads, 10 City "
            "building-permit contact rows in 94122 with no licence number, and 15 platform or community listings. "
            "All are held; the qualified master stays empty."
        ),
        "composition": composition,
        "sources": SOURCES,
        "businesses": BUSINESSES,
        "reviews": REVIEWS,
    }
    TARGET.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wave 16 written: {len(BUSINESSES)} records, {len(SOURCES)} sources, {len(REVIEWS)} reviews")
    print(f"composition: {composition}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
