# Wave 10 discovery log — 2026-09-12

Fifty new research records in three published evidence tiers, plus ten
verification upgrades and two registry upgrades applied to records earlier waves
had already stored. Three additional verification passes (Pass 22, 23 and 24)
were run. Nothing in this wave was promoted: the qualified master list is still
empty, and all 50 records still fail at least one gate.

Artifact: `data/wave10.json` (50 businesses, 48 sources, 5 review excerpts,
10 verification upgrades, 2 registry upgrades, 33 dedupe rejections).
Generators: `scripts/gen_wave10.py` → `scripts/merge_wave10.py`.
Source IDs 353–400. Review IDs R129–R133. Dataset after merge: **501 businesses,
400 sources, 133 reviews, 10 waves, 170 distinct CSLB licence-detail reads**.

---

## 1. Why this wave has three tiers

Discovery opened **33 CSLB licence-detail pages** directly. Twenty-three of those
licences belonged to businesses no earlier wave had stored, and became tier-1
records. Ten resolved to a business already in the corpus, so instead of minting
a duplicate the regulator reading was published as a **verification upgrade** on
the stored record — including the one case where the reading contradicted the
record's declared trade (Ren Lei Construction, licence 635360, which holds B
only; the stored trade was corrected to `general`). Two City registry rows
behaved the same way and became **registry upgrades**. Upgrades are published
separately and are never counted toward the 50.

| Tier | Records | What was read | What the record may assert |
| --- | ---: | --- | --- |
| 1 — `cslb_read` | 23 | CSLB `LicenseDetail.aspx` opened and transcribed field by field | legal entity, business form, address, phone, issue and expiry dates, status text, every classification, bond, workers' compensation, liability lines, Additional Status |
| 2 — `registry_only` | 22 | City open-data permit registries only | a recorded firm name, address, phone, licence **number** and permit identifiers — nothing else |
| 3 — `platform_listing` | 5 | A Thumbtack category page read directly | the listing's own category, hire count or review text, labelled as a platform claim |

Of the 23 tier-1 reads **15 are active and 8 are non-active and held**; across
all 33 pages read in this wave the split is 21 active and 12 non-active. No
non-active status is smoothed over: each carries a `hold`-level flag stating that
the licence cannot contract on that number at the check date.

Tier-2 records carry `license: null` and the trade value `registry-lead`
(“Registry lead · classification not read”). That value requires no CSLB class,
so `licenseSupportsTrade()` returns false and `mayPromote()` can never be
satisfied: **a registry lead is structurally incapable of reaching the master
list.** Each tier-2 record repeats the caveat in its area text, in a `hold`-level
flag and in its plain gap list.

Tier-3 records carry no licence at all — not even when the listing displays a
platform “Licensed pro” badge, which is a platform claim and not a CSLB read.

---

## 2. Discovery channels (all official, all queried directly)

| Sources | Dataset | Query intent |
| --- | --- | --- |
| 353–385 | CSLB `LicenseDetail.aspx` | 33 licence pages opened one at a time |
| 386 | `k6kv-9kix` Plumbing Permit Contacts | every licence with a firm address in ZIP 94122, grouped by licence, ordered by permit count |
| 387 | `3pee-9qhc` Building Permit Contacts | every `license1` whose own firm ZIP is 94122, grouped, ordered by permit count |
| 388 | `a6aw-rudh` plumbing permits | completed 94122 plumbing permits |
| 389 | `i98e-djp9` building permits | completed 94122 permits whose scope names drywall, sheetrock, gyp, ceiling, plaster or stucco |
| 390, 391 | Thumbtack category pages | drywall repair and plumbing listings near San Francisco, read directly |
| 392–397 | Reddit and trade-forum threads | the stuck trip-lever problem itself, as task evidence |
| 398–400 | BuildZoom, Yelp, Procore | identity probes on three records; the two false claims they carried were rejected (§7) |

There is still no CSLB bulk API; licence facts come from `cslb.ca.gov` one page
at a time.

---

## 3. Dedupe: 33 rejections, and the 12 that became evidence

Wave 10 re-mined two channels it had read before — the two City contact
registries and the Thumbtack category pages — so a large share of what it
surfaced was already stored. Thirty-three candidates were rejected as
duplicates; none was stored a second time. The 12 rejections that produced new
regulator or registry evidence became published upgrades instead:

