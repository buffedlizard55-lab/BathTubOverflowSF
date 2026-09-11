import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import {
  filterBusinesses,
  mayPromote,
  toCSV,
  csvCell,
  escapeHTML,
  evidenceCounts,
  licenseSupportsTrade,
  TRADE_CLASSES,
} from "../lib.js";
const data = JSON.parse(
  readFileSync(new URL("../data/research.json", import.meta.url)),
);
const sources = new Map(data.sources.map((s) => [s.id, s]));
const byId = new Map(data.businesses.map((b) => [b.id, b]));
const W6 = data.businesses.filter((b) => b.id.startsWith("w6-"));

test("exactly 301 unique discovery entries across six waves, no fabricated master approvals", () => {
  assert.equal(data.businesses.length, 301);
  assert.equal(data.schemaVersion, 2);
  assert.deepEqual(data.researchDates, ["2026-09-10", "2026-09-11"]);
  assert.equal(data.researchedAt, "2026-09-11");
  assert.equal(data.waves.length, 6);
  assert.equal(
    data.waves.reduce((n, w) => n + w.count, 0),
    301,
  );
  for (const field of ["id", "name"])
    assert.equal(
      new Set(data.businesses.map((b) => b[field].trim().toLowerCase())).size,
      301,
    );
  assert.deepEqual(data.master, []);
  assert.equal(data.businesses.filter((b) => b.master).length, 0);
  assert.equal(data.methodology.completeReviewCorpus, false);
  assert.equal(data.methodology.contactedBusinesses, false);
});

