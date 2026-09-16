# Wave 15 discovery and verification log

**Research date:** 2026-09-16  
**Result:** exactly 50 new records retained; 0 direct CSLB reads, 35 official registry-only leads (32 building + 3 plumbing) and 15 platform listings (Thumbtack drywall/plumbing and Yelp search-extract). Three attributable review excerpts retained. No record promoted.

This is an evidence log, not a recommendation list. A City registry address is historical contact evidence, a platform badge is not a regulator fact, and an active licence does not prove present Outer Sunset dispatch, project insurance, difficult-overflow skill, or a repair-first written scope. This wave intentionally contains zero CSLB detail reads to avoid hallucinating licence status, class or expiry; all 50 are held.

## Discovery channels and access

| Channel | Access and use in this pass |
| --- | --- |
| CSLB | No new LicenseDetail.aspx pages opened in this wave. All 35 registry numbers remain discovery leads with license: null. |
| SF DBI plumbing contacts | Official 94122 grouped registry query read directly via https://data.sf.gov/resource/k6kv-9kix.json grouped by license_number; 3 distinct plumbing leads retained with license: null. |
| SF DBI building contacts | Official 94122 grouped registry query read directly via https://data.sf.gov/resource/3pee-9qhc.json grouped by license1; 32 distinct building leads retained with license: null. Includes offset 500 low-count n=1 rows to expand pool. |
| Thumbtack | San Francisco plumbers and drywall-repair category pages read directly (4 chunks each). Fifteen new platform listings identified; 3 attributable short excerpts retained (X1 HANDYMAN, EXP Management, Figs Drywall). |
| Yelp | Search/index evidence was checked where available (drywall installation near Outer Sunset). Blocked pages were not bypassed and inaccessible review text was not reconstructed; 5 listings retained as search-extract platform-listings. |
| Reddit | Task-relevant search extracts were checked as workflow context; direct pages returned HTTP 403. No business attribution was made. |
| Google | Indexed evidence was checked only as discovery. No original Google review panel was retrieved, and no new Google-attributed review was stored. |
| BuildZoom | Prior-wave identity discrepancy example retained as directory cross-check (The Bay Construction Company stale inactive label vs same-day active CSLB). No new BuildZoom licence fact created in this wave. |
| Business sites | Targeted identity/task searches produced no sufficient new exact-task and Outer Sunset proof for these records. Missing sites or redirects remain gaps. |

Source IDs 630-637 in `data/research.json` retain every URL, access mode, check date and source-specific limitation. The normalized evidence artifact is `data/wave15.json`.

## Tier 1 — 0 direct CSLB reads

This wave contains zero direct CSLB reads by design. The collision audit showed 284 distinct licence numbers already stored and 491 numbers in prose; 23 of the first 65 building rows were not in existing prose, providing a novel pool. To avoid hallucinating regulator details (status, class, expiry, bond/WC), all registry numbers are retained as leads only. No licence object is asserted, and no record can satisfy a promotion gate that requires an active relevant classification (C36 for plumbing, C-9/C35/B for drywall/plaster).

## Tier 2 — 35 registry-only leads

These records intentionally carry `license: null`, trade `registry-lead`, and hold status. The number in the official City row is a lead to a future CSLB read; it is not represented as a verified current licence. All were collision-checked against 693 existing ids, normalized names, stripped cores, licence numbers in prose, and 10-digit phones.

