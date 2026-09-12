# Wave 9 discovery log — 2026-09-12

Fifty new research records, split into two evidence tiers **on purpose**, plus
three additional verification passes (Pass 19, 20, 21). Nothing in this wave was
promoted: the qualified master list is still empty, and all 50 records still
fail at least one gate.

Artifact: `data/wave9.json` (50 businesses, 47 sources, 7 review excerpts).
Generators: `scripts/gen_wave9.py` → `scripts/merge_wave9.py`.
Source IDs 306–352. Review IDs R122–R128. Dataset after merge: 451 businesses,
352 sources, 128 reviews, 137 distinct CSLB licence numbers read directly.

---

## 1. Why this wave looks different

Waves 6–8 each read a CSLB detail page for every record they stored. Wave 9
could not do that for 50 records inside one research session: each CSLB page
costs a full page read of heavy boilerplate, and the binding constraint was
verification depth, not candidate supply. Rather than read 50 pages shallowly or
invent facts for the ones not read, the wave was split:

| Tier | Records | What was read | What the record asserts |
| --- | --- | --- | --- |
| 1 — `cslb_read` | 17 | CSLB `LicenseDetail.aspx` opened directly, transcribed field by field | legal entity, form, address, phone, issue/expiry, status text, every classification, bond, workers' compensation, liability lines, Additional Status |
| 2 — `registry_only` | 33 | City open-data registries only | a recorded firm name, address, phone, licence **number** and permit identifiers — and nothing else |

Tier-2 records carry `license: null` and a new trade value, `registry-lead`
("Registry lead · classification not read"). That value requires no CSLB class,
so `licenseSupportsTrade()` returns false and `mayPromote()` can never be
satisfied: a registry lead is structurally incapable of reaching the master
list. Each tier-2 record repeats the caveat three times — in `areaText`, in a
`gap`-level flag, and in the plain `gaps` list — so no view of the data can
present it as a credential.

Three candidates shortlisted for a tier-1 read were not read in this session
(319594, 449998, 812877). 812877 was retained as a tier-2 registry lead; the
other two were dropped entirely rather than stored without evidence.

---

## 2. Discovery channels (all official, all queried directly)

Discovery ran **from permits to contacts**, the reverse of wave 8's direction,
so the cohort is anchored on completed work inside ZIP 94122 rather than on
firm addresses alone.

| Source | Dataset | Query intent |
| --- | --- | --- |
| 306 | `k6kv-9kix` Plumbing Permits Contacts | every licence with a firm address in ZIP 94122, grouped by licence, newest permit rows first |
| 307 | `i98e-djp9` building permits | completed 94122 permits whose description names drywall, sheetrock, gyp, ceiling, plaster or stucco |
| 308 | `a6aw-rudh` plumbing permits | completed 94122 plumbing permits, recent window (completed on/after 2025-06-01) |
| 309, 310 | `3pee-9qhc` Building Permit Contacts | contact join for the drywall-scope permits, in two batches |
| 311 | `k6kv-9kix` | contact join for the recent completed plumbing permits |
| 312 | `3pee-9qhc` | contractor contacts whose own firm ZIP is 94122 |
| 313–315 | `k6kv-9kix` | permit numbers for tier-2 licences, three small batches |
| 316 | `k6kv-9kix` | firm-address confirmation for the two licences whose CSLB page itself reads 94122 |

Two operational notes, recorded so the next wave does not repeat them:

* Wide contact joins get consumed by a single prolific firm. One five-licence
  query returned nothing but rows for licence 1039289 (Sunset Builders, 2309
  Noriega St), so batches were cut to three or four licences and re-run.
* Permit-number lookups for 1070527, 1079148 and 1084921 were truncated twice
  by the row limit. Those three were excluded from tier 2 rather than stored
  with a firm name and no supporting permit rows.

There is still no official CSLB bulk API or public REST endpoint (re-checked by
search this session); licence facts come from `cslb.ca.gov` pages one at a time.

---

## 3. Candidate screening and rejections

73 candidates survived the initial joins. Each was screened against all 401
stored records on normalized name, `core_name` (suffix-stripped), normalized
phone and licence number, and against the other wave-9 candidates.

Rejected before any page was read — identity already stored:

`119642, 329444, 343610, 410681, 410861, 440780, 486546, 533324, 536715,
595176, 969667, 983658, 1054611, 1055209, 1081386, 832092`

Rejected on a near-name (`core_name`) collision:

* `1070193` — core name already stored.
* `1024720` Peters Design-Build — core name already stored; substituted by
  `1027247` Richbay Construction.

