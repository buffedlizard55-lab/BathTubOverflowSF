# Wave-7 discovery log — September 11, 2026

Wave 7 adds **50 new records**, **21 new sources** (ids 197–217) and **20 new review
excerpts** (R69–R88). A follow-up pass in the same session added **4 more sources**
(ids 218–221) and **10 more review excerpts** (R89–R98), applied to **seven
pre-existing records** rather than counted as new rows. The merged directory now holds
**351 records / 221 sources / 98 reviews**. Nothing was promoted to the qualified master
list — it remains empty.

Wave 6 was a credential pass over the official permit registry. Wave 7 is a **channel
pass**: it deliberately mixes three evidence channels of very different strength, keeps
them separable in the data, and reports the mix rather than letting a single count
flatter the whole wave.

| Channel | New records | Verification level |
| --- | --- | --- |
| CSLB license detail page read directly | 10 | Regulator read: legal entity, classification(s), status, expiry, bond, workers-compensation lines, recorded business address — **as of the check date only** |
| SF DBI "Plumbing Permits Contacts" (`k6kv-9kix`), queried by firm ZIP | 20 | Registry row only: recorded firm name, licence number, address, ZIP, permit-row count. **No in-dataset dates, never a licence status** |
| Thumbtack category pages read directly | 20 | Platform listing: name, profile URL, ratings/review counts, badges, one published review each. **Discovery level; a platform badge is not a licence** |

Composition is asserted in `tests/research.test.js` and stored in `data.waves[6]` as
`{count: 50, cslbReads: 12, registryOnly: 20, thumbtack: 20}`.

## 1. What was retrieved, and at what verification level

All 25 new sources (197–221) carry `access: "page"` — every one was retrieved and read
this session, none is an index extract. Kinds: 21 `government`, 2 `directory`,
2 `platform`.

| Sources | What was read | Records / reviews it supports |
| --- | --- | --- |
| 197, 199, 200, 201 | SF DBI permit registry rolled up **per licence number** for ZIP 94122 (Outer Sunset) and 94116 (Parkside), plus two confirmatory re-queries | the 20 registry-only records; discovery of the 10 licence numbers taken to CSLB |
| 198 | SF DBI re-query of the **12 licence numbers taken to CSLB**, grouped by licence *and* ZIP, run *after* the CSLB reads | the multi-name licence histories in §7 |
| 220, 221 | SF DBI re-queries for licences 723992 and 660638 alone, grouped by firm name, address and ZIP | the two licence attaches in §9 |
| 202–213 | 12 CSLB `LicenseDetail.aspx` pages, one per licence number | 10 new records + 2 attaches |
| 214, 215 | Thumbtack `ca/san-francisco/drywall-repair` and `drywall-contractors` category pages | the 20 marketplace records, R69–R88, and three reviews attached to pre-existing records |
| 218, 219 | Thumbtack **pro profile pages** for New Age Drywall Inc and Caledonia Plastering & Stucco | R90–R94 and the Caledonia hold |
| 216 | data.ca.gov CKAN `package_search?q=contractor+license` | **documented negative result** — see §6 |
| 217 | CSLB `ZipCodeSearch.aspx` (Find A Licensed Contractor → Search by Location) | **documented negative result** — see §6 |

Direct access to complete Yelp, Google and Reddit review corpora remained unavailable
this session, exactly as in waves 1–6. Thumbtack, by contrast, was directly retrievable
— both category pages and individual pro profiles returned HTTP 200 — so for the first
time this project holds **dated, attributed review text read from the publishing
platform** rather than from a search index. Where that is true the review carries
`access: "page"` and `identity: "matched"`; where a reviewer's initials are not
displayed it carries `identity: "unverified-username"`.

## 2. How candidates were found (real retrievals, this session)

