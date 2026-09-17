# Next-session handover

Updated 2026-09-17 (after wave 19). This replaces the wave-18 next-session
instructions; historical wave evidence remains in `data/` and the README.

## Current state

- Existing corpus: **793 records, 673 sources, 172 retained review excerpts** — unchanged.
- Wave-17 queue: **50 leads**, 4 CSLB reads, separate from the corpus.
- Wave-18 queue: **50 leads** — 43 City registry records with 12 direct CSLB reads, plus
  7 platform listings; 6 retained excerpts; 1 fold.
- Wave-19 queue (this session): **50 leads** — 43 City registry records (each name/number
  pair confirmed in two City queries) with **16 direct CSLB reads** (14 active, 1 suspended,
  1 inactive), plus 7 Thumbtack platform listings; **7 retained excerpts** (6 customer
  reviews, 1 business self-description); 2 folds (Caledonia Plastering & Stucco into the
  stored wave-6 record with new plaster-ceiling review excerpts; D.C.K. Construction 553166
  into w19-531666 as an unreconciled second number).
- **Zero qualified master entries across everything.** Do not describe the combined records
  as verified businesses. Both plumbing and drywall remain unconfirmed for every wave-17,
  wave-18 and wave-19 lead.

## Highest-value next work — depth, not another generic 50

1. **Follow the three wave-19 multi-trade licence reads.** Detail Drywall & Stucco Inc
   (1032948, active B + C36 + C-9 + C35, Hayward address, 415 phone) is the second
   both-trades-on-one-licence record in the corpus and carries a completed 94122
   lath-and-stucco permit — it is the wave's lead candidate. Burton's Construction (937080,
   active B + C36 + C54, 137 Palm Avenue #4, SF 94118) and Kwan Chok Kee (1087358, active
   B + C36 + C10 + C16, 1460 Monterey Blvd, SF 94127) are the other two. For each, the next
   evidence is the two trade-confirmation questions (plumbing plus drywall/ceiling work for
   Outer Sunset), Outer Sunset dispatch, project insurance and a written repair-first scope.
   All three remain held until then.
2. **CSLB-read the 27 new wave-19 registry-only numbers** before treating any of them as
   contractors. Prioritize plumbing-named firms (Tom Mc Donald 466126, Harold Teitler
   555978, Lynda Cence 543983, Wing's General 565779, Kong Lai 579830, N & T 580391, Jimmy
   Tam 588779, Edison C. Cayabyab 501000) over electrical/concrete-named rows. Note the
   open identity questions: Dck Construction carries 531666 in one read and the name
   appears under 553166 in another (folded, unresolved); Smart Remodeling And Design Inc
   (580756) also appears as Rhino Builders Inc; Stephen Donnelly (573143) also appears as
   House To Home Remodeling; C & J Construction (568057) also appears as Cbj Design / Kar
   Tung See.
3. **Continue the standing licence rechecks from the earlier handovers.** Westside
   Plastering (750209, C35) bond suspension lifted-or-not check (bond cancellation
   2026-09-01); A Atlantiac Plastering Inc (830655, C35) reactivation check (cheapest read
   on the list); E-Construction / AAA Construction name question (819519, B+C36,
   suspended). Reborn Bath Solutions (443682) is suspended under four reasons with a
   complaint-disclosure link — re-read status before any contact and do not contact while
   suspended; read the disclosure only to note existence, not to publish details. Alansi's
   Rooter & Plumbing (933593) is inactive pending workers-comp; its 94122 drain-stack
   permit (PP20250514222) is the wave's closest in-wall plumbing permit, so a reactivation
   check is worth one read.
4. **Finish the standing unread registry lists** — 31 unread wave-18 registry numbers and
   46 unread wave-17 numbers — before treating any of them as contractors. ZIP 94122 in the
   City queries is the **firm contact ZIP**, not a project ZIP and not proof of Outer Sunset
   dispatch. Deprioritize unrelated trades.
