# Wave 17 — separate discovery queue

Checked 2026-09-17. **50 new discovery records; zero qualified additions.**

Both plumbing and drywall are required; neither is confirmed for these new leads. The existing 793-record corpus was not changed. No outreach occurred.

## Three audit passes

### Pass 1 — Source transcription
50 name/registry-number pairs transcribed from the opened City response; four CSLB name/status/class/expiry/address checks. Unread fields not inferred. All 50 pairs re-read in a second, targeted query; its complete response contains 52 rows including two aliases.

### Pass 2 — Collision and attribution
Compared all 50 names, stripped name cores and registry numbers against the existing corpus; known collisions excluded. Alias ambiguity still flagged, not treated as proof of distinct legal entities.

### Pass 3 — Qualification and privacy
All 50 held outside the research corpus and qualified master. Eight requirement gates remain unconfirmed; no outreach, no fabricated reviews, no private project details.

These are three checks by one agent, not independent reviewers. Automated tests protect consistency and conservative gates; they do not prove external facts.

## Official sources

1. [city-94122](https://data.sf.gov/resource/3pee-9qhc.json?%24select=firm_name%2Clicense1%2Cfirm_address%2Cfirm_zipcode%2Ccount%28%2A%29&%24group=firm_name%2Clicense1%2Cfirm_address%2Cfirm_zipcode&%24where=firm_zipcode+like+%2794122%25%27+AND+license1+is+not+null&%24order=license1&%24limit=200&%24offset=60) — Only chunks 0 and 1 of a four-chunk response read; retained fields limited to firm_name and license1. Not a complete registry export.

2. [city-crosscheck](https://data.sf.gov/resource/3pee-9qhc.json?%24select=distinct+firm_name%2Clicense1&%24where=firm_zipcode+like+%2794122%25%27+AND+license1+in%28%271074796%27%2C%271081032%27%2C%271084921%27%2C%271094431%27%2C%271096962%27%2C%271098696%27%2C%271098726%27%2C%271100947%27%2C%271114561%27%2C%271115136%27%2C%271118121%27%2C%271121578%27%2C%271124434%27%2C%271124454%27%2C%271125334%27%2C%271126048%27%2C%271128513%27%2C%271131714%27%2C%271138590%27%2C%271146766%27%2C%27297604%27%2C%27319513%27%2C%27362047%27%2C%27369697%27%2C%27375350%27%2C%27389511%27%2C%27403201%27%2C%27407271%27%2C%27415669%27%2C%27424435%27%2C%27433839%27%2C%27461090%27%2C%27464662%27%2C%27474526%27%2C%27482691%27%2C%27496378%27%2C%27508694%27%2C%27511843%27%2C%27521996%27%2C%27522799%27%2C%27526298%27%2C%27530261%27%2C%27537565%27%2C%27545704%27%2C%27548472%27%2C%27572384%27%2C%27582513%27%2C%27595286%27%2C%27611177%27%2C%27615049%27%29&%24order=license1%2Cfirm_name&%24limit=200) — Entire targeted response read: 52 name/number pairs for 50 registry numbers. Two alias rows consolidated; not an export of all firms.

## Line-by-line retained evidence

Each name and number below was visible in both City queries above. Numbers are City registry fields, **not verified active licences** except where an actual CSLB check is separately noted. No phone, website, review, project count or current dispatch was inferred. ZIP filtering is on firm contacts, not work locations.

| # | Name as recorded by City | Registry number | CSLB page read this session |
|---|---|---|---|
| 1 | Stephen Mc Elroy Construction Llc | 1074796 | [active; B; expiry 2027-04-30](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1074796) |
| 2 | Doc Painting & Maintenance Inc | 1081032 | [active; B; expiry 2027-09-30](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1081032) |
| 3 | Bay Cities General Construction | 1084921 | Not read |
| 4 | Zhiwing Builders Inc | 1094431 | Not read |
| 5 | Ccf Construction, Llc | 1096962 | Not read |
| 6 | Doherty Construction | 1098696 | Not read |
| 7 | Alwyn Construction Inc | 1098726 | Not read |
| 8 | Tadashi Wood Construction Company | 1100947 | Not read |
| 9 | Twc Design & Construction Inc | 1114561 | Not read |
| 10 | De Barra Builders | 1115136 | Not read |
| 11 | Cal Builder Inc | 1118121 | Not read |
| 12 | Zm Builders Inc | 1121578 | Not read |
| 13 | Ho Pronamic Construction Inc | 1124434 | [suspended; B; expiry 2028-07-31](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1124434) |
| 14 | Shiny Home Builders & Development Inc | 1124454 | [active; B; expiry 2028-07-31](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1124454) |
| 15 | Module Construction | 1125334 | Not read |
| 16 | Bjy Construction Inc | 1126048 | Not read |
| 17 | Bz And Bz Corporation Inc | 1128513 | Not read |
| 18 | Lin Wang Construction | 1131714 | Not read |
| 19 | Faultline Construction Inc | 1138590 | Not read |
| 20 | Pro Design Build And Construction Inc | 1146766 | Not read |
| 21 | D G Construction Co. | 297604 | Not read |
| 22 | Quality Construction Co | 319513 | Not read |
| 23 | Jack Yim | 362047 | Not read |
| 24 | The Magic Christian | 369697 | Not read |
| 25 | North Beach Construction | 375350 | Not read |
| 26 | Patterson Frank P | 389511 | Not read |
| 27 | Gee Construction | 403201 | Not read |
| 28 | Keane Construction | 407271 | Not read |
| 29 | Kyin Way Ngoon | 415669 | Not read |
| 30 | Guntren Builders Construction | 424435 | Not read |
| 31 | Best Waterproofing Co. | 433839 | Not read |
| 32 | Gerard Keightley Construction Inc | 461090 | Not read |
| 33 | Superior Construction Co | 464662 | Not read |
| 34 | Jacuzzi Properties, Inc | 474526 | Not read |
| 35 | Peletz & Company | 482691 | Not read |
| 36 | Nutek Construction Inc. | 496378 | Not read |
| 37 | Mac Kenzie Construction | 508694 | Not read |
| 38 | Benkee Construction Co | 511843 | Not read |
| 39 | Szeto Construction | 521996 | Not read |
| 40 | Wey Cheng Construction Co | 522799 | Not read |
| 41 | Jan Weith General Contractor | 526298 | Not read |
| 42 | Don Bauer & Co | 530261 | Not read |
| 43 | Benjamin Gilmore Bolles | 537565 | Not read |
| 44 | C D Construction Co | 545704 | Not read |
| 45 | Margason Construction | 548472 | Not read |
| 46 | Guan Han Jie Construction | 572384 | Not read |
| 47 | Gill Construction | 582513 | Not read |
| 48 | Steven Lau Construction | 595286 | Not read |
| 49 | Wei Suen | 611177 | Not read |
| 50 | Yee Lau Construction Co | 615049 | Not read |

## Material flags

- Ho Pronamic: displayed bond suspension, despite a future licence expiry. Held.
- Doc Painting: City address differs from CSLB address; licence page displays a complaint-disclosure link. Details were not read; no allegation or conclusion about its merits is made.
- Doc Painting and Tadashi Wood: same-number name variants were consolidated, not counted twice.
- Gee Construction: the initial response also lists another registry number under the same name. Relationship unresolved.
- All 50: no verified Outer Sunset dispatch, no firm-specific seized-overflow outcome, no confirmed both-trade scope, no project-specific insurance confirmation.

## Review/platform research — no new review records

Searches covered Outer Sunset plumbing/drywall and stuck bathtub trip-lever discussions. Sources were used as discovery/context only; no review was assigned to these 50 registry identities. The following links document the material examined, not proof of a qualified firm:

- [1](https://www.yelp.com/search?cflt=plumbing&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA&start=80) — indexed search extract only.
- [2](https://www.yelp.com/search?find_desc=Dry+Wall+Repair&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA) — indexed search extract only.
- [1](https://www.thumbtack.com/ca/san-francisco/drywall-repair) — indexed extract plus partial live page read; listings differ.
- [5](https://www.thumbtack.com/ca/san-francisco/suspended-ceiling-installers) — indexed extract plus partial live page read; listings differ.
- [3](https://www.reddit.com/r/Plumbing/comments/170tvds/stuck_trip_lever_old_bathtub_wouldnt_turn_up_or/) — indexed community discussion, not a verified contractor review.
- [5](https://www.reddit.com/r/askaplumber/comments/teulx3/trip_lever_rod_broken_off_and_tub_wont_drain_how/) — indexed community discussion, not a verified contractor review.

No complete Google review corpus was obtained. No exhaustive platform coverage, review authenticity, or full re-verification of the inherited corpus is claimed. See `docs/remaining-work.md` for next-session priorities.