**Official registry (data.sf.gov, dataset `k6kv-9kix`).** The column is `zipcode`, not
`firm_zip`. Two SoQL rollups grouped by `license_number` on `zipcode like '94122%'` and
`zipcode like '94116%'` returned every firm with a plumbing-permit history at those
addresses, ordered by permit-row count (~130 and ~52 firms). Both lists were
de-duplicated against all 301 pre-existing records **by exact licence number and by
normalised name**, leaving 112 new 94122 candidates and 42 new 94116 candidates. The 30
highest-count new 94122 candidates were split: the top 10 by row count were taken to
CSLB for a direct licence read, the next 20 are stored as registry-only records.

94116 (Parkside) is labelled adjacent, never `outer`, and 94134 / 94110 / 94996 rows are
never treated as Outer Sunset coverage.

**Thumbtack.** `thumbtack.com/ca/san-francisco/drywall-repair` (5 chunks) and
`/drywall-contractors` (3 chunks) were read directly. Each pro entry publishes a profile
URL whose **path encodes the pro's home market** (`/ca/san-francisco/`, `/ca/redwood-city/`,
`/id/boise/`, `/ca/san-pablo/moving-companies/`), which is what exposed three of this
wave's area irregularities. Category pages also mix in unrelated trades (house cleaning,
floors, furniture assembly, moving); those were filtered out by category relevance and
logged in §8 rather than stored.

## 3. All 12 direct CSLB reads

`Data current as of 9/11/2026` on every page read (times 4:58–5:03 PM). Sorted by licence
number.

| Licence | Legal entity on the page | Class | Status | Expires | CSLB-recorded address | Outcome |
| --- | --- | --- | --- | --- | --- | --- |
| 141304 | KEN TOPPING HOME IMPROVEMENTS | B, C20 | **expired** (canceled after expiration) | 2011-04-30 | 3101 Vicente St, SF 94116 | new record `w7-ken-topping-home-improvements`, held |
| 576600 | MICHAEL KUENZLI PLUMBING CO | **C36** | **CURRENT AND ACTIVE** | 2027-09-30 | 1234 21 Avenue, SF **94122** | new record, **call 09** |
| 600722 | — | — | — | — | — | registry-only (see §5) |
| 609942 | GRANT PLUMBING & CONSTRUCTION | C36, B | **expired** | 2007-01-31 | 1613 142nd Avenue, **San Leandro 94578** | new record, held; identity mismatch |
| 644189 | RU MAHN PLUMBING | C36 | **expired** (32 years) | 1994-05-31 | 1339 16th Avenue #4, SF **94122** | new record `w7-ru-mahn-plumbing`, held |
| 660638 | BILL CALLAWAY PLUMBER | C36 | **expired** | 2014-12-31 | 3141 Balboa St, SF 94121 | **attached** to wave-1 `bill-callaway`, held |
| 661818 | EHRICH'S PLUMBING | C36 | **INACTIVE** | 2026-12-31 | 1607 31st Avenue, SF **94122** | new record, held |
| 708086 | BUILDING REPAIR CO | B only | **expired** | 2022-01-31 | 579 17th Ave, SF 94121 | new record, held; scope exclusion |
| 708885 | HO'S CONTRACTOR CO | B only | **expired** | 2015-06-30 | 1371 46th Ave, SF **94122** | new record, held; scope exclusion |
| 716856 | ALPINE CONSTRUCTION | **A only** | **expired** | 2021-12-31 | 1032 Irving Street #713, SF **94122** | new record, held; scope exclusion |
| 721668 | A R PLUMBING | C36 | **expired** | 2012-04-30 | 1902 Spencer Street, **Napa 94559** | new record, held; address drift |
| 723992 | JOE WATTERSON PLUMBING | **C36** | **CURRENT AND ACTIVE** | 2028-06-30 | 3653 Folsom Street, SF 94110 | **corroborating re-read** of wave-2 `joe-watterson` |
| 734011 | MIDMARKET DEVELOPMENT COMPANY INC | B only | **REVOKED** | 2010-01-31 | 1072 Folsom Street Ste 483, SF 94103 | new record, held; complaint disclosure exists |

