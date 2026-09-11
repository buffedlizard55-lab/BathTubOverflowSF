# Wave-6 discovery log — September 11, 2026

Wave 6 adds **50 new records**, **47 new sources** (ids 150–196) and **6 new review
excerpts** (R60–R65). The merged directory now holds **301 records / 196 sources /
68 reviews**. Nothing was promoted to the qualified master list — it remains empty.

This wave is deliberately different from waves 3–5. Those were discovery passes over
indexed directory text. Wave 6 is a **credential pass**: 22 of its 50 records carry a
CSLB license detail page that was read directly on `cslb.ca.gov`, and a further 16
carry an official San Francisco DBI permit-registry row. Three direct CSLB reads were
also attached to pre-existing entries that had previously been discovery-level only.

## 1. What was retrieved, and at what verification level

| Evidence level | Sources | Records | What it can prove |
| --- | --- | --- | --- |
| CSLB license detail page read directly (`access: page`) | 22 | 22 wave-6 + 1 attached to `bernal-hill` | legal entity, classification(s), status, expiry, bond, workers-compensation lines, recorded business address — **as of the check date only** |
| SF DBI "Plumbing Permits Contacts" open data (`k6kv-9kix`) | 2 queries + 1 dataset source | 16 registry-only | firm name, registry-recorded CSLB number, recorded business address, plumbing-permit row count. Rows are historical and carry **no in-dataset dates** |
| SF.gov DBI service page (`sf.gov/apply-plumbing-and-mechanical-permit`) | 1 | drives the `compliance` block | the City's own statement of when a permit and an inspection are required |
| Indexed directory / marketing extracts (`search-extract`, `blocked-with-search-extract`) | 20 | 12 finish-trade records + corroboration for licensed records | names, ratings, badges, service-area statements, short review excerpts. **Discovery only** |
| Thumbtack structured review data (JSON-LD in an indexed extract) | 1 | R60–R65 | dated, attributed review text for one business |

Source kinds for ids 150–196: 27 `government`, 13 `directory`, 6 `business`,
1 `platform`. Access levels: 27 `page`, 11 `search-extract`,
9 `blocked-with-search-extract`.

Direct access to complete Yelp, Thumbtack, Google and Reddit review corpora remained
unavailable this session, exactly as in waves 1–5. Where that is true, the record says
so; no record claims a complete review corpus was read.

## 2. How candidates were found (real retrievals, this session)

**Official registry queries (data.sf.gov, dataset `k6kv-9kix`).** Grouped SoQL queries
on `zipcode like '94122%'` and `zipcode like '94116%'` returned every firm with a
plumbing-permit history at an Outer Sunset or Parkside address, ordered by permit-row
count. The 22 highest-count firms were each taken to CSLB for a direct license read.
The next 16 by row count are stored as **registry-only** records.

94116 (Parkside) is labelled "Parkside, adjacent to Outer Sunset" — never `outer` —
because it is a different neighbourhood with a different dispatch pattern.

**Indexed extracts.** Yelp Outer Sunset / SF drywall, plaster and stucco pages;
Thumbtack SF plastering; Angi/HomeAdvisor SF drywall; three company sites
(`bernalhilldrywall.com`, `rsdynamicbuilders.com`, `newlinedrywall.com`).

## 3. All 23 direct CSLB reads

`Data current as of 9/11/2026` on every page read. Sorted by license number.

