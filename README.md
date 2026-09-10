# Sunset Repair · BathTubOverflowSF

A static, source-linked research workspace for repair-first bathtub plumbing in San Francisco's Outer Sunset.

**Target Pages URL:** https://buffedlizard55-lab.github.io/BathTubOverflowSF/

**Publication status:** implementation is on the session branch and available in the Arena live preview. The public site has not been updated: repository Pages is configured for `main`, and the integration returned HTTP 403 when asked to change Pages settings. No credentials were requested or changed.

## Research snapshot — September 10, 2026 (waves 1 + 2)

- **100 distinct discovery records**, not 100 approved contractors. Wave 2 added exactly 50 new entries on top of wave 1's 50.
- **31 direct CSLB record checks** across both waves; wave 2 alone contributed 20 direct license page reads (11 active C-36, 9 expired).
- **Official SF DBI permit-firm registry** (data.sf.gov open dataset `k6kv-9kix`) queried by firm name and by Outer Sunset ZIPs (94122/94116) — an independent, government side channel that confirmed license numbers, recorded business addresses and permit-linked phone numbers for wave-2 entries.
- **29 short review excerpts** with provenance labels (Yelp/Thumbtack/Reddit/Angi/Nextdoor indexed extracts, one Yellow Pages page review, and explicitly labeled company-hosted testimonials).
- **90 evidence references** with source URL, retrieval mode and checked date; repeated URLs have separate roles, not independent corroboration.
- **0 fully qualified master entries.** No exact seized-overflow, no-opening success case was established. No outcome or availability is guaranteed.

### Decision brief

The site offers an **editorial diagnostic-call order**, not a ranking of guaranteed workmanship:

1. **Fast Response Plumbing & Rooter** — adjacent internal bathtub-drain mechanism review plus a direct active C-36 check.
2. **Heise's Plumbing** — explicit Outer Sunset coverage plus a direct active C-36 check.
3. **Genteel Plumbers** — explicit Outer Sunset coverage plus active C-36 and B classifications.
4. **O'Donovan Plumbing Inc** *(wave 2)* — active C36+C16 corporation whose license record shows a 94122 Outer Sunset business address, plus a long SF DBI permit history.
5. **Expert Plumbing Solutions** *(wave 2)* — active C36 corporation at 1465 44th Avenue (94122) with an indexed 4.8★/≈81 Yelp sample; license expires 10/31/2026, recheck before booking.

All factual support and caveats are in the business evidence files. Open the summary, directory or [`data/research.json`](data/research.json) for the exact sources. Ratings are never blended across platforms.

### Important irregularities

- **Mr. Rooter of San Francisco:** franchise site advertises 266 reviews at 4.8/5, but the local franchisee's C36 (SDP Plumbing Inc, #1016070) **expired 07/31/2024** per direct CSLB check. A brand site is not a license.
- **Master Rooter Plumbing (1208 38th Ave):** BBB lists it as *believed out of business*; Yelp sample is 1.6★/26 unclaimed; the SF registry links license 448788 to Metro Rooter/Simovich Plumbing at 1526 Irving St. A separate, unrelated active "Master Rooter & Plumbing Inc" (1044408) exists — identity confusion risk.
- **5 Star Plumbing & Rooter:** CSLB notes license 996627 was **reissued to another entity on 11/17/2025**; the registry also shows similarly named firms. Confirm the exact legal entity.
- **Expired neighborhood licenses (all direct CSLB reads):** Di Maggio Plumbing (2023), A Aero (2023), Gantley (1996), K.C. Plumbing (2018), Jeff Tom (2001), Sunset Plumbing (2024, previously inactivated), Purcell Bros → record now reads Rodney Conklin (2014, El Dorado Hills), Scott Fisher → record reads Scott's Plumbing (2012). Several long-established Outer Sunset shops cannot be booked as-is.
- Plus wave-1 findings: expired Plumbing Pure license, Thumbtack profile redirect between legal entities, Precision Rooter scope mismatch, conflicting dates and an expired website. Flags are dated observations — not allegations or proof that a business has closed.

## Features

- Decision summary at the top of the site (five-entry call order)
- Search, area / license / status filters, and intentionally separate qualified master
- Compare up to three businesses (memory only; no tracking)
- Claim-by-claim source links and short supporting excerpts
- Review provenance, dates, topic filters and conservative analysis
- Registry checks, irregularities and source register
- Source-linked CSV export, complete JSON download and printable brief
- Responsive, keyboard-accessible UI and native accessible dialogs
- No runtime dependencies, external fonts, analytics or embedded third-party content

## Evidence limits

This is **not a complete all-review aggregation**. Direct Yelp and Reddit retrieval was blocked on tested pages. Indexed extracts are explicitly labeled and may be stale. Google's review panel did not load; company-republished Google excerpts are not labeled original Google reviews. Thumbtack exposes only a partial sample (and its Sunset category page was read through a 2020 index). A historical profile redirect prevents safely assigning that old corpus to the former business.

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

Tests cover unique entities (100 across two waves), all citation references, license provenance, review assignment, evidence dates, private-field exclusions, master admission, safe CSV/HTML escaping, search/filter combinations, source-monitor barriers and parsing, comparison limits, exports, dialogs, navigation and mobile overflow.

## Wave files and merging

`data/wave2.json` is the raw second-pass research record (50 businesses, 43 sources, 16 reviews, all line-checked). `scripts/merge_wave.py` merges a wave file into `data/research.json` and refuses to run if any structural invariant would break. `data/wave2-discovery-log.md` keeps the discovery trail, including rejected candidates and why.

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

The session branch is `arena/01a08d45-bathtuboverflowsf`. No changes are pushed to other branches.

## Structure

```text
index.html, styles.css, app.js   Static UI
lib.js                          Pure filtering/export/admission rules
assets/mark.svg                  Original local vector mark
data/research.json              Merged, source-linked dataset (waves 1 + 2, schema v2)
data/wave2.json                 Raw wave-2 research record
data/wave2-discovery-log.md     Discovery trail incl. rejected candidates
scripts/merge_wave.py           Fail-closed wave merge
scripts/check_sources.py        Read-only monitoring and review quarantine
scripts/serve.py                Public-file-only development preview
tests/                         Dataset, monitor and browser tests
.github/workflows/              Validation, Pages and source-audit automation
```
