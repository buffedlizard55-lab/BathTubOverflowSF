# Wave 11 discovery log — 2026-09-12

Wave 11 adds 50 new research records and three verification upgrades. It ran
three additional fail-closed verification passes (Passes 25, 26 and 27). No
record was promoted, assigned a priority, or added to the qualified master; the
master remains empty.

Artifact: `data/wave11.json` (50 businesses, 66 sources, 4 retained review
excerpts, 3 verification upgrades, 10 dedupe rejections). Generators:
`scripts/gen_wave11.py` → `scripts/merge_wave11.py`.

After merge: **551 businesses, 466 sources, 137 reviews, 11 waves, 215
CSLB detail-page reads, 144 active licences, 70 non-active licences**. The
wave's 42 directly read licences split into 28 active and 14 non-active; every
non-active record remains held.

---

## 1. Discovery composition and hard boundaries

The wave deliberately kept three evidence channels separate. Both plumbing and
drywall remain required for a qualified result; a single trade, a registry
number, a platform badge, or a general bathroom-remodeling claim cannot satisfy
that requirement.

| Tier | Records | What was read | What the record may assert |
| --- | ---: | --- | --- |
| CSLB read directly | **42** | Each `LicenseDetail.aspx` page was opened and transcribed field by field | The regulator-published entity, address, phone, status, dates, classifications and displayed credential details |
| Registry only | **4** | Official City permit-contact registries | A recorded firm name, address, phone, licence number and permit identifiers — not a CSLB status or classification |
| Platform listing | **4** | Thumbtack's San Francisco bathroom-remodeling category page | The platform's own listing, category, hire/review text or badge — not an independent licence fact |

All 50 records remain outside the call order and qualified master. The 42
licence reads are research evidence, not proof of current Outer Sunset dispatch,
insurance, exact-task experience, or a complete two-trade scope.

The four registry-only records have `license: null` and
`trade: "registry-lead"`. They are structurally unable to reach the master list
until their licence number is read directly and the remaining gates are met.
The four platform records also have no CSLB fact, even where a platform displays
a “Licensed pro” badge. Their four attached review excerpts are retained as
platform evidence with `exactTask: false`.

---

## 2. Sources and discovery channels

The wave added 66 source objects. Source IDs are intentionally not contiguous;
the artifact preserves the gaps in the source-number trail between channel
reads.

