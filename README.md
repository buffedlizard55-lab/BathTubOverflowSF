# Sunset Repair · BathTubOverflowSF

A static, source-linked research workspace for a repair-first bathtub overflow problem in San Francisco’s Outer Sunset. It covers both sides of a possible job:

- **plumbing diagnosis and repair**, prioritizing a careful attempt before hidden-pipe replacement; and
- **drywall, ceiling, framing, and access restoration** if an opening becomes necessary.

**Target Pages URL:** https://buffedlizard55-lab.github.io/BathTubOverflowSF/

## Current research snapshot

**Checked through September 12, 2026 · eight waves**

| Measure | Current result |
| --- | ---: |
| Unique business research records | **401** |
| Direct CSLB license-detail reads | **120** |
| Records with an active license at check time | **81** |
| Records with a non-active license | **38** |
| Records with no direct regulator read | **282** |
| Retained review excerpts | **121** |
| Evidence references | **305** |
| Held or scope-excluded records | **50** |
| Active-license records with regulator-recorded 94122 area evidence | **23** |
| Fully qualified master entries | **0** |

These are discovery and verification records, **not 401 approved contractors**. The qualified master remains empty because no business has all required evidence for legal identity, current relevant licensing, present Outer Sunset dispatch, applicable project insurance, exact difficult-overflow experience, and a written repair-first scope.

## Wave 8: 50 new records

Wave 8 adds **50 nonduplicate businesses** after normalized name, phone, and CSLB-number collision checks against all 351 earlier records.

- **23 plumbing-side records** and **27 restoration/general-building records**
- **50 CSLB detail pages read directly**
- **40 active** and **10 non-active** licenses at the check date
- **17 completed plumbing permits** joined to license contacts and work-location ZIP 94122
- **27 completed restoration permits** joined to license contacts and work-location ZIP 94122
- **23 selected review excerpts**, all marked `exactTask: false`
- **84 new sources**, including the current San Francisco Plumbing Code §104.2 page

The permit joins use separate official City datasets for contact identity and permit detail. A retained permit can establish a historical license contact, completion status, work ZIP, date, and described scope. It **cannot** establish current dispatch, current insurance, who performed every task on a multi-contact permit, or experience with the exact overflow mechanism.

### Most relevant new directions—not additions to the call order

- **Flow Form Plumbing** — active C-36; completed 94122 permit; indexed evidence mentions very old tub/shower fixtures and profile content describes avoiding tile work on an old valve. No stuck-overflow result was found.
- **Holland Plumbing Works** — active C-36; completed 94122 permit history; a dated syndicated account describes repair of a shower-handle mechanism. It is not an overflow trip lever and dates to 2011.
- **Axion Plumbing** — active C-36; completed 94122 house-trap/main-line work; one bathroom-diagnosis recommendation. Two published phone numbers conflict.
- **Bay Metro Corporation** — active B and C-36; completed 94122 framing/drywall permit; restoration and contractor-coordination evidence. No small access-hatch outcome was found.
- **Pro-Care Restoration Inc** — active B/C-22; completed 94122 water-damage drywall work; stated San Francisco County coverage. Duplicate review text, address variation, and an unsubstantiated negative allegation remain flagged.
- **Hargens Inc** — active B, C-36, C-33, C-43, and C-20; completed 94122 water-damage drywall/plumbing-leak permit. Exact access and finish matching remain unverified.

Every one remains outside the qualified master.

## Three additional verification passes

After the wave-8 discovery pass, the project ran three further fail-closed passes:

1. **Line-by-line source pass** — legal name, status, classifications, expiry, address, phone, permit number, completion date, work ZIP, and condensed scope checked against the cited regulator or City row.
2. **Collision and attribution pass** — names, phones, and licenses checked against earlier records; review identity and duplicate text checked across accessible Yelp/search, Yahoo-fed Yelp, Nextdoor, Birdeye, GuildQuality, BuildZoom, Judy’s Book, and official business pages.
3. **Publication-safety pass** — status/classification/coverage flags rechecked, public artifacts privacy-scrubbed, City permit guidance and Code §104.2 re-read, then structural, render, browser, source-monitor, and privacy tests run.

The reproducible gates are in [`scripts/merge_wave8.py`](scripts/merge_wave8.py), and the evidence trail is in [`data/wave8-discovery-log.md`](data/wave8-discovery-log.md).

## Review evidence and access limits

This project does **not** claim a complete all-review corpus.

