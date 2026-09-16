# Wave 16 discovery log — 50 new records: 25 direct CSLB reads, 10 registry-only rows, 15 platform/community listings

Checked 2026-09-16. Every record below was compared against all 743 earlier records on id, normalized legal name, stripped name core, licence number and ten-digit phone before it was kept. Every licence fact comes from a live CSLB LicenseDetail page opened that day and transcribed field by field (business information, entity, issue/expiry, status line, classifications, bond, workers compensation, and the liability line where one is printed). Every registry row comes from the official SF DBI open-data endpoints queried that day. Every platform or community line comes from a page read that day. All 50 records are held: `priority` null, `exactMatch` false, `insuranceVerified` false, `scopeConfirmed` false, `master` false. Nothing in this wave enters the call order or the qualified master.

## Tier 1 — 25 licences read line by line on CSLB (sources 638–662)

| # | Business | Licence | Class | Status | CSLB address as printed | Expires |
| ---: | --- | ---: | --- | --- | --- | --- |
| 1 | Thomas Engel | 1000783 | B | active | 1492 36TH AVE, SAN FRANCISCO, CA 94122. | 2027-02-28 |
| 2 | Kenneth Chou | 1003699 | B | inactive | 1430 28TH AVENUE, SAN FRANCISCO, CA 94122. | 2027-05-31 |
| 3 | Reichart Construction | 1006197 | B | active | 1540 GREAT HIGHWAY 14, SAN FRANCISCO, CA 94122. | 2027-08-31 |
| 4 | Nbay Construction | 1008172 | B | canceled | 2636 JUDAH STREET #233, SAN FRANCISCO, CA 94122. | 2023-09-18 |
| 5 | Zarin Gollogly Design & Build | 1009077 | B | expired | 1622 24TH AVENUE, SAN FRANCISCO, CA 94122. | 2025-11-30 |
| 6 | Zhuo Zhang Construction Inc | 1009112 | B | active | 1452 47TH AVENUE, SAN FRANCISCO, CA 94122. | 2027-11-30 |
| 7 | Riley Remodeling and Consulting Inc | 1014452 | B | active | 1032 IRVING STREET #436, SAN FRANCISCO, CA 94122. | 2028-05-31 |
| 8 | Chris William Construction Inc | 1018105 | B, C10 | active | 1245 LAWTON STREET, SAN FRANCISCO, CA 94122. | 2026-09-30 |
| 9 | Hybrid City Construction Inc | 1021804 | B | suspended | 251 FAXON AVENUE, SAN FRANCISCO, CA 94112. | 2026-12-31 |
| 10 | New City Construction Company | 1023648 | B, C10, C36 | active | 2309 NORIEGA ST STE 99, SAN FRANCISCO, CA 94122. | 2028-06-30 |
| 11 | Silver Lining Design Build Co | 1024550 | B | active | 1125 LAWTON STREET, SAN FRANCISCO, CA 94122. | 2028-10-31 |
| 12 | Fly Cloud Construction Inc | 1029195 | B | active | 1254 18TH AVE 3, SAN FRANCISCO, CA 94122. | 2027-06-30 |
| 13 | D-Finity Construction Inc | 1033149 | B | revoked | 1440 A 25TH AVE, SAN FRANCISCO, CA 94122. | 2024-10-29 |
| 14 | Shelter Cove Construction | 1033503 | B | expired | 1210 47TH AVE, SAN FRANCISCO, CA 94122. | 2021-12-31 |
| 15 | Actually Design Build | 1035799 | B | inactive | 1429 46TH AVENUE, SAN FRANCISCO, CA 94122. | 2030-02-28 |
| 16 | Slick Construction Inc | 1044915 | B | active | 1422 16TH AVE, SAN FRANCISCO, CA 94122. | 2027-09-30 |
| 17 | B&K Construction Inc | 1047639 | B | active | 1759 33RD AVENUE, SAN FRANCISCO, CA 94122. | 2026-12-31 |
| 18 | Jakobson Construction Inc | 1048032 | B | active | PO BOX 470253, SAN FRANCISCO, CA 94147. | 2026-12-31 |
| 19 | Jian Hua Construction | 1048617 | B | active | 1719 42ND AVENUE, SAN FRANCISCO, CA 94122. | 2027-01-31 |
| 20 | Yan Construction | 1048687 | B | active | 1433 7TH AVENUE, SAN FRANCISCO, CA 94122. | 2027-01-31 |
| 21 | CMAC Construction LLC | 1053452 | B | active | 704 CHERRY STREET, NOVATO, CA 94945. | 2027-05-31 |
| 22 | Basset Engineering | 1070288 | A | active | 2354 MARKET ST, SAN FRANCISCO, CA 94114. | 2028-10-31 |
| 23 | Dmsquare Construction 2 Inc | 1074425 | B | active | 2715 OTIS DRIVE, ALAMEDA, CA 94501. | 2027-04-30 |
| 24 | Dreamsky Construction | 1090715 | B | active | 1685 19TH AVENUE, SAN FRANCISCO, CA 94122. | 2028-04-30 |
| 25 | Sound Build | 1092217 | B, C-2 | active | 1798 GREAT HWY APT 3, SAN FRANCISCO, CA 94122. | 2028-06-30 |

### Thomas Engel — w16-1000783
- CSLB licence **1000783**, classification B, status **active**, entity Sole Ownership, expires 2027-02-28, read 2026-09-16 from source `638`.
- Area `sunset`: City permit-contact registry row in ZIP 94122 for licence 1000783 (1492 36th Ave, 8 grouped rows); CSLB business address on the same licence is 1492 36TH AVE, SAN FRANCISCO, CA 94122. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Phone printed on the CSLB page: (415) 652-3133 (source `638`).
- Claim [Discovery] (source `664`): Registry-recorded permit contact read 2026-09-16: licence 1000783, 1492 36th Ave, San Francisco 94122, across 8 grouped rows. The number was then opened at CSLB.
  - excerpt: “1000783 - Thomas Engel - 1492 36th Ave - 94122 - 8 grouped rows”
- Claim [License] (source `638`): CSLB page read 2026-09-16: current and active with classification B; issue date 02/04/2015, expire date 02/28/2027; business address as printed 1492 36TH AVE, SAN FRANCISCO, CA 94122.
  - excerpt: “Contractor's License Detail for License # 1000783”
- Claim [Bonding] (source `638`): CSLB bonding line read 2026-09-16: Merchants Bonding Company (Mutual) bond 101723325, $25,000, effective 01/08/2026.
  - excerpt: “Merchants Bonding Company (Mutual) bond 101723325, $25,000, effective 01/08/2026”
- Claim [Workers compensation] (source `638`): CSLB workers compensation line read 2026-09-16: exempt from workers compensation; certified no employees, effective 01/11/2025.
  - excerpt: “exempt from workers compensation; certified no employees, effective 01/11/2025”
