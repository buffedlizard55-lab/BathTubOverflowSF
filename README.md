# Sunset Repair · BathTubOverflowSF

A static, source-linked research workspace for repair-first bathtub plumbing in San Francisco’s Outer Sunset.

**Target Pages URL:** https://buffedlizard55-lab.github.io/BathTubOverflowSF/

**Publication status:** implementation is on the session branch and available in the Arena live preview. The public site has not been updated: repository Pages is configured for `main`, and the integration returned HTTP 403 when asked to change Pages settings. No credentials were requested or changed.

## Research snapshot — September 10, 2026

- **50 distinct discovery records**, not 50 approved contractors.
- **11 direct CSLB record checks:** 10 active C-36 licenses and one expired listed license at check time.
- **13 short review excerpts** from accessible pages, indexed text and explicitly labeled company-hosted testimonials.
- **47 evidence references** with source URL, retrieval mode and checked date; repeated URLs have separate roles, not independent corroboration.
- **0 fully qualified master entries.** No exact seized-overflow, no-opening success case was established. No outcome or availability is guaranteed.

### Decision brief

The site offers an **editorial diagnostic-call order**, not a ranking of guaranteed workmanship:

1. **Fast Response Plumbing & Rooter:** adjacent internal bathtub-drain mechanism review plus a direct active C-36 check.
2. **Heise’s Plumbing:** explicit Outer Sunset coverage plus a direct active C-36 check.
3. **Genteel Plumbers:** explicit Outer Sunset coverage plus active C-36 and B classifications.

All factual support and caveats are in the business evidence files. Open the summary, directory or [`data/research.json`](data/research.json) for the exact sources. Ratings are never blended across platforms.

### Important irregularities

The dataset flags an expired listed license, a Thumbtack profile redirect between different legal entities, an indexed business scope excluding plumbing repairs, conflicting source dates/contact information and an expired website. Flags are dated observations—not allegations or proof that a business has closed.

## Features

- Decision summary at the top of the site
- Search, area / license / status filters, and intentionally separate qualified master
- Compare up to three businesses (memory only; no tracking)
- Claim-by-claim source links and short supporting excerpts
- Review provenance, dates, topic filters and conservative analysis
- Registry checks, irregularities and source register
- Source-linked CSV export, complete JSON download and printable brief
- Responsive, keyboard-accessible UI and native accessible dialogs
- No runtime dependencies, external fonts, analytics or embedded third-party content

## Evidence limits

This is **not a complete all-review aggregation**. Direct Yelp and Reddit retrieval was blocked on tested pages. Indexed extracts are explicitly labeled and may be stale. Google’s review panel did not load; company-republished Google excerpts are not labeled original Google reviews. Thumbtack exposes only a partial sample, and a historical profile redirect prevents safely assigning that old corpus to the former business.

Many of the 50 entries remain **directory-only leads**. Their current operation, exact service area, credentials and repair expertise are unverified. An active license is a regulatory fact, not a technical outcome guarantee. General drain cleaning, trenchless sewer work and faucet replacement do not establish experience extracting a seized overflow mechanism.

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

Tests cover unique entities, all citation references, license provenance, review assignment, evidence dates, private-field exclusions, master admission, safe CSV/HTML escaping, search/filter combinations, source-monitor barriers and parsing, comparison limits, exports, dialogs, navigation and mobile overflow.

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

The session branch is `arena/01a08d34-bathtuboverflowsf`. No changes are pushed to other branches. Initial repo review found only a one-line README and legacy Pages configured for `main`.

## Structure

```text
index.html, styles.css, app.js   Static UI
lib.js                          Pure filtering/export/admission rules
assets/mark.svg                  Original local vector mark
data/research.json              Curated, source-linked research snapshot
scripts/check_sources.py        Read-only monitoring and review quarantine
scripts/serve.py                Public-file-only development preview
tests/                         Dataset, monitor and browser tests
.github/workflows/              Validation, Pages and source-audit automation
```
