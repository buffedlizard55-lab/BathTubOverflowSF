# Wave 18 — separate discovery queue

Checked 2026-09-17. **50 new discovery records; zero qualified additions.**

Both plumbing and drywall are required; neither is confirmed for these new leads. The existing 793-record corpus and the separate wave-17 queue were not changed. No outreach occurred. This wave deliberately continues discovery while the next-session priority remains depth (identity resolution, attributable reviews, both-trade evidence) on the existing shortlists.

## What was done, line by line

1. **City building-contact query (dataset 3pee-9qhc), firm ZIP prefix 94122, ordered by license1, offset 200.** All four chunks of the response were read through the page reader; roughly 215 displayed rows were transcribed.
2. **City plumbing-contact query (dataset k6kv-9kix), ZIP prefix 94122, ordered by license_number, offset 100.** All four chunks read; roughly 130 displayed rows transcribed, including phone variants per grouped row.
3. **Dedupe.** Every transcribed name, stripped name core and registry number was compared with the 793-record corpus (including full-text number scan of `data/research.json`) and the 50 wave-17 records. 104 of the 240 transcribed candidate rows were rejected as collisions (names and numbers already stored by earlier waves — Stan Plumbing, Pro Plumbing, Abe's Plumbing, Bill Bragg Plumbing, Feng K. Plumbing, Euro Plastering, Shek's, Lam & Lee, David Chu, Hawk N Lee and most Thumbtack/Yelp/Reddit names, among others).
4. **Selection.** 43 clean registry candidates were retained: all plastering/painting/plumbing/tile-named firms still available plus the highest-count general builders at 94122 contact addresses.
5. **Cross-check.** Two targeted City queries re-read all 43 retained numbers in the same datasets: 33 building-contact pairs returned exactly (one row each) and 11 plumbing-contact rows for 10 numbers (one alias row: "Johnson Control/Nis, Inc." at 307912). Every retained registry record therefore appears in two independent City reads.
6. **CSLB reads.** 12 licence detail pages were opened and transcribed field by field (business information, entity, issue/reissue/expiry, status text, classifications, bond line, workers' compensation line, additional status). Result: **2 active, 2 suspended, 2 inactive, 6 expired.** Every non-active record is held.
7. **Platform/community.** Live Thumbtack category pages (plumbers, drywall, plastering, ceiling repair) were read; Yelp evidence came from search-extracts; Reddit pages returned HTTP 403, so thread evidence is search-extract only. Every displayed Thumbtack drywall/plastering/ceiling pro and nearly every Yelp and Reddit name was already stored in the corpus and was **not** re-counted. Seven genuinely new platform identities were retained. One Thumbtack business (Repipe Specialists) matched an existing corpus record and is published as a fold, not a parallel entry.

## Three audit passes

### Pass 1 — Source transcription
All 43 registry pairs were transcribed from the opened City responses; displayed addresses, ZIPs, phones and counts are stored exactly as displayed on the retained grouped row (alias-row and phone-variant notes are published per record). The 12 CSLB pages were transcribed field by field; unread fields were left absent. Platform ratings, hire counts, badges and quotes are stored only where displayed; missing displays stay missing.

### Pass 2 — Collision and attribution
All 50 names, stripped name cores, ids and registry numbers were compared against the corpus and wave 17 before any record was written (104 candidate rows rejected as collisions). Each registry number was then re-read in a targeted cross-check query of the same dataset. One alias pair (Johnson Construction Co / Johnson Control/Nis, Inc.) was consolidated into a single record. The Repipe Specialists account was folded into the stored wave-10 record instead of being duplicated.

### Pass 3 — Qualification and privacy
All 50 records held outside the corpus and the qualified master. Eight requirement gates remain unconfirmed on every record; no outreach, no fabricated reviews, no reconciled-by-assumption conflicts, no private project details in any field. Truncated excerpts are marked truncated at the cut point rather than completed.

These are three checks by one agent, not three independent reviewers. Automated tests (`tests/discovery18.test.js`, `tests/browser/discovery18.spec.js`) protect consistency and conservative gates; they do not prove external facts.

## Official sources

1. [city-a](https://data.sf.gov/resource/3pee-9qhc.json?%24select=firm_name%2Clicense1%2Cfirm_address%2Cfirm_zipcode%2Ccount%28%2A%29&%24group=firm_name%2Clicense1%2Cfirm_address%2Cfirm_zipcode&%24where=firm_zipcode+like+%2794122%25%27+AND+license1+is+not+null&%24order=license1&%24limit=200&%24offset=200) — building contacts, entire four-chunk response read.
2. [city-a-crosscheck](https://data.sf.gov/resource/3pee-9qhc.json?%24select=distinct+firm_name%2Clicense1&%24where=license1+in%28%27750209%27%2C%27830655%27%2C%27819519%27%2C%27711115%27%2C%27730800%27%2C%27721644%27%2C%27847215%27%2C%27845353%27%2C%27719222%27%2C%27791127%27%2C%27685718%27%2C%27749150%27%2C%27871463%27%2C%27681955%27%2C%27686057%27%2C%27761394%27%2C%27754649%27%2C%27778667%27%2C%27880429%27%2C%27786487%27%2C%27738744%27%2C%27850582%27%2C%27866221%27%2C%27850016%27%2C%27866340%27%2C%27797155%27%2C%27795882%27%2C%27718999%27%2C%27707090%27%2C%27879073%27%2C%27887672%27%2C%27901734%27%2C%27765291%27%29&%24order=license1%2Cfirm_name&%24limit=200) — 33 pairs re-read.
3. [city-b](https://data.sf.gov/resource/k6kv-9kix.json?%24select=firm_name%2Clicense_number%2Caddress%2Czipcode%2Cphone%2Ccount%28%2A%29&%24group=firm_name%2Clicense_number%2Caddress%2Czipcode%2Cphone&%24where=zipcode+like+%2794122%25%27&%24order=license_number&%24limit=200&%24offset=100) — plumbing contacts, entire four-chunk response read.
4. [city-b-crosscheck](https://data.sf.gov/resource/k6kv-9kix.json?%24select=distinct+firm_name%2Clicense_number&%24where=license_number+in%28%27348588%27%2C%27376048%27%2C%27446707%27%2C%27307912%27%2C%27315962%27%2C%27368898%27%2C%27398232%27%2C%27462311%27%2C%27415007%27%2C%27369977%27%29&%24order=license_number%2Cfirm_name&%24limit=200) — 11 rows for 10 numbers re-read (one alias row).
5. Twelve CSLB licence detail pages (linked per record in `wave18.json`).
6. Live Thumbtack pages: [plumbers](https://www.thumbtack.com/ca/san-francisco/plumbers/), [drywall](https://www.thumbtack.com/ca/san-francisco/drywall-contractors), [plastering](https://www.thumbtack.com/ca/san-francisco/plastering), [ceiling repair](https://www.thumbtack.com/ca/san-francisco/ceiling-repair-companies).
7. Yelp search-extracts: [dry wall repair near Outer Sunset](https://www.yelp.com/search?find_desc=Dry+Wall+Repair&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA), [drywall installation near Outer Sunset](https://www.yelp.com/search?find_desc=Drywall+Installation&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA), [drywall repair service SF](https://www.yelp.com/search?find_desc=drywall+repair+service&find_loc=San+Francisco%2C+CA), [near-me drywall repair](https://www.yelp.com/nearme/drywall-repair).
8. Reddit search-extracts (direct fetch returned HTTP 403): [r/SouthSanFrancisco plumber recommendations](https://www.reddit.com/r/SouthSanFrancisco/comments/1df11w7/plumber_recommendations_for_ssf/), [r/AskSF plumber thread](https://www.reddit.com/r/AskSF/comments/jcy9dl/can_you_recommend_a_plumber/).
9. Mechanism context (not business evidence): [trip-lever drain wiki](https://www.jaspector.com/wiki/trip-lever-drain/), [DIY forum thread on rusted-off overflow screws](https://www.doityourself.com/forum/toilets-sinks-showers-dishwashers-tubs-garbage-disposals/570507-replacing-bathtub-drain-lever-no-screw-holes-screws-rusted-off.html).

## Line-by-line retained registry evidence

Each name and number below was visible in **both** City queries listed above. Numbers are City registry fields, **not verified active licences** except where a CSLB check is separately noted.

| # | Name as recorded by City | Registry number | CSLB page read this session |
|---|---|---|---|
| 1 | Westside Plastering | 750209 | [suspended — Contractors Bond Suspension; C35 Lathing and Plastering; expiry 2028-06-30](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=750209) |
| 2 | A Atlantiac Plastering Inc | 830655 | [inactive — not able to contract; C35; expiry 2028-01-31](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=830655) |
| 3 | E-Construction And Plumbing Co | 819519 | [suspended — Contractors Bond Suspension; B + C36 Plumbing; expiry 2027-01-31; CSLB name "AAA CONSTRUCTION AND PLUMBING CO"](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=819519) |
| 4 | Ron Chan Painting | 711115 | [active; C33 Painting and Decorating; expiry 2027-08-31; CSLB licensee YONG RONG CHEN at matching 94122 address](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=711115) |
| 5 | Carpentech Co | 730800 | [active; B General Building; expiry 2027-08-31; CSLB licensee YU OUYANG, Madera address](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=730800) |
| 6 | All Trades Contracting | 721644 | [expired 2013-07-31; B; CSLB name ALLTRADES, San Diego](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=721644) |
| 7 | Sunset Improvements | 847215 | [expired 2018-09-30; B; matching 94122 address](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=847215) |
| 8 | Ciganovich Constr****Bond Suspend****** | 845353 | [expired 2014-08-31; B; bond cancelled 2007; matching 94122 address](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=845353) |
| 9 | Winner Remodel & Const | 719222 | [inactive; B; CSLB name "BAK REMODEL & CONSTRUCTION" at same address; expiry 2030-02-28](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=719222) |
| 10 | Owens Design Build Inc | 791127 | [expired 2025-06-30; B; Secretary of State status must be restored to reactivate](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=791127) |
| 11 | Visual Building & Remodeling Inc | 685718 | [expired 2006-09-30; B; reissued to another entity 1998 per displayed note](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=685718) |
| 12 | Morris Home Inc | 749150 | [expired 2004-05-31; B; historical disciplinary bond displayed](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=749150) |
| 13 | Huff Construction Company Inc | 871463 | Not read |
| 14 | Baseline Homes | 681955 | Not read |
| 15 | Guilfoyle Construction | 686057 | Not read |
| 16 | Kelly & Gallagher Bldg Co | 761394 | Not read |
| 17 | James Garcia Construction | 754649 | Not read |
| 18 | Maguire Construction | 778667 | Not read |
| 19 | P J Hegarty Construction | 880429 | Not read |
| 20 | Brody Construction | 786487 | Not read |
| 21 | Carson Construction | 738744 | Not read |
| 22 | Aotearoa Construction | 850582 | Not read |
| 23 | Stellar Construction | 866221 | Not read |
| 24 | P J M Construction | 850016 | Not read |
| 25 | Patrick Keightley Construction | 866340 | Not read |
| 26 | Sean O'neill Construction | 797155 | Not read |
| 27 | Mcelroy Construction | 795882 | Not read |
| 28 | J & H Construction Co. | 718999 | Not read |
| 29 | Sun Shing Construction Co | 707090 | Not read |
| 30 | C & K Builders Inc | 879073 | Not read |
| 31 | Hong's Custom Builders | 887672 | Not read |
| 32 | Quest Builders Inc. | 901734 | Not read |
| 33 | Shamrock Builders Inc | 765291 | Not read |
| 34 | Phil's Refrigeration | 348588 | Not read |
| 35 | Russell Tile Company | 376048 | Not read |
| 36 | Metrom Construction | 446707 | Not read |
| 37 | Johnson Construction Co | 307912 | Not read (alias row "Johnson Control/Nis, Inc." consolidated) |
| 38 | Duncan  Construction | 315962 | Not read |
| 39 | Wing On Construction Co | 368898 | Not read |
| 40 | Fogarty Construction | 398232 | Not read |
| 41 | Lau's Construction Co | 415007 | Not read |
| 42 | Lotti Construction | 462311 | Not read |
| 43 | United Pacific Construction Company | 369977 | Not read |

## Platform / community records (7)

| # | Name | Where seen | Retained evidence |
|---|---|---|---|
| 1 | Drain Geeks | Thumbtack SF plumbers category (live read) | 4.9 (9), 8 hires; Meredith N. water-heater replacement excerpt; no licence badge displayed on the card |
| 2 | Handy Teddy | Thumbtack SF plumbers category reviews section (live read) | Michael L. short endorsement; Sausalito profile path; rating not displayed in the read fragment |
| 3 | JC PLUMBING | Thumbtack SF plumbers category reviews section (live read) | Duncan C. quote truncated at the read boundary; no profile opened |
| 4 | Robert Insulation & Drywall | Yelp drywall-repair SF search-extract | 4.5 (15); "Verified License" label; reviewer quote truncated in the extract |
| 5 | Bendana Drywall | Yelp drywall-repair SF search-extract | 5.0 (1) — thin base; quote truncated in the extract |
| 6 | M A Drywall & Restoration | Yelp drywall-repair SF search-extract | 5.0 (1) — thin base; retained text is the business's own description, not a customer review |
| 7 | The Handyman Can | Yelp near-me drywall search-extract | Category tags and review count only; no excerpt displayed |

**Fold:** Repipe Specialists - San Francisco Bay Area was displayed on the Thumbtack plumbers page with a galvanized-repipe account describing wall/ceiling opening plus full restoration. The corpus already stores this business (`w10-repipe-specialists-san-francisco-bay-area`, same profile URL), so no parallel record was created; the fold is recorded in `wave18.json` → `dedupeFolds`.

## Queued irregularities

- **Westside Plastering (750209):** Contractors Bond Suspension with the bond cancelled 09/01/2026; C35 is the closest displayed trade to the restoration side but the licence cannot currently contract. CSLB address is Mill Valley vs the City row's 1870 25th Av 94122.
- **A Atlantiac Plastering Inc (830655):** inactive; registry spelling differs from the CSLB spelling; 94127 CSLB address vs 94122 registry address.
- **E-Construction And Plumbing Co (819519):** CSLB prints a different business name (AAA CONSTRUCTION AND PLUMBING CO) and a Santa Clara address; B + C36 would otherwise be the strongest displayed plumbing match. Identity left flagged.
- **Winner Remodel & Const (719222) vs BAK REMODEL & CONSTRUCTION:** same number, same address, different displayed names; inactive since 2023 per the displayed miscellaneous note.
- **Carpentech Co (730800):** active B but CSLB address is Madera; current Outer Sunset presence unestablished.
- **Morris Home Inc (749150):** historical disciplinary bond displayed; transcribed, not characterised.
- **Drain Geeks:** no licence badge displayed on the read card while neighbouring cards show badges; recorded as displayed, not interpreted.
- **Reddit access:** direct fetch returned HTTP 403; thread content is search-extract only. All attributable names in the threads read were already stored, so Reddit produced no new records this wave.
- **Yelp access:** business pages remain blocked; all Yelp evidence is search-extract, stated on every record that uses it.

## What this wave does NOT establish

- No record demonstrates **both** required trades for this project. The two C35 plastering reads are non-active; the single C36 plumbing read is suspended with an unresolved name; the two active reads are C33 painting (adjacent only) and B general building in Madera.
- No seized-overflow outcome (successful or unsuccessful) was attributable to any new lead. The Repipe Specialists fold describes the replacement path, not a repair-first extraction.
- No insurance, availability, dispatch or written scope was obtained; nothing was sent or requested.
- No claim is made to have read all reviews of any business.
