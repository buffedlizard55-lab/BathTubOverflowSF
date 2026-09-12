#!/usr/bin/env python3
"""Merge the verified wave-9 artifact into data/research.json.

The merge is idempotent and deliberately fail-closed. It refuses source, name,
phone, license, review, classification, date, privacy, or qualification drift
instead of repairing ambiguous input silently.

Wave 9 splits its evidence into two published tiers: 17 records whose CSLB
detail page was opened and transcribed line by line, and 33 registry-only
records whose City-recorded licence number was deliberately NOT promoted into a
licence fact. For registry-only rows ``license`` stays ``null`` and the trade is
``registry-lead``, a channel label rather than a classification claim.

The one phone overlap with a stored record is a finding, not a duplicate: CSLB
licence 1112261 reads the same address and phone as registry-only record
w6-c-t-construction-plumb, which carries a different, never-read licence number
(533324). Both readings are published and cross-referenced.

Run:
    python3 scripts/gen_wave9.py
    python3 scripts/merge_wave9.py
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import parse_qs, unquote_plus, urlsplit

ROOT = Path(__file__).resolve().parents[1]
WAVE_FILE = ROOT / "data" / "wave9.json"
TARGET = ROOT / "data" / "research.json"
DATE = "2026-09-12"

NON_ACTIVE = {"expired", "suspended", "canceled", "inactive", "revoked"}
STATUSES = {"active"} | NON_ACTIVE
SOURCE_ACCESS = {
    "page",
    "search-extract",
    "blocked-with-search-extract",
    "redirect",
    "expired-site",
    "review-panel-unavailable",
}
SOURCE_KINDS = {
    "business",
    "community",
    "directory",
    "government",
    "platform",
    "testimonial",
}
ALLOWED_CLASSES = {
    "A",
    "B",
    # B-2 Residential Remodeling is a distinct CSLB classification. It was read
    # directly on licence 1120735 in wave 9 and added here rather than being
    # silently mapped onto B, which would overstate its scope.
    "B-2",
    "C-2",
    "C-4",
    "C-7",
    "C-9",
    "C4",
    "C10",
    "C15",
    "C16",
    "C20",
    "C22",
    "C33",
    "C35",
    "C36",
    "C38",
    "C42",
    "C43",
    "D34",
    "D39",
    "D56",
}
TRADE_REQUIRES = {
    "plumbing": [{"C36"}],
    # A registry-only lead asserts no classification, so no class can satisfy
    # it and such a record can never pass the promotion gate.
    "registry-lead": [],
    "drywall": [{"C-9"}, {"B"}],
    "plaster": [{"C35"}, {"B"}],
    "finish": [{"C-9"}, {"C35"}, {"B"}],
    "general": [{"B"}],
    "engineering": [{"A"}],
    "multi-trade": [{"B", "C36"}],
}
BUSINESS_KEYS = {
    "id",
    "name",
    "trade",
    "phone",
    "phoneSource",
    "website",
    "websiteSource",
    "area",
    "areaText",
    "status",
    "checkedAt",
    "claims",
    "license",
    "reviewIds",
    "platformLinks",
    "flags",
    "gaps",
    "priority",
    "rationale",
    "nextStep",
    "exactMatch",
    "insuranceVerified",
    "scopeConfirmed",
    "master",
}
CLAIM_KEYS = {"field", "text", "source", "excerpt"}
FLAG_KEYS = {"level", "text", "sources"}
LICENSE_KEYS = {"number", "entity", "classes", "status", "expires", "checkedAt", "source"}
LINK_KEYS = {"label", "url", "source"}
REVIEW_KEYS = {
    "id",
    "business",
    "platform",
    "source",
    "author",
    "published",
    "checkedAt",
    "quote",
    "theme",
    "analysis",
    "exactTask",
    "negative",
    "access",
    "identity",
}
SOURCE_KEYS = {"id", "title", "url", "kind", "access", "checkedAt", "note"}

# One-way fingerprints prevent known private-context markers from being printed
# in the repository while retaining a regression guard. Inputs are normalized
# to lower-case alphanumeric word windows before hashing.
PRIVATE_MARKER_DIGESTS = {
    "710cdcb6c633b8993d8a341d73f247282495408c2a12cc797c8006bc327464a8",
    "bea6c284fb02b5d0aa611eb727ee69cdfa283f832f667cc45edb395d9510841f",
    "510d3a4233002578d42ac8558c5324d8ffbd34ab0e08eb0b2a2c00485f77a361",
    "ae2785f2d5d577ecc622fecffaec531fd1687d55c347569fe805bf27af17c47e",
    "66f4a7521f5a2a3b0b21c97c9fd4e28c0564fbe5b75ae3ce316b4d157dd55bfc",
    "9903c83e316d8a40f84bc00adf967aa5caa0e58bec37584e45cf16b97edcd317",
    "cf109ac20d0a56c95192a248efbe6bc41c16113928b786d8588830efbb79f5d6",
    "4c2733abf54ccb0f418600316449c0a3d7bfe21de1894dae833860be7f5f3434",
    "bcbb4b2505d42b71121ea904ec141a825e4f3fd90d4f694d5b81e4a3f77a07e1",
    "7cca84535e81d2d1d7a838c892dac1d7ba7d409313d44810b742b8192a63bb1d",
    "8f53059107c1aca3174b4a75a6b8f520653b0fa5e2180b2121ddb4bd59a1e4ea",
    "2c7f437a907912af18e334413020d366916094f724ec3159f823470ad701cfd4",
    "57a8ef6d2c7995352c6a74233741e7bef6c1113782966662a8eccb586d7356d3",
    "e9f172ce2a0beb97843f2a5b9aab9978d9a956a23606da206789ec714d98efa0",
}


def norm_name(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def core_name(value: str) -> str:
    suffixes = {
        "and",
        "co",
        "company",
        "corp",
        "corporation",
        "dba",
        "inc",
        "incorporated",
        "llc",
        "the",
    }
    return " ".join(token for token in norm_name(value).split() if token not in suffixes)


def norm_phone(value: str | None) -> str:
    digits = re.sub(r"\D", "", value or "")
    return digits[-10:] if len(digits) >= 10 else digits


def review_fingerprint(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def assert_privacy_safe(value: object) -> None:
    words = re.findall(r"[a-z0-9]+", json.dumps(value, ensure_ascii=False).lower())
    for width in range(1, 5):
        for index in range(len(words) - width + 1):
            marker = " ".join(words[index : index + width])
            digest = hashlib.sha256(marker.encode()).hexdigest()
            assert digest not in PRIVATE_MARKER_DIGESTS, "private-context marker detected"


def supports_trade(business: dict) -> bool:
    # Mirrors licenseSupportsTrade in lib.js: a record with no licence read can
    # never satisfy a trade requirement, which is what keeps registry-only rows
    # permanently outside the promotion gate.
    if not business["license"]:
        return False
    classes = set(business["license"]["classes"])
    return any(required <= classes for required in TRADE_REQUIRES[business["trade"]])


# CSLB licence 1112261 reads the same business address (1847 48th Ave, 94122)
# and the same phone as stored registry-only record w6-c-t-construction-plumb,
# which carries registry licence 533324 that has never been read on CSLB. The
# overlap is published on both sides and is never deduplicated by assumption.
DOCUMENTED_PHONE_OVERLAP = {"4152037178": "w6-c-t-construction-plumb"}

wave = json.loads(WAVE_FILE.read_text())
data = json.loads(TARGET.read_text())

assert wave["wave"] == 9 and wave["date"] == DATE
assert wave["composition"] == {
    "businesses": 50,
    "cslbPagesRead": 17,
    "activeLicenses": 12,
    "nonActiveLicenses": 5,
    "registryOnlyRecords": 33,
    "multiTradeVerified": 4,
    "completedPermits94122": 35,
    "holdsRaised": 7,
    "retainedReviewExcerpts": 7,
    "unattributedCategoryExcerpts": 3,
    "communityTaskThreadsRead": 5,
    "discrepancyFlags": 15,
}
assert len(wave["businesses"]) == 50
assert len(wave["sources"]) == 47
assert len(wave["reviews"]) == 7
assert_privacy_safe(wave)

# Idempotence comes before mutation. A partial or drifted prior merge is not
# accepted: every wave row must still equal the deterministic artifact, and the
# cohort must remain collision-free against the 351-record baseline.
merged_wave_businesses = [
    b for b in data["businesses"] if b["id"].startswith("w9-")
]
if merged_wave_businesses:
    merged_wave_sources = [s for s in data["sources"] if 306 <= s["id"] <= 352]
    merged_wave_reviews = [
        r for r in data["reviews"] if r["business"].startswith("w9-")
    ]
    assert merged_wave_businesses == wave["businesses"], "merged wave-9 business drift"
    assert merged_wave_sources == wave["sources"], "merged wave-9 source drift"
    assert merged_wave_reviews == wave["reviews"], "merged wave-9 review drift"
    assert data["waves"][-1] == {
        "wave": 9,
        "date": DATE,
        "count": 50,
        "cslbReads": 17,
        "registryOnly": 33,
        "activeLicenses": 12,
        "nonActiveLicenses": 5,
        "completedPermits94122": 35,
        "retainedReviewExcerpts": 7,
    }
    assert (len(data["businesses"]), len(data["sources"]), len(data["reviews"])) == (
        451,
        352,
        128,
    )
    prior = [b for b in data["businesses"] if not b["id"].startswith("w9-")]
    prior_names = {norm_name(b["name"]) for b in prior}
    prior_cores = {core_name(b["name"]) for b in prior}
    prior_phones = {norm_phone(b.get("phone")) for b in prior if norm_phone(b.get("phone"))}
    prior_licenses = {
        str(b["license"]["number"]) for b in prior if b.get("license")
    }
    for business in merged_wave_businesses:
        assert norm_name(business["name"]) not in prior_names, business["name"]
        assert core_name(business["name"]) not in prior_cores, business["name"]
        phone = norm_phone(business["phone"])
        if phone:
            assert phone not in prior_phones or phone in DOCUMENTED_PHONE_OVERLAP, business["name"]
        if business["license"]:
            assert str(business["license"]["number"]) not in prior_licenses, business["name"]
    assert_privacy_safe(data)
    print("wave 9 already merged and artifact-equal — no changes written.")
    raise SystemExit(0)

# ---------------------------------------------------------------- source gate
existing_source_ids = {s["id"] for s in data["sources"]}
wave_source_ids = [s["id"] for s in wave["sources"]]
assert wave_source_ids == list(range(306, 353)), "wave-9 source IDs must be contiguous"
assert not (set(wave_source_ids) & existing_source_ids)

for source in wave["sources"]:
    assert set(source) == SOURCE_KEYS, source["id"]
    assert source["kind"] in SOURCE_KINDS, source["id"]
    assert source["access"] in SOURCE_ACCESS, source["id"]
    assert source["checkedAt"] == DATE, source["id"]
    parsed = urlsplit(source["url"])
    assert parsed.scheme == "https" and parsed.hostname and not parsed.username, source["id"]
    assert source["title"].strip() and source["note"].strip(), source["id"]
    if source["kind"] == "government":
        assert source["access"] == "page", source["id"]
        assert parsed.hostname in {
            "www.cslb.ca.gov",
            "data.sf.gov",
            "codelibrary.amlegal.com",
        }, source["id"]
    if parsed.hostname == "www.cslb.ca.gov":
        assert re.search(
            r"/(LicenseDetail|ComplaintDisclosure)\.aspx\?Lic(?:Num|Type)=", source["url"]
        ), source["id"]
    if parsed.hostname == "data.sf.gov":
        assert re.match(r"^/resource/(k6kv-9kix|a6aw-rudh|3pee-9qhc|i98e-djp9)\.json$", parsed.path), source["id"]
        query = parse_qs(parsed.query)
        assert "$select" in query and "$limit" in query, source["id"]
        decoded = unquote_plus(source["url"])
        assert "status_date" not in decoded, source["id"]
        if "3pee-9qhc" in source["url"]:
            assert "license1" in decoded and "firm_name" in decoded, source["id"]
            assert "license_number" not in decoded and "contact_name" not in decoded, source["id"]

cslb_sources = [
    source
    for source in wave["sources"]
    if "LicenseDetail.aspx?LicNum=" in source["url"]
]
assert len(cslb_sources) == 17, "wave 9 reads 17 CSLB detail pages"
assert {source["id"] for source in cslb_sources} == set(range(317, 334))
disclosure_sources = [
    source for source in wave["sources"] if "ComplaintDisclosure.aspx" in source["url"]
]
assert [source["id"] for source in disclosure_sources] == [334]
assert "1017991" in disclosure_sources[0]["url"]
source_by_id = {s["id"]: s for s in data["sources"] + wave["sources"]}

# ------------------------------------------------------------- collision gate
existing_ids = {b["id"] for b in data["businesses"]}
existing_names = {norm_name(b["name"]): b["id"] for b in data["businesses"]}
existing_cores = {core_name(b["name"]): b["id"] for b in data["businesses"]}
existing_phones = {
    norm_phone(b.get("phone")): b["id"]
    for b in data["businesses"]
    if norm_phone(b.get("phone"))
}
existing_licenses = {
    str(b["license"]["number"]): b["id"]
    for b in data["businesses"]
    if b.get("license")
}

wave_names: set[str] = set()
wave_cores: set[str] = set()
wave_phones: set[str] = set()
wave_licenses: set[str] = set()

for business in wave["businesses"]:
    assert set(business) == BUSINESS_KEYS, business.get("id")
    assert business["id"].startswith("w9-") and business["id"] not in existing_ids
    name = norm_name(business["name"])
    core = core_name(business["name"])
    phone = norm_phone(business["phone"])
    assert name not in existing_names, f"name collision: {business['name']}"
    assert core not in existing_cores, f"near-name collision: {business['name']}"
    assert name not in wave_names and core not in wave_cores
    if phone:
        if phone in existing_phones:
            assert phone in DOCUMENTED_PHONE_OVERLAP, f"phone collision: {business['name']}"
            prior_id = DOCUMENTED_PHONE_OVERLAP[phone]
            assert any(
                flag["level"] == "discrepancy" and prior_id in flag["text"]
                for flag in business["flags"]
            ), f"documented phone overlap not cross-referenced: {business['name']}"
            assert any(
                claim["field"] == "Relationship" and prior_id in claim["text"]
                for claim in business["claims"]
            ), f"documented phone overlap not explained: {business['name']}"
        assert phone not in wave_phones
        wave_phones.add(phone)
    else:
        assert business["phoneSource"] is None, business["id"]
    if business["license"]:
        number = str(business["license"]["number"])
        assert number not in existing_licenses, f"license collision: {number}"
        assert number not in wave_licenses
        wave_licenses.add(number)
    else:
        assert business["trade"] == "registry-lead", business["id"]
    wave_names.add(name)
    wave_cores.add(core)

# --------------------------------------------------------------- record gate
active = 0
non_active = 0
registry_only = 0
for business in wave["businesses"]:
    assert business["checkedAt"] == DATE
    assert business["status"] in {"research", "hold"}
    assert business["area"] in {"outer", "sunset", "sf", "unknown", "outside"}
    assert business["trade"] in TRADE_REQUIRES
    assert business["claims"] and business["claims"][0]["field"] == "Discovery"
    assert len(business["gaps"]) >= 4
    assert business["priority"] is None
    assert business["rationale"].strip() and business["nextStep"].strip()
    assert business["master"] is False
    assert business["exactMatch"] is False
    assert business["insuranceVerified"] is False
    assert business["scopeConfirmed"] is False

    license_ = business["license"]
    if license_ is None:
        # Tier 2: a City registry row whose licence number was never read on CSLB.
        registry_only += 1
        assert business["trade"] == "registry-lead", business["id"]
        assert business["status"] == "research", business["id"]
        # No regulator read, so no Outer Sunset area label may be claimed.
        assert business["area"] in {"sunset", "sf", "unknown"}, business["id"]
        assert any(
            flag["level"] == "gap" and "NOT read on CSLB" in flag["text"]
            for flag in business["flags"]
        ), f"{business['id']} registry-only record must publish the no-regulator-read gap"
        assert any(
            gap.startswith("No CSLB page was read") or "NOT read on CSLB" in gap
            for gap in business["gaps"]
        ), f"{business['id']} registry-only record must carry the gap in plain text too"
        assert not supports_trade(business), business["id"]
    else:
        assert set(license_) == LICENSE_KEYS
        assert license_["checkedAt"] == DATE
        assert license_["status"] in STATUSES
        assert license_["classes"] and set(license_["classes"]) <= ALLOWED_CLASSES
        assert license_["source"] in range(317, 334)
        license_source = source_by_id[license_["source"]]
        assert license_source["kind"] == "government"
        assert license_source["access"] == "page"
        assert license_source["url"].endswith(f"LicNum={license_['number']}")
        assert supports_trade(business), f"{business['id']} classification/trade mismatch"
        if license_["status"] == "active":
            active += 1
            assert license_["expires"] > DATE
        else:
            non_active += 1
            assert business["status"] == "hold"
            assert any(flag["level"] == "hold" for flag in business["flags"])

    if business["phone"]:
        assert business["phoneSource"] in source_by_id
    else:
        assert business["phoneSource"] is None
    if business["website"]:
        assert business["websiteSource"] in source_by_id
    else:
        assert business["websiteSource"] is None
    for claim in business["claims"]:
        assert set(claim) == CLAIM_KEYS
        assert claim["source"] in source_by_id
        assert claim["text"].strip() and claim["excerpt"].strip()
    for flag in business["flags"]:
        assert set(flag) == FLAG_KEYS
        assert flag["level"] in {"hold", "notice", "gap", "discrepancy"}
        assert flag["sources"] and all(sid in source_by_id for sid in flag["sources"])
    for link in business["platformLinks"]:
        assert set(link) == LINK_KEYS
        assert link["source"] in source_by_id
        assert link["url"].startswith("https://")

assert (active, non_active, registry_only) == (12, 5, 33)

# --------------------------------------------------------------- review gate
existing_review_ids = {review["id"] for review in data["reviews"]}
expected_review_ids = [f"R{number}" for number in range(122, 129)]
assert [review["id"] for review in wave["reviews"]] == expected_review_ids
assert not (set(expected_review_ids) & existing_review_ids)
wave_business_ids = {business["id"] for business in wave["businesses"]}

for review in wave["reviews"]:
    assert set(review) == REVIEW_KEYS, review["id"]
    assert review["business"] in wave_business_ids
    assert review["source"] in source_by_id
    assert review["access"] == source_by_id[review["source"]]["access"]
    assert review["checkedAt"] == DATE
    assert review["exactTask"] is False
    assert isinstance(review["negative"], bool)
    assert review["identity"] in {"matched", "indexed", "unverified-username", "company-published"}
    assert 0 < len(review["quote"]) < 500
    assert len(review["analysis"]) > 40
    if review["published"] is not None:
        assert re.match(r"^\d{4}-\d{2}-\d{2}$", review["published"])

for business in wave["businesses"]:
    assigned = [
        review["id"] for review in wave["reviews"] if review["business"] == business["id"]
    ]
    assert business["reviewIds"] == assigned, business["id"]

fingerprints: dict[tuple[str, str], str] = {}
for review in data["reviews"] + wave["reviews"]:
    key = (review["business"], review_fingerprint(review["quote"]))
    assert key not in fingerprints, (
        f"duplicate review text: {review['id']} and {fingerprints.get(key)}"
    )
    fingerprints[key] = review["id"]

# --------------------------------------------------------------- merge data
data["sources"].extend(wave["sources"])
data["businesses"].extend(wave["businesses"])
data["reviews"].extend(wave["reviews"])
data["researchedAt"] = DATE
if DATE not in data["researchDates"]:
    data["researchDates"].append(DATE)
assert data["researchDates"] == sorted(set(data["researchDates"]))

assert [entry["wave"] for entry in data["waves"]] == list(range(1, 9))
data["waves"].append(
    {
        "wave": 9,
        "date": DATE,
        "count": 50,
        "cslbReads": 17,
        "registryOnly": 33,
        "activeLicenses": 12,
        "nonActiveLicenses": 5,
        "completedPermits94122": 35,
        "retainedReviewExcerpts": 7,
    }
)

# Compliance posture is unchanged by wave 9. Sources 175 (SF DBI permit page)
# and 305 (San Francisco Plumbing Code 104.2) were read on 2026-09-12 and were
# not re-read in this pass, so their stamps and the published facts stay exactly
# as they are rather than being re-dated without a fresh read.
compliance = data["compliance"]
assert compliance["sourceId"] == 175
assert compliance["sourceIds"] == [175, 305]
assert compliance["checkedAt"] == DATE
assert compliance["facts"] and compliance["officialLinks"]

# Update methodology without changing the fail-closed qualified-list standard.
method = data["methodology"]
read_numbers = sorted(
    {
        match.group(1)
        for source in data["sources"]
        if source["access"] == "page"
        and (match := re.search(r"LicenseDetail\.aspx\?LicNum=(\d+)", source["url"]))
    }
)
assert len(read_numbers) == 137
method["governmentSources"] = re.sub(
    r"^CSLB license detail pages read directly \([^)]*\)",
    "CSLB license detail pages read directly (137 distinct license numbers, 17 read in wave 9)",
    method["governmentSources"],
    count=1,
)
method["governmentSources"] += (
    " Wave 9 ran the same joins in the other direction - from completed 94122 permits to "
    "their recorded contacts - and read 17 CSLB detail pages directly. The remaining 33 "
    "wave-9 records are registry-only: the City's own open data returns a licence number "
    "for them, that number was deliberately not promoted into a licence fact, and the "
    "record says so on its face. Wave 9 also established 35 completed permits at "
    "work-location ZIP 94122 across both tiers."
)
assert "Pass 19" not in method["passes"]
method["passes"] = method["passes"].rstrip() + (
    " Pass 19 (wave 9, Sep 12 2026): regulator pass - 17 CSLB detail pages opened "
    "directly and transcribed field by field, five found non-active, the complaint "
    "disclosure behind licence 1017991 read separately, and every licence number the "
    "City registry returned but that was NOT read published as a lead with license null "
    "and trade registry-lead. Pass 20: cross-source pass - registry identity compared "
    "field by field with regulator identity, producing 15 discrepancy flags including "
    "four phone conflicts, six registry name variants on one licence, a licence reissued "
    "to another entity in 2006, three ZIP variants on one active multi-trade licence, and "
    "one address plus phone shared by two different licence numbers; public directory "
    "pages checked for review corpora; unattributable Thumbtack category quotes and "
    "Reddit task threads quarantined as sources instead of being converted into reviews; "
    "CSLB class B-2 discovered and added to the schema rather than mapped onto B. "
    "Pass 21: fail-closed qualification pass - no record promoted, the qualified master "
    "list stays empty, holds raised for expired and inactive licences, a workers-"
    "compensation cancellation dated before the research date, a single unreachable 1.0 "
    "star review, and licences appearing on plumbing permits without C-36; public-data "
    "privacy scrub and structural, render and browser tests re-run."
)
# Wave 8's Pass 15-18 text is already stored in the dataset; wave 9 only appends
# its own three passes and never re-states a previous wave's.

method["ranking"] += (
    " Wave 8 does not add or reorder diagnostic calls. Its permit history and adjacent "
    "reviews improve research directions, but no new record has written exact-task scope, "
    "current project insurance, and a verified repair-first outcome together; all 50 remain "
    "outside the qualified master list."
)
method["ranking"] += (
    " Wave 9 also adds no diagnostic calls and reorders nothing. Its best verified finding "
    "is a trade-coverage pattern rather than a business: licence 1013565 holds C-36 and B "
    "on one active licence with a completed 94122 permit whose printed scope combines new "
    "drain and water lines with replacing a section of drywall, and licence 341277 has held "
    "B and C-36 since 1977. Neither is promoted: the first is held on a single unreachable "
    "1.0 star public review, and the second has no retrievable customer review at all. All "
    "50 wave-9 records remain outside the qualified master list."
)

# ------------------------------------------------------------- final invariants
assert len(data["businesses"]) == 451
assert len(data["sources"]) == 352
assert len(data["reviews"]) == 128
assert len(data["waves"]) == 9
assert sum(entry["count"] for entry in data["waves"]) == 451
assert data["master"] == []
assert not any(b["master"] for b in data["businesses"])
assert not any(
    b.get("exactMatch") or b.get("insuranceVerified") or b.get("scopeConfirmed")
    for b in data["businesses"]
)
assert len({b["id"] for b in data["businesses"]}) == 451
assert len({s["id"] for s in data["sources"]}) == 352
assert len({r["id"] for r in data["reviews"]}) == 128
assert len({norm_name(b["name"]) for b in data["businesses"]}) == 451
assert_privacy_safe(data)

all_source_ids = {source["id"] for source in data["sources"]}
all_reviews = {review["id"]: review for review in data["reviews"]}
for business in data["businesses"]:
    assert business["checkedAt"] in data["researchDates"], business["id"]
    assert business["claims"] and business["claims"][0]["field"] == "Discovery"
    for claim in business["claims"]:
        assert claim["source"] in all_source_ids
    for flag in business["flags"]:
        assert flag["sources"] and all(sid in all_source_ids for sid in flag["sources"])
    for review_id in business["reviewIds"]:
        assert all_reviews[review_id]["business"] == business["id"]

TARGET.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
print(
    "merged wave 9: "
    f"{len(data['businesses'])} businesses, {len(data['sources'])} sources, "
    f"{len(data['reviews'])} reviews, {len(read_numbers)} direct CSLB records"
)
