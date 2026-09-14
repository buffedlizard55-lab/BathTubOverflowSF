# Sunset Repair · BathTubOverflowSF

A static, source-linked research workspace for a repair-first bathtub overflow problem in San Francisco’s Outer Sunset. It covers both sides of a possible job:

- **plumbing diagnosis and repair**, prioritizing a careful attempt before hidden-pipe replacement; and
- **drywall, ceiling, framing, and access restoration** if an opening becomes necessary.

**Target Pages URL:** https://buffedlizard55-lab.github.io/BathTubOverflowSF/

## Current research snapshot

**Checked through September 14, 2026 · twelve waves**

| Measure | Current result |
| --- | ---: |
| Unique business research records | **601** |
| Direct CSLB license-detail reads | **218** |
| BuildZoom-verified CSLB reads | **3** |
| Records with an active license at check time | **147** |
| Records with a non-active license | **70** |
| Records with no direct regulator read | **384** |
| Retained review excerpts | **147** |
| Evidence references | **517** |
| Held or scope-excluded records | **91** |
| Active-license records with regulator-recorded 94122 area evidence | **37** |
| Fully qualified master entries | **0** |

These are discovery and verification records, **not 601 approved contractors**. The qualified master remains empty because no business has all required evidence for legal identity, current relevant licensing, present Outer Sunset dispatch, applicable project insurance, exact difficult-overflow experience, and a written repair-first scope.

## Wave 12: 50 new records with BuildZoom CSLB verification

Wave 12 adds **50 nonduplicate businesses** from fresh platform discovery across Yelp, Thumbtack, BuildZoom, Google, Reddit, Porch, and company websites. The wave prioritises businesses advertising combined plumbing and drywall/repair services, old-house experience, and verified Outer Sunset service.

**Key CSLB discoveries via BuildZoom:**

| Business | License | Classifications | Status | Significance |
| --- | --- | --- | --- | --- |
| Rapid Flow Plumbing & Rooter Inc | 1115649 | B (General Building) + C-36 (Plumbing) | Active through Jan 2028 | Dual-licensed: can perform both plumbing AND general building/drywall work |
| Handyman Heroes Inc | 1003394 | B + C-10 (Electrical) + C-36 (Plumbing) | Active | Triple-licensed; SF DBI permit at 1225 Quintara St (94122/Outer Sunset) |
| Repipe Champions Plumbing and Rooter | 1057926 | B + C-36 + C-22 + C-2 | Active | Includes drywall patching in every repipe; galvanized pipe expertise |

- **51 new sources** (IDs 475–525) and **10 retained review excerpts** (R138–R147)
- **5 false claims rejected** — Yelp/Thumbtack badges are not CSLB reads; proximity search results are not service confirmation
- No record was promoted, assigned a priority, or added to the qualified master; wave 12 remains fully held or research-only
- The three BuildZoom reads are treated as third-party aggregator evidence; direct CSLB `LicenseDetail.aspx` reads remain the verification gold standard

## Wave 11: 50 new records in three published evidence tiers

Wave 11 adds **50 nonduplicate businesses** after identity, phone, normalized-name, licence-number and source checks against the earlier corpus. It keeps the evidence tiers separate and publishes three verification upgrades against existing records rather than counting them as new businesses:

| Tier | Records | What was read | What the record may assert |
| --- | ---: | --- | --- |
| CSLB read directly | **42** | `LicenseDetail.aspx` opened and transcribed field by field | legal entity, business form, address, phone, issue and expiry dates, status text, every classification, bond, workers’ compensation, liability lines and Additional Status |
| Registry only | **4** | City open-data permit registries | a recorded firm name, address, phone, licence **number** and permit identifiers — nothing more |
| Platform listing | **4** | Thumbtack category page read directly | the listing’s own category, hire count or review text, with no licence implication |

