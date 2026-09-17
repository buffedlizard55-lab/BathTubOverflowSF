# Next-session handover

Updated 2026-09-17. This replaces the wave-16 next-session instructions; historical
wave evidence remains in `data/` and the README.

## Current state

- Existing corpus: **793 records, 673 sources, 172 retained review excerpts**.
  These inherited claims were not all re-read this session; their original dates remain.
- Separate wave-17 queue: **50 new name/registry-number records**, 4 CSLB detail
  checks (3 active B, 1 suspended B), no new retained business reviews.
- **Zero qualified master entries.** Do not call the combined records 843 verified businesses.
- `data/research.json` is unchanged. `data/wave17.json` records the baseline SHA-256,
  field transcriptions, two City query URLs, licence observations and unresolved gates.
- Pages already existed. `discovery.html` adds a searchable, responsive, exportable
  queue linked from the existing site. The queue is intentionally not merged into the corpus.
- Three audit passes are documented in `data/wave17-discovery-log.md` and regression-tested.

## Highest-value next work — prioritize depth, not another generic 50

1. **Prove both services.** Use the existing diagnostic shortlist as the plumbing track
   and existing drywall candidates as the restoration track. Obtain firm-specific public
   evidence for small repair work, ceiling restoration and access-hatch installation.
   Keep a coordinated two-business option distinct from a single-business option.
   Neither a name nor a B classification demonstrates either service for this project.
2. **Resolve current identity and service area.** Read current CSLB details for the 46
   unchecked registry numbers before treating them as contractors. Resolve aliases,
   address changes and other licence numbers, then locate each firm's own current service
   page. ZIP 94122 in the City query is the **firm contact ZIP**, not a project ZIP and not
   proof of Outer Sunset dispatch. Deprioritize unrelated trades instead of inflating a list.
3. **Review attribution before aggregation.** Find original business profiles on Yelp,
   Thumbtack and Google; retain permitted excerpts with author, date when visible,
   profile identity, URL, read date and access mode. Keep platform ratings separate;
   do not average incompatible or duplicated corpora. Reddit is anecdotal context unless
   a named firm and outcome can actually be attributed. Never invent missing dates.
4. **Exact-task outcome.** Seek accounts of a seized bathtub-overflow mechanism being
   freed without pipe replacement, and note unsuccessful attempts or necessary replacement.
   This session found no attributable outcome for its new leads. That is **not** proof
   that no public evidence exists anywhere. Avoid guaranteeing a non-destructive result.
5. **Resolve the flags.** Ho Pronamic's observed bond suspension; Doc Painting's differing
   addresses and complaint-disclosure link (underlying details unread); Gee Construction's
   multiple registry numbers; Doc and Tadashi name aliases. A displayed complaint link is
   not an adjudication or a basis to invent allegations.
6. **Obtain project-specific confirmation only with outreach authorization.** Insurance,
   availability, actual dispatch, the assigned technician, subcontractor coordination and
   a written repair-first scope are not established here. No messages or forms were sent.
   Keep the master empty until the relevant evidence and scope requirements are satisfied.
7. **Check applicable City requirements before work.** General research is not a site
   assessment, permit determination, hazardous-material assessment or guarantee of safe
   access. Use the existing official-source compliance panel and qualified professionals.

## Access and verification limitations

- Shell HTTPS retrieval of the City dataset failed TLS in this sandbox. The page-reader
  tool succeeded. Evidence is explicitly a field transcription, not a raw-byte download.
- The initial City response was only partly read. The second targeted query returned 52
  name/number pairs and was read completely. Two aliases were counted once. This establishes
  the retained pairs, not the completeness of the City's registry or 50 distinct legal entities.
- Search excerpts and live Thumbtack category pages differed during this session. Do not
  silently promote indexed listings, ratings or snippets into a verified live profile.
- No complete Google review corpus was retrieved, and no claim of reading all reviews is made.
- Tests check consistency, source references, escaping, privacy markers and conservative
  gates. They cannot independently prove source truth or review authenticity. The three
  passes are audits by one agent, not three independent reviewers.
- The existing privacy digest test is a regression safeguard, not a comprehensive privacy
  scanner. Review all new public artifacts before publishing. Keep nonpublic context out
  of data, logs, issue text, commit messages, pull requests and outreach.

## Reproducible validation

```sh
npm ci
npm test
npm run test:monitor
npx playwright install --with-deps chromium
npm run test:browser
npm start
```

Local unit and monitor tests passed. Local browser launch was initially blocked because
Chromium was absent and its download failed TLS; use the GitHub Actions browser result as
the deployment gate, not that failed local launch. `CHROMIUM_PATH` can select an already
installed browser. The preview binds to `0.0.0.0:4173` and serves only allowlisted files.

Future corpus edits must deliberately update the wave-17 baseline guard after an audited
merge, not remove it just to make a test pass. Existing wave-specific tests intentionally
retain historical counts. The source monitor currently covers the main research corpus,
not the separate wave-17 queue; extend it without confusing availability with verification.

## Pages configuration limitation

The existing Pages site is public and uses legacy publication from `main` at `/`.
The API refused changing it to Actions publication with HTTP 403 (integration permission
limit), so that setting was left unchanged. The workflow stages an explicit public-file
allowlist for a future Actions deployment, but **legacy publication does not use that
allowlist**. Treat every tracked file as public. An authorized repository administrator
can select GitHub Actions as the Pages source later; no credential should be stored in
this project. The existing legacy site can still publish the merged change.