| Stored record | Licence | Status | Classes | CSLB address | Source |
| --- | --- | --- | --- | --- | --- |
| `national` — National Plumbing | 619642 | active | C36 | 1472 24TH AVENUE, SAN FRANCISCO, CA 94122 |  |
| `sunny-plumbing` — Sunny's Plumbing Inc | 536715 | active | C16, C36 | 1786 35TH AVENUE, SAN FRANCISCO, CA 94122 |  |
| `w5-stan-plumbing` — Stan Plumbing | 410861 | suspended | C36 | 1429 9TH AVE APT 3, SAN FRANCISCO, CA 94122 |  |
| `chosen` — Chosen Rooter & Plumbing | 1054611 | active | C36 | 338 N CANAL ST STE 12, SOUTH SAN FRANCISCO, CA 94080 |  |
| `w7-franks-all-city-plumbing` — Franks All City Plumbing | 319594 | expired | C36 | 2560 TURNBERRY DRIVE, SAN BRUNO, CA 94066 |  |
| `w6-ren-lei-construction-co` — Ren Lei Construction Co | 635360 | active | B | 750 LAWTON STREET, SAN FRANCISCO, CA 94122 |  |
| `sberlo` — Sberlo Plumbing Inc | 487017 | canceled | C36 | 1663 12TH AVENUE, SAN FRANCISCO, CA 94122 |  |
| `w6-bill-bragg-plumbing` — Bill Bragg Plumbing | 440780 | active | C36 | 620A GUERRERO ST, SAN FRANCISCO, CA 94110 |  |
| `w7-david-chu-plumbing` — David Chu Plumbing | 343610 | inactive | C36 | 1530 29TH AVENUE, SAN FRANCISCO, CA 94122 |  |
| `cl` — C&L Plumbing Inc | 982738 | active | C36 | 1516 MORAGA STREET, SAN FRANCISCO, CA 94122 |  |

| `kh-construction` | 1079861 | 387 |
| `oshaughnessy` | 922762 | 386 |

The remaining rejections were platform and directory listings already in the
corpus, and none produced new evidence: Magaña Time Handyman, Aldana co, Jovel Quality painting, Honart, Fairfield Drywall Inc, Walty Handy Service Pro, Sandoval drywall, Lazarit Construction, Handyman Express, RoDidIt, Baruch handyman services, THWC home improvement, Savr Handyman, New Age Drywall Inc, Rock & Smooth Drywall, Dr. Drain Plumbing and Rooter, AMX Plumbing, Ocean Air Heating, Jones Bros Construction & Design Inc and Abe's Plumbing, plus one already-stored review
excerpt (Josael Reinosa, retained as R69 in wave 7).

---

## 4. Tier 1 — the 23 CSLB pages read directly

| Licence | Entity as printed by CSLB | Status | Classes | CSLB address | Source |
| --- | --- | --- | --- | --- | --- |
| 324708 | HAWK N LEE DESIGN & CONSTRUCTION COMPANY | active | A, B, C10, C36 | 1032 Irving Street #930, San Francisco, CA 94122 | 361 |
| 443478 | A & W CONTRACTORS | active | B | 1549 Noriega Street, San Francisco, CA 94122 | 375 |
| 486122 | PLUMBWORKS INC | canceled | C16, C36 | 494 Silver Ave Unit A, Half Moon Bay, CA 94019 | 354 |
| 486546 | WINSON WAH LAU | expired | B, C36 | 1346 26th Avenue, San Francisco, CA 94122 | 362 |
| 489739 | TILE ARTS INC | active | C54 | 63 Tamalpais, Fairfax, CA 94930 | 370 |
| 546425 | CONNOR DALY CORPORATION | active | B | 289 Bungalow Ave, San Rafael, CA 94901 | 372 |
| 586693 | LEE PLUMBING CO | active | C36 | 2407 21st Avenue, San Francisco, CA 94116 | 360 |
| 595176 | SNC PLUMBING & FIRE PROTECTION INC | canceled | C16, C36 | 1595 Fairfax Avenue Ste A, San Francisco, CA 94124 | 376 |
| 604689 | M F CONSTRUCTION | active | B | 1459 32nd Ave, San Francisco, CA 94122 | 368 |
| 652992 | MR ROOTER PLUMBING | expired | C36 | 30100 Town Center Dr Ste 0-425, Laguna Niguel, CA 92677 | 381 |
| 762214 | ORAN PLUMBING CORP | active | C36 | 95 El Plazuela St, San Francisco, CA 94127 | 358 |
| 782830 | BENJAMIN FRANKLIN PLUMBING | expired | A, C36 | 517 Jacoby Street Suite C, San Rafael, CA 94901 | 377 |
| 797580 | TERENCE MCMAHON CONSTRUCTION | active | B | 1400 Irving Street, San Francisco, CA 94122 | 371 |
| 803442 | A W CONSTRUCTION COMPANY | suspended | B | 1201-32nd Avenue, San Francisco, CA 94122 | 380 |
| 804459 | HAMMERHOUSE CONSTRUCTION INC | active | B | 19 Cerritos Avenue, San Francisco, CA 94127 | 385 |
| 834292 | BRENDAN WATERS CONSTRUCTION INC | active | B | 1382 7th Avenue, San Francisco, CA 94122 | 373 |
| 856173 | H Y CONSTRUCTION INC | active | B | 1774 8th Avenue, San Francisco, CA 94122 | 367 |
| 863410 | J & A STONE AND TILE INC | active | C29 | 3425 Gravenstein Highway South, Sebastopol, CA 95472 | 369 |
| 869710 | URBAN BUILDER GENERAL CONTRACTING INC | active | B | 1258 33rd Avenue, San Francisco, CA 94122 | 374 |
| 917101 | VECTOR CONSTRUCTION INC | inactive | B, C10 | 3618 Ortega St, San Francisco, CA 94122 | 379 |
| 917252 | SEDERAP'S DRYWALL INC | active | B, C-9, C10, C36 | 3469 Mission Street, San Francisco, CA 94110 | 384 |
| 943574 | JONES BROS CONSTRUCTION INC | canceled | B | 1879 35th Avenue, San Francisco, CA 94122 | 382 |
| 950725 | SAN FRANCISCO DESIGN BUILD | active | B | 1560 Great Highway, Apt 1, San Francisco, CA 94122 | 378 |