One overlap was **kept and documented** instead of rejected (see §6, item 4):
CSLB licence 1112261 shares an address and a phone with stored registry-only
record `w6-c-t-construction-plumb`, which carries a *different* licence number
(533324) that has never been read on CSLB. Both readings are published and
cross-referenced; neither is assumed to be the contracting party, and no record
was merged or deleted.

---

## 4. Tier 1 — the 17 CSLB pages read directly

Source IDs 317–333 follow `VERIFIED_ORDER` in `scripts/gen_wave9.py`; 334 is the
complaint-disclosure page for 1017991.

| # | Licence | Entity as printed by CSLB | Status | Classes | CSLB address | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1140051 | AMERICAN PLUMBING AND TRENCHLESS LLC | active | C36 | Vallejo 94589 | 317 |
| 2 | 830368 | GARZAC PLUMBING | active | C36 | Hayward 94545 | 318 |
| 3 | 786183 | SMELLY MEL'S PLUMBING INC | active | A, C36, B, C16 | South San Francisco 94080 | 319 |
| 4 | 1051988 | YU PLUMBING INC | active | C36 | Daly City 94014 | 320 |
| 5 | 1097098 | H&J PLUMBING INC | active | C36 | Daly City 94014 | 321 |
| 6 | 1140843 | DISCOUNT PLUMBING ROOTER SERVICES LLC | active | C36, A | Burlingame 94010 | 322 |
| 7 | 1026009 | SPEEDY SERRANO PLUMBING | active | C36 | Pacifica 94044 | 323 |
| 8 | 1013565 | INNOVATION PLUMBING AND ROOTER | active | C36, B | San Francisco 94110 | 324 |
| 9 | 1112261 | CT PLUMBING & FIRE PROTECTION | active | C36, C16 | **San Francisco 94122** | 325 |
| 10 | 341277 | COIT CONSTRUCTION | active | B, C36 | San Francisco 94110 | 326 |
| 11 | 1017991 | SAN FRANCISCO REMODEL | active | B | Richmond 94803 | 327 + 334 |
| 12 | 1120735 | KNB TILE AND STONE INC dba KNB REMODELING | active | **B-2**, B | San Carlos 94070 | 328 |
| 13 | 1002370 | CHARLES LAKAMP | inactive | B | Sonora 95370 | 329 |
| 14 | 1028917 | EURO PLUMBING INC dba GENERAL CONTRACTOR | expired 2021 | B (no C36) | San Francisco 94108 | 330 |
| 15 | 658767 | EURO PLASTERING | expired 2000 | C35 | **San Francisco 94122** | 331 |
| 16 | 373337 | LAM PUI ELECTRICAL & PLUMBING INC | expired 2010 | B, C10, C36 | San Francisco 94116 | 332 |
| 17 | 342141 | LEE'S PLUMBING CO | expired 1997 | C36 | San Francisco 94118 | 333 |

Twelve active, five non-active. Every non-active licence is held, not hidden.

**Only two records earned the `outer` area label** (1112261 and 658767), because
only for those two does the regulator itself — not a directory, not a permit —
place the business inside ZIP 94122, and the City registry agrees. Everything
else is `sunset`: a completed 94122 work location, which is historical local
scope and not a dispatch promise.

Four licences hold both plumbing and building classifications on one licence
(786183, 1013565, 373337, 341277). That is the pattern this project actually
needs, and none of the four is promoted: 1013565 is held on its only public
review, 373337 expired in 2010 and was reissued to another entity, and the
other two have no retrievable customer review at all.

---

## 5. Tier 2 — the 33 registry-only leads

Nine came from the plumbing-permit registry filtered on firm ZIP 94122 (with
permit numbers confirmed by a second query), nine from the recent completed
plumbing-permit contact join, and fifteen from the completed building-permit
join where the printed scope names drywall, sheetrock, ceiling or plaster work.

Firm ZIP 94122 (sources 306 + 313–315): 1015230 Buteo Builders · 1016488
Kilb's Construction · 1018406 Jones Bros Construction & Design · 1021221 Kevel
Home Performance · 1024196 Wnc Construction · 1027247 Richbay Construction ·
1033146 Block 12 Construction · 1039289 Sunset Builders · 1047605 Sunset
Remodeling And Design.

Plumbing-permit join (sources 311 + 308): 1106329 Excalibur Water Heaters ·
1059891 Zhongwei Construction · 960561 Chl Construction Company · 893710 Elux
Construction · 805968 Flmc Development Corp dba Adamo Campagna · 1113396 Anova
Build · 872779 All Bay Cities Construction · 1059074 Vij Construction · 851213
328 Construction.

