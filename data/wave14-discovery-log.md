# Wave 14 discovery and verification log

**Research date:** 2026-09-16  
**Result:** exactly 50 new records retained; 25 direct CSLB reads, 20 official building-registry-only leads and five Thumbtack plumbing listings. Four attributable review excerpts retained. No record promoted.

This is an evidence log, not a recommendation list. A City registry address is historical contact evidence, a platform badge is not a regulator fact, and an active licence does not prove present Outer Sunset dispatch, project insurance, difficult-overflow skill, or a repair-first written scope.

## Discovery channels and access

| Channel | Access and use in this pass |
| --- | --- |
| CSLB | 25 individual `LicenseDetail.aspx` pages read directly and transcribed. Status and class are reported only for this tier. |
| SF DBI plumbing contacts | Official 94122 grouped registry query read directly; used as historical identity/address cross-check for the direct CSLB tier. |
| SF DBI building contacts | Official 94122 grouped registry query read directly; 20 distinct leads retained with `license: null`. |
| Thumbtack | San Francisco plumbers, drywall-repair and ceiling-repair category pages read directly. Five new plumber listings and four attributable short excerpts retained. Attributable drywall identities were already in the corpus and were not counted again. |
| Yelp | Search/index evidence was checked where available. Blocked pages were not bypassed and inaccessible review text was not reconstructed. |
| Reddit | Task-relevant search extracts were checked as workflow context; direct pages returned HTTP 403. No business attribution was made. |
| Google | Indexed evidence was checked only as discovery. No original Google review panel was retrieved, and no new Google-attributed review was stored. |
| BuildZoom | The Bay Construction Company, Soon Yu Construction and Mallard Construction pages were read. Stale status and mixed-identity conflicts are preserved as discrepancies, never as regulator facts. |
| Business sites | Targeted identity/task searches produced no sufficient new exact-task and Outer Sunset proof for these records. Missing sites or redirects remain gaps. |

Source IDs 596–629 in `data/research.json` retain every URL, access mode, check date and source-specific limitation. The normalized evidence artifact is `data/wave14.json`.

## Tier 1 — 25 direct CSLB reads

Every licence below was read from its matching regulator detail page. The area column reflects this dataset's evidence tier: `outer` means a current regulator 94122 address; `sunset` can mean historical 94122 City registry relevance but does not establish present dispatch.

| Business | Licence | Status | Classes | Area tier | CSLB source |
| --- | ---: | --- | --- | --- | ---: |
| H2Pro Inc | 765149 | expired | B, C-4, C36 | sunset | 602 |
| Elite Engineering Contractors | 917633 | active | A, B | outer | 603 |
| Good Neighbor Construction | 912166 | active | B | sunset | 604 |
| KNJ General Construction | 693830 | active | B | sunset | 605 |
| C & M Development and Construction Inc | 950296 | expired | B | sunset | 606 |
| Cheng Chang Construction Co | 756611 | active | B | sunset | 607 |
| Chih Jin Wen | 466541 | expired | B | sunset | 608 |
| Martin Mar Construction Co | 706442 | expired | B, C51 | outer | 609 |
| Shun Construction | 658187 | revoked | B | sunset | 610 |
| Da Chung Incorporated | 809529 | active | B | sunset | 611 |
| Mallard Construction | 849492 | active | B | outer | 612 |
| New United Construction | 690708 | expired | B | outer | 613 |
| The Bay Construction Company | 653045 | active | B | outer | 614 |
| J N Pacific Construction Co | 749693 | active | B, C36 | sunset | 615 |
| P E I Construction Inc | 769813 | canceled | B | outer | 616 |
| Custom Concepts | 667991 | expired | B | outer | 617 |
| Wong Construction Inc | 377610 | active | B | sunset | 618 |
| Mc Eleney Construction | 839263 | expired | B | outer | 619 |
| Sunset Electric Construction Inc | 413998 | canceled | C10 | sunset | 620 |
| Excelsior Construction | 614864 | revoked | B | outer | 621 |
| Castle Builders Co | 787392 | expired | B | outer | 622 |
| Z M General Contractor | 483659 | inactive | B, C10, C36 | sunset | 623 |
| I W Construction | 964968 | inactive | B | outer | 624 |
| Tony Oei | 407633 | expired | C36, B | sunset | 625 |
| Soon Yu Construction | 667984 | active | B | outer | 626 |