Notes:

- **Sederap's Drywall Inc (917252)** is the first licence in the corpus carrying
  **C-9 drywall and C36 plumbing together**, and it also holds B and C10. It is
  the wave's closest single-licence match to the project's two required trades,
  and it is held anyway: no review evidence was attributable to it and its
  registry address does not match the regulator's.
- **Hawk N Lee Design & Construction Company (324708)** is the only tier-1
  licence holding A, B, C10 and C36 at once, and CSLB places it inside ZIP 94122.
- Twelve tier-1 licences place the licensee at a 94122 address on the regulator's
  own page: 324708, 443478, 486546, 604689, 797580, 803442, 834292, 856173,
  869710, 917101, 943574 and 950725 — three of them (803442, 917101, 943574) read
  non-active.
- The remaining tier-1 active records are general-building or specialty licences
  with no C36, so they can support the drywall side of a scope claim but never
  the plumbing side.

---

## 5. Tier 2 — the 22 registry-only leads

Each row below is a City registry record: a firm name, an address, a phone and a
licence **number** — and nothing more. None of these licence numbers was read at
the regulator, so none of these records has a legal entity, a classification or
a status. Every one is held with the caveat repeated three times.

| Firm as recorded | Licence number | Registry location | Record |
| --- | --- | --- | --- |
| Macro Builder Inc | 797077 | 2121 19th Av, ZIP 94122 |
| Tony Tiejun Hu | 792165 | 1214 40th Av, ZIP 94122 |
| Danny Chen | 893929 | 1659 23rd Av, ZIP 94122 |
| D S Management Inc dba Metrocon Builders | 978867 | 2004 Irving St, ZIP 94122 |
| R C Construction Co | 747801 | 2037 Irving St #203, ZIP 94122 |
| W J L Construction Inc | 775086 | 1518 26th Av, ZIP 94122 |
| Jason Liu Construction Company | 662067 | 1495 40th Av, ZIP 94122 |
| Samco Construction Inc | 899541 | 1623 Noriega St, ZIP 94122 |
| Ireland Tile & Stone Inc | 897547 | 1558 39th Avenue, ZIP 94122 |
| D Construction Inc | 1024901 | 1726 45th Av, ZIP 94122 |
| Cht Properties Development | 812058 | 1449 Moraga St, ZIP 94122 |
| Z Construction Company Inc | 740407 | 1226 28th Av, ZIP 94122 |
| C G Adams Construction | 777558 | 1487 45th Av, ZIP 94122 |
| Ht Construction Company | 993020 | 1488 28th Av, ZIP 94122 |
| Nicholas Spencer Firth Gen Contr | 873895 | 1543 17th Av, ZIP 94122 |
| John Woo Construction llc | 765131 | 1326 11th Av, ZIP 94122 |
| J-T A C  Corp | 512826 | 1465 46th Av, ZIP 94122 |
| L.G. Construction Co.,Inc | 656193 | 1032 Irving St, ZIP 94122 |
| Chin Pang Construction Co | 442727 | 1526 40th Av, ZIP 94122 |
| Stewart Cheung Const | 362539 | 1277 41st Ave, ZIP 94122 |
| K A Lau Construction | 823195 | 1362 33rd Av, ZIP 94122 |
| X T Construction Co. | 608799 | 1875 19th Avenue, ZIP 94122 |

