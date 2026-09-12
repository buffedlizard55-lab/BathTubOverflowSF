# Wave 8 discovery and verification log

**Research date:** 2026-09-12  
**Result:** 50 new records · 23 plumbing-side · 27 restoration-side · 50 direct CSLB reads · 84 sources · 23 selected review excerpts

## 1. Scope and fail-closed outcome

This wave looked for both a diagnostic plumber and restoration capability for a possible wall/ceiling opening or access panel. Repair evidence was treated as relevant only when it supported careful diagnosis, older fixtures, difficult mechanisms, pipe work, or local plumbing history. Restoration evidence was treated separately and includes drywall, sheetrock, framing, water-damage repair, insulation, painting, or cross-trade coordination.

Every new record remains `master=false`, `exactMatch=false`, `insuranceVerified=false`, and `scopeConfirmed=false`. No source established all of the following together: successful extraction of the exact stuck overflow linkage, a non-destructive-first written scope, older galvanized-assembly experience, current Outer Sunset dispatch, and project-specific insurance.

## 2. Official-source method

- **Sources 228–277:** 50 individual CSLB detail pages, read directly on the research date. Legal name, business form, phone, address, status, classifications, displayed expiry, and notable bond/workers-compensation or disclosure lines were transcribed conservatively.
- **[Source 222](https://data.sf.gov/resource/k6kv-9kix.json?%24select=permit_number%2Clicense_number%2Cfirm_name%2Caddress%2Ccity%2Czipcode%2Cphone&%24where=license_number+in+%28%27817607%27%2C%27887553%27%2C%27902830%27%2C%271028751%27%2C%27791342%27%2C%27498866%27%2C%27957727%27%2C%27975509%27%2C%271122605%27%2C%27814802%27%2C%271115284%27%2C%27343837%27%2C%27488896%27%2C%27306841%27%2C%27581431%27%2C%27693052%27%2C%27900145%27%2C%27811534%27%2C%27667361%27%2C%27942224%27%2C%27908590%27%2C%27406739%27%2C%27520892%27%29+and+permit_number+in+%28%27PP20190501385%27%2C%27PW20240812801%27%2C%27PW20190501695%27%2C%27PW20241212759%27%2C%27PW20260320521%27%2C%27PW20221005482%27%2C%27PW20250331196%27%2C%27PP20260813825%27%2C%27PP20080528027%27%2C%27PW20240627846%27%2C%27PP20230517004%27%2C%27PP20120124951%27%2C%27PP20110207859%27%2C%27PP20100621871%27%2C%27PP20080125460%27%2C%27PP20101004304%27%2C%27PP20100930251%27%29&%24limit=100&%24order=license_number%2Cpermit_number):** exact selected plumbing license/permit contact mappings from SF DBI dataset `k6kv-9kix`.
- **[Source 223](https://data.sf.gov/resource/a6aw-rudh.json?%24select=permit_number%2Cstatus%2Ccompleted_date%2Cdescription%2Cstreet_number%2Cstreet_name%2Cstreet_suffix%2Czipcode&%24where=permit_number+in+%28%27PP20190501385%27%2C%27PW20240812801%27%2C%27PW20190501695%27%2C%27PW20241212759%27%2C%27PW20260320521%27%2C%27PW20221005482%27%2C%27PW20250331196%27%2C%27PP20260813825%27%2C%27PP20080528027%27%2C%27PW20240627846%27%2C%27PP20230517004%27%2C%27PP20120124951%27%2C%27PP20110207859%27%2C%27PP20100621871%27%2C%27PP20080125460%27%2C%27PP20101004304%27%2C%27PP20100930251%27%29&%24limit=100&%24order=permit_number):** the selected plumbing permits from `a6aw-rudh`, including `status`, `completed_date`, full description, work address fields, and `zipcode`.
- **[Source 224](https://data.sf.gov/resource/k6kv-9kix.json?%24select=permit_number%2Clicense_number%2Cfirm_name%2Caddress%2Ccity%2Czipcode%2Cphone&%24where=license_number+in+%28%27791342%27%2C%27908590%27%29+and+zipcode+like+%2794122%25%27&%24limit=50&%24order=license_number):** contractor-contact ZIP history for Impressive Plumbing and Almo Plumbing. This is not work-location proof.
- **[Source 225](https://data.sf.gov/resource/3pee-9qhc.json?%24select=permit_number%2Cfirm_name%2Clicense1%2Crole%2Cfirm_address%2Cfirm_city%2Cfirm_zipcode&%24where=license1+in+%28%27850352%27%2C%27361402%27%2C%271090249%27%2C%271002753%27%2C%271082165%27%2C%271119854%27%2C%271141495%27%2C%271142594%27%2C%271022801%27%2C%27944813%27%2C%271064544%27%2C%271132400%27%2C%271018292%27%2C%27855109%27%2C%27937457%27%2C%271008141%27%2C%27773300%27%2C%271072943%27%2C%27697522%27%2C%27701864%27%2C%27592325%27%2C%27900156%27%2C%271108341%27%2C%271057565%27%2C%271031942%27%2C%27754201%27%2C%27998906%27%2C%27343837%27%29+and+permit_number+in+%28%27202605181462%27%2C%27202603318629%27%2C%27202603318559%27%2C%27202603308518%27%2C%27202603258250%27%2C%27202603187849%27%2C%27202603026793%27%2C%27202602045258%27%2C%27202601133757%27%2C%27202512151795%27%2C%27202512081247%27%2C%27202511260567%27%2C%27202511250390%27%2C%27202507140728%27%2C%27202506027697%27%2C%27202505196742%27%2C%27202505075931%27%2C%27202504174635%27%2C%27202501077889%27%2C%27202412187085%27%2C%27202411124782%27%2C%27202411054443%27%2C%27202605141289%27%2C%27202408239341%27%2C%27202410012093%27%2C%27202512111572%27%2C%27202412126731%27%2C%27200408040636%27%29&%24limit=200&%24order=license1%2Cpermit_number):** exact building-contact mappings from `3pee-9qhc`, using the actual fields `firm_name`, `license1`, and `role`.
- **[Source 226](https://data.sf.gov/resource/i98e-djp9.json?%24select=permit_number%2Cstatus%2Ccompleted_date%2Cdescription%2Cstreet_number%2Cstreet_name%2Cstreet_suffix%2Czipcode&%24where=permit_number+in+%28%27202605181462%27%2C%27202603318629%27%2C%27202603318559%27%2C%27202603308518%27%2C%27202603258250%27%2C%27202603187849%27%2C%27202603026793%27%2C%27202602045258%27%2C%27202601133757%27%2C%27202512151795%27%2C%27202512081247%27%2C%27202511260567%27%2C%27202511250390%27%2C%27202507140728%27%2C%27202506027697%27%2C%27202505196742%27%2C%27202505075931%27%2C%27202504174635%27%2C%27202501077889%27%2C%27202412187085%27%2C%27202411124782%27%2C%27202411054443%27%2C%27202605141289%27%2C%27202408239341%27%2C%27202410012093%27%2C%27202512111572%27%2C%27202412126731%27%29&%24limit=100&%24order=permit_number):** selected building permits from `i98e-djp9`, including `status`, `completed_date`, description, and work ZIP.
- **[Source 227](https://data.sf.gov/resource/i98e-djp9.json?%24select=permit_number%2Cstatus%2Ccompleted_date%2Cdescription%2Cstreet_number%2Cstreet_name%2Cstreet_suffix%2Czipcode&%24where=permit_number%3D%27200408040636%27&%24limit=10):** a separately retained 2004 completed building permit for Frank J O’Brien.
- **Sources [302](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/ComplaintDisclosure.aspx?LicType=LIC&LicNum=814802), [303](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/ComplaintDisclosure.aspx?LicType=LIC&LicNum=306841), and [304](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/ComplaintDisclosure.aspx?LicType=LIC&LicNum=1108341):** direct CSLB disclosure pages for records whose detail pages link or report a complaint, disciplinary, or pending-citation issue.
- **[Source 305](https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_building/0-0-0-85830):** the current San Francisco Plumbing Code §104.2 page, read directly after following the official SF.gov permit-page link.

A contact mapping and a permit-detail row were both required before a selected permit was attached. The merge gate rejects the obsolete `status_date` field, rejects the wrong building-contact field names, and checks that every City URL uses `data.sf.gov`.

## 3. Fifty-record line check

`94122 record` below means either a selected completed work-location permit or, where stated, regulator-recorded business-address evidence. It is historical/local evidence, never a promise of current dispatch.

| # | Business | CSLB | Status | Classes | Declared lane | 94122 record | Flags |
| ---: | --- | ---: | --- | --- | --- | --- | --- |
| 1 | Holland Plumbing Works | [817607](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=817607) | active | C36 | plumbing | `PP20190501385` · 2019-05-06 · replacement of main sewer | — |
| 2 | Glenn's Plumbing | [887553](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=887553) | active | C36 | plumbing | `PW20240812801` · 2024-08-16 · replace sewer lateral and water-main services | — |
| 3 | R E M Boiler and Plumbing | [902830](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=902830) | active | C-4, C36 | plumbing | `PW20190501695` · 2019-08-26 · install bypass backflow on existing fire-service backflow | — |
| 4 | Panhandle Plumbing | [1028751](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1028751) | active | C36 | plumbing | `PW20241212759` · 2025-05-07 · remodel bathroom and kitchen and add a bathroom | — |
| 5 | Impressive Plumbing | [791342](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=791342) | active | C36 | plumbing | contact ZIP history only | — |
| 6 | O'Connor Plumbing & Fire Protection Inc | [498866](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=498866) | active | C16, C36 | plumbing | `PW20260320521` · 2026-09-02 · half-bath/powder-room and roof-drain work | notice |
| 7 | Flow Form Plumbing | [957727](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=957727) | active | C36 | plumbing | `PW20221005482` · 2022-10-14 · reopened final for kitchen waterlines and bathroom-sink waste line | — |
| 8 | L & Y Plumbing | [975509](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=975509) | active | C36 | plumbing | `PW20250331196` · 2025-04-08 · replace 25 feet of sewer pipe and a house trap | — |
| 9 | Axion Plumbing | [1122605](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1122605) | active | C36 | plumbing | `PP20260813825` · 2026-08-18 · house-trap replacement and possible main-line spot repair | discrepancy |
| 10 | Chen's Construction and Mechanical Inc | [814802](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=814802) | active | A, B, C10, C16, C20, C36, C38 | plumbing | `PP20080528027` · 2008-10-15 · four new bathrooms, water piping, tubs and shower fixtures | notice, discrepancy |
| 11 | DC Plumbing LLC | [1115284](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1115284) | active | C36 | plumbing | `PW20240627846` · 2024-09-26 · repair sewer line and house trap | — |
| 12 | Frank J O'Brien | [343837](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=343837) | active | B, C10, C36 | multi-trade | `200408040636` · 2004-09-13 · kitchen remodel | — |
| 13 | Peter So Company | [488896](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=488896) | active | B, C36 | multi-trade | `PP20230517004` · 2023-05-30 · legalization work in a kitchen area | — |
| 14 | Shek's Plumbing | [306841](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=306841) | revoked | C36 | plumbing | no selected completed join | hold |
| 15 | Le's Plumbing & Construction Co | [581431](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=581431) | suspended | C36, B | multi-trade | `PP20120124951` · 2012-06-21 · new kitchen, bathroom, powder-room, laundry and gas-line plumbing | hold |
| 16 | Applied Plumbing Company | [693052](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=693052) | expired | C36 | plumbing | no selected completed join | hold |
| 17 | Morrison Plumbing | [900145](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=900145) | expired | C36 | plumbing | `PP20110207859` · 2011-04-19 · commercial sinks, grease trap, floor drain and gas line | hold |
| 18 | Walsemann Mechanical | [811534](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=811534) | expired | C36 | plumbing | `PP20080125460` · 2008-02-21 · kitchen remodel | hold |
| 19 | City Construction Inc | [667361](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=667361) | expired | B, C10, C36 | multi-trade | `PP20100930251` · 2011-03-01 · gas line and ground-floor kitchen/bathroom remodeling | hold |
| 20 | Tully Plumbing | [942224](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=942224) | inactive | C36 | plumbing | `PP20100621871` · 2010-06-21 · new sewer in the street | hold |
| 21 | Almo Plumbing | [908590](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=908590) | inactive | C36 | plumbing | contact ZIP history only | hold |
| 22 | Polytec Construction Company Inc | [406739](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=406739) | canceled | B, C16, C20, C38, C36, A, C10 | multi-trade | `PP20101004304` · 2010-10-12 · kitchen, bathroom and laundry-room water-pipe work | hold |
| 23 | Meridian Plumbing Company Inc | [520892](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=520892) | canceled | C16, C36 | plumbing | no selected completed join | hold |
| 24 | Bay Metro Corporation | [850352](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=850352) | active | B, C36 | multi-trade | `202605181462` · 2026-08-14 · fire-damage framing and drywall repair | — |
| 25 | Sarris Construction | [361402](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=361402) | active | B | general | `202603318629` · 2026-06-24 · remove plaster ceiling and install drywall | — |
| 26 | Pro-Care Restoration Inc | [1090249](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1090249) | active | B, C22 | general | `202603318559` · 2026-09-08 · water-damage drywall, tape, texture and paint | discrepancy, notice |
| 27 | Buck Construction | [1002753](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1002753) | active | B | general | `202603308518` · 2026-07-10 · new drywall, tape and smooth finish | — |
| 28 | Safe Step Walk In Tub LLC | [1082165](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1082165) | active | B | general | `202603258250` · 2026-05-13 · tub work and drywall patching | — |
| 29 | Raxe Construction Inc | [1119854](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1119854) | active | B | general | `202603187849` · 2026-06-30 · tub relocation, new drywall and insulation | notice |
| 30 | Brus Box Contractor Works | [1141495](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1141495) | active | B | general | `202603026793` · 2026-09-03 · drain/supply, bathroom, framing and drywall work | hold, notice |
| 31 | O'Neil Engineering Inc | [1142594](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1142594) | active | A, B | general | `202602045258` · 2026-07-17 · in-kind drywall and roof-ceiling repair | — |
| 32 | Precise Construcion | [1022801](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1022801) | active | B | general | `202601133757` · 2026-03-30 · old/new sheetrock and small framing work | — |
| 33 | Solid Design Construction | [944813](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=944813) | active | B | general | `202512151795` · 2026-01-02 · wall and ceiling sheetrock | — |
| 34 | Kelun Construction | [1064544](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1064544) | active | B | general | `202512081247` · 2026-03-10 · ceiling drywall replacement | — |
| 35 | RPRW Inc dba James Macmillan | [1132400](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1132400) | active | B | general | `202511260567` · 2026-01-02 · remediation with drywall removal and replacement | hold |
| 36 | Bold Restoration Inc | [1018292](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1018292) | active | B, C-2, D39, C33 | general | `202511250390` · 2026-01-28 · water-damage drywall on walls and ceilings | — |
| 37 | Yong Hong Construction Inc | [855109](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=855109) | active | B | general | `202507140728` · 2025-12-05 · bath remodel with wall/ceiling drywall removal and replacement | — |
| 38 | Cleanair Image Inc dba Servpro of Belmont / San Carlos | [937457](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=937457) | active | B | general | `202506027697` · 2025-09-02 · approximately 1,600 square feet of drywall | — |
| 39 | Blue Wood Construction Inc | [1008141](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1008141) | active | B, C-7, C10, C36 | multi-trade | `202505196742` · 2026-06-04 · bathroom work and sheetrock | — |
| 40 | Constantine Construction | [773300](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=773300) | active | B, C36 | multi-trade | `202505075931` · 2025-08-21 · kitchen sheetrock with plumbing/electrical work | — |
| 41 | BAA General Builder | [1072943](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1072943) | active | B, C36 | multi-trade | `202504174635` · 2025-05-16 · framing to cover duct and drywall | — |
| 42 | Kobliska Construction | [697522](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=697522) | active | B | general | `202501077889` · 2025-05-07 · bathroom rebuild with plumbing, drywall and tile | — |
| 43 | Spotlight Construction Groups Inc | [701864](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=701864) | active | B, D34 | general | `202412187085` · 2025-02-11 · mold/damaged sheetrock and repair after plumbing leakage | — |
| 44 | Hargens Inc | [592325](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=592325) | active | B, C33, C43, C20, C36 | multi-trade | `202411124782` · 2025-02-06 · water-damage drywall repair and plumbing-leak repair | discrepancy |
| 45 | Simply Building Inc | [900156](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=900156) | active | B, C36, C15 | multi-trade | `202411054443` · 2025-07-22 · bathroom/kitchen work and wall/ceiling sheetrock | — |
| 46 | Gerson Construction Inc | [1108341](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1108341) | active | B | general | `202605141289` · 2026-08-19 · exploratory ceiling demolition for design drawings | hold |
| 47 | Alpha Construction & Solutions Inc | [1057565](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1057565) | active | B, C10, C36 | multi-trade | `202408239341` · 2025-03-21 · sheetrock, bathroom and insulation work | — |
| 48 | Winwin Construction Inc | [1031942](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=1031942) | active | B | general | `202410012093` · 2025-03-31 · multiple-bathroom remodel work | — |
| 49 | Wolfe Painting Co | [754201](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=754201) | active | C33, B | general | `202512111572` · 2026-07-30 · wall/ceiling demolition and patching after electrical work | hold |
| 50 | Yong and Zhuo Construction Inc | [998906](https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum=998906) | active | B | general | `202412126731` · 2025-09-15 · kitchen/bathroom work and sheetrock | — |

### Permit-selection totals

- **17 plumbing licenses** have an exact source-222 contact mapping and a selected completed source-223 permit at work ZIP 94122.
- **27 restoration licenses** have an exact source-225 contact mapping and a selected completed source-226 permit at work ZIP 94122.
- **Frank J O’Brien** has a separate exact source-225/source-227 mapping for completed permit `200408040636` (2004-09-13, ZIP 94122). It is not counted among the 27 restoration selections.
- The plumbing query can return two work-address rows for one permit; permits are counted by unique permit number, not raw row count.

## 4. Review and platform pass

| Business | Retained | Platforms / source IDs | Conservative result |
| --- | ---: | --- | --- |
| Holland Plumbing Works | 2 | Yelp [280](https://www.yelp.com/biz/holland-plumbing-works-san-francisco); Citysearch via Judy's Book [281](https://www.judysbook.com/Holland-Plumbing-Works-BtoB~Plumbing-Contractors-sanfrancisco-r29770409.htm) | Repeat plumbing service, Shower-handle mechanism repair; every excerpt remains `exactTask=false` |
| Panhandle Plumbing | 1 | BuildZoom [282](https://www.buildzoom.com/contractor/panhandle-plumbing-san-francisco-ca) | Small-project willingness; every excerpt remains `exactTask=false` |
| Flow Form Plumbing | 1 | Yelp [279](https://www.yelp.com/biz/flow-form-plumbing-san-francisco-3) | Older tub fixtures; every excerpt remains `exactTask=false` |
| Axion Plumbing | 2 | Nextdoor [284](https://nextdoor.com/pages/axion-plumbing-san-francisco-ca/) | Bathroom diagnosis, Communication; every excerpt remains `exactTask=false` |
| Bay Metro Corporation | 3 | GuildQuality [290](https://www.guildquality.com/profile/bay-metro-corporation) | Repair reliability, Trade coordination, Repeat intent; every excerpt remains `exactTask=false` |
| Pro-Care Restoration Inc | 7 | Google via Birdeye [287](https://reviews.birdeye.com/pro-care-restoration-inc-171673259657633); Yelp via Yahoo [288](https://local.yahoo.com/info-235468637-procare-restoration-hayward/) | Complex restoration, Bathroom remediation, Multi-room restoration, Repeat restoration work, Leak mitigation, Mold remediation, Business-practices allegation; every excerpt remains `exactTask=false` |
| Brus Box Contractor Works | 3 | Yelp via Yahoo [294](https://local.yahoo.com/info-232677711-brus-box-contractor-works-san-francisco/) | Fixture and cross-trade work, Opening/restoration work, Plumbing fixture replacement; every excerpt remains `exactTask=false` |
| Hargens Inc | 4 | Business site [296](https://www.hargensinc.com/); Yelp [297](https://www.yelp.com/biz/hargens-south-san-francisco-2) | Restoration testimonial, Project guidance, Crew conduct, Response-time concern; every excerpt remains `exactTask=false` |

### What was actually accessible

- **Flow Form:** one indexed Yelp excerpt plus business/profile content about older fixtures and avoiding tile work on an old valve. The complete Yelp corpus was not read.
- **Holland:** one reproducible indexed Yelp excerpt and both reviews displayed directly on Judy’s Book. One selected Citysearch-fed account concerns a shower-handle mechanism; the other displayed review concerns a water heater and was read but not selected.
- **Panhandle:** one directly displayed BuildZoom review; BuildZoom’s score was not substituted for CSLB.
- **Axion:** two indexed Nextdoor recommendations matched by license, address, website, and phone evidence. The full Nextdoor corpus was not read.
- **Pro-Care:** five Birdeye rows represented only three unique texts because two pairs were verbatim duplicates. Four dated, truncated Yahoo-hosted Yelp-fed excerpts were also retained, including one unsubstantiated negative allegation.
- **Bay Metro:** three dated GuildQuality excerpts were available in indexed results; the complete survey corpus was not exposed.
- **Brus Box:** three task-adjacent Yahoo-hosted Yelp-fed excerpts were retained. They do not establish who lawfully performed plumbing under a B-only license.
- **Hargens:** one company-hosted rebuilding testimonial and three indexed Yelp highlights were retained. The testimonial is labeled `company-published`.

No original Google review panel was retrieved. Three Google-attributed Pro-Care texts are labeled **Google via Birdeye**, not original Google reads. No safely attributable wave-8 Reddit or Thumbtack review was found. Those channels are recorded as checked but incomplete, not as zero-review corpora.

## 5. Entity resolution, collisions, and rejections

The generator’s final cohort and `scripts/merge_wave8.py` both check normalized names, suffix-stripped near-names, ten-digit phones, CSLB numbers, business IDs, source IDs, and review IDs. The merge refused any overlap with the 351-record baseline.

- **Oran Plumbing #762214** — rejected because the license number already existed in the merged dataset.
- **New Golden State Plumbing #778200** — rejected because the license number already existed.
- **Euro Plumbing #1028917** — rejected because the regulator’s legal identity did not match the discovery identity safely enough for attachment.
- **National Safe Step BBB/ConsumerAffairs corpora (sources 300–301)** — retained only as rejection evidence; California contracting-entity continuity was not established.
- **Unrelated “DC Plumbing” pages** — rejected because they did not safely match license 1115284.
- Search-index text naming another person/business was not reassigned to a nearby result.

## 6. Irregularities preserved

- **O’Connor #498866:** CSLB shows a 2026-04-02 reissue to another entity. The selected permit completed 2026-09-02; confirm the current contracting corporation.
- **Chen #814802:** source 222’s 2008 permit contact uses an earlier firm name and predates CSLB’s 2020 reissue to the current corporation. The permit proves license-number history only.
- **Axion #1122605:** CSLB prints `415-672-0249`; the official site/matched profile print `415-286-3451`.
- **Pro-Care #1090249:** duplicate review texts were deduplicated; multiple street addresses are published; one negative excerpt remains an allegation.
- **Brus Box #1141495:** markets plumbing but CSLB lists B without C-36; its displayed workers-compensation date had passed by the research date.
- **RPRW #1132400:** CSLB displayed workers-compensation cancellation dated 2026-08-26.
- **Raxe #1119854:** displayed workers-compensation expiry equals the research date.
- **Gerson #1108341:** CSLB says a citation is pending and cautions against assuming an outcome; the record is held.
- **Wolfe #754201:** near-term license expiry and displayed workers-compensation cancellation require a fresh check.
- **Hargens #592325:** CSLB/official-site address differs from older Yelp/Nextdoor address; exact phone/name support continuity but do not resolve current contracting location.
- **Shek #306841:** revoked and held; source 303 was read directly.
- Every expired, suspended, canceled, inactive, or revoked record has a hold-level flag.

## 7. Three additional verification passes

1. **Pass 16 — line-by-line source verification.** Rechecked all 50 CSLB identities/statuses/classes/expiries and every selected permit mapping, date, complete status, work ZIP, and scope condensation.
2. **Pass 17 — collision and attribution verification.** Re-ran full baseline collisions; reproduced the Holland excerpts; deduplicated Pro-Care; checked review identity continuity; logged rejected Reddit, Thumbtack, national, and name-mismatched corpora.
3. **Pass 18 — fail-closed publication verification.** Rechecked status/classification/coverage holds; re-read SF.gov and Code §104.2; scrubbed public artifacts; ran structural, render, monitor, browser, source, and privacy checks.

## 8. Remaining unknowns

- No business was contacted; current availability and dispatch remain unknown.
- No source confirms the exact seized overflow/trip-lever mechanism or guarantees extraction without opening finishes.
- No selected source proves experience with the exact hidden galvanized assembly likely to be encountered.
- Permit history does not prove present insurance or allocate every task among all permit contacts.
- A B license does not by itself establish C-36 self-performance; records marketing plumbing without C-36 are flagged.
- Review identities and transactions are not independently authenticated.
- Platform corpora remain incomplete wherever access was blocked, truncated, indexed, republished, or dynamically unavailable.

## 9. Reproducibility

```sh
python3 scripts/gen_wave8.py
python3 scripts/merge_wave8.py
npm test
python3 -m unittest discover -s tests -p "test_*.py"
npm run test:browser
```

The merge is idempotent after success and preserves an empty qualified master unless every promotion gate is affirmatively supported.
