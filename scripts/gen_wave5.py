#!/usr/bin/env python3
"""Build wave 5: 50 additional, source-linked plumbing/drywall discovery leads.

These are discovery records, not endorsements. Directory badges, ratings and service
areas are preserved as attributed claims and never converted into license facts.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-10"
SOURCES = [
 {"id":141,"title":"Yelp · Outer Sunset plumber results (Sep 2026 index)","url":"https://www.yelp.com/search?find_desc=plumber&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA","kind":"directory","access":"blocked-with-search-extract","checkedAt":DATE,"note":"Indexed result page; direct review corpus was unavailable. New leads include Walker's Plumbing and Castillo General Remodel."},
 {"id":142,"title":"Yelp · Outer Sunset plumbing, deep results","url":"https://www.yelp.com/search?find_desc=24+Hour+Plumbers&find_loc=Outer+Sunset,+San+Francisco,+CA&start=120","kind":"directory","access":"blocked-with-search-extract","checkedAt":DATE,"note":"Deep indexed results supplied new plumbing and construction names. Location and ratings are platform claims only."},
 {"id":143,"title":"Yelp · licensed plumber San Francisco indexed results","url":"https://yelp.com/search?find_desc=Licensed+Plumber&find_loc=San+Francisco%2C+CA","kind":"directory","access":"blocked-with-search-extract","checkedAt":DATE,"note":"Indexed result extract supplied Alphabet Plumbing and Selvin Plumbing; badges are not CSLB verification."},
 {"id":144,"title":"Thumbtack · San Francisco drywall repair","url":"https://www.thumbtack.com/ca/san-francisco/drywall-repair","kind":"directory","access":"search-extract","checkedAt":DATE,"note":"Indexed page names drywall providers and selected review excerpts; profiles and licenses remain unchecked."},
 {"id":145,"title":"Thumbtack · San Francisco drywall contractors (2026)","url":"https://www.thumbtack.com/ca/san-francisco/drywall-contractors","kind":"directory","access":"search-extract","checkedAt":DATE,"note":"Indexed top-provider page with platform rating samples, hires and stated SF service area."},
 {"id":146,"title":"Yelp · San Francisco ceiling drywall installation","url":"https://www.yelp.com/search?find_desc=Ceiling+Drywall+Installation&find_loc=San+Francisco,+CA","kind":"directory","access":"blocked-with-search-extract","checkedAt":DATE,"note":"Indexed results for ceiling drywall installation; badges and reviews remain platform-provided evidence."},
 {"id":147,"title":"Yelp · San Francisco ceiling repair","url":"https://www.yelp.com/search?find_desc=ceiling+repair&find_loc=San+Francisco%2C+CA","kind":"directory","access":"blocked-with-search-extract","checkedAt":DATE,"note":"Indexed ceiling-repair results used for restoration and plaster/drywall discovery."},
 {"id":148,"title":"Yelp · Outer Sunset handyman (Aug 2026 index)","url":"https://www.yelp.com/search?find_desc=Handyman&find_loc=Outer+Sunset%2C+San+Francisco%2C+CA","kind":"directory","access":"blocked-with-search-extract","checkedAt":DATE,"note":"Indexed Outer Sunset handyman page; candidates are finish/access-hatch leads, not plumbers."},
 {"id":149,"title":"Thumbtack · San Francisco general contractors","url":"https://www.thumbtack.com/ca/san-francisco/general-contractors","kind":"directory","access":"search-extract","checkedAt":DATE,"note":"Indexed general-contractor results; used only for multi-trade discovery."}
]
# name, source, area, exact indexed evidence
ROWS = [
 ("Walker's Plumbing Services",141,"outside","5.0 (18 reviews); Richmond-area listing; family-owned; free estimates."),
 ("Castillo General Remodel",141,"sf","Indexed as serving San Francisco; bathroom remodeling and plumbing work for a new ADU shown."),
 ("Mr Unger's Kitchen & Bathroom Remodeling",141,"outside","4.8 (59 reviews); South San Francisco area; profile says general and plumbing contractor."),
 ("Mason Plumbing",141,"outside","4.6 (87 reviews); San Anselmo-area listing."),
 ("San Francisco Plumbing Experts",141,"sf","5.0 (1 review); indexed as serving San Francisco; family-owned."),
 ("Sovereignty Plumbing",142,"outside","4.6 (46 reviews); indexed at 102 Mountain Rd with a Verified License badge."),
 ("VRG Plumbing",142,"outside","4.9 (128 reviews); Temescal listing offering remodels, tub installation and drain cleaning."),
 ("SJS Plumbing Construction & Design Services",142,"sf","Indexed as serving San Francisco; no rating shown in extract."),
 ("ABF Construction",142,"sf","5.0 (2 reviews); serves San Francisco; excerpt references tricky plumbing and a solution."),
 ("BayPro Plumbing",142,"outside","5.0 (3 reviews); Pacifica-area listing."),
 ("Young's Plumbing",142,"sf","1.0 (1 review); indexed at 483 19th Ave, Outer Richmond."),
 ("Stan Plumbing",142,"sunset","Indexed in Inner Sunset; no rating shown."),
 ("415 Backflow Testing",142,"sf","Indexed as serving San Francisco; specialty appears to be backflow testing."),
 ("Alphabet Plumbing",143,"outside","5.0 (10 reviews); 950 S McGlincy Ln; Verified License badge in Yelp extract."),
 ("Selvin Plumbing And Rooter",143,"sf","5.0 (85 reviews); Verified License badge; excerpt discusses old galvanized drain pipe."),
 ("Magaña Time Handyman",144,"sf","Thumbtack lists drywall repair/texturing; 4.8 across 68 reviews in page JSON-LD."),
 ("JAP Drywall Comp. Corp.",144,"sf","5.0 (2 reviews); serves San Francisco; reviewer says provider advised fixing a leak before patching."),
 ("Artur Astanov",144,"sf","5.0 (9 reviews); 14 hires; serves San Francisco."),
 ("Monkey's Remodeling",144,"sf","5.0 (1 review); serves San Francisco."),
 ("Tim's Handyman Services",144,"sf","Review excerpt says Mike repaired and patched drywall and identified a sink issue."),
 ("WATER'S FAULT Restoration",144,"sf","Indexed review says bathroom-ceiling drywall hole was patched and texture matched; painting excluded."),
 ("New Age Drywall Inc",145,"sf","4.9 (144 reviews); 260 hires; serves San Francisco; Thumbtack labels Licensed pro."),
 ("Walty Handy Service Pro",144,"sf","Indexed review praises drywall patching/repair and communication."),
 ("Mayorga Handyman & Remodeling Services",144,"sf","Indexed review describes fast apartment drywall repair."),
 ("Figs Drywall Repair & Paint",144,"sf","Named in Thumbtack's San Francisco drywall-review section."),
 ("Atlas Construction",144,"sf","Indexed review describes repair and color-matched painting of a large drywall hole."),
 ("Alpha & Omega General Construction",144,"sf","Indexed review describes repeated visits to let layers dry and additional drywall patches."),
 ("C&C Painting",145,"sf","4.9 (130 reviews); drywall repair, texturing and installation; serves San Francisco."),
 ("Bautista Drywall",145,"sf","5.0 (27 reviews); 43 hires; serves San Francisco; bathroom-wall hole review."),
 ("M P Drywall",145,"sf","4.8 (22 reviews); drywall installation and hanging; serves San Francisco."),
 ("Ampier's Drywall",145,"sf","5.0 (5 reviews); drywall repair and texturing; serves San Francisco."),
 ("Eduardo Paz Garcia's Painting",145,"sf","4.3 (113 reviews); drywall installation/repair; serves San Francisco."),
 ("Perez Drywall",145,"sf","5.0 (1 review); drywall installation/repair; serves San Francisco."),
 ("Brush Bros Painting",145,"sf","5.0 (5 reviews); drywall installation; serves San Francisco; Licensed pro badge."),
 ("Scott Snell — Yeah I Can Fix That",145,"sf","4.1 (28 reviews); drywall repair and installation; serves San Francisco."),
 ("Spaicer Painting & Repair",145,"sf","4.7 (9 reviews); drywall repair; serves San Francisco."),
 ("Chito's Drywall Stucco Repair",146,"sf","Family-owned; 11 years in business; drywall installation/repair listing."),
 ("E Custom Design",146,"sf","4.9 (73 reviews); Verified License badge in Yelp indexed results."),
 ("Estrada Design Build",146,"sf","New Yelp listing with Verified License badge; no review count shown."),
 ("Landers Drywall",146,"sf","5.0 (27 reviews); drywall installation/replacement listing."),
 ("Peña & Peña Drywall",146,"unknown","5.0 (10 reviews); 51 years in business; family-owned."),
 ("Navarro Drywall Inc",146,"unknown","5.0 (8 reviews); Verified License badge; ceiling drywall repair excerpt."),
 ("Genuine Drywall Contractors",147,"outside","4.9 (286 reviews); Pleasant Hill area; website tag says ceiling repair."),
 ("McKenna Plastering",147,"sf","4.8 (108 reviews); indexed as serving San Francisco; plaster/stucco specialty."),
 ("Jimenez Bro",147,"sf","5.0 (1 review); review concerns replacement of a bathroom ceiling after water damage."),
 ("Doug Demattei Drywall",147,"outside","5.0 (19 reviews); Pacifica-area listing; reviewer calls him a drywall-repair craftsman."),
 ("Your Castro Handyman",148,"sf","4.7 (111 reviews); indexed as serving San Francisco."),
 ("Bay Assembly",148,"sf","4.8 (38 reviews); indexed as serving San Francisco."),
 ("GAXL Construction & Plumbing",149,"sf","Thumbtack general-contractor result; review excerpt recommends its quality and customer service."),
 ("Edri Construction",149,"sf","Review describes plumbing and drywall among end-to-end remodeling trades and care protecting common areas.")
]
assert len(ROWS)==50

def slug(s):
 import re
 return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")

def build(row):
 name,src,area,evidence=row
 trade="drywall/finish" if src in (144,145,146,147,148) else "plumbing/multi-trade"
 return {"id":"w5-"+slug(name),"name":name,"website":None,"websiteSource":None,"status":"research","area":area,
  "areaText":evidence,"license":None,"phone":None,"phoneSource":None,
  "claims":[{"field":"Discovery","text":f"{name} appears in the cited {trade} result with the attributed details below.","source":src,"excerpt":evidence}],
  "flags":[],"reviewIds":[],"exactMatch":False,"master":False,"checkedAt":DATE,"platformLinks":[],
  "gaps":["No exact seized bathtub-overflow extraction outcome verified.","CSLB identity and active trade classification not directly verified in this pass.","Outer Sunset dispatch and current availability require confirmation unless explicitly stated."]}

wave={"wave":5,"note":"50 new plumbing, drywall, finish and multi-trade discovery records; no promotions.","businesses":[build(x) for x in ROWS],"sources":SOURCES,"reviews":[]}
assert len({b['id'] for b in wave['businesses']})==50
(ROOT/'data/wave5.json').write_text(json.dumps(wave,indent=1,ensure_ascii=False)+'\n')
print('wrote wave5.json: 50 businesses, 9 sources')