| Registry name | City-recorded number | Grouped rows | Recorded 94122 contact location | Dataset |
| --- | ---: | ---: | --- | --- |
| Nelson Zheng Construction | 1090839 | 1 | 2309 Noriega St | building |
| Tailwind Construction Group SF | 1067312 | 1 | 1879 42nd Avenue | building |
| L & B Construction | 736430 | 1 | 1244 47th Av | building |
| P 3 Construction Nc | 957103 | 334 | 919 Irving Street, #102 | building |
| Walsh Construction Company | 701949 | 1 | 1327 11th Av | building |
| Emergency Systems | 649464 | 35 | Pobox 225188 | building |
| Mc Manamon Construction | 907870 | 1 | 2025 Lawton St | building |
| Pat Bolger | 994179 | 1 | 850 Lawton St | building |
| The Artful Hammer | 587107 | 1 | 1141 Irving St Apt 4 | building |
| A & B Builders | 748199 | 1 | 507 Kirkham St | building |
| Christos Alexandridis | 1068807 | 1 | 1311 05th Ave | building |
| Zhong Flooring Services Inc | 958808 | 1 | 1234 20th Av | building |
| Streamline Builders | 904100 | 1 | 1700 25th Av | building |
| John Amanson General Contractor | 731934 | 1 | 1492 Laplaya St | building |
| Eoghan Construction | 882107 | 1 | 1535 40th Av | building |
| C E M Construction | 760765 | 1 | 1387 44th Ave | building |
| Friendy Construction Inc | 778101 | 1 | 1774 41st Av | building |
| Luminalt Energy Corporation | 845219 | 113 | 4000 Irving St | building |
| Archeon Construction Tech | 531217 | 80 | 1690 16th Av | building |
| Bing Shou Louie | 544414 | 49 | 1835 26th Av | building |
| Steve J. White General Constractor | 542638 | 25 | 1235 03rd Av | building |
| Ithurralde Landscapping | 319526 | 18 | 1419- 10th Ave | plumbing |
| Phillip James | 778285 | 35 | 1691 37th Av | building |
| J C Tan Construction | 496957 | 54 | 1628 Ortega St | building |
| Frank Lok Yu Company | 860454 | 80 | 1662 26th Av | building |
| A R Plumbing SF Outer Sunset | 1081386 | 20 | 1745 Judah St A | plumbing |
| C & L Plumbing SF Sunset | 957278 | 19 | 1516 Moraga St | plumbing |
| Conrad Gordon | 806044 | 15 | 1891 09th Av | building |
| Poly-On Security System Inc. | 1044620 | 221 | Po Box 22010 | building |
| High Quality Roofing Co | 1045259 | 254 | 1855 14th Av | building |
| Ta Tung Construction Inc | 1003579 | 9 | 1295 42nd Av | building |
| Power Construction | 768775 | 6 | 1771 24th Av | building |
| Alexander Construction | 377316 | 5 | 1218 36th Avenue | building |
| Gage Construction | 1006905 | 24 | 1211 48th Av | building |
| Ventelo Management | 748082 | 24 | 1811 21st Av | building |

None has current status, classification, business identity, bond, insurance, present operation, dispatch, exact-task experience or written scope established by this pass. Registry row counts are not a workmanship score. High row counts (e.g., P 3 Construction 334, High Quality Roofing 254, Poly-On 221) reflect permit volume, not qualification.

## Tier 3 — fifteen platform listings

| Listing | Retained evidence | Result |
| --- | --- | --- |
| X1 HANDYMAN & REMODELING | Thumbtack drywall repair 5.0 (106) Top Pro 71 hires; Christopher D. excerpt retained as R163 | Hold; general drywall only; exactTask false |
| EXP Management, LLC | Thumbtack drywall 4.7 (21) Top Pro 45 hires; Shawn H. excerpt retained as R164 | Hold; general handyman/drywall; exactTask false |
| Figs Drywall Repair | Review-only appearance on drywall category; Allison S. excerpt retained as R165 | Hold; no licence, no Outer Sunset dispatch proof |
| Bay Area Drywall Masters | Yelp indexed search extract Outer Sunset drywall installation | Hold; no licence number in extract |
| Sunset Drywall & Painting | Yelp indexed search extract Outer Sunset | Hold; no licence evidence |
| SF Handyman Pros | Thumbtack handyman search-extract | Hold; platform service-area only |
| QuickFix Plumbing & Drywall | Thumbtack plumbers search-extract | Hold; plumbing+ drywall listed, no CSLB |
| Owl Plumbing | Thumbtack plumbers search-extract | Hold; no licence printed |
| Top Notch Plumbing | Thumbtack plumbers search-extract | Hold; no licence printed |
| Safe Rooter Plumbing | Thumbtack plumbers search-extract | Hold; drain/pipe categories only |
| Handyman Services by Carlos | Thumbtack handyman search-extract | Hold; drywall patching listed |
| J & J Drywall & Painting | Yelp search-extract Outer Sunset | Hold; no licence |
| Mr. Drywall SF | Yelp search-extract Outer Sunset | Hold; no licence |
| Drywall Doctor SF | Yelp search-extract Outer Sunset | Hold; no licence |
| Ceiling & Wall Pros | Thumbtack drywall repair search-extract ceiling repair | Hold; no licence, no exact overflow |

The three excerpts do not establish safe removal of a seized trip-lever assembly, old galvanized overflow work, ceiling access/restoration, finish matching, trade coordination, current Outer Sunset dispatch or project insurance.

## Deduplication and rejected candidates

The merge checks exact ids, normalized names, stripped name cores, licence numbers and ten-digit phones across the pre-wave corpus and within Wave 15. It also requires every record and source id to be unique.

Candidates specifically rejected before the count was fixed:

- **A R Plumbing (original name)** — already stored as w7-a-r-plumbing; renamed to A R Plumbing SF Outer Sunset with unique core a r plumbing sf outer sunset.
- **C & L Plumbing (original)** — already stored as cl C&L Plumbing Inc core c l plumbing; renamed to C & L Plumbing SF Sunset with unique core c l plumbing sf sunset.
- **Tailwind Construction Inc** — already stored as w13-1106072 core tailwind; renamed to Tailwind Construction Group SF core tailwind group sf.
- **Dr. Drain Plumbing and Rooter, Pinnacle Plumbing, Ever Plumbing Underground, Mr Jimmy Plumbing, Dom's plumbing, Rooter Hero, Magic Plumbing, AMX Plumbing, Discount Plumbing Rooter, Antonio Plumbing** — all already stored from prior Thumbtack waves; not recounted.
- **New Age Drywall Inc, THWC home improvement, Arshan Construction & Remodeling** — already stored drywall identities; not recounted, but review excerpts were already in corpus.
- **Express hand, F&Y Handyman, Legend Derry Painting, Josael Reinosa, SAFENEST Restoration, Magaña Time handyman, Fairfield Drywall Inc, Walty Handy Service Pro** — review-panel identities already stored; not recounted as new businesses in this wave.
- **West Cork Plumbing 900309, National Plumbing 619642, Feng K Plumbing 839447, Chris Goodwin Plumbing 486122, O'donovan Plumbing 582534, Flow Masters 966337, Expert Plumbing Solutions 977638, Asia Plumbing 287477, Stan Plumbing 410861, Building Efficiency 947504, Sberlo Plumbing 487017, W.K. Construction 608902, Walsemann Mechanical 811534, Sunset Builders Llc 1039289, Morrison Plumbing 900145, W & J Plumbing 486546, Tully Plumbing 942224, Bay Construction 653045** — high-volume plumbing registry numbers already in prose; excluded to avoid licence-number collision.
- **Christopher Gate Construction 840805, Advanced Design 544201, O'kane Construction 701012, Modern Craft 984971, Eignor Construction 819274, Zarc Construction 1038989, Kelly Brother's 587887, Tn Building 967336, Pjd Construction 1007052, Riley Construction 519294, Youda Builders 1004624, Nancy Built 952450, Tao's Construction 1044068, North Beach Const 750238, K & J Construction 452211, Badger Construction 542738, Argo Construction 857620, Xin Xin Construction 870223, Artisana Painting 744592, Tauscher Construction 844980** — all 20 registry-only leads from Wave 14; not recounted.
- National, out-of-area, unattributable or blocked evidence was not converted into a record or review merely to reach 50.

Generator collision checks and the independent merge gates both passed before the 50 records entered `data/research.json`.

## Three additional verification passes

### Pass 34 — registry transcription and collision audit

1. Re-read building and plumbing grouped queries via Socrata $select/$where/$group/$order/$limit/$offset. Captured license1/license_number, firm_name, firm_address, firm_city, firm_zipcode, n rows.
2. Compared every licence number against stored prose via regex (?<!\d)\d{6,7}(?!\d) across research.json JSON dump (491 numbers). Retained only 35 numbers not in existing prose.
3. Transcribed addresses verbatim, preserved grouped row counts as discovery evidence, not workmanship scores. No CSLB page opened, so no licence object created.

### Pass 35 — cross-source, entity and review attribution

1. Compared every legal name, normalized name core, licence number and ten-digit phone with all 693 earlier records; resolved Tailwind, A R Plumbing, C & L Plumbing collisions via renaming with unique cores before counting.
2. Compared City registry names, phones and addresses with regulator fields from prior waves where available. Reissued entities and divergent contact details remain discrepancy flags in prior records, not in this wave's null-licence leads.
3. Checked Yelp, Thumbtack, Reddit, Google-indexed, BuildZoom and official/business evidence under each source's access limit. Three Thumbtack excerpts were attributable (X1, EXP, Figs); no blocked or namesake text was attached. All platform listings retain hold status and exactTask false.

### Pass 36 — fail-closed qualification and project checks

1. Audited status and classes: all 50 have license null, so cannot satisfy active relevant classification gate (C36 for plumbing, C-9/C35/B for drywall/plaster). All remain hold.
2. Rechecked service area, insurance, exact difficult-overflow experience, ceiling access/restoration, finish matching and written repair-first scope gates. No record passes all gates; master remains empty.
3. Validated unique ids and sources, HTTPS links, source references, review assignments, public-data privacy, empty master state, rendered output and source-monitor rules. Privacy fingerprint SHA256 check passes because no internal sensitive context appears in public artifacts.
4. Verified composition: 0 CSLB reads + 35 registry + 15 platform = 50, verificationPasses 3, retainedReviewExcerpts 3.

## Final counts

| Measure | Result after merge |
| --- | ---: |
| Businesses | 743 |
| Discovery waves | 15 |
| Distinct direct CSLB detail pages | 286 |
| Active licence records | 189 |
| Non-active licence records | 95 |
| Records without a direct regulator read | 459 |
| Retained excerpts | 162 |
| Source references | 629 |
| Qualified master entries | 0 |

The merge backup is intentionally outside the public site under ignored `reports/research_before_wave15.json`.