- **28 active** and **14 non-active** licenses among the 42 direct reads; every non-active one is held
- **3 verification upgrades** attached to `amx`, `sugar-bear` and `a1-plumbing`; the expired upgrade remains held
- **66 new sources** (IDs 401–474, with deliberate gaps in the artifact IDs) and **4 retained review excerpts** (R134–R137)
- No record was promoted, assigned a priority, or added to the qualified master; wave 11 remains fully held or research-only
- The adjacent-ZIP discovery channel is evidence of a recorded registry address only. It does not establish present Outer Sunset dispatch, both-trade coverage, insurance, or exact repair experience.

The four registry-only records carry `license: null` and the trade value `registry-lead` (“Registry lead · classification not read”). A registry lead is structurally incapable of reaching the master list because it has no regulator-backed classification. The four platform records likewise carry no CSLB fact, even when the platform displays a “Licensed pro” badge. All four attached review excerpts are retained as platform evidence and marked `exactTask: false`.

## Wave 10: 50 new records in three published evidence tiers

Wave 10 adds **50 nonduplicate businesses** after normalized name, near-name, phone, and CSLB-number collision checks against all 451 earlier records. Thirty-three further candidates were rejected as duplicates; none was stored twice. It keeps three evidence tiers separate on every record:

| Tier | Records | What was read | What the record may assert |
| --- | ---: | --- | --- |
| CSLB read directly | **23** | `LicenseDetail.aspx` opened and transcribed field by field | legal entity, business form, address, phone, issue and expiry dates, status text, every classification, bond, workers’ compensation, liability lines, Additional Status |
| Registry only | **22** | City open-data permit registries | a recorded firm name, address, phone, license **number**, and permit identifiers — nothing more |
| Platform listing | **5** | Thumbtack category pages read directly | the listing's own category, hire count or review text, with no licence implication |