---

## 6. Tier 3 — the five platform listings read directly

| Record | Listing | Declared trade | Status | Review |
| --- | --- | --- | --- | --- |
| w10-sham | Sham | finish | hold | R129 |
| w10-repipe-specialists-san-francisco-bay-area | Repipe Specialists - San Francisco Bay Area | plumbing | research | R130 |
| w10-jose-garcia | Jose Garcia | plumbing | research | R131 |
| w10-century-build-group-inc | Century Build Group, Inc. | general | research | R132 |
| w10-canel-solutions | Canel Solutions | drywall | research | R133 |

A platform listing is evidence about the listing, not about a licence. The
“Licensed pro” badge Thumbtack prints for Repipe Specialists was refused as
licence evidence: no wave-10 platform record carries a licence, a classification
or a status. Sham's listing review is attributed to a generic platform account
and the business name is a single word, so its identity could not be resolved
and the record is held rather than presented as bookable.

---

## 7. Irregularity register

**Status contradictions (all held)**

- **Plumbworks Inc dba Chris Goodwin Plumbing (486122)** reads canceled at
  CSLB — while the City registry still lists 944 permit rows under the licence.
  It is the second-highest 94122 plumbing permit count found in this pass.
- **Stan Plumbing (410861)**, stored since wave 5 as an unread registry lead,
  now reads **suspended** for a contractor's-bond cancellation dated 09/01/2026,
  eleven days before the check date.
- **A W Construction Company (803442)** reads suspended for a
  workers'-compensation cancellation dated 02/18/2026; **Vector Construction
  Inc (917101)** was inactivated 08/17/2026 after its exemption was cancelled on
  08/07/2026 — both inside the month before this research date.
- **A & W Contractors (443478)** reads “current and active” while CSLB displays
  a bond **cancellation date of 09/30/2026**, eighteen days after the check.
  Recorded as a forward-dated hold, not as a current credential.
- **Sberlo Plumbing (487017)**, **SNC Plumbing & Fire Protection (595176)** and
  **Jones Bros Construction Inc (943574)** all read canceled; Jones Bros was
  dissolved by the Secretary of State on 01/30/2018 while the City building
  registry still lists 84 permit rows.
- Expired and inactive: **Winson Wah Lau dba W & J Plumbing Co (486546)**,
  **Mr Rooter Plumbing (652992)**, **Benjamin Franklin Plumbing (782830)**,
  **Franks All City Plumbing (319594)** and **David Chu Plumbing (343610)**.

**Identity conflicts between registry and regulator**

- **Lee Plumbing Co (586693)**: the registry name (“C W Lee Plumbing Company”,
  1650 34th Avenue) does not match the regulator's (“LEE PLUMBING CO”, 2407 21st
  Avenue), the phone digits are transposed (415-689-9323 against
  (415) 681-9323), and the licence was reissued to a family member in 2025.
  Recorded; not merged.
- **Oran Plumbing Corp (762214)**: registry name, address and phone all differ
  from CSLB, and the CSLB phone is the same number the registry stores against
  the earlier record held as “Francis John Burke”. The regulator resolves the
  overlap — the page names Francis John Burke as the qualifying individual.
- **Hawk N Lee**: the registry row sits at 1609 Noriega Street while CSLB prints
  1032 Irving Street #930 for the licence, and a separate P.E. registration
  (CE28526) shares the Noriega address.
- **Plumbworks**, **SNC**, **Mr Rooter**, **Hammerhouse (804459)** and
  **Connor Daly Corporation (546425)** each print a registry address in or near
  94122 while CSLB places the licensee outside San Francisco.
- Near-identical phone numbers: the registry phone for **Benjamin Franklin
  Plumbing** is one digit from the Judah Street number already stored against an
  unrelated licence.

**Scope contradictions**

- **J & A Stone and Tile Inc (863410)** holds C29 Masonry only and **Tile Arts
  Inc (489739)** holds C54 Tile only — neither can self-perform plumbing or
  drywall — yet the City registry records 88 and 78 plumbing-permit contact rows
  under them. Both are scope-excluded.