Building-permit join, drywall/ceiling scope (sources 309/310 + 307): 1108989
Gagne Rossie Enterprises · 752768 Zhou's International · 1035618 Gendros
Construction · 812877 Sean M O'Reilly · 1087651 All Property Tech · 1106767
Wtam Builder · 1020870 Zamora Construction · 1004147 Kevin Lin Construction ·
1111917 Mars Construction And Remodeling · 1111133 Boman Design & Construction ·
613489 Lin's Builder · 1101204 Csq Inc · 1078252 Plus One Construction · 685246
David Rodriguez Construction · 1114615 Blue Sky Building.

Eight of these rows carry no phone number in the registry (`phone: null`,
`phoneSource: null`) and say so in a flag: no contact channel is established by
this research.

The most on-point permit scopes found in tier 2, quoted as printed:

* 202603127447 (812877) — "replace dryrot framing and drywall inside unit … all
  work is interior."
* 202408027842 (1106767) — "remove interior drywall in living room & insulate …
  replace drywall w/ 5/8".
* 202501228824 (1108989) — "interior demolition for fire/water damage
  mitigation: plaster, drywall, flooring. replacement by others."
* 202512051101 (1111133) — a bathroom remodel replacing toilet, vanity and
  shower "using existing electrical & plumbing, in kind", the closest published
  analogue in this wave to like-for-like fixture repair.

---

## 6. Irregularity register

Every item below is published as a flag on its record with the source that
showed it. Fifteen are `discrepancy`, seven are `hold`.

1. **Admonishment letter on an active licence.** 1017991 San Francisco Remodel:
   the licence page carries an Additional Status line pointing to complaint
   disclosure; the disclosure page (source 334) lists Complaint # N A 2025 2297,
   dated 06/23/2026, status **LETTER OF ADMONISHMENT ISSUED**. CSLB's own
   disclaimer — a listed complaint is only an allegation of a probable violation
   and does not affect licence status — is reproduced on the record. Recorded as
   an allegation, never as a finding.
2. **One review, 1.0 stars, text unreachable.** 1013565 Innovation Plumbing and
   Rooter is the strongest trade match verified in this wave (active C-36 **and**
   B, with completed 94122 permit 202510288289 whose printed scope combines new
   drain and water lines with "replace a section of drywall apprx. 2x4'"). Its
   only public review is a single 1.0-star Yelp entry on an unclaimed listing,
   and the review text, date and author could not be retrieved in this
   environment. The record is **held**, and no review is attached — an
   unreachable review is never paraphrased into existence.
3. **Plumbing-scope permits without C-36.** Three licences appear on City
   plumbing or plumbing-scope permits while CSLB shows no C-36: 1028917 (B only,
   expired 2021-07-31, bond cancelled 2022), 1017991 (B only, active) and
   1120735 (B-2 + B, active, on a tub-replacement permit). Each record states
   that pipe work requires identifying a properly licensed plumbing contractor.
   Wave 8 had rejected 1028917 for a name mismatch; wave 9 opened the page and
   resolved it, so it is stored as a documented hold rather than dropped.
4. **One address and phone, two licence numbers.** CSLB reads 1112261 CT
   PLUMBING & FIRE PROTECTION at 1847 48th Ave, San Francisco 94122, phone
   (415) 203-7178. The City registry stores the same address and phone for
   "C T Construction & Plumb" under licence **533324** (234 permit rows), which
   has never been read on CSLB. 1112261 was issued 2023, which is consistent
   with a re-licensing, a shared office or a registry error — all three remain
   open. This is the wave's only permitted phone overlap; the merge gate accepts
   it **only** if the record carries a `discrepancy` flag and a `Relationship`
   claim naming `w6-c-t-construction-plumb`, and the test suite enforces both.
5. **Registry phone versus regulator phone (4 conflicts).** 786183 registry
   650-738-2030 vs CSLB (415) 758-6237 · 1097098 registry 415-819-8126 vs CSLB
   (510) 388-8126 · 1140843 registry 650-991-2164 vs CSLB (650) 991-2100 ·
   1028917 registry 415-509-9527 vs CSLB (415) 509-9577. The CSLB reading is
   stored; the registry reading is flagged.
6. **Six registry spellings of one licensee.** 373337 appears in the 94122
   registry rows as Lam Pui / Pui Lam / Lam Pui Elec And Plumbing / Lam Pui
   Electrical & Plbg / Lam Pui Electrical & Plumbin / Pui Lam Electrical, while
   CSLB's legal name is LAM PUI ELECTRICAL & PLUMBING INC at 94116. The page also
   shows Reissue Date 04/06/2006 and "LICENSE REISSUED TO ANOTHER ENTITY", so
   the number no longer identifies the original contractor. Expired 2010 → held.
