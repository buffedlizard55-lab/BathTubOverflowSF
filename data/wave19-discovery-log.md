# Wave 19 discovery log (2026-09-17)

Discovery-only wave: 50 new records in `data/wave19.json`, none merged into the
793-record corpus, master still empty. All records held, all gates unconfirmed.

## Method

1. **Drywall/plaster permit scope join.** Queried the City building-permits
   dataset (`i98e-djp9`, data as of 2025-10-25) for completed 94122 permits in
   the drywall/plaster/ceiling/sheetrock/lath keyword scope (1,419 match in
   total), took the 60 most recent by issued date, and joined them to the
   building-permit contacts dataset (`3pee-9qhc`) on `permit_number`.
2. **In-wall plumbing permit scope join.** Queried the plumbing-permits
   dataset (`a6aw-rudh`, data as of 2026-09-17) for completed 94122 permits in
   the in-wall/trap/overflow/tub-drain keyword scope (40 rows), and joined the
   17 most relevant to the plumbing-permit contacts dataset (`k6kv-9kix`).
3. **Registry continuation.** Paged the grouped 94122 rows of `k6kv-9kix` at
   offset 300 (all 4 chunks) and offset 500 (2 chunks) - offsets 0-299 were
   already consumed by waves 16-18.
4. **Dedupe.** Every candidate name, stripped name core, id and licence number
   was screened against the 793-record corpus, the wave 17/18 queues, and
   every 5-7 digit number stored in corpus prose. Known collisions were
   excluded before any record was written.
5. **CSLB reads.** 16 direct licence detail reads on cslb.ca.gov (data
   current as of the 9/17/2026 stamps transcribed into each record).
6. **Cross-checks.** Every retained name/number pair was re-read in a targeted
   `distinct` query of the same dataset (city-crosscheck-* sources).
7. **Platform reads.** Thumbtack drywall/plastering/ceiling/plumbers category
   pages read live; Yelp and Reddit read through search extracts (direct fetch
   is blocked in this environment).

## Candidates excluded as known collisions (not recorded)

Permit-join pool (39 candidates; 5 kept): Kobliska Construction 697522,
Gagne Rossie Enterpreses 1108989, Lin's Builder 613489, Baa General Builder
1072943, Constantine Construction 773300, Blue Wood Construction 1008141,
Cleanair Image/Servpro 937457, All Property Tech 1087651, Yong Hong
Construction 855109, M & L Construction 832092, Bay Metro 850352, Zamora
Construction 1020870, Edri Construction 1070193, Kevin Lin Construction
1004147, Innovation Plumbing 1013565, Csq Inc 1101204, Bold Construction
Group 1018292, Rprw/Macmillan 1132400, Mars Construction 1111917, Boman Deign
& Construction 1111133, Kelun Construction 1064544, Wolfe Painting 754201,
Solid Design Construction 944813, Precise Construcion 1022801, O'neil
Engineering 1142594, Plus One Construction 1078252, Brus Box Contractor Works
1141495, Sean M O'Reilly 812877, Raxe Construction 1119854, Safe Step Walk-In
Tub 1082165, Buck Construction 1002753, Pro Care Restoration 1090249, Sarris
Construction 361402, Gerson Construction 1108341.

Plumbing-permit-join pool: A G Quality Plumbing 828200 (name/core stored),
Wolfe Painting Co 754201, Axion Plumbing 1122605, Garzac Plumbing 830368,
Amx Plumbing 822482, Yu Plumbing 1051988 (all stored numbers).

Registry offset 300-499 (25 screened; 17 kept): Constant Construction 466541,
Ecd Construction 470364, Jacuzzi Properties 474526, Fong's Plumbing 479286,
Peletz & Company 482691, Z M General Contractor 483659, Chris Goodwin
Plumbing 486122, Wah Lau Plumbing 486546, W & J Plumbing 486546, Sberlo
Plumbing 487017, Peter So 488896, Tile Arts 489739, Purcell Bros 493818,
Nutek Construction 496378, J C Tan Construction 496957, Emerald Plumbing &
Fire 498866, Fong's Construction 499286, Mazzys Fire Protection 502015.