| # | Business / legal entity | Class | Status | Expires | CSLB-recorded area |
| --- | --- | --- | --- | --- | --- |
| 265709 | Ron Hogan Drywall | C-9 | active | 2026-11-30 | outside (Fairfield) |
| 287477 | Asia Plumbing | C16/C36 | **expired** | 2014-05-31 | outer (1354 31st Ave) |
| 570753 | Ricky's Plumbing Company | C36 | **canceled** | 2005-06-30 | sunset |
| 665412 | Chen's Plumbing Inc | C16/C36 | **canceled** | 2015-02-16 | sunset |
| 812845 | B R Troika Inc. dba Mr Rooter Plumbing | C36 | **expired** | 2018-09-30 | outer (2341 Judah) |
| 820321 | Hegarty Plumbing | C36 | active | 2027-06-30 | sf (PO Box 94127) |
| 837694 | Goodrich Plumbing Inc | C36 | **canceled** | 2025-02-11 | sunset |
| 839447 | Feng K Plumbing Co | C36 | active | 2028-05-31 | outer (1654 23rd Ave) |
| 859973 | Pro Plumbing | C36/C16 | **expired** | 2023-06-30 | sunset (Barneveld Ave) |
| 885083 | Ros Plumbing LLC | C36/C-4/B | active | 2027-02-28 | outside (Novato) |
| 898289 | Gorman Pipeline Inc | **A only** | active | 2027-06-30 | outer (1518 27th Ave) |
| 900309 | West Cork Plumbing Inc | C36 | active | 2027-08-31 | outside (Novato) |
| 916617 | De Barra Plumbing | C36 | active | 2028-06-30 | **outer (1511 39th Ave)** ★ |
| 947504 | Building Efficiency Inc | B/C20/C36/C10 | active | 2028-05-31 | **outer (2037 Irving)** ★ |
| 950265 | All-Point Solutions Plumbing Co | C36 | **suspended** | 2028-07-31 | outer (1651 42nd Ave) |
| 966337 | Flow Masters Plumbing Inc | C36/C16/C20 | active | 2027-10-31 | outside (Daly City) |
| 976543 | Moonlight Plumbing | C36 | active | **2026-09-30** | outside (Yucca Valley) |
| 989225 | Parks Plumbing Inc | C36 | active | 2026-12-31 | outside (Pacifica) |
| 998141 | Faherty Plumbing and Heating | C36 | active | 2028-09-30 | **outer (4004 Irving)** ★ |
| 1022789 | F C Company | B/C36 | **suspended** | 2027-01-31 | outside |
| 1057063 | Caledonia Plastering & Stucco Inc | **C35** | active | 2027-08-31 | **outer (1551 Judah St)** ★★ |
| 1130530 | R S Dynamic Builders Inc | **B only** | active | 2026-12-31 | sunset (909 Ocean View Ave) |
| 995163 | Bernal Hill Drywall (attached to existing `bernal-hill`) | C-9 + B | active | 2028-07-31 | sf (720 Anderson) |

Result: **14 active, 3 expired, 3 canceled, 2 suspended.**

★ = the license's own CSLB page records a 94122 Outer Sunset business address. These
four became shortlist calls 06–09. The distinction matters: a marketing page can claim
any service area, but the regulator's address of record cannot.

## 4. Classification-versus-scope audit (pass 8)

Every licensed record is now checked against the classification its declared trade
actually requires, not merely against "is the license active". Two findings would have
been invisible to a status-only check:

- **Gorman Pipeline Inc (898289)** — active, at an Outer Sunset address, but `A`
  (General Engineering) only, with sewer-construction workers-compensation codes and no
  C-36. Recorded as a **scope exclusion**, not a hold, so it is not mistaken for a
  plumber.
- **R S Dynamic Builders Inc (1130530)** — active, but `B` (General Building) only: no
  C-36 and no C-9. A B licensee may *contract* for the work but must subcontract the
  trade; that is recorded as a hold-level flag rather than as a capability.

`licenseSupportsTrade()` in `lib.js` encodes this, and `mayPromote()` now refuses to
promote a plumbing requirement on a drywall classification or vice versa.

## 5. Registry-only records: deliberately fail-closed

16 firms have an official SF DBI registry row but **no CSLB page was read**. For every
one of them `license` is `null`, and the CSLB number appears only inside the Discovery
excerpt, worded "registry-recorded … has NOT been read on CSLB this pass". A hold-level
flag repeats that. The registry is a permit-history table; it is not a licensing
authority and cannot establish present status.

Ocean Air Heating, Bill Bragg Plumbing, C T Construction & Plumb, Francis John Burke,
Hawk N Lee Co, Ren Lei Construction Co, Abe's Plumbing, City Plumbing Company (94122);
Best Plumbing Choice, O M P P Inc., L R Plumbing, Yao Star Construction,
L C Plumbing & Fire Protection Inc, J A Plumbing Inc, F-1 Plumbing Services,
Excellent Plumbing Co (94116).

## 6. Entity resolution and de-duplication (pass 7)

