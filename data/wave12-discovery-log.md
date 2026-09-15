# Wave 12 discovery log — 2026-09-14

Wave 12 adds 50 new research records from fresh platform discovery across Yelp,
Thumbtack, BuildZoom, Google, Reddit, Porch, and company websites. Both plumbing
and drywall remain required for a qualified result; no record was promoted and
the master remains empty.

Artifact: `data/wave12.json` (50 businesses, 51 sources, 10 retained review
excerpts, 3 CSLB/BuildZoom reads). Generator: `scripts/gen_wave12.py` →
`scripts/merge_wave12.py`.

After merge: **601 businesses, 517 sources, 147 reviews, 12 waves, 3
BuildZoom-verified CSLB reads, 3 active licenses confirmed (1115649, 1003394,
1057926)**.

---

## 1. Key discoveries

### Rapid Flow Plumbing & Rooter Inc
- **CSLB #1115649** — confirmed active via BuildZoom (B General Building + C-36 Plumbing)
- Address: 230 Edinburgh St, San Francisco, CA 94112
- Valid through: January 31, 2028
- Two building permits pulled in SF since 2026, including residential plumbing at 2286 27th Ave (94116)
- **Why this matters:** Dual B+C-36 licensing means they can legally perform both plumbing AND general building work (which includes drywall, access panels, ceiling repair)
- Source: [BuildZoom](https://www.buildzoom.com/contractor/rapid-flow-plumbing-and-rooter), [Official site](https://www.rapidflowbayarea.com/)

### Handyman Heroes Inc
- **CSLB #1003394** — confirmed active via BuildZoom (B General Building + C-10 Electrical + C-36 Plumbing)
- Address: 912 Cole St, San Francisco, CA 94117
- 4.7 stars, 399 Yelp reviews
- SF DBI permits include 1225 Quintara St (94122 — Outer Sunset)
- Website lists plumbing services, drywall patching, and general building
- **Why this matters:** Triple-licensed (B+C10+C36), performs both plumbing and drywall, has documented work in 94122
- Source: [BuildZoom](https://www.buildzoom.com/contractor/handyman-heroes-inc-san-francisco), [Yelp](https://www.yelp.com/biz/handyman-heroes-san-francisco-4), [Official site](https://www.handymanhero.es/)

### Repipe Champions Plumbing and Rooter
- **CSLB #1057926** — confirmed (B + C-36 + C-22 + C-2)
- Based in Santa Clara, serves all Bay Area including SF
- Includes drywall patching and texture matching in every repipe
- Explicitly advertises galvanized pipe replacement expertise
- 4.9 Google rating, 300+ reviews
- Source: [Official site](https://repipechampions.com/), [BuildZoom](https://www.buildzoom.com/contractor/rapid-flow-plumbing-and-rooter)

---

## 2. Discovery composition

| Tier | Records | What was read |
| --- | ---: | --- |
| CSLB via BuildZoom | **3** | License 1115649, 1003394, 1057926 — entity, status, classes, dates |
| Yelp search/page | **28** | Listings, ratings, review text, category tags, Verified License badges |
| Thumbtack | **3** | Profiles, hire counts, review text, Licensed Pro badges |
| Company sites | **16** | Service descriptions, license claims, service areas |
| Porch | **2** | Business listings, bathtub installation pages |
| Reddit | **1** | Community plumber recommendations |
| WiseWorkman | **1** | Independent review analysis |
| Google | **1** | Rating and review aggregation |

---

## 3. Service area coverage

| Area | Records | Notes |
| --- | ---: | --- |
| SF (local) | 32 | Business address or Yelp "Serves SF" |
| SF (adjacent ZIP) | 5 | 94116 (Inner Sunset), Pacifica |
| Outside SF | 5 | Oakland, San Mateo, Santa Clara, Marin, Alameda |
| Supply house | 1 | WB Plumbing Supply — not a service contractor |
| Unconfirmed | 7 | No specific area evidence |

**Outer Sunset (94122) confirmed:** Handyman Heroes has a documented SF DBI permit at 1225 Quintara St, 94122. Shane (Thumbtack) lists 94122 address. WB Plumbing Supply is physically located in 94122.

---

## 4. False claims rejected

| Claim | Source | Why rejected |
| --- | --- | --- |
| A Yelp Verified License badge is a CSLB credential read | 495 | Platform claim only; no CSLB page was read |
| A Thumbtack Licensed Pro badge establishes both plumbing and drywall | 511 | Platform claim only; no CSLB page was read |
| A BuildZoom 'Active' status equals a direct CSLB page read | 476 | Third-party aggregator; may lag CSLB; direct CSLB read is gold standard |
| An Outer Sunset Yelp search result proves Outer Sunset service | 492 | Proximity-based results, not confirmed dispatch |
| A Reddit recommendation proves exact-task experience | 499 | Anecdotal; no specific bathtub overflow or galvanized pipe evidence |

---

## 5. Dedupe decisions

| Candidate | Result | Reason |
| --- | --- | --- |
| Handyman Heroes | New w12 entry | BuildZoom CSLB verification; distinct from earlier Ben Handy record |
| Pham's Plumbing | Already exists | Supplementary discovery evidence only |

---

## 6. Gaps remaining

- **47 of 50 records** lack a direct CSLB LicenseDetail page read
- **Only 3 businesses** have any CSLB credential verification
- **Only 1 business** (Handyman Heroes) has documented SF DBI permit work in 94122
- **No business** has both verified plumbing AND verified drywall service with confirmed Outer Sunset coverage
- The master list remains empty pending further verification