Result: **2 active** (one of which was already a wave-2 record), **1 inactive**,
**8 expired**, **1 revoked**. Two new statuses — `inactive` and `revoked` — enter the
dataset for the first time in this wave; both are handled by the same fail-closed rule as
`expired`, `canceled` and `suspended`, and `tests/research.test.js` now asserts the full
six-value status vocabulary.

Not read: every CSLB page read here was reached by typing the literal
`…/LicenseDetail.aspx?LicNum=<number>` URL. Constructed proxy or rewritten URLs fail with
`SignatureDoesNotMatch` and were discarded rather than retried, so no read in this log
rests on a URL that was not fetched.

## 4. Classification-versus-scope audit (pass 12)

Every licence read this wave was compared against the work it would lawfully cover:

- **716856 Alpine Construction** holds class **A (General Engineering) only** — no B, no
  C36, no C-9. An A licence cannot self-perform a bathtub repair or a ceiling patch, so
  the record is a scope exclusion as well as an expiry hold. Its contractor's bond
  (Western Surety $25,000) is effective **01/01/2023**, i.e. *after* the 12/31/2021
  licence expiry, and was itself cancelled 04/28/2023 — a bond line that postdates the
  licence it supposedly supports is recorded verbatim rather than smoothed over.
- **708086 Building Repair Co** and **708885 Ho's Contractor Co** are **B-only**: a
  general building contractor may coordinate but not self-perform plumbing, and neither
  holds C-9 for the ceiling patch.
- **141304 Ken Topping** is B + C20 (warm-air heating), issued **10/06/1953**, with
  miscellaneous entries showing authority to continue until 07/19/2011 and cancellation
  per request on that date. A 1953 issue date is retained because it bears on whether a
  1940s galvanized assembly is within living memory of the business — but the licence has
  been gone for fifteen years.
- **660638 Bill Callaway** is C36, so the trade matches, but the licence expired
  12/31/2014 and the bond of record was cancelled 03/09/2012.
- **576600 Kuenzli** is the one clean read: C36, active to 09/30/2027, bond $25,000
  (Atlantic Specialty) effective 08/22/2025 with no cancellation, issued 09/06/1989.
  Miscellaneous entries show cash-deposit letters sent 11/06/2015 and 01/14/2016
  ($15,000); they are recorded verbatim because they are part of the page, not because
  anything was concluded from them.
- Every workers'-compensation line on these pages is either an **exemption** or a lapsed
  policy. An exemption is not coverage, and each record says so.

## 5. Registry-only records: deliberately fail-closed

The 20 registry-only records are the next 20 firms by 94122 permit-row count that had not
already been read on CSLB and were not already in the directory:

C W Lee Plumbing Company (586693, 221 rows) · W & J Plumbing (486546, 181) · David Chu
Plumbing (343610, 122) · Franks All City Plumbing (319594, 82) · W.K. Construction
(608902, 67) · J K Construction (552359, 63) · Snc Plumbing (595176, 61) · Allen
Mechanical (611082, 60) · Chow's Plumbing (502603, 51) · Coast Pacific Construction
(735719, 20) · Larry Fitzsimmons Plumbing (459387, 13) · K L Plumbing (510452, 12) ·
Wallace Plumbing (703293, 11) · Transpacific (664585, 9) · Noriega Heating (542108, 5) ·
Lam & Lee Plumbing (329444, 4) · Campbell Custom Woodwork (710842, 2) · Hammerhead
Construction (637927, 10) · Ecd Construction Inc (470364, 3) · Admond Construction Inc
(600722, 3).

Each one:

- has **`license: null`** — the registry's licence number is stored in the Registry claim
  text and excerpt, never in the licence field;
- carries a `gap` flag stating the number **has NOT been read on CSLB** and that registry
  rows never establish that a licence is current, that the firm still operates, or that it
  dispatches to the Outer Sunset today;
- is stored at `area: "sunset"`, **not** `outer`, because a registry ZIP is a recorded
  address and not a service-area statement (this is the wave-6 convention, kept);
- was re-read in a confirmatory grouped query (sources 199 / 201) so no name, address, ZIP
  or permit count is published from a single transient reading.