7. **Registry name does not match the regulator.** 342141 is stored in the
   registry as "L & L Plumbing Inc." with a 94122 address, but the CSLB licensee
   is LEE'S PLUMBING CO at 217 Willard North, 94118, expired 1997-09-30, with
   "no workers comp information found for this license". Published as-read and
   left unresolved.
8. **Three ZIP variants on one active multi-trade licence.** 341277 Coit
   Construction: CSLB 94110 (2180 Bryant St 212), plumbing registry 94122,
   building-permit contact row and BuildZoom 94114 (763 Noe St).
9. **Workers' compensation cancelled the day before the check.** 830368 Garzac
   Plumbing reads active, but State Fund policy 9242676 shows CANCELLATION DATE
   09/11/2026 — one day before this research date. Held, matching the wave-8
   precedent for coverage that lapses on or before the check date.
10. **Directory name misspelling and a same-address inactive entity.** BuildZoom
    prints 1051988 as "Yu Pluming Inc" and links an inactive "Y&L Plumbing Inc"
    (licence 1041444, expired 2018) at the same 148 San Diego Ave address. The
    misspelling is treated as an error, and **no record was created for
    1041444** — an inactive same-address entity is an entity-confusion risk, not
    a candidate.
11. **Registry annotations left unresolved by the City.** 1016488 is printed as
    "Kilb's Construction Inc\*\*\*Check Id\*\*\*"; 1033146 carries two firm names
    ("Block 12 Construction" and "Shaun Ryan Construction"); 1111133 is printed
    as "Boman Deign & Construction Inc". Each is flagged as a discrepancy and
    the registry string is quoted as-read in the claim excerpt.
12. **Trade coverage contradicted in both directions.** 1021221 Kevel Home
    Performance sits on five plumbing and water-heater permit rows in the City
    registry, while its Yelp categories are HVAC, energy and insulation. Two
    Yelp snapshots also disagree on whether the listing is claimed. No CSLB page
    was read, so the record asserts neither plumbing nor drywall capability.
13. **A third-party "Google" score that could not be confirmed.** A directory
    restates 4.8 of 5 from 243 Google reviews for Smelly Mel's. It is stored as
    an unverified third-party claim and is never rendered as a Google rating.
    The same page was useful for one thing only: it prints (415) 758-6237,
    matching CSLB exactly, which supports the review identity match.
14. **B-2 is a real classification this schema did not have.** 1120735 holds
    B-2 Residential Remodeling plus B. `ALLOWED_CLASSES` in `lib.js` gained
    `"B-2"` rather than mapping it onto B, because a residential-remodelling
    licence does not carry the same scope as a general building licence.
15. **Star value contradicts review text.** The retained HomeAdvisor review from
    Michael N. (October 2009, $10,000 band) displays **1.0 of 5** while its text
    reads as satisfied apart from cleanup delays, and the extract ends
    mid-phrase. Both the star value and the words are preserved exactly as
    published, the review is marked negative so the signal is not suppressed,
    and the mismatch is flagged on the record.

---

## 7. Review evidence: attached versus refused

Seven excerpts were attached (R122–R128). Everything else found was refused.

**Attached — identity established, text attributable:**

* R122–R124, Smelly Mel's Plumbing Inc (786183), HomeAdvisor rated page
  (source 338): Gordon M. 5.0 (Oct 2010, ~$5,000) on a main sewer line and full
  drainage-pipe replacement; Bill H. 4.0 (Aug 2010, ~$5,000) crediting named
  diagnostic knowledge; Michael N. 1.0 (Oct 2009, ~$10,000) with the mismatch
  above. Identity matched on exact corporate name, South San Francisco
  location, and the CSLB phone appearing on an independent directory page.
  `published` is `null` for all three: the platform shows month and year only,
  and no day was invented.
* R125–R127, Kevel Home Performance (1021221), Yelp (source 343): David K.
  (work carried out while tenants were in place), Chris Y. (workmanship care),
  Abby D. (energy audit and upgrades). Identity matched on the Yelp listing's
  own 3624 Ortega St 94122 address and (415) 213-5545 phone, both identical to
  the City registry row for this licence.
* R128, Kevel Home Performance, Angi (source 344): Ian H., 5.0, June 2014 —
  whole-house fan, attic exhausts and insulation. Twelve years old, and it
  describes ceiling and attic work rather than plumbing or drywall patching.

**Refused, with the reason recorded on the source:**

