# Sunset Repair · BathTubOverflowSF

A static, source-linked research workspace for repair-first bathtub plumbing in San Francisco's Outer Sunset.

**Target Pages URL:** https://buffedlizard55-lab.github.io/BathTubOverflowSF/

**Publication status:** waves 1–7 are complete on the session branch and viewable in the Arena live preview. Repository Pages is configured to publish `main`, so the public site updates only when this branch is merged there — a pull request is opened for that purpose. The integration returned HTTP 403 when asked to change Pages settings in an earlier session, so no settings were changed and no credentials were requested.

## Research snapshot — September 10–11, 2026 (waves 1–7)

- **351 distinct discovery records**, not 351 approved contractors. Wave 1 = 50, Wave 2 = 50, Wave 3 = 51, Wave 4 = 50, Wave 5 = 50, Wave 6 = 50, Wave 7 = 50 (this session).
- **70 distinct direct CSLB record reads**: 31 across waves 1–2, 5 in wave 4, 23 in wave 6 and **12 in wave 7** — every one read live on `cslb.ca.gov`, with `Data current as of 9/11/2026`. Wave 7 produced **1 active C-36 recorded at a 94122 address, 1 inactive, 8 expired and 1 revoked** license; two of its reads were attached to pre-existing records instead of counted twice (`bill-callaway` #660638, and a corroborating re-read of `joe-watterson` #723992). Waves 3 and 5 remain otherwise discovery-level: their leads await CSLB checks (see `data/wave3-discovery-log.md` … `data/wave7-discovery-log.md`).
- **41 active licenses, 28 non-active** (expired, canceled, suspended, and — new in wave 7 — **inactive** and **revoked**), **36 records held or excluded**, and **14 records whose CSLB page itself records a 94122 Outer Sunset address** — the strongest area evidence in the dataset, because a regulator's address of record cannot be chosen by marketing.
- **Official SF DBI permit-firm registry** (data.sf.gov open dataset `k6kv-9kix`) queried by firm name and by Outer Sunset ZIPs (94122/94116) — an independent, government side channel. Wave 6 turned it into a discovery method in its own right: the 22 highest-permit-count 94122/94116 firms were each taken to CSLB, and the next 16 are stored as **registry-only** records with `license: null` and an explicit "not independently checked" flag. A permit-history row is never treated as a license status.
- **98 short review excerpts** with provenance labels (Yelp/Thumbtack/Reddit/Angi/Nextdoor indexed extracts, one Yellow Pages page review, six dated Thumbtack structured-data excerpts for wave 6, **20 read directly from Thumbtack pages in wave 7 plus 10 more from two Thumbtack pro profiles**, and explicitly labeled company-hosted testimonials, check-ins and portfolio captions). **4 excerpts are marked `negative`**, including one that removed a shortlisted contractor from the call order.
- **221 evidence references** with source URL, retrieval mode and checked date; repeated URLs have separate roles, not independent corroboration. All 25 new wave-7 references carry `access: "page"` — every one was retrieved and read this session, including **two documented negative results** (a State open-data catalogue query that returned no CSLB dataset, and CSLB's own POST-only area search whose results page returns HTTP 404 to a direct request).
- **Verified official permit rules.** `sf.gov/apply-plumbing-and-mechanical-permit` was read directly and stored in `data.compliance`, then rendered on the decision brief with its own citations — including the City's requirement that **pipes must be inspected before they are covered**. The exemption text (SF Plumbing Code §104.2) was **not** retrieved, and the site says so rather than paraphrasing it.
- **0 fully qualified master entries.** No exact seized-overflow, no-opening success case was established. No outcome or availability is guaranteed.
- **Thumbtack became directly readable this session** — category pages *and* individual pro profiles returned HTTP 200 — so for the first time the dataset holds **dated, attributed review text read from the publishing platform** rather than from a search index. That is what exposed a mis-attributed wave-6 review (corrected in place, with the displaced author's real review restored) and a directly-read negative review against a shortlisted contractor.

### Scope, permits & privacy

This repository is **public, source-linked research** for a repair-first bathtub-overflow
job in San Francisco's Outer Sunset. It is built to identify and verify **licensed,
credentialed** contractors from public records (CSLB, SF DBI) and to aggregate reviews with
provenance. It is deliberately **not** a concealed work order and does not recommend or rank
contractors for unpermitted or "discreet" work.

- **No private data.** No property address, occupant information, access instruction, or private
  project note is stored in this repository or its artifacts.
- **Permits & licensing are the owner's responsibility.** Any plumbing, drywall, ceiling or
  structural work in San Francisco — especially work affecting an occupied or in-law unit —
  should be performed by licensed contractors in line with San Francisco Department of Building
  Inspection (DBI) requirements. A license check verifies legal identity and status at a recorded
  date; it is **not** a guarantee of a specific repair outcome.
- **Reviews are not authenticated.** Excerpts are aggregated with platform/date labels and are not
  independently confirmed as genuine transactions. No complete all-review corpus is claimed.
- **Fail-closed.** Missing exact-task evidence, insurance, or written scope is recorded as a gap,
  never inferred. The qualified master list is empty by design.

### Decision brief

The site offers an **editorial diagnostic-call order**, not a ranking of guaranteed workmanship:

1. **Fast Response Plumbing & Rooter** — adjacent internal bathtub-drain mechanism review plus a direct active C-36 check.
2. **Heise's Plumbing** — explicit Outer Sunset coverage plus a direct active C-36 check.
3. **Genteel Plumbers** — explicit Outer Sunset coverage plus active C-36 and B classifications.
4. **O'Donovan Plumbing Inc** *(wave 2)* — active C36+C16 corporation whose license record shows a 94122 Outer Sunset business address, plus a long SF DBI permit history.
5. **Expert Plumbing Solutions** *(wave 2)* — active C36 corporation at 1465 44th Avenue (94122) with an indexed 4.8★/≈81 Yelp sample; license expires 10/31/2026, recheck before booking.

Waves 6 and 7 add a clearly-labelled **second tier**, admitted on a stricter basis than calls 01–05 — each holds an active license whose CSLB page *itself* records a 94122 Outer Sunset address, plus the classification its trade requires:

6. **Building Efficiency Inc** *(wave 6)* — active B / C20 / **C36** / C10 at 2037 Irving Street (94122), exp 05/31/2028; one of very few records that could legitimately hold both halves of this job.
7. **Faherty Plumbing and Heating** *(wave 6)* — active C36 at 4004 Irving Street (94122), exp 09/30/2028.
8. **De Barra Plumbing** *(wave 6)* — active C36 at 1511 39th Avenue (94122), exp 06/30/2028.
9. **Michael Kuenzli Plumbing Co** *(wave 7)* — active **C36** sole ownership at 1234 21 Avenue (94122), issued **09/06/1989**, exp 09/30/2027, bond $25,000 effective 08/22/2025 with no cancellation, and 66 plumbing-permit rows at the same address in the City's own registry. Admitted **without** a review, a website or a seized-overflow case — long tenure on older SF housing is plausible, not proven, and the record says so.

**Removed from the call order in wave 7:** *Caledonia Plastering & Stucco Inc* held call 06 in wave 6 on an active **C35** licence at 1551 Judah Street (94122). Its Thumbtack profile, read directly, published a negative review alleging **refused corrections**, a **bathroom exhaust covered with plaster** and a request for cash payment; the platform also answered "Sorry this pro can't do your job" for a plastering enquiry in the profile's own stated ZIP **94116**, showed no review later than 2018, ended its Top Pro badges at 2020 and listed no drywall service. The record is **held**, its licence read is unchanged, and calls 06–09 were renumbered. A 4.9★ rating across 56 reviews is not treated as cancelling out a specific, directly-read allegation about corrections refused in a bathroom.

All factual support and caveats are in the business evidence files. Open the summary, directory or [`data/research.json`](data/research.json) for the exact sources. Ratings are never blended across platforms.

### Important irregularities

- **Mr. Rooter of San Francisco:** franchise site advertises 266 reviews at 4.8/5, but the local franchisee's C36 (SDP Plumbing Inc, #1016070) **expired 07/31/2024** per direct CSLB check. A brand site is not a license.
- **Master Rooter Plumbing (1208 38th Ave):** BBB lists it as *believed out of business*; Yelp sample is 1.6★/26 unclaimed; the SF registry links license 448788 to Metro Rooter/Simovich Plumbing at 1526 Irving St. A separate, unrelated active "Master Rooter & Plumbing Inc" (1044408) exists — identity confusion risk.
- **5 Star Plumbing & Rooter:** CSLB notes license 996627 was **reissued to another entity on 11/17/2025**; the registry also shows similarly named firms. Confirm the exact legal entity.
- **Expired neighborhood licenses (all direct CSLB reads):** Di Maggio Plumbing (2023), A Aero (2023), Gantley (1996), K.C. Plumbing (2018), Jeff Tom (2001), Sunset Plumbing (2024, previously inactivated), Purcell Bros → record now reads Rodney Conklin (2014, El Dorado Hills), Scott Fisher → record reads Scott's Plumbing (2012). Several long-established Outer Sunset shops cannot be booked as-is.
- **Repipe Champions (wave 4):** the "CSLB #1057927" printed on its marketing page resolves — by direct CSLB read — to **Ortega's Bay Area General Construction Inc of Hayward, an active B (General Building) license**, not a C-36 plumbing license and not the marketing name. Held with a booking/scope hold flag.
- **AB Plumbing (wave-4 license attach):** CSLB #876212 is active, but the record's address is **Oakland** (12909 Skyline Blvd) against SF-focused marketing, the contractor's bond shows a **cancellation date of 10/03/2026**, and the license carries a no-employees workers-comp exemption. Verify current base and bond before relying on the historic review sample.
- **24-7 Rooter & Plumbing:** active C-36 (#954813) but the license **expires 11/30/2026** — recheck before booking.
- **Wave-4 identity cautions:** True-Tech Water and Plumbing appears as a promoted result on an Outer Sunset page while its own profile is San-Jose based; "Discount Plumbing San Francisco / Rooter Services" naming variants likely overlap the existing Discount Plumbing Rooter entry (not double-counted); a SAFENEST Restoration listing excerpt praises Mike's Water Damage (index text bleed); Marco's Plumbing vs Thumbtack's "Marco's Plumbing and Cleaning" and Plumbing Bay Area vs Bay Area Plumbing are near-name pairs kept deliberately separate.
- **Two licenses suspended on one bond date (wave 6):** All-Point Solutions Plumbing Co (#950265, CSLB address 1651 42nd Ave, 94122) and F C Company (#1022789) both read "License is under Contractors Bond Suspension", and both show a contractor's bond with Hudson Insurance Company carrying a cancellation date of **09/01/2026**. A suspended license cannot lawfully contract. The shared date and surety suggest a surety-wide event rather than two unrelated failures.
- **A second lapsed C-36 behind the Mr. Rooter brand (wave 6):** B R Troika Inc. dba Mr Rooter Plumbing (#812845) at 2341 Judah, 94122 **expired 09/30/2018** and reads "not able to contract" — alongside SDP Plumbing Inc (#1016070, expired 07/31/2024). The registry records two spellings and two Judah Street numbers for the same firm.
- **Right address, wrong classification (wave 6):** Gorman Pipeline Inc (#898289) is active at 1518 27th Ave, 94122 but holds **A (General Engineering) only** — no C-36 — and is recorded as a scope exclusion. R S Dynamic Builders (#1130530) is active but **B only**, issued 12/16/2024, with no covered employees; its own JSON-LD gives `streetAddress: "123 Main Street"` against CSLB's 909 Ocean View Ave and a 415 phone against CSLB's 650 number.
- **Registry history ≠ present operation (wave 6):** West Cork Plumbing (Novato), Flow Masters Plumbing (Daly City) and Moonlight Plumbing (Yucca Valley, license expiring **09/30/2026**) each hold 94122 permit histories with non-SF current addresses.
- **Rejected rather than attached (wave 6):** an indexed excerpt praising "Singh" appeared on the Jose HandyMan Services listing — the same index-text-bleed pattern as wave 4 — so it was rejected; SR Water Mitigation was rejected as restoration scope; Yelp's "Verified License" badges for All About Plastering, Gray Lath and Plaster and Marcelino Plastering are platform badges, not CSLB reads, and all three are stored with `license: null`.
- **Two new non-active CSLB statuses (wave 7):** `inactive` — Ehrich's Plumbing (#661818) at 1607 31st Avenue, 94122, C36, whose expiry date 12/31/2026 is still in the future while the status reads "not able to contract" — and `revoked` — MidMarket Development Company Inc (#734011), B-only, with **complaint disclosure information** on file and a 01/15/2008 reissue to another entity, against a registry row naming "Killarney Construction" at 1291-11th Ave 94122. A future expiry date on an inactive license is a trap a status-only check would miss.
- **A bond dated after the license expired (wave 7):** Alpine Construction (#716856) at 1032 Irving Street 94122 holds **A (General Engineering) only**, expired 12/31/2021, yet shows a contractor's bond effective **01/01/2023** — cancelled 04/28/2023.
- **Multi-name license histories (wave 7):** the registry re-query grouped by license *and* ZIP showed four licenses whose registry firm names differ from the CSLB licensee. License 723992 (active C36) appears as both "Joe Watterson Plumbing" and "Slemish Plumbing" across **four ZIPs** (94134, 94116, 94110, 94996) with **no 94122 row at all**; 609942 reads "Drop Stop Plumbing Service" in the registry against CSLB's Grant Plumbing & Construction in **San Leandro**, expired 2007; 660638 splits 170 permit rows at 94121 and 7 at 94122; 708086 has rows at both 94121 and 94122 against a 94121 CSLB address.
- **Out-of-state and out-of-category profile paths inside San Francisco results (wave 7):** "Figs Drywall Repair" is published on Thumbtack's SF drywall-repair page with a profile path of **`/id/boise/`** (Idaho), and "Walty Handy Service Pro" with **`/ca/san-pablo/moving-companies/`** (Contra Costa County, moving category). Both are flagged and labelled outside-area. A category page's inclusion of a pro is not evidence the pro serves that city.
- **An unlicensed-work allegation that official records could neither confirm nor refute (wave 7):** Elite Solution Will Team is held on a directly-read review alleging work "without a proper license", **no moisture testing** on water-damaged material, a "cosmetic cover-up" over unprepped surfaces and a refusal to return — but no CSLB number is published on the profile, so nothing was read on CSLB and the allegation stays an allegation.
- **A confirmed review mis-attribution in the existing dataset (wave 7):** wave 6's review R60 was stored as "Tom S.", "Jun 2, 2018" carrying the quote "Quick to respond, fair price … John took care of the hole in the ceiling …". The profile read directly shows that quote under **Vipada W., Oct 5, 2017**, and Tom S.'s Jun 2, 2018 review as a different text about exterior stucco. R60 was corrected in place and Tom S.'s real review restored as R98 — the wave-4 / wave-6 index-text-bleed pattern, now confirmed rather than suspected.
- **Platform credential dates that predate the read by years (wave 7):** New Age Drywall Inc shows "License type: C9 – Drywall / License verified on **10/29/2020**" and **no CSLB number anywhere in the page**, so `license` stays `null` despite a 4.9★/237 sample, 455 hires and current Top Pro status. A platform badge is not a regulator read.
- Plus wave-1 findings: expired Plumbing Pure license, Thumbtack profile redirect between legal entities, Precision Rooter scope mismatch, conflicting dates and an expired website. Flags are dated observations — not allegations or proof that a business has closed.

## Features

- Decision summary at the top of the site (nine-entry call order in two clearly-labelled tiers)
- **Official permit & inspection panel** sourced from sf.gov, with the exemption section flagged as not retrieved rather than paraphrased
- **Verification ladder** on the audit page: every record is placed on exactly one evidence level (regulator read / official registry / directory & marketing) with counts and what each level can and cannot prove
- **Trade labels and classification checks** — each record declares a trade, and a license is only accepted where its CSLB classification actually covers that trade
- Search, area / license / status filters, and intentionally separate qualified master
- Compare up to three businesses (memory only; no tracking)
- Claim-by-claim source links and short supporting excerpts
- Review provenance, dates, topic filters and conservative analysis
- Registry checks, irregularities and source register
- Source-linked CSV export, complete JSON download and printable brief
- Responsive, keyboard-accessible UI and native accessible dialogs
- No runtime dependencies, external fonts, analytics or embedded third-party content

## Evidence limits

This is **not a complete all-review aggregation**. Direct Yelp and Reddit retrieval was blocked on tested pages. Indexed extracts are explicitly labeled and may be stale. Google's review panel did not load; company-republished Google excerpts are not labeled original Google reviews. Thumbtack exposes only a partial sample: wave 7 read its San Francisco drywall category pages and two pro profiles directly, but a category page shows a handful of featured reviews per pro, not the full corpus, and the earlier Sunset category page was read through a 2020 index. A historical profile redirect prevents safely assigning that old corpus to the former business.

The official SF DBI plumbing-permit registry contains **plumbing-permit contacts only**, so no drywall, plaster or handyman firm can be discovered through it; the finish trades came from indexed directories and company sites, which is weaker evidence and is labelled as such on the verification ladder. Third-party license numbers (BuildZoom, BBB, company footers) are treated as leads and re-read on CSLB: in wave 6 all three corroborated #1057063, while wave 4's Repipe Champions number resolved to a different entity entirely.

Many entries remain **directory- or registry-only leads**. Their current operation, exact service area, credentials and repair expertise are unverified. SF DBI registry rows are historical permit records without in-dataset dates: they prove a recorded address and license linkage, never present operation. An active license is a regulatory fact, not a technical outcome guarantee. General drain cleaning, trenchless sewer work and faucet replacement do not establish experience extracting a seized overflow mechanism.

The master admission rule is fail-closed: entity / active C-36, exact area, relevant task evidence, applicable insurance, written scope and no blocking identity/license flag. Missing information is not inferred. Reviews remain unverified customer accounts.

No businesses have been contacted and no appointments booked. **Do not add property addresses, occupant details or private project notes to this public repository or its artifacts.**

## Run locally

Python 3.11+ and Node 22 are used for development. The site itself needs only a static HTTP server. The included preview server exposes an explicit public-file allowlist, not repository internals.

```sh
npm start
# http://localhost:4173 — server binds to 0.0.0.0 for remote previews
```

All browser-facing URLs are relative. The site works at the GitHub project path `/BathTubOverflowSF/`. Hash routes do not need server rewrites.

## Tests

```sh
npm ci
npm test
npm run test:monitor
npx playwright install --with-deps chromium
npm run test:browser
```

For an already-installed compatible Chromium, set `CHROMIUM_PATH` to its executable. The sandbox browser smoke tests used a separately obtained headless Chromium binary because the standard Playwright browser CDN was inaccessible; no browser binaries are committed.

`npm test` runs **24 assertions** in two files. `tests/research.test.js` covers unique entities (351 across seven waves), all citation references, license provenance, review assignment, evidence dates, private-field exclusions, master admission, safe CSV/HTML escaping, search/filter combinations, wave-6 composition, **wave-7 composition (10 CSLB reads + 20 registry-only + 20 Thumbtack, kept separable)**, **the wave-7 follow-up attaches (including the call-order renumbering and the corrected review attribution)**, the rule that a non-active license must always be held, the classification-versus-trade audit, and the official permit citations. `tests/render.test.js` exercises the real UI templates against a hand-rolled DOM stub (no jsdom dependency) so every route is checked for `undefined`, `NaN`, `[object Object]` and unresolved citations **without a browser**.

Browser specs additionally cover source-monitor barriers and parsing, comparison limits, exports, dialogs, navigation and mobile overflow. Row, card, ladder and shortlist counts all derive from the dataset, so a wave can never silently desync the UI.

## Wave files and merging

`data/wave2.json` is the raw second-pass research record (50 businesses, 43 sources, 16 reviews, all line-checked). `scripts/merge_wave.py` merges a wave file into `data/research.json` and refuses to run if any structural invariant would break. `data/wave2-discovery-log.md` keeps the discovery trail, including rejected candidates and why.

`data/wave3.json` / `scripts/gen_wave3.py` is the raw third-pass record (51 businesses, 10 sources, 10 reviews, all line-checked). `data/wave3-discovery-log.md` documents wave-3 sources, categories and the license spot-checks performed this session.

`data/wave4.json` / `scripts/gen_wave4.py` is the raw fourth-pass record (50 businesses, 40 sources, 19 reviews, all line-checked). `scripts/patch_wave4_licenses.py` runs after the merge to attach wave-4's direct CSLB reads to three pre-existing entries and two task-relevant site reads; it mirrors the merge's fail-closed invariants. `data/wave4-discovery-log.md` documents wave-4 sources, categories, the five license reads with outcomes, and every rejected candidate with reasons.

`data/wave5.json` / `scripts/gen_wave5.py` is the raw fifth-pass record (50 businesses: 15 plumbing-adjacent, 32 drywall/finish, 3 multi-trade) and `data/wave5-discovery-log.md` documents its indexed sources and limitations.

`data/wave6.json` / `scripts/gen_wave6.py` is the raw sixth-pass record (**50 businesses, 47 sources, 6 reviews**). Wave 6 is a credential pass rather than a discovery pass: 22 records carry a direct CSLB read, 16 are official-registry-only with `license: null`, and 12 are indexed finish-trade leads. `scripts/merge_wave6.py` performs a **trade-aware, fail-closed** merge (idempotent — it refuses to re-merge a wave already present) and writes the `compliance` block, `researchDates` and methodology counters. `scripts/patch_wave6_attaches.py` then attaches three direct CSLB reads to pre-existing entries. `data/wave6-discovery-log.md` documents all 23 CSLB reads, the registry queries, entity-resolution decisions, every rejection and every irregularity.

`data/wave7.json` / `scripts/gen_wave7.py` is the raw seventh-pass record (**50 businesses, 21 sources, 20 reviews**). Wave 7 is a **channel pass**: 10 records carry a direct CSLB read, 20 are official-registry-only with `license: null`, and 20 are Thumbtack listings read directly — and the three channels are asserted separately so a single count cannot flatter the wave. `scripts/merge_wave7.py` performs a fail-closed, idempotent merge that additionally runs a **name-and-license collision gate against all 301 pre-existing records** (this is what caught "Joe Watterson Plumbing" and turned it into a re-read attach rather than a duplicate row), accepts the two new non-active statuses `inactive` and `revoked`, and refuses any CSLB source that is not a `LicenseDetail.aspx?LicNum=` page unless its note records what the page actually returned. `scripts/patch_wave7_attaches.py` then applies four further direct reads (two Thumbtack pro profiles, two grouped registry re-queries) to **seven pre-existing records**, corrects one mis-attributed review in place, removes a shortlisted record from the call order and renumbers the rest. `data/wave7-discovery-log.md` documents all 12 CSLB reads, both documented negative results, every rejection, and every irregularity.

`scripts/merge_wave.py` (waves 1–5) cannot ingest wave 6 or 7: it hardcodes C36 as the only acceptable classification, and those waves legitimately introduce C-9, C35, B-only and A-only licenses plus `inactive` and `revoked` statuses.

## Read-only source monitoring

```sh
npm run audit:sources
# Optional bounded smoke test:
python3 scripts/check_sources.py --limit 3
```

The standard-library monitor groups duplicate URLs, checks robots policy, rate-limits each host, validates public network targets, inspects redirects, looks for retained excerpts and extracts short JSON-LD review candidates into a **quarantined artifact**. It never promotes businesses, submits contact forms, bypasses access controls or overwrites the reviewed dataset. A successful HTTP response is not semantic verification.

Output is `reports/source-audit.json` and `reports/source-audit.md` (ignored by Git). Missing quotes are flagged as changed/partial evidence, not as false statements. Credentials, cookies and full copyrighted review corpora are not stored.

**Initial sandbox monitor result:** 45 unique registered URLs attempted; 44 skipped because robots policy could not be established, one DNS failure, and zero pages retrieved. This is separate from the curated web-research tool checks recorded in the dataset. It demonstrates fail-closed behavior, not successful automated re-verification. GitHub runners may have different access; consult their actual audit artifact.

The `Public source audit` workflow runs on relevant pushes and supports dispatch. It also contains a weekly Monday schedule. **GitHub schedules run only from the default branch**, so the weekly trigger is not active while this workflow exists only on the session branch. Push-triggered audits work immediately. Artifacts expire after 30 days; no branch is automatically modified and no approved data is silently replaced.

## GitHub Pages

`Test and deploy Pages` validates the dataset and UI, stages only `index.html`, `styles.css`, `app.js`, `lib.js`, `assets/mark.svg` and `data/research.json`, then optionally deploys through GitHub Pages Actions on `main` when the repository uses the Actions build type. The current legacy Pages configuration publishes the repository root from `main` independently after the changes are merged. The workflow deliberately skips deployment on the session branch rather than failing against the known branch restriction. If repository integration permissions prevent changing those settings, the workflow and local live preview still work but the public deployment is not complete.

The session branch is `arena/01a092e2-bathtuboverflowsf`. No changes are pushed to other branches.

## Structure

```text
index.html, styles.css, app.js   Static UI
lib.js                          Pure filtering/export/admission rules
assets/mark.svg                  Original local vector mark
data/research.json              Merged, source-linked dataset (waves 1–7, schema v2)
data/wave2.json                 Raw wave-2 research record
data/wave2-discovery-log.md     Discovery trail incl. rejected candidates
data/wave3.json                 Raw wave-3 research record
data/wave3-discovery-log.md     Wave-3 sources, categories, spot-checks
data/wave4.json                 Raw wave-4 research record (50 new entries)
data/wave4-discovery-log.md     Wave-4 sources, CSLB read outcomes, rejected candidates
data/wave5.json                 Raw wave-5 research record (50 new entries)
data/wave5-discovery-log.md     Wave-5 sources, limitations and irregularities
data/wave6.json                 Raw wave-6 credential pass (50 new entries, 22 CSLB reads)
data/wave6-discovery-log.md     All 23 CSLB reads, registry queries, rejections, irregularities
data/wave7.json                 Raw wave-7 channel pass (50 new entries, 12 CSLB reads)
data/wave7-discovery-log.md     All 12 CSLB reads, negative results, attaches, rejections
scripts/gen_wave5.py            Reproducible wave-5 dataset builder
scripts/gen_wave6.py            Reproducible wave-6 dataset builder
scripts/merge_wave6.py          Trade-aware fail-closed merge (waves with non-C36 classes)
scripts/patch_wave6_attaches.py Wave-6 CSLB attaches for pre-existing entries
scripts/gen_wave7.py            Reproducible wave-7 dataset builder
scripts/merge_wave7.py          Collision-gated fail-closed merge (adds inactive/revoked)
scripts/patch_wave7_attaches.py Wave-7 attaches, review correction, call-order renumber
scripts/merge_wave.py           Fail-closed wave merge
scripts/gen_wave4.py            Reproducible wave-4 dataset builder
scripts/patch_wave4_licenses.py Wave-4 CSLB attaches for pre-existing entries
scripts/check_sources.py        Read-only monitoring and review quarantine
scripts/serve.py                Public-file-only development preview
tests/research.test.js          15 dataset invariants (line-by-line citation & license checks)
tests/render.test.js            9 browser-free UI render assertions (no jsdom dependency)
tests/                          Monitor tests and Playwright browser specs
.github/workflows/              Validation, Pages and source-audit automation
```