- **Ren Lei Construction (635360)**, **H Y Construction (856173)** and **M F
  Construction (604689)** hold B only, so they can support a drywall-side claim
  but not a plumbing one, however many plumbing-permit rows the registry carries.

**Registry data quality**

- Malformed phone strings appear throughout the City rows: “6811306”, “7863683”,
  “5501129”, “451-517-8123”, “451-225-8086”. The 451 values look like
  transposed 415 area codes, but a transposition is not a fact: the registry
  value is stored as printed and flagged.
- One City row annotates itself “Chin Pang Construction Co ***Check Id***” — the
  City's own unresolved-identity warning, preserved verbatim.
- One licence number carries two firm names and two street numbers across the
  two registries (747801: “R C Construction Co” at 2037 Irving St #203 and
  “C R Construction” at 1226 28th Av).

**Rejected third-party claims**

- A Yelp JSON-LD aggregate of 4.5 from 2,603 reviews belongs to a “Things to Do”
  search page, not to Sunny's Plumbing; discarded as a rating.
- A construction-network page prints +1 415-753-1618 for National Plumbing. The
  regulator's own page for licence 619642 prints (415) 310-4928; the directory
  value is rejected.
- A BuildZoom profile attaches licence 524327 to Sunny's Plumbing alongside
  536715. Only 536715 was read at the regulator; 524327 stays a directory-stated
  number and is never rendered as a licence.
- Thumbtack's “Licensed pro” badge is a platform claim and was refused as
  licence evidence.

---

## 8. Review evidence: attached versus refused

Five excerpts were attached, each to a wave-10 record with a platform source:

- **R129** — Sham, Thumbtack, drywall holes repaired on the customer's schedule.
- **R130** — Repipe Specialists (San Francisco Bay Area), Thumbtack: a customer
  describes walls and ceiling cut open for pipe access, visqueen sheeting used to
  protect the house, and the openings closed afterwards.
- **R131** — Jose Garcia, Thumbtack: short praise from a repeat customer; the
  record carries the platform's hire count, not a licence.
- **R132** — Century Build Group, Thumbtack: water damage and mould remediation,
  with the customer describing the process as easier than expected.
- **R133** — Canel Solutions, Thumbtack, drywall category: a wall and a ceiling
  that had been ripped out were rebuilt, insulated, textured and painted.

Every excerpt keeps `published: null` where the platform shows no day. Forum
threads in sources 392–397 stayed task evidence: they describe the stuck
trip-lever problem and what trade work it implies, and none names a business.

---

## 9. The three additional verification passes (Pass 22, 23, 24)

1. **Regulator pass (22)** — 33 CSLB detail pages opened directly and transcribed
   field by field, including bond, workers'-compensation and liability lines.
   Twelve readings resolved to stored records and became upgrades; eight of the
   23 new records came back non-active and were held.
2. **Cross-source pass (23)** — registry identity compared with regulator
   identity field by field, producing the discrepancy flags in §7 (phone, name,
   address and scope conflicts); directory false claims and platform badges
   refused; platform listings checked for review corpora and quarantined where
   attribution failed.
3. **Fail-closed qualification pass (24)** — no record promoted, the master list
   left empty and the nine-call order unchanged; holds raised for every
   non-active status, including two bond cancellations and one compensation
   cancellation dated inside the month before the check; the 33 duplicate
   rejections folded into ten verification upgrades and two registry upgrades;
   structural, render and browser tests re-run; merge verified idempotent.

---

## 10. What wave 10 does not claim

- It does not claim any business has been verified for the project, or that any
  registry or platform listing is a licence.
- It does not claim a licence status establishes exact-task experience, current
  insurance in force, or willingness to take the work.
- It does not claim any business will arrive at an Outer Sunset address: a
  registry or regulator address is a recorded location, not a dispatch promise.
- It does not turn a rating, a hire count or a badge into a credential, and it
  does not repeat private project context in any public artifact.

---

## 11. Reproducing this wave

```sh
git checkout -- data/research.json      # committed 451-record baseline
python3 scripts/gen_wave10.py           # rebuilds data/wave10.json, runs the collision pre-flight
python3 scripts/merge_wave10.py         # fail-closed merge; idempotent after success
npm test
```

The merge refuses on any source-id, name, phone, licence-number, review,
classification, date, privacy or qualification collision, and it is the same
gate that produced the 33 dedupe rejections above.
