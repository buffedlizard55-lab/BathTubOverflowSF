# Wave 13 discovery log — 2026-09-15

Wave 13 adds 50 new research records and 34 regulator upgrades. It ran three
additional fail-closed verification passes (Passes 28, 29 and 30). No record
was promoted, assigned a priority, or added to the qualified master; the master
remains empty.

Artifact: `data/wave13.json` (50 businesses, 70 sources, 11 retained review
excerpts, 34 upgrades). Generators: `scripts/gen_wave13.py` →
`scripts/merge_wave13.py` → `scripts/patch_wave13_normalise.py`.

After merge: **643 businesses, 587 sources, 155 reviews, 13 waves**. Live
counts used by the site: **261** distinct CSLB `LicenseDetail.aspx` licence
numbers, **179** active licences, **80** non-active licences, **384** records
with no regulator read, **60** records that combine an active licence with an
Outer Sunset (`area: outer`) evidence label. The methodology string counts
**259** distinct stored licence numbers among those 24 new-record reads.

Rebuild (the only safe chain; never re-run the generator against the live
merged file):

```sh
cp reports/research_before_wave13.json data/research.json
python3 scripts/gen_wave13.py
python3 scripts/merge_wave13.py
python3 scripts/patch_wave13_normalise.py
python3 scripts/patch_wave13_closed_gaps.py
```

---

## 1. Discovery composition and hard boundaries

Both plumbing and drywall remain required for a qualified result. A single
trade, a registry number, a platform badge, or a general bathroom-remodeling
claim cannot satisfy that requirement. The wave kept three evidence channels
separate on every new record.

| Tier | Records | What was read | What the record may assert |
| --- | ---: | --- | --- |
| CSLB read directly | **24** | Each `LicenseDetail.aspx` page opened and transcribed field by field | The regulator-published entity, address, phone, status, dates, classifications and displayed credential details |
| Registry only | **14** | Official City permit-contact registry (`k6kv-9kix`) 94122 firm-address roll-up | A recorded firm name, address, licence **number** and permit-row count — not a CSLB status or classification |
| Platform listing | **12** | Thumbtack San Francisco category pages read directly | The platform's own listing, category, hire/review text or badge — not an independent licence fact |

Of the 24 new-record reads **18 are active and 6 are non-active and held**
(canceled 825060, expired 912469 and 431972, suspended 928524 and 824155,
inactive 757766). Every non-active status carries a `hold`-level flag.

The 14 registry-only records have `license: null` and `trade: "registry-lead"`.
They are structurally unable to reach the master list until their licence
number is read directly. The 12 platform records likewise carry no CSLB fact,
even where Thumbtack displays a “Licensed pro” or Top Pro badge. Eleven
attached review excerpts are retained as platform evidence with
`exactTask: false`.

Thirty-four further CSLB pages were read for licence numbers earlier waves had
already stored. They are upgrades, never counted toward the 50:

| Upgrade kind | Count | What it does |
| --- | ---: | --- |
| verification | **16** | Re-reads a licence the stored record already carried |
| registry | **17** | Attaches a first licence fact to a record that had published the unread gap |
| unresolved-identity | **1** | Licence 608902 reads to an individual, not to the stored firm name |

Four of those reads were folded into the stored record rather than published as
a second row, because the stored registry evidence already named the same
number: 805968 (`w9-flmc-development-corp-dba-adamo-campagna`), 611082
(`w7-allen-mechanical-plbg-co`), 968927 (`w6-ocean-air-heating`) and 797077
(`w10-macro-builder-inc`).

Wave 12's eight same-name re-listings were folded into the earlier records
(`dedupeCorrections` = 8) and three Google-attributed excerpts were withdrawn
(`reviewWithdrawals` = 3: R145, R146, R147), so wave 12 now counts 42 records
and seven retained excerpts.

---

## 2. Sources and discovery channels

Source IDs 526–595 (70 objects). Government queries and CSLB pages were read
directly on 2026-09-15.

