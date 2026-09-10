# Wave-4 candidate pool (discovery log — Sep 10 2026, this session)

Wave 4 added **50 new discovery records** (201 total), **40 new sources** (ids 101–140)
and **19 new review excerpts** (R40–R58), followed by a license patch that attached
three of this session's direct CSLB reads to pre-existing entries and added one
company-published check-in excerpt (R59). Nothing was promoted to the qualified
master list (fail-closed; it remains empty).

## How candidates were found (real retrievals, this session)

Every name, rating sample, quote, address and phone in `data/wave4.json` appears
verbatim in a retrieval captured this session. Sources 101–105 and 139 are **direct
live page reads** (CSLB license detail pages and the Economy Plumbing site). Yelp,
Thumbtack, Reddit, Yellow Pages and Yahoo Local content is **indexed search extract**
(direct corpus access blocked) and is labeled as such on every claim.

Searched this session:
- Yelp plumbing pages for Outer Sunset / Sunset (several sorts, May–Sep 2026 extracts) → sources 107–112
- Yelp drywall/contractor/repair/handyman pages for SF and Outer Sunset → sources 113–118
- Yelp ceiling-leak / water-ceiling-leak pages for SF → sources 120–121
- Yelp business profiles (Sunset Handyman, SF Handyman Services, Mike's Water Damage, F&A, Legend, True-Tech) → 115, 118, 119, 136, 138, 140
- Thumbtack SF / South SF / 24-hour plumber pages → sources 122–125
- Reddit r/PlumberSanFrancisco top-10 thread + r/sanfrancisco handyman/plumber thread → sources 126–127
- Yahoo Local editorial best-plumbers list → source 128
- Yellow Pages SF plumber lists → sources 129–130
- Business sites: Heise's drain page (106), 5 Star repiping (131), Chosen repiping (132), Repipe Champions (133), Repipe Specialists SF (134), legendplumbingsf.com (135), economysf.com (139, direct read)
- CSLB direct license detail reads → sources 101–105
- "Access panel/hatch installer San Francisco" search: **no dedicated SF installer exists**;
  results are product suppliers (BAUCO, F.W. Webb, SupplyHouse). Hatch installation is a
  carpenter/handyman task — recorded here so the gap is explicit, not forgotten.
- Reddit r/AskSF+r/sanfrancisco Sunset threads: mostly neighborhood chatter; the two
  plumber threads above were the substantive sources. Pipeline/A-1/Ace recommendations
  there map to already-tracked entities.

## Categories carried (50)

- **Plumbing — directories (17):** True-Tech (San Jose — flagged), Legend Plumbing & Drain (SF 94117), F&A Plumbing & Rooter (Pacifica), Portola Plumbing Services (bathtub repair tag), Pham's, Marco's (name-collision flag), X-Ray, ASAP (SSF), Maverick Water Heaters, Wizard Plumbing & Drain (listicle — flagged), Economy Plumbing (direct site read), Integrity First Plumbing (**active C-36 attached**), San Francisco Plumbing Repairs (94122 storefront, brand-pattern flag), Gateway Rooter & Plumbing Inc, Urban Bay Engineering (name/scope flag), Absolute Sanitation Plumbing and Restoration, Plumbing Bay Area (name-collision flag).
- **Plumbing — repipe marketing (2):** Repipe Champions (license-mismatch **hold flag**), Repipe Specialists SF (franchise, hosted testimonials).
- **Plumbing — Thumbtack tradespeople (13):** Antonio Cárcamo Reyes' Plumbing & Rooter Service (745 hires, serves SF), Navta, Maximus, Ayala's, Bright Ideas, Dr. Drain, LGM, The Route To Your Problem, Alpha, Dom's, Costello's, JN and Son, Natan.
- **Drywall / finish (6):** A1 Drywall (ceiling-open quote), Paint Studio SF, Benjamin Shaw, Carlos' Painting & Handyman, Northwest Builders & Renovation (low-rating flag), Fullhouse Remodeling & Handyman.
- **Handyman (7):** Sunset Handyman (finish carpenter), Handyman Heroes (handyman+plumbing excerpt), Reasonably Honest Mike's, Handlify, Paul Woodford Services, Octavio Handyman, San Francisco Handyman Services.
- **Water damage / restoration (5):** Mike's Water Damage (SF, ceiling+drywall reviews), Dry Kings Restoration (Mission Bay), All Action Water Damage (Burlingame; upstairs-bathroom-through-ceiling quote), SAFENEST (index text-bleed flag), Max Restoration (SSF).

## Direct CSLB license reads — all five with outcomes

| # | Read on cslb.ca.gov 09/10/2026 | Outcome |
|---|---|---|
| 698806 | MAGIC PLUMBING dba MAGIC PLUMBING HEATING & COOLING, SF 94114 — active, C36+C20, exp 03/31/2027 | **Matches existing `magic` entry** → attached; 415-441-2255 |
| 954813 | 24/7 ROOTER AND PLUMBING SERVICES INC dba A & R PLUMBING, SF 94124 — active, C36+D56+A, **exp 11/30/2026** | **Matches existing `rooter-247`** → attached + expiry notice |
| 876212 | A B PLUMBING, **12909 Skyline Blvd, OAKLAND 94619** — active C36, exp 04/30/2028; bond cancellation 10/03/2026; no-employees WC exemption | **Matches existing `ab`** → attached + base/bond flags |
| 1006178 | INTEGRITY FIRST PLUMBING INC, 1485 Bayshore Blvd, SF 94124 — active C36, exp 08/31/2027 | **Matches new entry `integrity-first`** → attached |
| 1057927 | **ORTEGA'S BAY AREA GENERAL CONSTRUCTION INC, Hayward — B (General Building), not C-36** | **FAILED match to Repipe Champions marketing** → hold flag, not attached |

A sixth read (1024971, Fast Response) re-validated the wave-1 record: still current and
active, C36, exp 03/31/2027 — consistent with the existing dataset; counted as a
re-validation, not a distinct new license fact. **Distinct CSLB reads across the
project now total 36 (31 waves 1–2, 5 wave 4).**

License numbers came from public claims found this session (Reddit table 126,
marketing pages 131/133) and were each confirmed or refuted only by a direct
`cslb.ca.gov` read — never by copying a third-party aggregator.

## Irregularities flagged for review (new this wave)

1. **Repipe Champions license mismatch (hold).** Marketing prints #1057927, which is
   a Hayward B-license under another entity's name. Do not engage for plumbing until
   the contracting entity is named and holds the right classification.
2. **AB Plumbing base ambiguity.** Active license, but CSLB shows Oakland against
   SF-forward marketing; bond cancellation date 10/03/2026; no-employees exemption.
3. **24-7 Rooter near-term expiry.** #954813 expires 11/30/2026 — re-read before booking.
4. **True-Tech location mismatch.** Promoted on Outer Sunset pages; profile is San Jose.
5. **Discount Plumbing naming variants.** "Discount Plumbing San Francisco" (4.5★/1.3k)
   and "Discount Plumbing Rooter Services" (Daly City, 4.8★/1.1k) both surfaced; the
   wave-1 `discount` entry is not duplicated — identity consolidation needs profile reads.
6. **SAFENEST index text-bleed** — its listing excerpt quotes praise for Mike's Water
   Damage; ratings must not be blended.
7. **Near-name pairs kept separate:** Marco's Plumbing / Marco's Plumbing and Cleaning;
   Plumbing Bay Area / Bay Area Plumbing. "Sal's Plumbing" appeared in one Thumbtack
   quote — name-only, added to the watch list, not admitted.
8. **A1 Drywall quote anomaly** — one indexed slot under A1 names "Genuine Drywall";
   treat samples cautiously.
9. **Urban Bay Engineering** — engineering name under a drain-repair tag; scope unconfirmed.
10. **San Francisco Plumbing Repairs** — generic directory-brand pattern (like wave 3's
    Judah/Irving/Noriega storefronts); entity and license unproven.

## Rejected candidates (with reasons)

- **Out of area as primary base** with no SF dispatch evidence: Amorim (Rohnert Park),
  Peña Drywall (Campbell), American Drywall (Santa Rosa), Palacios Painting (San Ramon),
  The Home Remodeling And Water Damage Company (Redwood City), A2Z Restoration (Martinez),
  SI Construction (Alameda), PuroClean of San Rafael, APLUS (Hayward), Letts (Concord),
  Mario's (Redwood City), Pro-care Restoration — all logged here for the record.
- **WB Plumbing Supply (1928 Lawton St, Outer Sunset):** a supply house, not a repair
  contractor. Not admitted as a service provider; noted as a useful parts source.
- **Allied Bay Contractors:** 5.0 but **1 review** — insufficient to characterize.
- **Active Scaffold / ROOF EXPRESS:** scaffolding and roofing — out of scope.
- **Platypus:** sponsored carpentry mention without a resolvable profile in the extract.
- **Access-panel suppliers (BAUCO et al.):** product vendors, not installers — no SF
  installer of record found; gap recorded above.
- **Marco's Plumbing and Cleaning / Sal's Plumbing / HR Renovation / Rooter Hero /
  EJ Home Services / Genuine Drywall:** insufficient independently attributable
  evidence this pass; watch list only, no new entries or merged reviews.

## Honesty / scope notes (unchanged guardrails)

- No wave-4 entry asserts insurance, exact seized-overflow experience, or guaranteed
  Outer Sunset dispatch unless a cited retrieval states it; absences are explicit gaps.
- Indexed extracts may be stale; stars are never blended across platforms; sponsored
  placements are labeled advertising.
- The privacy guardrail holds: no property address, occupant detail, access instruction
  or private project note is stored anywhere in this repository.
- Licensing and any permit obligations remain the owner's responsibility; this research
  identifies licensed, credentialed options from public records (CSLB, SF DBI) and does
  not arrange or endorse unpermitted work.