* Yelp 4.5 stars from ~1,300 reviews for Discount Plumbing Rooter Services
  (source 337): the only reachable review text is JSON-LD photo-caption
  metadata. Caption metadata is quarantined as a source, never converted into a
  review. The aggregate is reported; no excerpt is attached.
* Yelp 1.0 star for Innovation Plumbing (source 335): text, date and author
  unreachable. Aggregate reported, record held, nothing attached.
* BuildZoom profiles for Coit Construction, Yu Plumbing and H&J Plumbing
  (sources 340–342): each states the profile "hasn't received any reviews".
  Absence of reviews is stored as a `gap`, never as a neutral or positive
  signal. Their permit JSON-LD was used only to corroborate addresses.
* Thumbtack category pages (sources 345–347): a bathroom-ceiling patch with
  texture matching, a customer describing a pro "installing a panel for a hole
  in our ceiling", and one pro's JSON-LD aggregate (4.677 of 5 from 31). None
  can be tied to a wave-9 licensee, so all three remain sources.
* Reddit threads (sources 348–352): four are directly on-task for the repair
  itself — a stuck trip lever where penetrating oil and steam failed and the
  work "went thru the drywall"; access "from behind and below" through a
  downstairs neighbour's ceiling with galvanized rust debris and an endoscope
  inspection; a 1940s tub with an odd 1⅜ inch pipe; and a reply framing the
  patch as "sheetrock isn't hard". The fifth is San Francisco pricing and
  marketplace behaviour. **None names a business**, so none became a review.
  They are the strongest task evidence in this wave and the weakest business
  evidence, and they are labelled that way.

Aggregate scores are never blended across platforms, negative claims stay
allegations, and no business-hosted testimonial appears in this wave.

---

## 8. The three additional verification passes

**Pass 19 — regulator pass.** Seventeen CSLB detail pages opened directly and
transcribed field by field, including bond, workers' compensation and liability
lines and every Additional Status line. Five licences found non-active. The
complaint disclosure behind 1017991 read as a separate page. Every licence
number the City registry returned but that was not read is published as a lead
with `license: null` and trade `registry-lead`.

**Pass 20 — cross-source pass.** Registry identity compared with regulator
identity field by field, producing the fifteen discrepancy flags in §6: four
phone conflicts, six registry spellings of one licensee, a 2006 reissue to
another entity, three ZIP variants on one active multi-trade licence, and one
address plus phone shared by two different licence numbers. Public directory
pages checked for review corpora. Unattributable Thumbtack and Reddit extracts
quarantined as sources. CSLB class B-2 discovered and added to the schema
instead of being mapped onto B. Review identity re-checked: every attached
excerpt is matched by exact name plus address or phone against a regulator or
City row, and `published` stays `null` wherever only a month and year exist.

**Pass 21 — fail-closed qualification pass.** No record promoted; the master
list stays empty; the nine-call diagnostic order is unchanged. Holds raised for
expired and inactive licences, for a workers' compensation cancellation dated
before the research date, and for a single unreachable 1.0-star review.
Public-data privacy scrub re-run over every artifact (one draft phrase was
rejected by the fingerprint scan and rewritten). Structural, render and browser
test suites updated and re-run; the merge was verified idempotent.

---

## 9. What wave 9 does not claim

* No record proves a seized bathtub overflow trip lever was freed without
  opening finishes. Not in tier 1, not in tier 2.
* No record proves a small ceiling opening was finished as a reusable access
  hatch. The closest published scopes are a 2×4-foot drywall section
  replacement (1013565) and interior drywall replacement after water damage
  (812877, 1108989).
* A completed 94122 permit is historical local scope. It is not present
  dispatch, not availability, and not a minimum-job-size commitment.
* A registry licence number is a lead. Thirty-three of them are published in
  this wave with no status, no classification, no entity and no expiry.
* Displayed insurance and bond lines are recorded as displayed. None was
  confirmed with an insurer for this project.
* Seven review excerpts are not a review corpus. Four of the seven describe
  energy, sewer or attic work rather than anything resembling this job.

## 10. Reproducing this wave

```bash
python3 scripts/gen_wave9.py     # rebuilds data/wave9.json, runs a collision pre-flight
python3 scripts/merge_wave9.py   # fail-closed merge; idempotent on re-run
npm test                         # 29 dataset + render invariants
npm run test:monitor             # source-monitor unit tests
npm run test:browser             # Playwright (CI installs Chromium; needs network)
```

The merge refuses source, name, phone, licence, review, classification, date,
privacy or qualification drift instead of repairing ambiguous input. The single
accepted phone overlap is gated on the record publishing it.