| Source IDs | Channel | Limitation recorded in the dataset |
| --- | --- | --- |
| 526–531 | [SF DBI plumbing contacts](https://data.sf.gov/resource/k6kv-9kix.json), [building contacts](https://data.sf.gov/resource/3pee-9qhc.json), [plumbing permits](https://data.sf.gov/resource/a6aw-rudh.json), [building permits](https://data.sf.gov/resource/i98e-djp9.json) | Official registry and permit rows identify recorded contacts, work ZIP and quoted scope; a queried ZIP is not present dispatch |
| 532–537 | Thumbtack category pages: drywall contractors, drywall repair, plumbers, ceiling repair, bathroom remodeling, ceiling-drywall-repair | Category listings and badges are platform claims; they do not substitute for a CSLB read or establish Outer Sunset coverage |
| 538–561 | CSLB `LicenseDetail.aspx` for the 24 new-record licences | Direct regulator facts for the licence number shown; a CSLB page does not certify the job, current dispatch, insurance or drywall coverage |
| 562–595 | CSLB `LicenseDetail.aspx` for the 34 upgrades | Attached to the stored record; never a new business |

Negative results, recorded as findings rather than inferred identities:

- Thumbtack `/ca/san-francisco/ceiling-drywall-repair` (source 536) repeated
  listings already found on sources 532–535, so no separate record was created.
- `data.sf.gov` name-scoped drywall / plaster / sheetrock queries against 94122
  returned an empty array.
- Permit-contact lookups for twelve recent 2026 building-permit numbers
  returned `[]`, so those drywall-scope building permits cannot be attributed
  to a licence through City data in this wave.
- Homeowner's Permit rows (licence 000001) appeared in contact lookups and
  were rejected, not stored as businesses.
- Licence 957278 (C & L Plumbing) was opened, then not stored: the page is
  fresh but the name core collides with the stored `cl` record.

No business was contacted, no access control was bypassed, and no inaccessible
review text was reconstructed. New review excerpts are limited to eleven
Thumbtack-attributed records (R148–R158).

---

## 3. Tier 1 — the 24 CSLB pages read as new records

| Licence | Entity as printed by CSLB | Status | Classes | CSLB address |
| --- | --- | --- | --- | --- |
| 843160 | LUSHOV CONSTRUCTION INC | active | B, A | 750 La Playa Street Unit 865, San Francisco, CA 94121 |
| 1036851 | WESTGATE PLUMBING | active | C36 | 121 Quint Street Unit 5E, San Francisco, CA 94124 |
| 1078954 | MISSION HOME REMODELING INC | active | B | 475 Gough St, San Francisco, CA 94102 |
| 1067347 | A2Z REMODELING INC - dba A2Z KITCHEN & BATH | active | B | 3291 Lakeshore Ave, Oakland, CA 94610 |
| 1029472 | XTEAM DESIGN CONSTRUCTION | active | B | 168 S Lake Merced Hls, San Francisco, CA 94132 |
| 1029997 | O'PRO CONSTRUCTION INC | active | B | 229 Cloverbrook Circle, Pittsburg, CA 94565 |
| 1058907 | OLMEC BUILDERS INC | active | B | PO Box 318051, San Francisco, CA 94131 |
| 1074133 | KATZ GROUP | active | B | 587 Castro Street, San Francisco, CA 94114 |
| 825060 | K L PLUMBING INC | canceled | C36 | 1926 Lawton Street, San Francisco, CA 94122 |
| 984413 | FENG K PLUMBING CORP - dba XIN FENG PLUMBING | active | C36 | 1654 23rd Ave, San Francisco, CA 94122 |
| 912469 | BALLA CONSTRUCTION AND DESIGN | expired | B | 1352 10th Avenue 103, San Francisco, CA 94122 |
| 431972 | HONG LEE CONSTRUCTION | expired | B | 532 Grand Ave, South San Francisco, CA 94080 |
| 937334 | CHUBBY CONSTRUCTION | active | B | 1867 45th Avenue, San Francisco, CA 94122 |
| 928524 | LIANG GENERAL CONSTRUCTION INC | suspended | B | 263 Aviador Ave, Millbrae, CA 94030 |
| 961952 | DOUGLAS CLEAVELAND | active | B | 1492 6th Ave, San Francisco, CA 94122 |
| 951781 | KOHLER HEATING | active | C20 | 1229 4th Ave, San Francisco, CA 94122 |
| 656774 | ZE SHENG LIAO | active | B | 2930 Lawton Street, San Francisco, CA 94122 |
| 876008 | SUCCESS CONSTRUCTION | active | B, C10, C36 | 808 Geary St, San Francisco, CA 94109 |
| 898949 | SAN FRANCISCO INVESTMENT DEVELOPMENT | active | B | 1890 14th Avenue, San Francisco, CA 94122 |
| 795316 | L & G CONSTRUCTION CO | active | B | 1742 21st Avenue, San Francisco, CA 94122 |
| 427779 | J & L CONSTRUCTION COMPANY | active | B | 2231 37th Ave, San Francisco, CA 94116 |
| 757766 | B K L CONSTRUCTION | inactive | B | 1245 30th Ave, San Francisco, CA 94122 |
| 1106072 | TAILWIND CONSTRUCTION INC | active | B, C10, C36 | 1762 42nd Ave, San Francisco, CA 94122 |
| 824155 | WING CHOW CONSTRUCTION | suspended | B | 1039 Grant Ave Ste 201, San Francisco, CA 94133 |

Notes:

- **Tailwind Construction Inc (1106072)** is an active B + C10 + C36 licence
  that CSLB itself places at 1762 42nd Ave, 94122. The City registry carries
  the same number at 1879 42nd Av across 22 permit rows. No C-9 or C35 is on
  the page; ceiling restoration would have to be confirmed in writing against
  the B classification. Qualifying individual: Liyuan Liu.
- **Success Construction (876008)** also holds B + C10 + C36, but CSLB places
  it in 94109, workers' compensation shows a cancellation date of 07/31/2026,
  and the Outer Sunset link is a registry row at 1887 25th Av. Held for the
  compensation cancellation.
- **Kohler Heating (951781)** is a documented scope exclusion: C20 only.
- **Wing Chow Construction (824155)** is a different name core from the stored
  `w10-wing-chow-construction-inc` record. It is under contractors-bond
  suspension (Hudson 30138239, cancellation date 09/01/2026).
- **K L Plumbing Inc (825060)** is canceled, corporation dissolved 08/16/2011,
  at an Outer Sunset address. Wave 7 already stored “K L Plumbing” against
  registry number 510452 at the same street; both numbers are published.

---

## 4. Tier 2 — the 14 registry-only leads

Each row is a City registry record: a firm name, a 94122 address, a licence
**number**, and a permit-row count. None of these numbers was read at CSLB in
this wave.

| Firm as recorded | Licence number | Registry location | Permit rows |
| --- | --- | --- | ---: |
| Ting Kun Chow | 771796 | 1735 29th Av, 94122 | 83 |
| C R Construction Co Inc | 747801 | 1687 26th Avenue, 94122 | 31 |
| Andrew Moore Consulting | 859089 | 1230 11th Av, 94122 | 30 |
| Johnston Tile Company | 766814 | 1501 33rd Av, 94122 | 68 |
| Sai Cheung Constr. Co | 577073 | 2029 Kirkham St, 94122 | 62 |
| John Woo Constructionllc | 765131 | 1326 11th Av, 94122 | 49 |
| Lin Hop Construction Inc | 447752 | 1623 Noriega Street, 94122 | 17 |
| Stodoni Construction | 817377 | 1478 38th Av, 94122 | 32 |
| Sun Sun Construction Co | 410660 | 1285 27th Av, 94122 | 36 |
| City Builder Company | 728611 | 1494 47th Av, 94122 | 36 |
| De Star Construction | 982071 | 2209 Moraga Street, 94122 | 35 |
| Mazzys Fire Protection | 502015 | 1280 20th Av, 94122 | 92 |
| Fire Star Heating | 674169 | 4650 Irving St, 94122 | 38 |
| Mediterranean Tile | 572992 | 1735 35th Av, 94122 | 16 |

Several numbers print under more than one firm name or address; each alias is
flagged rather than resolved. John Woo Constructionllc is stored exactly as
the registry prints it (no space before “llc”).

---

## 5. Tier 3 — the 12 platform listings

| Record | Listing | Category page | Review |
| --- | --- | --- | --- |
| w13-plat-willy-floors | Willy Floors | plumbers / drywall-repair | R148 |
| w13-plat-arshan | Arshan Construction & Remodeling | plumbers / drywall-repair | R149 |
| w13-plat-jco | J.Co Contractors Inc | drywall-contractors | none |
| w13-plat-pinnacle | Pinnacle Plumbing, Inc. | plumbers | R150 |
| w13-plat-wp-proline | WP Proline Construction | bathroom-remodeling | R151 |
| w13-plat-aquinos | Aquino's plastering and painting | ceiling-repair | R152 |
| w13-plat-swilly | Swilly Plastering and Stucco | ceiling-repair | R153 |
| w13-plat-bap | Bay Area plastering | ceiling-repair | R154 |
| w13-plat-city-handyman | City Handyman | ceiling-repair | R155 (negative, 3.7) |
| w13-plat-promodeling | Promodeling | bathroom-remodeling | R156 |
| w13-plat-gadi | GADI construction | bathroom-remodeling | R157 |
| w13-plat-antrmen | ANTORMEN | bathroom-remodeling | R158 |

A “Licensed pro” badge is a platform claim and was refused as licence
evidence. City Handyman is retained as the lowest rating in the sample so the
tier is not skewed toward favourable listings. The Arshan excerpt is the
closest adjacent review this wave (frozen shut-off valves; an earlier plumber
who caused damage); the analysis states it is not seized-trip-lever evidence.

---

## 6. Upgrades attached to stored records

| Stored record | Licence | Kind | Status | Classes |
| --- | --- | --- | --- | --- |
| w8-brus-box-contractor-works | 1141495 | verification | active | B |
| w8-wolfe-painting-co | 754201 | verification | active | C33, B |
| w9-elux-construction-inc | 893710 | verification | active | B |
| w9-vij-construction-inc | 1059074 | verification | active | B, D06 |
| w9-american-plumbing-and-trenchless-llc | 1140051 | verification | active | C36 |
| w9-speedy-serrano-plumbing | 1026009 | verification | active | C36 |
| w10-samco-construction-inc | 899541 | registry | active | B, C10 |
| w10-danny-chen | 893929 | registry | inactive | C36 |
| w10-d-s-management-inc-dba-metrocon-builders | 978867 | registry | active | B |
| w10-w-j-l-construction-inc | 775086 | registry | active | B |
| w6-city-plumbing-company | 792165 | registry | canceled | C36 |
| w7-w-k-construction-company | 608902 | unresolved-identity | active | B |
| be-home | 1115373 | registry | active | B |
| reliable-construction | 983658 | registry | active | B |
| w9-all-bay-cities-construction | 872779 | registry | active | B |
| w6-abe-s-plumbing | 439862 | registry | expired | C36 |
| w7-chow-s-plumbing-co | 502603 | registry | expired | C16, C36 |
| w6-west-cork-plumbing-inc | 900309 | verification | active | C36 |
| w6-flow-masters-plumbing-inc | 966337 | verification | active | C36, C16, C20 |
| w6-building-efficiency-inc | 947504 | verification | active | B, C20, C36, C10 |
| w6-pro-plumbing | 859973 | verification | expired | C36, C16 |
| odonovan | 582534 | verification | active | C16, C36 |
| w10-oran-plumbing-corp | 762214 | verification | active | C36 |
| purcell | 493818 | verification | expired | C20, C36 |
| w6-goodrich-plumbing-inc | 837694 | verification | canceled | C36 |
| w6-c-t-construction-plumb | 533324 | registry | active | B |
| w9-kevel-home-performance | 1021221 | registry | active | B, C20 |
| w12-rapid-flow-plumbing | 1115649 | verification | active | B, C36 |
| w12-handyman-heroes | 1003394 | verification | active | B, C10, C36 |
| w10-z-construction-company-inc | 740407 | registry | active | B |
| w9-flmc-development-corp-dba-adamo-campagna | 805968 | registry | active | B |
| w7-allen-mechanical-plbg-co | 611082 | registry | active | C36 |
| w6-ocean-air-heating | 968927 | registry | active | C20 |
| w10-macro-builder-inc | 797077 | registry | active | B |

Classification **D06** (C-61/D06, concrete-related services) was first read on
licence 1059074 and added to `ALLOWED_CLASSES`. It covers neither plumbing nor
drywall.

---

## 7. False claims rejected and dedupe decisions

| Claim | Why rejected |
| --- | --- |
| A Thumbtack “Licensed pro” or Top Pro badge is a CSLB credential | No licence number, class or status is published on the listing |
| A Homeowner's Permit row (licence 000001) is a contractor | Rejected, not stored |
| A City-recorded licence number is a classification | Left unpromoted on all 14 leads |
| Licence 608902 belongs to “W.K. Construction Company” | CSLB issues it to WING HANG CHENG, sole ownership; the stored record keeps asserting no licence fact for the company name |
| A platform review that names a different tradesperson than the listing | Rejected rather than attached, same rule as waves 4, 7 and 12 |

Dedupe:

- Seven licences already stored from waves 8–10 became dated verification
  upgrades: 1141495, 754201, 893710, 1059074, 1140051, 1026009, 899541.
- Five stored registry leads whose own published gap said the number had never
  been read were answered on the existing records: 893929, 978867, 775086,
  792165, 608902 — plus further stored numbers listed in §6.
- Thumbtack listings already in the corpus were not re-created: Bautista
  Drywall, THWC home improvement, Dr. Drain Plumbing and Rooter, Plumbing &
  Rooter Service (Antonio Carcamo Reyes), Dom's plumbing, Discount Plumbing
  Rooter Services, J. Gomez.
- Licence 839447 (Feng K Plumbing Co) and 984413 (Feng K Plumbing Corp dba Xin
  Feng Plumbing) share a near-identical name but are different numbers,
  addresses and individuals; both stand, collision flagged.
- Wave 12's platform record “Mission Home Remodeling” and this wave's
  regulator read “Mission Home Remodeling Inc” (1078954) stay two records: the
  wave-12 row has no address and the identity link is unverifiable.
- Name-core collisions ruled out of the new-record pool included 662067 Jason
  Liu, 1047605 Sunset Remodeling, 1027247 Richbay, 803442 A W Construction,
  834292 Brendan Waters.

---

## 8. Irregularities retained for manual review

- **One insurer cancellation date, four stored suspensions.** Hudson Insurance
  cancellation date 09/01/2026 now appears on All-Point Solutions Plumbing
  950265, F C Company 1022789, Liang General Construction 928524, and Wing Chow
  Construction 824155.
- **Licence 533324 is now read.** Wave 9 published an open question that CT
  Plumbing & Fire Protection (1112261) shares 1847 48th Ave and a phone with
  registry number 533324. CSLB reads 533324 as CT CONSTRUCTION, sole ownership,
  active B only, phone (415) 793-3615 — not the (415) 203-7178 stored on
  1112261. B alone cannot cover pipe work the registry spelling “Construction &
  Plumb” implies. Both records stand.
- **Kevel Home Performance (1021221)** is no longer a registry lead. CSLB
  reads active B + C20 at 3624 Ortega Street, 94122, expiring 11/30/2026. The
  workers' compensation profile is heating and air-conditioning duct work; Yelp
  categories remain HVAC, energy and insulation. Trade corrected to
  `scope-exclusion`. The four attributable reviews stay attached.
- **Danny Chen (893929)** is inactive C36 at 1659 23rd Avenue, 94122
  (“05/05/2025 - WC EXEMPT CANCELLED-LIC INACTIVATED”). The unread-licence
  question is closed negatively.
- **City Plumbing Company (792165)** is canceled by request (02/19/2025) at a
  regulator-recorded 94122 address.
- **Building Efficiency Inc (947504)** is active B + C20 + C36 + C10 at 2037
  Irving Street Suite 213, 94122, with an asbestos certification for bidding
  only. Classifications cover both sides of a wall opening on paper; exact-task
  evidence, insurance for this job, and a written repair-first scope remain
  missing.
- **Handyman Heroes (1003394)** now has a direct CSLB read (B + C10 + C36).
  Additional Status warns that one or more classifications may be removed if
  the qualifying person is not replaced by 10/01/2026, and the page carries a
  complaint-disclosure marker that was **not** opened.
- **American Plumbing and Trenchless LLC (1140051)** is the first stored
  licence in this corpus to display a liability-insurance line (Ategrity
  Specialty, $2,000,000). That still does not satisfy the other master gates.
- **Lushov Construction Inc (843160)** and **Xteam Design Construction
  (1029472)** carry complaint-disclosure markers that were not opened.
- **Fourth Avenue / 94122 pairing** on Kohler Heating and a Barneveld Avenue /
  94122 pairing on Pro Plumbing are flagged: the street sits outside the Outer
  Sunset grid while both CSLB and the registry print ZIP 94122.
- **Task evidence remains zero** for seized overflow extraction, ceiling access
  hatch work, and galvanised-pipe repair. Adjacent review text (frozen valves,
  a stucco hole, a truncated bathroom-remodel sentence) is analysed as adjacent
  only.

These are evidence boundaries, not conclusions about workmanship or intent.

---

## 9. Three fail-closed verification passes (Pass 28, 29, 30)

### Pass 28 — discovery and evidence tiering

The discovery pool was queried from the official SF DBI plumbing-contact
registry (94122 firm-address roll-up, rows 1–210), completed 94122 plumbing
permits, drywall-named building permits, and Thumbtack plumbing, drywall,
ceiling and bathroom-remodeling category pages. Candidates were separated into
direct regulator reads, registry-only leads, and platform listings. A registry
number was never treated as a licence fact, and a platform badge was never
treated as a CSLB credential. Duplicate licence numbers and name cores were
folded into upgrades instead of parallel rows so the wave stayed at 50 new
records.

### Pass 29 — regulator, identity and source audit

Each selected CSLB page was checked line by line for entity name, licence
number, status, dates, address, phone and classification. The merge required a
matching government URL ending in the licence number, rejected
licence/name/phone/source collisions unless a published collision flag named
the twin, checked that trade labels are supported by the recorded classes
(including new class D06), and held every non-active status. Wave-12 duplicate
rows were folded; three Google excerpts were withdrawn. New source metadata,
citations, review IDs and privacy-sensitive text were checked before the merge
could write.

### Pass 30 — attribution, qualification, render and close-out audit

Review business IDs, platform attribution, source links and quoted excerpts
were checked separately. The final gate confirmed that every wave-13 record
has an unresolved gap, no record has an exact-match, insurance, scope-confirmed,
master or priority assertion, and no non-active record is presented as
bookable. Stale summary copy that still described Kevel Home Performance and
licence 533324 as unread was corrected to match the regulator pages. Snapshot
numbers on `README.md` and `index.html` were brought to 643 / 13 waves. The
session branch was added to both workflow YAML triggers. Structural, render,
monitor and browser tests were re-run. The required plumbing-plus-drywall
condition remains a hard gate.

The passes are intentionally conservative: they preserve irregularities for
manual review rather than reconciling conflicting names, addresses, phone
numbers, categories or review text by assumption.

---

## 10. What wave 13 does not claim

- It does not claim any business has been verified for the project, or that any
  registry or platform listing is a licence.
- It does not claim a licence status establishes exact-task experience, current
  insurance in force, or willingness to take the work.
- It does not claim any business will arrive at an Outer Sunset address: a
  registry or regulator address is a recorded location, not a dispatch promise.
- It does not turn a rating, a hire count or a badge into a credential, and it
  does not repeat private project context in any public artifact.

The qualified master remains empty.