- Tested Yelp pages frequently returned access barriers; indexed extracts and Yahoo-fed Yelp excerpts are labeled as such.
- The original Google panel was not retrieved. Three Google-attributed rows were read only through Birdeye and are labeled **Google via Birdeye**.
- Birdeye displayed five Pro-Care rows but only three unique texts; two verbatim duplicate pairs were counted once each.
- No safely attributable new wave-8 Reddit or Thumbtack review was found. Earlier-wave Reddit and Thumbtack evidence remains separately labeled.
- National Safe Step review corpora were rejected because continuity to the California contracting entity was not established.
- A mismatched “DC Plumbing” review corpus was rejected rather than attached to license 1115284.
- Business-hosted testimonials are labeled `company-published`, never presented as independent reviews.
- Negative claims are retained as allegations, not converted into factual findings.

Ratings are not blended across platforms. Inaccessible text remains incomplete rather than reconstructed.

## Important wave-8 irregularities

- All **10 non-active licenses** are held and cannot be presented as bookable.
- **O’Connor Plumbing & Fire Protection** carries a CSLB reissue notice; confirm the current entity.
- **Chen’s Construction and Mechanical** has a 2008 permit-contact row under an earlier firm name, predating the current entity’s 2020 reissue. That row proves license-number history, not current-entity performance.
- **Axion Plumbing** has conflicting regulator and business/profile phone numbers.
- **Pro-Care Restoration** has duplicate republished review text, address variation, and one preserved but unsubstantiated negative excerpt.
- **Brus Box Contractor Works** markets plumbing, while CSLB lists B without C-36; the properly licensed plumbing performer must be identified. Its displayed workers-compensation date also requires a fresh check.
- **RPRW / James Macmillan**, **Gerson Construction**, and **Wolfe Painting** remain held on current coverage, pending-citation, or near-term status concerns described in their records.
- **Raxe Construction** has a workers-compensation policy date equal to the research date and requires rechecking.
- **Hargens** has a current regulator/site address and an older platform address; the discrepancy remains visible.

No irregularity is treated as wrongdoing unless an official source actually establishes it.

## Existing diagnostic call order

The site retains the earlier nine-entry **diagnostic conversation order**. Wave 8 does not add or reorder it.

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

`lib.js` and the merge scripts enforce the gate. Missing evidence never becomes a positive assumption.

## Permits and current official guidance

The project re-read both sources on September 12, 2026:

- [SF.gov · Apply for a plumbing and mechanical permit](https://www.sf.gov/apply-plumbing-and-mechanical-permit)
- [San Francisco Plumbing Code §104.2 · Exempt Work](https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_building/0-0-0-85830)

The City page states the trigger for cutting into or replacing pipes and requires inspection before permitted pipes are covered. Section 104.2 lists narrow categories whose wording turns on what is actually cut into or removed. The dataset reports that text without deciding how it applies to an unseen condition; the contractor and DBI must confirm the actual scope.

## Privacy and responsible publication

Only a generalized repair objective and public business evidence belong in this repository. Nonpublic project details and personal data are excluded. A one-way-fingerprint regression test scans repository text artifacts so excluded context is not restated in the test itself.

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

Rebuild and validate wave 8:

```sh
python3 scripts/gen_wave8.py
python3 scripts/merge_wave8.py   # idempotent after a successful merge
npm test
```

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

Actions deployment occurs from `main` when the repository uses the Actions Pages build type. Session-branch runs validate and build but intentionally do not alter repository Pages settings.

This workspace is fixed to branch `arena/01a09694-bathtuboverflowsf`; no other branch is used.

## Key files

```text
index.html, styles.css, app.js    Static GitHub Pages UI
lib.js                           Filters, exports, counts, and promotion gate
data/research.json               Merged schema-v2 dataset (401 records, 8 waves)
data/wave2.json … wave8.json     Reproducible per-wave artifacts
data/wave*-discovery-log.md      Source, rejection, and irregularity trails
scripts/gen_wave8.py             Wave-8 generator
scripts/merge_wave8.py           Collision-gated, privacy-gated fail-closed merge
scripts/check_sources.py         Read-only source monitor
scripts/serve.py                 Public-file-only preview server
tests/research.test.js           Dataset, collision, privacy, and qualification invariants
tests/render.test.js             Browser-free rendering checks
tests/browser/site.spec.js       Browser, accessibility, export, and mobile checks
tests/test_monitor.py            Source-monitor unit tests
.github/workflows/               Pages validation and source-audit automation
```