## 6. Two documented negative results

Both are stored as sources with `access: "page"` because both were genuinely retrieved;
neither supports any business record, and neither is presented as evidence of anything
except what it ruled out.

- **216 — data.ca.gov CKAN `package_search?q=contractor+license`.** Tested whether the
  State publishes an official CSLB licence extract through an open-data API, which would
  allow every active 94122 C-36 and C-9 licensee to be **enumerated** rather than sampled.
  Returned `success: true` with `result.count: 4` and **no Contractors State License Board
  dataset** (the hits were water-rights and unrelated records). Consequence: CSLB facts in
  this wave still come from individual licence detail pages read one at a time, and the
  directory remains a **sample**, not a census. This is stated on the site.
- **217 — CSLB `ZipCodeSearch.aspx`.** CSLB's own area search says it will return "a
  randomly generated list of all eligible contractors in that license classification whose
  CSLB license of record is in the area you entered", and that "You can select only one
  license classification at a time." The form **posts** to a results page that returned
  **HTTP 404** to a direct GET, so it cannot be read without a browser session. Two
  consequences are recorded rather than worked around: the randomly-generated nature of
  the list means it is not an exhaustive enumeration even in a browser, and one
  classification per query means a 94122 census would need separate C-36, C-9 and C-35
  passes.

`lib.js` counts `cslbReads` from `LicenseDetail.aspx?LicNum=` URLs only, so source 217
cannot inflate the "licence pages read directly" figure. It is 70.

## 7. Entity resolution and de-duplication (pass 11)

Every candidate was checked against all 301 pre-existing records by **exact licence
number** and by **normalised name** (case, punctuation and accent insensitive) before the
generator was written. `scripts/merge_wave7.py` re-runs that collision gate and refuses to
merge on any hit.

**One collision was caught and it changed the wave's composition.** "Joe Watterson
Plumbing" appeared in the 94116 registry rollup as a new candidate; it is already record
`joe-watterson` (wave 2, licence 723992, active C36). It was therefore **removed from the
new-record list** and converted into a corroborating re-read attach (§9). Three
registry-only firms were added in its place so the wave still totals exactly 50 new
records, and that substitution is recorded in `data.waves[6]` and source 201's note rather
than being absorbed silently.

**Registry firm names frequently are not the CSLB licensee names.** Source 198 (grouped by
licence *and* ZIP, run after the CSLB reads) exposed four multi-name licence histories:

- **723992** — CSLB: JOE WATTERSON PLUMBING, 3653 Folsom St 94110. Registry: "Slemish
  Plumbing" at 2186 46th Ave 94116 (269 rows across five address spellings) **and** "Joe
  Watterson Plumbing" at 384 Somerset St 94134 (194), 3653 Folsom St 94110 (53), 2186
  46th Av 94116 (5) and Po Box 415 94996 (5). Four ZIPs, two firm names, one licence.
  **No 94122 row exists**, so the record's area stays `sunset` and is *not* widened.
- **609942** — CSLB: GRANT PLUMBING & CONSTRUCTION, San Leandro 94578, expired 2007.
  Registry: "Drop Stop Plumbing Service", 1481 25th Ave Ste 4, 94122 (7 rows) plus a
  misspelled variant (2). Same pattern as wave 4's Repipe Champions (#1057927).
- **734011** — CSLB: MIDMARKET DEVELOPMENT COMPANY INC, 1072 Folsom St 94103, **REVOKED**,
  complaint disclosure information exists, reissued to another entity 01/15/2008.
  Registry: "Killarney Construction", 1291-11th Ave #5, 94122 (3 rows).
- **660638** — CSLB: BILL CALLAWAY PLUMBER, 3141 Balboa 94121. Registry: 170 rows at 3141
  Balboa (94121) and 7 rows at 1850 42nd Avenue (**94122**), the two 94122 rows filed
  under the exact CSLB entity name.
- **708086** — registry rows at both 94121 (44) and 94122 (23); CSLB address is 94121.

