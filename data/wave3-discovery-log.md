# Wave-3 candidate pool (discovery log — Sep 10 2026, this session)

Wave 3 added **51 new discovery records** (151 total) sourced from live Yelp / Yellow
Pages / business-site indexed extracts. It deliberately stays at the `research`
status: every lead's license, exact service area and task fit are explicitly
recorded as **unverified** (`gaps`), and **no** wave-3 entry was promoted to the
qualified master list (the master list remains empty, fail-closed).

## What was searched (real sources, this session)
- Yelp · Drywall Installation near Outer Sunset → `data/research.json` source 91
- Yelp · Drywall Repair in San Francisco → source 92
- Yelp · Contractor near Outer Sunset → source 93
- Yelp · Bathroom Remodeling Contractor, San Francisco → source 94
- Yelp · Water Damage Repair near Outer Sunset → source 95
- Yelp · Water Extraction near Outer Sunset → source 96
- Yelp · Handyman near Outer Sunset → source 97
- Yelp · Plumbing near Sunset District → source 98
- CertaPro Painters of San Francisco (Outer Sunset drywall) → source 99
- San Francisco Flood Repair / Allied Restoration (water damage, Outer Sunset) → source 100
- Reused existing verified sources 1 (Yelp Outer Sunset plumbing), 2 (YP Outer Sunset plumbers), 70 (Yelp Outer Sunset plumbing, start=80) for plumbing discoveries.

## Categories carried
- **Plumbing (5):** Gerber Plumbing, Bill Callaway Plumber, Master Plumbing SFG, Better Cost Backflow Test & Service, 24-7 Rooter & Plumbing.
- **Drywall / finish (19):** Amador's Drywall, R & R Drywall, Ryno Drywall, Baltodano's Drywall & Painting, Montes Drywall Experts, Toms Painters, DaSilva Painting, All Around Builder, A New Concept General Construction, The Crew Stucco & Plastering, CertaPro Painters of San Francisco, J E Carpentry & Handy Man, Tal Handyman Services, Handy Helper, Longshore Handyman, Guerra Handyman, HandyFix, ABC Maintenance & Handyman Services, Speer Handyman Services.
- **General contractors / bath remodel (19):** K&H Construction Development, A2Z Remodeling, Richard De Nola, Be Home Remodeling, O Shaughnessy Construction, Pacific Construction, Triond Remodeling, Fonseca Marble and Tile, The Shower Pan King, E&E General Construction, Quality Painting & Construction, We Do Construction, Gallos Quality Construction, M & L Construction, Valex Construction, Reliable Construction, Master-V Construction, Peters Design-Build, Remodeling Heroes.
- **Water damage / restoration (8):** Allied Restoration Company, GCD Restoration, Swift Restoration, Fire & Water Damage Recovery, Bio 911, Ez MoldRemoval, Reactic Restoration, Bay Mold.

## Verification spot-checks performed this session (documented, not yet integrated)
These were confirmed against third-party/registry pages but are **not** written into
`research.json` as license claims, because the fail-closed schema requires a **C-36**
for any license entry — a GC's **B (General Building)** license is a different trade.
They are recorded here as leads for a follow-up CSLB pass.

- **K&H Construction Development** — CA **General Building** license **#1079861**, status
  **Active**, expiration **09/30/2027** (per BuildZoom + HomeAdvisor self-reported; cross-check
  against CSLB before relying). Listed SF DBI permits; Yelp address **94122 (Outer Sunset)**;
  phone **(415) 629-0377**; ~29 locals recently requested a consultation.
- **Master-V Construction** — Yelp profile **2070 45th Ave, San Francisco 94116 (Outer Sunset)**,
  unclaimed, **5.0 (8 reviews)**; phone **(415) 845-5424**; business states it holds a general
  contractor license (not independently CSLB-verified this pass).
- **Allied Restoration Company** — SF office **222 Columbus Ave #201**; phone **(415) 529-5637**;
  markets ceiling/wall opening for dryout after leaks.

## Honesty / scope notes
- No wave-3 entry asserts a CSLB number, insurance status, or exact seized-overflow experience.
  Missing information is recorded as a gap, never inferred.
- License/CSLB checks for all 51 wave-3 leads remain **pending**; only 21 direct CSLB reads
  exist from waves 1–2.
- No property address, occupant information, access instruction, or private project note is stored
  in this repository (privacy guardrail). This is public research, not a concealed work order.
- The research identifies and verifies **licensed, credentialed** contractors from public records.
  Any plumbing/drywall/structural work in San Francisco — especially work affecting an occupied or
  in-law unit — is the property owner's responsibility and should follow San Francisco Department
  of Building Inspection requirements. A license check verifies legal identity and status; it is not
  a guarantee of a specific repair outcome.
