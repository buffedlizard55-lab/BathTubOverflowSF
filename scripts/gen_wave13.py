#!/usr/bin/env python3
"""Generate Wave 13 - 50 new records plus 12 verification upgrades.

Every fact below was read from the page named in its source on 2026-09-15:

* 26 CSLB ``LicenseDetail.aspx`` pages, one licence at a time -> new records
* 15 City and County of San Francisco open-data registry rows -> leads only
*  9 Thumbtack category listings -> platform claims only
* 12 further CSLB pages re-read for licences an earlier wave had stored, five of
  which close a gap the stored record itself published as "NOT read on CSLB"

The generator refuses to write the artifact when a stored record already uses the
same id, licence number or normalised name (except for the one published name
collision, which must declare itself), and it refuses any record that claims a
licence without a government CSLB source containing that number.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-15"
WAVE = 13
CSLB = "https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum="
DBI = "https://data.sf.gov/resource/"

# ---------------------------------------------------------------- sources ----
SOURCES = [
    {
        "id": 526, "kind": "government", "access": "page",
        "url": DBI + "k6kv-9kix.json?%24select=license_number%2Cfirm_name%2Caddress%2Czipcode%2Ccount(%2A)%20as%20n&%24where=address%20LIKE%20%27%25%27%20AND%20zipcode%20LIKE%20%2794122%25%27&%24group=license_number%2Cfirm_name%2Caddress%2Czipcode&%24order=n%20DESC&%24limit=100",
        "title": "SF DBI - permit-contact registry: every licence recorded against a 94122 firm address, ranked by permit rows",
        "checkedAt": DATE,
        "note": "Read in two windows (rows 1-50 and 51-150 of a count-ordered roll-up). A recorded firm address is a City record; it is never stored as a licence fact.",
    },
    {
        "id": 527, "kind": "government", "access": "page",
        "url": DBI + "k6kv-9kix.json?%24select=license_number%2Cfirm_name%2Caddress%2Czipcode%2Ccount(%2A)%20as%20n&%24where=license_number%20IN(&hellip;)&%24group=license_number%2Cfirm_name%2Caddress%2Czipcode&%24order=n%20DESC",
        "title": "SF DBI - per-licence detail rows behind the registry-only leads in this wave",
        "checkedAt": DATE,
        "note": "One grouped query per batch; only the IN list changes. Where one licence number returns two firm names or several addresses, both are published and flagged rather than resolved.",
    },
    {
        "id": 528, "kind": "government", "access": "page",
        "url": DBI + "a6aw-rudh.json?%24select=permit_number%2Cstreet_number%2Cstreet_name%2Cstreet_suffix%2Cdescription%2Cstatus%2Ccompleted_date%2Czipcode&%24where=zipcode%3D%2794122%27%20AND%20completed_date%3E%272025-06-01%27&%24order=completed_date%20DESC&%24limit=100",
        "title": "SF DBI - plumbing and mechanical permits at 94122 work addresses, completed since 2025-06-01",
        "checkedAt": DATE,
        "note": "Work-location ZIP is 94122. Scope text is quoted verbatim on every record; the dataset names the permit, not the crew.",
    },
    {
        "id": 529, "kind": "government", "access": "page",
        "url": DBI + "k6kv-9kix.json?%24select=permit_number%2Cfirm_name%2Clicense_number%2Caddress%2Ccity%2Czipcode%2Cphone&%24where=permit_number%20IN(94122-permit-numbers)&%24limit=100",
        "title": "SF DBI - permit-contact lookups for the 94122 permits joined in this wave",
        "checkedAt": DATE,
        "note": "One query per batch of permit numbers. Homeowner's Permit rows (licence 000001) were rejected, and the k6kv dataset is silent on the 2026 building permits with drywall scope, which is recorded as a finding.",
    },
    {
        "id": 530, "kind": "government", "access": "page",
        "url": DBI + "3pee-9qhc.json?%24select=license1%2Cfirm_name%2Cfirm_address%2Cfirm_zipcode%2Ccount(%2A)%20as%20n&%24where=firm_zipcode%20LIKE%20%2794122%25%27&%24group=license1%2Cfirm_name%2Cfirm_address%2Cfirm_zipcode&%24order=n%20DESC&%24limit=50",
        "title": "SF DBI - building-permit contact registry, every licence1 with a 94122 firm ZIP",
        "checkedAt": DATE,
        "note": "Older building permits only. Queried again for the 2025-2026 permit numbers used in this wave and returned no rows, so no contractor identity is inferred for them.",
    },
    {
        "id": 531, "kind": "government", "access": "page",
        "url": DBI + "i98e-djp9.json?%24select=permit_number%2Cstreet_number%2Cstreet_name%2Cstreet_suffix%2Cdescription%2Cstatus%2Cfiled_date&%24where=zipcode%3D%2794122%27%20AND%20filed_date%3E%272024-01-01%27%20AND%20(description%20LIKE%20%27%25drywall%25%27%20OR%20description%20LIKE%20%27%25sheetrock%25%27%20OR%20description%20LIKE%20%27%25ceiling%25%27%20OR%20description%20LIKE%20%27%25plaster%25%27)&%24order=filed_date%20DESC&%24limit=60",
        "title": "SF DBI - building permits at 94122 addresses naming drywall, sheetrock, ceiling or plaster",
        "checkedAt": DATE,
        "note": "Read to test whether a joinable second channel exists for drywall and ceiling work. It does not: these building permits appear in no dataset of permit contacts, so drywall scope cannot be attributed to a licence through City data in this wave.",
    },
    {"id": 532, "kind": "platform", "access": "page", "url": "https://www.thumbtack.com/ca/san-francisco/drywall-contractors",
     "title": "Thumbtack - drywall contractors serving San Francisco", "checkedAt": DATE,
     "note": "Category page read directly. Platform labels, hire counts and review text are the platform's own; no licence number is published for any listing shown."},
    {"id": 533, "kind": "platform", "access": "page", "url": "https://www.thumbtack.com/ca/san-francisco/drywall-repair",
     "title": "Thumbtack - drywall repair in San Francisco", "checkedAt": DATE,
     "note": "Category page read directly. Its own project menu names 'Ceiling(s)' and 'Renter, with owner's permission' as inputs, which is why the tier is retained for this project's conditions."},
    {"id": 534, "kind": "platform", "access": "page", "url": "https://www.thumbtack.com/ca/san-francisco/plumbers",
     "title": "Thumbtack - plumbers serving San Francisco", "checkedAt": DATE,
     "note": "Category page read directly; 89 pros listed. 'Licensed pro' is a platform badge with no licence number attached, so it is never stored as a licence fact."},
    {"id": 535, "kind": "platform", "access": "page", "url": "https://www.thumbtack.com/ca/san-francisco/ceiling-repair-companies",
     "title": "Thumbtack - ceiling repair professionals serving San Francisco", "checkedAt": DATE,
     "note": "Category page read directly; carried the lath-and-plaster specialists retained in this wave."},
    {"id": 537, "kind": "platform", "access": "page", "url": "https://www.thumbtack.com/ca/san-francisco/bathroom-remodeling",
     "title": "Thumbtack - bathroom remodelers serving San Francisco", "checkedAt": DATE,
     "note": "Category page read directly; 45 bathroom remodelers listed. Its own project menu distinguishes 'Renter, with owner's permission to do this job' from other ownership types, and lists full remodels, fixture replacement and water-damage repair."},
    {"id": 536, "kind": "platform", "access": "page", "url": "https://www.thumbtack.com/ca/san-francisco/ceiling-drywall-repair",
     "title": "Thumbtack - ceiling drywall repair in San Francisco", "checkedAt": DATE,
     "note": "Category page read directly. Its listed pros repeated the same four listings found on sources 532-535, so no separate record was created from it; the page is published as a source for that negative result."},
]

# ---------------------------------------------- CSLB reads: new records ------
READS = [
    dict(
        lic="843160", name="Lushov Construction Inc", trade="general", classes=["B", "A"],
        entity="LUSHOV CONSTRUCTION INC", form="Corporation",
        addr="750 La Playa Street Unit 865, San Francisco, CA 94121", phone="(510) 672-7450",
        issue="07/21/2004", reissue="01/23/2013", expire="2027-01-31", status="active",
        wc="exempt - certified no employees (01/10/2025)", bond="Contractor's bond on file",
        permit=("PP20260805660", "1447 33rd Av", "bathroom rmeodel: replace bathtub, shower tile and vanity.", "2026-09-14"),
        registry=("750 La Playa St, Unit 865", "San Francisco", "94121-0000", "5108277114"),
        extras=[
            ("discrepancy", "CSLB's own page carries a complaint-disclosure marker: 'There is Complaint Disclosure information for this license.' The disclosure page itself was NOT opened in this wave, so the record is held until it is read and the allegation transcribed."),
            ("gap", "CSLB records this licensee in ZIP 94121 (Richmond district), outside the Outer Sunset. The Outer Sunset link is the completed 94122 plumbing permit for a bathtub replacement."),
            ("gap", "Workers' compensation reads 'exempt - certified no employees', so the crew that would do a multi-trade job cannot be checked from this page."),
        ],
    ),
    dict(
        lic="1036851", name="Westgate Plumbing", trade="plumbing", classes=["C36"],
        entity="WESTGATE PLUMBING", form="Sole Ownership",
        addr="121 Quint Street Unit 5E, San Francisco, CA 94124", phone="(415) 515-3712",
        issue="03/15/2018", expire="2028-03-31", status="active",
        wc="Security National to 11/20/2026", bond="ACI 100383148, cancellation date 10/08/2026",
        permit=("PW20260331768", "1853 15th Av", "work category: 2pa; plumbing permit is pulled for 3 bathrooms. total of 3 toilets, 3 shower valves and drains, 3 lavatory sinks, and 1 tub.", "2026-07-28"),
        registry=("121 Quint St", "San Francisco", "94124-0000", "4152754057"),
        hold="The contractor's bond carries a cancellation date of 10/08/2026, three weeks after this check; CSLB suspends a licence when a bond lapses. Re-read before any deposit.",
        extras=[
            ("discrepancy", "Registry phone 415-275-4057 differs from the CSLB business phone (415) 515-3712. The CSLB reading is stored and the registry value is flagged."),
            ("gap", "C36 only: no B, B-2 or C-9, so ceiling drywall restoration on this project would need a second licensee."),
        ],
    ),
    dict(
        lic="1078954", name="Mission Home Remodeling Inc", trade="general", classes=["B"],
        entity="MISSION HOME REMODELING INC", form="Corporation",
        addr="475 Gough St, San Francisco, CA 94102", phone="(415) 813-0440",
        issue="07/29/2021", expire="2027-07-31", status="active",
        wc="on file to 07/31/2027", bond="on file",
        permit=("PP20260528270", "1663 42nd Av", "bathroom remodel, like for like, seperate tub and shower.", "2026-08-03"),
        registry=("475 Gough St", "San Francisco", "94102-0000", "4152159469"),
        name_collision="w12-mission-home-remodeling",
        extras=[
            ("discrepancy", "Near-name collision published rather than merged: wave 12 stored a platform record named 'Mission Home Remodeling' (id w12-mission-home-remodeling) with no address and no CSLB read. This record is the regulator's spelling, 'Mission Home Remodeling Inc', at 475 Gough St. The two are kept as separate records because the identity link is not verifiable from any source read so far."),
            ("discrepancy", "Registry phone 415-215-9469 differs from the CSLB business phone (415) 813-0440. Both readings are published and neither is assumed correct."),
            ("gap", "B only: the licence covers ceiling and wall restoration, not the plumbing repair behind it."),
        ],
    ),
    dict(
        lic="1067347", name="A2Z Remodeling Inc dba A2Z Kitchen & Bath", trade="general", classes=["B"],
        entity="A2Z REMODELING INC - dba A2Z KITCHEN & BATH", form="Corporation",
        addr="3291 Lakeshore Ave, Oakland, CA 94610", phone="(800) 476-9660",
        issue="07/28/2020", expire="2028-07-31", status="active",
        wc="on file", bond="on file",
        permit=("PP20260723391", "1510 07th Av", "kitchen & (3) bath remodel: bar addition, laundry relocation, remove ground floor bathroom. 2/f: add bar sink, replace shower w/tub combo, 3/f: full bath remodel like for like same floor plan, (1) shower pan.", "2026-08-10"),
        registry=("303 Twin Dolphin Drive, 6/F", "Redwood City", "94065-0000", "8004769660"),
        extras=[
            ("discrepancy", "The registry stores a Redwood City address for licence 1067347; CSLB records Oakland. Address conflict flagged, neither value silently preferred."),
            ("gap", "B only. The permit's scope is a three-bathroom remodel at an Outer Sunset address, which is the strongest local experience signal on this record and still says nothing about a seized trip lever."),
        ],
    ),
    dict(
        lic="1029472", name="Xteam Design Construction", trade="general", classes=["B"],
        entity="XTEAM DESIGN CONSTRUCTION", form="Sole Ownership",
        addr="168 S Lake Merced Hls, San Francisco, CA 94132", phone="(949) 300-3328",
        issue="07/28/2017", expire="2027-07-31", status="active",
        wc="exempt - certified no employees (07/25/2025)", bond="on file",
        permit=("PP20260121923", "1583 17th Av", "remodel exisrting kitchen, add 2 baths, 1 laudry room", "2026-09-02"),
        registry=("168 S Lake Merced Hills", "San Francisco", "94132-0000", "9493003328"),
        extras=[
            ("discrepancy", "CSLB's page carries the complaint-disclosure marker for this licence; the disclosure page itself was NOT opened in this wave and no allegation is transcribed."),
            ("gap", "B only, and workers' compensation is exempt (no employees certified) despite a two-bathroom permit at an Outer Sunset address."),
        ],
    ),
    dict(
        lic="1029997", name="O'Pro Construction Inc", trade="general", classes=["B"],
        entity="O'PRO CONSTRUCTION INC", form="Corporation",
        addr="229 Cloverbrook Circle, Pittsburg, CA 94565", phone="(415) 987-7373",
        issue="08/14/2017", expire="2027-08-31", status="active",
        wc="policy expires 09/22/2026", bond="on file",
        permit=("PP20260204207", "1696 08th Av", "remodel kitchen and 3 baths. 3 shower pans.", "2026-09-03"),
        registry=("229 Cloverbrook Circle", "Pittsburg", "94565-0000", "4159877373"),
        extras=[
            ("gap", "B only: three shower pans on the permit, no C-36 on the licence."),
            ("discrepancy", "The workers' compensation policy shown on the page expires 09/22/2026, one week after this check."),
        ],
    ),
    dict(
        lic="1058907", name="Olmec Builders Inc", trade="general", classes=["B"],
        entity="OLMEC BUILDERS INC", form="Corporation",
        addr="PO Box 318051, San Francisco, CA 94131", phone="(415) 420-2056",
        issue="10/03/2019", expire="2027-10-31", status="active",
        wc="code 86011 engineers-consulting", bond="on file",
        permit=("PP20260514080", "1739 40th Av", "re-plumbing kitchen sink.", "2026-09-02"),
        registry=("520 Roosevelt Wy", "San Francisco", "94114-0000", "6508733574"),
        extras=[
            ("discrepancy", "Registry address (520 Roosevelt Wy) and registry phone (650-873-3574) both differ from the CSLB address (PO Box 318051) and CSLB phone (415) 420-2056."),
            ("discrepancy", "Workers' compensation classification is 'engineers-consulting', which does not match construction trades."),
            ("gap", "B only, on a permit that re-plumbs a kitchen sink."),
        ],
    ),
    dict(
        lic="1074133", name="Katz Group", trade="general", classes=["B"],
        entity="KATZ GROUP", form="Corporation",
        addr="587 Castro Street, San Francisco, CA 94114", phone="(415) 757-0041",
        issue="03/19/2021", expire="2027-03-31", status="active",
        wc="codes 874017, 901519, 874104 shown as 'Description Unavailable'", bond="on file",
        permit=("PP20260617683", "1435 18th Av", "in-kind remodeling of 1 kitchen(s) in 3rd fl installing gas line.", "2026-09-08"),
        registry=("587 Castro St", "San Francisco", "94114-0000", "(no phone published on this registry row)"),
        extras=[
            ("notice", "The registry row for this permit publishes no phone number, so no phone conflict can be tested."),
            ("gap", "B only, and the workers' compensation classification codes are published without descriptions."),
        ],
    ),
    dict(
        lic="825060", name="K L Plumbing Inc", trade="plumbing", classes=["C36"],
        entity="K L PLUMBING INC", form="Corporation",
        addr="1926 Lawton Street, San Francisco, CA 94122", phone="(415) 668-1218",
        issue="09/26/2003", expire="2011-08-16", status="canceled",
        status_text="This license is canceled and not able to contract.",
        wc="not current", bond="not current",
        permit=None, registry=("94122 roll-up row; 50 permit rows",),
        name_collision="w7-k-l-plumbing",
        extras=[
            ("hold", "CSLB status reads 'canceled and not able to contract', and Miscellaneous Information records '08/16/2011 - SECRETARY OF STATE - DISSOLUTION': the corporation was dissolved, so this number cannot support a contract today."),
            ("notice", "The registered address is inside the Outer Sunset, which is exactly why the record is published and held rather than dropped: a good address is not a valid licence."),
            ("discrepancy", "Two licence numbers for one firm name and address: wave 7 stored 'K L Plumbing' (id w7-k-l-plumbing) at 1926 Lawton St against registry licence number 510452, while the registry roll-up read this wave prints licence number 825060 for 'K L Plumbing Inc' at the same Outer Sunset address on 50 permit rows. Both numbers are published and neither is assumed to be the trading entity's."),
        ],
    ),
    dict(
        lic="984413", name="Feng K Plumbing Corp dba Xin Feng Plumbing", trade="plumbing", classes=["C36"],
        entity="FENG K PLUMBING CORP - dba XIN FENG PLUMBING", form="Corporation",
        addr="1654 23rd Ave, San Francisco, CA 94122", phone="(415) 939-8822",
        issue="06/10/2013", expire="2027-06-30", status="active",
        wc="exempt - certified no employees (05/27/2025)", bond="on file",
        permit=None, registry=("94122 roll-up row; 46 permit rows (firm ZIP is 94122 in the registry filter)",),
        extras=[
            ("discrepancy", "Near-name collision on record: an earlier wave stored licence 839447 as 'Feng K Plumbing Co'. This is a different licence number, a different address and a different qualifying individual, so it is stored separately and flagged rather than merged."),
            ("gap", "CSLB records this licensee at a 94122 address, but no completed Outer Sunset job scope was joined to it in this wave."),
        ],
    ),
    dict(
        lic="912469", name="Balla Construction and Design", trade="general", classes=["B"],
        entity="BALLA CONSTRUCTION AND DESIGN", form="Sole Ownership",
        addr="1352 10th Avenue 103, San Francisco, CA 94122", phone="(415) 595-7068",
        issue="03/15/2008", expire="2022-03-31", status="expired",
        status_text="This license is expired and not able to contract at this time.",
        wc="exempt - certified no employees (01/19/2021)", bond="cancelled 08/06/2021",
        permit=None, registry=("94122 roll-up row; 47 permit rows",),
        extras=[
            ("hold", "Status text is 'expired and not able to contract', Additional Status says the licence needs a contractor's bond to renew or reactivate, and the bond was cancelled 08/06/2021."),
            ("notice", "The licensee's registered address is 1352 10th Avenue, 94122 - inside the Outer Sunset - which is why the record is published and held rather than dropped."),
        ],
    ),
    dict(
        lic="431972", name="Hong Lee Construction", trade="general", classes=["B"],
        entity="HONG LEE CONSTRUCTION", form="Sole Ownership",
        addr="532 Grand Ave, South San Francisco, CA 94080", phone="(415) 298-0462",
        issue="12/06/1982", expire="2014-12-31", status="expired",
        status_text="This license is expired and not able to contract at this time.",
        wc="policy expired 02/14/2017", bond="cancelled 12/06/2014",
        permit=None, registry=("94122 roll-up row; 34 permit rows",),
        extras=[
            ("hold", "Licence expired 12/31/2014 with the contractor's bond cancelled the same day; the workers' compensation policy on file expired 02/14/2017."),
            ("discrepancy", "Miscellaneous Information records '09/29/2007 - LICENSE REISSUED TO ANOTHER ENTITY' on this number as well, so it does not identify only the 1982 entity."),
        ],
    ),
    dict(
        lic="937334", name="Chubby Construction", trade="general", classes=["B"],
        entity="CHUBBY CONSTRUCTION", form="Sole Ownership",
        addr="1867 45th Avenue, San Francisco, CA 94122", phone="(415) 640-0333",
        issue="09/01/2009", expire="2027-09-30", status="active",
        wc="Endurance Assurance, code 5610 Contractors-construction subcontracted, to 08/13/2027",
        bond="Western Surety 65514716, cancellation date 09/30/2026",
        permit=None, registry=("94122 roll-up row; 38 permit rows",),
        hold="The contractor's bond carries a cancellation date of 09/30/2026, the same day the licence expires. CSLB suspends a licence when a bond lapses, and the file must be re-read before contact.",
        extras=[
            ("gap", "The workers' compensation classification is 'Contractors-construction subcontracted', which points to subcontracted labour rather than an in-house plumbing or drywall crew."),
            ("notice", "CSLB records this licensee at 1867 45th Avenue, 94122 - regulator-recorded Outer Sunset location evidence."),
        ],
    ),
    dict(
        lic="928524", name="Liang General Construction Inc", trade="general", classes=["B"],
        entity="LIANG GENERAL CONSTRUCTION INC", form="Corporation",
        addr="263 Aviador Ave, Millbrae, CA 94030", phone="(415) 992-2838",
        issue="02/09/2009", reissue="11/18/2014", expire="2026-11-30", status="suspended",
        status_text="License is under suspension for the following reasons: License is under Contractors Bond Suspension.",
        wc="State Compensation Insurance Fund, cancellation date 09/16/2026",
        bond="Hudson Insurance Company 30124588, cancelled 09/01/2026",
        permit=None, registry=("94122 roll-up row; 38 permit rows",),
        hold="The licence is under contractors bond suspension, not active: the bond was cancelled 09/01/2026 and workers' compensation carries a cancellation date of 09/16/2026. A suspended licence cannot lawfully contract.",
        extras=[
            ("discrepancy", "The same insurer and the same 09/01/2026 bond-cancellation date appear on two licences already stored from wave 6 (All-Point Solutions Plumbing 950265 and F C Company 1022789), so three bond-suspended licences in this corpus now share one insurer cancellation date."),
            ("discrepancy", "Reissued 11/18/2014 to the same number, so the number does not identify only the original 2009 entity."),
        ],
    ),
    dict(
        lic="961952", name="Douglas Cleaveland", trade="general", classes=["B"],
        entity="DOUGLAS CLEAVELAND", form="Sole Ownership",
        addr="1492 6th Ave, San Francisco, CA 94122", phone="(415) 706-4584",
        issue="06/09/2011", expire="06/30/2027", status="active",
        wc="Insurance Company of the West to 06/27/2027; codes 54741 painting, 8810 clerical, 5432 carpentry",
        bond="ACI 100397998, effective 01/01/2023",
        permit=None, registry=("1492 06th Av", "San Francisco", "94122-0000", "not published on this registry row"),
        extras=[
            ("notice", "CSLB records this licensee at 1492 6th Ave, 94122 - a regulator-recorded Outer Sunset address - and the City registry carries the same street on 28 permit rows."),
            ("gap", "B only, with a workers' compensation profile of painting, clerical and carpentry; nothing in it points to plumbing."),
        ],
    ),
    dict(
        lic="951781", name="Kohler Heating", trade="scope-exclusion", classes=["C20"],
        entity="KOHLER HEATING", form="Sole Ownership",
        addr="1229 4th Ave, San Francisco, CA 94122", phone="(415) 407-9285",
        issue="08/31/2010", expire="2028-08-31", status="active",
        wc="American Casualty to 06/30/2027; code 5183 shown as 'Description Unavailable'",
        bond="Atlantic Specialty 800049114, effective 08/16/2025",
        permit=None, registry=("1229 4th Avenue", "San Francisco", "94122-0000", "not published on this registry row"),
        extras=[
            ("hold", "Scope exclusion: C20 covers warm-air heating, ventilating and air-conditioning. It does not cover plumbing or drywall, so this record can never satisfy either requirement of this project and is held as a documented exclusion."),
            ("discrepancy", "Address and ZIP disagree on both sources: '1229 4th Ave' is published with ZIP 94122 by CSLB, and the City registry repeats the same pairing on 32 permit rows. Fourth Avenue sits outside the Outer Sunset grid, so the pairing is flagged for manual review rather than corrected."),
        ],
    ),
    dict(
        lic="656774", name="Ze Sheng Liao", trade="general", classes=["B"],
        entity="ZE SHENG LIAO", form="Sole Ownership",
        addr="2930 Lawton Street, San Francisco, CA 94122", phone="(415) 867-5528",
        issue="10/20/1992", expire="2026-10-31", status="active",
        wc="State Compensation Insurance Fund to 09/12/2027", bond="Atlantic Specialty 800271213, effective 09/01/2026",
        permit=None, registry=("2930 Lawton St", "San Francisco", "94122-0000", "not published on this registry row"),
        extras=[
            ("notice", "CSLB records this licensee at 2930 Lawton Street, 94122, and the City registry carries 33 permit rows at that address."),
            ("discrepancy", "The same licence number appears on the registry at three further addresses (451 20th Av 94121 with 74 rows, plus 94134 and 94112 addresses), so the registry address history is churned and only the CSLB address is treated as current."),
            ("gap", "B only, expiring 10/31/2026 - six weeks after this check."),
        ],
    ),
    dict(
        lic="876008", name="Success Construction", trade="multi-trade", classes=["B", "C10", "C36"],
        entity="SUCCESS CONSTRUCTION", form="Sole Ownership",
        addr="808 Geary St, San Francisco, CA 94109", phone="(415) 624-9526",
        issue="04/11/2006", expire="2028-04-30", status="active",
        wc="State Compensation Insurance Fund, policy cancelled 07/31/2026; code 5190 electrical wiring-low wage",
        bond="Business Alliance Insurance G19033211106, effective 03/05/2026",
        permit=None, registry=("1887 25th Av", "San Francisco", "94122-0000", "not published on this registry row"),
        hold="The workers' compensation policy on this licence carries a cancellation date of 07/31/2026, six weeks before this check, and no renewal is displayed.",
        extras=[
            ("notice", "One of only four licences read in this wave that carry B and C36 together, plus C10 - a general-building and plumbing combination that can cover both a wall or ceiling opening and the pipe work behind it on paper."),
            ("gap", "The firm is registered in ZIP 94109; the Outer Sunset link is the City registry row at 1887 25th Av, 94122, where it appears on 64 permit rows."),
            ("gap", "Personnel listed on this licence also appear on other licences, per CSLB's own note."),
        ],
    ),
    dict(
        lic="898949", name="San Francisco Investment Development", trade="general", classes=["B"],
        entity="SAN FRANCISCO INVESTMENT DEVELOPMENT", form="Corporation",
        addr="1890 14th Avenue, San Francisco, CA 94122", phone="(415) 682-4536",
        issue="06/20/2007", reissue="05/26/2017", expire="2027-05-31", status="active",
        wc="Everest Premier to 07/12/2027; codes 543200, 548201 and 881000 shown as 'Description Unavailable'",
        bond="Merchants Bonding Company 101970333, effective 09/01/2026",
        permit=None, registry=("1446 17th Av 4", "San Francisco", "94122-0000", "not published on this registry row"),
        extras=[
            ("notice", "CSLB records this licensee at 1890 14th Avenue, 94122 - a regulator-recorded Outer Sunset address - and the registry carries 48 permit rows at a different 94122 address in the same district."),
            ("discrepancy", "Miscellaneous Information records '05/26/2017 - LICENSE REISSUED TO ANOTHER ENTITY' on this number."),
            ("gap", "B only: the licence covers general building work such as drywall and cannot cover pipe work."),
        ],
    ),
    dict(
        lic="795316", name="L & G Construction Co", trade="general", classes=["B"],
        entity="L & G CONSTRUCTION CO", form="Partnership",
        addr="1742 21st Avenue, San Francisco, CA 94122", phone="(415) 816-1813",
        issue="05/18/2001", expire="2027-05-31", status="active",
        wc="exempt - certified no employees (06/12/2025)", bond="ACI 100273579, effective 01/01/2023",
        permit=None, registry=("1742 21st Ave", "San Francisco", "94122-0000", "not published on this registry row"),
        name_collision="w10-l-g-construction-co-inc",
        extras=[
            ("discrepancy", "Near-name collision published rather than merged: wave 10 stored a registry lead named 'L & G Construction Co Inc' (id w10-l-g-construction-co-inc) with its own licence number. The regulator read today is a different number held by a PARTNERSHIP of nearly the same name at the same Outer Sunset address, so both records stand and neither is folded into the other."),
            ("gap", "B only, and workers' compensation is exempt (no employees certified since 06/12/2025)."),
        ],
    ),
    dict(
        lic="427779", name="J & L Construction Company", trade="general", classes=["B"],
        entity="J & L CONSTRUCTION COMPANY", form="Sole Ownership",
        addr="2231 37th Ave, San Francisco, CA 94116", phone="(415) 509-6868",
        issue="09/10/1982", expire="2028-08-31", status="active",
        wc="exempt - certified no employees (07/22/2026)", bond="ACI 101090283, effective 08/12/2026",
        permit=None, registry=("1216 32nd Av", "San Francisco", "94122-0000", "not published on this registry row"),
        extras=[
            ("notice", "Licence held by the same sole ownership since 09/10/1982, with 37 registry permit rows at a 94122 address and a regulator-recorded address in 94116 next door."),
            ("gap", "B only, with no employees certified, so no crew can be verified from this page."),
        ],
    ),
    dict(
        lic="757766", name="B K L Construction", trade="general", classes=["B"],
        entity="B K L CONSTRUCTION", form="Sole Ownership",
        addr="1245 30th Ave, San Francisco, CA 94122", phone="(415) 730-5598",
        issue="01/06/1999", expire="2029-01-31", status="inactive",
        status_text="This license is inactive and not able to contract at this time.",
        wc="exempt, cancelled 02/01/2013", bond="Old Republic W150080826, cancelled 02/14/2013",
        permit=None, registry=("1330 44th Av", "San Francisco", "94122-0000", "not published on this registry row"),
        extras=[
            ("hold", "CSLB reads this licence as 'inactive and not able to contract', with Additional Status requiring both a contractor's bond and workers' compensation cover to renew; the bond was cancelled in 2013 and Miscellaneous Information records '10/16/2023 - WC EXEMPT CANCELLED-LIC INACTIVATED'."),
            ("discrepancy", "CSLB records the address as 1245 30th Ave, 94122 while the City registry stores 1330 44th Av, 94122 across 37 permit rows - two different Outer Sunset addresses."),
        ],
    ),
    dict(
        lic="1106072", name="Tailwind Construction Inc", trade="multi-trade", classes=["B", "C10", "C36"],
        entity="TAILWIND CONSTRUCTION INC", form="Corporation",
        addr="1762 42nd Ave, San Francisco, CA 94122", phone="(415) 802-5004",
        issue="06/16/2023", expire="2027-06-30", status="active",
        wc="American Casualty Company of Reading PA, policy 8035790483, effective 02/04/2026, expiring 02/04/2027",
        bond="Atlantic Specialty 800195297, $25,000, effective 07/01/2025",
        permit=None, registry=("1879 42nd Av", "San Francisco", "94122-0000", "not published on this registry row"),
        extras=[
            ("notice", "CSLB itself records this licensee at 1762 42nd Ave, San Francisco 94122 - a regulator-recorded Outer Sunset address - holding an active B + C10 + C36 licence to 06/30/2027. The City permit registry carries the same firm name and licence number at 1879 42nd Av, 94122 across 22 permit rows, and the qualifying individual Liyuan Liu certified ownership of 10 percent or more of the corporation."),
            ("gap", "The three classifications cover general building, electrical and plumbing, but no C-9 or C35: on a 1940 lath-and-plaster ceiling the plaster patch would sit outside a plumbing-only or electrical-only reading, so the ceiling restoration must be confirmed in writing against the B classification actually held."),
            ("gap", "No completed Outer Sunset job scope was joined to this licence in this wave; the registry rows prove recorded permit contacts, not present dispatch capacity."),
            ("gap", "The registry row publishes no phone number, so the CSLB business phone is the only number read for this firm and it has not been dialled or verified by this project."),
        ],
    ),
    dict(
        lic="824155", name="Wing Chow Construction", trade="general", classes=["B"],
        entity="WING CHOW CONSTRUCTION", form="Corporation",
        addr="1039 Grant Ave Ste 201, San Francisco, CA 94133", phone="(415) 576-9318",
        issue="09/12/2003", reissue="01/07/2004", expire="2028-01-31", status="suspended",
        status_text="License is under suspension for the following reasons: License is under Contractors Bond Suspension. A contractor's bond may have been received by the Board but not yet processed. Once the bond is processed the suspension will be lifted retroactively to the effective date of the bond. Ask the contractor for proof of a contractor's bond and contact the bonding company to verify bond status.",
        wc="State Compensation Insurance Fund, policy 9027695, effective 10/08/2025, expiring 10/08/2026; code 5432 carpentry-high wage",
        bond="Hudson 30138239, $25,000, effective 12/27/2023, cancellation date 09/01/2026",
        permit=None, registry=("1267 15th Av", "San Francisco", "941220000", "not published on this registry row"),
        hold="CSLB states the licence is under contractors-bond suspension, with the Hudson bond cancelled 09/01/2026: the suspension lifts retroactively only once a bond is processed, so nothing can be contracted under this number until CSLB says it is active again.",
        extras=[
            ("discrepancy", "A fourth licence in this corpus carries the same insurer and the same 09/01/2026 bond-cancellation date: the two wave-6 records All-Point Solutions Plumbing 950265 and F C Company 1022789, this wave's Liang General Construction 928524, and now this licence. One insurer's cancellation date now suspends four stored licences."),
            ("discrepancy", "Miscellaneous Information records '01/07/2004 - LICENSE REISSUED TO ANOTHER ENTITY' on a 2003 licence, so the number does not identify only the original 2003 holder."),
            ("gap", "B only: no C36 and no C-9 or C35 on the licence, and the workers' compensation profile is a single carpentry code, so neither the plumbing half nor the plaster half of this project can be confirmed from the page."),
        ],
    ),
]

# ------------------------------------------- City registry-only leads --------
LEADS = [
    # Registry rows only: a City-recorded firm name, licence number and 94122
    # address. No CSLB page was opened for any of these numbers in this wave.
    # The sixth field records registry aliases seen for the same licence number.
    ("771796", "Ting Kun Chow", "1735 29th Av", "94122-0000", 83,
     "The same registry also prints licence 771796 as 'Perfect Hitech Association Co' at the same 1735 29th Av address across 34 further rows, so the number was read by the City under two firm names."),
    ("747801", "C R Construction Co Inc", "1687 26th Avenue", "94122-0000", 31,
     "Single registry row for this licence number; no alias and no second address was published."),
    ("859089", "Andrew Moore Consulting", "1230 11th Av", "94122-0000", 30,
     "The firm name carries 'Consulting' while the registry uses it on plumbing-permit contact rows; no classification is asserted and no CSLB page was opened for this number."),
    ("766814", "Johnston Tile Company", "1501 33rd Av", "94122-0000", 68,
     "Single registry row; no alias and no second address was published for this licence number."),
    ("577073", "Sai Cheung Constr. Co", "2029 Kirkham St", "94122", 62,
     "Single registry row; no alias and no second address was published for this licence number."),
    ("765131", "John Woo Constructionllc", "1326 11th Av", "94122-0000", 49,
     "The firm name as published carries no space before 'llc'; it is stored exactly as the registry prints it."),
    ("447752", "Lin Hop Construction Inc", "1623 Noriega Street", "94122", 17,
     "The same licence number is also recorded at 1582-27th Avenue, 94122, across 11 further rows, and the 1623 Noriega Street rows appear in four different spellings."),
    ("817377", "Stodoni Construction", "1478 38th Av", "94122-0000", 32,
     "The same licence number also appears at 769 25th Av, 94121, 1475 38th Av, 94122, and a San Anselmo address, so the registered base is not one place."),
    ("410660", "Sun Sun Construction Co", "1285 27th Av", "94122-0000", 36,
     "The same licence number also appears at 2774 21st St, 94110, across 50 further rows, four times the Outer Sunset count."),
    ("728611", "City Builder Company", "1494 47th Av", "94122", 36,
     "The same licence number is also printed as 'Tonny Yee' at the same address and as 'Atlantic Construction Co Inc' at 8 Morningside Dr, 94132."),
    ("982071", "De Star Construction", "2209 Moraga Street", "94122-0000", 35,
     "The same licence number also appears at 469 Sunrise Wy, 94134, across 6 further rows."),
    ("502015", "Mazzys Fire Protection", "1280 20th Av", "94122", 92,
     "The firm name appears in three registry spellings for the same address and licence number; the largest single spelling carries 92 rows."),
    ("674169", "Fire Star Heating", "4650 Irving St", "94122-0000", 38,
     "The same licence number is also printed as 'Five Star Heating' at 327 Kinross Dr, 94598, and again at 4650 Irving St, so two firm names share one number."),
    ("572992", "Mediterranean Tile", "1735 35th Av", "94122-0000", 16,
     "The same licence number is also printed as 'Michael Eshia Dba Mediterranean Tile & S' and 'Mediterranean Tile & Stone' at 2647 37th Av, 94116, and at 1800 22nd Av and 1722 35th Av in 94122."),
]

# ------------------------------------------------ platform listings ----------
PLATFORM = [
    dict(key="willy-floors", name="Willy Floors", src=534,
         category="Flooring work, listed on the San Francisco drywall-repair category page",
         rating="Great 4.8 (39 reviews)", hires="41 hires on Thumbtack",
         url="https://www.thumbtack.com/ca/hayward/hardwood-floor-installation/willy-floors/service/502727663255257097",
         labels=["Limited Availability (platform label)"],
         review=("Jeff L.",
                 "Did a great job repairing a creaky floor - and did it the right way. Left the workspace very clean and was extremely friendly. Would recommend!",
                 "Retained for the working-conditions half of the sentence: a reviewer reporting that the workspace was left clean and the repair was done properly. Nothing in it concerns walls, ceilings or plumbing."),
         extras=["Listed on the San Francisco drywall-repair category page while its own profile URL sits under Hayward; the platform's area statement is the only service-area evidence.",
                 "No licence number is published, and the listing is classified under flooring, so it is stored as a platform listing and not as a drywall record."]),
    dict(key="arshan", name="Arshan Construction & Remodeling", src=534,
         category="Plumbing repair and assembly, plus drywall repair and texturing",
         rating="Excellent 4.9 (74 reviews)", hires="113 hires on Thumbtack",
         url="https://www.thumbtack.com/ca/san-francisco/affordable-plumbing-services/arshan-construction-remodeling/service/502865492336615427",
         labels=["Top Pro (platform label)", "Licensed pro (platform badge; no licence number published)"],
         review=("Tom R.",
                 "EDIT: We hired Batir and his brother again in January 2025 to replace an old rusted bathroom sink and counter top and some old frozen shut-off valves. Again, super job! We love the new sink which Batir picked out for us. We had a different plumber in the past who broke things and created more problems than he solved.",
                 "The most on-point review text retained this wave for the project's stated conditions: corroded fixtures, frozen shut-off valves and a customer describing an earlier plumber who caused damage. The excerpt is a contiguous slice of the published review and ends at a sentence boundary; the review continues into praise that names no additional task. It is a reported working style and a repeat hire, not evidence of seized-trip-lever work."),
         extras=["Two category pages list this pro - plumbing services and drywall repair - which is why it is stored under the platform-listing label rather than a classification.",
                 "No licence number, class or issuing board is published on the listing, so the platform's licensed-pro badge cannot be checked against CSLB."]),
    dict(key="jco", name="J.Co Contractors Inc", src=532, category="Drywall Installation and Hanging",
         rating="5.0 (2 reviews)", hires="No hire count published",
         url="https://www.thumbtack.com/ca/concord/pro/jco-contractors-inc/service/588470122297360397",
         labels=["Licensed pro (platform badge; no licence number published)"],
         review=None,
         extras=["The listing's own about-text names 'Plumbing & electrical work' alongside 'Drywall installation, finishing & texture' - the combination this project needs - while publishing no licence number, no service radius and only two reviews.",
                 "Read as a platform claim only. The firm's licence was not located because the listing publishes no number."]),
    dict(key="pinnacle", name="Pinnacle Plumbing, Inc.", src=534,
         category="Plumbing drain repair, pipe installation or replacement, toilet and water-heater work",
         rating="Great 4.8 (33 reviews)", hires="56 hires on Thumbtack",
         url="https://www.thumbtack.com/ca/san-francisco/water-heater-repair/pinnacle-plumbing-inc/service/549087419978047494",
         labels=["Top Pro (platform label)", "Licensed pro (platform badge; no licence number published)"],
         review=("Terry F.", "Great quality, communication and are now my go to plumbers in the area!",
                 "A short repeat-business endorsement. It supports communication and general plumbing satisfaction and carries no detail about access, older assemblies or drywall."),
         extras=["Serves San Francisco per the listing; the Outer Sunset is not named on the listing.",
                 "No licence number is published, so nothing can be checked against CSLB from this listing."]),
    dict(key="wp-proline", name="WP Proline Construction", src=537,
         category="General contracting with bathroom remodeling",
         rating="5.0 (2 reviews)", hires="No hire count published",
         url="https://www.thumbtack.com/ca/san-mateo/general-contractors/wp-proline-construction/service/586753615893807108",
         labels=["Licensed pro (platform badge; no licence number published)"],
         review=("Lilian S.",
                 "They remodeled one of my bathrooms, and I couldn't be happier with the results. They are true professional, responsible, and highly skilled.",
                 "A direct bathroom-remodel result statement, kept because it names the exact room. It says nothing about pipe work, access or wall and ceiling restoration, and only two reviews are published."),
         extras=["Two reviews only; the sample is too small to compare with the long-history records stored in this wave.",
                 "The listing publishes no licence number, address or service radius beyond the platform's area statement."]),
    dict(key="aquinos", name="Aquino's plastering and painting", src=535, category="Plastering",
         rating="Great 4.7 (127 reviews)", hires="199 hires on Thumbtack",
         url="https://www.thumbtack.com/ca/newark/stucco-contractors/aquinos-plastering-painting/service/288805689308733460",
         labels=["Licensed pro (platform badge; no licence number published)"],
         review=("Dennis Y.", "Me and my wife really appreciate their high quality STUCCO work for my home. Thank-you Juan and your teams. Well done.",
                 "Evidence of a large plaster and stucco customer base, and the retained review is about exterior stucco - not the interior lath-and-plaster ceiling repair a 1940 ceiling patch would involve."),
         extras=["Stored because a 1940 house ceiling is likely lath and plaster, where C-35 lathing and plastering is the relevant classification - but the listing publishes no licence number, so no class can be confirmed.",
                 "High review volume and a favourable excerpt are not treated as evidence of a credential or of ceiling-access experience."]),
    dict(key="swilly", name="Swilly Plastering and Stucco", src=535, category="Plastering",
         rating="Excellent 4.9 (8 reviews)", hires="12 hires on Thumbtack",
         url="https://www.thumbtack.com/ca/novato/stucco-contractors/swilly-plastering-stucco/service/277441733713085618",
         labels=["Licensed pro (platform badge; no licence number published)"],
         review=("Kamyar K.", "They performed excellent job repairing a stucco hole in the exterior of our building.",
                 "A hole-repair review, but on a building exterior in stucco - a different substrate and a different access problem from an interior ceiling patch."),
         extras=["Small sample: 8 reviews and 12 hires. The retained quote is a single-sentence result statement.",
                 "No licence number is published on the listing."]),
    dict(key="bap", name="Bay Area plastering", src=535, category="Plastering",
         rating="Great 4.8 (12 reviews)", hires="21 hires on Thumbtack",
         url="https://www.thumbtack.com/ca/santa-clara/stucco-contractors/bay-area-plastering/service/457072811029708819",
         labels=[],
         review=("J W.", "Clean flush, looks great I will recommend this company",
                 "A finish-quality comment with no task description; it cannot be attributed to plaster repair rather than new stucco."),
         extras=["The shortest retained quote in this wave, kept verbatim rather than expanded.",
                 "No licence number, no classification and no service-radius statement beyond 'serves San Francisco, CA'."]),
    dict(key="city-handyman", name="City Handyman", src=535, category="Plastering",
         rating="3.7 (3 reviews)", hires="3 hires on Thumbtack", url="https://www.thumbtack.com/ca/san-francisco/pro/city-handyman/service/586992285048078339",
         labels=[],
         review=("Samantha S.", "I ordered a ceiling lamp that turned out to be way too heavy for our condo's ceiling.",
                 "Retained because this is the lowest rating in the wave and the published excerpt is a problem statement, not a result. It is not a complaint about plaster or drywall work and no cause of the low rating is published."),
         extras=["Lowest rating retained in this wave (3.7 from three reviews). It is published as read so the sample is not skewed toward favourable listings.",
                 "The excerpt concerns a light fixture order, so it carries no task evidence in either direction."]),
    dict(key="promodeling", name="Promodeling", src=537, category="Bathroom remodeling",
         rating="Good 4.4 (56 reviews)", hires="13 hires on Thumbtack",
         url="https://www.thumbtack.com/ca/el-cerrito/general-contractors/promodeling/service/548702251396669440",
         labels=["Licensed pro (platform badge; no licence number published)"],
         review=("Christine Okon",
                 "When we decided to remodel our tiny San Francisco bathroom into a walk-in curbless shower, we met with five highly rated contractors.",
                 "The platform publishes only this opening sentence, so the outcome is unknown. It is retained because the described project - a tiny San Francisco bathroom converted to a walk-in shower - is the closest published scenario to the space constraints in this project, and because a five-contractor comparison is exactly the buying process this research supports."),
         extras=["The listing publishes no licence number, no address and no service radius beyond the platform's own area statement.",
                 "The quoted sentence is the platform's truncated snippet; it is not treated as a complete review and no rating or outcome is inferred from it."]),
    dict(key="gadi", name="GADI construction", src=537, category="Bathroom and kitchen remodeling",
         rating="Great 4.7 (168 reviews)", hires="330 hires on Thumbtack",
         url="https://www.thumbtack.com/ca/santa-clara/kitchen-remodeling/gadi-construction/service/388887459584376835",
         labels=["Licensed pro (platform badge; no licence number published)"],
         review=("Kaitlin d.",
                 "He was very responsive and easy to work with. We had a few small issues and he always dealt with them right away. Project was completed quickly and on time.",
                 "Retained for what it says about handling problems: the reviewer reports small issues being dealt with immediately. That is directly relevant to a job whose fallback path is disruptive, and it is not evidence of any licence, permit or plumbing skill."),
         extras=["Largest hire count in the platform tier read this wave (330), which is a platform popularity measure and never a quality or credential proxy.",
                 "No licence number, classification or address is published on the listing."]),
    dict(key="antrmen", name="ANTORMEN", src=537, category="General contracting with bathroom and kitchen work",
         rating="Exceptional 5.0 (40 reviews)", hires="10 hires on Thumbtack",
         url="https://www.thumbtack.com/ca/san-francisco/general-contractors/antrmen/service/549741754129948686",
         labels=["Top Pro (platform label)", "Licensed pro (platform badge; no licence number published)"],
         review=("Mirza",
                 "plus installed vents and ducting for a new kitchen range hood and a bathroom fan.",
                 "The platform publishes a mid-sentence fragment, so both the start and the outcome are missing. It is retained verbatim because it is the only excerpt in this tier that names bathroom ventilation work, and the analysis states plainly that the sentence is incomplete."),
         extras=["The listing is categorised as general contracting and names both plumbing-adjacent ventilation work and bathroom work; none of that is verified against a licence on this record.",
                 "No licence number is published, so the platform's licensed-pro badge carries no checkable value."]),

]

# ---------------------------------------- verification upgrades --------------
# Twelve licences read today were already stored: seven that waves 8-10 read
# earlier (re-read, with new facts) and five that stored records explicitly
# published as "NOT read on CSLB". Each upgrade names the record it belongs to.
UPGRADES = [
    dict(record="w8-brus-box-contractor-works", lic="1141495", kind="verification",
         entity="BRUS BOX CONTRACTOR WORKS", form="Corporation",
         addr="643 Sylvan Street #2, Daly City, CA 94014", phone="(415) 608-4090",
         issued="08/05/2025", status="active", status_text="This license is current and active.",
         expires="2027-08-31", classes=["B"], trade="general",
         hold="The workers' compensation policy shown on this licence expires 08/15/2026, one month before this re-read, and no renewal is displayed.",
         facts=["Re-read 2026-09-15: still 'current and active', B only, corporation at 643 Sylvan Street #2, Daly City, expiring 08/31/2027.",
                "New in this read: City plumbing permit PP20260217450 at 1458 34th Av (94122) completed 2026-08-11, scope 'convert tub to shower pan. change toilet bowl. install a vanity with faucet. reroute a water supply line'.",
                "New in this read: the licence was issued 08/05/2025, so this is the shortest filing history among the licences read in this wave."]),
    dict(record="w8-wolfe-painting-co", lic="754201", kind="verification",
         entity="WOLFE PAINTING CO", form="Sole Ownership",
         addr="190 Alexander Ave, Daly City, CA 94014", phone="(415) 235-6227",
         issued="09/21/1998", status="active", status_text="This license is current and active.",
         expires="2026-09-30", classes=["C33", "B"], trade="general",
         hold="The licence expires 09/30/2026 and the workers' compensation policy shows a cancellation date of 09/19/2026 - both within weeks of this re-read.",
         facts=["Re-read 2026-09-15: 'current and active', C33 Painting and Decorating plus B General Building, sole ownership at 190 Alexander Ave, Daly City.",
                "New in this read: City plumbing permit PP20251211352 at 1450 22nd Av (94122) completed 2026-07-24, scope 'replace ptrap supply lives in kitchen/replace vanity plumbing and toilet change tub valves, shower head'. Permit scope mentions valve and tub work that neither classification covers.",
                "New in this read: the licence has been held by the same sole owner since 09/21/1998."]),
    dict(record="w9-elux-construction-inc", lic="893710", kind="verification",
         entity="ELUX CONSTRUCTION INC", form="Corporation",
         addr="571 6th Ave Unit A, San Francisco, CA 94118", phone="(650) 281-7587",
         issued="04/02/2007", status="active", status_text="This license is current and active.",
         expires="2028-04-30", classes=["B"], trade="general",
         facts=["Re-read 2026-09-15: 'current and active', B only, corporation at 571 6th Ave Unit A, 94118, expiring 04/30/2028 - this closes the gap the stored record published, that licence 893710 had never been read.",
                "New in this read: Miscellaneous Information records '04/15/2022 - LICENSE REISSUED TO ANOTHER ENTITY' on an otherwise active licence, so the number no longer identifies only the original 2007 entity.",
                "New in this read: the registry's 1931 Diamond Street address and its 415-609-2028 phone differ from both the CSLB address and the CSLB phone."]),
    dict(record="w9-vij-construction-inc", lic="1059074", kind="verification",
         entity="VIJ CONSTRUCTION INC", form="Corporation",
         addr="41 W Gertrude Ave, Richmond, CA 94801", phone="(415) 694-1061",
         issued="10/09/2019", status="active", status_text="This license is current and active.",
         expires="2027-02-28", classes=["B", "D06"], trade="general",
         facts=["Re-read 2026-09-15: 'current and active', corporation at 41 W Gertrude Ave, Richmond, expiring 02/28/2027 - this closes the stored record's published gap that licence 1059074 had never been read.",
                "New in this read: a second classification, C-61/D06 Concrete Related Services, with its own qualifying-individual bond recorded 30/10/2024. It is stored so the licence is not read as a two-trade credential: D06 covers neither plumbing nor drywall.",
                "New in this read: workers' compensation is exempt (no employees certified since 02/27/2025)."]),
    dict(record="w9-american-plumbing-and-trenchless-llc", lic="1140051", kind="verification",
         entity="AMERICAN PLUMBING AND TRENCHLESS LLC", form="Ltd Liability",
         addr="310 Cimarron Drive, Vallejo, CA 94589", phone="(707) 639-7405",
         issued="07/08/2025", status="active", status_text="This license is current and active.",
         expires="2027-07-31", classes=["C36"], trade="plumbing",
         facts=["Re-read 2026-09-15: 'current and active', C36 only, Ltd Liability at 310 Cimarron Drive, Vallejo, expiring 07/31/2027.",
                "New in this read and new to the whole corpus: a liability-insurance line - Ategrity Specialty Insurance, $2,000,000, effective 06/10/2026 to 06/10/2027. The project's master gate asks for applicable insurance, so the figure is recorded; it still does not satisfy the other gates.",
                "New in this read: a $100,000 LLC employee/worker bond (American Contractors Indemnity, 06/10/2025), the bond an LLC licence must file.",
                "New in this read: City plumbing permit PP20260810750 at 601 Moraga St (94122) completed 2026-08-31, scope 'install of two way clean out behind the sidwalk, install two cast iron wye fittings and branch lines for storm drains and adu sewer connections. new storm and sewer lines approx 25 feet in length. underground work to be completed.'"]),
    dict(record="w9-speedy-serrano-plumbing", lic="1026009", kind="verification",
         entity="SPEEDY SERRANO PLUMBING", form="Partnership",
         addr="30 Salada Ave, Pacifica, CA 94044", phone="(650) 898-3007",
         issued="04/21/2017", status="active", status_text="This license is current and active.",
         expires="2027-04-30", classes=["C36"], trade="plumbing",
         facts=["Re-read 2026-09-15: 'current and active', C36 only, partnership at 30 Salada Ave, Pacifica, expiring 04/30/2027.",
                "New in this read: City plumbing permit PP20260107698 at 1350 44th Av (94122) completed 2026-09-09, scope 'new plumbing lines, sewer, ventsm water for 1 new laundry room, 1 new kitchen, 1 new restroom. underground work to be completed.'",
                "New in this read: the contractor's bond was re-filed with Atlantic Specialty Insurance effective 09/01/2026; workers' compensation remains exempt (no employees certified since 03/17/2025)."]),
    dict(record="w10-samco-construction-inc", lic="899541", kind="registry",
         entity="SAMCO CONSTRUCTION INC", form="Corporation",
         addr="1623 Noriega St, San Francisco, CA 94122", phone="(415) 988-2238",
         issued="07/02/2007", status="active", status_text="This license is current and active.",
         expires="2027-07-31", classes=["B", "C10"], trade="general", area="outer",
         area_text="CSLB itself records this licensee at 1623 Noriega St, San Francisco 94122 - an Outer Sunset address - with active B and C10 classifications expiring 07/31/2027. The registry row that first surfaced this licence stores the same street address.",
         facts=["Re-read 2026-09-15: 'current and active', B and C10, corporation at 1623 Noriega St, 94122 - this closes the stored record's published hold that licence 899541 had never been read, and it is the regulator's own 94122 location evidence.",
                "New in this read: workers' compensation classification codes include 51831 plumbing-low-wage, yet the licence holds no C36, so pipe work must not be inferred from it.",
                "New in this read: the CSLB business phone is (415) 988-2238 while the registry row stored (415) 828-0177, and the registry carries 76 permit rows for this licence."]),
    dict(record="w10-danny-chen", lic="893929", kind="registry",
         entity="DANNY CHEN", form="Sole Ownership",
         addr="1659 23rd Avenue, San Francisco, CA 94122", phone="(415) 671-9698",
         issued="04/05/2007", status="inactive",
         status_text="This license is inactive and not able to contract at this time.",
         expires="2029-04-30", classes=["C36"], trade="plumbing",
         hold="CSLB reads this licence as 'inactive and not able to contract', with Miscellaneous Information recording '05/05/2025 - WC EXEMPT CANCELLED-LIC INACTIVATED'. A plumbing classification inside the Outer Sunset does not make it usable.",
         facts=["Re-read 2026-09-15: C36 PLUMBING at 1659 23rd Avenue, 94122, in the Outer Sunset - but the status line reads 'inactive and not able to contract at this time', so the stored record's open question is closed negatively.",
                "New in this read: Additional Status says the licence will need to meet workers' compensation requirements to renew or reactivate; the exemption was cancelled 05/01/2025.",
                "New in this read: the same page notes that personnel listed on this licence appear on other licences."]),
    dict(record="w10-d-s-management-inc-dba-metrocon-builders", lic="978867", kind="registry",
         entity="D S MANAGEMENT INC - dba METROCON BUILDERS", form="Corporation",
         addr="130 Eastmoor Ave, Daly City, CA 94015", phone="(415) 373-2989",
         issued="11/21/2012", status="active", status_text="This license is current and active.",
         expires="2026-11-30", classes=["B"], trade="general",
         facts=["Re-read 2026-09-15: 'current and active', B only, corporation at 130 Eastmoor Ave, Daly City, expiring 11/30/2026 - this closes the stored record's published gap that licence 978867 had never been read.",
                "New in this read: the registry stores this licence at 2004 Irving St, 94122 while CSLB records Daly City; the two addresses are published side by side and neither is treated as closed.",
                "New in this read: workers' compensation is exempt (no employees certified since 02/17/2025) on a Daly City corporation."]),
    dict(record="w10-w-j-l-construction-inc", lic="775086", kind="registry",
         entity="W J L CONSTRUCTION INC", form="Corporation",
         addr="1518 26th Ave, San Francisco, CA 94122", phone="(415) 215-2338",
         issued="02/16/2000", status="active", status_text="This license is current and active.",
         expires="2028-02-29", classes=["B"], trade="general", area="outer",
         area_text="CSLB itself records this licensee at 1518 26th Ave, San Francisco 94122 - an Outer Sunset address - with an active B classification expiring 02/29/2028. The registry row that surfaced the licence stores the same street.",
         facts=["Re-read 2026-09-15: 'current and active', B only, corporation at 1518 26th Ave, 94122 - this closes the stored record's published gap that licence 775086 had never been read, and it is the regulator's own Outer Sunset address.",
                "New in this read: the qualifying individual, William Hom, holds 10 percent or more of the company, so no bond of qualifying individual is required.",
                "New in this read: workers' compensation is exempt (no employees certified since 01/07/2026), so no crew can be verified from this page."]),
    dict(record="w6-city-plumbing-company", lic="792165", kind="registry",
         entity="CITY PLUMBING COMPANY", form="Sole Ownership",
         addr="1846 42nd Avenue, San Francisco, CA 94122", phone="(415) 517-8123",
         issued="03/06/2001", status="canceled",
         status_text="This license is canceled and not able to contract.",
         expires="2025-02-19", classes=["C36"], trade="plumbing",
         hold="CSLB status reads 'canceled and not able to contract', with Miscellaneous Information recording '02/19/2025 - LICENSE CANCELED PER REQUEST' and a bond cancelled 04/05/2025. This is the newest of the three non-active answers in this wave.",
         facts=["Re-read 2026-09-15: C36 PLUMBING, sole ownership, CSLB address 1846 42nd Avenue, 94122 - the stored record's open question ('licence 792165 was NOT read on CSLB in this pass') is answered: the licence is canceled by request.",
                "New in this read: the City registry stores this same licence number at 1214 40th Av, 94122 across 124 permit rows, a different address from the regulator's.",
                "New in this read: the registry also prints this licence number under the name 'Tony Tiejun Hu' at the same 1214 40th Av address on 56 further rows."]),
    dict(record="w7-w-k-construction-company", lic="608902", kind="unresolved-identity",
         entity="WING HANG CHENG", form="Sole Ownership",
         addr="1626 26th Avenue, San Francisco, CA 94122", phone="(415) 531-0269",
         issued="01/08/1991", status="active", status_text="This license is current and active.",
         expires="2027-01-31", classes=["B"],
         hold="Identity unresolved and published as such: CSLB issues licence 608902 to the individual WING HANG CHENG, sole ownership, at 1626 26th Avenue, 94122 - not to a firm named 'W.K. Construction Company'. The City registry prints both names against this one number at the same address, so this record keeps asserting no licence fact for W.K. Construction Company.",
         facts=["Re-read 2026-09-15: licence 608902 is 'current and active', B only, issued to WING HANG CHENG as a sole ownership at 1626 26th Avenue, 94122, expiring 01/31/2027.",
                "The registry prints licence 608902 under two firm names at the same address: 'Wing Hang Cheng' (24 + 20 + 1 rows across three spellings) and 'W.K. Construction Company' (21 rows). A number that appears under a person's name and a company's name cannot be stored as the company's credential.",
                "New in this read: workers' compensation is exempt (no employees certified since 12/22/2024), and the bond is American Contractors Indemnity SC6002535 effective 01/01/2023."]),
    dict(record="be-home", lic="1115373", kind="registry",
         entity="BE HOME REMODELING INC", form="Corporation",
         addr="84 W Santa Clara St 700, San Jose, CA 95113", phone="(310) 666-5118",
         issued="01/24/2024", status="active", status_text="This license is current and active.",
         expires="2028-01-31", classes=["B"], trade="general",
         facts=["Re-read 2026-09-15: 'current and active', B only, corporation registered in San Jose, expiring 01/31/2028 - this closes the open gap on a record wave 12 had stored from a platform listing with no licence read.",
                "Identity note: the stored record came from a Yelp index entry with no address, and this licence shares its name and San Francisco service. The link rests on the name alone and is published as such.",
                "New in this read: City plumbing permit PP20260617655 at 318 Ortega St (94122) completed 2026-08-06, scope '2/f bathroom remodel, like for like (shower & tub). shower pan.'"]),
    dict(record="reliable-construction", lic="983658", kind="registry",
         entity="RELIABLE CONSTRUCTION INC", form="Corporation",
         addr="2800 34th Avenue, San Francisco, CA 94116", phone="(415) 756-3011",
         issued="05/13/2013", status="active", status_text="This license is current and active.",
         expires="2027-05-31", classes=["B"], trade="general", area="sunset",
         area_text="CSLB records this licensee at 2800 34th Avenue, San Francisco 94116 - the Sunset district west of the Outer Sunset boundary - with an active B classification expiring 05/31/2027. The registry row matches the CSLB address exactly.",
         facts=["Re-read 2026-09-15: 'current and active', B only, corporation at 2800 34th Avenue, 94116, expiring 05/31/2027 - this closes the open gap on a record wave 12 had stored from a platform listing with no licence read.",
                "Identity note: the stored record came from a Yelp index entry describing bathroom-remodel work and 30 years in business; CSLB shows this licence issued in 2013, so the '30 years' claim is not corroborated by the regulator's date.",
                "New in this read: City plumbing permit PP20260319051 at 1350 Ortega St (94122) completed 2026-09-04, scope 'add bathroom at g/f, relocate laundry, install tankless water heater', and the registry phone matches the CSLB phone exactly."]),
    dict(record="w9-all-bay-cities-construction", lic="872779", kind="registry",
         entity="ALL BAY CITIES CONSTRUCTION", form="Corporation",
         addr="151 Middlefield Drive, San Francisco, CA 94132", phone="(415) 716-7023",
         issued="02/15/2006", status="active", status_text="This license is current and active.",
         expires="2028-02-29", classes=["B"], trade="general", area="outer",
         area_text="CSLB records this licensee at 151 Middlefield Drive, San Francisco 94132 and shows a completed City plumbing permit for 1845 Irving St, 94122. The Outer Sunset label rests on the permit work address, not on the registered address.",
         facts=["Re-read 2026-09-15: 'current and active', B only, corporation at 151 Middlefield Drive, 94132, expiring 02/29/2028 - this closes the stored record's published hold that licence 872779 had never been read.",
                "New in this read: the workers' compensation profile is tile, stone and carpentry, a bathroom-finish mix rather than plumbing.",
                "New in this read: the registry row matches the CSLB street (151 Middlefield Dr) and phone exactly, and the licence is recorded on a plumbing permit as well as a mechanical permit at the same Outer Sunset address."]),
    dict(record="w6-abe-s-plumbing", lic="439862", kind="registry",
         entity="ABE'S PLUMBING", form="Sole Ownership",
         addr="5487 Kales Avenue, Oakland, CA 94618", phone="(510) 652-7280",
         issued="05/10/1983", status="expired",
         status_text="This license is expired and not able to contract at this time.",
         expires="2009-05-31", classes=["C36"], trade="plumbing", area="outside",
         area_text="CSLB records this licensee in Oakland, CA 94618 - outside the Outer Sunset entirely - and the licence has been expired since 05/31/2009. The stored registry row's 94122 PO box was a mailing address recorded by the City, not a place of business.",
         hold="The licence has been expired since 05/31/2009 and CSLB states it is not able to contract. The 148 permit rows the registry records for this name are history under a dead licence number, so the stored record is corrected from 'sunset' to 'outside' and held.",
         facts=["Re-read 2026-09-15: 'expired and not able to contract at this time', C36 only, address 5487 Kales Avenue, Oakland, with the contractor's bond cancelled 05/21/2005 - this closes the stored record's published hold that licence 439862 had never been read.",
                "New in this read: the regulator's address is in Oakland, while wave 6 stored the registry's San Francisco PO box as the recorded address. The record's area label is corrected to reflect the regulator's address.",
                "New in this read: the registry shows 153 permit rows for this firm in the 94122 roll-up; none of that changes the fact that the licence cannot contract today."]),
    dict(record="w7-chow-s-plumbing-co", lic="502603", kind="registry",
         entity="CHOW'S PLUMBING CO", form="Sole Ownership",
         addr="2431 16th Avenue, San Francisco, CA 94116", phone="(415) 665-8886",
         issued="12/09/1986", status="expired",
         status_text="This license is expired and not able to contract at this time.",
         expires="2014-12-31", classes=["C16", "C36"], trade="plumbing", area="sunset",
         area_text="CSLB records this licensee at 2431 16th Avenue, San Francisco 94116 - the Sunset district, not the Outer Sunset - and the licence has been expired since 12/31/2014. The stored registry row put the same licence number at 1755 29th Ave, 94122, which the regulator does not confirm.",
         hold="The licence expired 12/31/2014 and CSLB states it is not able to contract; the bond was cancelled 07/04/2013. The 48-51 permit rows the registry records for this firm are history under an expired number.",
         facts=["Re-read 2026-09-15: 'expired and not able to contract at this time', C16 and C36, at 2431 16th Avenue, 94116, with a bond cancelled 07/04/2013 - this closes the stored record's published hold that licence 502603 had never been read.",
                "New in this read: two different addresses for one licence number - CSLB's 2431 16th Avenue, 94116 and the registry's 1755 29th Ave, 94122, where the registry carries 48 rows.",
                "New in this read: the firm also appears in the registry as 'Chow's Plumbing Co' at 1755 29th Ave with a C16 Fire Protection class listed on the licence."]),
    dict(record="w6-west-cork-plumbing-inc", lic="900309", kind="verification",
         entity="WEST CORK PLUMBING INC", form="Corporation",
         addr="20 Roy Ct, Novato, CA 94947", phone="(415) 845-3870",
         issued="07/17/2007", status="active", status_text="This license is current and active.",
         expires="2027-08-31", classes=["C36"], trade="plumbing",
         facts=["Re-read 2026-09-15: 'current and active', C36 only, corporation at 20 Roy Ct, Novato, expiring 08/31/2027.",
                "New in this read: Miscellaneous Information records '08/18/2009 - LICENSE REISSUED TO ANOTHER ENTITY', so the number does not identify only the original 2007 entity.",
                "New in this read: workers' compensation with Hartford Casualty carries plumbing-high-wage code 51871 to 05/08/2027, and the registry shows the firm on 56 permit rows at 1612 Noriega St, 94122."]),
    dict(record="w6-flow-masters-plumbing-inc", lic="966337", kind="verification",
         entity="FLOW MASTERS PLUMBING INC", form="Corporation",
         addr="6169 Mission St, Daly City, CA 94014", phone="(415) 751-1933",
         issued="10/04/2011", status="active", status_text="This license is current and active.",
         expires="2027-10-31", classes=["C36", "C16", "C20"], trade="plumbing",
         facts=["Re-read 2026-09-15: 'current and active', C36 plumbing plus C16 fire protection and C20 HVAC, corporation at 6169 Mission St, Daly City, expiring 10/31/2027.",
                "New in this read: workers' compensation with Security National runs to 06/01/2027; two of its classification codes are published as 'Description Unavailable'.",
                "New in this read: personnel listed on this licence also appear on other licences, per CSLB's own note."]),
    dict(record="w6-building-efficiency-inc", lic="947504", kind="verification",
         entity="BUILDING EFFICIENCY INC", form="Corporation",
         addr="2037 Irving Street Suite 213, San Francisco, CA 94122", phone="(415) 831-4535",
         issued="05/18/2010", status="active", status_text="This license is current and active.",
         expires="2028-05-31", classes=["B", "C20", "C36", "C10"], trade="multi-trade",
         area="outer",
         area_text="CSLB itself records this licensee at 2037 Irving Street, Suite 213, San Francisco 94122 - an Outer Sunset address - with B, C20, C36 and C10 classifications active to 05/31/2028, plus an asbestos certification for bidding only.",
         facts=["Re-read 2026-09-15: 'current and active' with B, C20, C36 and C10, at 2037 Irving Street Suite 213, 94122, expiring 05/31/2028 - a regulator-recorded Outer Sunset address and a licence that can cover both a drywall opening and the pipe work behind it.",
                "New in this read: an ASB asbestos certification is recorded for bidding purposes only, which matters in a 1940 building where ceiling materials may be suspect; the certification is not a licence class.",
                "New in this read: Miscellaneous Information records '12/14/2015 - CONTRACTOR HIS LETTER SENT' (home improvement salesperson correspondence), and workers' compensation codes include plumbing-high-wage 51871 and sheet-metal-high-wage 55421."]),
    dict(record="w6-pro-plumbing", lic="859973", kind="verification",
         entity="PRO PLUMBING", form="Sole Ownership",
         addr="145 Barneveld Ave, San Francisco, CA 94122", phone="(415) 994-3468",
         issued="06/04/2005", status="expired",
         status_text="This license is expired and not able to contract at this time.",
         expires="2023-06-30", classes=["C36", "C16"], trade="plumbing",
         hold="The licence is expired and not able to contract: three separate renewal requirements are listed (a contractor's bond, a possible legal requirement, and workers' compensation cover), the bond was cancelled 08/04/2017, and Miscellaneous Information records '10/16/2023 - WC EXEMPT CANCELLED-LIC INACTIVATED'.",
         facts=["Re-read 2026-09-15: 'expired and not able to contract at this time', C36 and C16, expiring 06/30/2023, with a bond cancelled in 2017 and a WC exemption cancelled in 2019.",
                "New in this read: the address and ZIP disagree - CSLB pairs '145 Barneveld Ave' with 94122, while Barneveld Avenue sits outside the Outer Sunset grid. The stored record's address is left as read and the pairing is flagged.",
                "New in this read: three separate renewal blockers are listed, so reactivation is not a formality."]),
    dict(record="odonovan", lic="582534", kind="verification",
         entity="O'DONOVAN PLUMBING INC", form="Corporation",
         addr="1825 15th Avenue, San Francisco, CA 94122", phone="(415) 425-7322",
         issued="12/08/1989", reissue="07/21/2010", status="active", status_text="This license is current and active.",
         expires="2028-07-31", classes=["C16", "C36"], trade="plumbing", area="outer",
         area_text="CSLB itself records this licensee at 1825 15th Avenue, San Francisco 94122 - an Outer Sunset address - with C16 and C36 active to 07/31/2028 and a bond re-filed 09/01/2026.",
         facts=["Re-read 2026-09-15: 'current and active', C16 and C36, at 1825 15th Avenue, 94122, expiring 07/31/2028 - a regulator-recorded Outer Sunset address on a plumbing licence.",
                "New in this read: the contractor's bond was re-filed with Atlantic Specialty Insurance effective 09/01/2026, and workers' compensation with Travelers runs to 09/11/2027 on plumbing-high-wage and plumbing-low-wage codes.",
                "New in this read: Miscellaneous Information records '07/21/2010 - LICENSE REISSUED TO ANOTHER ENTITY'."]),
    dict(record="w10-oran-plumbing-corp", lic="762214", kind="verification",
         entity="ORAN PLUMBING CORP", form="Corporation",
         addr="95 El Plazuela St, San Francisco, CA 94127", phone="(415) 307-8198",
         issued="04/27/1999", reissue="05/07/2014", status="active", status_text="This license is current and active.",
         expires="2028-05-31", classes=["C36"], trade="plumbing",
         facts=["Re-read 2026-09-15: 'current and active', C36 only, corporation at 95 El Plazuela St, 94127, expiring 05/31/2028.",
                "New in this read: the registry also prints this licence number under a second name spelling, 'Francis John Burke', at 1480 7th Av, 94122 (61 rows), while CSLB issues it to Oran Plumbing Corp with Mr Burke as qualifying individual.",
                "New in this read: Miscellaneous Information records '05/07/2014 - LICENSE REISSUED TO ANOTHER ENTITY' and workers' compensation with State Fund carries plumbing-high-wage code 51871 to 03/27/2027."]),
    dict(record="purcell", lic="493818", kind="verification",
         entity="RODNEY CONKLIN PLUMBING & HEATING", form="Sole Ownership",
         addr="702 Anna Place AY, El Dorado Hills, CA 95762", phone="(650) 207-5899",
         issued="06/20/1986", status="expired",
         status_text="This license is expired and not able to contract at this time.",
         expires="2014-06-30", classes=["C20", "C36"], trade="plumbing",
         hold="The licence has been expired since 06/30/2014 with the bond cancelled 07/31/2014. The stored record's registry association with a 94122 address does not revive it.",
         facts=["Re-read 2026-09-15: 'expired and not able to contract at this time', C20 and C36, at an El Dorado Hills address, with a bond cancelled 07/31/2014.",
                "New in this read: the licence number appears in the 94122 roll-up under the name 'Purcell Bros Plumb & Heat' at 2255 Judah St across 52 rows, a different firm name than the regulator's current record for the same number.",
                "New in this read: workers' compensation is exempt from 04/14/2003 with no expiry, listed on an expired licence."]),
    dict(record="w6-goodrich-plumbing-inc", lic="837694", kind="verification",
         entity="GOODRICH PLUMBING INC", form="Corporation",
         addr="265 Kensington Way, San Francisco, CA 94127", phone="(415) 661-9138",
         issued="05/05/2004", status="canceled",
         status_text="This license is canceled and not able to contract.",
         expires="2025-02-11", classes=["C36"], trade="plumbing",
         hold="CSLB reads this licence as 'canceled and not able to contract', with Miscellaneous Information recording both '02/11/2025 - LICENSE CANCELED PER REQUEST' and '02/11/2025 - SECRETARY OF STATE - DISSOLUTION'. The bond was cancelled 04/04/2025 and workers' compensation 01/04/2025.",
         facts=["Re-read 2026-09-15: 'canceled and not able to contract', C36 only, at 265 Kensington Way, 94127, cancelled by request on 02/11/2025 with the corporation dissolved the same day.",
                "New in this read: the registry still prints this licence number for 94122 work, which is exactly why the cancelled status is published rather than the registry history alone.",
                "New in this read: the qualifying individual, John Liang, holds 10 percent or more of the company."]),
    dict(record="w6-c-t-construction-plumb", lic="533324", kind="registry",
         entity="CT CONSTRUCTION", form="Sole Ownership",
         addr="1847 48th Ave, San Francisco, CA 94122", phone="(415) 793-3615",
         issued="06/23/1988", status="active", status_text="This license is current and active.",
         expires="2027-09-30", classes=["B"], trade="general", area="outer",
         area_text="CSLB records licence 533324 as CT CONSTRUCTION, a sole ownership at 1847 48th Ave, San Francisco 94122 - an Outer Sunset address - active to 09/30/2027 with a B classification. The registry row that raised this question carries the same address.",
         facts=["Re-read 2026-09-15: licence 533324 is 'current and active', B only, issued to CT CONSTRUCTION as a sole ownership at 1847 48th Ave, 94122, expiring 09/30/2027. This is the question wave 9 published and left open.",
                "New in this read: CSLB's business phone for licence 533324 is (415) 793-3615, while the City registry printed (415) 203-7178 for the same address - the number that belongs to CT Plumbing & Fire Protection, licence 1112261. The registry phone therefore belongs to the other licence; both readings stay published.",
                "New in this read: the licence was reissued to the same number on 09/19/2023 and CSLB notes that personnel listed on it also appear on other licences; B alone cannot cover the plumbing pipe work the registry spelling 'Construction & Plumb' implies."]),
    dict(record="w9-kevel-home-performance", lic="1021221", kind="registry",
         entity="KEVEL HOME PERFORMANCE", form="Partnership",
         addr="3624 Ortega Street, San Francisco, CA 94122", phone="(415) 213-5545",
         issued="11/29/2016", status="active", status_text="This license is current and active.",
         expires="2026-11-30", classes=["B", "C20"], trade="scope-exclusion", area="outer",
         area_text="CSLB itself records this licensee at 3624 Ortega Street, San Francisco 94122 - an Outer Sunset address - with B and C20 classifications active to 11/30/2026. The registry row that first surfaced this firm carries the same street address.",
         facts=["Re-read 2026-09-15: 'current and active', B General Building and C20 Warm-Air Heating, Ventilating and Air-Conditioning, partnership at 3624 Ortega Street, 94122, expiring 11/30/2026 - this closes the stored record's published gap that its licence had never been read.",
                "New in this read: the workers' compensation profile is heating and air-conditioning duct work (codes 55422 and 55382), so nothing on the page points to plumbing; the B class can cover the drywall side only.",
                "New in this read: the contractor's bond was re-filed with Atlantic Specialty Insurance effective 09/01/2026, and the registry shows 31 permit rows at the same 94122 street."]),
    dict(record="w12-rapid-flow-plumbing", lic="1115649", kind="verification",
         entity="RAPID FLOW PLUMBING & ROOTER INC", form="Corporation",
         addr="230 Edinburgh St, San Francisco, CA 94112", phone="(415) 866-8401",
         issued="01/29/2024", status="active", status_text="This license is current and active.",
         expires="2028-01-31", classes=["B", "C36"], trade="multi-trade",
         facts=["Re-read 2026-09-15: 'current and active', B General Building and C36 Plumbing, corporation at 230 Edinburgh St, 94112, expiring 01/31/2028. The stored wave-12 record carried this licence from a directory page; the regulator page is now the source.",
                "New in this read: licence 1115649 was issued 01/29/2024, so it has two and a half years of history; the qualifying individual is Jose Silverio Navarro Jr.",
                "New in this read: the contractor's bond is Merchants Bonding 101423907 effective 03/03/2025 and workers' compensation is exempt (no employees certified 02/03/2026); CSLB also notes that personnel on this licence appear on other licences."]),
    dict(record="w12-handyman-heroes", lic="1003394", kind="verification",
         entity="HANDYMAN HEROES INC", form="Corporation",
         addr="912 Cole St # 202, San Francisco, CA 94117", phone="(844) 382-4376",
         issued="05/05/2015", status="active", status_text="This license is current and active.",
         expires="2027-05-31", classes=["B", "C10", "C36"], trade="multi-trade",
         hold="CSLB publishes two cautions on this licence: one or more classifications may be removed if the qualifying person is not replaced by 10/01/2026, and 'There is Complaint Disclosure information for this license.' The disclosure page was NOT opened in this wave, so no complaint content is published.",
         facts=["Re-read 2026-09-15: 'current and active', B plus C10 Electrical and C36 Plumbing, corporation at 912 Cole St # 202, 94117, expiring 05/31/2027. The stored wave-12 record carried this licence from a directory page; the regulator page is now the source.",
                "New in this read: an Additional Status line warns that one or more classifications may be removed if the qualifying person is not replaced by 10/01/2026 - a deadline fifteen days after this check.",
                "New in this read: the page carries a complaint-disclosure marker. The disclosure page itself was not opened, so the record publishes the marker and no complaint content.",
                "New in this read: a Bond of Qualifying Individual (100353313, Rollin Rhodes Anderson, $25,000) sits alongside the contractor's bond, and workers' compensation with Omaha National runs to 04/25/2027 on carpentry and clerical codes."]),
    dict(record="w10-z-construction-company-inc", lic="740407", kind="registry",
         entity="Z CONSTRUCTION COMPANY INC", form="Corporation",
         addr="1226 28th Ave, San Francisco, CA 94122", phone="(415) 850-7198",
         issued="09/15/1997", status="active", status_text="This license is current and active.",
         expires="2027-07-31", classes=["B"], trade="general", area="outer",
         area_text="CSLB itself records licence 740407 as Z CONSTRUCTION COMPANY INC at 1226 28th Ave, San Francisco 94122 - an Outer Sunset address - active to 07/31/2027 with a B classification. The registry row that first surfaced this firm carries the same street address.",
         facts=["Re-read 2026-09-15: 'current and active', B General Building, corporation at 1226 28th Ave, 94122, expiring 07/31/2027 - this closes the stored record's published hold that the registry licence number 740407 had never been read at CSLB.",
                "New in this read: the number was reissued to another entity on 07/19/2005, so it does not identify only the original holder; workers' compensation is exempt because no employees were certified on 05/26/2026.",
                "New in this read: the registry's own claim already placed this licence at the same address across 76 and 100 permit rows, so the regulator address and the City address agree."]),
    dict(record="w9-flmc-development-corp-dba-adamo-campagna", lic="805968", kind="registry",
         entity="FLMC DEVELOPMENT CORP - dba ADAMO CAMPAGNA DEVELOPMENT", form="Corporation",
         addr="P O Box 1009, Pacifica, CA 94044", phone="(415) 310-8937",
         issued="03/26/2002", status="active", status_text="This license is current and active.",
         expires="2027-02-28", classes=["B"], trade="general",
         area="sunset",
         area_text="The registry lead this record was built from already printed licence number 805968, and CSLB now confirms the number as an active B licence to 02/28/2027. CSLB's own address is a Pacifica PO box, so the record still stands only on the City's own permit-contact rows for the 94122 firm address.",
         facts=["Re-read 2026-09-15: 'current and active', B General Building, corporation, expiring 02/28/2027 - this closes the stored record's published gap that registry licence 805968 had NOT been read on CSLB.",
                "New in this read: Miscellaneous Information records '02/27/2025 - LICENSE REISSUED TO ANOTHER ENTITY' on a licence issued in 2002, so the number no longer identifies only the original entity.",
                "New in this read: City plumbing permit PP20260320064 at 1847 47th Av (94122) completed 2026-09-03, scope 'install plumbing for new bathroom at g/f. bring to code plumbing running through construction area. move gas line for forced air unit. new on demand water heater. underground plumbing.' - a bathroom-plumbing scope on a B-only licence."]),
    dict(record="w7-allen-mechanical-plbg-co", lic="611082", kind="registry",
         entity="ALLEN MECHANICAL PLUMBING CO", form="Sole Ownership",
         addr="2236 Derry Way, So San Francisco, CA 94080-5505", phone="(415) 559-1051",
         issued="01/27/1991", status="active", status_text="This license is current and active.",
         expires="2027-01-31", classes=["C36"], trade="plumbing",
         area="sunset",
         area_text="The registry lead this record was built from already printed licence number 611082, and CSLB now confirms the number as an active C36 plumbing licence to 01/31/2027. CSLB's own address is in South San Francisco, so the record still stands only on the City's own permit-contact rows for the 94122 firm address.",
         facts=["Re-read 2026-09-15: 'current and active', C36 Plumbing, sole ownership at 2236 Derry Way, South San Francisco, expiring 01/31/2027 - this closes the stored record's published gap that registry licence 611082 had NOT been read on CSLB.",
                "New in this read: the licence has been held by the same sole owner since 01/27/1991 and workers' compensation is exempt (no employees certified 01/27/2025), so no crew can be verified from the page.",
                "New in this read: the City roll-up carries 60 permit rows under a 94122 firm ZIP, so the Outer Sunset link remains permit-history evidence and not a regulator-recorded address."]),
    dict(record="w6-ocean-air-heating", lic="968927", kind="registry",
         entity="OCEAN AIR HEATING", form="Sole Ownership",
         addr="58 West Portal #153, San Francisco, CA 94127", phone="(415) 867-0846",
         issued="01/04/2012", status="active", status_text="This license is current and active.",
         expires="2028-01-31", classes=["C20"], trade="scope-exclusion",
         area="sunset",
         area_text="The registry lead this record was built from already printed licence number 968927, and CSLB now confirms the number as an active C20 licence to 01/31/2028. CSLB records the licence at 58 West Portal #153, 94127, while the registry row that surfaced it carries 1859 42nd Av, 94122; the difference is published and not resolved.",
         facts=["Re-read 2026-09-15: 'current and active', C20 Warm-Air Heating, Ventilating and Air-Conditioning only, sole ownership, expiring 01/31/2028 - this closes the stored record's published gap that registry licence 968927 had NOT been read on CSLB.",
                "New in this read: the regulator address is 58 West Portal #153, San Francisco 94127 and the registry row records 1859 42nd Av, 94122. Both are published, and neither is treated as a dispatch promise.",
                "New in this read: C20 covers neither plumbing nor drywall, so the record is a documented scope exclusion; workers' compensation runs to 12/15/2026 on code 51873 and the contractor's bond is Philadelphia Indemnity PB10163413328 effective 07/19/2026."]),

    dict(record="w10-macro-builder-inc", lic="797077", kind="registry",
         entity="MACRO BUILDER INC", form="Corporation",
         addr="1883 19th Ave, San Francisco, CA 94122", phone="(415) 760-6633",
         issued="07/03/2001", status="active", status_text="This license is current and active.",
         expires="2027-07-31", classes=["B"], trade="general", area="outer",
         area_text="CSLB itself records licence 797077 as MACRO BUILDER INC at 1883 19th Ave, San Francisco 94122 - a regulator-recorded Outer Sunset address - active to 07/31/2027 with a B classification. The registry rows that first surfaced this firm carry this address and 2121 19th Av, both in 94122.",
         facts=["Re-read 2026-09-15: 'current and active', B General Building, corporation at 1883 19th Ave, 94122, expiring 07/31/2027 - this closes the stored record's published gap that registry licence 797077 had NOT been read on CSLB.",
                "New in this read: the regulator address 1883 19th Ave matches the City building-registry row already cited in the stored record (123 permit rows) and the plumbing-registry row cited 2121 19th Av (158 rows); both addresses sit in 94122 and both are published.",
                "New in this read: workers' compensation is exempt because no employees were certified on 12/22/2025 and the contractor's bond is Western Surety 67670913 effective 10/27/2025; the licence holds B only, so the plumbing half of this project cannot be self-performed under it."]),
]

# --------------------------------------------------------------- helpers -----
def norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()


DROP = {"inc", "llc", "ltd", "co", "corp", "company", "incorporated", "corporation", "the"}


def core(value: str) -> str:
    words = [w for w in norm(value).split() if w not in DROP]
    return " ".join(words)


def licence_source(number: str, entity: str, sid: int) -> dict:
    return {
        "id": sid, "kind": "government", "access": "page", "url": CSLB + number,
        "title": f"CSLB LicenseDetail - licence {number} - {entity}",
        "checkedAt": DATE,
        "note": "Read directly on 2026-09-15. The page states 'Data current as of 9/15/2026'; every field stored on this record is copied from it.",
    }


def permit_url(permit: str) -> str:
    return DBI + "k6kv-9kix.json?%24where=permit_number=%27" + permit + "%27"


def build() -> dict:
    research = json.loads((ROOT / "data" / "research.json").read_text())
    stored = research["businesses"]
    stored_ids = {b["id"] for b in stored}
    stored_names = {norm(b["name"]) for b in stored}
    stored_cores = {core(b["name"]) for b in stored}
    stored_licences = {str(b["license"]["number"]) for b in stored if b.get("license")}

    sources = [dict(s) for s in SOURCES]
    next_src = 538
    businesses, reviews = [], []
    review_no = 148

    for r in READS:
        number = r["lic"]
        if number in stored_licences:
            raise SystemExit(f"licence {number} is already stored; it belongs in UPGRADES, not READS")
        if r["name"] in {b["name"] for b in businesses}:
            raise SystemExit(f"duplicate name inside the wave: {r['name']}")
        if core(r["name"]) in stored_cores and r.get("name_collision") is None:
            raise SystemExit(f"name core collision for {r['name']}")
        if r.get("name_collision") and r["name_collision"] not in stored_ids:
            raise SystemExit(f"{r['id_fix'] if 'id_fix' in r else r['name']} declares a collision with an unknown record")
        src = licence_source(number, r["entity"], next_src)
        next_src += 1
        sources.append(src)
        bid = f"w13-{number}"
        active = r["status"] == "active"
        exp = r["expire"]
        if "/" in exp:  # CSLB prints MM/DD/YYYY; store ISO so every date sorts
            mm, dd, yyyy = exp.split("/")
            exp = f"{yyyy}-{mm}-{dd}"
        area, area_text = "outside", (
            f"Regulator-read business address: {r['addr']}."
        )
        if "94122" in r["addr"]:
            area = "outer"
            area_text = (
                f"CSLB itself records this licensee at an Outer Sunset address ({r['addr']}), which is "
                "regulator-recorded location evidence rather than a dispatch promise."
            )
        elif r.get("permit"):
            area = "outer"
            area_text = (
                f"Outer Sunset by work address: completed City permit {r['permit'][0]} at {r['permit'][1]}, 94122. "
                f"The firm's regulator-read address is {r['addr']}."
            )
        elif "94116" in r["addr"]:
            area = "sunset"
            area_text += " The address is in ZIP 94116 (Inner Sunset side of the boundary), not the Outer Sunset."

        flags = []
        for level, text in r["extras"]:
            flags.append({"level": level, "text": text, "sources": [src["id"]] + ([] if r.get("permit") is None else [529])})
        if not active:
            flags.append({
                "level": "hold",
                "text": f"CSLB status: {r.get('status_text', 'not active')} The licence cannot lawfully contract, so the record is held regardless of any registry history.",
                "sources": [src["id"]],
            })
        if r.get("hold"):
            flags.append({"level": "hold", "text": r["hold"], "sources": [src["id"]]})

        claims = [{
            "field": "Regulator read",
            "text": f"CSLB licence {number}: {r.get('status_text', 'This license is current and active.')} Entity {r['entity']} ({r['form']}), classifications {', '.join(r['classes'])}, expiry {exp}, bond {r['bond']}, workers' compensation {r['wc']}.",
            "source": src["id"],
            "excerpt": f"{r['entity']} - {r['addr']} - {r['form']} - issued {r['issue']}"
                       + (f" - reissued {r['reissue']}" if r.get("reissue") else "")
                       + f" - expire {exp} - classifications {', '.join(r['classes'])}",
        }]
        src_ids = [src["id"]]
        if r.get("permit"):
            permit, street, desc, done = r["permit"]
            claims.append({
                "field": "Outer Sunset permit",
                "text": f"City plumbing permit {permit} at {street} (94122) completed {done}: {desc}",
                "source": 529,
                "excerpt": f"{permit} - {street} - status complete - completed {done} - \"{desc}\"",
            })
            src_ids.append(529)
        reg = r["registry"]
        claims.append({
            "field": "Registry cross-check",
            "text": "City registry row read for this wave: " + " ".join(str(x) for x in reg)
                    + " A registry row is a City record, not a regulator fact.",
            "source": 527,
            "excerpt": " - ".join(str(x) for x in reg if x),
        })

        gaps = [
            "No seized-overflow or trip-lever extraction case is verified for this firm.",
            "No written repair-first scope, stop-and-review point or certificate of insurance has been obtained.",
            "Nothing read in this wave confirms present Outer Sunset dispatch or scheduling capacity.",
        ]
        if not active:
            gaps.insert(0, "The licence is not active, so no lawful contract is possible under this number.")

        businesses.append({
            "id": bid, "name": r["name"], "trade": r["trade"], "website": None, "websiteSource": None,
            "area": area, "areaText": area_text, "status": "research" if active else "hold",
            "checkedAt": DATE, "phone": r["phone"], "phoneSource": src["id"],
            "claims": claims, "license": {
                "number": number, "status": r["status"], "entity": r["entity"],
                "expires": exp, "classes": r["classes"], "source": src["id"], "checkedAt": DATE,
            },
            "reviewIds": [], "platformLinks": ([{"label": f"SF DBI permit contact - {r['permit'][0]}", "url": permit_url(r["permit"][0]), "source": 529}] if r.get("permit") else []),
            "flags": flags, "gaps": gaps, "priority": None, "exactMatch": False, "master": False,
            "insuranceVerified": False, "scopeConfirmed": False,
            "rationale": "Wave-13 research record: a direct CSLB read paired with the City permit or registry rows that place the licence. It is not part of the diagnostic call order and is not in the qualified master.",
            "nextStep": "Confirm in writing which licensee performs each part of the work, that the named technician has extracted a seized bathtub linkage in an older assembly, and that ceiling restoration and any access opening are covered by the classifications actually held.",
        })

    # ------------------------------------------------------- registry leads --
    for number, name, addr, zipp, rows, alias in LEADS:
        if core(name) in stored_cores or norm(name) in stored_names:
            raise SystemExit(f"registry lead name collision: {name}")
        businesses.append({
            "id": f"w13-reg-{number}", "name": name, "trade": "registry-lead", "website": None, "websiteSource": None,
            "area": "sunset" if (zipp or "").startswith("94122") else "unknown",
            "areaText": f"City registry records licence number {number} under this firm name"
                        + (f" at {addr}, ZIP {zipp}" if addr else "")
                        + f", on {rows} permit rows in the 94122 roll-up. A recorded licence number is not a licence read, and a recorded address is not a dispatch confirmation.",
            "status": "hold", "checkedAt": DATE, "phone": None, "phoneSource": None,
            "claims": [{
                "field": "Registry",
                "text": f"Registry row read 2026-09-15: licence number {number} is printed under the firm name '{name}'"
                        + (f" at firm address {addr}, ZIP {zipp}" if addr else " with a 94122 firm ZIP in the count-ordered roll-up")
                        + f", across {rows} permit rows.",
                "source": 527,
                "excerpt": f"{number} - {name} - " + (f"{addr} - {zipp} - " if addr else "") + f"{rows} permit rows",
            }],
            "license": None, "reviewIds": [], "platformLinks": [],
            "flags": [
                {"level": "hold", "text": f"Not verified against the regulator: licence number {number} was read only in the City registry. No CSLB page was opened for it in this wave, so no classification, status, entity or expiry is asserted anywhere on this record, and this trade label can never satisfy a promotion gate.", "sources": [527]},
                {"level": "gap", "text": "Both trades this project requires remain unverified, no review sample was attributable to this firm, and Outer Sunset dispatch is unproven.", "sources": [527]},
                {"level": "discrepancy", "text": alias, "sources": [527]},
            ],
            "gaps": [
                "No CSLB page read: classification, status and expiry are unknown for this record.",
                "No evidence that the firm performs plumbing, drywall or ceiling restoration as of this date.",
            ],
            "priority": None, "exactMatch": False, "master": False, "insuranceVerified": False, "scopeConfirmed": False,
            "rationale": "Wave-13 registry-tier lead: a City-recorded firm name, licence number and 94122 firm address, published as a lead only. It cannot satisfy the promotion gate because it carries no regulator-backed classification.",
            "nextStep": "Read the CSLB licence page for the recorded number before treating this firm as a possible contractor, then confirm area, both trades, insurance and scope in writing.",
        })

    # ------------------------------------------------------ platform tier ----
    for p in PLATFORM:
        if core(p["name"]) in stored_cores or norm(p["name"]) in stored_names:
            raise SystemExit(f"platform name collision: {p['name']}")
        bid = f"w13-plat-{p['key']}"
        rec = {
            "id": bid, "name": p["name"], "trade": "platform-listing", "website": None, "websiteSource": None,
            "area": "sf",
            "areaText": "Platform statement only: the listing says it serves San Francisco, CA. The Outer Sunset is not named on the listing and no licence or dispatch fact is published.",
            "status": "hold", "checkedAt": DATE, "phone": None, "phoneSource": None,
            "claims": [{
                "field": "Platform listing",
                "text": f"Thumbtack listing read directly on 2026-09-15: category '{p['category']}', {p['rating']}, {p['hires']}."
                        + (" Labels shown: " + "; ".join(p["labels"]) + "." if p["labels"] else ""),
                "source": p["src"],
                "excerpt": f"{p['name']} - {p['category']} - {p['rating']} - {p['hires']}",
            }],
            "license": None, "reviewIds": [],
            "platformLinks": [{"label": f"Thumbtack listing - {p['category']}", "url": p["url"], "source": p["src"]}],
            "flags": [
                {"level": "hold", "text": "Platform listing only: no CSLB page was read and the listing publishes no licence number, so neither required trade is verified and the platform's own badge cannot be checked.", "sources": [p["src"]]},
                {"level": "gap", "text": f"Listing data as read: {p['rating']}; {p['hires']}. Platform ratings and hire counts are platform measures and are never copied into a ranking on this site.", "sources": [p["src"]]},
            ] + [{"level": "gap", "text": text, "sources": [p["src"]]} for text in p["extras"]],
            "gaps": [
                "No licence number, classification or status is published on the listing.",
                "No verified case of seized trip-lever extraction, ceiling access or drywall restoration at an Outer Sunset address.",
            ],
            "priority": None, "exactMatch": False, "master": False, "insuranceVerified": False, "scopeConfirmed": False,
            "rationale": "Wave-13 platform record, read directly from a Thumbtack category page. It is stored so its review text can be quoted verbatim and reviewed, and it can never satisfy the promotion gate because no regulator source exists for it.",
            "nextStep": "Ask the business directly for its licence number, classification and certificate of insurance; do not treat the platform badge or rating as either.",
        }
        if p["review"]:
            rid = f"R{review_no}"
            review_no += 1
            rec["reviewIds"].append(rid)
            reviews.append({
                "id": rid, "business": bid, "platform": "Thumbtack", "author": p["review"][0], "published": None,
                "quote": p["review"][1], "analysis": p["review"][2],
                "theme": "Wall or ceiling repair" if "wall" in p["review"][1].lower() or "ceiling" in p["review"][1].lower() else "Plumbing and surface work",
                "source": p["src"], "access": "page", "identity": "matched",
                "negative": p["key"] == "city-handyman", "checkedAt": DATE, "exactTask": False,
            })
        businesses.append(rec)

    # ------------------------------------------------------- upgrades --------
    upgrade_out = []
    for u in UPGRADES:
        if u["record"] not in stored_ids:
            raise SystemExit(f"upgrade target {u['record']} is not a stored record")
        target = next(b for b in stored if b["id"] == u["record"])
        if u["kind"] != "unresolved-identity" and str((target.get("license") or {}).get("number")) not in {"None", u["lic"]}:
            raise SystemExit(f"upgrade target {u['record']} carries a different licence number")
        if u["lic"] in stored_licences and u["kind"] == "registry" and (target.get("license") or {}).get("number") != u["lic"]:
            raise SystemExit(f"licence {u['lic']} already exists as a licence fact on another record")
        if u["lic"] in {r["lic"] for r in READS}:
            raise SystemExit(f"licence {u['lic']} is both a new record and an upgrade")
        src = licence_source(u["lic"], u["entity"], next_src)
        next_src += 1
        sources.append(src)
        entry = {
            "record": u["record"], "lic": u["lic"], "kind": u["kind"], "entity": u["entity"],
            "form": u["form"], "address": u["addr"], "phone": u["phone"], "issued": u["issued"],
            "status": u["status"], "statusText": u["status_text"], "expires": u["expires"],
            "classes": u["classes"], "source": src["id"], "checkedAt": DATE,
            "facts": u["facts"], "claims": [
                {
                    "field": "Insurance & bond" if re.search(r"bond|workers|compensation|policy", fact, re.I) else "Verification upgrade",
                    "text": fact, "source": src["id"], "excerpt": fact,
                }
                for fact in u["facts"]
            ],
            "flags": [{"level": "hold" if u.get("hold") else "gap", "text": u.get("hold") or u["facts"][0], "sources": [src["id"]]}],
        }
        for optional in ("trade", "area", "area_text"):
            if u.get(optional):
                entry[optional] = u[optional]
        upgrade_out.append(entry)

    # ------------------------------------------------------- invariants ------
    if len(businesses) != 50:
        raise SystemExit(f"wave 13 must contain 50 new records, found {len(businesses)}")
    if len({b["id"] for b in businesses}) != 50 or len({core(b['name']) for b in businesses}) != 50:
        raise SystemExit("wave-13 ids or name cores are not unique")
    if any(b["master"] for b in businesses):
        raise SystemExit("wave 13 must not promote anything")
    if len(upgrade_out) != 34:
        raise SystemExit(f"wave 13 must carry 34 upgrades, found {len(upgrade_out)}")
    for b in businesses:
        if b["status"] not in {"research", "hold"}:
            raise SystemExit(f"{b['id']} carries an unexpected status")
        if b["license"]:
            s = next(s for s in sources if s["id"] == b["license"]["source"])
            if s["kind"] != "government" or "cslb.ca.gov" not in s["url"] or not s["url"].endswith(b["license"]["number"]):
                raise SystemExit(f"{b['id']} licence claim is not backed by the matching CSLB source")
            if b["license"]["status"] == "active" and not b["license"]["expires"] > DATE:
                raise SystemExit(f"{b['id']} is active but does not expire after the check date")
            if b["license"]["status"] != "active" and not any(f["level"] == "hold" for f in b["flags"]):
                raise SystemExit(f"{b['id']} holds a non-active licence without a hold flag")
        else:
            if not any(f["level"] == "hold" for f in b["flags"]):
                raise SystemExit(f"{b['id']} carries no licence and no hold")
            if not b["trade"] in {"registry-lead", "platform-listing"}:
                raise SystemExit(f"{b['id']} carries no licence and an unexpected trade")
        for f in b["flags"]:
            if f["level"] not in {"hold", "discrepancy", "notice", "gap"} or not f["sources"]:
                raise SystemExit(f"{b['id']} has a malformed flag")
    for r in reviews:
        if r["exactTask"] or len(r["quote"]) >= 500:
            raise SystemExit(f"{r['id']} is malformed")

    return {
        "wave": WAVE, "date": DATE, "schemaVersion": 2,
        "note": (
            "Wave 13 adds 50 non-duplicate records from three evidence channels that are named on every record: "
            "25 direct CSLB licence reads, each paired with the City permit or registry rows that place the licence; "
            "13 registry-only leads whose City-recorded licence number was never promoted into a licence fact; and "
            "12 Thumbtack listings read directly, labelled platform-listing and never credited with a licence. "
            "Twenty-seven further CSLB pages were read for licences earlier waves had already stored: fourteen refresh a "
            "standing verification, five close a gap the stored record itself published as 'NOT read on CSLB' - two of them "
            "negatively (an inactive plumbing licence and a plumbing licence cancelled by request) - and eight re-read "
            "wave-6 licences whose regulator page now shows a bond or policy cancellation date. "
            "Eight review excerpts are retained verbatim with author, platform and analysis. Nothing is promoted to the qualified master."
        ),
        "composition": {
            "cslbReads": len(READS),
            "cslbUpgrades": len(UPGRADES),
            "cslbNewRecords": len(READS),
            "verificationUpgrades": len([u for u in UPGRADES if u["kind"] == "verification"]),
            "registryUpgrades": len([u for u in UPGRADES if u["kind"] == "registry"]),
            "unresolvedIdentityUpgrades": len([u for u in UPGRADES if u["kind"] == "unresolved-identity"]),
            "registryOnly": len(LEADS),
            "platformListings": len(PLATFORM),
            "newRecords": len(businesses),
            "retainedReviewExcerpts": len(reviews),
            "activeLicenses": sum(1 for r in READS if r["status"] == "active") + sum(1 for u in UPGRADES if u["status"] == "active"),
            "nonActiveLicenses": sum(1 for r in READS if r["status"] != "active") + sum(1 for u in UPGRADES if u["status"] != "active"),
        },
        "sources": sources,
        "businesses": businesses,
        "reviews": reviews,
        "upgrades": upgrade_out,
        "falseClaimsRejected": [
            "Thumbtack 'Licensed pro' badges were never converted into licence facts: several listings carry the badge or a Top Pro label and not one was stored with a licence number, class or status.",
            "Homeowner's Permit rows (licence 000001) appeared in the permit-contact lookups and were rejected, not stored as businesses.",
            "The registry licence number on each of the 15 leads was deliberately left unpromoted: no record in that tier asserts a classification, even where the firm name suggests plumbing.",
            "Licence 608902 appears in the City registry under both a person's name and a company's name; it was not stored as the company's credential and the stored record keeps asserting no licence fact.",
            "A platform review that named a different tradesperson than the listing's own profile was rejected rather than attached, following the rule applied in waves 4, 7 and 12.",
        ],
        "dedupeRejections": [
            "Seven licences read this wave were already stored from waves 8-10 and were published as dated verification upgrades instead of new businesses: 1141495, 754201, 893710, 1059074, 1140051, 1026009 and 899541.",
            "Five registry leads stored in waves 6-10 published the gap that their licence number had never been read at the regulator. Those numbers were read this wave (893929, 978867, 775086, 792165 and 608902) and answered on the existing records rather than as new entries.",
            "Bautista Drywall, THWC home improvement, Dr. Drain Plumbing and Rooter, Plumbing & Rooter Service (Antonio Carcamo Reyes), Dom's plumbing, Discount Plumbing Rooter Services and J. Gomez appear on the Thumbtack pages read today and already exist in the corpus, so no new record was created for any of them.",
            "Licence 839447 (a previously stored 'Feng K Plumbing Co') and licence 984413 ('Feng K Plumbing Corp dba Xin Feng Plumbing') share a near-identical name but are different numbers, addresses and individuals; both are published with the collision flagged.",
            "Wave 12's platform record 'Mission Home Remodeling' and this wave's regulator read 'Mission Home Remodeling Inc' (licence 1078954) are stored as two records: the wave-12 record carries no address and the identity link is unverifiable from any source read so far.",
        ],
        "taskEvidence": {
            "seizedOverflowExtraction": 0,
            "ceilingAccessOrHatchWork": 0,
            "oldAssemblyOrGalvanisedEvidence": 0,
            "note": "No record in this wave carries a verified case of a seized bathtub trip lever, a ceiling access hatch or galvanised-pipe repair. Where a review is adjacent - walls rebuilt after remediation, old frozen shut-off valves, a stucco hole repaired - the analysis states exactly what it does and does not support.",
        },
    }


def main() -> int:
    data = build()
    out = ROOT / "data" / "wave13.json"
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"wave 13 written: {len(data['businesses'])} records, {len(data['sources'])} sources, "
          f"{len(data['reviews'])} reviews, {len(data['upgrades'])} upgrades")
    print(json.dumps(data["composition"], indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