The systemic reading: registry rows are **historical permit contacts**, so a firm name on
a row is the name that pulled a permit at some point, while CSLB shows the licensee today.
Where the two disagree the record says so, keeps both, and infers neither.

**Thumbtack name-alikes kept separate.** Three different first names recur across distinct
profiles on the same page: "Alfredo" for both Sandoval drywall and Baruch handyman
services, "Sergio" for Fairfield Drywall Inc and for a rejected candidate, "Jose" for
Honart. Profile URLs and reviewers differ, so the records stay separate and the coincidence
is logged on each rather than merged.

## 8. Rejections

Candidates found this session and **deliberately not added**, with the reason:

| Candidate | Why rejected |
| --- | --- |
| Joe Watterson Plumbing (registry, 94116 rollup) | Already `joe-watterson` (wave 2) — converted to a re-read attach |
| Figs Drywall Repair, Mayorga Remodeling, Magaña Time Handyman, Walty Handy Service Pro | Already wave-5 records — reviews and profile URLs attached instead (§9) |
| My solution in (Daly City, 4.8/71) | Cut to keep the wave at exactly 50 after the Joe Watterson substitution; out-of-area and no ceiling/plumbing evidence in its listing |
| Sham | Out-of-area listing with a shared-first-name ambiguity ("Sergio") that this pass could not resolve |
| SAFENEST Restoration (Zachary S. drywall-patching review) | Excluded in wave 4 on an index-text-bleed identity problem; a category-page review is not enough to reopen an exclusion |
| Willy Floors, Laurita Qualiclean, MBond, Gomez painting | Surfaced in the same Thumbtack category pages but are flooring, cleaning and painting trades with no drywall or ceiling evidence |
| Eric Brand, Genteel-style Yelp plumber names (Plumbing Pure, Pham's, Franco's Magical, True-Tech, Legend Plumbing & Drain, WB Plumbing Supply, ASAP Plumbing Pros, USA Rooter, Maverick Water Heaters, Allied Bay Contractors, General SF, Bay Area Plumbing) | Found by web search only, **not** by a page this session could read directly. Yelp pages remain blocked, so none could be given a `page`-level source. Logged here as the next wave's candidate pool rather than stored as unverified records |
| r/PlumberSanFrancisco rate consensus (94122 = $120–$180/hr standard hours) | A forum consensus is not a price quote and Reddit remains blocked; recorded here only, not attached to any business |

Nothing rejected was stored as a record, and no rejected candidate's reviews were
attached to a similarly-named business.

## 9. Attaches to pre-existing entries

Applied by `scripts/patch_wave7_attaches.py` after the merge, so that verification work
lands on the record it belongs to instead of creating a duplicate row.

**`bill-callaway` (wave 1).** Was discovery-level from a Yellow Pages Outer Sunset
directory listing with no credential at all. Now: CSLB 660638 read directly — **BILL
CALLAWAY PLUMBER**, sole ownership, issued 12/08/1992, **EXPIRED 12/31/2014**, C36 only,
bond $12,500 (Old Republic Surety, eff 01/13/2008) **CANCELLED 03/09/2012**, workers'
compensation **exempt** eff 11/23/1992. Registry re-query (source 221) adds 170 permit
rows at 3141 Balboa 94121 and **7 rows at 1850 42nd Avenue 94122**, two of them under the
exact CSLB entity name. Area moved `sf` → `outer` on the strength of the City's own 94122
row, `status` → `hold`, `trade` → plumbing, `checkedAt` → 2026-09-11. Two flags: a `hold`
(expired licence, cancelled bond, WC exemption — a directory listing does not revive a
licence) and a `discrepancy` (three different addresses across three sources).