5. **Review attribution before aggregation.** Find original business profiles on Yelp,
   Thumbtack and Google; retain permitted excerpts with author, date when visible, profile
   identity, URL, read date and access mode. Waves 18 and 19 both showed how thin platform
   evidence is: nearly every Thumbtack drywall/plastering/ceiling pro and every Yelp or
   Reddit-named business displayed this session was already stored. New review value now
   mostly sits on already-stored businesses. Keep platform ratings separate; do not average
   incompatible or duplicated corpora.
6. **Exact-task outcome.** Seek accounts of a seized bathtub-overflow mechanism being freed
   without pipe replacement, and note unsuccessful attempts or necessary replacement. The
   wave-18 Repipe Specialists fold documents the destructive-access path with full
   restoration, and the wave-19 PLASTER EFFECT review excerpt documents the restoration
   step after a plumber's ceiling cut; the repair-first path still has no attributable
   public outcome. Avoid guaranteeing a non-destructive result.
7. **Resolve the standing flags.** Ho Pronamic's observed bond suspension; Doc Painting's
   differing addresses and complaint-disclosure link; Gee Construction's multiple registry
   numbers; Doc and Tadashi name aliases; the wave-18 name questions (Ron Chan / YONG RONG
   CHEN, Carpentech / YU OUYANG, Winner Remodel / BAK REMODEL, Morris Home's historical
   disciplinary bond); and the new wave-19 items: Reborn Bath Solutions' four-reason
   suspension, the several unreadable workers-comp classification codes (543200 on
   1013908; 5183 on 1050217; 5183/518764/881001 on 1003568; 5146 on 915382), and the 515
   phone on Chiang's Construction (536542). A displayed complaint or bond line is not an
   adjudication.
8. **Obtain project-specific confirmation only with outreach authorization.** Insurance,
   availability, actual dispatch, the assigned technician, subcontractor coordination and a
   written repair-first scope are not established here. No messages or forms were sent. Keep
   the master empty until the relevant evidence and scope requirements are satisfied.
9. **Check applicable City requirements before work.** General research is not a site
   assessment, permit determination, hazardous-material assessment or guarantee of safe
   access. Use the existing official-source compliance panel and qualified professionals.

## Access and verification limitations

- Shell HTTPS retrieval fails in this sandbox; the page-reader tool succeeds. Evidence is a
  field transcription, not a raw-byte download.
- Yelp business pages remain blocked; all Yelp evidence is search-extract and marked as such
  on every record. Reddit pages returned HTTP 403 this session; thread evidence is
  search-extract only. No claim is made to have read all reviews of any business.
- Thumbtack category pages change between sessions; wave 19's displayed ratings and hire
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

Local unit and monitor tests passed for wave 19. Local Chromium was not installed in this
session; use the GitHub Actions browser result (including the new
`tests/browser/discovery19.spec.js`) as the deployment gate. `CHROMIUM_PATH` can select an
already installed browser. The preview binds to `0.0.0.0:4173` and serves only allowlisted
files (`scripts/serve.py` — add new public files to its allowlist if serving locally fails
for them).

Future corpus edits must deliberately update the wave-17 baseline guard after an audited
merge, not remove it just to make a test pass. Waves 18 and 19 add their own baseline
guards (`tests/discovery18.test.js`, `tests/discovery19.test.js`) computed over the same
unchanged `data/research.json`.

## Pages configuration limitation

The existing Pages site is public and uses legacy publication from `main` at `/`. The API
refused changing it to Actions publication with HTTP 403 (integration permission limit), so
that setting was left unchanged. The workflow stages an explicit public-file allowlist for a
future Actions deployment and now includes `discovery19.html`, `discovery19.js`,
`data/wave19.json` and `data/wave19-discovery-log.md`, but **legacy publication does not use
that allowlist**. Treat every tracked file as public. An authorized repository administrator
can select GitHub Actions as the Pages source later; no credential should be stored in this
project. Once this wave is merged to `main`, legacy Pages republishes it automatically.
