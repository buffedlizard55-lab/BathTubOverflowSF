#!/usr/bin/env python3
"""Generate Wave 14: 25 direct CSLB reads, 20 registry leads and 5 platform listings.

The facts in this artifact were read on 2026-09-16. The generator treats the
City permit-contact registries as discovery evidence only: a licence number in
a registry row is never converted into a licence fact unless the matching CSLB
LicenseDetail page was opened and transcribed. Every new identity is compared
with the live pre-wave-14 corpus before the artifact is written.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "wave14.json"
RESEARCH = ROOT / "data" / "research.json"
DATE = "2026-09-16"
CSLB = "https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum="
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


# Values in ``registry_*`` are copied from the official k6kv-9kix roll-up.
# Values in every other field are copied from the matching CSLB page. A changed
# legal entity is therefore printed under the current regulator name, with the
# historical City name retained as a discrepancy rather than silently merged.
READS = [
    dict(lic="765149", name="H2Pro Inc", registry_name="Emb Plumbing", trade="multi-trade",
         classes=["B", "C-4", "C36"], status="expired", expires="2022-07-31",
         entity_form="Corporation", issued="06/30/1999", reissued="07/30/2008",
         address="1282 Chase Road, Veazie, ME 04401", phone="2072498806",
         registry_address="1211 Ramsel Ct B, San Francisco, CA 94122-0000",
         registry_phone="4159483670", registry_rows=15,
         insurance="Contractor bond cancelled 03/01/2017; displayed workers' compensation policy expired 07/23/2009.",
         special="CSLB says the licence was reissued to another entity on 07/30/2008. The current H2PRO INC identity does not match the registry's historical EMB PLUMBING name."),
    dict(lic="917633", name="Elite Engineering Contractors", registry_name="Elite Engineering Contractors", trade="general",
         classes=["A", "B"], status="active", expires="2028-06-30",
         entity_form="Sole Ownership", issued="06/16/2008", address="1875 25th Avenue, San Francisco, CA 94122",
         phone="4157285086", registry_address="1875 25th Avenue, San Francisco, CA 94122-0000",
         registry_phone="4157285086", registry_rows=15,
         insurance="Contractor bond $25,000 effective 06/25/2025; displayed workers' compensation policy expired 08/03/2026.",
         special="The licence remains current and active, but the workers' compensation line displayed on the page expired before this check. Current crew coverage must be established separately."),
    dict(lic="912166", name="Good Neighbor Construction", registry_name="Good Neighbor Construction", trade="general",
         classes=["B"], status="active", expires="2028-03-31",
         entity_form="Sole Ownership", issued="03/11/2008", address="380 Vallejo Dr 227, Millbrae, CA 94030",
         phone="4156808817", registry_address="1917 Judah St, San Francisco, CA 94122-0000",
         registry_phone="4156808817", registry_rows=21,
         insurance="Contractor bond $25,000 effective 09/01/2026; displayed workers' compensation policy expires 04/28/2027.",
         special="CSLB now records Millbrae while the City registry retains a 1917 Judah Street firm address. The registry row is historical area evidence, not present dispatch proof."),
    dict(lic="693830", name="KNJ General Construction", registry_name="K N J General Construction", trade="general",
         classes=["B"], status="active", expires="2027-12-31",
         entity_form="Sole Ownership", issued="08/03/1994", address="1800 Taraval St 16154, San Francisco, CA 94116",
         phone="4155664151", registry_address="1654 31st Av, San Francisco, CA 94122-0000",
         registry_phone="4157400043", registry_rows=14,
         insurance="Contractor bond $25,000 effective 09/01/2026; workers' compensation exemption (no employees) effective 12/02/2025.",
         special="The CSLB page links to complaint-disclosure information and notes a disciplinary bond requirement dated 01/21/2005. The disclosure page was not read, so no allegation is summarized and the record is held."),
    dict(lic="950296", name="C & M Development and Construction Inc", registry_name="C&M Development & Construction Inc", trade="general",
         classes=["B"], status="expired", expires="2024-07-31",
         entity_form="Corporation", issued="07/22/2010", address="870 Junipero Serra Blvd, San Francisco, CA 94127",
         phone="4154980327", registry_address="2034 Lawton St, San Francisco, CA 94122-0000",
         registry_phone="4157302508", registry_rows=14,
         insurance="Contractor bond cancelled 03/06/2022; workers' compensation exemption cancelled 02/11/2021.",
         special="CSLB says the expired licence must resolve an outstanding civil judgment before renewal or reactivation. The current CSLB phone differs from the City registry phone."),
    dict(lic="756611", name="Cheng Chang Construction Co", registry_name="Cheng Chang Construction", trade="general",
         classes=["B"], status="active", expires="2026-11-30",
         entity_form="Sole Ownership", issued="11/25/1998", address="341 Sebastian Drive, Millbrae, CA 94030",
         phone="4158129898", registry_address="1322 20th Av, San Francisco, CA 94122-0000",
         registry_phone="4158129898", registry_rows=14,
         insurance="Contractor bond $25,000 effective 09/01/2026; displayed workers' compensation policy expires 05/23/2027.",
         special="The active licence expires in 75 days and CSLB now records Millbrae. Recheck status and dispatch immediately before relying on it."),
    dict(lic="466541", name="Chih Jin Wen", registry_name="Constant Construction", trade="general",
         classes=["B"], status="expired", expires="2021-04-30",
         entity_form="Sole Ownership", issued="12/04/1984", reissued="04/05/1999",
         address="101 South Hill Blvd, San Francisco, CA 94112", phone="4159921327",
         registry_address="1356 20th Av, San Francisco, CA 94122-0000", registry_phone="4158196362", registry_rows=13,
         insurance="Contractor bond cancelled 09/07/2023; workers' compensation exemption remains displayed with no expiry.",
         special="CSLB prints CHIH JIN WEN, not the registry's CONSTANT CONSTRUCTION name, and both address and phone differ. The historical alias is not assumed to be a current business identity."),
    dict(lic="706442", name="Martin Mar Construction Co", registry_name="Martin T J Mar", trade="general",
         classes=["B", "C51"], status="expired", expires="2001-05-31",
         entity_form="Sole Ownership", issued="05/11/1995", address="2433 Moraga St, San Francisco, CA 94122",
         phone="4156610634", registry_address="2433 Moraga St, San Francisco, CA 94122",
         registry_phone="4156610634", registry_rows=13,
         insurance="Contractor bond cancelled 01/30/2002; workers' compensation exemption is displayed with no expiry.",
         special="The licence expired in 2001. C51 structural steel is retained as a real class but does not expand this record into plumbing or drywall evidence."),
    dict(lic="658187", name="Shun Construction", registry_name="Shun Construction / Lin Xi Shun", trade="general",
         classes=["B"], status="revoked", expires="2019-06-17",
         entity_form="Sole Ownership", issued="11/09/1992", address="4828 California Street, San Francisco, CA 94118-1113",
         phone="4157224828", registry_address="1474 46th Ave, San Francisco, CA 94122",
         registry_phone="4153878112", registry_rows=15,
         insurance="Contractor bond cancelled 01/06/2018; workers' compensation exemption is displayed with no expiry.",
         special="The licence is revoked and the page links to complaint-disclosure information. The City registry splits 15 rows across SHUN CONSTRUCTION and LIN XI SHUN with two phones."),
    dict(lic="809529", name="Da Chung Incorporated", registry_name="Da Chung Incorporated", trade="general",
         classes=["B"], status="active", expires="2028-06-30",
         entity_form="Corporation", issued="06/17/2002", address="36 Miriam St, Daly City, CA 94014",
         phone="4153857206", registry_address="1675 30th Av, San Francisco, CA 94122-0000",
         registry_phone="4153857206", registry_rows=8,
         insurance="Contractor bond $25,000 effective 04/25/2025; displayed workers' compensation policy expires 10/19/2026.",
         special="CSLB now records Daly City. The displayed compensation policy expires 33 days after this check; current coverage and Outer Sunset dispatch need a fresh written check."),
    dict(lic="849492", name="Mallard Construction", registry_name="Mallard Construction", trade="general",
         classes=["B"], status="active", expires="2026-11-30",
         entity_form="Sole Ownership", issued="11/06/2004", address="1519 26th Avenue, San Francisco, CA 94122",
         phone="4154071507", registry_address="1519 26th Avenue, San Francisco, CA 94122-0000",
         registry_phone="4154071507", registry_rows=8,
         insurance="Contractor bond $25,000 effective 01/01/2023; workers' compensation exemption (no employees) effective 11/03/2024.",
         special="A BuildZoom page combines licence 849492 with an Orange, California contractor, a 760 phone and two other licence numbers. That directory identity conflict is unresolved; CSLB controls the licence facts stored here."),
    dict(lic="690708", name="New United Construction", registry_name="New United Construction", trade="general",
         classes=["B"], status="expired", expires="1996-06-30",
         entity_form="Sole Ownership", issued="06/20/1994", address="1635 23rd Avenue, San Francisco, CA 94122",
         phone="4156657328", registry_address="1635 23rd Avenue, San Francisco, CA 94122",
         registry_phone="7319182", registry_rows=8,
         insurance="Contractor bond cancelled 07/07/1996; workers' compensation exemption is displayed with no expiry.",
         special="The licence expired in 1996. The registry prints only a seven-digit phone, which is not promoted into the contact field."),
    dict(lic="653045", name="The Bay Construction Company", registry_name="The Bay Construction Co", trade="general",
         classes=["B"], status="active", expires="2028-08-31",
         entity_form="Partnership", issued="08/26/1992", address="2029 Kirkham Street, San Francisco, CA 94122",
         phone="4152037398", registry_address="2029 Kirkham Street, San Francisco, CA 94122",
         registry_phone="4152037398", registry_rows=19,
         insurance="Contractor bond $25,000 effective 09/01/2026; workers' compensation exemption (no employees) effective 09/02/2026.",
         special="BuildZoom still prints 'Inactive when we last checked' while CSLB reads current and active on 09/16/2026. The stale directory status is flagged; no BuildZoom customer reviews were available."),
    dict(lic="749693", name="J N Pacific Construction Co", registry_name="J N Pacific Construction", trade="multi-trade",
         classes=["B", "C36"], status="active", expires="2028-05-31",
         entity_form="Sole Ownership", issued="05/19/1998", address="768 Brannan St, Suite 200, San Francisco, CA 94103",
         phone="6508261190", registry_address="1271 39th Av, San Francisco, CA 94122-0000",
         registry_phone="6505529648", registry_rows=7,
         insurance="Contractor bond $25,000 effective 01/22/2025; workers' compensation exemption (no employees) effective 04/06/2026.",
         special="This is the wave's only active direct read with both B and C36. CSLB now records 94103 and a different phone; the 94122 registry row is historical, and no exact overflow or ceiling-restoration outcome was found."),
    dict(lic="769813", name="P E I Construction Inc", registry_name="Bo Zhong Construction", trade="general",
         classes=["B"], status="canceled", expires="2013-12-10",
         entity_form="Corporation", issued="10/06/1999", reissued="01/14/2010",
         address="1759 33rd Avenue, San Francisco, CA 94122", phone="4159909431",
         registry_address="1759 33rd Av, San Francisco, CA 94122-0000", registry_phone="4157538673", registry_rows=7,
         insurance="Contractor bond cancelled 02/14/2013; displayed workers' compensation policy expired 12/01/2012.",
         special="CSLB says this licence was reissued to another entity twice and the corporation dissolved 12/10/2013. The current printed P E I identity differs from the registry's BO ZHONG CONSTRUCTION name."),
    dict(lic="667991", name="Custom Concepts", registry_name="Custom Concepts", trade="general",
         classes=["B"], status="expired", expires="2025-03-31",
         entity_form="Sole Ownership", issued="03/24/1993", address="1251 31st Avenue, San Francisco, CA 94122",
         phone="4157252449", registry_address="1255 31st Av, San Francisco, CA 94122-0000",
         registry_phone="4157316596", registry_rows=7,
         insurance="Contractor bond cancelled 03/07/2025; workers' compensation exemption is displayed with no expiry.",
         special="The licence is expired. Registry and regulator differ by four street numbers and publish different phones."),
    dict(lic="377610", name="Wong Construction Inc", registry_name="Wong's Construction Co", trade="general",
         classes=["B"], status="active", expires="2028-09-30",
         entity_form="Corporation", issued="06/15/1979", reissued="09/17/2014",
         address="800 Morningside Dr, Millbrae, CA 94030", phone="4153702335",
         registry_address="1782 9th Avenue, San Francisco, CA 94122", registry_phone="4155669683", registry_rows=7,
         insurance="Contractor bond $25,000 effective 01/01/2023; displayed workers' compensation policy expires 08/21/2027.",
         special="CSLB's compensation codes include wallboard installation, but CSLB says it does not verify those codes. That adjacent signal is not a C-9 classification or proof of the required ceiling work."),
    dict(lic="839263", name="Mc Eleney Construction", registry_name="Mc Eleney Construction", trade="general",
         classes=["B"], status="expired", expires="2010-05-31",
         entity_form="Sole Ownership", issued="05/26/2004", address="1646 27th Avenue, San Francisco, CA 94122",
         phone="4156064866", registry_address="1646 27th Av, San Francisco, CA 94122-0000",
         registry_phone="4156064866", registry_rows=7,
         insurance="Contractor bond cancelled 11/23/2008; workers' compensation exemption is displayed with no expiry.",
         special="The licence expired in 2010 and cannot contract."),
    dict(lic="413998", name="Sunset Electric Construction Inc", registry_name="Sunset Electric & Const", trade="scope-exclusion",
         classes=["C10"], status="canceled", expires="2019-04-23",
         entity_form="Corporation", issued="11/16/1981", reissued="05/30/2017",
         address="2078 36 Ave, San Francisco, CA 94416", phone="4159729983",
         registry_address="1547 26th Ave, San Francisco, CA 94122", registry_phone="4155665665", registry_rows=13,
         insurance="Contractor bond cancelled 04/25/2018; workers' compensation policy cancelled 01/08/2018.",
         special="The cancelled licence is C10 electrical only. CSLB prints San Francisco with ZIP 94416, an internal city/ZIP inconsistency, and the City registry carries a different address and phone."),
    dict(lic="614864", name="Excelsior Construction", registry_name="Excelsior Construction", trade="general",
         classes=["B"], status="revoked", expires="2007-03-05",
         entity_form="Sole Ownership", issued="03/13/1991", address="1874 31st Street, San Francisco, CA 94122",
         phone="4155641822", registry_address="1874 31st Avenue, San Francisco, CA 94122",
         registry_phone="4156817944", registry_rows=12,
         insurance="Contractor bond cancelled 03/01/2007; workers' compensation policy cancelled 01/17/2007.",
         special="The licence is revoked and the page links to complaint-disclosure information. Street suffix and phone differ between regulator and registry."),
    dict(lic="787392", name="Castle Builders Co", registry_name="Castle Builder Co", trade="general",
         classes=["B"], status="expired", expires="2023-12-31",
         entity_form="Sole Ownership", issued="11/15/2000", reissued="12/24/2012",
         address="1870 16th Avenue, San Francisco, CA 94122", phone="4159632079",
         registry_address="1870 16th Av, San Francisco, CA 94122-0000", registry_phone="4159632079", registry_rows=12,
         insurance="Contractor bond cancelled 02/05/2023; workers' compensation exemption is displayed with no expiry.",
         special="The licence is expired and CSLB says a legal requirement may have to be met before renewal or reactivation."),
    dict(lic="483659", name="Z M General Contractor", registry_name="Z M General Contractor", trade="multi-trade",
         classes=["B", "C10", "C36"], status="inactive", expires="2029-12-31",
         entity_form="Sole Ownership", issued="12/05/1985", address="765 Victoria St, San Francisco, CA 94127",
         phone="4152698078", registry_address="1610 41st Ave, San Francisco, CA 94122", registry_phone="4155662637", registry_rows=12,
         insurance="Contractor bond cancelled 11/03/2005; displayed workers' compensation policy expired 07/27/2012.",
         special="The licence has B, C10 and C36 but is inactive and cannot contract. Current regulator address and phone differ from the historical 94122 registry row."),
    dict(lic="964968", name="I W Construction", registry_name="I W Construction", trade="general",
         classes=["B"], status="inactive", expires="2029-08-31",
         entity_form="Sole Ownership", issued="08/26/2011", address="1706 48th Avenue, San Francisco, CA 94122",
         phone="4158285211", registry_address="1706 48th Av, San Francisco, CA 94122-0000", registry_phone="4158285211", registry_rows=12,
         insurance="Contractor bond cancelled 09/07/2024; workers' compensation exemption cancelled 11/27/2025.",
         special="The licence was inactivated after its workers' compensation exemption was cancelled and is not able to contract."),
    dict(lic="407633", name="Tony Oei", registry_name="Coast Pacific Properties", trade="multi-trade",
         classes=["C36", "B"], status="expired", expires="2024-07-31",
         entity_form="Sole Ownership", issued="06/24/1981", reissued="07/02/2014",
         address="2054 Sloat Blvd, San Francisco, CA 94116", phone="4157531643",
         registry_address="2319 Noriega Street, San Francisco, CA 94122", registry_phone="4155645626", registry_rows=12,
         insurance="Contractor bond cancelled 09/25/2021; workers' compensation exemption cancelled 08/01/2020.",
         special="CSLB prints TONY OEI while the City registry prints COAST PACIFIC PROPERTIES. The expired credential is not assigned to the registry business by assumption."),
    dict(lic="667984", name="Soon Yu Construction", registry_name="Soon Yu Construction", trade="general",
         classes=["B"], status="active", expires="2027-03-31",
         entity_form="Sole Ownership", issued="03/24/1993", address="2926 Judah Street, San Francisco, CA 94122",
         phone="4156645579", registry_address="2926 Judah St, San Francisco, CA 94122-0000", registry_phone="4156645579", registry_rows=12,
         insurance="Contractor bond $25,000 effective 02/24/2025; workers' compensation exemption (no employees) effective 04/23/2025.",
         special="BuildZoom matches this licence and reports 22 permit projects but no customer reviews. An indexed 94122 permit describes in-kind bathtub removal and replacement, not seized-overflow diagnosis."),
]

# Building-permit contacts remain registry-only. Their licence numbers were not
# read at CSLB during this wave and therefore never enter the ``license`` field.
REGISTRY = [
    ("840805", "Christopher Gate Construction Inc", "Pobox 225232", "San Francisco", "94122-0000", 179),
    ("544201", "Advanced Design General Contractor", "3922 Kirkham St", "San Francisco", "94122-0000", 106),
    ("701012", "O'kane Construction Llc", "1842 21st Av", "San Francisco", "94122-0000", 81),
    ("984971", "Modern Craft Construction", "P O Box 22025", "San Francisco", "94122-0000", 73),
    ("819274", "Eignor Construction Inc.", "1032 Irving Street, Pmb# 905", "San Francisco", "94122-0000", 70),
    ("1038989", "Zarc Construction Inc", "1549 Noriega St", "San Francisco", "94122-0000", 66),
    ("587887", "Kelly Brother's Construction", "1319 22nd Av", "San Francisco", "94122-0000", 65),
    ("967336", "Tn Building", "1312 Ortega St", "San Francisco", "94122-0000", 61),
    ("1007052", "Pjd Construction Inc", "1856 29th Av", "San Francisco", "94122-0000", 58),
    ("519294", "Riley Construction Co", "1032 Irving St., #436 *", "San Francisco", "94122", 53),
    ("1004624", "Youda Builders Inc", "1500 18th Av", "San Francisco", "94122-0000", 53),
    ("952450", "Nancy Built Llc", "1656 18th Av", "San Francisco", "94122-0000", 50),
    ("1044068", "Tao's Construction Inc.", "1419 22nd Avenue", "San Francisco", "94122-0000", 47),
    ("750238", "North Beach Const.", "1443 21st Av", "San Francisco", "94122-0000", 46),
    ("452211", "K & J Construction Co.", "1459 24th Ave *", "San Francisco", "94122-0000", 46),
    ("542738", "Badger Construction", "1683 24th Av", "San Francisco", "94122", 46),
    ("857620", "Argo Construction Inc", "1227 39th Av", "San Francisco", "94122-0000", 43),
    ("870223", "Xin Xin Construction", "1666 26th Av", "San Francisco", "94122-0000", 41),
    ("744592", "Artisana Painting", "500 Noriega St", "San Francisco", "94122-0000", 40),
    ("844980", "Tauscher Construction", "1416 34th Av", "San Francisco", "94122-0000", 38),
]

PLATFORM = [
    dict(key="rooter-hero-east-bay", name="Rooter Hero - East Bay", category="Thumbtack plumbers",
         summary="New on Thumbtack; serves San Francisco, CA; plumbing repair, inspection and fixture categories are listed.",
         url="https://www.thumbtack.com/ca/antioch/pro/thumbtack/service/579558043682717702", review=None),
    dict(key="ever-plumbing-underground", name="Ever Plumbing Underground", category="Thumbtack plumbers",
         summary="4.7 (133); Top Pro; 286 hires; serves San Francisco, CA; plumbing pipe repair is listed.",
         url="https://www.thumbtack.com/ca/san-jose/24-hour-plumbers/ever-plumbing-underground/service/447719536336732174",
         review=("Dina C.", "Fantastic plumber- super responsive and professional and does quality work.")),
    dict(key="mr-jimmy", name="Mr Jimmy Plumbing & Rooter", category="Thumbtack plumbers",
         summary="5.0 (30); Top Pro; platform 'Licensed pro' badge; 41 hires; one similar job shown near the search location.",
         url="https://www.thumbtack.com/ca/san-bruno/affordable-plumbing-services/mr-jimmy-plumbing-rooter-serious-inquiries/service/551031238488915971",
         review=("Kevin M.", "Jimmy's a great, honest plumber and gave me a very reasonable deal. I would highly recommend him to anyone looking for emergency plumbing.")),
    dict(key="i-rooter", name="I Rooter & Plumbing", category="Thumbtack plumbers review section",
         summary="A review-only appearance on the San Francisco plumber category page; no licence number or Outer Sunset dispatch statement is printed there.",
         url="https://www.thumbtack.com/ca/san-francisco/water-heater-installation/i-rooter-plumbing/service/357706607642730513",
         review=("Aly I.", "Great working with Dwayne. Don’t think twice about working with him. Best plumber I’ve worked with.")),
    dict(key="ag-quality", name="AG Quality Plumbing", category="Thumbtack plumbers review section",
         summary="A review-only appearance on the San Francisco plumber category page; no licence number or Outer Sunset dispatch statement is printed there.",
         url="https://www.thumbtack.com/ca/san-francisco/bathroom-remodeling/ag-quality-plumbing/service/246594380429837318",
         review=("Thumbtack Customer", "He is such a honest and good plumber. He solved my problem pretty quickly and guided me in the best way.")),
]


def source_url(dataset: str, field: str, numbers: list[str], select: str) -> str:
    """Build a grouped City-registry URL whose row counts can be reviewed."""
    where = f"{field} IN(" + ",".join(f"'{number}'" for number in numbers) + ")"
    return DBI + dataset + ".json?" + urlencode([
        ("$select", f"{select},count(*) as n"),
        ("$where", where),
        ("$group", select),
        ("$order", "n DESC"),
        ("$limit", "1000"),
    ])


def make_sources() -> list[dict]:
    sources = [
        {"id": 596, "kind": "government", "access": "page",
         "url": source_url("k6kv-9kix", "license_number", [r["lic"] for r in READS],
                           "license_number,firm_name,address,city,zipcode,phone"),
         "title": "SF DBI plumbing permit-contact rows for the 25 Wave 14 CSLB reads",
         "checkedAt": DATE,
         "note": "Read as an official City registry cross-check. These rows are historical contact evidence, not a current licence status, classification or dispatch confirmation."},
        {"id": 597, "kind": "government", "access": "page",
         "url": ("https://data.sf.gov/resource/3pee-9qhc.json?%24select="
                 "license1%2Cfirm_name%2Cfirm_address%2Cfirm_city%2Cfirm_zipcode%2Ccount%28%2A%29+as+n"
                 "&%24where=firm_zipcode+like+%2794122%25%27+AND+license1+is+not+null"
                 "&%24group=license1%2Cfirm_name%2Cfirm_address%2Cfirm_city%2Cfirm_zipcode"
                 "&%24order=n+DESC&%24limit=200"),
         "title": "SF DBI building-permit contact rows for the 20 Wave 14 registry-only leads",
         "checkedAt": DATE,
         "note": "Read line by line after the 94122 roll-up. No CSLB page was opened for these 20 numbers; the City rows are discovery evidence only."},
        {"id": 598, "kind": "platform", "access": "page",
         "url": "https://www.thumbtack.com/ca/san-francisco/drywall-repair",
         "title": "Thumbtack - drywall repairers near San Francisco",
         "checkedAt": DATE,
         "note": "Read all four chunks. The page displayed 17 top listings and a longer review panel; every attributable firm in that panel was already in the dataset, so none was recounted in Wave 14."},
        {"id": 599, "kind": "platform", "access": "page",
         "url": "https://www.thumbtack.com/ca/san-francisco/plumbers",
         "title": "Thumbtack - plumbers near San Francisco",
         "checkedAt": DATE,
         "note": "Read all four chunks. Category labels, ratings, hire counts, badges and review text remain platform claims; no badge is treated as a CSLB credential."},
        {"id": 600, "kind": "community", "access": "search-extract",
         "url": "https://www.reddit.com/r/AskSF/comments/171irdh/looking_for_a_contractor_in_or_near_sf_who_does/",
         "title": "Reddit /r/AskSF - looking for a contractor who does good drywall repair",
         "checkedAt": DATE,
         "note": "Direct fetch returned HTTP 403, so only the indexed extract was read. It repeated Paul Woodford Services and Sederap, both already stored; no review text was added or reconstructed."},
        {"id": 601, "kind": "platform", "access": "search-extract",
         "url": "https://www.yelp.com/search?find_desc=Drywall+Installation&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA",
         "title": "Yelp indexed search - drywall installation near Outer Sunset",
         "checkedAt": DATE,
         "note": "Search extract only. Results were checked against stored names and did not establish a new exact identity among the 50 Wave 14 records; inaccessible review text was not inferred."},
    ]
    for offset, row in enumerate(READS, start=602):
        sources.append({
            "id": offset, "kind": "government", "access": "page",
            "url": CSLB + row["lic"],
            "title": f"CSLB LicenseDetail - licence {row['lic']} - {row['name'].upper()}",
            "checkedAt": DATE,
            "note": "Opened directly on 2026-09-16. The page printed 'Data current as of 9/16/2026'; legal name, entity type, status, dates, classifications, contact and displayed bond/WC lines were transcribed field by field.",
        })
    sources.extend([
        {"id": 627, "kind": "directory", "access": "search-extract",
         "url": "https://www.buildzoom.com/contractor/the-bay-construction-company",
         "title": "BuildZoom - The Bay Construction Company",
         "checkedAt": DATE,
         "note": "Page and indexed extract checked. It identifies licence 653045, 31 projects and no customer reviews, but its stale 'inactive' label conflicts with the same-day active CSLB reading."},
        {"id": 628, "kind": "directory", "access": "search-extract",
         "url": "https://www.buildzoom.com/contractor/soon-yu-construction",
         "title": "BuildZoom - Soon Yu Construction",
         "checkedAt": DATE,
         "note": "Page and indexed extract checked. It matches licence 667984 and 22 projects, including a 2024 94122 in-kind bathtub replacement; the profile says it has received no customer reviews."},
        {"id": 629, "kind": "directory", "access": "page",
         "url": "https://www.buildzoom.com/contractor/mallard-construction-inc",
         "title": "BuildZoom - Mallard Construction Inc, Orange",
         "checkedAt": DATE,
         "note": "Read directly. It mixes licence 849492 with an Orange business, a 760 phone and licences 826607/578723; this is retained as an identity discrepancy, not merged into the CSLB entity."},
    ])
    return sources


def direct_record(row: dict, source_id: int) -> dict:
    direct_outer = "SAN FRANCISCO, CA 94122" in row["address"].upper()
    area = "outer" if direct_outer else "sunset"
    current = row["status"] == "active"
    status = "research" if current else "hold"
    if row["lic"] in {"917633", "693830", "849492"}:
        status = "hold"
    class_text = ", ".join(row["classes"])
    source_ids = [source_id, 596]
    flags = []
    if not current:
        flags.append({"level": "hold", "text": f"CSLB status is {row['status']}: this licence is not able to contract at this time.", "sources": [source_id]})
    elif row["trade"] == "general":
        flags.append({"level": "gap", "text": "The active licence is B general building only and has no C36 plumbing classification. Any pipe work requires a properly classified contractor; B is not treated as plumbing evidence.", "sources": [source_id]})
    if row["lic"] == "917633":
        flags.append({"level": "hold", "text": "The displayed workers' compensation policy expired 08/03/2026 even though CSLB still marks the licence active. Current applicable coverage is unresolved.", "sources": [source_id]})
    if row["lic"] == "693830":
        flags.append({"level": "hold", "text": "CSLB links complaint disclosure and notes a historical disciplinary-bond requirement; the disclosure page was not read, so this remains an unresolved blocking check rather than a summarized allegation.", "sources": [source_id]})
    if row["lic"] == "849492":
        flags.append({"level": "hold", "text": "BuildZoom combines this number with an Orange contractor and two other licence numbers. The directory identity conflict is unresolved and no directory evidence is merged into the CSLB entity.", "sources": [source_id, 629]})
        source_ids.append(629)
    if row["lic"] == "653045":
        flags.append({"level": "discrepancy", "text": "BuildZoom says 'Inactive when we last checked'; the same-day CSLB page is current and active. CSLB controls the status in this snapshot, while the stale directory label remains visible.", "sources": [source_id, 627]})
        source_ids.append(627)
    if row["lic"] == "667984":
        source_ids.append(628)
    if not direct_outer:
        flags.append({"level": "discrepancy", "text": f"Current CSLB address is {row['address']}; the City registry instead prints {row['registry_address']}. The 94122 row is historical area evidence, not current dispatch proof.", "sources": source_ids[:2]})
    flags.append({"level": "gap", "text": row["special"], "sources": source_ids})
    flags.append({"level": "gap", "text": "No attributable review establishes seized trip-lever/plunger extraction, repair-first preservation of an older assembly, ceiling access restoration or an access panel for this legal entity.", "sources": [source_id, 598, 599]})
    area_basis = (
        f"CSLB itself records the licensee at {row['address']}. This is a regulator-backed 94122 address, not confirmation that the business accepts this job."
        if direct_outer else
        f"The City registry records {row['registry_name']} at {row['registry_address']} across {row['registry_rows']} grouped permit-contact rows. CSLB now records {row['address']}; present Outer Sunset dispatch is unconfirmed."
    )
    return {
        "id": f"w14-{row['lic']}", "name": row["name"], "trade": row["trade"],
        "website": None, "websiteSource": None, "area": area, "areaText": area_basis,
        "status": status, "checkedAt": DATE, "phone": fmt_phone(row["phone"]), "phoneSource": source_id,
        "claims": [
            {"field": "CSLB credential",
             "text": f"Direct CSLB read 2026-09-16: {row['name'].upper()}, {row['entity_form']}, licence {row['lic']} is {row['status']}, expires {row['expires']}, classes {class_text}, address {row['address']}, phone {fmt_phone(row['phone'])}.",
             "source": source_id,
             "excerpt": f"This license is {row['status']}; {class_text}; {row['address']}; {fmt_phone(row['phone'])}"},
            {"field": "City registry cross-check",
             "text": f"SF DBI prints licence number {row['lic']} under '{row['registry_name']}' at {row['registry_address']} across {row['registry_rows']} grouped plumbing permit-contact rows"
                     + (f", phone {fmt_phone(row['registry_phone'])}." if len(digits(row['registry_phone'])) == 10 else "; its phone is incomplete and not stored as contact evidence."),
             "source": 596,
             "excerpt": f"{row['lic']} - {row['registry_name']} - {row['registry_address']} - {row['registry_rows']} rows"},
            {"field": "Displayed bond / workers' compensation",
             "text": row["insurance"] + " These regulator lines do not verify project-specific liability coverage.",
             "source": source_id, "excerpt": row["insurance"]},
        ],
        "license": {"number": row["lic"], "status": row["status"], "entity": row["name"].upper(),
                    "expires": row["expires"], "classes": row["classes"], "source": source_id, "checkedAt": DATE},
        "reviewIds": [],
        "platformLinks": ([{"label": "BuildZoom identity cross-check", "url": "https://www.buildzoom.com/contractor/mallard-construction-inc", "source": 629}] if row["lic"] == "849492" else
                          [{"label": "BuildZoom project/profile cross-check", "url": "https://www.buildzoom.com/contractor/the-bay-construction-company", "source": 627}] if row["lic"] == "653045" else
                          [{"label": "BuildZoom project/profile cross-check", "url": "https://www.buildzoom.com/contractor/soon-yu-construction", "source": 628}] if row["lic"] == "667984" else []),
        "flags": flags,
        "gaps": [
            "No verified current Outer Sunset dispatch commitment unless confirmed in writing; a 94122 address or historical City row is not acceptance of this job.",
            "No applicable project insurance certificate, written repair-first scope, exact difficult-overflow outcome or coordinated ceiling-restoration plan.",
        ],
        "priority": None, "rationale": "Wave-14 regulator-read record. Status, identity and classes come only from the matching CSLB page; City, directory and platform evidence stays visibly separate.",
        "nextStep": "If still eligible, verify the same legal entity and licence again, ask for a comparable older overflow job, current insurance and a written non-destructive-first scope before scheduling.",
        "exactMatch": False, "insuranceVerified": False, "scopeConfirmed": False, "master": False,
    }


def registry_record(row: tuple) -> dict:
    lic, name, address, city, zipcode, rows = row
    return {
        "id": f"w14-reg-{lic}", "name": name, "trade": "registry-lead",
        "website": None, "websiteSource": None, "area": "sunset",
        "areaText": f"The official building-permit contact registry prints this firm at {address}, {city}, {zipcode} across {rows} grouped rows. This is historical registry evidence, not current Outer Sunset dispatch.",
        "status": "hold", "checkedAt": DATE, "phone": None, "phoneSource": None,
        "claims": [{"field": "Registry",
                    "text": f"Registry-recorded building contact read 2026-09-16: licence1 {lic}, firm '{name}', address {address}, {city}, {zipcode}, across {rows} grouped rows.",
                    "source": 597, "excerpt": f"{lic} - {name} - {address} - {zipcode} - {rows} rows"}],
        "license": None, "reviewIds": [], "platformLinks": [],
        "flags": [
            {"level": "hold", "text": f"Registry only: licence1 {lic} was not opened at CSLB in this wave. No legal entity, current status, classification or expiry is asserted, so the row cannot satisfy a promotion gate.", "sources": [597]},
            {"level": "gap", "text": "The building registry does not identify drywall, plaster or plumbing classification and does not prove who performed any particular scope.", "sources": [597]},
            {"level": "gap", "text": "No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact registry identity in the accessible sample.", "sources": [597, 598, 599, 600, 601]},
        ],
        "gaps": [
            "No direct CSLB page read; status and classifications are unknown.",
            "No current dispatch, exact overflow, ceiling restoration, insurance or written repair-first evidence.",
        ],
        "priority": None, "rationale": "Wave-14 building-registry discovery lead. It is retained for drywall/general-building follow-up but carries no regulator-backed trade fact.",
        "nextStep": "Read the recorded CSLB number and reject it if inactive or if its classes do not cover the proposed work; then verify current service and scope in writing.",
        "exactMatch": False, "insuranceVerified": False, "scopeConfirmed": False, "master": False,
    }


def platform_record(row: dict, review_id: str | None) -> dict:
    record = {
        "id": f"w14-plat-{row['key']}", "name": row["name"], "trade": "platform-listing",
        "website": None, "websiteSource": None, "area": "sf",
        "areaText": "The listing appears on Thumbtack's San Francisco plumber category. That is a platform service-area statement, not verified Outer Sunset dispatch.",
        "status": "hold", "checkedAt": DATE, "phone": None, "phoneSource": None,
        "claims": [{"field": "Platform listing", "text": f"Thumbtack category read 2026-09-16: {row['summary']}",
                    "source": 599, "excerpt": f"{row['name']} - {row['summary']}"}],
        "license": None, "reviewIds": [review_id] if review_id else [],
        "platformLinks": [{"label": row["category"], "url": row["url"], "source": 599}],
        "flags": [
            {"level": "hold", "text": "Platform listing only: no CSLB licence number was published or read for this record. A 'Licensed pro' badge, when shown, is not a regulator fact.", "sources": [599]},
            {"level": "gap", "text": "The category does not name the Outer Sunset, a seized bathtub overflow, ceiling access or drywall/plaster closeout for this listing.", "sources": [599]},
        ],
        "gaps": [
            "No CSLB legal identity, status or classification verified.",
            "No exact-task outcome, project insurance or written repair-first scope.",
        ],
        "priority": None, "rationale": "Wave-14 platform-tier discovery record. The listing and any excerpt are retained verbatim but cannot meet a licence or qualification gate.",
        "nextStep": "Obtain and independently check the exact CSLB number and legal entity before considering the listing; verify Outer Sunset dispatch, insurance and scope in writing.",
        "exactMatch": False, "insuranceVerified": False, "scopeConfirmed": False, "master": False,
    }
    return record


def build() -> dict:
    live = json.loads(RESEARCH.read_text(encoding="utf-8"))
    sources = make_sources()
    businesses = [direct_record(row, 602 + index) for index, row in enumerate(READS)]
    businesses.extend(registry_record(row) for row in REGISTRY)
    reviews = []
    next_review = 159
    for row in PLATFORM:
        review_id = f"R{next_review}" if row["review"] else None
        record = platform_record(row, review_id)
        businesses.append(record)
        if row["review"]:
            author, quote_text = row["review"]
            reviews.append({
                "id": review_id, "business": record["id"], "platform": "Thumbtack", "author": author,
                "published": None, "quote": quote_text,
                "analysis": "Attributable platform excerpt about general plumbing responsiveness or quality. It does not describe a seized overflow mechanism, older concealed assembly, ceiling access, drywall restoration or an Outer Sunset job.",
                "theme": "General plumbing", "source": 599, "access": "page", "identity": "matched",
                "negative": False, "checkedAt": DATE, "exactTask": False,
            })
            next_review += 1

    if len(businesses) != 50 or len(READS) != 25 or len(REGISTRY) != 20 or len(PLATFORM) != 5:
        raise SystemExit("wave 14 composition is not 25 direct + 20 registry + 5 platform = 50")
    if len({b["id"] for b in businesses}) != 50:
        raise SystemExit("duplicate wave-14 id")
    if len({core(b["name"]) for b in businesses}) != 50:
        raise SystemExit("duplicate wave-14 normalized name core")

    stored_ids = {b["id"] for b in live["businesses"]}
    stored_names = {norm(b["name"]): b["id"] for b in live["businesses"]}
    stored_cores = {core(b["name"]): b["id"] for b in live["businesses"]}
    stored_licences = {str(b["license"]["number"]) for b in live["businesses"] if b.get("license")}
    stored_numbers = set(re.findall(r'(?<!\d)\d{6,7}(?!\d)', json.dumps(live)))
    stored_phones = {digits(b.get("phone")): b["id"] for b in live["businesses"] if len(digits(b.get("phone"))) == 10}
    wave_phones: dict[str, str] = {}
    for business in businesses:
        if business["id"] in stored_ids:
            raise SystemExit(f"stored id collision: {business['id']}")
        if norm(business["name"]) in stored_names or core(business["name"]) in stored_cores:
            owner = stored_names.get(norm(business["name"])) or stored_cores.get(core(business["name"]))
            raise SystemExit(f"stored name collision: {business['name']} -> {owner}")
        if business["license"] and business["license"]["number"] in stored_licences:
            raise SystemExit(f"stored licence-fact collision: {business['license']['number']}")
        # Registry-only numbers are also checked against all stored prose, because
        # a previous lead may have named the number without a licence object.
        claimed = business["license"]["number"] if business["license"] else business["id"].split("-")[-1]
        if claimed in stored_numbers:
            raise SystemExit(f"stored licence/registry number collision: {claimed}")
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
        "wave": 14, "date": DATE, "schemaVersion": 2,
        "note": "Wave 14 adds 50 genuinely new, collision-vetted records: 25 matching CSLB pages read directly, 20 building-registry-only leads and five current Thumbtack plumber listings. Both trade channels were searched; inaccessible or duplicate drywall results were logged rather than recounted. Nothing is promoted.",
        "composition": {
            "cslbReads": 25, "registryOnly": 20, "platformListings": 5,
            "activeLicenses": sum(row["status"] == "active" for row in READS),
            "nonActiveLicenses": sum(row["status"] != "active" for row in READS),
            "retainedReviewExcerpts": len(reviews), "verificationPasses": 3,
        },
        "sources": sources, "businesses": businesses, "reviews": reviews,
    }


if __name__ == "__main__":
    artifact = build()
    TARGET.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wave 14 written: {len(artifact['businesses'])} businesses, {len(artifact['sources'])} sources, {len(artifact['reviews'])} reviews")
