# Next-session handover

Updated 2026-09-17 (after wave 18). This replaces the wave-17 next-session instructions;
historical wave evidence remains in `data/` and the README.

## Current state

- Existing corpus: **793 records, 673 sources, 172 retained review excerpts** — unchanged.
- Wave-17 queue: **50 leads**, 4 CSLB reads, separate from the corpus.
- Wave-18 queue (this session): **50 leads** — 43 City registry records (each pair confirmed
  in two City queries) with **12 direct CSLB reads** (2 active, 2 suspended, 2 inactive,
  6 expired), plus 7 platform/community listings; **6 retained excerpts** (5 reviews, 1
  business self-description); 1 fold into the stored Repipe Specialists record.
- **Zero qualified master entries across everything.** Do not describe the combined records
  as verified businesses. Both plumbing and drywall remain unconfirmed for every wave-17 and
  wave-18 lead.

## Highest-value next work — depth, not another generic 50

1. **Prove both services on the existing shortlist.** Use the corpus diagnostic shortlist as
   the plumbing track and the drywall/plastering candidates as the restoration track. Obtain
   firm-specific public evidence for small repair work, ceiling restoration and access-hatch
   installation. Keep a coordinated two-business option distinct from a single-business
   option. Neither a name nor a B classification demonstrates either service for this project.
2. **Follow the two most relevant wave-18 licence facts.** Westside Plastering (750209, C35)
   is under Contractors Bond Suspension with the bond cancelled 2026-09-01 — check whether the
   suspension is lifted retroactively if a new bond was filed. A Atlantiac Plastering Inc
   (830655, C35) is inactive but its expiry date is 2028 — a reactivation check is cheaper
   than new discovery. Resolve the E-Construction / AAA Construction name question (819519,
   B+C36, suspended) before spending any further effort on it.
3. **Resolve current identity and service area for registry leads.** Read current CSLB details
   for the 31 unread wave-18 registry numbers and the 46 unread wave-17 numbers before treating
   any of them as contractors. ZIP 94122 in the City queries is the **firm contact ZIP**, not a
   project ZIP and not proof of Outer Sunset dispatch. Deprioritize unrelated trades.
4. **Review attribution before aggregation.** Find original business profiles on Yelp, Thumbtack
   and Google; retain permitted excerpts with author, date when visible, profile identity, URL,
   read date and access mode. Wave 18 showed how thin platform evidence is: most Thumbtack
   drywall/plastering/ceiling pros and Reddit-named plumbers were already stored. New review
   value now mostly sits on already-stored businesses. Keep platform ratings separate; do not
   average incompatible or duplicated corpora.
5. **Exact-task outcome.** Seek accounts of a seized bathtub-overflow mechanism being freed
   without pipe replacement, and note unsuccessful attempts or necessary replacement. The
   wave-18 Repipe Specialists fold documents the destructive-access path with full restoration;
   the repair-first path still has no attributable public outcome. Avoid guaranteeing a
   non-destructive result.
6. **Resolve the standing flags.** Ho Pronamic's observed bond suspension; Doc Painting's
   differing addresses and complaint-disclosure link; Gee Construction's multiple registry
   numbers; Doc and Tadashi name aliases; now also the wave-18 name questions (Ron Chan /
   YONG RONG CHEN, Carpentech / YU OUYANG, Winner Remodel / BAK REMODEL, Morris Home's
   historical disciplinary bond). A displayed complaint or bond line is not an adjudication.
7. **Obtain project-specific confirmation only with outreach authorization.** Insurance,
   availability, actual dispatch, the assigned technician, subcontractor coordination and a
   written repair-first scope are not established here. No messages or forms were sent. Keep
   the master empty until the relevant evidence and scope requirements are satisfied.
8. **Check applicable City requirements before work.** General research is not a site
   assessment, permit determination, hazardous-material assessment or guarantee of safe
   access. Use the existing official-source compliance panel and qualified professionals.

## Access and verification limitations

- Shell HTTPS retrieval fails in this sandbox; the page-reader tool succeeds. Evidence is a
  field transcription, not a raw-byte download.
- Yelp business pages remain blocked; all Yelp evidence is search-extract and marked as such
  on every record. Reddit pages returned HTTP 403 this session; thread evidence is
  search-extract only. No claim is made to have read all reviews of any business.
- Thumbtack category pages change between sessions; wave 18's displayed ratings and hire
  counts are dated 2026-09-17.
- Tests check consistency, source references, escaping, privacy markers and conservative
  gates. They cannot independently prove source truth or review authenticity. The three
  passes per wave are audits by one agent, not three independent reviewers.
- The existing privacy digest test is a regression safeguard, not a comprehensive privacy
  scanner. Review all new public artifacts before publishing. Keep nonpublic context out of
  data, logs, issue text, commit messages, pull requests and outreach.

## Reproducible validation

```sh
npm ci
npm test
npm run test:monitor
npx playwright install --with-deps chromium
npm run test:browser
npm start
```

Local unit and monitor tests passed for wave 18. Local Chromium was not installed in this
session; use the GitHub Actions browser result as the deployment gate. `CHROMIUM_PATH` can
select an already installed browser. The preview binds to `0.0.0.0:4173` and serves only
allowlisted files (`scripts/serve.py` — add new public files to its allowlist if serving
locally fails for them).

Future corpus edits must deliberately update the wave-17 baseline guard after an audited
merge, not remove it just to make a test pass. Wave 18 adds its own baseline guard
(`tests/discovery18.test.js`) computed over the same unchanged `data/research.json`.

## Pages configuration limitation

The existing Pages site is public and uses legacy publication from `main` at `/`. The API
refused changing it to Actions publication with HTTP 403 (integration permission limit), so
that setting was left unchanged. The workflow stages an explicit public-file allowlist for a
future Actions deployment and now includes `discovery18.html`, `discovery18.js` and
`data/wave18.json`, but **legacy publication does not use that allowlist**. Treat every
tracked file as public. An authorized repository administrator can select GitHub Actions as
the Pages source later; no credential should be stored in this project. Once this wave is
merged to `main`, legacy Pages republishes it automatically.