test("every claim, contact, license and flag is source-linked", () => {
  const httpWebsites = [];
  for (const b of data.businesses) {
    assert.ok(b.claims.length > 0, b.id);
    assert.ok(b.gaps.length >= 2, b.id);
    assert.ok(data.researchDates.includes(b.checkedAt), b.id);
    for (const c of b.claims) {
      assert.ok(sources.has(c.source), b.id);
      assert.ok(c.excerpt.trim());
      assert.ok(c.text.trim());
    }
    if (b.website) {
      assert.ok(sources.has(b.websiteSource));
      assert.match(b.website, /^https?:\/\//);
    }
    if (b.phone) assert.ok(sources.has(b.phoneSource), b.id);
    // Exactly one legacy discovery record still carries a bare http:// website
    // (kenneth-asire, wave 3). It is counted here so a second one cannot appear
    // unnoticed; it is surfaced in the wave-6 discovery log rather than edited,
    // because re-verifying a wave-3 URL is out of scope for this pass.
    if (b.website && b.website.startsWith("http://")) httpWebsites.push(b.id);
    if (b.license) {
      assert.equal(sources.get(b.license.source).kind, "government");
      assert.match(sources.get(b.license.source).url, /www\.cslb\.ca\.gov/);
      assert.ok(
        sources.get(b.license.source).url.includes(String(b.license.number)),
        b.id,
      );
      assert.ok(b.license.entity, b.id);
      assert.equal(b.license.checkedAt, b.checkedAt, b.id);
      assert.ok(b.license.classes.length, b.id);
      if (b.license.status === "active")
        assert.ok(b.license.expires > b.license.checkedAt, b.id);
    }
    for (const f of b.flags) {
      assert.ok(f.sources.length);
      f.sources.forEach((id) => assert.ok(sources.has(id), b.id));
    }
    for (const p of b.platformLinks) assert.ok(sources.has(p.source), b.id);
  }
  assert.deepEqual(httpWebsites, ["kenneth-asire"]);
});

test("source metadata makes access limitations explicit", () => {
  assert.equal(sources.size, data.sources.length);
  for (const s of data.sources) {
    assert.ok(
      [
        "page",
        "search-extract",
        "blocked-with-search-extract",
        "redirect",
        "expired-site",
        "review-panel-unavailable",
      ].includes(s.access),
      s.id,
    );
    assert.ok(
      ["business", "community", "directory", "government", "platform",
        "testimonial"].includes(s.kind),
      s.id,
    );
    assert.match(s.url, /^https:\/\//);
    assert.ok(s.title.trim(), s.id);
    assert.ok(data.researchDates.includes(s.checkedAt), s.id);
  }
});

test("review identities, source dates, quotes and provenance stay separate", () => {
  assert.equal(new Set(data.reviews.map((r) => r.id)).size, data.reviews.length);
  const fingerprints = new Set();
  for (const r of data.reviews) {
    const b = byId.get(r.business);
    assert.ok(b, r.id);
    assert.ok(b.reviewIds.includes(r.id), r.id);
    assert.ok(sources.has(r.source), r.id);
    assert.ok(r.quote.length < 500, r.id);
    assert.ok(r.analysis.length > 30, r.id);
    assert.equal(r.exactTask, false, r.id);
    assert.ok(data.researchDates.includes(r.checkedAt), r.id);
    const fp = [r.business, r.author, r.quote].join("|");
    assert.ok(!fingerprints.has(fp), r.id);
    fingerprints.add(fp);
  }
  assert.equal(byId.get("plumbing-pure").reviewIds.length, 0);
  assert.equal(data.reviews.filter((r) => r.platform === "Google").length, 0);
  for (const b of data.businesses)
    for (const id of b.reviewIds)
      assert.equal(data.reviews.find((r) => r.id === id)?.business, b.id);
});

test("shortlist requires an active license whose class covers its trade", () => {
  const short = data.businesses.filter((b) => b.priority);
  assert.equal(short.length, 9);
  assert.deepEqual(
    short.map((b) => b.priority).sort((a, b) => a - b),
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
  );
  short.forEach((b) => {
    assert.equal(b.license.status, "active", b.id);
    assert.equal(b.license.checkedAt, b.checkedAt, b.id);
    assert.ok(licenseSupportsTrade(b), `${b.id} class/trade mismatch`);
    assert.equal(b.master, false);
    assert.equal(b.exactMatch, false);
    assert.ok(b.rationale);
    assert.ok(b.nextStep);
  });
  // calls 06-09 were admitted on a stricter basis: the regulator itself
  // records an Outer Sunset 94122 address for the license.
  short
    .filter((b) => b.priority > 5)
    .forEach((b) => {
      assert.equal(b.area, "outer", b.id);
      assert.match(b.license.entity, /SAN FRANCISCO|INC|CO|PLUMBING|STUCCO/i);
      assert.ok(/94122/.test(b.areaText), b.id);
    });
  assert.equal(evidenceCounts(data).active, 40);
  assert.equal(evidenceCounts(data).inactive, 18);
});

test("case-insensitive search, status, area and active-license filters combine", () => {
  assert.equal(
    filterBusinesses(data.businesses, { query: "FAST RESPONSE" }).length,
    1,
  );
  assert.equal(
    filterBusinesses(data.businesses, { query: "caledonia" }).length,
    1,
  );
  assert.equal(filterBusinesses(data.businesses, { status: "shortlist" }).length, 9);
  assert.equal(filterBusinesses(data.businesses, { status: "master" }).length, 0);
  assert.equal(filterBusinesses(data.businesses, { license: true }).length, 40);
  const exact = filterBusinesses(data.businesses, {
    area: "outer",
    license: true,
  });
  assert.ok(exact.length > 0);
  assert.ok(
    exact.every((b) => b.area === "outer" && b.license.status === "active"),
  );
  assert.equal(
    filterBusinesses(data.businesses, { query: "nonexistent plumbing zebra" })
      .length,
    0,
  );
});

test("promotion fails closed; missing insurance/scope/exact evidence cannot pass", () => {
  data.businesses.forEach((b) => assert.equal(mayPromote(b), false));
  const b = {
    ...data.businesses[0],
    trade: "plumbing",
    area: "outer",
    exactMatch: true,
    insuranceVerified: true,
    scopeConfirmed: true,
    flags: [],
  };
  assert.equal(mayPromote(b), true);
  for (const field of ["exactMatch", "scopeConfirmed", "insuranceVerified"])
    assert.equal(mayPromote({ ...b, [field]: false }), false);
  assert.equal(mayPromote({ ...b, flags: [{ level: "hold" }] }), false);
  // a drywall license can never promote a plumbing requirement, and vice versa
  assert.equal(
    mayPromote({ ...b, license: { ...b.license, classes: ["C-9"] } }),
    false,
  );
  assert.equal(
    mayPromote({
      ...b,
      trade: "drywall",
      license: { ...b.license, classes: ["C36"] },
    }),
    false,
  );
});

test("exports preserve citations, handle commas/quotes and neutralize spreadsheet formulas", () => {
  assert.equal(csvCell('A "quote", here'), '"A ""quote"", here"');
  assert.equal(csvCell('=HYPERLINK("x")'), '"\'=HYPERLINK(""x"")"');
  const csv = toCSV(data.businesses, [...sources.values()]);
  assert.match(csv, /https:\/\/www.cslb.ca.gov/);
  assert.match(csv, /Qualified master/);
  assert.match(csv, /Fast Response/);
  assert.match(csv, /Caledonia Plastering/);
  assert.match(csv, /License classes/);
});

test("HTML is escaped and public schema excludes private property fields", () => {
  assert.equal(
    escapeHTML('<img onerror="x">'),
    "&lt;img onerror=&quot;x&quot;&gt;",
  );
  for (const key of [
    "propertyAddress",
    "occupants",
    "privateNotes",
    "accessInstructions",
    "tenantStatus",
    "rentControl",
    "permitAvoidance",
  ]) {
    assert.equal(Object.hasOwn(data, key), false);
    data.businesses.forEach((b) => assert.equal(Object.hasOwn(b, key), false));
  }
  const raw = readFileSync(
    new URL("../data/research.json", import.meta.url),
    "utf8",
  ).toLowerCase();
  for (const forbidden of [
    "rent control",
    "rent-controlled",
    "in-law unit",
    "inlaw unit",
    "without a permit",
    "no permit",
    "unpermitted",
    "discreet",
    "do not disclose",
  ])
    assert.equal(raw.includes(forbidden), false, `dataset leaks "${forbidden}"`);
});

test("wave 6 is 50 new records with regulator reads kept separate from registry leads", () => {
  assert.equal(W6.length, 50);
  assert.equal(new Set(W6.map((b) => b.id)).size, 50);
  const licensed = W6.filter((b) => b.license);
  assert.equal(licensed.length, 22);
  assert.equal(licensed.filter((b) => b.license.status === "active").length, 14);
  for (const b of licensed) {
    const s = sources.get(b.license.source);
    assert.equal(s.kind, "government", b.id);
    assert.equal(s.access, "page", b.id);
    assert.match(s.url, /LicenseDetail\.aspx\?LicNum=/, b.id);
    assert.ok(licenseSupportsTrade(b), `${b.id} class/trade mismatch`);
  }
  // a registry row must never be silently promoted into a license fact
  const registryOnly = W6.filter(
    (b) =>
      !b.license &&
      b.claims.some((c) => /Registry-recorded/.test(c.text)),
  );
  assert.equal(registryOnly.length, 16);
  for (const b of registryOnly)
    assert.ok(
      b.flags.some((f) => /has NOT been read on CSLB/.test(f.text)),
      b.id,
    );
  assert.equal(W6.filter((b) => b.trade).length, 50);
  assert.equal(
    W6.filter((b) => b.area === "outer").length >= 8,
    true,
    "expected several regulator-confirmed Outer Sunset records",
  );
});

test("non-active licenses are always held, never presented as bookable", () => {
  for (const b of data.businesses) {
    if (!b.license || b.license.status === "active") continue;
    const held =
      ["hold", "excluded"].includes(b.status) ||
      b.flags.some((f) => f.level === "hold");
    assert.ok(held, `${b.id} has a ${b.license.status} license but no hold`);
  }
  const statuses = new Set(
    data.businesses.filter((b) => b.license).map((b) => b.license.status),
  );
  assert.deepEqual(
    [...statuses].sort(),
    ["active", "canceled", "expired", "suspended"],
  );
});

test("classification-versus-scope audit: every trade is supported by a real CSLB class", () => {
  for (const b of data.businesses) {
    if (b.trade) assert.ok(TRADE_CLASSES[b.trade], b.id);
    if (b.license) assert.ok(licenseSupportsTrade(b), b.id);
  }
  // the wave-6 scope exclusion is recorded, not dropped
  const gorman = byId.get("w6-gorman-pipeline-inc");
  assert.deepEqual(gorman.license.classes, ["A"]);
  assert.equal(gorman.status, "excluded");
  assert.ok(gorman.flags.some((f) => f.level === "hold"));
  // an active B-only licence cannot self-perform plumbing or drywall
  const rs = byId.get("w6-r-s-dynamic-builders-inc");
  assert.deepEqual(rs.license.classes, ["B"]);
  assert.ok(rs.flags.some((f) => f.level === "hold"));
});

test("official permit rules are cited to a government page and nothing is paraphrased as exempt", () => {
  const c = data.compliance;
  assert.ok(c, "compliance block missing");
  const s = sources.get(c.sourceId);
  assert.equal(s.kind, "government");
  assert.equal(s.access, "page");
  assert.match(s.url, /^https:\/\/www\.sf\.gov\//);
  assert.ok(c.facts.length >= 6);
  assert.ok(
    c.facts.some((f) => /permit before cutting into or replacing pipes/.test(f)),
  );
  assert.ok(c.facts.some((f) => /must have it inspected/.test(f)));
  assert.ok(/does not plan, sequence, recommend or assist/.test(c.position));
  for (const l of c.officialLinks)
    assert.match(l.url, /^https:\/\/(www\.)?(sf\.gov|dbiweb02\.sfgov\.org)\//);
  // the exemption section itself was not retrieved, and the dataset says so
  assert.equal(c.notRetrieved.length, 1);
  assert.match(c.notRetrieved[0].note, /NOT\s+retrieved/);
  const raw = JSON.stringify(data).toLowerCase();
  assert.equal(raw.includes("permit is not required"), false);
  assert.equal(raw.includes("no permit needed"), false);
});