- Flag (hold, sources [638]): Active licence 1000783 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- Flag (gap, sources [638, 664, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### Kenneth Chou — w16-1003699
- CSLB licence **1003699**, classification B, status **inactive**, entity Sole Ownership, expires 2027-05-31, read 2026-09-16 from source `639`.
- Area `sunset`: City permit-contact registry row in ZIP 94122 for licence 1003699 (1430 28th Av, 10 grouped plumbing rows and 9 grouped building rows); CSLB business address on the same licence is 1430 28TH AVENUE, SAN FRANCISCO, CA 94122. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Claim [Discovery] (source `663`): Registry-recorded permit contact read 2026-09-16: licence 1003699, 1430 28th Av, San Francisco 94122, across 10 grouped plumbing rows and 9 grouped building rows. The number was then opened at CSLB.
  - excerpt: “1003699 - Kenneth Chou - 1430 28th Av - 94122 - 10 grouped plumbing rows and 9 grouped building rows”
- Claim [License] (source `639`): CSLB page read 2026-09-16: inactive with classification B; issue date 05/15/2015, expire date 05/31/2027; business address as printed 1430 28TH AVENUE, SAN FRANCISCO, CA 94122.
  - excerpt: “Contractor's License Detail for License # 1003699”
- Claim [Bonding] (source `639`): CSLB bonding line read 2026-09-16: Western National Mutual Insurance Company bond W70424746752, $15,000, effective 04/10/2017, cancellation date 04/11/2018.
  - excerpt: “Western National Mutual Insurance Company bond W70424746752, $15,000, effective 04/10/2017, cancellation date 04/11/2018”
- Claim [Workers compensation] (source `639`): CSLB workers compensation line read 2026-09-16: State Compensation Insurance Fund policy 9156653, effective 04/09/2016, cancellation date 02/26/2018.
  - excerpt: “State Compensation Insurance Fund policy 9156653, effective 04/09/2016, cancellation date 02/26/2018”
- Flag (hold, sources [639]): CSLB status for licence 1003699 was read as inactive. A licence that is not current and active cannot be contracted on, so the record is held and never promoted.
- Flag (discrepancy, sources [639, 663]): CSLB prints (415) 867-0054 for licence 1003699, but the same ten digits are already stored against a different record in this dataset. The number is left unstored so two licence identities are not merged by a shared phone line.
- Flag (note, sources [639, 663]): CSLB additional status: the licence will need a contractors bond to renew active or reactivate, and will need to meet the workers compensation requirements.
- Flag (gap, sources [639, 663, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### Reichart Construction — w16-1006197
- CSLB licence **1006197**, classification B, status **active**, entity Sole Ownership, expires 2027-08-31, read 2026-09-16 from source `640`.
- Area `sunset`: City permit-contact registry row in ZIP 94122 for licence 1006197 (1540 La Playa, 2 grouped plumbing rows, 14 and 4 grouped building rows); CSLB business address on the same licence is 1540 GREAT HIGHWAY 14, SAN FRANCISCO, CA 94122. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Phone printed on the CSLB page: (415) 410-6694 (source `640`).
- Claim [Discovery] (source `663`): Registry-recorded permit contact read 2026-09-16: licence 1006197, 1540 La Playa, San Francisco 94122, across 2 grouped plumbing rows, 14 and 4 grouped building rows. The number was then opened at CSLB.
  - excerpt: “1006197 - Reichart Construction - 1540 La Playa - 94122 - 2 grouped plumbing rows, 14 and 4 grouped building rows”
- Claim [License] (source `640`): CSLB page read 2026-09-16: current and active with classification B; issue date 08/06/2015, expire date 08/31/2027; business address as printed 1540 GREAT HIGHWAY 14, SAN FRANCISCO, CA 94122.
  - excerpt: “Contractor's License Detail for License # 1006197”
- Claim [Bonding] (source `640`): CSLB bonding line read 2026-09-16: Nationwide Mutual Insurance Company bond 7901259666, $25,000, effective 07/09/2025.
  - excerpt: “Nationwide Mutual Insurance Company bond 7901259666, $25,000, effective 07/09/2025”
- Claim [Workers compensation] (source `640`): CSLB workers compensation line read 2026-09-16: exempt from workers compensation; certified no employees, effective 08/02/2025.
  - excerpt: “exempt from workers compensation; certified no employees, effective 08/02/2025”
- Flag (hold, sources [640]): Active licence 1006197 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- Flag (discrepancy, sources [640, 663]): The City registry prints 1540 La Playa while the CSLB page prints 1540 Great Highway 14 for the same licence and the same ZIP.
- Flag (gap, sources [640, 663, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### Nbay Construction — w16-1008172
- CSLB licence **1008172**, classification B, status **canceled**, entity Corporation, expires 2023-09-18, read 2026-09-16 from source `641`.
- Area `sunset`: City permit-contact registry row in ZIP 94122 for licence 1008172 (2636 Judah St 233, 16 grouped plumbing rows and 22 grouped building rows); CSLB business address on the same licence is 2636 JUDAH STREET #233, SAN FRANCISCO, CA 94122. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Claim [Discovery] (source `663`): Registry-recorded permit contact read 2026-09-16: licence 1008172, 2636 Judah St 233, San Francisco 94122, across 16 grouped plumbing rows and 22 grouped building rows. The number was then opened at CSLB.
  - excerpt: “1008172 - Nbay Construction - 2636 Judah St 233 - 94122 - 16 grouped plumbing rows and 22 grouped building rows”
- Claim [License] (source `641`): CSLB page read 2026-09-16: canceled with classification B; issue date 10/15/2015, expire date 09/18/2023; business address as printed 2636 JUDAH STREET #233, SAN FRANCISCO, CA 94122.
  - excerpt: “Contractor's License Detail for License # 1008172”
- Claim [Bonding] (source `641`): CSLB bonding line read 2026-09-16: Hudson Insurance Company bond 30007841, $15,000, effective 01/01/2016, cancellation date 02/05/2022.
  - excerpt: “Hudson Insurance Company bond 30007841, $15,000, effective 01/01/2016, cancellation date 02/05/2022”
- Claim [Workers compensation] (source `641`): CSLB workers compensation line read 2026-09-16: State Compensation Insurance Fund policy 9157965, effective 09/28/2016, cancellation date 02/22/2022.
  - excerpt: “State Compensation Insurance Fund policy 9157965, effective 09/28/2016, cancellation date 02/22/2022”
- Flag (hold, sources [641]): CSLB status for licence 1008172 was read as canceled. A licence that is not current and active cannot be contracted on, so the record is held and never promoted.
- Flag (discrepancy, sources [641, 663]): CSLB prints (415) 341-7285 for licence 1008172, but the same ten digits are already stored against a different record in this dataset. The number is left unstored so two licence identities are not merged by a shared phone line.
- Flag (note, sources [641, 663]): CSLB miscellaneous information records 09/18/2023 SECRETARY OF STATE - DISSOLUTION.
- Flag (note, sources [641, 663]): The qualifying individual CHUN ZHONG certified ownership of 10 percent or more; CSLB notes personnel listed on this licence are listed on other licences.
- Flag (gap, sources [641, 663, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### Zarin Gollogly Design & Build — w16-1009077
- CSLB licence **1009077**, classification B, status **expired**, entity Sole Ownership, expires 2025-11-30, read 2026-09-16 from source `642`.
- Area `sunset`: City permit-contact registry row in ZIP 94122 for licence 1009077 (1622 24th Avenue and 1622 24th Avenue S, 10 and 2 grouped building rows); CSLB business address on the same licence is 1622 24TH AVENUE, SAN FRANCISCO, CA 94122. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Phone printed on the CSLB page: (415) 377-0300 (source `642`).
- Claim [Discovery] (source `664`): Registry-recorded permit contact read 2026-09-16: licence 1009077, 1622 24th Avenue and 1622 24th Avenue S, San Francisco 94122, across 10 and 2 grouped building rows. The number was then opened at CSLB.
  - excerpt: “1009077 - Zarin Gollogly Design & Build - 1622 24th Avenue and 1622 24th Avenue S - 94122 - 10 and 2 grouped building rows”
- Claim [License] (source `642`): CSLB page read 2026-09-16: expired with classification B; issue date 11/18/2015, expire date 11/30/2025; business address as printed 1622 24TH AVENUE, SAN FRANCISCO, CA 94122.
  - excerpt: “Contractor's License Detail for License # 1009077”
- Claim [Bonding] (source `642`): CSLB bonding line read 2026-09-16: Old Republic Surety Company bond GCL5926879, $25,000, effective 01/01/2023.
  - excerpt: “Old Republic Surety Company bond GCL5926879, $25,000, effective 01/01/2023”
- Claim [Workers compensation] (source `642`): CSLB workers compensation line read 2026-09-16: Endurance Assurance Corporation policy EAW0000167800, effective 07/05/2024, expire 07/05/2025.
  - excerpt: “Endurance Assurance Corporation policy EAW0000167800, effective 07/05/2024, expire 07/05/2025”
- Flag (hold, sources [642]): CSLB status for licence 1009077 was read as expired. A licence that is not current and active cannot be contracted on, so the record is held and never promoted.
- Flag (hold, sources [642, 664]): The licence expiry date 11/30/2025 has passed by the read date, so the CSLB status line reads expired and not able to contract.
- Flag (gap, sources [642, 664, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### Zhuo Zhang Construction Inc — w16-1009112
- CSLB licence **1009112**, classification B, status **active**, entity Corporation, expires 2027-11-30, read 2026-09-16 from source `643`.
- Area `sunset`: City permit-contact registry row in ZIP 94122 for licence 1009112 (1452 47th Avenue and 1452 7th Avenue, 7 plumbing and 27 building rows for 47th Avenue; 9 plumbing and 2 building rows for 7th Avenue); CSLB business address on the same licence is 1452 47TH AVENUE, SAN FRANCISCO, CA 94122. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Phone printed on the CSLB page: (415) 307-0177 (source `643`).
- Claim [Discovery] (source `663`): Registry-recorded permit contact read 2026-09-16: licence 1009112, 1452 47th Avenue and 1452 7th Avenue, San Francisco 94122, across 7 plumbing and 27 building rows for 47th Avenue; 9 plumbing and 2 building rows for 7th Avenue. The number was then opened at CSLB.
  - excerpt: “1009112 - Zhuo Zhang Construction Inc - 1452 47th Avenue and 1452 7th Avenue - 94122 - 7 plumbing and 27 building rows for 47th Avenue; 9 plumbing and 2 building rows for 7th Avenue”
- Claim [License] (source `643`): CSLB page read 2026-09-16: current and active with classification B; issue date 11/19/2015, expire date 11/30/2027; business address as printed 1452 47TH AVENUE, SAN FRANCISCO, CA 94122.
  - excerpt: “Contractor's License Detail for License # 1009112”
- Claim [Bonding] (source `643`): CSLB bonding line read 2026-09-16: Western Surety Company bond 67225016, $25,000, effective 11/16/2024.
  - excerpt: “Western Surety Company bond 67225016, $25,000, effective 11/16/2024”
- Claim [Workers compensation] (source `643`): CSLB workers compensation line read 2026-09-16: State Compensation Insurance Fund policy 9336701, effective 04/14/2023, expire 04/14/2027; classification codes 5432 carpentry-high wage and 5140 electrical wiring-high wage.
  - excerpt: “State Compensation Insurance Fund policy 9336701, effective 04/14/2023, expire 04/14/2027; classification codes 5432 carpentry-high wage and 5140 electrical wiring-high wage”
- Flag (hold, sources [643]): Active licence 1009112 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- Flag (discrepancy, sources [643, 663]): The City registry stores both 1452 47th Avenue and 1452 7th Avenue against this licence; the CSLB page prints 1452 47th Avenue.
- Flag (gap, sources [643, 663, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### Riley Remodeling and Consulting Inc — w16-1014452
- CSLB licence **1014452**, classification B, status **active**, entity Corporation, expires 2028-05-31, read 2026-09-16 from source `644`.
- Area `sunset`: City permit-contact registry row in ZIP 94122 for licence 1014452 (1032 Irving Street #436, 2 grouped plumbing rows and 6 grouped building rows); CSLB business address on the same licence is 1032 IRVING STREET #436, SAN FRANCISCO, CA 94122. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Phone printed on the CSLB page: (415) 725-1525 (source `644`).
- Claim [Discovery] (source `663`): Registry-recorded permit contact read 2026-09-16: licence 1014452, 1032 Irving Street #436, San Francisco 94122, across 2 grouped plumbing rows and 6 grouped building rows. The number was then opened at CSLB.
  - excerpt: “1014452 - Riley Remodeling and Consulting Inc - 1032 Irving Street #436 - 94122 - 2 grouped plumbing rows and 6 grouped building rows”
- Claim [License] (source `644`): CSLB page read 2026-09-16: current and active with classification B; issue date 05/23/2016, expire date 05/31/2028; business address as printed 1032 IRVING STREET #436, SAN FRANCISCO, CA 94122.
  - excerpt: “Contractor's License Detail for License # 1014452”
- Claim [Bonding] (source `644`): CSLB bonding line read 2026-09-16: Merchants Bonding Company (Mutual) bond 101846030, $25,000, effective 04/18/2026.
  - excerpt: “Merchants Bonding Company (Mutual) bond 101846030, $25,000, effective 04/18/2026”
- Claim [Workers compensation] (source `644`): CSLB workers compensation line read 2026-09-16: exempt from workers compensation; certified no employees, effective 04/18/2026.
  - excerpt: “exempt from workers compensation; certified no employees, effective 04/18/2026”
- Flag (hold, sources [644]): Active licence 1014452 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- Flag (note, sources [644, 663]): The qualifying individual RICHARD LEROY RILEY certified ownership of 10 percent or more.
- Flag (gap, sources [644, 663, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### Chris William Construction Inc — w16-1018105
- CSLB licence **1018105**, classification B, C10, status **active**, entity Corporation, expires 2026-09-30, read 2026-09-16 from source `645`.
- Area `sunset`: City permit-contact registry row in ZIP 94122 for licence 1018105 (1245 Lawton St, 1 grouped plumbing row); CSLB business address on the same licence is 1245 LAWTON STREET, SAN FRANCISCO, CA 94122. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Phone printed on the CSLB page: (415) 917-9928 (source `645`).
- Claim [Discovery] (source `663`): Registry-recorded permit contact read 2026-09-16: licence 1018105, 1245 Lawton St, San Francisco 94122, across 1 grouped plumbing row. The number was then opened at CSLB.
  - excerpt: “1018105 - Chris William Construction Inc - 1245 Lawton St - 94122 - 1 grouped plumbing row”
- Claim [License] (source `645`): CSLB page read 2026-09-16: current and active with classification B + C10; issue date 09/12/2016, expire date 09/30/2026; business address as printed 1245 LAWTON STREET, SAN FRANCISCO, CA 94122.
  - excerpt: “Contractor's License Detail for License # 1018105”
- Claim [Bonding] (source `645`): CSLB bonding line read 2026-09-16: Business Alliance Insurance Company bond G80809416767, $25,000, effective 01/01/2023.
  - excerpt: “Business Alliance Insurance Company bond G80809416767, $25,000, effective 01/01/2023”
- Claim [Workers compensation] (source `645`): CSLB workers compensation line read 2026-09-16: exempt from workers compensation; certified no employees, effective 09/23/2024.
  - excerpt: “exempt from workers compensation; certified no employees, effective 09/23/2024”
- Flag (hold, sources [645]): Active licence 1018105 (B + C10) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- Flag (note, sources [645, 663]): Two qualifying individuals are listed: DAVID TD NGUYEN (effective 09/12/2016) and JOHNNY NGUYEN (effective 08/18/2022).
- Flag (note, sources [645, 663]): C10 is electrical; the licence carries no plumbing or drywall classification.
- Flag (gap, sources [645, 663, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### Hybrid City Construction Inc — w16-1021804
- CSLB licence **1021804**, classification B, status **suspended**, entity Corporation, expires 2026-12-31, read 2026-09-16 from source `646`.
- Area `sf`: City permit-contact registry row in ZIP 94122 for licence 1021804 (251 Faxon Av, 6 grouped plumbing rows and 16 grouped building rows); CSLB business address on the same licence is 251 FAXON AVENUE, SAN FRANCISCO, CA 94112. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Phone printed on the CSLB page: (415) 812-1117 (source `646`).
- Claim [Discovery] (source `663`): Registry-recorded permit contact read 2026-09-16: licence 1021804, 251 Faxon Av, San Francisco 94122, across 6 grouped plumbing rows and 16 grouped building rows. The number was then opened at CSLB.
  - excerpt: “1021804 - Hybrid City Construction Inc - 251 Faxon Av - 94122 - 6 grouped plumbing rows and 16 grouped building rows”
- Claim [License] (source `646`): CSLB page read 2026-09-16: suspended with classification B; issue date 12/15/2016, expire date 12/31/2026; business address as printed 251 FAXON AVENUE, SAN FRANCISCO, CA 94112.
  - excerpt: “Contractor's License Detail for License # 1021804”
- Claim [Bonding] (source `646`): CSLB bonding line read 2026-09-16: Hudson Insurance Company bond 30119677, $25,000, effective 09/19/2023, cancellation date 09/01/2026.
  - excerpt: “Hudson Insurance Company bond 30119677, $25,000, effective 09/19/2023, cancellation date 09/01/2026”
- Claim [Workers compensation] (source `646`): CSLB workers compensation line read 2026-09-16: Benchmark Insurance Company policy 99WCGC00009821500, effective 08/05/2026, expire 08/05/2027; classification codes 5403 carpentry-low wage and 5432 carpentry-high wage.
  - excerpt: “Benchmark Insurance Company policy 99WCGC00009821500, effective 08/05/2026, expire 08/05/2027; classification codes 5403 carpentry-low wage and 5432 carpentry-high wage”
- Flag (hold, sources [646]): CSLB status for licence 1021804 was read as suspended. A licence that is not current and active cannot be contracted on, so the record is held and never promoted.
- Flag (hold, sources [646, 663]): CSLB status line reads: License is under suspension for the following reasons: License is under Contractors Bond Suspension.
- Flag (discrepancy, sources [646, 663]): The CSLB address ZIP is 94112 while the City registry row prints 94122; the CSLB phone is (415) 812-1117 while the City row prints (415) 971-8890.
- Flag (gap, sources [646, 663, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### New City Construction Company — w16-1023648
- CSLB licence **1023648**, classification B, C10, C36, status **active**, entity Sole Ownership, expires 2028-06-30, read 2026-09-16 from source `647`.
- Area `sunset`: City permit-contact registry row in ZIP 94122 for licence 1023648 (2309 Noriega St, 1 grouped plumbing row); CSLB business address on the same licence is 2309 NORIEGA ST STE 99, SAN FRANCISCO, CA 94122. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Claim [Discovery] (source `663`): Registry-recorded permit contact read 2026-09-16: licence 1023648, 2309 Noriega St, San Francisco 94122, across 1 grouped plumbing row. The number was then opened at CSLB.
  - excerpt: “1023648 - New City Construction Company - 2309 Noriega St - 94122 - 1 grouped plumbing row”
- Claim [License] (source `647`): CSLB page read 2026-09-16: current and active with classification B + C10 + C36; issue date 02/10/2017, expire date 06/30/2028; business address as printed 2309 NORIEGA ST STE 99, SAN FRANCISCO, CA 94122.
  - excerpt: “Contractor's License Detail for License # 1023648”
- Claim [Bonding] (source `647`): CSLB bonding line read 2026-09-16: American Contractors Indemnity Company bond 100864589, $25,000, effective 06/17/2024.
  - excerpt: “American Contractors Indemnity Company bond 100864589, $25,000, effective 06/17/2024”
- Claim [Workers compensation] (source `647`): CSLB workers compensation line read 2026-09-16: exempt from workers compensation; certified no employees, effective 05/02/2026.
  - excerpt: “exempt from workers compensation; certified no employees, effective 05/02/2026”
- Flag (hold, sources [647]): Active licence 1023648 (B + C10 + C36) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- Flag (discrepancy, sources [647, 663]): CSLB prints (415) 509-5025 for licence 1023648, but the same ten digits are already stored against a different record in this dataset. The number is left unstored so two licence identities are not merged by a shared phone line.
- Flag (note, sources [647, 663]): CSLB miscellaneous information records 10/16/2023 WC EXEMPT CANCELLED-LIC INACTIVATED.
- Flag (note, sources [647, 663]): The closest new single-licence B plus C36 (plumbing) read of this wave at a 94122 address; held anyway because no attributable review, ceiling-restoration or written repair-first evidence was joined to it.
- Flag (gap, sources [647, 663, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### Silver Lining Design Build Co — w16-1024550
- CSLB licence **1024550**, classification B, status **active**, entity Corporation, expires 2028-10-31, read 2026-09-16 from source `648`.
- Area `sunset`: City permit-contact registry row in ZIP 94122 for licence 1024550 (1125 Lawton St, 1 grouped plumbing row and 7 grouped building rows); CSLB business address on the same licence is 1125 LAWTON STREET, SAN FRANCISCO, CA 94122. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Phone printed on the CSLB page: (303) 819-3086 (source `648`).
- Claim [Discovery] (source `663`): Registry-recorded permit contact read 2026-09-16: licence 1024550, 1125 Lawton St, San Francisco 94122, across 1 grouped plumbing row and 7 grouped building rows. The number was then opened at CSLB.
  - excerpt: “1024550 - Silver Lining Design Build Co - 1125 Lawton St - 94122 - 1 grouped plumbing row and 7 grouped building rows”
- Claim [License] (source `648`): CSLB page read 2026-09-16: current and active with classification B; issue date 03/10/2017, expire date 10/31/2028; business address as printed 1125 LAWTON STREET, SAN FRANCISCO, CA 94122.
  - excerpt: “Contractor's License Detail for License # 1024550”
- Claim [Bonding] (source `648`): CSLB bonding line read 2026-09-16: Atlantic Specialty Insurance Company bond 800273117, $25,000, effective 09/01/2026.
  - excerpt: “Atlantic Specialty Insurance Company bond 800273117, $25,000, effective 09/01/2026”
- Claim [Workers compensation] (source `648`): CSLB workers compensation line read 2026-09-16: exempt from workers compensation; certified no employees, effective 09/08/2026.
  - excerpt: “exempt from workers compensation; certified no employees, effective 09/08/2026”
- Flag (hold, sources [648]): Active licence 1024550 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- Flag (note, sources [648, 663]): CSLB reissue date 10/30/2018 with miscellaneous information LICENSE REISSUED TO ANOTHER ENTITY.
- Flag (note, sources [648, 663]): The qualifying individual CARL BEN SAVITZ certified ownership of 10 percent or more.
- Flag (gap, sources [648, 663, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### Fly Cloud Construction Inc — w16-1029195
- CSLB licence **1029195**, classification B, status **active**, entity Corporation, expires 2027-06-30, read 2026-09-16 from source `649`.
- Area `sunset`: City permit-contact registry row in ZIP 94122 for licence 1029195 (1254 18th Av, 10 grouped building rows); CSLB business address on the same licence is 1254 18TH AVE 3, SAN FRANCISCO, CA 94122. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Phone printed on the CSLB page: (415) 879-6118 (source `649`).
- Claim [Discovery] (source `664`): Registry-recorded permit contact read 2026-09-16: licence 1029195, 1254 18th Av, San Francisco 94122, across 10 grouped building rows. The number was then opened at CSLB.
  - excerpt: “1029195 - Fly Cloud Construction Inc - 1254 18th Av - 94122 - 10 grouped building rows”
- Claim [License] (source `649`): CSLB page read 2026-09-16: current and active with classification B; issue date 07/24/2017, expire date 06/30/2027; business address as printed 1254 18TH AVE 3, SAN FRANCISCO, CA 94122.
  - excerpt: “Contractor's License Detail for License # 1029195”
- Claim [Bonding] (source `649`): CSLB bonding line read 2026-09-16: American Contractors Indemnity Company bond 100754712, $25,000, effective 06/23/2023.
  - excerpt: “American Contractors Indemnity Company bond 100754712, $25,000, effective 06/23/2023”
- Claim [Workers compensation] (source `649`): CSLB workers compensation line read 2026-09-16: exempt from workers compensation; certified no employees, effective 05/09/2025.
  - excerpt: “exempt from workers compensation; certified no employees, effective 05/09/2025”
- Flag (hold, sources [649]): Active licence 1029195 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- Flag (note, sources [649, 664]): CSLB reissue date 06/23/2023 with miscellaneous information LICENSE REISSUED TO ANOTHER ENTITY.
- Flag (discrepancy, sources [649, 664]): The City registry row prints phone (415) 350-9953 for this licence; the CSLB page prints (415) 879-6118.
- Flag (gap, sources [649, 664, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### D-Finity Construction Inc — w16-1033149
- CSLB licence **1033149**, classification B, status **revoked**, entity Corporation, expires 2024-10-29, read 2026-09-16 from source `650`.
- Area `sunset`: City permit-contact registry row in ZIP 94122 for licence 1033149 (1440 25th Av A, 16 grouped plumbing rows and 21 grouped building rows); CSLB business address on the same licence is 1440 A 25TH AVE, SAN FRANCISCO, CA 94122. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Phone printed on the CSLB page: (415) 806-5888 (source `650`).
- Claim [Discovery] (source `663`): Registry-recorded permit contact read 2026-09-16: licence 1033149, 1440 25th Av A, San Francisco 94122, across 16 grouped plumbing rows and 21 grouped building rows. The number was then opened at CSLB.
  - excerpt: “1033149 - D-Finity Construction Inc - 1440 25th Av A - 94122 - 16 grouped plumbing rows and 21 grouped building rows”
- Claim [License] (source `650`): CSLB page read 2026-09-16: revoked with classification B; issue date 11/20/2017, expire date 10/29/2024; business address as printed 1440 A 25TH AVE, SAN FRANCISCO, CA 94122.
  - excerpt: “Contractor's License Detail for License # 1033149”
- Claim [Bonding] (source `650`): CSLB bonding line read 2026-09-16: Hudson Insurance Company bond 30049985, $25,000, effective 01/01/2023, cancellation date 09/07/2024.
  - excerpt: “Hudson Insurance Company bond 30049985, $25,000, effective 01/01/2023, cancellation date 09/07/2024”
- Claim [Workers compensation] (source `650`): CSLB workers compensation line read 2026-09-16: exempt from workers compensation; certified no employees, effective 04/03/2024.
  - excerpt: “exempt from workers compensation; certified no employees, effective 04/03/2024”
- Flag (hold, sources [650]): CSLB status for licence 1033149 was read as revoked. A licence that is not current and active cannot be contracted on, so the record is held and never promoted.
- Flag (hold, sources [650, 663]): CSLB status line reads: This license is revoked and not able to contract at this time.
- Flag (note, sources [650, 663]): The CSLB page also links complaint disclosure and states there is complaint disclosure information for this licence. The complaint page itself was not opened in this wave, so no allegation is characterised here.
- Flag (note, sources [650, 663]): The qualifying individual DAVID SIUMAN TANG certified ownership of 10 percent or more.
- Flag (gap, sources [650, 663, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### Shelter Cove Construction — w16-1033503
- CSLB licence **1033503**, classification B, status **expired**, entity Partnership, expires 2021-12-31, read 2026-09-16 from source `651`.
- Area `sunset`: City permit-contact registry row in ZIP 94122 for licence 1033503 (1210 47th Av, 9 grouped building rows); CSLB business address on the same licence is 1210 47TH AVE, SAN FRANCISCO, CA 94122. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Phone printed on the CSLB page: (415) 640-3970 (source `651`).
- Claim [Discovery] (source `664`): Registry-recorded permit contact read 2026-09-16: licence 1033503, 1210 47th Av, San Francisco 94122, across 9 grouped building rows. The number was then opened at CSLB.
  - excerpt: “1033503 - Shelter Cove Construction - 1210 47th Av - 94122 - 9 grouped building rows”
- Claim [License] (source `651`): CSLB page read 2026-09-16: expired with classification B; issue date 12/01/2017, expire date 12/31/2021; business address as printed 1210 47TH AVE, SAN FRANCISCO, CA 94122.
  - excerpt: “Contractor's License Detail for License # 1033503”
- Claim [Bonding] (source `651`): CSLB bonding line read 2026-09-16: Navigators Insurance Company bond NAV00011485, $15,000, effective 11/10/2019, cancellation date 11/11/2021.
  - excerpt: “Navigators Insurance Company bond NAV00011485, $15,000, effective 11/10/2019, cancellation date 11/11/2021”
- Claim [Workers compensation] (source `651`): CSLB workers compensation line read 2026-09-16: State Compensation Insurance Fund policy 9231998, effective 05/22/2019, expire 05/22/2022.
  - excerpt: “State Compensation Insurance Fund policy 9231998, effective 05/22/2019, expire 05/22/2022”
- Flag (hold, sources [651]): CSLB status for licence 1033503 was read as expired. A licence that is not current and active cannot be contracted on, so the record is held and never promoted.
- Flag (note, sources [651, 664]): The licence expiry date 12/31/2021 has passed by the read date.
- Flag (note, sources [651, 664]): A second licence, 1082812, is also printed as Shelter Cove Construction at 1210 47th Av in the City registry; it was not read in this wave and is not stored.
- Flag (gap, sources [651, 664, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### Actually Design Build — w16-1035799
- CSLB licence **1035799**, classification B, status **inactive**, entity Sole Ownership, expires 2030-02-28, read 2026-09-16 from source `652`.
- Area `sunset`: City permit-contact registry row in ZIP 94122 for licence 1035799 (1359 48th Av, 21 grouped building rows; a separate row prints 1429 46th Ave); CSLB business address on the same licence is 1429 46TH AVENUE, SAN FRANCISCO, CA 94122. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Phone printed on the CSLB page: (415) 243-6701 (source `652`).
- Claim [Discovery] (source `664`): Registry-recorded permit contact read 2026-09-16: licence 1035799, 1359 48th Av, San Francisco 94122, across 21 grouped building rows; a separate row prints 1429 46th Ave. The number was then opened at CSLB.
  - excerpt: “1035799 - Actually Design Build - 1359 48th Av - 94122 - 21 grouped building rows; a separate row prints 1429 46th Ave”
- Claim [License] (source `652`): CSLB page read 2026-09-16: inactive with classification B; issue date 02/12/2018, expire date 02/28/2030; business address as printed 1429 46TH AVENUE, SAN FRANCISCO, CA 94122.
  - excerpt: “Contractor's License Detail for License # 1035799”
- Claim [Bonding] (source `652`): CSLB bonding line read 2026-09-16: Suretec Insurance Company bond 138346, $25,000, effective 01/01/2023, cancellation date 01/28/2023.
  - excerpt: “Suretec Insurance Company bond 138346, $25,000, effective 01/01/2023, cancellation date 01/28/2023”
- Claim [Workers compensation] (source `652`): CSLB workers compensation line read 2026-09-16: exempt from workers compensation; effective 01/13/2020, cancellation date 03/01/2022.
  - excerpt: “exempt from workers compensation; effective 01/13/2020, cancellation date 03/01/2022”
- Flag (hold, sources [652]): CSLB status for licence 1035799 was read as inactive. A licence that is not current and active cannot be contracted on, so the record is held and never promoted.
- Flag (hold, sources [652, 664]): CSLB status is inactive and not able to contract; the additional status notes a contractors bond and workers compensation are needed to reactivate.
- Flag (discrepancy, sources [652, 664]): The City registry row prints 1359 48th Av while the CSLB page prints 1429 46th Avenue.
- Flag (note, sources [652, 664]): CSLB miscellaneous information records 10/16/2023 WC EXEMPT CANCELLED-LIC INACTIVATED.
- Flag (gap, sources [652, 664, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### Slick Construction Inc — w16-1044915
- CSLB licence **1044915**, classification B, status **active**, entity Corporation, expires 2027-09-30, read 2026-09-16 from source `653`.
- Area `sunset`: City permit-contact registry row in ZIP 94122 for licence 1044915 (1422 16th Av, 11 grouped building rows); CSLB business address on the same licence is 1422 16TH AVE, SAN FRANCISCO, CA 94122. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Phone printed on the CSLB page: (415) 940-9199 (source `653`).
- Claim [Discovery] (source `664`): Registry-recorded permit contact read 2026-09-16: licence 1044915, 1422 16th Av, San Francisco 94122, across 11 grouped building rows. The number was then opened at CSLB.
  - excerpt: “1044915 - Slick Construction Inc - 1422 16th Av - 94122 - 11 grouped building rows”
- Claim [License] (source `653`): CSLB page read 2026-09-16: current and active with classification B; issue date 09/27/2018, expire date 09/30/2027; business address as printed 1422 16TH AVE, SAN FRANCISCO, CA 94122.
  - excerpt: “Contractor's License Detail for License # 1044915”
- Claim [Bonding] (source `653`): CSLB bonding line read 2026-09-16: Atlantic Specialty Insurance Company bond 800209324, $25,000, effective 09/26/2025.
  - excerpt: “Atlantic Specialty Insurance Company bond 800209324, $25,000, effective 09/26/2025”
- Claim [Workers compensation] (source `653`): CSLB workers compensation line read 2026-09-16: American Casualty Company of Reading PA policy WC8035983569, effective 09/08/2026, expire 09/08/2027; classification codes 5432 carpentry-high wage and 5403 carpentry-low wage.
  - excerpt: “American Casualty Company of Reading PA policy WC8035983569, effective 09/08/2026, expire 09/08/2027; classification codes 5432 carpentry-high wage and 5403 carpentry-low wage”
- Flag (hold, sources [653]): Active licence 1044915 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- Flag (note, sources [653, 664]): CSLB reissue date 09/26/2019 with miscellaneous information LICENSE REISSUED TO ANOTHER ENTITY.
- Flag (note, sources [653, 664]): The qualifying individual NICHOLAS GERARD COLEMAN certified ownership of 10 percent or more.
- Flag (gap, sources [653, 664, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### B&K Construction Inc — w16-1047639
- CSLB licence **1047639**, classification B, status **active**, entity Corporation, expires 2026-12-31, read 2026-09-16 from source `654`.
- Area `sunset`: City permit-contact registry row in ZIP 94122 for licence 1047639 (1759 1759 33rd Av, 3 grouped plumbing rows and 3 grouped building rows); CSLB business address on the same licence is 1759 33RD AVENUE, SAN FRANCISCO, CA 94122. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Claim [Discovery] (source `663`): Registry-recorded permit contact read 2026-09-16: licence 1047639, 1759 1759 33rd Av, San Francisco 94122, across 3 grouped plumbing rows and 3 grouped building rows. The number was then opened at CSLB.
  - excerpt: “1047639 - B&K Construction Inc - 1759 1759 33rd Av - 94122 - 3 grouped plumbing rows and 3 grouped building rows”
- Claim [License] (source `654`): CSLB page read 2026-09-16: current and active with classification B; issue date 12/07/2018, expire date 12/31/2026; business address as printed 1759 33RD AVENUE, SAN FRANCISCO, CA 94122.
  - excerpt: “Contractor's License Detail for License # 1047639”
- Claim [Bonding] (source `654`): CSLB bonding line read 2026-09-16: Atlantic Specialty Insurance Company bond 800210107, $25,000, effective 09/05/2025.
  - excerpt: “Atlantic Specialty Insurance Company bond 800210107, $25,000, effective 09/05/2025”
- Claim [Workers compensation] (source `654`): CSLB workers compensation line read 2026-09-16: State Compensation Insurance Fund policy 9241920, effective 01/15/2019, expire 01/15/2027; classification codes 54031, 51831 plumbing-low wage and 52011 concrete-cement work-sidewalks-low wage.
  - excerpt: “State Compensation Insurance Fund policy 9241920, effective 01/15/2019, expire 01/15/2027; classification codes 54031, 51831 plumbing-low wage and 52011 concrete-cement work-sidewalks-low wage”
- Flag (hold, sources [654]): Active licence 1047639 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- Flag (discrepancy, sources [654, 663]): CSLB prints (415) 990-9431 for licence 1047639, but the same ten digits are already stored against a different record in this dataset. The number is left unstored so two licence identities are not merged by a shared phone line.
- Flag (discrepancy, sources [654, 663]): The CSLB classifications page lists B only, while the workers compensation classification codes include 51831 plumbing-low wage. The mismatch is recorded, not resolved.
- Flag (note, sources [654, 663]): The qualifying individual BO ZHONG LIANG certified ownership of 10 percent or more.
- Flag (gap, sources [654, 663, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### Jakobson Construction Inc — w16-1048032
- CSLB licence **1048032**, classification B, status **active**, entity Corporation, expires 2026-12-31, read 2026-09-16 from source `655`.
- Area `sf`: City permit-contact registry row in ZIP 94122 for licence 1048032 (1675 08th Av, 10 grouped building rows); CSLB business address on the same licence is PO BOX 470253, SAN FRANCISCO, CA 94147. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Phone printed on the CSLB page: (415) 875-0690 (source `655`).
- Claim [Discovery] (source `664`): Registry-recorded permit contact read 2026-09-16: licence 1048032, 1675 08th Av, San Francisco 94122, across 10 grouped building rows. The number was then opened at CSLB.
  - excerpt: “1048032 - Jakobson Construction Inc - 1675 08th Av - 94122 - 10 grouped building rows”
- Claim [License] (source `655`): CSLB page read 2026-09-16: current and active with classification B; issue date 12/18/2018, expire date 12/31/2026; business address as printed PO BOX 470253, SAN FRANCISCO, CA 94147.
  - excerpt: “Contractor's License Detail for License # 1048032”
- Claim [Bonding] (source `655`): CSLB bonding line read 2026-09-16: Western Surety Company bond 67292353, $25,000, effective 12/23/2024.
  - excerpt: “Western Surety Company bond 67292353, $25,000, effective 12/23/2024”
- Claim [Workers compensation] (source `655`): CSLB workers compensation line read 2026-09-16: National Liability and Fire Insurance Company policy N9WC668123, effective 04/28/2026, expire 04/28/2027.
  - excerpt: “National Liability and Fire Insurance Company policy N9WC668123, effective 04/28/2026, expire 04/28/2027”
- Flag (hold, sources [655]): Active licence 1048032 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- Flag (discrepancy, sources [655, 664]): The CSLB business address is a PO box in ZIP 94147 while the City registry row prints 1675 08th Av, 94122. No service-area claim is inferred from either.
- Flag (note, sources [655, 664]): The qualifying individual MIKAEL JAKOBSON certified ownership of 10 percent or more.
- Flag (gap, sources [655, 664, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### Jian Hua Construction — w16-1048617
- CSLB licence **1048617**, classification B, status **active**, entity Sole Ownership, expires 2027-01-31, read 2026-09-16 from source `656`.
- Area `sunset`: City permit-contact registry row in ZIP 94122 for licence 1048617 (1719 42nd St, 1 grouped plumbing row and 2 grouped building rows); CSLB business address on the same licence is 1719 42ND AVENUE, SAN FRANCISCO, CA 94122. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Phone printed on the CSLB page: (415) 760-8817 (source `656`).
- Claim [Discovery] (source `663`): Registry-recorded permit contact read 2026-09-16: licence 1048617, 1719 42nd St, San Francisco 94122, across 1 grouped plumbing row and 2 grouped building rows. The number was then opened at CSLB.
  - excerpt: “1048617 - Jian Hua Construction - 1719 42nd St - 94122 - 1 grouped plumbing row and 2 grouped building rows”
- Claim [License] (source `656`): CSLB page read 2026-09-16: current and active with classification B; issue date 01/04/2019, expire date 01/31/2027; business address as printed 1719 42ND AVENUE, SAN FRANCISCO, CA 94122.
  - excerpt: “Contractor's License Detail for License # 1048617”
- Claim [Bonding] (source `656`): CSLB bonding line read 2026-09-16: Western Surety Company bond 66864390, $25,000, effective 03/15/2024.
  - excerpt: “Western Surety Company bond 66864390, $25,000, effective 03/15/2024”
- Claim [Workers compensation] (source `656`): CSLB workers compensation line read 2026-09-16: exempt from workers compensation; certified no employees, effective 12/06/2024.
  - excerpt: “exempt from workers compensation; certified no employees, effective 12/06/2024”
- Flag (hold, sources [656]): Active licence 1048617 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- Flag (discrepancy, sources [656, 663]): The City registry row prints 1719 42nd St while the CSLB page prints 1719 42ND AVENUE.
- Flag (gap, sources [656, 663, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### Yan Construction — w16-1048687
- CSLB licence **1048687**, classification B, status **active**, entity Sole Ownership, expires 2027-01-31, read 2026-09-16 from source `657`.
- Area `sunset`: City permit-contact registry row in ZIP 94122 for licence 1048687 (1433 07th Ave, 2 grouped building rows); CSLB business address on the same licence is 1433 7TH AVENUE, SAN FRANCISCO, CA 94122. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Phone printed on the CSLB page: (415) 867-5797 (source `657`).
- Claim [Discovery] (source `664`): Registry-recorded permit contact read 2026-09-16: licence 1048687, 1433 07th Ave, San Francisco 94122, across 2 grouped building rows. The number was then opened at CSLB.
  - excerpt: “1048687 - Yan Construction - 1433 07th Ave - 94122 - 2 grouped building rows”
- Claim [License] (source `657`): CSLB page read 2026-09-16: current and active with classification B; issue date 01/07/2019, expire date 01/31/2027; business address as printed 1433 7TH AVENUE, SAN FRANCISCO, CA 94122.
  - excerpt: “Contractor's License Detail for License # 1048687”
- Claim [Bonding] (source `657`): CSLB bonding line read 2026-09-16: Merchants Bonding Company (Mutual) bond 101320809, $25,000, effective 10/30/2024.
  - excerpt: “Merchants Bonding Company (Mutual) bond 101320809, $25,000, effective 10/30/2024”
- Claim [Workers compensation] (source `657`): CSLB workers compensation line read 2026-09-16: exempt from workers compensation; certified no employees, effective 01/14/2025.
  - excerpt: “exempt from workers compensation; certified no employees, effective 01/14/2025”
- Flag (hold, sources [657]): Active licence 1048687 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- Flag (discrepancy, sources [657, 664]): The City registry row for this licence prints the malformed ZIP 941222; the CSLB page prints 94122.
- Flag (gap, sources [657, 664, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### CMAC Construction LLC — w16-1053452
- CSLB licence **1053452**, classification B, status **active**, entity Ltd Liability, expires 2027-05-31, read 2026-09-16 from source `658`.
- Area `outside`: City permit-contact registry row in ZIP 94122 for licence 1053452 (1295 41st Av, 1 grouped plumbing row and 13 grouped building rows); CSLB business address on the same licence is 704 CHERRY STREET, NOVATO, CA 94945. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Phone printed on the CSLB page: (415) 680-6036 (source `658`).
- Claim [Discovery] (source `663`): Registry-recorded permit contact read 2026-09-16: licence 1053452, 1295 41st Av, San Francisco 94122, across 1 grouped plumbing row and 13 grouped building rows. The number was then opened at CSLB.
  - excerpt: “1053452 - CMAC Construction LLC - 1295 41st Av - 94122 - 1 grouped plumbing row and 13 grouped building rows”
- Claim [License] (source `658`): CSLB page read 2026-09-16: current and active with classification B; issue date 05/13/2019, expire date 05/31/2027; business address as printed 704 CHERRY STREET, NOVATO, CA 94945.
  - excerpt: “Contractor's License Detail for License # 1053452”
- Claim [Bonding] (source `658`): CSLB bonding line read 2026-09-16: Merchants Bonding Company (Mutual) bond 101889415, $25,000, effective 05/24/2026; LLC Employee/Worker Bond with Great American Insurance Company, bond 4906454, $100,000, effective 05/24/2023.
  - excerpt: “Merchants Bonding Company (Mutual) bond 101889415, $25,000, effective 05/24/2026; LLC Employee/Worker Bond with Great American Insurance Company, bond 4906454, $100,000, effective 05/24/2023”
- Claim [Workers compensation] (source `658`): CSLB workers compensation line read 2026-09-16: Everest Premier Insurance Company policy 7600028319261, effective 07/31/2026, expire 07/31/2027; classification codes 5432 carpentry-high wage, 5403 carpentry-low wage and 5484 plastering-stucco work-low wage.
  - excerpt: “Everest Premier Insurance Company policy 7600028319261, effective 07/31/2026, expire 07/31/2027; classification codes 5432 carpentry-high wage, 5403 carpentry-low wage and 5484 plastering-stucco work-low wage”
- Claim [Liability insurance] (source `658`): CSLB liability line read 2026-09-16: Gotham Insurance Company policy GL202600040991, amount $2,000,000, effective 02/24/2026, expiration 02/24/2027.
  - excerpt: “Gotham Insurance Company policy GL202600040991, amount $2,000,000, effective 02/24/2026, expiration 02/24/2027”
- Flag (hold, sources [658]): Active licence 1053452 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- Flag (note, sources [658, 663]): CSLB reissue date 05/24/2023 with miscellaneous information LICENSE REISSUED TO ANOTHER ENTITY.
- Flag (discrepancy, sources [658, 663]): The CSLB business address is in Novato while the City registry row prints 1295 41st Av, 94122.
- Flag (discrepancy, sources [658, 663]): This is the only record of the 25 direct reads in this wave whose CSLB page prints a liability-insurance line, and it is still held: the address, the past 94122 permit rows and the absence of attributable reviews leave area and task evidence open.
- Flag (gap, sources [658, 663, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### Basset Engineering — w16-1070288
- CSLB licence **1070288**, classification A, status **active**, entity Corporation, expires 2028-10-31, read 2026-09-16 from source `659`.
- Area `sf`: City permit-contact registry row in ZIP 94122 for licence 1070288 (P.O.Box 22095, 3 grouped building rows); CSLB business address on the same licence is 2354 MARKET ST, SAN FRANCISCO, CA 94114. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Phone printed on the CSLB page: (415) 930-2385 (source `659`).
- Claim [Discovery] (source `664`): Registry-recorded permit contact read 2026-09-16: licence 1070288, P.O.Box 22095, San Francisco 94122, across 3 grouped building rows. The number was then opened at CSLB.
  - excerpt: “1070288 - Basset Engineering - P.O.Box 22095 - 94122 - 3 grouped building rows”
- Claim [License] (source `659`): CSLB page read 2026-09-16: current and active with classification A; issue date 10/26/2020, expire date 10/31/2028; business address as printed 2354 MARKET ST, SAN FRANCISCO, CA 94114.
  - excerpt: “Contractor's License Detail for License # 1070288”
- Claim [Bonding] (source `659`): CSLB bonding line read 2026-09-16: Great Midwest Insurance Company bond GM222619, $25,000, effective 12/13/2023.
  - excerpt: “Great Midwest Insurance Company bond GM222619, $25,000, effective 12/13/2023”
- Claim [Workers compensation] (source `659`): CSLB workers compensation line read 2026-09-16: An employee service group holds the workers compensation insurance; policy C58905495, effective 06/01/2025, expire 06/01/2027.
  - excerpt: “An employee service group holds the workers compensation insurance; policy C58905495, effective 06/01/2025, expire 06/01/2027”
- Flag (hold, sources [659]): Active licence 1070288 (A) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- Flag (note, sources [659, 664]): The classification is A - GENERAL ENGINEERING, not B and not C36, so it does not cover either trade this project needs.
- Flag (note, sources [659, 664]): The qualifying individual SHANE JOSEPH MCCARTHY certified ownership of 10 percent or more; CSLB notes personnel listed on this licence are listed on other licences.
- Flag (gap, sources [659, 664, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### Dmsquare Construction 2 Inc — w16-1074425
- CSLB licence **1074425**, classification B, status **active**, entity Corporation, expires 2027-04-30, read 2026-09-16 from source `660`.
- Area `outside`: City permit-contact registry row in ZIP 94122 for licence 1074425 (571 Edinburgh St, 4 grouped plumbing rows); CSLB business address on the same licence is 2715 OTIS DRIVE, ALAMEDA, CA 94501. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Phone printed on the CSLB page: (415) 806-6687 (source `660`).
- Claim [Discovery] (source `663`): Registry-recorded permit contact read 2026-09-16: licence 1074425, 571 Edinburgh St, San Francisco 94122, across 4 grouped plumbing rows. The number was then opened at CSLB.
  - excerpt: “1074425 - Dmsquare Construction 2 Inc - 571 Edinburgh St - 94122 - 4 grouped plumbing rows”
- Claim [License] (source `660`): CSLB page read 2026-09-16: current and active with classification B; issue date 04/01/2021, expire date 04/30/2027; business address as printed 2715 OTIS DRIVE, ALAMEDA, CA 94501.
  - excerpt: “Contractor's License Detail for License # 1074425”
- Claim [Bonding] (source `660`): CSLB bonding line read 2026-09-16: Western Surety Company bond 72347495, $25,000, effective 01/01/2023.
  - excerpt: “Western Surety Company bond 72347495, $25,000, effective 01/01/2023”
- Claim [Workers compensation] (source `660`): CSLB workers compensation line read 2026-09-16: exempt from workers compensation; certified no employees, effective 04/03/2025.
  - excerpt: “exempt from workers compensation; certified no employees, effective 04/03/2025”
- Flag (hold, sources [660]): Active licence 1074425 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- Flag (discrepancy, sources [660, 663]): The CSLB business address is in Alameda while the City registry row prints 571 Edinburgh St, 94122.
- Flag (note, sources [660, 663]): The qualifying individual DAN VI FUNG certified ownership of 10 percent or more.
- Flag (gap, sources [660, 663, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### Dreamsky Construction — w16-1090715
- CSLB licence **1090715**, classification B, status **active**, entity Sole Ownership, expires 2028-04-30, read 2026-09-16 from source `661`.
- Area `sunset`: City permit-contact registry row in ZIP 94122 for licence 1090715 (1685 19th Av, 7 grouped plumbing rows and 8 grouped building rows); CSLB business address on the same licence is 1685 19TH AVENUE, SAN FRANCISCO, CA 94122. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Phone printed on the CSLB page: (415) 350-9953 (source `661`).
- Claim [Discovery] (source `663`): Registry-recorded permit contact read 2026-09-16: licence 1090715, 1685 19th Av, San Francisco 94122, across 7 grouped plumbing rows and 8 grouped building rows. The number was then opened at CSLB.
  - excerpt: “1090715 - Dreamsky Construction - 1685 19th Av - 94122 - 7 grouped plumbing rows and 8 grouped building rows”
- Claim [License] (source `661`): CSLB page read 2026-09-16: current and active with classification B; issue date 04/26/2022, expire date 04/30/2028; business address as printed 1685 19TH AVENUE, SAN FRANCISCO, CA 94122.
  - excerpt: “Contractor's License Detail for License # 1090715”
- Claim [Bonding] (source `661`): CSLB bonding line read 2026-09-16: Atlantic Specialty Insurance Company bond 800233214, $25,000, effective 03/16/2026.
  - excerpt: “Atlantic Specialty Insurance Company bond 800233214, $25,000, effective 03/16/2026”
- Claim [Workers compensation] (source `661`): CSLB workers compensation line read 2026-09-16: exempt from workers compensation; certified no employees, effective 03/06/2026.
  - excerpt: “exempt from workers compensation; certified no employees, effective 03/06/2026”
- Flag (hold, sources [661]): Active licence 1090715 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- Flag (discrepancy, sources [661, 663]): The City registry prints (415) 350-9953 for both this licence and Fly Cloud Construction (1029195). The CSLB pages print (415) 350-9953 for this licence and (415) 879-6118 for 1029195, so the shared registry phone is a City-row irregularity, not a shared CSLB phone.
- Flag (gap, sources [661, 663, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

### Sound Build — w16-1092217
- CSLB licence **1092217**, classification B, C-2, status **active**, entity Corporation, expires 2028-06-30, read 2026-09-16 from source `662`.
- Area `sunset`: City permit-contact registry row in ZIP 94122 for licence 1092217 (1798 Great Hwy Apt 3, 1 grouped plumbing row and 9 grouped building rows); CSLB business address on the same licence is 1798 GREAT HWY APT 3, SAN FRANCISCO, CA 94122. The registry row is historical permit-contact evidence and the CSLB address is a mailing address, so neither proves current Outer Sunset dispatch.
- Phone printed on the CSLB page: (415) 672-2485 (source `662`).
- Claim [Discovery] (source `663`): Registry-recorded permit contact read 2026-09-16: licence 1092217, 1798 Great Hwy Apt 3, San Francisco 94122, across 1 grouped plumbing row and 9 grouped building rows. The number was then opened at CSLB.
  - excerpt: “1092217 - Sound Build - 1798 Great Hwy Apt 3 - 94122 - 1 grouped plumbing row and 9 grouped building rows”
- Claim [License] (source `662`): CSLB page read 2026-09-16: current and active with classification B + C-2; issue date 06/01/2022, expire date 06/30/2028; business address as printed 1798 GREAT HWY APT 3, SAN FRANCISCO, CA 94122.
  - excerpt: “Contractor's License Detail for License # 1092217”
- Claim [Bonding] (source `662`): CSLB bonding line read 2026-09-16: Western Surety Company bond 67695089, $25,000, effective 03/01/2026; the CSLB page links a Bond of Qualifying Individual history.
  - excerpt: “Western Surety Company bond 67695089, $25,000, effective 03/01/2026; the CSLB page links a Bond of Qualifying Individual history”
- Claim [Workers compensation] (source `662`): CSLB workers compensation line read 2026-09-16: Norguard Insurance Company policy SOWC762069, effective 02/27/2026, expire 02/27/2027; classification codes 5432 carpentry-high wage, 5403 carpentry-low wage and 9011.
  - excerpt: “Norguard Insurance Company policy SOWC762069, effective 02/27/2026, expire 02/27/2027; classification codes 5432 carpentry-high wage, 5403 carpentry-low wage and 9011”
- Flag (hold, sources [662]): Active licence 1092217 (B + C-2) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- Flag (note, sources [662, 663]): C-2 is insulation and acoustical; the licence carries no plumbing or drywall classification.
- Flag (note, sources [662, 663]): The qualifying individual BRIAN WARD VEIT is effective 05/26/2026.
- Flag (gap, sources [662, 663, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this exact licence identity in the evidence read on 2026-09-16.
- Gap: No review or job record describes a seized bathtub overflow linkage on this exact licence.
- Gap: No documented ceiling opening and drywall closeout, and no access-hatch installation evidence.
- Gap: No confirmation of current Outer Sunset dispatch, project insurance or a written repair-first scope.
- Next step: Ask for the number and verify the same details at CSLB before contracting; then confirm Outer Sunset dispatch, project insurance and a written repair-first scope with a stop-and-review point.

## Tier 2 — 10 registry-only leads (official SF DBI rows; no licence fact asserted)

### Eky Builder Inc. — w16-reg-eky-builder
- Trade `registry-lead`, status `hold`, area `sunset`.
- Claim [Registry] (source `665`): Registry-recorded building contact read 2026-09-16: firm 'Eky Builder Inc.', address 4525 Lincoln Way, Suite# A, ZIP 94122, across 26 grouped rows. The rows carry no licence number.
  - excerpt: “Eky Builder Inc. - 4525 Lincoln Way, Suite# A - 94122 - 26 rows - licence field empty”
- Flag (hold, sources [665]): Registry only: the City row records no licence number and no CSLB page was opened, so no legal entity, status, classification or expiry is asserted.
- Flag (gap, sources [665]): The registry does not say which trade was performed under these permit rows, and a permit contact row is not proof that a given firm performed a given scope.
- Flag (gap, sources [665, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this registry identity in the evidence read on 2026-09-16.
- Gap: No licence number in the City row and no direct CSLB read, so status and classification are unknown.
- Gap: No current dispatch, exact overflow, ceiling-restoration, insurance or written repair-first evidence.
- Next step: Look the firm up at CSLB and match the legal name and address before any contact; then verify dispatch, insurance and scope in writing.

### S & J Constructions Inc — w16-reg-s-and-j-constructions
- Trade `registry-lead`, status `hold`, area `sunset`.
- Claim [Registry] (source `665`): Registry-recorded building contact read 2026-09-16: firm 'S & J Constructions Inc', address 1846 - 33rd Avenue, ZIP 94122, across 32 grouped rows. The rows carry no licence number.
  - excerpt: “S & J Constructions Inc - 1846 - 33rd Avenue - 94122 - 32 rows - licence field empty”
- Flag (hold, sources [665]): Registry only: the City row records no licence number and no CSLB page was opened, so no legal entity, status, classification or expiry is asserted.
- Flag (gap, sources [665]): The registry does not say which trade was performed under these permit rows, and a permit contact row is not proof that a given firm performed a given scope.
- Flag (gap, sources [665, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this registry identity in the evidence read on 2026-09-16.
- Gap: No licence number in the City row and no direct CSLB read, so status and classification are unknown.
- Gap: No current dispatch, exact overflow, ceiling-restoration, insurance or written repair-first evidence.
- Next step: Look the firm up at CSLB and match the legal name and address before any contact; then verify dispatch, insurance and scope in writing.

### Property Specialists — w16-reg-property-specialists
- Trade `registry-lead`, status `hold`, area `sunset`.
- Claim [Registry] (source `665`): Registry-recorded building contact read 2026-09-16: firm 'Property Specialists', address 1516 23rd Ave, ZIP 94122, across 20 grouped rows. The rows carry no licence number.
  - excerpt: “Property Specialists - 1516 23rd Ave - 94122 - 20 rows - licence field empty”
- Flag (hold, sources [665]): Registry only: the City row records no licence number and no CSLB page was opened, so no legal entity, status, classification or expiry is asserted.
- Flag (gap, sources [665]): The registry does not say which trade was performed under these permit rows, and a permit contact row is not proof that a given firm performed a given scope.
- Flag (gap, sources [665, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this registry identity in the evidence read on 2026-09-16.
- Gap: No licence number in the City row and no direct CSLB read, so status and classification are unknown.
- Gap: No current dispatch, exact overflow, ceiling-restoration, insurance or written repair-first evidence.
- Next step: Look the firm up at CSLB and match the legal name and address before any contact; then verify dispatch, insurance and scope in writing.

### X Tean Design & Construction — w16-reg-x-tean-design-construction
- Trade `registry-lead`, status `hold`, area `sunset`.
- Claim [Registry] (source `665`): Registry-recorded building contact read 2026-09-16: firm 'X Tean Design & Construction', address 2099 Irving Street Ste 205, ZIP 94122, across 3 grouped rows. The rows carry no licence number.
  - excerpt: “X Tean Design & Construction - 2099 Irving Street Ste 205 - 94122 - 3 rows - licence field empty”
- Flag (hold, sources [665]): Registry only: the City row records no licence number and no CSLB page was opened, so no legal entity, status, classification or expiry is asserted.
- Flag (gap, sources [665]): The registry does not say which trade was performed under these permit rows, and a permit contact row is not proof that a given firm performed a given scope.
- Flag (gap, sources [665, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this registry identity in the evidence read on 2026-09-16.
- Gap: No licence number in the City row and no direct CSLB read, so status and classification are unknown.
- Gap: No current dispatch, exact overflow, ceiling-restoration, insurance or written repair-first evidence.
- Next step: Look the firm up at CSLB and match the legal name and address before any contact; then verify dispatch, insurance and scope in writing.

### Woods Construction — w16-reg-woods-construction
- Trade `registry-lead`, status `hold`, area `sunset`.
- Claim [Registry] (source `665`): Registry-recorded building contact read 2026-09-16: firm 'Woods Construction', address 2625 Judah St#2, ZIP 94122, across 2 grouped rows. The rows carry no licence number.
  - excerpt: “Woods Construction - 2625 Judah St#2 - 94122 - 2 rows - licence field empty”
- Flag (hold, sources [665]): Registry only: the City row records no licence number and no CSLB page was opened, so no legal entity, status, classification or expiry is asserted.
- Flag (gap, sources [665]): The registry does not say which trade was performed under these permit rows, and a permit contact row is not proof that a given firm performed a given scope.
- Flag (gap, sources [665, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this registry identity in the evidence read on 2026-09-16.
- Gap: No licence number in the City row and no direct CSLB read, so status and classification are unknown.
- Gap: No current dispatch, exact overflow, ceiling-restoration, insurance or written repair-first evidence.
- Next step: Look the firm up at CSLB and match the legal name and address before any contact; then verify dispatch, insurance and scope in writing.

### Friendly Construction — w16-reg-friendly-construction
- Trade `registry-lead`, status `hold`, area `sunset`.
- Claim [Registry] (source `665`): Registry-recorded building contact read 2026-09-16: firm 'Friendly Construction', address 1774 41st Ave, ZIP 94122, across 1 grouped rows. The rows carry no licence number.
  - excerpt: “Friendly Construction - 1774 41st Ave - 94122 - 1 rows - licence field empty”
- Flag (hold, sources [665]): Registry only: the City row records no licence number and no CSLB page was opened, so no legal entity, status, classification or expiry is asserted.
- Flag (gap, sources [665]): The registry does not say which trade was performed under these permit rows, and a permit contact row is not proof that a given firm performed a given scope.
- Flag (gap, sources [665, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this registry identity in the evidence read on 2026-09-16.
- Gap: No licence number in the City row and no direct CSLB read, so status and classification are unknown.
- Gap: No current dispatch, exact overflow, ceiling-restoration, insurance or written repair-first evidence.
- Next step: Look the firm up at CSLB and match the legal name and address before any contact; then verify dispatch, insurance and scope in writing.

### Hegarty Construction — w16-reg-hegarty-construction
- Trade `registry-lead`, status `hold`, area `sunset`.
- Claim [Registry] (source `665`): Registry-recorded building contact read 2026-09-16: firm 'Hegarty Construction', address 1834 26th Ave, ZIP 94122, across 1 grouped rows. The rows carry no licence number.
  - excerpt: “Hegarty Construction - 1834 26th Ave - 94122 - 1 rows - licence field empty”
- Flag (hold, sources [665]): Registry only: the City row records no licence number and no CSLB page was opened, so no legal entity, status, classification or expiry is asserted.
- Flag (gap, sources [665]): The registry does not say which trade was performed under these permit rows, and a permit contact row is not proof that a given firm performed a given scope.
- Flag (gap, sources [665, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this registry identity in the evidence read on 2026-09-16.
- Gap: No licence number in the City row and no direct CSLB read, so status and classification are unknown.
- Gap: No current dispatch, exact overflow, ceiling-restoration, insurance or written repair-first evidence.
- Next step: Look the firm up at CSLB and match the legal name and address before any contact; then verify dispatch, insurance and scope in writing.

### Seastar Construction — w16-reg-seastar-construction
- Trade `registry-lead`, status `hold`, area `sunset`.
- Claim [Registry] (source `665`): Registry-recorded building contact read 2026-09-16: firm 'Seastar Construction', address 1439 23rd Ave, ZIP 94122, across 1 grouped rows. The rows carry no licence number.
  - excerpt: “Seastar Construction - 1439 23rd Ave - 94122 - 1 rows - licence field empty”
- Flag (hold, sources [665]): Registry only: the City row records no licence number and no CSLB page was opened, so no legal entity, status, classification or expiry is asserted.
- Flag (gap, sources [665]): The registry does not say which trade was performed under these permit rows, and a permit contact row is not proof that a given firm performed a given scope.
- Flag (gap, sources [665, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this registry identity in the evidence read on 2026-09-16.
- Gap: No licence number in the City row and no direct CSLB read, so status and classification are unknown.
- Gap: No current dispatch, exact overflow, ceiling-restoration, insurance or written repair-first evidence.
- Next step: Look the firm up at CSLB and match the legal name and address before any contact; then verify dispatch, insurance and scope in writing.

### Cg Adams Construction — w16-reg-cg-adams-construction
- Trade `registry-lead`, status `hold`, area `sunset`.
- Claim [Registry] (source `665`): Registry-recorded building contact read 2026-09-16: firm 'Cg Adams Construction', address 1487 45th Ave, ZIP 94122, across 1 grouped rows. The rows carry no licence number.
  - excerpt: “Cg Adams Construction - 1487 45th Ave - 94122 - 1 rows - licence field empty”
- Flag (hold, sources [665]): Registry only: the City row records no licence number and no CSLB page was opened, so no legal entity, status, classification or expiry is asserted.
- Flag (gap, sources [665]): The registry does not say which trade was performed under these permit rows, and a permit contact row is not proof that a given firm performed a given scope.
- Flag (gap, sources [665, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this registry identity in the evidence read on 2026-09-16.
- Gap: No licence number in the City row and no direct CSLB read, so status and classification are unknown.
- Gap: No current dispatch, exact overflow, ceiling-restoration, insurance or written repair-first evidence.
- Next step: Look the firm up at CSLB and match the legal name and address before any contact; then verify dispatch, insurance and scope in writing.

### Mark Huff Construction, Inc. — w16-reg-mark-huff-construction
- Trade `registry-lead`, status `hold`, area `sunset`.
- Claim [Registry] (source `665`): Registry-recorded building contact read 2026-09-16: firm 'Mark Huff Construction, Inc.', address 1527 43rd Ave, ZIP 94122, across 1 grouped rows. The rows carry no licence number.
  - excerpt: “Mark Huff Construction, Inc. - 1527 43rd Ave - 94122 - 1 rows - licence field empty”
- Flag (hold, sources [665]): Registry only: the City row records no licence number and no CSLB page was opened, so no legal entity, status, classification or expiry is asserted.
- Flag (gap, sources [665]): The registry does not say which trade was performed under these permit rows, and a permit contact row is not proof that a given firm performed a given scope.
- Flag (gap, sources [665, 666, 667, 669, 672]): No attributable Yelp, Thumbtack, Reddit or directory review was matched to this registry identity in the evidence read on 2026-09-16.
- Gap: No licence number in the City row and no direct CSLB read, so status and classification are unknown.
- Gap: No current dispatch, exact overflow, ceiling-restoration, insurance or written repair-first evidence.
- Next step: Look the firm up at CSLB and match the legal name and address before any contact; then verify dispatch, insurance and scope in writing.

## Tier 3 — 15 platform and community listings (no licence implication)

### Ace on Taraval — w16-plat-ace-on-taraval
- Trade `platform-listing`, status `hold`, area `sunset`.
- Claim [Community thread] (source `676`): Community thread mention read 2026-09-16: a commenter replies to a request for a plumber with 'Ace on Taraval has treated us great'. Taraval Street runs through the Sunset, but the listing itself is not read, no licence is published and no scope is stated.
  - excerpt: “Ace on Taraval - Community thread mention: 'Ace on Taraval has treated us great'. No licence, address, classification or scope is published in the thread.”
- Platform link (source `676`): Reddit thread — https://www.reddit.com/r/AskSF/comments/jcy9dl/can_you_recommend_a_plumber/
- Flag (hold, sources [676]): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- Flag (gap, sources [676]): Nothing in the listing names a seized bathtub overflow linkage, a concealed 1940s-era assembly, a ceiling opening, drywall closeout or an installed access hatch.
- Flag (gap, sources [676]): No Outer Sunset address, dispatch radius, project insurance or written repair-first scope was confirmed for this listing on 2026-09-16.
- Gap: No CSLB legal identity, status or classification verified.
- Gap: No exact-task outcome, project insurance or written repair-first scope.
- Next step: Obtain the exact CSLB number and legal entity, check both at CSLB, then verify Outer Sunset dispatch, insurance and scope in writing.

### Legend Plumbing and Drain — w16-plat-legend-plumbing-and-drain
- Trade `platform-listing`, status `hold`, area `sf`.
- Claim [Platform listing] (source `672`): Search extract read 2026-09-16: 'Legend Plumbing and Drain 5.0 (14 reviews) Verified License'. The same search shows a second card 'Legend Plumbing & Drain 5.0 (20 reviews) Verified License'; the two cards carry different review counts and are not merged here.
  - excerpt: “Legend Plumbing and Drain - Platform card: 5.0 (14 reviews) and a 'Verified License' badge. A second card for the near-identical name shows 5.0 (20 reviews).”
- Platform link (source `672`): Yelp 24-hour plumbers near Outer Sunset — https://www.yelp.com/search?find_desc=24+Hour+Plumbers&find_loc=Outer+Sunset,+San+Francisco,+CA&start=120
- Flag (hold, sources [672]): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- Flag (gap, sources [672]): Nothing in the listing names a seized bathtub overflow linkage, a concealed 1940s-era assembly, a ceiling opening, drywall closeout or an installed access hatch.
- Flag (gap, sources [672]): No Outer Sunset address, dispatch radius, project insurance or written repair-first scope was confirmed for this listing on 2026-09-16.
- Gap: No CSLB legal identity, status or classification verified.
- Gap: No exact-task outcome, project insurance or written repair-first scope.
- Next step: Obtain the exact CSLB number and legal entity, check both at CSLB, then verify Outer Sunset dispatch, insurance and scope in writing.

### Friendly Plumbing — w16-plat-friendly-plumbing
- Trade `platform-listing`, status `hold`, area `sf`.
- Claim [Platform listing] (source `674`): Search extract read 2026-09-16: 'Friendly Plumbing 5.0 (15 reviews) Verified License - Sewer repair' with an excerpt about replacing a leaky fixture. Yelp did not serve the page directly (HTTP 403 on 2026-09-16), so only the search extract is retained.
  - excerpt: “Friendly Plumbing - Platform card: 5.0 (15 reviews), 'Verified License', sewer-repair category and an attributable excerpt beginning 'Highly recommend! Friendly Plumbing had completed two services for my house replaced my leaky'.”
- Platform link (source `674`): Yelp sewer line repair near Outer Sunset — https://www.yelp.com/search?find_desc=Sewer+Line+Repair&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA
- Flag (hold, sources [674]): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- Flag (gap, sources [674]): Nothing in the listing names a seized bathtub overflow linkage, a concealed 1940s-era assembly, a ceiling opening, drywall closeout or an installed access hatch.
- Flag (gap, sources [674]): No Outer Sunset address, dispatch radius, project insurance or written repair-first scope was confirmed for this listing on 2026-09-16.
- Gap: No CSLB legal identity, status or classification verified.
- Gap: No exact-task outcome, project insurance or written repair-first scope.
- Next step: Obtain the exact CSLB number and legal entity, check both at CSLB, then verify Outer Sunset dispatch, insurance and scope in writing.

### Water Heater Boys — w16-plat-water-heater-boys
- Trade `platform-listing`, status `hold`, area `sf`.
- Claim [Platform listing] (source `666`): Category read 2026-09-16: 5.0 (13), Top Pro, 27 hires, water-heater installation and replacement. No licence number is published on the category card.
  - excerpt: “Water Heater Boys - Platform card: 5.0 (13); Top Pro; 27 hires; water heater installation or replacement; 'Serves San Francisco, CA'.”
- Platform link (source `666`): Thumbtack San Francisco plumbers category — https://www.thumbtack.com/ca/san-francisco/plumbers
- Flag (hold, sources [666]): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- Flag (gap, sources [666]): Nothing in the listing names a seized bathtub overflow linkage, a concealed 1940s-era assembly, a ceiling opening, drywall closeout or an installed access hatch.
- Flag (gap, sources [666]): No Outer Sunset address, dispatch radius, project insurance or written repair-first scope was confirmed for this listing on 2026-09-16.
- Gap: No CSLB legal identity, status or classification verified.
- Gap: No exact-task outcome, project insurance or written repair-first scope.
- Next step: Obtain the exact CSLB number and legal entity, check both at CSLB, then verify Outer Sunset dispatch, insurance and scope in writing.

### Magic Plumbing Heating Cooling — w16-plat-magic-plumbing-heating-cooling
- Trade `platform-listing`, status `hold`, area `sf`.
- Claim [Platform listing] (source `666`): Category read 2026-09-16: the card states licensed technicians and lists repiping, drain and water-heater work; no rating or licence number is exposed in the extract that was read.
  - excerpt: “Magic Plumbing Heating Cooling - Platform card: repiping list, drain clearing and water-heater installs; the card states 'Our licensed technicians handle everything from leaky faucets and clogged drains to full repipes'. No licence number is published.”
- Platform link (source `666`): Thumbtack San Francisco plumbers category — https://www.thumbtack.com/ca/san-francisco/repiping-specialists/magic-plumbing-heating-cooling/service/588097039016427524
- Flag (hold, sources [666]): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- Flag (gap, sources [666]): Nothing in the listing names a seized bathtub overflow linkage, a concealed 1940s-era assembly, a ceiling opening, drywall closeout or an installed access hatch.
- Flag (gap, sources [666]): No Outer Sunset address, dispatch radius, project insurance or written repair-first scope was confirmed for this listing on 2026-09-16.
- Gap: No CSLB legal identity, status or classification verified.
- Gap: No exact-task outcome, project insurance or written repair-first scope.
- Next step: Obtain the exact CSLB number and legal entity, check both at CSLB, then verify Outer Sunset dispatch, insurance and scope in writing.

### J.A. Emmanuel Construction — w16-plat-ja-emmanuel-construction
- Trade `platform-listing`, status `hold`, area `sf`.
- Claim [Community thread] (source `675`): Community thread read 2026-09-16 asking for a contractor who does good drywall repair in or near San Francisco; one commenter recommends this firm from direct experience and says drywall work was involved. No licence, address or scope is published.
  - excerpt: “J.A. Emmanuel Construction - Community thread: 'I didn't ask him to work on dry wall specifically (although he redid several walls in my house and so there must have been dry wall work involved), but I had a great experience with J.A. Emmanuel Construction.'”
- Platform link (source `675`): Reddit thread — https://www.reddit.com/r/AskSF/comments/171irdh/looking_for_a_contractor_in_or_near_sf_who_does/
- Flag (hold, sources [675]): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- Flag (gap, sources [675]): Nothing in the listing names a seized bathtub overflow linkage, a concealed 1940s-era assembly, a ceiling opening, drywall closeout or an installed access hatch.
- Flag (gap, sources [675]): No Outer Sunset address, dispatch radius, project insurance or written repair-first scope was confirmed for this listing on 2026-09-16.
- Gap: No CSLB legal identity, status or classification verified.
- Gap: No exact-task outcome, project insurance or written repair-first scope.
- Next step: Obtain the exact CSLB number and legal entity, check both at CSLB, then verify Outer Sunset dispatch, insurance and scope in writing.

### Sederap — w16-plat-sederap
- Trade `platform-listing`, status `hold`, area `sf`.
- Claim [Community thread] (source `675`): Community thread read 2026-09-16: a commenter who had not hired the firm says it appears licensed and insured and has done drywall work nearby. A second-hand, unverified mention.
  - excerpt: “Sederap - Community thread: 'haven't used them myself, but a friend almost did - i'd check out sederap since theyre licensed, insured, and looks like they've done a lot of drywall work nearby.'”
- Platform link (source `675`): Reddit thread — https://www.reddit.com/r/AskSF/comments/171irdh/looking_for_a_contractor_in_or_near_sf_who_does/
- Flag (hold, sources [675]): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- Flag (gap, sources [675]): Nothing in the listing names a seized bathtub overflow linkage, a concealed 1940s-era assembly, a ceiling opening, drywall closeout or an installed access hatch.
- Flag (gap, sources [675]): No Outer Sunset address, dispatch radius, project insurance or written repair-first scope was confirmed for this listing on 2026-09-16.
- Gap: No CSLB legal identity, status or classification verified.
- Gap: No exact-task outcome, project insurance or written repair-first scope.
- Next step: Obtain the exact CSLB number and legal entity, check both at CSLB, then verify Outer Sunset dispatch, insurance and scope in writing.

### C Max Construction — w16-plat-c-max-construction
- Trade `platform-listing`, status `hold`, area `sf`.
- Claim [Community thread] (source `678`): Community thread read 2026-09-16 recommending general contractors in San Francisco. The recommending username matches the firm name, so the comment reads as self-promotion and is flagged rather than treated as independent review evidence.
  - excerpt: “C Max Construction - Community thread: 'C Max Construction - reasonable prices & excellent customer service, skillful craftmanship!' posted by the username cmaxconstruction.”
- Platform link (source `678`): Reddit thread — https://www.reddit.com/r/sanfrancisco/comments/1aj2hy6/general_contractor_recommendations/
- Flag (hold, sources [678]): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- Flag (gap, sources [678]): Nothing in the listing names a seized bathtub overflow linkage, a concealed 1940s-era assembly, a ceiling opening, drywall closeout or an installed access hatch.
- Flag (gap, sources [678]): No Outer Sunset address, dispatch radius, project insurance or written repair-first scope was confirmed for this listing on 2026-09-16.
- Flag (discrepancy, sources [678]): The recommending username matches the firm name, so the comment reads as self-promotion and is not treated as independent review evidence.
- Gap: No CSLB legal identity, status or classification verified.
- Gap: No exact-task outcome, project insurance or written repair-first scope.
- Next step: Obtain the exact CSLB number and legal entity, check both at CSLB, then verify Outer Sunset dispatch, insurance and scope in writing.

### Cameron Bryce Construction — w16-plat-cameron-bryce-construction
- Trade `platform-listing`, status `hold`, area `sf`.
- Claim [Community thread] (source `678`): Community thread read 2026-09-16: a shortlist of three names posted in one comment with no detail about the work, the licence, the address or any scope.
  - excerpt: “Cameron Bryce Construction - Community thread: 'Cameron Bryce Construction / Dreamt Design and Build / Kiely Construction'.”
- Platform link (source `678`): Reddit thread — https://www.reddit.com/r/sanfrancisco/comments/1aj2hy6/general_contractor_recommendations/
- Flag (hold, sources [678]): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- Flag (gap, sources [678]): Nothing in the listing names a seized bathtub overflow linkage, a concealed 1940s-era assembly, a ceiling opening, drywall closeout or an installed access hatch.
- Flag (gap, sources [678]): No Outer Sunset address, dispatch radius, project insurance or written repair-first scope was confirmed for this listing on 2026-09-16.
- Gap: No CSLB legal identity, status or classification verified.
- Gap: No exact-task outcome, project insurance or written repair-first scope.
- Next step: Obtain the exact CSLB number and legal entity, check both at CSLB, then verify Outer Sunset dispatch, insurance and scope in writing.

### Eduardo & Jose's Paz Garcia's Painting — w16-plat-eduardo-jose-paz-garcia-painting
- Trade `platform-listing`, status `hold`, area `sf`.
- Claim [Platform listing] (source `667`): Category read 2026-09-16: 4.4 (137), Top Pro, 151 hires, 'In high demand', appears on the San Francisco drywall-repair category and its review excerpt is about painting. No licence number is published.
  - excerpt: “Eduardo & Jose's Paz Garcia's Painting - Platform card: 4.4 (137); Top Pro; 151 hires; drywall-repair category; retained excerpt is about a paint job, not about drywall repair.”
- Platform link (source `667`): Thumbtack San Francisco drywall repair category — https://www.thumbtack.com/ca/berkeley/interior-painting/eduardo-joses-paz-garcias-painting/service/220902047590138914
- Flag (hold, sources [667]): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- Flag (gap, sources [667]): Nothing in the listing names a seized bathtub overflow linkage, a concealed 1940s-era assembly, a ceiling opening, drywall closeout or an installed access hatch.
- Flag (gap, sources [667]): No Outer Sunset address, dispatch radius, project insurance or written repair-first scope was confirmed for this listing on 2026-09-16.
- Flag (discrepancy, sources [667]): The retained excerpt does not describe the category the card appears in; the excerpt is quoted exactly as published and is not read as evidence of the missing scope.
- Gap: No CSLB legal identity, status or classification verified.
- Gap: No exact-task outcome, project insurance or written repair-first scope.
- Next step: Obtain the exact CSLB number and legal entity, check both at CSLB, then verify Outer Sunset dispatch, insurance and scope in writing.

### Economy Plumbing Sewer & Drain — w16-plat-economy-plumbing-sewer-drain
- Trade `platform-listing`, status `hold`, area `sf`.
- Claim [Platform listing] (source `672`): Search extract read 2026-09-16: 'Economy Plumbing Sewer & Drain 3.5 (149 reviews)' with a price-comparison excerpt. No licence badge is shown on the card, unlike neighbouring cards that print 'Verified License'.
  - excerpt: “Economy Plumbing Sewer & Drain - Platform card: 3.5 (149 reviews); the retained excerpt compares an estimate against other quotes.”
- Platform link (source `672`): Yelp 24-hour plumbers near Outer Sunset — https://www.yelp.com/search?find_desc=24+Hour+Plumbers&find_loc=Outer+Sunset,+San+Francisco,+CA&start=120
- Flag (hold, sources [672]): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- Flag (gap, sources [672]): Nothing in the listing names a seized bathtub overflow linkage, a concealed 1940s-era assembly, a ceiling opening, drywall closeout or an installed access hatch.
- Flag (gap, sources [672]): No Outer Sunset address, dispatch radius, project insurance or written repair-first scope was confirmed for this listing on 2026-09-16.
- Gap: No CSLB legal identity, status or classification verified.
- Gap: No exact-task outcome, project insurance or written repair-first scope.
- Next step: Obtain the exact CSLB number and legal entity, check both at CSLB, then verify Outer Sunset dispatch, insurance and scope in writing.

### Lemus Construction — w16-plat-lemus-construction
- Trade `platform-listing`, status `hold`, area `sf`.
- Claim [Platform listing] (source `673`): Search extract read 2026-09-16: 'Lemus Construction 4.8 (21 reviews) Serving San Francisco and the Surrounding Area' with an excerpt about a design approval and an engineer. No licence badge is shown on the card.
  - excerpt: “Lemus Construction - Platform card: 4.8 (21 reviews); the retained excerpt is about design approval with the city and an engineer.”
- Platform link (source `673`): Yelp construction near Outer Sunset — https://yelp.com/search?find_desc=Construction&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA
- Flag (hold, sources [673]): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- Flag (gap, sources [673]): Nothing in the listing names a seized bathtub overflow linkage, a concealed 1940s-era assembly, a ceiling opening, drywall closeout or an installed access hatch.
- Flag (gap, sources [673]): No Outer Sunset address, dispatch radius, project insurance or written repair-first scope was confirmed for this listing on 2026-09-16.
- Gap: No CSLB legal identity, status or classification verified.
- Gap: No exact-task outcome, project insurance or written repair-first scope.
- Next step: Obtain the exact CSLB number and legal entity, check both at CSLB, then verify Outer Sunset dispatch, insurance and scope in writing.

### Five Star Plumbing & Rooter — w16-plat-five-star-plumbing-rooter
- Trade `platform-listing`, status `hold`, area `sf`.
- Claim [Platform listing] (source `672`): Search extract read 2026-09-16: 'Five Star Plumbing & Rooter 4.9 (89 reviews) Verified License'. No review text is exposed for this card in the extract, so no excerpt is retained.
  - excerpt: “Five Star Plumbing & Rooter - Platform card: 4.9 (89 reviews) with a 'Verified License' badge and free estimates.”
- Platform link (source `672`): Yelp 24-hour plumbers near Outer Sunset — https://www.yelp.com/search?find_desc=24+Hour+Plumbers&find_loc=Outer+Sunset,+San+Francisco,+CA&start=120
- Flag (hold, sources [672]): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- Flag (gap, sources [672]): Nothing in the listing names a seized bathtub overflow linkage, a concealed 1940s-era assembly, a ceiling opening, drywall closeout or an installed access hatch.
- Flag (gap, sources [672]): No Outer Sunset address, dispatch radius, project insurance or written repair-first scope was confirmed for this listing on 2026-09-16.
- Gap: No CSLB legal identity, status or classification verified.
- Gap: No exact-task outcome, project insurance or written repair-first scope.
- Next step: Obtain the exact CSLB number and legal entity, check both at CSLB, then verify Outer Sunset dispatch, insurance and scope in writing.

### Precise Plumbing & Drain — w16-plat-precise-plumbing-drain
- Trade `platform-listing`, status `hold`, area `sf`.
- Claim [Platform listing] (source `672`): Search extract read 2026-09-16: 'Precise Plumbing & Drain 5.0 (11 reviews)' with free consultations. No licence badge and no review text appear on the card.
  - excerpt: “Precise Plumbing & Drain - Platform card: 5.0 (11 reviews); free consultations; no licence badge shown.”
- Platform link (source `672`): Yelp 24-hour plumbers near Outer Sunset — https://www.yelp.com/search?find_desc=24+Hour+Plumbers&find_loc=Outer+Sunset,+San+Francisco,+CA&start=120
- Flag (hold, sources [672]): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- Flag (gap, sources [672]): Nothing in the listing names a seized bathtub overflow linkage, a concealed 1940s-era assembly, a ceiling opening, drywall closeout or an installed access hatch.
- Flag (gap, sources [672]): No Outer Sunset address, dispatch radius, project insurance or written repair-first scope was confirmed for this listing on 2026-09-16.
- Gap: No CSLB legal identity, status or classification verified.
- Gap: No exact-task outcome, project insurance or written repair-first scope.
- Next step: Obtain the exact CSLB number and legal entity, check both at CSLB, then verify Outer Sunset dispatch, insurance and scope in writing.

### ANTÖRMEN — w16-plat-antormen
- Trade `platform-listing`, status `hold`, area `sf`.
- Claim [Platform listing] (source `668`): Category read 2026-09-16: 5.0 (40), Top Pro, 10 hires, 'Licensed pro' badge, Serves San Francisco. The retained excerpt mentions vents and ducting for a range hood and a bathroom fan, not a drain assembly or ceiling access.
  - excerpt: “ANTÖRMEN - Platform card: 5.0 (40); Top Pro; 10 hires; 'Licensed pro' badge; excerpt about ventilation work.”
- Platform link (source `668`): Thumbtack San Francisco bathroom remodeling category — https://www.thumbtack.com/ca/san-francisco/general-contractors/antrmen/service/549741754129948686
- Flag (hold, sources [668]): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- Flag (gap, sources [668]): Nothing in the listing names a seized bathtub overflow linkage, a concealed 1940s-era assembly, a ceiling opening, drywall closeout or an installed access hatch.
- Flag (gap, sources [668]): No Outer Sunset address, dispatch radius, project insurance or written repair-first scope was confirmed for this listing on 2026-09-16.
- Flag (discrepancy, sources [668]): The retained excerpt does not describe the category the card appears in; the excerpt is quoted exactly as published and is not read as evidence of the missing scope.
- Gap: No CSLB legal identity, status or classification verified.
- Gap: No exact-task outcome, project insurance or written repair-first scope.
- Next step: Obtain the exact CSLB number and legal entity, check both at CSLB, then verify Outer Sunset dispatch, insurance and scope in writing.

## Retained review excerpts (R166–R175)

- **R166** · w16-plat-ace-on-taraval · Reddit · author City_Goat · published None · rating (not shown) · access `search-extract` · identity `unverified-username` · source `676`
  - “Ace on Taraval has treated us great”
- **R167** · w16-plat-friendly-plumbing · Yelp · author Yelp reviewer (name not shown in extract) · published None · rating (not shown) · access `search-extract` · identity `indexed` · source `674`
  - “Highly recommend! Friendly Plumbing had completed two services for my house replaced my leaky”
- **R168** · w16-plat-water-heater-boys · Thumbtack · author Jon D. · published None · rating (not shown) · access `page` · identity `indexed` · source `666`
  - “I was bracing myself for days without hot showers and the hassle of finding a reliable plumber. Then I stumbled upon Water Heater Boys.”
- **R169** · w16-plat-ja-emmanuel-construction · Reddit · author lessachu · published None · rating (not shown) · access `search-extract` · identity `unverified-username` · source `675`
  - “I didn't ask him to work on dry wall specifically (although he redid several walls in my house and so there must have been dry wall work involved), but I had a great experience with J.A. Emmanuel Construction.”
- **R170** · w16-plat-sederap · Reddit · author No-Doubt9029 · published None · rating (not shown) · access `search-extract` · identity `unverified-username` · source `675`
  - “haven't used them myself, but a friend almost did - i'd check out sederap since theyre licensed, insured, and looks like they've done a lot of drywall work nearby”
- **R171** · w16-plat-c-max-construction · Reddit · author cmaxconstruction · published None · rating (not shown) · access `search-extract` · identity `unverified-username` · source `678`
  - “C Max Construction - reasonable prices & excellent customer service, skillful craftmanship!”
- **R172** · w16-plat-cameron-bryce-construction · Reddit · author pandabearak · published None · rating (not shown) · access `search-extract` · identity `unverified-username` · source `678`
  - “Cameron Bryce Construction Dreamt Design and Build Kiely Construction”
- **R173** · w16-plat-eduardo-jose-paz-garcia-painting · Thumbtack · author KARLOS G. · published None · rating (not shown) · access `page` · identity `indexed` · source `667`
  - “Fantastic paint job. High quality work and very responsiveness”
- **R174** · w16-plat-economy-plumbing-sewer-drain · Yelp · author Yelp reviewer (name not shown in extract) · published None · rating (not shown) · access `search-extract` · identity `indexed` · source `672`
  - “Franco came out in person within 30 minutes of calling him and gave me an estimate that was $500 cheaper than the next cheapest quote.”
- **R175** · w16-plat-lemus-construction · Yelp · author Yelp reviewer (name not shown in extract) · published None · rating (not shown) · access `search-extract` · identity `indexed` · source `673`
  - “getting a design approved by both an engineer and the city, we hired Jose from Lemus Construction.”

## Collision, rejection and negative-result log

- The 94122 grouped plumbing-contact query, the 94122 building-contact query with a licence recorded, and the 94122 building-contact query with no licence recorded were each re-read on 2026-09-16 and every number diffed against the 531-number baseline (284 stored licence numbers plus 523 six/seven-digit prose tokens). Exactly 25 numbers were new; all 25 are the tier-1 records above and every one was then opened at CSLB.
- Names already stored were rejected rather than re-published as new wave-16 records: WB Plumbing Supply (also a supply house, not a contracting record), Gerber Plumbing, X-Ray Plumbing And Drain, Eric Brand Plumbing, General SF, GCD Restoration, Kenneth Asire Plumbing, Plumbing Pure, VRG Plumbing, Handyman Heroes, Happy Bay Construction, Edri Construction, Inspired Builders Inc, Promodeling, Paul Woodford Services, Owl Plumbing, Safe Rooter Plumbing, Reasonably Honest Mike's, Handy Helper, Speer Handyman Services, Tal Handyman Services, ABC Maintenance & Handyman Services, Paint Studio SF, M & L Construction, Valex Construction and Precision Rooter & Drain.
- Yelp pages could not be read directly; the Outer Sunset plumbing, drywall and handyman search extract is stored as a search-extract source with access `search-extract`, and only names and counts shown in the extract are asserted.
- Registry-only firms whose licence could not be independently read at CSLB stayed in tier 2 with `license: null`; no number was promoted into a licence fact anywhere in this wave.

## Verification passes 37–39

1. **Pass 37 — regulator pass.** Registry queries re-read; 25 new numbers opened at CSLB and transcribed field by field; nothing asserted beyond the page printed.
2. **Pass 38 — collision and attribution pass.** All 50 candidates compared against every stored normalized name, stripped name core, licence number and ten-digit phone; a phone already stored elsewhere was left unstored and flagged instead of merging two identities; 10 attributable excerpts were retained and every card without readable review text was recorded with no excerpt.
3. **Pass 39 — fail-closed qualification pass.** All 50 held; `exactMatch`, `insuranceVerified`, `scopeConfirmed` and `master` remain false on every record; the privacy fingerprint scan is unchanged; the qualified master remains empty.

## Irregularities queued for manual review

- **Thomas Engel** (w16-1000783): Active licence 1000783 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- **Kenneth Chou** (w16-1003699): CSLB status for licence 1003699 was read as inactive. A licence that is not current and active cannot be contracted on, so the record is held and never promoted.
- **Kenneth Chou** (w16-1003699): CSLB prints (415) 867-0054 for licence 1003699, but the same ten digits are already stored against a different record in this dataset. The number is left unstored so two licence identities are not merged by a shared phone line.
- **Reichart Construction** (w16-1006197): Active licence 1006197 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- **Reichart Construction** (w16-1006197): The City registry prints 1540 La Playa while the CSLB page prints 1540 Great Highway 14 for the same licence and the same ZIP.
- **Nbay Construction** (w16-1008172): CSLB status for licence 1008172 was read as canceled. A licence that is not current and active cannot be contracted on, so the record is held and never promoted.
- **Nbay Construction** (w16-1008172): CSLB prints (415) 341-7285 for licence 1008172, but the same ten digits are already stored against a different record in this dataset. The number is left unstored so two licence identities are not merged by a shared phone line.
- **Zarin Gollogly Design & Build** (w16-1009077): CSLB status for licence 1009077 was read as expired. A licence that is not current and active cannot be contracted on, so the record is held and never promoted.
- **Zarin Gollogly Design & Build** (w16-1009077): The licence expiry date 11/30/2025 has passed by the read date, so the CSLB status line reads expired and not able to contract.
- **Zhuo Zhang Construction Inc** (w16-1009112): Active licence 1009112 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- **Zhuo Zhang Construction Inc** (w16-1009112): The City registry stores both 1452 47th Avenue and 1452 7th Avenue against this licence; the CSLB page prints 1452 47th Avenue.
- **Riley Remodeling and Consulting Inc** (w16-1014452): Active licence 1014452 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- **Chris William Construction Inc** (w16-1018105): Active licence 1018105 (B + C10) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- **Hybrid City Construction Inc** (w16-1021804): CSLB status for licence 1021804 was read as suspended. A licence that is not current and active cannot be contracted on, so the record is held and never promoted.
- **Hybrid City Construction Inc** (w16-1021804): CSLB status line reads: License is under suspension for the following reasons: License is under Contractors Bond Suspension.
- **Hybrid City Construction Inc** (w16-1021804): The CSLB address ZIP is 94112 while the City registry row prints 94122; the CSLB phone is (415) 812-1117 while the City row prints (415) 971-8890.
- **New City Construction Company** (w16-1023648): Active licence 1023648 (B + C10 + C36) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- **New City Construction Company** (w16-1023648): CSLB prints (415) 509-5025 for licence 1023648, but the same ten digits are already stored against a different record in this dataset. The number is left unstored so two licence identities are not merged by a shared phone line.
- **Silver Lining Design Build Co** (w16-1024550): Active licence 1024550 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- **Fly Cloud Construction Inc** (w16-1029195): Active licence 1029195 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- **Fly Cloud Construction Inc** (w16-1029195): The City registry row prints phone (415) 350-9953 for this licence; the CSLB page prints (415) 879-6118.
- **D-Finity Construction Inc** (w16-1033149): CSLB status for licence 1033149 was read as revoked. A licence that is not current and active cannot be contracted on, so the record is held and never promoted.
- **D-Finity Construction Inc** (w16-1033149): CSLB status line reads: This license is revoked and not able to contract at this time.
- **Shelter Cove Construction** (w16-1033503): CSLB status for licence 1033503 was read as expired. A licence that is not current and active cannot be contracted on, so the record is held and never promoted.
- **Actually Design Build** (w16-1035799): CSLB status for licence 1035799 was read as inactive. A licence that is not current and active cannot be contracted on, so the record is held and never promoted.
- **Actually Design Build** (w16-1035799): CSLB status is inactive and not able to contract; the additional status notes a contractors bond and workers compensation are needed to reactivate.
- **Actually Design Build** (w16-1035799): The City registry row prints 1359 48th Av while the CSLB page prints 1429 46th Avenue.
- **Slick Construction Inc** (w16-1044915): Active licence 1044915 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- **B&K Construction Inc** (w16-1047639): Active licence 1047639 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- **B&K Construction Inc** (w16-1047639): CSLB prints (415) 990-9431 for licence 1047639, but the same ten digits are already stored against a different record in this dataset. The number is left unstored so two licence identities are not merged by a shared phone line.
- **B&K Construction Inc** (w16-1047639): The CSLB classifications page lists B only, while the workers compensation classification codes include 51831 plumbing-low wage. The mismatch is recorded, not resolved.
- **Jakobson Construction Inc** (w16-1048032): Active licence 1048032 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- **Jakobson Construction Inc** (w16-1048032): The CSLB business address is a PO box in ZIP 94147 while the City registry row prints 1675 08th Av, 94122. No service-area claim is inferred from either.
- **Jian Hua Construction** (w16-1048617): Active licence 1048617 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- **Jian Hua Construction** (w16-1048617): The City registry row prints 1719 42nd St while the CSLB page prints 1719 42ND AVENUE.
- **Yan Construction** (w16-1048687): Active licence 1048687 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- **Yan Construction** (w16-1048687): The City registry row for this licence prints the malformed ZIP 941222; the CSLB page prints 94122.
- **CMAC Construction LLC** (w16-1053452): Active licence 1053452 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- **CMAC Construction LLC** (w16-1053452): The CSLB business address is in Novato while the City registry row prints 1295 41st Av, 94122.
- **CMAC Construction LLC** (w16-1053452): This is the only record of the 25 direct reads in this wave whose CSLB page prints a liability-insurance line, and it is still held: the address, the past 94122 permit rows and the absence of attributable reviews leave area and task evidence open.
- **Basset Engineering** (w16-1070288): Active licence 1070288 (A) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- **Dmsquare Construction 2 Inc** (w16-1074425): Active licence 1074425 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- **Dmsquare Construction 2 Inc** (w16-1074425): The CSLB business address is in Alameda while the City registry row prints 571 Edinburgh St, 94122.
- **Dreamsky Construction** (w16-1090715): Active licence 1090715 (B) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- **Dreamsky Construction** (w16-1090715): The City registry prints (415) 350-9953 for both this licence and Fly Cloud Construction (1029195). The CSLB pages print (415) 350-9953 for this licence and (415) 879-6118 for 1029195, so the shared registry phone is a City-row irregularity, not a shared CSLB phone.
- **Sound Build** (w16-1092217): Active licence 1092217 (B + C-2) read directly at CSLB, but the promotion gates for Outer Sunset dispatch, exact-task outcome, project insurance and a written repair-first scope are not satisfied, so the record stays out of the qualified master.
- **Eky Builder Inc.** (w16-reg-eky-builder): Registry only: the City row records no licence number and no CSLB page was opened, so no legal entity, status, classification or expiry is asserted.
- **S & J Constructions Inc** (w16-reg-s-and-j-constructions): Registry only: the City row records no licence number and no CSLB page was opened, so no legal entity, status, classification or expiry is asserted.
- **Property Specialists** (w16-reg-property-specialists): Registry only: the City row records no licence number and no CSLB page was opened, so no legal entity, status, classification or expiry is asserted.
- **X Tean Design & Construction** (w16-reg-x-tean-design-construction): Registry only: the City row records no licence number and no CSLB page was opened, so no legal entity, status, classification or expiry is asserted.
- **Woods Construction** (w16-reg-woods-construction): Registry only: the City row records no licence number and no CSLB page was opened, so no legal entity, status, classification or expiry is asserted.
- **Friendly Construction** (w16-reg-friendly-construction): Registry only: the City row records no licence number and no CSLB page was opened, so no legal entity, status, classification or expiry is asserted.
- **Hegarty Construction** (w16-reg-hegarty-construction): Registry only: the City row records no licence number and no CSLB page was opened, so no legal entity, status, classification or expiry is asserted.
- **Seastar Construction** (w16-reg-seastar-construction): Registry only: the City row records no licence number and no CSLB page was opened, so no legal entity, status, classification or expiry is asserted.
- **Cg Adams Construction** (w16-reg-cg-adams-construction): Registry only: the City row records no licence number and no CSLB page was opened, so no legal entity, status, classification or expiry is asserted.
- **Mark Huff Construction, Inc.** (w16-reg-mark-huff-construction): Registry only: the City row records no licence number and no CSLB page was opened, so no legal entity, status, classification or expiry is asserted.
- **Ace on Taraval** (w16-plat-ace-on-taraval): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- **Legend Plumbing and Drain** (w16-plat-legend-plumbing-and-drain): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- **Friendly Plumbing** (w16-plat-friendly-plumbing): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- **Water Heater Boys** (w16-plat-water-heater-boys): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- **Magic Plumbing Heating Cooling** (w16-plat-magic-plumbing-heating-cooling): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- **J.A. Emmanuel Construction** (w16-plat-ja-emmanuel-construction): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- **Sederap** (w16-plat-sederap): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- **C Max Construction** (w16-plat-c-max-construction): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- **C Max Construction** (w16-plat-c-max-construction): The recommending username matches the firm name, so the comment reads as self-promotion and is not treated as independent review evidence.
- **Cameron Bryce Construction** (w16-plat-cameron-bryce-construction): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- **Eduardo & Jose's Paz Garcia's Painting** (w16-plat-eduardo-jose-paz-garcia-painting): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- **Eduardo & Jose's Paz Garcia's Painting** (w16-plat-eduardo-jose-paz-garcia-painting): The retained excerpt does not describe the category the card appears in; the excerpt is quoted exactly as published and is not read as evidence of the missing scope.
- **Economy Plumbing Sewer & Drain** (w16-plat-economy-plumbing-sewer-drain): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- **Lemus Construction** (w16-plat-lemus-construction): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- **Five Star Plumbing & Rooter** (w16-plat-five-star-plumbing-rooter): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- **Precise Plumbing & Drain** (w16-plat-precise-plumbing-drain): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- **ANTÖRMEN** (w16-plat-antormen): Platform or community listing only: no CSLB licence number was published or read for this record. A 'Verified License' or 'Licensed pro' badge, when shown, is platform wording and not a regulator fact.
- **ANTÖRMEN** (w16-plat-antormen): The retained excerpt does not describe the category the card appears in; the excerpt is quoted exactly as published and is not read as evidence of the missing scope.
