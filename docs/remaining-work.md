# Remaining work and limitations

Status at the end of wave 16 (2026-09-16): **793 research records across 16 waves, 673 evidence
references, 172 review excerpts, 311 direct CSLB licence reads, 0 qualified master entries.**
This document is the handover: what still has to happen, what is blocking it, and the exact
next actions. It is written to be executed autonomously in this or the next session.

## 1. What still needs doing

### 1.1 Continue the wave programme (waves 17+)

Wave 16 was pass block 37–39. The programme's repeating unit is one 50-record discovery wave
followed by three verification passes, and the same fail-closed shape should continue.

Queued, already-diffed licence numbers that were seen in the SF DBI 94122 building-contact
registry but **not yet opened at CSLB** (do not assert anything about them before reading the
page):

```text
1074796 Stephen Mc Elroy   1079861 K&H                 1081032 Doc Painting
1082812 Shelter Cove       1084921 Bay Cities          1090839 Nelson Zheng
1094431 Zhiwing Builders   1096962 CCF Construction    1098145 Cota Glass
1098696 Doherty            1098726 Alwyn               1100947 Tadashi Wood
1106072 Tailwind           1114561 TWC Design          1115136 De Barra
1116597/1148830 RF Fire Alarm                      1118121 Cal Builder
1121578 ZM Builders        1124434 Ho Pronamic        1124454 Shiny Home
1125334 Module             1126048 BJY                1128513 Bz and Bz
1131714 Lin Wang           1138590 Faultline           1146766 Pro Design Build
1536 Lang Engineering      20189/403201 Gee Construction
297604 D G Construction    299971 Lea Electric         306841 Shek's Plumbing
319513 Quality Construction 324708 Hawk N Lee          328973 Delao Electric
343837 Frank J Obrien      359453 Jim Wong Electric    362047 Jack Yim
362539 Stewart Cheung      36260 Peters Design-Build    369697 The Magic Christian
375350 North Beach Construction                       377316 Alexander Construction
389511 Patterson Frank P   407271 Keane Construction    410660 Sun Sun Construction
415669 Kyin Way Ngoon      424435 Guntren Builders      425741 Aaron Electric
427779 J & L Construction  431622 Sunset Glass         433839 Best Waterproofing
440780 Bill Bragg Plumbing 442727 Chin Pang Construction
```

Each wave must keep the three tiers separate, re-diff every number against the whole corpus
(ids, normalized names, stripped cores, licence numbers, ten-digit phones), open each claimed
licence page live, and end with three passes: regulator transcription, collision/attribution,
fail-closed qualification.

### 1.2 Close the trade-evidence gap (the real blocker)

- 163 records hold a C36 (plumbing) licence and **3** hold a C-9 (drywall) licence; only
  **Sederap's Drywall Inc** holds both on one licence — and it is held, because its registry
  address does not match the regulator's and no review was attributable to it.
- No record yet publishes a readable account of a **seized bathtub-overflow trip lever** being
  freed, whether from above, from behind the wall, or via a below-floor access hatch. The
  closest evidence remains the Reddit/forum material already stored, which is general rather
  than firm-specific.
- Highest-value next searches:
  1. CSLB licence search by classification (C36, and C-9) filtered to San Francisco, then read
     each hit's detail page; add only firms whose printed address or registry history touches
     94122.
  2. SF DBI **permit detail** dataset filtered to work-location ZIP 94122 with descriptions
     mentioning tub, overflow, trip lever, access panel, sheetrock, drywall repair or ceiling,
     then join the permit numbers back to the contact datasets to recover firm identities.
  3. The building/plumbing contact datasets at **firm ZIP 94122 excluding licences already
     stored** (the wave-16 method) — the remaining low-count rows and `license1 is null` rows
     are still unmined; re-query with `$offset` paging because the 60-row limit was reached.

### 1.3 Review corpus

- Yelp pages return HTTP 403 to this workspace; Yelp material is search-extract only.
- The original Google review corpus is not retrievable; three Google-attributed rows were read
  through Birdeye and labelled as such.
- Reddit threads are readable and were used, but no thread has yet named a firm together with
  an overflow/trip-lever outcome.
- Next: try Thumbtack pro pages for the C36 firms already stored (some publish dated reviews
  with photos), and re-check the Yelp search extract for the exact phrases already used; never
  reconstruct a blocked corpus from memory.

### 1.4 The two gates that no record can currently pass by research alone

1. **Applicable insurance.** CSLB prints a liability line on only a minority of pages (CMAC
   1053452 in wave 16 was the only one); project-specific certificates of insurance are not
   public.
2. **Written non-destructive-first scope.** This exists only in a conversation with the firm.

Both require contacting businesses — which this workspace deliberately does not do (no forms
submitted, no messages sent, no appointments booked). Until that changes, the qualified master
must stay empty. The correct output remains the evidence-linked shortlist and the call order.

### 1.5 Call order

The 9-entry diagnostic call order is unchanged and no wave-16 record was admitted. New City
Construction Company (1023648, active B + C10 + C36 at a 94122 address) is the strongest new
candidate for eventual admission, but it stays out until area dispatch, an attributable
review, or written scope evidence is attached.

## 2. Limitations blocking a successful outcome

- **No exact-task evidence exists publicly for this problem.** "Stuck overflow trip lever
  behind a 1940s wall" is unlikely to appear in a dated, attributable public review for any
  specific firm. The research can prove identity, classification, status, local permit history
  and platform conduct; it cannot prove the one thing the project most wants to know.
- **Address ≠ dispatch.** CSLB addresses and registry rows are mailing or historical permit
  contacts. Nothing in the public record proves a firm currently dispatches to Outer Sunset on
  the day of the job.
- **Platform badges are not credentials.** "Licensed pro" and "Verified License" are platform
  statements; the corpus only ever treats a CSLB read as a licence fact.
- **Single-trade licences.** C36 (plumbing) and C-9/B (drywall/ceiling) are separate
  classifications; the fallback path (opening a ceiling from the unit below and installing an
  access hatch) may need two contractors plus coordination on the inspection before covering.
- **Permit and inspection reality.** Any work that cuts into or removes piping needs a City
  permit and inspection before the ceiling is closed; the governing exemption in SF Plumbing
  Code §104.2 is narrow and condition-dependent, and no site visit is possible from here.
- **Privacy.** Nonpublic project details are excluded from every artifact by policy and by a
  digest test in the test suite. Nothing from the private context may be written into records,
  sources, commit messages, issues or outreach; only the generalized repair objective below is
  ever published.
- **Tenancy context.** Landlord consent, who signs the permit, and restoration expectations
  are open questions that no public source can answer; the corpus stores only the generalized
  repair objective.

## 3. Next-session checklist

```sh
cp reports/research_before_wave16.json /tmp/verify_wave16_snapshot.json   # keep for diffs
# wave 17 candidates: re-query both SF DBI datasets with $offset paging, read new licence
# numbers live at CSLB, then follow the wave-16 scripts as templates:
#   scripts/gen_wave17.py  →  data/wave17.json  →  scripts/merge_wave17.py
npm test && npm run test:monitor
gh pr create --base main --head arena/01a0ac7b-bathtuboverflowsf
```

Also worth doing next session:

- Add a permit-join pass that searches SF DBI permit descriptions for tub/overflow/ceiling
  keywords at 94122 and joins the hits to contractor contacts.
- Grow the review corpus where a platform permits it, and mark every unread panel as a gap —
  never as a neutral finding.
- Keep the 60-row registry limit in mind: page with `$offset` so a capped query is never
  mistaken for a complete pool.