- **Chris Goodwin Plumbing** — rejected as a duplicate of the existing `plumbworks`
  record; no second entry created.
- **Feng K Plumbing Co (839447)** — CSLB records a *sole ownership*, while a directory
  extract styles the entity "Corp.". Recorded as a discrepancy flag; the CSLB entity
  name is the one stored. Three different phone numbers appear across sources; only the
  CSLB number is attached, normalised to `415-845-3870` so the `tel:` link works.
- **"San Francisco Plumbing" (registry 323223)** — likely dual-license confusion with the
  existing Ace Plumbing record (829071). Logged as a verify item, not merged.
- **Pro Plumbing (859973)** — CSLB ZIP is 94122 but the street is Barneveld Ave, which is
  not in the Outer Sunset. Recorded as an address conflict, area `sunset` rather than
  `outer`.
- **Caledonia Plastering & Stucco (1057063)** — Yelp labels 1551 Judah St as "Outer
  Sunset" (94122); Thumbtack structured data says 94116; CSLB says 94122. The regulator
  wins; the ZIP discrepancy is flagged rather than silently resolved. BBB and BuildZoom
  independently publish #1057063 expiring 08/31/2027, matching the CSLB read.

## 7. Rejections

- **SR Water Mitigation** — restoration/mitigation scope, not repair; rejected.
- **Jose HandyMan Services** — the indexed review excerpt on this listing names a
  reviewer ("Singh") who does not correspond to the business name. Same index-text-bleed
  pattern flagged in wave 4. The review was **rejected, not attached**, and the source is
  retained (id 178) with the irregularity recorded on the summary page.
- **Access-panel installers** — re-confirmed the wave-4 finding: no dedicated SF access
  hatch installer exists. Hatch framing remains a carpenter/drywall task.

## 8. New irregularities recorded this wave

- **Two licenses suspended on one bond date.** All-Point Solutions Plumbing Co (950265,
  CSLB address 1651 42nd Ave, 94122) and F C Company (1022789) both read "License is
  under Contractors Bond Suspension", and both show a contractor's bond with Hudson
  Insurance Company carrying a cancellation date of **09/01/2026**. A suspended license
  cannot lawfully contract. The shared date and shared surety suggest a surety-wide event
  rather than two unrelated business failures — flagged as a pattern, not explained away.
- **A second lapsed C-36 behind the Mr. Rooter brand.** B R Troika Inc. dba Mr Rooter
  Plumbing (812845) at 2341 Judah, 94122 expired 09/30/2018 and reads "not able to
  contract". This sits alongside the existing finding that SDP Plumbing Inc (1016070)
  expired 07/31/2024. The registry also records two spellings and two Judah Street
  numbers for the same firm.
- **Moonlight Plumbing (976543)** is active but expires **2026-09-30**, nineteen days
  after the check — and CSLB now records a Yucca Valley address despite an Outer Sunset
  permit history.
- **Registry history ≠ present operation.** West Cork (Novato), Flow Masters (Daly City)
  and Moonlight (Yucca Valley) each hold 94122 permit histories with non-SF current
  addresses.
- **Marketing that does not match the regulator.** `rsdynamicbuilders.com` publishes
  CSLB# 1130530 and lists "Sunset" in its service area, but its own JSON-LD gives
  `streetAddress: "123 Main Street"` against CSLB's 909 Ocean View Ave, and a
  `+1 415 450 7338` phone against CSLB's `(650) 918-2317`. Placeholder content in
  structured data is recorded as an identity flag.
- **Third-party "Verified License" badges** on Yelp for All About Plastering (4.8/34),
  Gray Lath and Plaster and Marcelino Plastering (4.9/40) are platform badges, not CSLB
  reads. All three are stored with `license: null`.
- **Truncated indexed quotes.** The Bernal Hill ceiling quotes and the Meticulous
  Handyman plaster-ceiling quote arrive truncated in the index extract. They are quoted
  only up to the truncation; no quote was completed or paraphrased into a fuller sentence.

## 9. Carried-forward irregularities (unchanged, still on the records)