| Source IDs | Channel | Limitation recorded in the dataset |
| --- | --- | --- |
| 401–442 | [CSLB License Detail](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=593386) and 41 parallel numbered pages | Direct regulator facts for the licence number shown on each page; a CSLB page does not certify the job, current dispatch, insurance or drywall coverage |
| 443–444 | [CSLB complaint disclosures](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/ComplaintDisclosure.aspx?LicType=LIC&LicNum=766142) | A disclosure is preserved as displayed and is not converted into an unsupported conclusion |
| 445–448 | [SF DBI plumbing contact registry](https://data.sf.gov/resource/k6kv-9kix.json) and [building contact registry](https://data.sf.gov/resource/3pee-9qhc.json) | Official registry rows identify recorded contacts and historical permit counts; a queried ZIP is not a service-area confirmation |
| 449 | [Thumbtack San Francisco bathroom-remodeling category](https://www.thumbtack.com/ca/san-francisco/bathroom-remodeling) | Category listings and badges are platform claims; they do not substitute for a CSLB read or establish Outer Sunset coverage |
| 450, 452–455, 458–461, 464–465, 468–470 | Public directory, review-mirror and company pages used for identity or task-context checks | Search extracts, directories and mirrors remain attributed to their publisher; they cannot upgrade a licence or make a review exact-task evidence |
| 472–474 | [AMX CSLB read](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=822482), [Sugar Bear CSLB read](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=876480), [A-1 CSLB read](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=0454201) | Verification upgrades attached to existing records; they are not new businesses |

The registry discovery pool used adjacent ZIP records. The merge therefore
leaves every wave-11 area value outside the Outer Sunset label. A historical
registry address is retained as discovery context only and is never rewritten as
present dispatch coverage.

No business was contacted, no access control was bypassed, and no inaccessible
review text was reconstructed. New review excerpts were limited to four
Thumbtack-attributed records (R134–R137); no Google or Reddit text was promoted
into a wave-11 review.

---

## 3. Dedupe decisions and upgrades

The pre-flight and merge gates checked IDs, exact names, normalized names,
phones, licence numbers, source IDs, review IDs, classification coverage and
privacy boundaries before writing the dataset. Ten surfaced names were rejected
as new records:

| Candidate | Result | Reason |
| --- | --- | --- |
| Heise's Plumbing | Existing `heises` | Same phone and CSLB-linked entity; the older page was not added as a parallel row |
| Astorga Construction | Existing wave-11 active record | The expired 309814 predecessor is retained separately from active 1008360, rather than merged by name alone |
| Anderson Roofing & Sheet Metal | Existing wave-11 active record | The canceled 146802 predecessor is retained separately from active 797144 |
| AMX Plumbing | Existing `amx` | CSLB evidence became a verification upgrade |
| Sugar Bear Plumbing | Existing `sugar-bear` | CSLB evidence became a verification upgrade |
| A-1 Plumbing | Existing `a1-plumbing` | CSLB evidence became a verification upgrade |
| Deng's Plumbing Company | Existing `w11-dengs-plumbing` | Directory name variant resolved to the directly read CSLB identity |
| Hong Wei Construction | Existing `w11-hong-wei-construction` | Directory name variant resolved to licence 946861 |
| West Bay Plumbing | Existing `w11-west-bay-plumbing` | BBB and BuildZoom pages support the same CSLB identity |
| Jin's Plumbing | Existing `w11-jins-plumbing` | Directory and review pages resolve to licence 877300 |

The three upgrades are additive and retain their original record IDs and
history:

- `amx` → active C36, licence 822482, CSLB source 472.
- `sugar-bear` → expired C36, licence 876480, CSLB source 473; held because
  the status is non-active.
- `a1-plumbing` → active C36, licence 0454201, CSLB source 474; the upgrade
  does not establish Outer Sunset dispatch or drywall evidence.

No duplicate was silently renamed, merged, or counted as a new business.

---

## 4. Three fail-closed verification passes

### Pass 25 — discovery and evidence tiering

The discovery pool was queried from the official SF DBI plumbing and building
contact registries, then candidates were separated into direct regulator reads,
registry-only leads, and platform listings. The merge retained the distinction
on every record. A registry number was never treated as a licence fact, and a
platform badge was never treated as a CSLB credential.

### Pass 26 — regulator, identity and source audit

Each selected CSLB page was checked line by line for entity name, licence
number, status, dates, address, phone and classification. The merge required a
matching government URL and licence number, rejected licence/name/phone/source
collisions, checked that trade labels are supported by the recorded classes, and
held every non-active status. New source metadata, citations, review IDs and
privacy-sensitive text were checked before the merge could write.

### Pass 27 — attribution, qualification and render boundary audit

Review business IDs, platform attribution, source links and quoted excerpts
were checked separately. The final gate confirmed that every wave-11 record has
an unresolved gap, no record has an exact-match, insurance, scope-confirmed,
master or priority assertion, and no non-active record is presented as
bookable. The required plumbing-plus-drywall condition remains a hard gate.

The passes are intentionally conservative: they preserve irregularities for
manual review rather than reconciling conflicting names, addresses, phone
numbers, categories or review text by assumption.

---

## 5. Irregularities retained for manual review

- An active class or a local registry row does not establish current service in
  the Outer Sunset. The wave's adjacent-ZIP area evidence remains outside and
  is shown with its source link.
- Several directly read licences are specialty, general-building, roofing or
  other scope exclusions. They remain visible with their regulator class and
  are not presented as plumbing-plus-drywall matches.
- Astorga Construction has an active licence and a separate expired predecessor;
  Anderson Roofing likewise has active and canceled predecessor records. The
  merge keeps each licence identity separate.
- Jin's Plumbing has adjacent plumbing evidence in a review mirror, but the
  excerpt does not establish drywall or the exact repair task; it remains
  research-only.
- The four platform excerpts describe general bathroom-remodeling work and are
  marked non-exact. Sentiment, hire counts and “Licensed pro” badges are not
  blended into regulator facts.
- The Daniel P Heath replacement read is canceled and held; it is not a
  recommendation.

These are evidence boundaries, not conclusions about workmanship or intent.

## Rebuild

On a clean wave-10 baseline:

```sh
python3 scripts/gen_wave11.py
python3 scripts/merge_wave11.py
npm test
```

The merge is fail-closed and idempotent only when starting from its expected
pre-wave-11 dataset. It refuses to write if any tier boundary, source link,
identity collision, licence status, classification, review attribution,
upgrade, or privacy gate fails.