### Direct-tier findings

- The group contains **10 active** and **15 non-active** licence records. Every expired, canceled, inactive or revoked record is held and is not presented as bookable.
- **J N Pacific Construction Co (749693)** is the only active direct record with both B and C36. Its CSLB address is in 94103; the 94122 relevance comes from historical City contact evidence. No exact seized-overflow result, C-9/C35 classification, applicable insurance, present dispatch or written repair-first scope was found.
- Four active records have a current CSLB 94122 address: Elite Engineering Contractors, Mallard Construction, The Bay Construction Company and Soon Yu Construction. Address does not prove job acceptance. Each still lacks one required trade or direct exact-task evidence and every promotion gate.
- **Sunset Electric Construction Inc (413998)** has C10 only. It is retained as a non-promotable scope exclusion, not treated as plumbing or drywall evidence.
- C51 first appears in this corpus on Martin Mar Construction Co's expired regulator record. It is retained verbatim, but structural-steel classification is not treated as coverage for either required project trade.
- Material registry/regulator identity changes remain explicit: EMB Plumbing/H2PRO, Constant Construction/Chih Jin Wen, Lin Xi Shun/Shun Construction, Bo Zhong Construction/P E I Construction, Wong's Construction/Wong Construction Inc, and Coast Pacific Properties/Tony Oei.
- BuildZoom labels The Bay inactive although the same-day CSLB page is active. The regulator fact remains primary and the stale third-party conflict remains visible.
- BuildZoom's Mallard page combines San Francisco licence 849492 with an Orange business, a 760 phone and licences 469683 and 536485. None of those mixed fields was attributed to the San Francisco sole owner.
- Soon Yu's BuildZoom page supports identity continuity and indexes 94122 work, including a bathtub-replacement permit. It does not prove a seized-overflow repair or restoration outcome, and stale bond text was not substituted for the current regulator line.

## Tier 2 — 20 building-registry-only leads

These records intentionally carry `license: null`, trade `registry-lead`, and hold status. The number in the official City row is a lead to a future CSLB read; it is not represented as a verified current licence.

| Registry name | City-recorded number | Grouped rows | Recorded 94122 contact location |
| --- | ---: | ---: | --- |
| Christopher Gate Construction Inc | 840805 | 179 | PO Box 225232 |
| Advanced Design General Contractor | 544201 | 106 | 3922 Kirkham St |
| O'kane Construction LLC | 701012 | 81 | 1842 21st Ave |
| Modern Craft Construction | 984971 | 73 | PO Box 22025 |
| Eignor Construction Inc. | 819274 | 70 | 1032 Irving Street, PMB 905 |
| Zarc Construction Inc | 1038989 | 66 | 1549 Noriega St |
| Kelly Brother's Construction | 587887 | 65 | 1319 22nd Ave |
| TN Building | 967336 | 61 | 1312 Ortega St |
| PJD Construction Inc | 1007052 | 58 | 1856 29th Ave |
| Riley Construction Co | 519294 | 53 | 1032 Irving St, #436 |
| Youda Builders Inc | 1004624 | 53 | 1500 18th Ave |
| Nancy Built LLC | 952450 | 50 | 1656 18th Ave |
| Tao's Construction Inc. | 1044068 | 47 | 1419 22nd Avenue |
| North Beach Const. | 750238 | 46 | 1443 21st Ave |
| K & J Construction Co. | 452211 | 46 | 1459 24th Ave |
| Badger Construction | 542738 | 46 | 1683 24th Ave |
| Argo Construction Inc | 857620 | 43 | 1227 39th Ave |
| Xin Xin Construction | 870223 | 41 | 1666 26th Ave |
| Artisana Painting | 744592 | 40 | 500 Noriega St |
| Tauscher Construction | 844980 | 38 | 1416 34th Ave |

None has current status, classification, business identity, bond, insurance, present operation, dispatch, exact-task experience or written scope established by this pass. Registry row counts are not a workmanship score.

## Tier 3 — five Thumbtack platform listings