Mr. Rooter SF #1016070 expired; Master Rooter believed out of business; 5 Star #996627
reissued to another entity 11/17/2025; Repipe Champions #1057927 resolves to an
unrelated Hayward B licensee; AB Plumbing bond cancellation 10/03/2026; 24-7 Rooter
expires 11/30/2026; Plumbing Pure's listed license expired at check; Thumbtack's former
Plumbing Pure profile now redirects to Legato; Precision Rooter's indexed description
says no plumbing repairs.

One pre-existing minor observation surfaced by the tightened tests: `kenneth-asire`
(wave 3) still carries a bare `http://` website. It was **not** edited, because
re-verifying a wave-3 URL is out of scope for this pass; the test suite now asserts that
exactly one such record exists, so a second cannot appear unnoticed.

## 10. Attaches to pre-existing entries

| Record | What was attached | Source |
| --- | --- | --- |
| `bernal-hill` | CSLB #995163 (C-9 + B, active, exp 07/31/2028), website, phone, area → `sf`; two Yelp ceiling-patching reviews (R66, R67) | direct CSLB read + indexed Yelp extracts |
| `meticulous` | one plaster-ceiling review (R68); trade → `finish` | indexed Yelp extract, truncated |
| `bay-area` | a clearly-labelled **portfolio caption** claim (not a review); trade → `plumbing` | indexed extract |

These were previously discovery-level records. They now carry regulator-read licenses
where one was established, and their trade fields were set so the classification audit
applies to them too.

## 11. Official permit rules (pass 9)

Read directly from `https://www.sf.gov/apply-plumbing-and-mechanical-permit` and stored
in `data.compliance` with the source id, so the site can render it with citations
instead of paraphrase. Key facts retained verbatim-in-substance:

- A permit is required before cutting into or replacing pipes, "particularly pipes that
  will be covered by a wall".
- **Before covering pipes, you must have it inspected.**
- Exemptions live in SF Plumbing Code §104.2. The section text itself was **not**
  retrieved this session; the dataset says so and links to it rather than summarising it.
- Only SF-registered licensed contractors may apply online. Only an owner-installer of a
  stand-alone single-family home may self-permit.
- DBI Permit Services: 49 South Van Ness Ave, 2nd floor, SF 94103 · 628-652-3200.

Broad web searches on permit rules were deliberately **not** cited — they return SEO and
forum content. The City's own service page is authoritative and is the only source used.

## 12. Admission result

**0 of 50 added to the qualified master list.** The master list has been empty across
all six waves and stays empty. Each candidate still lacks at least one mandatory gate:
exact seized-overflow-trip-lever evidence, applicable insurance confirmation, and a
written repair-first scope. This is a fail-closed result, not a claim that the
businesses are unqualified.

The shortlist grew from 5 to **9** because four records now satisfy a stricter test than
calls 01–05: an active license **whose own CSLB page records a 94122 Outer Sunset
address**, plus the classification its trade requires. Calls 06–09 are rendered as a
clearly-labelled second tier on the decision brief.

| Call | Business | License | Class |
| --- | --- | --- | --- |
| 06 | Caledonia Plastering & Stucco Inc | 1057063 | C35 (Lathing & Plastering) |
| 07 | Building Efficiency Inc | 947504 | B / C20 / C36 / C10 |
| 08 | Faherty Plumbing and Heating | 998141 | C36 |
| 09 | De Barra Plumbing | 916617 | C36 |

Caledonia is the strongest **finish-trade** find of the whole six-wave exercise: an
active C-35 lathing-and-plaster licensee whose regulator-recorded address is 1551 Judah
Street, 94122 — i.e. in the Outer Sunset — with a Thumbtack sample of 4.875/56 and an
indexed excerpt stating the work passed city inspection. It is *not* a plumber and must
not be called for the trip lever.

## 13. Reproduction

```bash
python3 scripts/gen_wave6.py           # rebuilds data/wave6.json from the captured retrievals
python3 scripts/merge_wave6.py         # trade-aware, fail-closed merge into data/research.json
python3 scripts/patch_wave6_attaches.py # attaches CSLB reads to 3 pre-existing records
npm test                               # 22 data + render assertions
```

`merge_wave6.py` is idempotent: it refuses to re-merge a wave that is already present.
`scripts/merge_wave.py` (waves 1–5) cannot ingest wave 6 because it hardcodes C36 as the
only acceptable classification.