**`joe-watterson` (wave 2).** CSLB 723992 **re-read** on 2026-09-11 after the 2026-09-10
read: still CURRENT AND ACTIVE, C36, expires 06/30/2028, same 94110 licensee address.
Bond $25,000 (Philadelphia Indemnity, eff 04/26/2025, no cancellation); workers'
compensation exempt with no employees eff 05/19/2026. The licence field now cites the
later read (source 210) and the earlier one (source 60) is preserved as a claim so both
dates stay separately traceable. Source 220 resolves the wave-2 name-history flag into the
four-ZIP / two-name picture in §7, and a new `gap` flag records that **no 94122 row
exists** — so the area is *not* widened to `outer`.

**`w6-caledonia-plastering-stucco-inc` (wave 6, was call 06).** Profile page read directly
(source 219): header "**Plastering • 94116**", Excellent 4.9 (56), Hired 65 times,
background check on John Cullen, **no licence entry in Credentials**, Top Pro badges
**2018/2019/2020 only**, services limited to plastering and stucco (no drywall), and —
for the service and ZIP queried — Thumbtack's own message "**Sorry this pro can't do your
job, but we know other pros who can.**" linking to instant results for ZIP 94116. The
default review list shows five reviews dated 2016–2018 and **nothing later than Jun 2,
2018**. Thumbtack's SF drywall-contractors category page (source 215) publishes a long
negative review by "**Jay D.**" against this exact profile slug, alleging emotionally
volatile conduct, cash payment ("so apparently he doesn't report it to the IRS" — the
reviewer's inference, reproduced as such), an electrician's towel-warmer wire moved, a
**bathroom exhaust covered with plaster**, corrections **refused** on first request, and
name-calling when the defects were raised. No date is displayed for that review, and it is
not in the profile's default list.

Consequences: **removed from the diagnostic call order** and `status` → `hold`; new
`hold` flag; two new `discrepancy` flags (service ZIP 94116 vs the CSLB/Yelp 94122
address; the attribution correction below); reviews R89 (negative, `negative: true`) and
R90 (Jennifer H., Jan 16 2018 — old plaster removed after **water damage** and made to
match, in a building with 110 years of paint) added; claims added for the platform read,
the availability message and the review-sample dates. The active **C35** licence at 1551
Judah Street 94122 is unchanged and still recorded on the held row.

**A wave-6 review attribution was corrected in place.** R60 was stored as author "Tom S.",
published "Jun 2, 2018", carrying the quote "Quick to respond, fair price … John took care
of the hole in the ceiling …". The direct profile read shows that quote under **Vipada W.,
Oct 5, 2017**, and shows Tom S.'s Jun 2, 2018 review as a **different** text about
exterior stucco on a backyard structure. R60's author, date, source, access and identity
were corrected (`access: "page"`, `identity: "matched"`, source 219) and its analysis now
states the correction; Tom S.'s real review was added as **R98** so the displaced author
is restored rather than silently dropped. This is the extract-bleed pattern flagged in
wave 4 (SAFENEST / Mike's Water Damage) and suspected in wave 6 ("Singh" on the Jose
HandyMan listing), now **confirmed by direct read** rather than inferred from index text.

**`w5-new-age-drywall-inc` (wave 5).** Profile page read directly (source 218): Excellent
4.9 (**237** reviews), **Hired 455 times**, current Top Pro **2021–2025**, background
checked, "License verified", 6 employees, 6 years in business, responds in ~2 hours,
"**Serves Redwood City, CA**", header ZIP 94063, payments by Apple Pay/Cash/Check/Venmo,
services including "Patch damaged drywall" and "Replace one or more sheets of drywall",
and review-topic counts **ceiling・29, patching・23, texture・17, hole・13**. Credentials
state "License type: **C9 – Drywall** / License state: CA / **License verified on
10/29/2020**" and a background check on Jaime Lombera — but **no CSLB licence number is
published anywhere in the retrieved text**, so no CSLB page could be read and
`license` stays `null`. Four reviews attached:

- **R91 Colin I.** — "A great licensed pro! Did a great job patching the drywall hole in
  the **bathroom ceiling** and texturing it to match the surrounding areas. They did not
  paint and were upfront about this." The most task-adjacent drywall review in seven waves.
- **R92 Tuan T., Jan 8 2026** — "…patching a ceiling **our plumber had to cut into** to fix
  a leak." Dated, marked "Hired on Thumbtack", and it is the two-trade sequence this job
  would follow.
- **R93 Ray P.** — ceiling drywall repaired, trim nailed back unprompted.
- **R94 Winston P.** — written by a reviewer who patches drywall for a contractor himself;
  "probably the cleanest drywaller I've ever worked with".

`trade` → drywall; `area` narrowed `sf` → `outside` because the direct read states a
Redwood City home market (the business does appear in both SF category pages read
directly, so SF work is plausible but unproven); a `gap` flag records that the platform's
"License verified" badge carries a **2020** date and is not a CSLB status check.

**`w5-figs-drywall-repair-paint` (wave 5).** Review R95 (Allison S. — "an old apartment
with thin, crumbly drywall … repairing a small hole and went so far as to reiforce it",
sic) plus the profile URL published beside it: **`/id/boise/handyman/figs-drywall-repair/`**
— **Boise, Idaho**, under the handyman category, on a San Francisco drywall-repair page.
The listing name is also "Figs Drywall Repair", **without** the "& Paint" the wave-5 record
stored. Area → `outside`, `discrepancy` flag, gaps rewritten to ask whether this is a San
Francisco business at all.

**`w5-maga-a-time-handyman` (wave 5).** Review R96 (Priyam m. — small drywall repair
finished as promised, repeat intent) and profile URL `/ca/san-francisco/handyman/`. A
`notice` flag records that the platform files it under **handyman**, not drywall, and that
a handyman category is not a CSLB classification: in California work over $500 in combined
labour and materials requires an appropriate licence, and none was published or read.

**`w5-walty-handy-service-pro` (wave 5).** Review R97 (Erika M. — drywall patching, "for a
client of mine") and profile URL **`/ca/san-pablo/moving-companies/walty-handy-service-pro/`**
— San Pablo, Contra Costa County, filed under **moving companies**. Area → `outside`,
`discrepancy` flag, and the analysis records that the reviewer is relaying a job done for
a client rather than describing their own home.

**Call-order renumbering.** With Caledonia removed, calls 06–09 were renumbered so the
order stays contiguous: Building Efficiency Inc 07→**06**, Faherty Plumbing and Heating
08→**07**, De Barra Plumbing 09→**08**, and wave 7's Michael Kuenzli Plumbing Co 10→**09**.
The strict admission basis for calls 06–09 is unchanged (an active licence whose CSLB page
itself records a 94122 address, holding the classification its trade requires).

## 10. New irregularities recorded this wave

1. **Two new non-active CSLB statuses** — `inactive` (661818 Ehrich's Plumbing, 94122,
   C36, expiry date 12/31/2026 still in the future) and `revoked` (734011 MidMarket,
   B-only, with **complaint disclosure information** and a 01/15/2008 reissue to another
   entity). An `inactive` licence with a future expiry is a distinct trap: the date looks
   current while the status says the holder cannot contract. Both are held, and the site's
   badge text now names all five non-active statuses.
2. **A bond dated after the licence expired** — 716856 Alpine: licence expired 12/31/2021,
   contractor's bond effective 01/01/2023 and cancelled 04/28/2023.
3. **Multi-name licence histories** — four licences whose registry firm names differ from
   the CSLB licensee (§7), including one active C36 (723992) spread over two names and four
   ZIPs.
4. **Out-of-state and out-of-category profile paths inside San Francisco result sets** —
   Figs (`/id/boise/`, Idaho) and Walty (`/ca/san-pablo/moving-companies/`). A category
   page's inclusion of a pro is not evidence the pro serves that city.
5. **A directly-read negative review on a shortlisted record** — Caledonia (§9), plus
   Thumbtack's own "this pro can't do your job" response for the profile's stated ZIP.
6. **A negative review alleging unlicensed work** — Elite Solution Will Team (R88, Valerie
   H.): work "without a proper license", **no moisture testing** on water-damaged material,
   a "cosmetic cover-up" over unprepped surfaces, refusal to return, and the customer hiring
   a licensed **C-9** contractor to strip and redo it. The record is held; a `gap` flag
   notes that no CSLB number was published on the profile, so the licensing allegation
   could be **neither confirmed nor refuted** from official records in this pass.
7. **A confirmed review mis-attribution in the existing dataset** — wave 6's R60 (§9).
8. **Platform credential dates that predate the read by years** — New Age Drywall's
   "License verified on 10/29/2020".
9. **A rating distribution that hides a serious allegation** — Caledonia is 93% five-star
   of 56 with 2% one-star; the one-star review is the one describing refused corrections in
   a bathroom. Averaging it away would have been the wrong call, and the record says why.

## 11. Carried-forward irregularities (unchanged, still on the records)

Wave 4's Repipe Champions identity mismatch (#1057927), the SAFENEST / Mike's Water Damage
index-text bleed, wave 6's Gorman Pipeline A-only scope exclusion and R S Dynamic Builders
B-only booking hold, the two wave-6 bond suspensions, `kenneth-asire`'s http:// website,
and every expired record from waves 1–5 all remain on their records and still render as
holds. Nothing was quietly re-classified to make this wave's numbers look better.

## 12. Admission result

**The qualified master list is still empty: 0 of 351.**

| Count | Value |
| --- | --- |
| Discovery records | **351** across 7 waves (50/50/51/50/50/50/50) |
| Evidence sources | **221** (ids 1–221, all with URL, retrieval mode and checked date) |
| Review excerpts | **98** (4 marked `negative`) |
| Distinct CSLB licence numbers read directly | **70** |
| Records with an active licence | **41** |
| Records with a non-active licence | **28** (expired, canceled, suspended, inactive, revoked) |
| Records held or excluded | **36** |
| Registry-only records (licence never read on CSLB) | **36** |
| Active licence **+** regulator-recorded 94122 address | **14** |
| Diagnostic call order | **9 calls**, 01–09, contiguous |

New call 09 — **Michael Kuenzli Plumbing Co** (#576600): active **C36**, CSLB address
**1234 21 Avenue, 94122**, issued 09/06/1989, expires 09/30/2027, bond $25,000 effective
08/22/2025 with no cancellation, workers' compensation exempt with no employees, and 66
plumbing-permit rows at the same address in the City's own registry. Admitted on the same
strict basis as calls 06–08, and admitted **without** a review, a website or a
seized-overflow case: long tenure on older San Francisco housing is plausible from the
1989 issue date and the permit history but is **not proven**, and the record says so in its
own gaps.

The five promotion gates are unchanged, and no gate was relaxed to admit anything this
wave. Missing information was recorded as missing: 282 records have no regulator read at
all, and not one record in seven waves proves successful extraction of this exact seized
mechanism without opening a wall.

## 13. Reproduction

```bash
python3 scripts/gen_wave7.py            # writes data/wave7.json (50 records, 21 sources, 20 reviews)
python3 scripts/merge_wave7.py          # merges it into data/research.json (idempotent)
python3 scripts/patch_wave7_attaches.py # attaches the follow-up reads to 7 pre-existing records
npm test                                # 24 assertions in two files
npm run test:monitor                    # 8 read-only source-monitor tests
```

Both scripts are fail-closed and refuse to run out of order: the merge aborts if a
wave-7 id already exists, if a name or licence number collides with any of the 301
pre-existing records, if a licence is not sourced from a `cslb.ca.gov` page, if an active
licence is expired relative to its check date, if a non-active licence has no hold flag, if
a trade is not supported by the licence's classes, if a source uses a kind or access value
outside the published vocabularies, if a review quote reaches 500 characters, or if the
compliance block would change by even one byte. The patch aborts if sources 218–221 or
reviews R89–R98 already exist, and re-asserts the whole invariant set before writing.

Licence pages must be fetched by typing the literal CSLB URL
(`https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=<number>`).
Rewritten or proxied URLs fail signature validation and were discarded, not retried.