| Listing | Retained evidence | Result |
| --- | --- | --- |
| Rooter Hero - East Bay | Listing identity on the current SF plumber category page | Hold; no direct CSLB identity, exact task, both-trade proof or Outer Sunset dispatch established |
| Ever Plumbing Underground | Platform listing displays 4.7/133, Top Pro and 286 hires; Dina C. excerpt retained as R159 | General plumbing account only; `exactTask: false` |
| Mr Jimmy Plumbing & Rooter | Platform listing displays 5.0/30, Top Pro, 41 hires and “Licensed pro”; Kevin M. excerpt retained as R160 | Platform badge is not a CSLB fact; `exactTask: false` |
| I Rooter & Plumbing | Aly I. excerpt retained as R161 | General service account only; `exactTask: false` |
| AG Quality Plumbing | Thumbtack Customer excerpt retained as R162 | General service account only; `exactTask: false` |

The four excerpts do not establish safe removal of a seized trip-lever assembly, old galvanized overflow work, ceiling access/restoration, finish matching, trade coordination, current Outer Sunset dispatch or project insurance.

## Deduplication and rejected candidates

The merge checks exact ids, normalized names, stripped name cores, licence numbers and ten-digit phones across the pre-wave corpus and within Wave 14. It also requires every record and source id to be unique.

Candidates specifically rejected before the count was fixed:

- **Figs Drywall Repair & Paint** — already stored; “Figs Drywall Repair” is the same core identity, and the linked profile path raised an out-of-area Boise issue.
- **Mayorga Handyman & Remodeling Services** — already stored; “Mayorga Remodeling & Construction” is not a new business for count purposes.
- **Dom's Plumbing** — already stored.
- **Magic Plumbing Heating & Cooling** — same stored Magic Plumbing brand family; not counted again.
- **Advance Plumbing / licence 973345** — registry phone matches existing Expert Plumbing Solutions; excluded rather than creating a second identity.
- Targeted J N Pacific, Wong and Elite searches surfaced namesakes; no reviews were attributed.
- National, out-of-area, unattributable or blocked evidence was not converted into a record or review merely to reach 50.

Generator collision checks and the independent merge gates both passed before the 50 records entered `data/research.json`.

## Three additional verification passes

### Pass 31 — regulator and line transcription

1. Reopened the 25 exact licence URLs and transcribed the legal entity/form, address, phone, issue/expiry dates, status, every classification, bond and workers' compensation lines.
2. Checked regulator dates against 2026-09-16 and held all 15 non-active results.
3. Kept the 20 building numbers and five platform listings without a licence object because no matching direct read was performed for those rows.

### Pass 32 — cross-source, entity and review attribution

1. Compared every legal name, normalized name core, licence number and ten-digit phone with all 643 earlier records; resolved the Figs, Mayorga, Dom's, Magic and Advance/Expert collisions before counting.
2. Compared City registry names, phones and addresses with regulator fields. Reissued entities and divergent contact details remain discrepancy flags.
3. Checked Yelp, Thumbtack, Reddit, Google-indexed, BuildZoom and official/business evidence under each source's access limit. Four Thumbtack excerpts were attributable; no blocked or namesake text was attached.

### Pass 33 — fail-closed qualification and project checks

1. Audited status and classes against both required trades. C51 was added to the allowed regulator vocabulary; C10-only is permitted only as a non-promotable scope exclusion.
2. Rechecked service area, insurance, exact difficult-overflow experience, ceiling access/restoration, finish matching and written repair-first scope gates. No record passes all gates.
3. Validated unique ids and sources, HTTPS links, source references, review assignments, public-data privacy, empty master state, rendered output and source-monitor rules. The final master remains empty.

## Final counts

| Measure | Result after merge |
| --- | ---: |
| Businesses | 693 |
| Discovery waves | 14 |
| Distinct direct CSLB detail pages | 286 |
| Active licence records | 189 |
| Non-active licence records | 95 |
| Records without a direct regulator read | 409 |
| Retained excerpts | 159 |
| Source references | 621 |
| Qualified master entries | 0 |

The merge backup is intentionally outside the public site under ignored `reports/research_before_wave14.json`.
