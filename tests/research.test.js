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
} from "../lib.js";
const data = JSON.parse(
  readFileSync(new URL("../data/research.json", import.meta.url)),
);
const sources = new Map(data.sources.map((s) => [s.id, s]));

test("exactly 151 unique discovery entries across three waves, no fabricated master approvals", () => {
  assert.equal(data.businesses.length, 151);
  assert.equal(data.schemaVersion, 2);
  for (const field of ["id", "name"])
    assert.equal(
      new Set(data.businesses.map((b) => b[field].toLowerCase())).size,
      151,
    );
  assert.deepEqual(data.master, []);
  assert.equal(data.businesses.filter((b) => b.master).length, 0);
  assert.equal(data.methodology.completeReviewCorpus, false);
  assert.equal(data.methodology.contactedBusinesses, false);
});
test("every claim, contact, license and flag is source-linked", () => {
  for (const b of data.businesses) {
    assert.ok(b.claims.length > 0, b.id);
    assert.ok(b.gaps.length >= 2, b.id);
    assert.equal(b.checkedAt, data.researchedAt);
    for (const c of b.claims) {
      assert.ok(sources.has(c.source), b.id);
      assert.ok(c.excerpt.trim());
      assert.ok(c.text.trim());
    }
    if (b.website) {
      assert.ok(sources.has(b.websiteSource));
      assert.ok(/^https?:\/\//.test(b.website));
    }
    if (b.phone) assert.ok(sources.has(b.phoneSource));
    if (b.license) {
      assert.equal(sources.get(b.license.source).kind, "government");
      assert.match(sources.get(b.license.source).url, /www\.cslb\.ca\.gov/);
      assert.ok(b.license.classes.includes("C36"));
      assert.ok(b.license.entity);
      assert.equal(b.license.checkedAt, data.researchedAt);
      if (b.license.status === "active")
        assert.ok(b.license.expires > data.researchedAt);
    }
    for (const f of b.flags) {
      assert.ok(f.sources.length);
      f.sources.forEach((id) => assert.ok(sources.has(id)));
    }
    for (const p of b.platformLinks) assert.ok(sources.has(p.source));
  }
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
    );
    assert.match(s.url, /^https?:\/\//);
    assert.equal(s.checkedAt, data.researchedAt);
  }
});
test("review identities, source dates, quotes and provenance stay separate", () => {
  assert.equal(
    new Set(data.reviews.map((r) => r.id)).size,
    data.reviews.length,
  );
  const fingerprints = new Set();
  for (const r of data.reviews) {
    const b = data.businesses.find((b) => b.id === r.business);
    assert.ok(b);
    assert.ok(b.reviewIds.includes(r.id));
    assert.ok(sources.has(r.source));
    assert.ok(r.quote.length < 500);
    assert.ok(r.analysis.length > 30);
    assert.equal(r.exactTask, false);
    const fp = [r.business, r.author, r.quote].join("|");
    assert.ok(!fingerprints.has(fp));
    fingerprints.add(fp);
  }
  assert.equal(
    data.businesses.find((b) => b.id === "plumbing-pure").reviewIds.length,
    0,
  );
  assert.equal(data.reviews.filter((r) => r.platform === "Google").length, 0);
  for (const b of data.businesses)
    for (const id of b.reviewIds)
      assert.equal(data.reviews.find((r) => r.id === id)?.business, b.id);
});
test("shortlist requires current C36, but never claims exact qualification", () => {
  const short = data.businesses.filter((b) => b.priority);
  assert.equal(short.length, 5);
  assert.deepEqual(short.map((b) => b.priority).sort(), [1, 2, 3, 4, 5]);
  short.forEach((b) => {
    assert.equal(b.license.status, "active");
    assert.ok(b.license.classes.includes("C36"));
    assert.equal(b.master, false);
    assert.ok(b.rationale);
    assert.ok(b.nextStep);
  });
  assert.equal(evidenceCounts(data).active, 21);
});
test("case-insensitive search, status, area and active-license filters combine", () => {
  assert.equal(
    filterBusinesses(data.businesses, { query: "FAST RESPONSE" }).length,
    1,
  );
  assert.equal(
    filterBusinesses(data.businesses, { status: "shortlist" }).length,
    5,
  );
  assert.equal(
    filterBusinesses(data.businesses, { status: "master" }).length,
    0,
  );
  assert.equal(filterBusinesses(data.businesses, { license: true }).length, 21);
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
});
test("exports preserve citations, handle commas/quotes and neutralize spreadsheet formulas", () => {
  assert.equal(csvCell('A "quote", here'), '"A ""quote"", here"');
  assert.equal(csvCell('=HYPERLINK("x")'), '"\'=HYPERLINK(""x"")"');
  const csv = toCSV(
    data.businesses,
    sources.values().toArray
      ? sources.values().toArray()
      : [...sources.values()],
  );
  assert.match(csv, /https:\/\/www.cslb.ca.gov/);
  assert.match(csv, /Qualified master/);
  assert.match(csv, /Fast Response/);
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
  ]) {
    assert.equal(Object.hasOwn(data, key), false);
    data.businesses.forEach((b) => assert.equal(Object.hasOwn(b, key), false));
  }
});