- **15 active** and **8 non-active** licenses among the 23 reads; every non-active one is held, and across all 33 regulator pages opened in this wave the split is 21 active and 12 non-active
- **10 verification upgrades** and **2 registry upgrades** applied to records earlier waves had stored without a regulator read — including the trade correction on a wave-6 record whose license (635360) holds B only
- **the first license in the corpus carrying C-9 drywall and C36 plumbing together** (Sederap's Drywall Inc, 917252, also B and C10)
- **48 new sources** (IDs 353–400), 37 of them official CSLB or City pages
- **5 review excerpts** attached (R129–R133); every other platform or community extract stayed a source
- **24 discrepancy flags** and **40 hold flags** raised in this wave alone

Registry-only records carry `license: null` and the trade value `registry-lead` (“Registry lead · classification not read”). That value requires no CSLB class, so `licenseSupportsTrade()` returns false and `mayPromote()` can never be satisfied: **a registry lead is structurally incapable of reaching the master list.** Each of those records repeats the caveat in its area text, in a `hold`-level flag, and in its plain gap list.

Discovery ran licence-first from the two City contact registries — every licence with a 94122 firm address in `k6kv-9kix` and every `license1` with a 94122 firm ZIP in `3pee-9qhc`, grouped and ordered by permit count — then to completed 94122 drywall- and plumbing-scope permits in `i98e-djp9` and `a6aw-rudh`, then to the Thumbtack drywall and plumbing category pages. There is still no CSLB bulk API; license facts come from `cslb.ca.gov` one page at a time.

### Most relevant new directions—not additions to the call order

- **Sederap's Drywall Inc (917252)** — active **C-9 drywall plus C36 plumbing** on one licence, with B and C10 as well, and 113 registry permit rows at its 94110 firm address. The closest single-licence match to this project's two required trades verified so far, and **held anyway**: no review was attributable to it and its registry address does not match the regulator's.
- **Hawk N Lee Design & Construction Company (324708)** — active A, B, C10 and C36 on one licence, placed by CSLB itself inside ZIP 94122 (1032 Irving Street #930), with registry name and address conflicts flagged.
- **Oran Plumbing Corp (762214)** — active C36 with the largest 94122 permit count of any still-active licence read in this wave (362 rows); the regulator names the qualifying individual who resolves a phone overlap with an earlier stored record.
- **National Plumbing (619642)** — wave 10 upgraded a stored discovery record to a regulator read: active C36 with 1,036 registry permit rows and CSLB's own 1472 24th Avenue, 94122 address.
- **Canel Solutions** — the wave's drywall-category platform listing whose attached review describes a wall and a ceiling rebuilt, insulated, textured and painted after being opened.
- **Repipe Specialists (San Francisco Bay Area)** — a plumbing platform listing whose attached review describes walls and ceiling cut open for pipe access, visqueen sheeting, and the closed finish afterwards; no licence is asserted for the listing.

Every one remains outside the qualified master.

## Wave 9: 50 new records in two published evidence tiers

Wave 9 adds **50 nonduplicate businesses** after normalized name, near-name, phone, and CSLB-number collision checks against all 401 earlier records. Unlike earlier waves it does **not** claim a regulator read for every record, and the split is stated on each record rather than smoothed over:

| Tier | Records | What was read | What the record may assert |
| --- | ---: | --- | --- |
| CSLB read directly | **17** | `LicenseDetail.aspx` opened and transcribed field by field | legal entity, business form, address, phone, issue and expiry dates, status text, every classification, bond, workers’ compensation, liability lines, Additional Status |
| Registry only | **33** | City open-data permit registries | a recorded firm name, address, phone, license **number**, and permit identifiers — nothing more |

- **12 active** and **5 non-active** licenses among the 17 reads; every non-active one is held
- **35 completed permits** at work-location ZIP 94122 across both tiers
- **4 licenses hold both plumbing and building classifications** (786183, 1013565, 373337, 341277)
- **2 records earned the Outer Sunset area label**, because only for those does CSLB itself — not a directory — place the business in ZIP 94122
- **7 review excerpts** attached; every other platform or community extract stayed a source
- **47 new sources** (IDs 306–352), 29 of them official government pages
- **15 discrepancy flags** and **7 holds** raised in this wave alone

Registry-only records carry `license: null` and the trade value `registry-lead` (“Registry lead · classification not read”). That value requires no CSLB class, so `licenseSupportsTrade()` returns false and `mayPromote()` can never be satisfied: **a registry lead is structurally incapable of reaching the master list.** Each of those records repeats the caveat in its area text, in a `gap`-level flag, and in its plain gap list.

Discovery ran from permits to contacts — the reverse of wave 8 — using completed 94122 permits in `a6aw-rudh` and `i98e-djp9`, joined to their recorded contacts in `k6kv-9kix` and `3pee-9qhc`, plus a firm-ZIP 94122 sweep of both contact registries. There is still no official CSLB bulk API; license facts come from `cslb.ca.gov` one page at a time.

### Most relevant new directions—not additions to the call order

- **Innovation Plumbing and Rooter (1013565)** — active C-36 **and** B on one license, with completed 94122 permit 202510288289 whose printed scope combines new drain and water lines with “replace a section of drywall apprx. 2x4'”. The closest plumbing-plus-finish match verified in wave 9, and **held anyway**: its only public review is a single 1.0-star Yelp entry on an unclaimed listing whose text could not be retrieved.
- **Coit Construction (341277)** — active B and C-36 on one license since 1977, with a completed 94122 permit installing about 700 sq ft of 5/8 type sheetrock. Three ZIP variants across CSLB, the plumbing registry, and the building-permit contact row; BuildZoom reports no reviews.
- **CT Plumbing & Fire Protection (1112261)** — active C-36 plus C-16, and the only wave-9 record where the regulator itself places the business inside ZIP 94122 (1847 48th Ave). The same address and phone are already stored against a different, never-read license number.
- **Smelly Mel’s Plumbing Inc (786183)** — active A, C-36, B and C-16 with two completed 94122 sewer permits, and three attributable HomeAdvisor reviews. One displays 1.0 stars while its text reads as satisfied; both are preserved as published.
- **KNB Tile and Stone Inc dba KNB Remodeling (1120735)** — active **B-2** Residential Remodeling plus B on a completed 94122 permit reading “replace tub in same location upgrade plumbing up to code as needed”, with no C-36 on the license.
- **Kevel Home Performance (registry-only)** — a 94122 firm address with five plumbing and water-heater permit rows and four attributable reviews, including one describing work carried out while tenants were in place. Its Yelp categories are HVAC, energy and insulation, no CSLB page was read, and Angi prints that it does not offer free estimates.

Every one remains outside the qualified master.

## Wave 8: 50 new records

Wave 8 added **50 nonduplicate businesses** after normalized name, phone, and CSLB-number collision checks against all 351 earlier records.

- **23 plumbing-side records** and **27 restoration/general-building records**
- **50 CSLB detail pages read directly**
- **40 active** and **10 non-active** licenses at the check date
- **17 completed plumbing permits** joined to license contacts and work-location ZIP 94122
- **27 completed restoration permits** joined to license contacts and work-location ZIP 94122
- **23 selected review excerpts**, all marked `exactTask: false`
- **84 new sources**, including the current San Francisco Plumbing Code §104.2 page

The permit joins use separate official City datasets for contact identity and permit detail. A retained permit can establish a historical license contact, completion status, work ZIP, date, and described scope. It **cannot** establish current dispatch, current insurance, who performed every task on a multi-contact permit, or experience with the exact overflow mechanism.

### Most relevant wave-8 directions—not additions to the call order

- **Flow Form Plumbing** — active C-36; completed 94122 permit; indexed evidence mentions very old tub/shower fixtures and profile content describes avoiding tile work on an old valve. No stuck-overflow result was found.
- **Holland Plumbing Works** — active C-36; completed 94122 permit history; a dated syndicated account describes repair of a shower-handle mechanism. It is not an overflow trip lever and dates to 2011.
- **Axion Plumbing** — active C-36; completed 94122 house-trap/main-line work; one bathroom-diagnosis recommendation. Two published phone numbers conflict.
- **Bay Metro Corporation** — active B and C-36; completed 94122 framing/drywall permit; restoration and contractor-coordination evidence. No small access-hatch outcome was found.
- **Pro-Care Restoration Inc** — active B/C-22; completed 94122 water-damage drywall work; stated San Francisco County coverage. Duplicate review text, address variation, and an unsubstantiated negative allegation remain flagged.
- **Hargens Inc** — active B, C-36, C-33, C-43, and C-20; completed 94122 water-damage drywall/plumbing-leak permit. Exact access and finish matching remain unverified.

## Three additional verification passes (run for every wave)

After each discovery pass the project runs three further fail-closed passes. Wave 9’s were Passes 19–21; wave 10’s were Passes 22–24; wave 11’s were Passes 25–27:

1. **Regulator pass (19)** — 17 CSLB detail pages opened directly and transcribed field by field, including bond, workers’ compensation and liability lines; five licenses found non-active; the complaint disclosure behind 1017991 read as a separate page; every registry license number that was *not* read published as a lead with `license: null`.
2. **Cross-source pass (20)** — registry identity compared with regulator identity field by field, producing 15 discrepancy flags: four phone conflicts, six registry spellings of one licensee, a license reissued to another entity in 2006, three ZIP variants on one active multi-trade license, and one address plus phone shared by two different license numbers. Directory pages checked for review corpora; unattributable Thumbtack category quotes and Reddit task threads quarantined as sources; CSLB class **B-2** discovered and added to the schema rather than mapped onto B.
3. **Fail-closed qualification pass (21)** — no record promoted, the master list left empty, the nine-call order unchanged; holds raised for expired and inactive licenses, a workers’-compensation cancellation dated before the research date, and a single unreachable 1.0-star review; public-data privacy scrub; structural, render and browser tests re-run; merge verified idempotent.

The reproducible gates are in [`scripts/merge_wave11.py`](scripts/merge_wave11.py), [`scripts/merge_wave10.py`](scripts/merge_wave10.py), [`scripts/merge_wave9.py`](scripts/merge_wave9.py) and [`scripts/merge_wave8.py`](scripts/merge_wave8.py); the evidence trails are in [`data/wave11-discovery-log.md`](data/wave11-discovery-log.md), [`data/wave10-discovery-log.md`](data/wave10-discovery-log.md), [`data/wave9-discovery-log.md`](data/wave9-discovery-log.md) and [`data/wave8-discovery-log.md`](data/wave8-discovery-log.md).

## Review evidence and access limits

This project does **not** claim a complete all-review corpus.

- Tested Yelp pages frequently returned access barriers; indexed extracts and Yahoo-fed Yelp excerpts are labeled as such.
- The original Google panel was not retrieved. Three Google-attributed rows were read only through Birdeye and are labeled **Google via Birdeye**. A directory’s “Google 4.8 from 243 reviews” restatement for Smelly Mel’s could not be confirmed on Google and is stored as an unverified third-party claim, never rendered as a Google rating.
- Wave 9 attached seven excerpts only: three HomeAdvisor reviews for Smelly Mel’s (identity matched on exact corporate name, city, and the CSLB phone) and four for Kevel Home Performance (identity matched on the Yelp listing’s own 3624 Ortega St 94122 address and (415) 213-5545 phone, both identical to the City registry row). `published` stays `null` wherever a platform shows only a month and year — no day is invented.
- Yelp’s 4.5-star aggregate for Discount Plumbing Rooter Services was reachable only as JSON-LD photo-caption metadata, so it is quarantined as a source and no excerpt is attached. Yelp’s single 1.0-star review for Innovation Plumbing could not be retrieved at all; the record is held and nothing is attached.
- BuildZoom states that the Coit Construction, Yu Plumbing and H&J Plumbing profiles “haven’t received any reviews”. Absence of reviews is stored as a gap, never as a neutral or positive signal.
- Four Reddit threads in wave 9 are directly on-task for the repair itself — a stuck trip lever where penetrating oil and steam failed and the work “went thru the drywall”; access “from behind and below” through a downstairs neighbour’s ceiling with galvanized rust debris; a 1940s tub with an odd 1⅜ inch pipe; and a reply framing the patch as “sheetrock isn’t hard”. **None names a business**, so none became a review.
- No safely attributable new wave-8 or wave-9 Thumbtack review was found. Earlier-wave Reddit and Thumbtack evidence remains separately labeled.
- National Safe Step review corpora were rejected because continuity to the California contracting entity was not established.
- A mismatched “DC Plumbing” review corpus was rejected rather than attached to license 1115284.
- Business-hosted testimonials are labeled `company-published`, never presented as independent reviews.
- Negative claims are retained as allegations, not converted into factual findings.

Ratings are not blended across platforms. Inaccessible text remains incomplete rather than reconstructed.

## Important wave-9 irregularities

- **Admonishment letter on an active license.** San Francisco Remodel (1017991) is active with B only, and its CSLB page points to complaint disclosure: Complaint # N A 2025 2297, dated 06/23/2026, status **LETTER OF ADMONISHMENT ISSUED**. CSLB states a listed complaint is only an allegation of a probable violation and does not affect license status, so it is recorded as an allegation — and the firm’s completed 94122 permit includes plumbing repair it holds no C-36 for.
- **Plumbing-scope permits without C-36.** Three licenses appear on City plumbing or plumbing-scope permits while CSLB shows no C-36: Euro Plumbing Inc dba General Contractor (1028917, B only, expired 2021), San Francisco Remodel (1017991, B only), and KNB Remodeling (1120735, B-2 and B, on a tub-replacement permit). Wave 8 had rejected 1028917 for a name mismatch; wave 9 opened the page and resolved it, so it is stored as a documented hold rather than dropped.
- **One address and phone, two license numbers.** CSLB reads CT Plumbing & Fire Protection (1112261) at 1847 48th Ave, 94122 with (415) 203-7178 — the same address and phone the City registry stores for “C T Construction & Plumb” under license **533324**, which has never been read on CSLB. Re-licensing, shared office, and registry error all remain open. This is the wave’s only permitted phone overlap, and the merge gate accepts it **only** if the record publishes it.
- **Six registry spellings of one licensee, and a 2006 reissue.** Lam Pui (373337) appears under six firm-name variants in the 94122 registry rows; CSLB shows the license expired 2010 and “LICENSE REISSUED TO ANOTHER ENTITY” on 04/06/2006, so the number no longer identifies the original contractor.
- **Registry name does not match the regulator.** License 342141 is stored in the registry as “L & L Plumbing Inc.” with a 94122 address, but the CSLB licensee is LEE’S PLUMBING CO at 94118, expired 1997, with “no workers comp information found for this license”.
- **Registry phone versus regulator phone (four conflicts).** 786183, 1097098, 1140843 and 1028917 each print a different phone in the City registry than on their CSLB page. The CSLB reading is stored; the registry reading is flagged.
- **Workers’ compensation cancelled the day before the check.** Garzac Plumbing (830368) reads active, but State Fund policy 9242676 shows CANCELLATION DATE 09/11/2026 — one day before this research date. Held.
- **Directory misspelling and a same-address inactive entity.** BuildZoom prints Yu Plumbing (1051988) as “Yu Pluming” and links an inactive “Y&L Plumbing Inc” (1041444, expired 2018) at the same 148 San Diego Ave address. No record was created for 1041444.
- **City annotations left unresolved.** The registry prints “Kilb's Construction Inc\*\*\*Check Id\*\*\*”, two firm names against license 1033146, and “Boman Deign & Construction Inc” for 1111133. Each is flagged and the registry string is quoted as-read.
- **Trade coverage contradicted in both directions.** Kevel Home Performance (1021221) sits on plumbing and water-heater permit rows while its Yelp categories are HVAC, energy and insulation; two Yelp snapshots also disagree on whether the listing is claimed.
- **Star value contradicts review text.** The retained HomeAdvisor review from Michael N. displays 1.0 of 5 while its text reads as satisfied, and the extract ends mid-phrase. Both are preserved exactly as published and the mismatch is flagged.
- **B-2 is a real classification the schema did not have.** `ALLOWED_CLASSES` in `lib.js` gained `"B-2"` rather than mapping it onto B, because a residential-remodeling license does not carry the same scope as a general building license.

No irregularity is treated as wrongdoing unless an official source actually establishes it.

## Existing diagnostic call order

The site retains the earlier nine-entry **diagnostic conversation order**. Waves 8 and 9 do not add or reorder it.

1. Fast Response Plumbing & Rooter
2. Heise’s Plumbing
3. Genteel Plumbers
4. O’Donovan Plumbing Inc
5. Expert Plumbing Solutions
6. Building Efficiency Inc
7. Faherty Plumbing and Heating
8. De Barra Plumbing
9. Michael Kuenzli Plumbing Co

This is an editorial order for further questions—not a workmanship ranking, booking approval, or guarantee. None is in the qualified master.

## Promotion gates

A business can enter the qualified master only when all gates are supported:

1. exact legal entity and active classification appropriate to the work;
2. current Outer Sunset dispatch coverage;
3. documented relevant seized-overflow experience;
4. applicable insurance and a written non-destructive-first scope; and
5. no unresolved blocking identity, status, classification, or coverage issue.

`lib.js` and the merge scripts enforce the gate. Missing evidence never becomes a positive assumption. Registry-only records cannot satisfy gate 1 by construction, because a record with no license read supports no trade.

## Permits and current official guidance

Both sources were read on September 12, 2026 and were not re-read during wave 9, so their stamps and published facts are unchanged:

- [SF.gov · Apply for a plumbing and mechanical permit](https://www.sf.gov/apply-plumbing-and-mechanical-permit)
- [San Francisco Plumbing Code §104.2 · Exempt Work](https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_building/0-0-0-85830)

The City page states the trigger for cutting into or replacing pipes and requires inspection before permitted pipes are covered. Section 104.2 lists narrow categories whose wording turns on what is actually cut into or removed. The dataset reports that text without deciding how it applies to an unseen condition; the contractor and DBI must confirm the actual scope.

## Privacy and responsible publication

Only a generalized repair objective and public business evidence belong in this repository. Nonpublic project details and personal data are excluded. A one-way-fingerprint regression test scans repository text artifacts so excluded context is not restated in the test itself — it scans every text file, including wave logs, generators and UI copy, and it rejected one draft phrase during wave 9.

The project does not contact businesses, submit forms, book appointments, bypass access controls, or store credentials. Public source links are retained for manual review.

## Use the site locally

Requirements: Python 3.11+ and Node 22.

```sh
npm ci
npm start
# open http://localhost:4173
```

The development server binds to `0.0.0.0` for remote previews and exposes only the public site files.

Run validation:

```sh
npm test
npm run test:monitor
npm run test:browser
```

Rebuild and validate wave 11 from a clean wave-10 dataset:

```sh
git checkout -- data/research.json   # restore the committed 501-record baseline first
python3 scripts/gen_wave11.py        # rebuilds data/wave11.json and runs a collision pre-flight
python3 scripts/merge_wave11.py      # fail-closed merge; idempotent after a successful run
npm test
npm run test:browser
```

The wave-11 merge verifies source links, identity and licence collisions, registry/platform tier boundaries, classification coverage, review attribution, privacy, non-active holds and upgrade targets before writing the merged dataset. It does not promote records to the master list.


## Read-only source monitoring

```sh
npm run audit:sources
# bounded smoke check
python3 scripts/check_sources.py --limit 3
```

The monitor validates public network targets, respects robots policy, rate-limits hosts, checks redirects and retained excerpts, and quarantines newly seen JSON-LD review candidates. It never overwrites research or promotes a business. HTTP success is not semantic verification.

Reports are written under `reports/` and are ignored by Git. The `Public source audit` workflow also supports manual runs and a weekly default-branch schedule.

## GitHub Pages

`Test and deploy Pages` runs Node, Python, render, and browser validation; then stages only:

- `index.html`, `styles.css`, `app.js`, and `lib.js`
- `assets/mark.svg`
- `data/research.json`

Actions deployment occurs from `main` when the repository uses the Actions Pages build type. Session-branch runs validate and build but intentionally do not alter repository Pages settings. Both workflows now trigger on `main` and on this session branch, so wave-11 pushes are validated; deployment remains `main`-only.

This workspace is fixed to branch `arena/01a097d2-bathtuboverflowsf`; no other branch is used.

## Key files

```text
index.html, styles.css, app.js    Static GitHub Pages UI
lib.js                           Filters, exports, counts, allowed classes, and promotion gate
data/research.json               Merged schema-v2 dataset (551 records, 11 waves)
data/wave2.json … wave11.json    Reproducible per-wave artifacts
data/wave*-discovery-log.md      Source, rejection, and irregularity trails
scripts/gen_wave11.py            Wave-11 generator (three evidence tiers plus upgrades)
scripts/merge_wave11.py          Collision-, privacy- and tier-gated fail-closed merge
scripts/gen_wave10.py            Wave-10 generator (three evidence tiers)
scripts/merge_wave10.py          Wave-10 collision-, privacy- and tier-gated merge
scripts/gen_wave9.py             Wave-9 generator (two evidence tiers)
scripts/merge_wave9.py           Collision-, privacy- and tier-gated fail-closed merge
scripts/gen_wave8.py             Wave-8 generator
scripts/merge_wave8.py           Wave-8 fail-closed merge
scripts/check_sources.py         Read-only source monitor
scripts/serve.py                 Public-file-only preview server
tests/research.test.js           Dataset, collision, privacy, and qualification invariants
tests/render.test.js             Browser-free rendering checks
tests/browser/site.spec.js       Browser, accessibility, export, and mobile checks
tests/test_monitor.py            Source-monitor unit tests
.github/workflows/               Pages validation and source-audit automation
```
