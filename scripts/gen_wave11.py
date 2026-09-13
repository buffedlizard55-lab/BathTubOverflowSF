#!/usr/bin/env python3
"""Generate the fail-closed wave-11 evidence artifact.

This wave sweeps adjacent official SF DBI permit-contact registries, reads each
selected CSLB detail page directly, and keeps registry leads and platform
listings separate from regulator evidence. It does not promote any record.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "wave11.json"
DATE = "2026-09-12"
CSLB = "https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/LicenseDetail.aspx?LicNum="
KREG = "https://data.sf.gov/resource/k6kv-9kix.json?$select=license_number,max%28firm_name%29%20as%20firm,max%28address%29%20as%20addr,max%28phone%29%20as%20phone,count%28permit_number%29%20as%20permits&$where=zipcode%20like%20%2794112%25%27&$group=license_number&$order=permits%20DESC&$limit=100"
KCOUNT = "https://data.sf.gov/resource/k6kv-9kix.json?$select=license_number,count%28permit_number%29%20as%20permits&$where=zipcode%20like%20%2794112%25%27&$group=license_number&$order=permits%20DESC&$limit=100"
BREG = "https://data.sf.gov/resource/3pee-9qhc.json?$select=license1,max%28firm_name%29%20as%20firm,max%28firm_address%29%20as%20addr,max%28firm_zipcode%29%20as%20z,count%28permit_number%29%20as%20permits&$where=firm_zipcode%20like%20%2794112%25%27&$group=license1&$order=permits%20DESC&$limit=60"
BCOUNT = "https://data.sf.gov/resource/3pee-9qhc.json?$select=license1,count%28permit_number%29%20as%20permits&$where=firm_zipcode%20like%20%2794112%25%27&$group=license1&$order=permits%20DESC&$limit=100"
TT = "https://www.thumbtack.com/ca/san-francisco/bathroom-remodeling"


def c(field, text, source, excerpt):
    return {"field": field, "text": text, "source": source, "excerpt": excerpt}


def f(level, text, sources):
    return {"level": level, "text": text, "sources": sources}


def source(i, kind, access, url, title, note=None):
    d = {"id": i, "kind": kind, "access": access, "url": url, "title": title, "checkedAt": DATE}
    if note:
        d["note"] = note
    return d


def license_fact(number, entity, classes, status, expires, sid):
    return {"number": number, "entity": entity, "classes": classes, "status": status, "expires": expires, "checkedAt": DATE, "source": sid}


def base(rid, name, trade, phone, phone_source, area, area_text, claims, flags, gaps,
         status="research", license=None, links=None, reviews=None):
    return {
        "id": rid, "name": name, "phone": phone, "phoneSource": phone_source,
        "website": None, "websiteSource": None, "trade": trade, "area": area,
        "areaText": area_text, "status": status, "checkedAt": DATE,
        "claims": claims, "license": license, "reviewIds": reviews or [],
        "platformLinks": links or [], "flags": flags, "gaps": gaps,
        "priority": None, "rationale": "Wave-11 research record; it is not part of the diagnostic call order.",
        "nextStep": "Confirm current service area, both required trades, scope, insurance and scheduling directly before considering contact.",
        "exactMatch": False, "insuranceVerified": False, "scopeConfirmed": False, "master": False,
    }


# 42 individually opened CSLB pages. Source IDs 401-442 correspond one-for-one
# with these rows. The displayed facts below are transcriptions of those pages;
# the permit counts are separate official City registry readings.
ROWS = [
("associated-heating-of-sf","486084","ASSOCIATED HEATING OF S F","415-585-0145","5786 MISSION STREET, SAN FRANCISCO, CA 94112",["C20"],"active","2028-01-31",2033,"Associated Heating Of Sf"),
("ruby-plumbing-electrical-supply","748426","RUBY PLUMBING & ELECTRICAL SUPPLY INC","415-337-9133","1234 GENEVA AVENUE, SAN FRANCISCO, CA 94112",["B","C10","C16","C36"],"active","2028-04-30",1947,"Ruby Plumbing & Electrical"),
("apollo-heating-ventilating","704593","APOLLO HEATING & VENTILATING","415-585-3635","1005 GENEVA AVENUE, SAN FRANCISCO, CA 94112",["C20"],"canceled","2020-05-19",1326,"Apollo Heating & Ventilating"),
("leis-construction-company","593386","LEI'S CONSTRUCTION COMPANY","415-531-8611","616 ROLPH STREET, SAN FRANCISCO, CA 94112",["B","C36","C10"],"active","2028-05-31",1144,"Lei's Construction Company"),
("sl-mechanical-contractors","697542","S L MECHANICAL CONTRACTORS","415-706-1767","49 CERRITOS AVENUE, SAN FRANCISCO, CA 94127",["C20","C43"],"active","2026-10-31",1025,"S L Mechanical Contractor"),
("zh-mechanical","998449","ZH MECHANICAL INC","415-671-9138","56 NEWTON STREET, SAN FRANCISCO, CA 94112",["C20"],"active","2026-11-30",710,"Zh Mechanical Inc"),
("astorga-construction-legacy","309814","ASTORGA CONSTRUCTION","415-846-6896","289 MINERVA STREET, SAN FRANCISCO, CA 94112",["B","C10","C16","C20"],"expired","2023-10-31",659,"Astorga Construction Co.**Se"),
("daniel-p-heath","785326","DANIEL P HEATH INC","415-999-2127","4228 MISSION STREET, SAN FRANCISCO, CA 94112",["C36"],"canceled","2022-05-11",190,"Daniel P Heath Inc."),
("dengs-plumbing","636742","DENG'S PLUMBING INC","415-334-7005","206 GENEBERN WAY, SAN FRANCISCO, CA 94112",["C36"],"active","2028-04-30",563,"Denis Deng's Plumbing"),
("sure-inc","561658","SURE INC","415-221-2888","1728 OCEAN AVE 360, SAN FRANCISCO, CA 94112",["B","C10"],"active","2027-03-31",513,"Sure, Inc."),
("jins-plumbing","877300","JIN'S PLUMBING INC","415-307-0186","832 GRAFTON AVE, SAN FRANCISCO, CA 94112",["C36"],"active","2028-07-31",462,"Jin's Plumbing Inc"),
("brother-co","702388","BROTHER CO","415-652-7280","763 VIENNA ST, SAN FRANCISCO, CA 94112",["C36","C10"],"active","2027-04-30",447,"Brother Company"),
("madden-plumbing","825418","MADDEN PLUMBING LLC","415-923-8510","1228 FOLSOM STREET SUITE 101, SAN FRANCISCO, CA 94103",["C36","C16"],"active","2028-08-31",409,"Madden Plumbing"),
("hing-wah-construction","662696","HING WAH CONSTRUCTION INC","415-640-6474","1485 BAYSHORE BLVD #159, SAN FRANCISCO, CA 94124",["B","A","C10"],"inactive","2028-08-31",357,"Hing Wah Construction Inc"),
("celso-plumbing","972573","CELSO'S PLUMBING A PARTNERSHIP","415-240-2024","427 SILVER AVENUE, SAN FRANCISCO, CA 94112",["C36"],"active","2028-05-31",353,"Celso's Plumbing"),
("a-and-a-plumbing","685266","A & A PLUMBING","415-672-1640","47 GRANADA AVENUE, SAN FRANCISCO, CA 94112",["C36"],"active","2028-03-31",310,"A & A Plumbing"),
("bay-ct-construction","922224","BAY C T CONSTRUCTION INC","415-308-2838","419 ELLINGTON AVE, SAN FRANCISCO, CA 94112",["B"],"active","2026-09-30",281,"Bay C T Construction Inc."),
("gary-chan-plumbing","596143","GARY CHAN PLUMBING","415-298-9332","268 ONONDAGA AVE, SAN FRANCISCO, CA 94112",["C16","C36"],"active","2028-06-30",267,"Gary Chan Plumbing"),
("george-salet-plumbing","385567","GEORGE V SALET JR PLUMBING CO","850-355-4006","215 SUNSHINE DRIVE, PACIFICA, CA 94044",["C16","C36"],"inactive","2029-12-31",265,"George V Salet Plumbing Inc"),
("astorga-construction","1008360","ASTORGA CONSTRUCTION INC","415-846-6896","289 MINERVA ST, SAN FRANCISCO, CA 94112",["B","C10","C16","C20","C36"],"active","2027-10-31",248,"Astorga Construction Inc"),
("west-bay-plumbing","920624","WEST BAY PLUMBING","415-335-5732","130 RAE AVE, SAN FRANCISCO, CA 94112",["C36"],"active","2028-08-31",238,"West Bay Plumbing"),
("hong-wei-construction","946861","HONG WEI CONSTRUCTION INC","415-297-3288","120 TINGLEY ST, SAN FRANCISCO, CA 94112",["B","C10","C16","C36"],"active","2028-05-31",234,"Hong Wei Construction Inc"),
("wilson-plumbing","752868","WILSON PLUMBING","415-307-1378","945 TARAVAL ST #112, SAN FRANCISCO, CA 94116-2422",["C36"],"expired","2024-08-31",220,"Wilson Plumbing"),
("bruce-stabio","454357","BRUCE STABIO","916-725-7136","8200 FIREWOOD COURT, ORANGEVALE, CA 95662",["B","C16","C36","C-4","C20"],"expired","2006-03-31",215,"Bruce Stabio - A Aballa Plbg"),
("wf-construction","856142","W F CONSTRUCTION CO","650-278-3882","635 CAYUGA AVE, SAN FRANCISCO, CA 94112",["B","C10","C36"],"active","2027-03-31",214,"W F Construction Co"),
("prontito-plumbing","366870","PRONTITO PLUMBING","415-894-7399","48 OCEAN AVENUE, SAN FRANCISCO, CA 94112",["C36"],"active","2026-12-31",205,"Prontito Plumb"),
("greene-sons-mechanical","749915","GREENE & SONS MECHANICAL INC","415-760-7312","12501 HIGHWAY 9, BOULDER CREEK, CA 95006",["B","C16","C36"],"expired","2012-05-31",200,"Green & Sons Mechanical Inc."),
("luos-construction","766142","LUO'S CONSTRUCTION COMPANY","415-740-4988","725 PERU AVENUE, SAN FRANCISCO, CA 94112",["B","C10","C36"],"inactive","2029-07-31",195,"Luo's Construction Company"),
("marco-polo-plumbing","1025967","MARCO POLO PLUMBING INC","415-871-5772","118 ACACIA AVE, SAN BRUNO, CA 94066",["C36"],"active","2028-09-30",195,"Marco Polo Plumbing"),
("cb-plumbing","751699","C B PLUMBING","415-517-7709","930 CAYUGA AVENUE, SAN FRANCISCO, CA 94112",["C36"],"active","2028-07-31",192,"C B Pumbing"),
("sure-roofing-systems","591676","SURE ROOFING SYSTEMS INC","415-333-7663","118 SAGAMORE STREET, SAN FRANCISCO, CA 94112",["C39"],"active","2028-04-30",934,"Sure Roofing Systems/R.O.Choy"),
("anderson-roofing-sheet-metal","797144","ANDERSON ROOFING & SHEET METAL CO INC","415-584-9575","2940 SAN JOSE AVENUE, SAN FRANCISCO, CA 94112-3030",["C39","C43"],"active","2028-06-30",870,"Anderson Roofing & Sheet Metal"),
("am-rocca","757461","A M ROCCA INC","415-239-0484","4722 MISSION ST, SAN FRANCISCO, CA 94112",["B","C10","C36","A"],"active","2026-12-31",511,"A M Rocca Inc."),
("redwood-roofing","1054215","REDWOOD ROOFING CO","650-303-3705","130 STAPLES AVENUE, SAN FRANCISCO, CA 94112",["C39"],"active","2027-06-30",377,"Redwood Roofing Co"),
("sj-gogol-construction","477484","S J GOGOL CONSTRUCTION","415-333-9733","575 SILVER AVENUE, SAN FRANCISCO, CA 94112",["B","C10"],"canceled","2014-05-18",274,"S J Gogol Construction"),
("anderson-roofing-legacy","146802","ANDERSON ROOFING AND SHEET METAL CO INC","415-584-9575","2940 SAN JOSE AVENUE, SAN FRANCISCO, CA 94112",["C39","C43"],"canceled","2001-06-30",239,"Anderson Roofing & Sheet"),
("madonna-construction","65547","MADONNA CONSTRUCTION COMPANY","805-543-0300","PO BOX 3910, SAN LUIS OBISPO, CA 93403",["A","B","C12"],"canceled","2005-04-22",238,"Jingbo Yang"),
("amherst-associates","811425","AMHERST ASSOCIATES CONSTRUCTION MANAGEMENT INC","415-271-8828","1208 VINCENTE STREET, SAN FRANCISCO, CA 94116",["A","B","C10","C16","C27","C36","C33"],"active","2027-02-28",233,"Amherst Associates Const"),
("better-properties-contractors","876526","BETTER PROPERTIES CONTRACTORS INC","415-334-9438","1205 PLYMOUTH AVENUE, SAN FRANCISCO, CA 94112",["B","C33"],"expired","2010-04-30",230,"Better Properties Inc"),
("hr-wellington","615685","H R WELLINGTON CONSTRUCTION INC","415-239-1700","4722 MISSION ST, SAN FRANCISCO, CA 94112",["B"],"suspended","2027-03-31",214,"H R Wellington Const Inc"),
("planart-construction","942728","PLANART CONSTRUCTION CORP","925-451-0932","839 EDINBURG STREET, SAN FRANCISCO, CA 94112",["B"],"active","2027-02-28",205,"Planart Construction Corp"),
("steve-pham","707590","STEVE PHAM","415-640-1793","2230 KEITH STREET, SAN FRANCISCO, CA 94124",["C45"],"active","2027-06-30",190,"Steve's Awning"),
]


def extra_claims(number):
    if number == "593386":
        return [c("Independent review", "Yellow Pages places Lei's Construction at 616 Rolph St, San Francisco 94112 but displays no customer reviews. A BuildZoom extract describes general-building, plumbing and electrical licensing and reports no BuildZoom reviews; these are directory facts, not regulator facts.", 464, "Lei's Construction · 616 Rolph St · no reviews displayed"), c("Review corpus", "No attributable customer review text was retrieved for this business; no review is invented.", 465, "BuildZoom: Lei's Construction Company Reviews · no reviews")], []
    if number == "309814":
        return [c("Identity review", "The CSLB page for 309814 is an expired predecessor record. A separate current CSLB page for Astorga Construction Inc, licence 1008360, is stored separately because the regulator publishes different licence records.", 407, "309814 ASTORGA CONSTRUCTION expired; separate 1008360 ASTORGA CONSTRUCTION INC active")], [f("discrepancy", "The expired Astorga record and the active Astorga record are retained separately; identity equivalence was not assumed.", [407, 420, 445])]
    if number == "636742":
        return [c("Review", "A Yelp-index extract identifies Deng's Plumbing Company at 206 Genebern Way with phone (415) 334-7005 and a 3.5 rating from 2 reviews. The rating is a platform aggregate, not a qualification finding.", 460, "DENG'S PLUMBING COMPANY · 206 Genebern Way · 3.5 (2 reviews)"), c("Review corpus", "The retrieved mirror shows adjacent plumbing-review text but does not reliably expose a complete attributable review identity, so no review record is created.", 461, "Yahoo Local mirror · review author not reliably exposed")], []
    if number == "877300":
        return [c("Review", "A Yelp page places Jin's Plumbing Inc at 832 Grafton Ave, San Francisco 94112, lists residential/commercial repair, drains, sewer, water heaters and remodeling, and displays 5.0 from 5 reviews. No drywall service is claimed from it.", 458, "Jin's Plumbing Inc · 832 Grafton Ave · Plumbing, Flooring · 5.0 (5 reviews)"), c("Review", "A review mirror exposes an excerpt describing a clogged bathroom and bathtub with sewage coming out of the tub. It is adjacent-task evidence, not proof of drywall skill.", 459, "2018 excerpt: clogged bathroom and bathtub; sewage coming out the tub")], []
    if number == "1008360":
        return [c("Independent review", "BBB lists Astorga Construction Inc at 289 Minerva St, San Francisco 94112 with phone (415) 846-6896 and no customer reviews. BuildZoom reports permits and no reviews; these are directory facts, not a substitute for the CSLB read.", 452, "289 Minerva St · (415) 846-6896 · 0 customer reviews"), c("Review corpus", "No attributable customer review text was retrieved for this business; no review is invented.", 453, "BuildZoom: Astorga Construction Inc Reviews · no reviews")], []
    if number == "920624":
        return [c("Independent review", "BBB places West Bay Plumbing at 130 Rae Ave, San Francisco 94112 with phone (415) 335-5732 and identifies CSLB licence 920624. It has no BBB rating; this is identity/service-area context only.", 454, "West Bay Plumbing · 130 Rae Ave · CSLB 920624 · no BBB rating"), c("Permit context", "A BuildZoom extract links West Bay Plumbing to SF plumbing permits including shower-pan work and says the business serves San Francisco. Permit records do not prove drywall capability.", 455, "West Bay Plumbing · 130 RAE AVE · San Francisco service area · shower-pan examples")], []
    if number == "946861":
        return [c("Independent review", "A BuildZoom extract places Hong Wei Construction Inc at 120 Tingley St, San Francisco 94112, links licence 946861 and reports one 1-star review describing a slow, over-budget renovation.", 450, "1 out of 5 stars · Very slow, overbudget, and took 9 months longer than expected")], [f("notice", "A directory-extracted 1-star renovation review is a material caution signal and is retained for manual review.", [450])]
    if number == "757461":
        return [c("Business website", "AM ROCCA's own company page describes a San Francisco Bay Area general contractor with experience in building, renovations and repairs. It does not establish a current Outer Sunset service promise or both-trade scope.", 468, "AM ROCCA, Inc · general contractor · building, renovations and repairs"), c("Independent review", "BuildZoom reports AM Rocca Inc at 4722 Mission St, links licence 757461, and reports permitted projects but no BuildZoom reviews. Permit volume is not a quality finding.", 469, "AM Rocca Inc · 4722 Mission St · no reviews"), c("Entity context", "A filing extract describes A.m. Rocca, Inc as an active California general contractor. This is identity context, not a replacement for the CSLB read.", 470, "A.m. Rocca, Inc · active filing · general contractor")], []
    return [], []


def regulator(row, index):
    rid, number, name, phone, address, classes, status, expires, count, regname = row
    sid = 401 + index
    if "B" in classes and "C36" in classes:
        trade = "multi-trade"
    elif "C36" in classes:
        trade = "plumbing"
    elif "B" in classes:
        trade = "general"
    else:
        trade = "scope-exclusion"
    area_text = f"CSLB places the licensee at {address}. The City registry records {count} permit-contact rows in the adjacent 94112 firm-address pool under {regname}. This does not confirm Outer Sunset service or current dispatch."
    scope = ("The page displays B general building and C36 plumbing; this is the relevant two-trade licence pattern, but project-specific drywall scope, insurance and Outer Sunset service remain unconfirmed." if trade == "multi-trade" else "The CSLB classification set does not establish both plumbing and drywall service; no two-trade qualification is claimed.")
    claims = [c("Credential", f"CSLB detail page {number} was opened directly and transcribed: legal entity {name}, address {address}, displayed classifications {', '.join(classes)}, status {status}, and expiration {expires}.", sid, f"License #{number} · {name} · {address} · {status} · classes {', '.join(classes)} · expires {expires}"), c("Scope", scope, sid, f"CSLB classifications on license #{number}: {', '.join(classes)}"), c("Registry", f"The official SF DBI plumbing-contact registry ranked licence {number} at {count} permit rows in the adjacent 94112 firm-address pool. A permit-contact row is historical administrative evidence, not a current service promise.", 445, f"license_number {number} · firm {regname} · permits {count}")]
    extra, extra_flags = extra_claims(number)
    claims += extra
    flags = list(extra_flags)
    record_status = "research"
    if status != "active":
        flags.insert(0, f("hold", f"CSLB status is {status}; this record is held and is not presented as bookable.", [sid]))
        record_status = "hold"
    if trade == "scope-exclusion":
        flags.append(f("hold", f"Displayed CSLB classifications {', '.join(classes)} do not establish both plumbing and drywall.", [sid]))
        record_status = "hold"
    if number == "811425":
        flags.append(f("discrepancy", "The CSLB page says current and active, while its displayed workers-compensation line shows cancellation dated 09/03/2026. Resolve this coverage discrepancy before any contact decision.", [sid]))
        record_status = "hold"
    if number == "766142":
        claims.append(c("Complaint disclosure", "CSLB shows citation 2 2018 002125 dated 02/15/2019 with status FOR DISCLOSURE ONLY PER B&P CODE 7124.6. It is recorded as published disclosure text, not treated as a finding.", 443, "Citation # 2 2018 002125 · 02/15/2019 · FOR DISCLOSURE ONLY PER B&P CODE 7124.6"))
        flags.append(f("notice", "CSLB complaint disclosure is present and should be reviewed as published regulator information.", [443]))
    if number == "942728":
        claims.append(c("Complaint disclosure", "CSLB shows complaint N A 2025 1215 dated 05/26/2026 with status LETTER OF ADMONISHMENT ISSUED. CSLB's disclaimer says a listed complaint is only an allegation of a probable violation.", 444, "Complaint # N A 2025 1215 · 05/26/2026 · LETTER OF ADMONISHMENT ISSUED"))
        flags.append(f("notice", "CSLB complaint disclosure is present and should be reviewed as an allegation under the regulator's disclaimer.", [444]))
    gaps = ["Outer Sunset service is not confirmed by a current business service-area statement.", "Insurance, drywall availability and scheduling must be confirmed directly.", "No source in this wave confirms this exact repair scope."]
    if trade != "multi-trade":
        gaps.insert(0, "Both plumbing and drywall service are not established by this CSLB classification set.")
    return base("w11-" + rid, name, trade, phone, sid, "outside", area_text, claims, flags, gaps, record_status, license_fact(number, name, classes, status, expires, sid))


REGISTRY_LEADS = [
    ("ray-tom-construction", "Ray Tom Construction", "415-584-3015", "1362 Geneva Av", "524717", 122),
    ("h-bo-construction", "H & Bo Construction Inc.", "415-816-0837", "639 Madrid St", "601847", 104),
    ("galaxy-building-construction", "Galaxy Building Construction", "415-756-3355", "180 Shawnee Av", "892100", 149),
    ("frank-lau-construction", "Frank Lau Construction Co", None, "534 Vienna St", "707497", 124),
]


def registry_lead(x):
    rid, name, phone, addr, lic, count = x
    claims = [c("Registry", f"The official SF DBI plumbing contact registry returns firm {name}, address {addr}, licence number {lic} and {count} permit rows in the 94112 firm-address pool.", 445, f"firm {name} · license_number {lic} · address {addr} · permits {count}"), c("Building registry", f"The official SF DBI building contact registry also returns licence {lic} in the 94112 firm-address pool. This is a registry lead, not a CSLB classification or status read.", 448, f"license1 {lic} · firm {name} · firm_address {addr} · firm_zipcode 94112"), c("Coverage", "A recorded adjacent-ZIP firm address is local-presence evidence only. It does not establish current Outer Sunset dispatch, both required trades or exact-task capability.", 448, f"firm_zipcode 94112 · {addr}")]
    return base("w11-" + rid, name, "registry-lead", phone, 445 if phone else None, "outside", f"Official SF DBI registries place this lead at {addr}, ZIP 94112, with {count} plumbing-registry permit rows. The number {lic} has NOT been read on CSLB; no status, classification or legal-entity conclusion is claimed, and Outer Sunset service is unconfirmed.", claims, [f("gap", f"Registry lead only: licence {lic} has NOT been read on CSLB. It cannot be presented as verified or as providing both plumbing and drywall.", [445, 448])], ["Licence number and legal entity have NOT been read on CSLB.", "Both plumbing and drywall service are not verified.", "Outer Sunset service and current dispatch are not confirmed."])


PLATFORM = [
("ot-bay-builders","OT Bay Builders","https://www.thumbtack.com/ca/san-jose/general-contractors/ot-bay-builders/service/471730547188039681","Excellent 4.9 (164)","564","Camilla W.","We are looking forward to doing our master bath remodel with OT Builders next."),
("happy-bay-construction","Happy Bay Construction","https://www.thumbtack.com/ca/san-francisco/general-contractors/happy-bay-construction/service/493258659225690120","Exceptional 5.0 (35)","25","Jiamin L.","We had a great experience with Happy Bay Construction remodeling our bathroom."),
("inspired-builders","Inspired Builders Inc","https://www.thumbtack.com/ca/sunnyvale/construction-estimating/inspired-builders-inc/service/454465370461519887","Excellent 4.9 (125)","155","Stephanie Cruz","We love our newly remodeled bathroom."),
("mountain-top-construction","Mountain Top Construction","https://www.thumbtack.com/ca/san-francisco/general-contractors/mountain-top-construction/service/","Exceptional 5.0 (21)","6","Michael Okoh-Esene","Our home never looked this beautiful Mountain Top Construction did wonders with our bathroom remodel."),
]


def platform(x, review_id):
    rid, name, url, rating, hires, author, quote = x
    claims = [c("Listing evidence", f"Thumbtack's San Francisco bathroom-remodeling page displays {name} with {rating}, {hires} hires and a Licensed pro badge where shown. These are platform claims and not CSLB verification.", 449, f"{name} · {rating} · {hires} hires · serves San Francisco, CA"), c("Coverage", "The category page says the listing serves San Francisco, but no separate Outer Sunset statement and no line-level evidence of both plumbing and drywall were retrieved.", 449, "Serves San Francisco, CA · bathroom-remodeling category")]
    return base("w11-" + rid, name, "finish", None, None, "sf", "Thumbtack category page lists this pro in San Francisco bathroom remodeling. Outer Sunset service and both required trades are not separately verified.", claims, [f("hold", "Platform listing only: no CSLB licence fact was read, and both required trades plus Outer Sunset coverage remain unverified.", [449])], ["No CSLB licence number or classification was read.", "Both plumbing and drywall service are not verified.", "Outer Sunset service is not separately confirmed."], "hold", links=[{"label": "Thumbtack profile", "url": url, "source": 449}], reviews=[review_id])


REVIEWS = [
{"id":"R134","business":"w11-ot-bay-builders","platform":"Thumbtack","author":"Camilla W.","published":None,"quote":"We are looking forward to doing our master bath remodel with OT Builders next.","analysis":"A positive bathroom-remodel statement; it does not identify plumbing work, drywall work, old-pipe experience or Outer Sunset service.","theme":"Bath remodel","source":449,"access":"page","identity":"matched","negative":False,"checkedAt":DATE,"exactTask":False},
{"id":"R135","business":"w11-happy-bay-construction","platform":"Thumbtack","author":"Jiamin L.","published":None,"quote":"We had a great experience with Happy Bay Construction remodeling our bathroom.","analysis":"A favorable bathroom-remodel excerpt; the text does not establish the two required trades or Outer Sunset service.","theme":"Bath remodel","source":449,"access":"page","identity":"matched","negative":False,"checkedAt":DATE,"exactTask":False},
{"id":"R136","business":"w11-inspired-builders","platform":"Thumbtack","author":"Stephanie Cruz","published":None,"quote":"We love our newly remodeled bathroom.","analysis":"A short positive outcome statement; it gives no line-level evidence about plumbing, drywall or building conditions.","theme":"Bath remodel","source":449,"access":"page","identity":"matched","negative":False,"checkedAt":DATE,"exactTask":False},
{"id":"R137","business":"w11-mountain-top-construction","platform":"Thumbtack","author":"Michael Okoh-Esene","published":None,"quote":"Our home never looked this beautiful Mountain Top Construction did wonders with our bathroom remodel.","analysis":"A favorable bathroom-remodel excerpt; it does not establish current Outer Sunset coverage or both required services.","theme":"Bath remodel","source":449,"access":"page","identity":"matched","negative":False,"checkedAt":DATE,"exactTask":False},
]

UPGRADES = [
{"key":"amx","name":"AMX Plumbing","lic":"822482","entity":"AMX PLUMBING","status":"active","expires":"2027-08-31","classes":["C36"],"phone":"415-688-5358","address":"767 STEWART AVENUE, DALY CITY, CA 94015","form":"Sole Ownership","issued":"2003-08-06","area":"outside","area_text":"CSLB places the active C36 licensee at 767 Stewart Avenue, Daly City 94015. This does not confirm Outer Sunset dispatch or drywall service.","status_text":"This license is current and active.","note":"Earlier record stored a Thumbtack discovery and SF DBI registry lead without a regulator read. CSLB now confirms licence 822482 as active C36; this upgrades the credential fact only.","false_claim":"The Thumbtack Licensed pro badge and registry number were not treated as regulator verification before this read.","source":472},
{"key":"sugar-bear","name":"Sugar Bear Plumbing","lic":"876480","entity":"SUGAR BEAR PLUMBING","status":"expired","expires":"2026-04-30","classes":["C36"],"phone":"650-583-3330","address":"101 A HICKEY BLVD #120, SOUTH SAN FRANCISCO, CA 94080","form":"Sole Ownership","issued":"2006-04-20","area":"outside","area_text":"CSLB places licence 876480 at 101 A Hickey Blvd #120, South San Francisco 94080 and states it is expired; Outer Sunset dispatch is not confirmed.","status_text":"This license is expired and not able to contract at this time.","note":"Earlier record stored a Thumbtack discovery and registry lead. CSLB confirms C36 but also confirms expiration, so the record remains held.","false_claim":"The platform listing and registry lead did not establish an active credential; CSLB states expired.","source":473,"hold":True},
{"key":"a1-plumbing","name":"A-1 Plumbing","lic":"0454201","entity":"A-1 PLUMBING","status":"active","expires":"2028-03-31","classes":["C36"],"phone":"209-541-4540","address":"PMB 199, 2625 F COFFEE RD, MODESTO, CA 95355","form":"Sole Ownership","issued":"1984-03-23","area":"outside","area_text":"CSLB places the active C36 licensee at a Modesto mailing address. Earlier community and registry evidence does not establish Outer Sunset service or drywall capability.","status_text":"This license is current and active.","note":"Earlier record stored a community recommendation and registry number. CSLB confirms active C36, but no Outer Sunset service or drywall evidence is claimed.","false_claim":"The Reddit recommendation and registry row were not treated as regulator credential facts before this read.","source":474},
]


def make_sources():
    out = []
    for i, row in enumerate(ROWS):
        out.append(source(401+i, "government", "page", CSLB+row[1], f"CSLB LicenseDetail {row[1]} · {row[2]}"))
    out += [
        source(443,"government","page","https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/ComplaintDisclosure.aspx?LicType=LIC&LicNum=766142","CSLB complaint disclosure 766142","Citation 2 2018 002125 dated 02/15/2019; displayed as disclosure information and not treated as a finding."),
        source(444,"government","page","https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/ComplaintDisclosure.aspx?LicType=LIC&LicNum=942728","CSLB complaint disclosure 942728","Complaint N A 2025 1215 dated 05/26/2026; the page says a complaint is only an allegation of a probable violation."),
        source(445,"government","page",KREG,"SF DBI plumbing permit-contact registry, 94112 grouped all-field query","Official City open data; permit-contact rows are historical administrative evidence and not current service promises."),
        source(446,"government","page",KCOUNT,"SF DBI plumbing permit-contact registry, 94112 grouped count query","Separate count-only query used for ranking; it does not establish licence status or service."),
        source(447,"government","page",BCOUNT,"SF DBI building permit-contact registry, 94112 grouped count query","One grouped row has no licence number; data-quality irregularities are not attributed to a business."),
        source(448,"government","page",BREG,"SF DBI building permit-contact registry, 94112 grouped all-field query","The dataset has no phone column; stored address text is quoted as returned."),
        source(449,"platform","page",TT,"Thumbtack San Francisco bathroom-remodeling category page","Direct page read. Platform ratings, hire counts and badges are platform claims, not licence evidence."),
        source(450,"directory","search-extract","https://www.buildzoom.com/contractor/hong-wei-construction-inc","BuildZoom Hong Wei Construction","Directory extract; one negative review retained as a caution signal."),
        source(452,"directory","search-extract","https://www.bbb.org/us/ca/san-francisco/profile/general-contractor/astorga-construction-inc-1116-922524","BBB Astorga Construction Inc","Directory identity and no-review extract."),
        source(453,"directory","search-extract","https://www.buildzoom.com/contractor/astorga-construction-inc","BuildZoom Astorga Construction","Directory identity and no-review extract."),
        source(454,"directory","search-extract","https://www.bbb.org/us/ca/san-francisco/profile/general-contractor/west-bay-plumbing-1116-922289","BBB West Bay Plumbing","Directory identity and service-area context."),
        source(455,"directory","search-extract","https://www.buildzoom.com/contractor/west-bay-plumbing","BuildZoom West Bay Plumbing","Directory permit/service-area context."),
        source(458,"directory","search-extract","https://www.yelp.com/biz/jins-plumbing-inc-san-francisco","Yelp Jin's Plumbing Inc","Platform aggregate and service list; no drywall claim inferred."),
        source(459,"directory","search-extract","https://mapsdirections.io/place/jins-plumbing-inc-AW1mwLNV188WHfN40g66","Review mirror Jin's Plumbing Inc","Third-party mirror used for an attributable adjacent-task excerpt."),
        source(460,"directory","search-extract","https://www.yelp.com/biz/dengs-plumbing-company-san-francisco","Yelp Deng's Plumbing Company","Platform aggregate; no complete attributable review record created."),
        source(461,"directory","search-extract","https://local.yahoo.com/info-21372973-deng-s-plumbing-company-san-francisco/","Yahoo Local Deng's Plumbing","Review mirror; author identity was not reliably exposed."),
        source(464,"directory","search-extract","https://www.yellowpages.com/san-francisco-ca/mip/leis-construction-31060868","Yellow Pages Lei's Construction","No customer reviews displayed in retrieved extract."),
        source(465,"directory","search-extract","https://www.buildzoom.com/contractor/leis-construction-company","BuildZoom Lei's Construction Company","No customer reviews displayed in retrieved extract."),
        source(468,"business","page","https://www.amrocca.com/","AM ROCCA company website","Business-site description of Bay Area building, renovations and repairs."),
        source(469,"directory","search-extract","https://www.buildzoom.com/contractor/am-rocca-inc","BuildZoom AM Rocca","Permit count and no-review extract."),
        source(470,"directory","search-extract","https://www.bizprofile.net/ca/san-francisco/a-m-rocca-inc","BizProfile A.m. Rocca","Filing identity context only."),
        source(472,"government","page",CSLB+"822482","CSLB AMX Plumbing verification upgrade"),
        source(473,"government","page",CSLB+"876480","CSLB Sugar Bear Plumbing verification upgrade"),
        source(474,"government","page",CSLB+"0454201","CSLB A-1 Plumbing verification upgrade"),
    ]
    return out


def main():
    businesses = [regulator(row, i) for i, row in enumerate(ROWS)]
    businesses += [registry_lead(x) for x in REGISTRY_LEADS]
    for i, x in enumerate(PLATFORM):
        businesses.append(platform(x, "R"+str(134+i)))
    assert len(businesses) == 50
    by_id = {b["id"]: b for b in businesses}
    for r in REVIEWS:
        by_id[r["business"]]["reviewIds"].append(r["id"])
    artifact = {
        "wave": 11,
        "date": DATE,
        "note": "Wave 11 adjacent-ZIP discovery plus three fail-closed verification passes. Both plumbing and drywall remain required for qualification; no record is promoted and master remains empty.",
        "composition": {"regulatorRead": 42, "registryOnly": 4, "platformListing": 4, "verificationUpgrades": 3},
        "sources": make_sources(), "businesses": businesses, "reviews": REVIEWS, "upgrades": UPGRADES,
        "registryUpgrades": [],
        "dedupeRejections": [
            {"name":"Heise's Plumbing","existing":"heises","why":"same phone and current CSLB-linked entity already stored; old 787733 page was not added"},
            {"name":"Astorga Construction","existing":"w11-astorga-construction","why":"expired 309814 predecessor kept separate from active 1008360 record"},
            {"name":"Anderson Roofing & Sheet Metal","existing":"w11-anderson-roofing-sheet-metal","why":"canceled 146802 predecessor kept separate from active 797144 record"},
            {"name":"AMX Plumbing","existing":"amx","why":"verification upgrade, not a new record"},
            {"name":"Sugar Bear Plumbing","existing":"sugar-bear","why":"verification upgrade, not a new record"},
            {"name":"A-1 Plumbing","existing":"a1-plumbing","why":"verification upgrade, not a new record"},
            {"name":"Deng's Plumbing Company","existing":"w11-dengs-plumbing","why":"directory name variant resolved to the CSLB identity"},
            {"name":"Hong Wei Construction","existing":"w11-hong-wei-construction","why":"directory name variant resolved to CSLB licence 946861"},
            {"name":"West Bay Plumbing","existing":"w11-west-bay-plumbing","why":"BBB and BuildZoom are supporting pages for the same CSLB identity"},
            {"name":"Jin's Plumbing","existing":"w11-jins-plumbing","why":"directory and review pages resolve to CSLB licence 877300"},
        ],
        "taskEvidence": [
            {"source":458,"point":"Jin's Plumbing lists residential/commercial repair, drains, sewer, water heaters and remodeling; this is adjacent-task evidence, not exact-task proof."},
            {"source":459,"point":"A review mirror exposes an excerpt about a clogged bathroom and bathtub; it is adjacent plumbing evidence and not drywall evidence."},
            {"source":450,"point":"Hong Wei Construction has a directory-extracted negative renovation review; the caution is preserved and not averaged away."},
            {"source":449,"point":"Thumbtack bathroom-remodeling snippets show sentiment but do not establish both trades or Outer Sunset coverage."},
            {"source":445,"point":"Official City plumbing contact rows connect adjacent-ZIP firm addresses with historical permit counts; they are discovery evidence only."},
            {"source":448,"point":"Official City building contact rows provide a second registry channel for four leads; their licence numbers remain un-read on CSLB."},
        ],
        "falseClaimsRejected": [
            {"claim":"An adjacent 94112 address proves Outer Sunset service.","source":445,"why":"The registry proves a recorded firm address in the queried ZIP only; service area remains a gap."},
            {"claim":"A Thumbtack Licensed pro badge is a CSLB credential read.","source":449,"why":"The badge is a platform claim; no licence, classification or status is attached to platform records."},
            {"claim":"A registry licence number establishes both plumbing and drywall service.","source":448,"why":"Registry numbers are stored as leads only; no classification or service combination is inferred."},
            {"claim":"A platform review proves exact-task experience.","source":449,"why":"The snippets describe bathroom remodeling generally and are marked exactTask false."},
        ],
    }
    OUT.write_text(json.dumps(artifact, indent=1, ensure_ascii=False)+"\n", encoding="utf-8")
    print(f"wrote {OUT}: businesses={len(businesses)} sources={len(artifact['sources'])} reviews={len(REVIEWS)}")

if __name__ == "__main__":
    main()