Registry offset 500+ (24 screened; 10 kept, 2 excluded): C D Construction
545704, Connor Daly 546425, Margason 548472, J K Construction 552359, Ricky's
Plumbing 570753, Guan Han Jie 572384, Mediterranean Tile 572992, Sai Cheung
577073, Le's Rooter 581431, Gill Construction 582513, C W Lee Plumbing
586693, Kelly Brother's 587887, Snc Plumbing 595176, Kuenzli 576600 (all
stored). D.C.K. Construction 553166 excluded as a parallel entry and folded
into w19-531666 (same address, unreconciled second number). Stephen Donnelly
573143 retained (individual-name row, single permit, flagged; also appears as
'House To Home Remodeling' under the same number).

Platform (19 screened; 7 kept): New Age Drywall, Bautista Drywall, Rock &
Smooth Drywall, THWC home improvement, Arshan Construction & Remodeling,
Aquino's plastering and painting, Swilly Plastering and Stucco, Bay Area
plastering, City Handyman, Caledonia Plastering & Stucco (folded into stored
w6-caledonia-plastering-stucco-inc with new review excerpts), Plumbing &
Rooter Service (Antonio Cárcamo Reyes), AMX Plumbing, Discount Plumbing
Rooter Services (all stored). Yelp search extracts (drywall repair SF;
drywall installation Outer Sunset; dry wall repair Outer Sunset; handyman
Outer Sunset): every displayed business (Toms Painters, The Meticulous
Handyman, DaSilva Painting, All Around Builder, J Gomez Painting, A New
Concept General Construction, Mullican Remodeling, Richard De Nola, Pacific
Construction, SF Building Group, Paul Woodford Services, Jose HandyMan
Services, Octavio Handyman, HandyFix, Speer, ABC Maintenance, Handyman
Heroes, Handy Helper, ABR PRO Painting, Carlos' Painting & Handyman) was
already stored. Reddit r/AskSF + r/bayarea drywall-repair threads: J.A.
Emmanuel Construction, Sederap, Paul Woodford Services all stored; one
unattributable "man and a van" pointer not retained.

## The 60 building permits in the drywall-scope join

202606183523 (2026-06-18, owner-builder - not a business lead), 202605181462
Bay Metro, 202605141289 Gerson 1108341, 202603318629 Sarris 361402,
202603318559 Pro Care 1090249, 202603308518 Buck 1002753, 202603258250 Safe
Step 1082165, 202603187849 Raxe 1119854, 202603127447 Sean M O'Reilly 812877,
202603026793 Brus Box 1141495, 202602176040 Brus Box 1141495, 202602105651
Plus One 1078252, 202602045258 O'neil 1142594, 202601133757 Precise
1022801, 202601123651 **Detail Drywall & Stucco 1032948 (KEPT)**, 202512151795
Solid Design 944813, 202512111572 Wolfe 754201, 202512081247 Kelun 1064544,
202512051101 Boman 1111133, 202512030860 Mars 1111917, 202511260567 Rprw
1132400, 202511250390 Bold 1018292, 202511129339 Bold 1018292, 202511079142
Bold 1018292, 202511079140 Bold 1018292, 202510298498 Csq 1101204, 202510288289
Innovation 1013565, 202509054630 Kevin Lin 1004147, 202508153141 Edri 1070193,
202508132992 Zamora 1020870, 202508072522 Bay Metro 850352, 202508062402 M & L
832092, 202507140728 Yong Hong 855109, 202506128626 All Property Tech 1087651,
202506027697 Servpro/Belmont 937457, 202505196742 Blue Wood 1008141,
202505086076 Blue Wood 1008141, 202505075931 Constantine 773300, 202505025665
**Quick Connect 394146 (KEPT)**, 202504235031 **Werner's 1074837 (KEPT)**,
202504174635 Baa 1072943, 202503308518 (dup line of 2026 row, registry row
shared), 202502180456 Lin's 613489, 202502110086 **Casman 1013908 (KEPT)**,
202502059715 **Kwan Chok Kee 1087358 (KEPT)**, 202507070245 Kwan Chok Kee
1087358 (KEPT, same licence), 202501228824 Gagne Rossie 1108989, 202501077889
Kobliska 697522, 202411215447 (owner row - not a business lead), plus the
remaining balance of the 60-row window (each row read in full across the
three response chunks; owner/Owner Builder rows and architect/engineer
classification rows C-40493, C74001, C29609, C32972, S5157, 56997 were not
usable as business leads).

## CSLB reads (16)

| number | name (CSLB legal) | status | classes | note |
|---|---|---|---|---|
| 1032948 | DETAIL DRYWALL & STUCCO INC | active | B, C35, C-9, C36 | wave's standout: both required trades on one licence; Hayward address, 415 phone |
| 1087358 | KWAN CHOK KEE INC | active | B, C10, C36, C16 | SF address 94127; WC exempt (no employees) |
| 1013908 | CASMAN CONSTRUCTION INC | active | B | Pacifica; WC code 543200 unreadable |
| 1074837 | WERNER'S GENERAL CONTRACTOR INC | active | B | Novato; reissued to another entity 02/23/2022 |
| 394146 | QUICK CONNECT ELECTRIC CO | active | C10, B | electrical-first; expires 09/30/2026 |
| 1042086 | BAY HOME REMODELING INC | active | B | Orinda |
| 430548 | STEVEN HARRIS GLORIT PLUMBING CONTRACTOR | active | C36 | S SF; WC renewal window |
| 443682 | REBORN CABINETS LLC dba REBORN BATH SOLUTIONS | suspended | B, C-6 | four suspension reasons; complaint disclosure exists |
| 933593 | ALANSI'S ROOTER & PLUMBING | inactive | C36 | WC required to reactivate |
| 915382 | SCHICKER INC dba SCHICKER LUXURY BATH | active | B | Concord; earlier dba Re-Bath By Schicker |
| 1050217 | ERWYN'S INCORPORATED dba ERWYN'S PLUMBING | active | C36, C42 | Richmond; WC code 5183 unreadable |
| 937080 | BURTON'S CONSTRUCTION | active | B, C36, C54 | SF 94118 address; WC exempt |
| 1003568 | DESIRED PLUMBING INC | active | C36 | Petaluma; WC codes unreadable |
| 1045949 | DELEON PLUMBING | active | C36 | Daly City |
| 732885 | D K M PLUMBING | active | C36 | San Bruno; permit = main supply line moved for wall repair |
| 832458 | ISIP FAMILY CORPORATION DBA ARIEL'S PLUMBING | active | C36 | San Bruno; reissued 11/06/2023 |

## Caledonia fold (stored record, not a new entry)

Caledonia Plastering & Stucco (w6-caledonia-plastering-stucco-inc) gained
evidence this session: five interior plaster/ceiling repair review excerpts
from the Thumbtack plastering category page (including a 110-year-old-home
re-plaster account), Yelp stucco extract (1551 Judah St, Outer Sunset tag,
5.0 (36), Verified License), BBB profile (CSLB licence 1057063, expiration
8/31/2027), BuildZoom (active Lathing And Plastering, 91 permits). The stored
record remains unqualified; this wave does not edit the corpus.

## What the wave establishes

- Two new active multi-trade licences (B+C36): Detail Drywall & Stucco
  (1032948, also C-9 + C35) and Burton's Construction (937080, also C54),
  plus Kwan Chok Kee (1087358, B+C10+C36+C16).
- The plumbing side produced 10 active C36 leads with completed 94122
  in-wall/tub/trap permit evidence; the closest single permit is D K M
  Plumbing's PW20260403844 (main cold water supply relocated for wall
  repair) and Alansi's PP20250514222 (drain stack in a first-floor wall),
  though Alansi's licence is currently inactive.
- 27 registry-only 94122 leads remain unread (CSLB) by design of this wave.

## Next-session work (details in docs/remaining-work.md)

1. CSLB-read the 27 registry-only numbers, prioritizing plumbing-named firms.
2. Continue the standing unread lists (31 wave-18, 46 wave-17 numbers) and the
   handover rechecks (830655 reactivation, 819519 name question, 750209 bond).
3. Ask Detail Drywall & Stucco, Burton's, and Kwan Chok Kee the two
   trade-confirmation questions (plumbing + drywall/ceiling for Outer Sunset).
4. Re-verify the suspended Reborn licence and the complaint-disclosure link
   before any contact; do not contact while suspended.
