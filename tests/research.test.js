import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import { createHash } from "node:crypto";
import { extname, join } from "node:path";
import { fileURLToPath } from "node:url";
import {
  filterBusinesses,
  mayPromote,
  toCSV,
  csvCell,
  escapeHTML,
  evidenceCounts,
  licenseSupportsTrade,
  TRADE_CLASSES,
  ALLOWED_CLASSES,
} from "../lib.js";
const data = JSON.parse(
  readFileSync(new URL("../data/research.json", import.meta.url)),
);
const sources = new Map(data.sources.map((s) => [s.id, s]));
const byId = new Map(data.businesses.map((b) => [b.id, b]));
const W6 = data.businesses.filter((b) => b.id.startsWith("w6-"));
const W7 = data.businesses.filter((b) => b.id.startsWith("w7-"));
const W8 = data.businesses.filter((b) => b.id.startsWith("w8-"));
const W9 = data.businesses.filter((b) => b.id.startsWith("w9-"));

// Known private-context markers are held only as one-way fingerprints. This
// lets the public repository test every artifact without restating excluded
// details in source code or assertion output.
const privateMarkerDigests = new Set([
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
]);
const digest = (value) => createHash("sha256").update(value).digest("hex");
function assertPrivacySafe(value, label) {
  const words = value.toLowerCase().match(/[a-z0-9]+/g) || [];
  for (let width = 1; width <= 4; width += 1)
    for (let i = 0; i + width <= words.length; i += 1)
      assert.equal(
        privateMarkerDigests.has(digest(words.slice(i, i + width).join(" "))),
        false,
        `${label} contains an excluded private-context marker`,
      );
}

test("exactly 451 unique discovery entries across nine waves, no fabricated master approvals", () => {
  assert.equal(data.businesses.length, 451);
  assert.equal(data.schemaVersion, 2);
  assert.deepEqual(data.researchDates, [
    "2026-09-10",
    "2026-09-11",
    "2026-09-12",
  ]);
  assert.equal(data.researchedAt, "2026-09-12");
  assert.equal(data.waves.length, 9);
  assert.equal(
    data.waves.reduce((n, w) => n + w.count, 0),
    451,
  );
  assert.deepEqual(data.waves[7], {
    wave: 8,
    date: "2026-09-12",
    count: 50,
    cslbReads: 50,
    activeLicenses: 40,
    nonActiveLicenses: 10,
    completedPlumbingPermits94122: 17,
    completedRestorationPermits94122: 27,
    retainedReviewExcerpts: 23,
  });
  assert.deepEqual(data.waves[8], {
    wave: 9,
    date: "2026-09-12",
    count: 50,
    cslbReads: 17,
    registryOnly: 33,
    activeLicenses: 12,
    nonActiveLicenses: 5,
    completedPermits94122: 35,
    retainedReviewExcerpts: 7,
  });
  for (const field of ["id", "name"])
    assert.equal(
      new Set(data.businesses.map((b) => b[field].trim().toLowerCase())).size,
      451,
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
  // records an Outer Sunset 94122 address for the license. Calls 06-08 came
  // from wave 6 and call 09 from wave 7; wave 6's Caledonia held call 06 until
  // a directly-read negative review removed it from the order (see the
  // wave-7 follow-up test below), and the remaining calls were renumbered so
  // the order stays contiguous.
  short
    .filter((b) => b.priority > 5)
    .forEach((b) => {
      assert.equal(b.area, "outer", b.id);
      assert.match(b.license.entity, /SAN FRANCISCO|INC|CO|PLUMBING|STUCCO/i);
      assert.ok(/94122/.test(b.areaText), b.id);
    });
  // wave 9 adds 12 active and 5 non-active CSLB-read licences; its 33 registry-only
  // records hold no licence at all and therefore count in neither column.
  assert.equal(evidenceCounts(data).active, 93);
  assert.equal(evidenceCounts(data).inactive, 43);
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
  assert.equal(filterBusinesses(data.businesses, { license: true }).length, 93);
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

test("HTML is escaped and the public schema and artifacts pass the privacy allowlist", () => {
  assert.equal(
    escapeHTML('<img onerror="x">'),
    "&lt;img onerror=&quot;x&quot;&gt;",
  );
  const topLevel = new Set([
    "schemaVersion",
    "researchedAt",
    "scope",
    "master",
    "methodology",
    "researchDates",
    "waves",
    "compliance",
    "sources",
    "businesses",
    "reviews",
  ]);
  const businessFields = new Set([
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
  ]);
  for (const key of Object.keys(data)) assert.ok(topLevel.has(key), key);
  for (const b of data.businesses)
    for (const key of Object.keys(b)) assert.ok(businessFields.has(key), `${b.id}.${key}`);

  const root = fileURLToPath(new URL("../", import.meta.url));
  const ignored = new Set([".git", "node_modules", "reports", "test-results", "playwright-report"]);
  const textTypes = new Set([".css", ".html", ".js", ".json", ".md", ".py", ".yaml", ".yml"]);
  const visit = (dir) => {
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      if (ignored.has(entry.name)) continue;
      const path = join(dir, entry.name);
      if (entry.isDirectory()) visit(path);
      else if (textTypes.has(extname(entry.name)))
        assertPrivacySafe(readFileSync(path, "utf8"), path.slice(root.length));
    }
  };
  visit(root);
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
    ["active", "canceled", "expired", "inactive", "revoked", "suspended"],
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

test("official permit rules and the cited code section were read directly", () => {
  const c = data.compliance;
  assert.ok(c, "compliance block missing");
  assert.deepEqual(c.sourceIds, [175, 305]);
  for (const id of c.sourceIds) {
    const s = sources.get(id);
    assert.equal(s.kind, "government");
    assert.equal(s.access, "page");
  }
  assert.match(sources.get(175).url, /^https:\/\/www\.sf\.gov\//);
  assert.match(sources.get(305).url, /^https:\/\/codelibrary\.amlegal\.com\//);
  assert.ok(c.facts.length >= 9);
  assert.ok(
    c.facts.some((f) => /permit before cutting into or replacing pipes/.test(f)),
  );
  assert.ok(c.facts.some((f) => /inspected before pipes are covered/.test(f)));
  assert.ok(c.facts.some((f) => /Section 104\.2 was read directly/.test(f)));
  assert.ok(/does not plan, sequence, recommend or assist/.test(c.position));
  for (const link of c.officialLinks) {
    assert.ok(sources.has(link.sourceId));
    assert.match(
      link.url,
      /^https:\/\/(www\.)?(sf\.gov|dbiweb02\.sfgov\.org|codelibrary\.amlegal\.com)\//,
    );
  }
  assert.deepEqual(c.notRetrieved, []);
});

test("wave 7 is 50 new records with three evidence channels kept separate", () => {
  assert.equal(W7.length, 50);
  assert.equal(new Set(W7.map((b) => b.id)).size, 50);
  assert.equal(W7.filter((b) => b.trade).length, 50);
  // no Thumbtack profile is ever stored as the business's own website
  assert.deepEqual(
    W7.filter((b) => b.website).map((b) => b.id),
    [],
  );

  // channel 1 — CSLB licence pages read directly
  const licensed = W7.filter((b) => b.license);
  assert.equal(licensed.length, 10);
  assert.deepEqual(
    [...new Set(licensed.map((b) => b.license.status))].sort(),
    ["active", "expired", "inactive", "revoked"],
  );
  const active = licensed.filter((b) => b.license.status === "active");
  assert.equal(active.length, 1);
  assert.equal(active[0].id, "w7-michael-kuenzli-plumbing-co");
  assert.equal(active[0].area, "outer");
  assert.ok(/94122/.test(active[0].areaText));
  for (const b of licensed) {
    const s = sources.get(b.license.source);
    assert.equal(s.kind, "government", b.id);
    assert.equal(s.access, "page", b.id);
    assert.match(s.url, /LicenseDetail\.aspx\?LicNum=/, b.id);
    assert.ok(s.url.includes(b.license.number), b.id);
    assert.ok(licenseSupportsTrade(b), `${b.id} class/trade mismatch`);
    if (b.license.status !== "active") {
      assert.ok(b.flags.some((f) => f.level === "hold"), `${b.id} lapsed licence needs a hold`);
      assert.ok(["research", "hold"].includes(b.status), b.id);
    }
  }
  // "inactive" and "revoked" first appear in wave 7 and must never render green
  for (const st of ["inactive", "revoked"])
    assert.ok(licensed.some((b) => b.license.status === st), st);

  // channel 2 — registry-only leads: a permit row is never a licence read
  const registryOnly = W7.filter(
    (b) => !b.license && b.claims.some((c) => /Registry-recorded/.test(c.text)),
  );
  assert.equal(registryOnly.length, 20);
  for (const b of registryOnly) {
    assert.equal(b.area, "sunset", `${b.id} registry ZIP is not an Outer Sunset confirmation`);
    assert.ok(
      b.flags.some((f) => /has NOT been read on CSLB/.test(f.text)),
      `${b.id} registry-only record must carry the unread-licence flag`,
    );
    assert.ok(
      b.claims.some(
        (c) =>
          c.field === "Registry" &&
          /Registry-recorded plumbing-permit contact/.test(c.text) &&
          /Re-read in a confirmatory query/.test(c.text),
      ),
      b.id,
    );
  }

  // channel 3 — Thumbtack listings read directly; a platform badge is not a licence
  const marketplace = W7.filter((b) =>
    b.claims.some((c) => c.field === "Listing evidence"),
  );
  assert.equal(marketplace.length, 20);
  for (const b of marketplace) {
    assert.equal(b.license, null, `${b.id} may not carry a licence from a platform badge`);
    const c = b.claims.find((x) => x.field === "Listing evidence");
    const s = sources.get(c.source);
    assert.equal(s.access, "page", b.id);
    assert.match(s.url, /^https:\/\/www\.thumbtack\.com\//, b.id);
    assert.ok(
      b.platformLinks.some((p) => /^https:\/\/www\.thumbtack\.com\//.test(p.url)),
      `${b.id} should retain the profile URL it was read from`,
    );
  }
  assert.equal(licensed.length + registryOnly.length + marketplace.length, 50);

  // every wave-7 review comes from a Thumbtack page read directly, not an index
  const w7Reviews = data.reviews.filter((r) => r.business.startsWith("w7-"));
  assert.equal(w7Reviews.length, 20);
  assert.equal(new Set(w7Reviews.map((r) => r.business)).size, 20);
  for (const r of w7Reviews) {
    assert.equal(r.platform, "Thumbtack", r.id);
    assert.equal(r.access, "page", r.id);
    assert.match(sources.get(r.source).url, /^https:\/\/www\.thumbtack\.com\//, r.id);
    assert.equal(r.exactTask, false, r.id);
  }
  // the negative review that put a wave-7 record on hold is marked negative
  const elite = byId.get("w7-elite-solution-will-team");
  assert.equal(elite.status, "hold");
  assert.ok(elite.reviewIds.length >= 1);
  assert.ok(
    elite.reviewIds.some((id) => data.reviews.find((r) => r.id === id).negative),
    "the allegation must be flagged as a negative review, not buried",
  );
});

test("wave 8 adds 50 collision-free, directly licensed plumbing and restoration records", () => {
  assert.equal(W8.length, 50);
  assert.equal(new Set(W8.map((b) => b.id)).size, 50);
  assert.equal(new Set(W8.map((b) => b.name.toLowerCase())).size, 50);
  assert.equal(new Set(W8.map((b) => b.phone.replace(/\D/g, ""))).size, 50);
  assert.equal(new Set(W8.map((b) => b.license.number)).size, 50);
  const prior = data.businesses.filter((b) => !b.id.startsWith("w8-"));
  const priorPhones = new Set(prior.map((b) => b.phone?.replace(/\D/g, "")).filter(Boolean));
  const priorLicenses = new Set(prior.map((b) => b.license?.number).filter(Boolean));
  const suffixes = new Set([
    "and", "co", "company", "corp", "corporation", "dba",
    "inc", "incorporated", "llc", "the",
  ]);
  const coreName = (name) =>
    name
      .normalize("NFKD")
      .replace(/[^a-zA-Z0-9]+/g, " ")
      .trim()
      .toLowerCase()
      .split(" ")
      .filter((word) => !suffixes.has(word))
      .join(" ");
  const priorCores = new Set(prior.map((b) => coreName(b.name)));
  for (const b of W8) {
    assert.equal(priorPhones.has(b.phone.replace(/\D/g, "")), false, b.id);
    assert.equal(priorLicenses.has(b.license.number), false, b.id);
    assert.equal(priorCores.has(coreName(b.name)), false, b.id);
  }
  assert.equal(W8.filter((b) => b.license.status === "active").length, 40);
  assert.equal(W8.filter((b) => b.license.status !== "active").length, 10);
  assert.equal(W8.slice(0, 23).every((b) => ["plumbing", "multi-trade"].includes(b.trade)), true);
  assert.equal(W8.slice(23).every((b) => ["general", "multi-trade"].includes(b.trade)), true);

  for (const b of W8) {
    const s = sources.get(b.license.source);
    assert.equal(s.kind, "government", b.id);
    assert.equal(s.access, "page", b.id);
    assert.equal(s.checkedAt, "2026-09-12", b.id);
    assert.match(s.url, /LicenseDetail\.aspx\?LicNum=/, b.id);
    assert.ok(s.url.endsWith(b.license.number), b.id);
    assert.ok(licenseSupportsTrade(b), `${b.id} class/trade mismatch`);
    assert.equal(b.priority, null, b.id);
    assert.equal(b.master, false, b.id);
    assert.equal(b.exactMatch, false, b.id);
    assert.equal(b.insuranceVerified, false, b.id);
    assert.equal(b.scopeConfirmed, false, b.id);
    assert.ok(b.gaps.length >= 4, b.id);
    if (b.license.status !== "active") {
      assert.equal(b.status, "hold", b.id);
      assert.ok(b.flags.some((f) => f.level === "hold"), b.id);
    }
  }

  const directLicenseSources = data.sources.filter(
    (s) => s.id >= 228 && s.id <= 277,
  );
  assert.equal(directLicenseSources.length, 50);
  assert.equal(directLicenseSources.every((s) => /LicenseDetail\.aspx\?LicNum=/.test(s.url)), true);

  const plumbingLinks = W8.filter((b) =>
    b.claims.some((c) => c.field === "Permit linkage" && c.source === 222),
  );
  const restorationLinks = W8.filter((b) =>
    b.claims.some((c) => c.field === "Permit linkage" && c.source === 225),
  );
  assert.equal(plumbingLinks.length, 17);
  assert.equal(restorationLinks.length, 28, "27 restoration selections plus one historical multi-trade permit");
  assert.equal(
    W8.filter((b) => b.claims.some((c) => c.field === "Coverage" && c.source === 223)).length,
    17,
  );
  assert.equal(
    W8.filter((b) => b.claims.some((c) => c.field === "Coverage" && c.source === 226)).length,
    27,
  );
  assert.equal(
    W8.filter((b) => b.claims.some((c) => c.field === "Coverage" && c.source === 227)).length,
    1,
  );
  for (const id of [222, 223, 224, 225, 226, 227]) {
    const s = sources.get(id);
    assert.equal(s.kind, "government");
    assert.equal(s.access, "page");
    assert.match(s.url, /^https:\/\/data\.sf\.gov\/resource\//);
    assert.doesNotMatch(decodeURIComponent(s.url), /status_date/);
  }
  const buildingJoin = decodeURIComponent(sources.get(225).url);
  assert.match(buildingJoin, /license1/);
  assert.match(buildingJoin, /firm_name/);
  assert.doesNotMatch(buildingJoin, /contact_name|license_number/);
});

test("wave 8 review sample is attributable, deduplicated and explicitly incomplete", () => {
  const reviews = data.reviews.filter((r) => r.business.startsWith("w8-"));
  assert.equal(reviews.length, 23);
  assert.deepEqual(
    reviews.map((r) => r.id),
    Array.from({ length: 23 }, (_, i) => `R${99 + i}`),
  );
  for (const r of reviews) {
    assert.equal(r.checkedAt, "2026-09-12", r.id);
    assert.equal(r.exactTask, false, r.id);
    assert.equal(r.access, sources.get(r.source).access, r.id);
    assert.ok(W8.find((b) => b.id === r.business).reviewIds.includes(r.id), r.id);
  }
  const normalized = reviews.map((r) => r.quote.toLowerCase().replace(/[^a-z0-9]+/g, " ").trim());
  assert.equal(new Set(normalized).size, reviews.length);

  const proCare = reviews.filter((r) => r.business === "w8-pro-care-restoration-inc");
  assert.equal(proCare.length, 7);
  assert.equal(proCare.filter((r) => r.source === 287).length, 3);
  assert.ok(
    byId.get("w8-pro-care-restoration-inc").flags.some((f) => /duplicate text/i.test(f.text)),
  );
  const holland = reviews.filter((r) => r.business === "w8-holland-plumbing-works");
  assert.equal(holland.length, 2);
  assert.ok(holland.some((r) => /shower-control handle mechanism/.test(r.analysis)));
  assert.ok(holland.every((r) => !r.exactTask));
  assert.equal(reviews.some((r) => r.platform === "Reddit" || r.platform === "Thumbtack"), false);

  const safeStepRejections = [300, 301].map((id) => sources.get(id));
  assert.ok(safeStepRejections.every((s) => /rejected/i.test(`${s.title} ${s.note}`)));
  assert.equal(data.methodology.completeReviewCorpus, false);
});

test("wave 8 irregularities remain visible and never relax the master gate", () => {
  const axion = byId.get("w8-axion-plumbing");
  assert.ok(
    axion.flags.some(
      (f) => f.level === "discrepancy" && /415-672-0249/.test(f.text) && /415-286-3451/.test(f.text),
    ),
  );
  const chen = byId.get("w8-chen-s-construction-and-mechanical-inc");
  assert.ok(chen.flags.some((f) => f.level === "discrepancy" && /earlier firm name/i.test(f.text)));
  for (const id of [
    "w8-brus-box-contractor-works",
    "w8-rprw-inc-dba-james-macmillan",
    "w8-gerson-construction-inc",
    "w8-wolfe-painting-co",
  ]) {
    const b = byId.get(id);
    assert.ok(b.flags.some((f) => f.level === "hold"), id);
    assert.equal(b.master, false, id);
  }
  assert.equal(sources.get(302).kind, "government");
  assert.equal(sources.get(303).kind, "government");
  assert.equal(sources.get(304).kind, "government");
  assert.equal(sources.get(305).kind, "government");
  assert.match(data.methodology.passes, /Pass 16:[\s\S]*Pass 17:[\s\S]*Pass 18:/);
});

test("wave 7 follow-up attaches to pre-existing records instead of double-counting", () => {
  // Wave 7 still contributed exactly 50 rows; later waves do not duplicate its
  // seven follow-up targets, which remain pre-existing ids.
  assert.equal(data.businesses.length, 451);
  for (const s of [218, 219, 220, 221]) {
    assert.equal(sources.get(s).access, "page", s);
    assert.equal(sources.get(s).checkedAt, "2026-09-11", s);
  }
  assert.equal(sources.get(218).kind, "platform");
  assert.equal(sources.get(219).kind, "platform");
  assert.equal(sources.get(220).kind, "government");
  assert.equal(sources.get(221).kind, "government");

  // wave-1 record: an expired C-36 is attached, held, and never bookable
  const bc = byId.get("bill-callaway");
  assert.equal(bc.license.number, "660638");
  assert.equal(bc.license.status, "expired");
  assert.deepEqual(bc.license.classes, ["C36"]);
  assert.equal(bc.license.source, 211);
  assert.equal(bc.status, "hold");
  assert.equal(bc.trade, "plumbing");
  assert.ok(bc.flags.some((f) => f.level === "hold" && /EXPIRED/.test(f.text)));
  assert.ok(bc.flags.some((f) => f.level === "discrepancy"));
  assert.equal(bc.checkedAt, "2026-09-11");

  // wave-2 record: corroborating re-read, name history resolved, area NOT widened
  const jw = byId.get("joe-watterson");
  assert.equal(jw.license.status, "active");
  assert.equal(jw.license.source, 210, "the later read must be the cited one");
  assert.equal(jw.license.checkedAt, "2026-09-11");
  assert.equal(jw.checkedAt, "2026-09-11");
  assert.notEqual(jw.area, "outer", "no 94122 row exists for 723992");
  assert.ok(jw.claims.some((c) => c.source === 60), "the original read stays traceable");
  assert.ok(jw.claims.some((c) => c.source === 220 && c.field === "Registry cross-check"));
  assert.ok(jw.flags.some((f) => f.level === "discrepancy" && /Slemish/.test(f.text)));
  assert.ok(jw.flags.some((f) => f.level === "gap" && /94122/.test(f.text)));

  // wave-6 shortlisted record: removed from the call order and held
  const cal = byId.get("w6-caledonia-plastering-stucco-inc");
  assert.equal(cal.priority, null);
  assert.equal(cal.status, "hold");
  assert.equal(cal.license.status, "active", "the licence read is unchanged by the hold");
  assert.ok(cal.flags.some((f) => f.level === "hold" && /call order/.test(f.text)));
  assert.ok(/Removed from the call order/.test(cal.rationale));
  const r89 = data.reviews.find((r) => r.id === "R89");
  assert.equal(r89.business, cal.id);
  assert.equal(r89.negative, true);
  assert.equal(r89.author, "Jay D.");
  assert.equal(r89.published, null, "no date is displayed for that review");
  assert.ok(/covered up a square bathroom exhaust with plaster/.test(r89.quote));
  // the mis-attributed wave-6 review is corrected, and the displaced author is restored
  const r60 = data.reviews.find((r) => r.id === "R60");
  assert.equal(r60.author, "Vipada W.");
  assert.equal(r60.published, "Oct 5, 2017");
  assert.equal(r60.source, 219);
  assert.equal(r60.access, "page");
  assert.equal(r60.identity, "matched");
  const r98 = data.reviews.find((r) => r.id === "R98");
  assert.equal(r98.business, cal.id);
  assert.equal(r98.author, "Tom S.");
  assert.equal(r98.published, "Jun 2, 2018");
  assert.ok(/exterior stucco/.test(r98.quote));
  assert.ok(cal.flags.some((f) => f.level === "discrepancy" && /attribution corrected/.test(f.text)));

  // wave-5 drywall record: platform credential must not become a licence fact
  const na = byId.get("w5-new-age-drywall-inc");
  assert.equal(na.license, null);
  assert.equal(na.trade, "drywall");
  assert.equal(na.area, "outside");
  assert.deepEqual(na.reviewIds.sort(), ["R91", "R92", "R93", "R94"]);
  assert.ok(na.claims.some((c) => /C9 – Drywall/.test(c.excerpt) && c.source === 218));
  assert.ok(na.flags.some((f) => f.level === "gap" && /No CSLB licence number is published/.test(f.text)));
  const tuan = data.reviews.find((r) => r.id === "R92");
  assert.equal(tuan.published, "Jan 8, 2026");
  assert.ok(/ceiling our plumber had to cut into/.test(tuan.quote));

  // wave-5 records whose profile paths put them outside the area
  const figs = byId.get("w5-figs-drywall-repair-paint");
  assert.equal(figs.area, "outside");
  assert.ok(figs.platformLinks.some((p) => p.url.includes("/id/boise/")));
  assert.ok(figs.flags.some((f) => f.level === "discrepancy" && /Boise/.test(f.text)));
  assert.ok(figs.reviewIds.includes("R95"));
  const walty = byId.get("w5-walty-handy-service-pro");
  assert.equal(walty.area, "outside");
  assert.ok(walty.platformLinks.some((p) => p.url.includes("/ca/san-pablo/moving-companies/")));
  assert.ok(walty.reviewIds.includes("R97"));
  const magana = byId.get("w5-maga-a-time-handyman");
  assert.ok(magana.reviewIds.includes("R96"));
  assert.ok(magana.platformLinks.some((p) => p.url.includes("/ca/san-francisco/handyman/")));

  // the call order stays contiguous and every call still clears the strict gate
  const short = data.businesses.filter((b) => b.priority).sort((a, b) => a.priority - b.priority);
  assert.deepEqual(short.map((b) => b.priority), [1, 2, 3, 4, 5, 6, 7, 8, 9]);
  assert.ok(!short.some((b) => b.id === cal.id));
  assert.equal(short[8].id, "w7-michael-kuenzli-plumbing-co");
  for (const b of short) {
    assert.equal(b.status, "research", `${b.id} a held record must not sit in the call order`);
    assert.equal(b.license.status, "active", b.id);
  }
  assert.equal(
    data.reviews.filter((r) => !r.business.startsWith("w8-") && !r.business.startsWith("w9-"))
      .length,
    98,
  );
  assert.equal(data.reviews.length, 128);
});

test("wave 9 separates CSLB-read records from registry-only leads and promotes nothing", () => {
  assert.equal(W9.length, 50);
  const licensed = W9.filter((b) => b.license);
  const registryOnly = W9.filter((b) => !b.license);
  assert.equal(licensed.length, 17);
  assert.equal(registryOnly.length, 33);
  assert.equal(licensed.filter((b) => b.license.status === "active").length, 12);
  assert.equal(licensed.filter((b) => b.license.status !== "active").length, 5);

  // Tier 1: every licence fact traces to a CSLB detail page read on the wave date.
  for (const b of licensed) {
    const s = sources.get(b.license.source);
    assert.equal(s.kind, "government", b.id);
    assert.equal(s.access, "page", b.id);
    assert.equal(s.checkedAt, "2026-09-12", b.id);
    assert.match(s.url, /LicenseDetail\.aspx\?LicNum=/, b.id);
    assert.ok(s.url.endsWith(b.license.number), b.id);
    assert.ok(licenseSupportsTrade(b), `${b.id} class/trade mismatch`);
    for (const field of ["priority", "master", "exactMatch", "insuranceVerified", "scopeConfirmed"])
      assert.ok(!b[field], `${b.id} ${field} must stay falsy`);
    assert.ok(b.claims.some((c) => c.field === "Insurance & bond"), `${b.id} bond/WC read`);
    if (b.license.status !== "active") {
      assert.equal(b.status, "hold", b.id);
      assert.ok(b.flags.some((f) => f.level === "hold"), b.id);
    } else {
      assert.ok(b.license.expires > "2026-09-12", b.id);
    }
  }

  // Tier 2: a registry number is a lead, never a credential, and can never promote.
  for (const b of registryOnly) {
    assert.equal(b.license, null, b.id);
    assert.equal(b.trade, "registry-lead", b.id);
    assert.equal(licenseSupportsTrade(b), false, b.id);
    assert.equal(mayPromote(b), false, b.id);
    assert.equal(b.status, "research", b.id);
    assert.notEqual(b.area, "outer", `${b.id} no Outer Sunset label without a regulator read`);
    assert.ok(b.flags.some((f) => f.level === "gap" && /NOT read on CSLB/.test(f.text)), b.id);
    assert.ok(b.gaps.some((g) => /NOT read on CSLB/.test(g)), b.id);
    assert.ok(b.flags.some((f) => /registry lead/i.test(f.text)), `${b.id} trade caveat`);
    if (!b.phone) assert.equal(b.phoneSource, null, b.id);
  }

  // The single documented cross-wave overlap: one address and phone, two licences.
  const ct = byId.get("w9-ct-plumbing-fire-protection");
  const priorCt = byId.get("w6-c-t-construction-plumb");
  assert.equal(ct.phone.replace(/\D/g, ""), priorCt.phone.replace(/\D/g, ""));
  assert.equal(ct.license.number, "1112261");
  assert.equal(priorCt.license, null, "the stored registry row still asserts no licence fact");
  assert.ok(priorCt.claims.some((c) => /533324/.test(c.excerpt)), "registry licence 533324");
  assert.ok(
    ct.flags.some((f) => f.level === "discrepancy" && f.text.includes("w6-c-t-construction-plumb")),
    "the overlap must be flagged, not deduplicated silently",
  );
  assert.ok(
    ct.claims.some((c) => c.field === "Relationship" && /533324/.test(c.text)),
    "the overlap must be explained on the record",
  );
  assert.ok(ct.gaps.some((g) => /533324/.test(g)), "the overlap must remain an open gap");

  // Apart from that documented case no wave-9 phone repeats the baseline.
  const priorPhones = new Set(
    data.businesses
      .filter((b) => !b.id.startsWith("w9-"))
      .map((b) => b.phone?.replace(/\D/g, ""))
      .filter(Boolean),
  );
  const wavePhones = [];
  for (const b of W9) {
    const digits = b.phone?.replace(/\D/g, "");
    if (!digits) continue;
    assert.ok(!priorPhones.has(digits) || digits === "4152037178", b.id);
    wavePhones.push(digits);
  }
  assert.equal(new Set(wavePhones).size, wavePhones.length, "wave-9 phones are unique");
  assert.equal(new Set(W9.map((b) => b.license?.number).filter(Boolean)).size, 17);

  // B-2 Residential Remodeling is a real CSLB class, added rather than mapped onto B.
  const knb = byId.get("w9-knb-tile-and-stone-inc-dba-knb-remodeling");
  assert.deepEqual(knb.license.classes, ["B-2", "B"]);
  assert.ok(ALLOWED_CLASSES.includes("B-2"));
  assert.ok(TRADE_CLASSES["registry-lead"], "registry-lead is a declared trade");
  assert.equal(TRADE_CLASSES["registry-lead"].length, 0, "it requires no class, so it can never pass");
  assert.ok(knb.flags.some((f) => /B-2/.test(f.text)), "the B-2 distinction must be published");
  assert.ok(knb.flags.some((f) => /C-36/.test(f.text)), "the missing C-36 must be published");

  // A CSLB complaint disclosure stays an allegation sourced to CSLB itself.
  assert.equal(sources.get(334).kind, "government");
  assert.match(sources.get(334).url, /ComplaintDisclosure\.aspx\?LicNum=1017991$/);
  const sfr = byId.get("w9-san-francisco-remodel");
  assert.ok(
    sfr.flags.some((f) => /allegation/i.test(f.text) && f.sources.includes(334)),
    "admonishment letter recorded as an allegation",
  );
  assert.equal(sfr.license.status, "active");
  assert.equal(sfr.master, false);

  // Holds are raised for coverage and review problems, not only for lapsed licences.
  const garzac = byId.get("w9-garzac-plumbing");
  assert.equal(garzac.license.status, "active");
  assert.equal(garzac.status, "hold");
  assert.ok(garzac.flags.some((f) => f.level === "hold" && /09\/11\/2026/.test(f.text)));
  const innovation = byId.get("w9-innovation-plumbing-and-rooter");
  assert.equal(innovation.license.status, "active");
  assert.equal(innovation.status, "hold");
  assert.ok(innovation.flags.some((f) => f.level === "hold" && /1\.0-star/.test(f.text)));
  assert.equal(innovation.reviewIds.length, 0, "an unreachable review is never attached");
  for (const id of [
    "w9-euro-plumbing-inc-dba-general-contractor",
    "w9-lam-pui-electrical-plumbing-inc",
    "w9-lee-s-plumbing-co",
    "w9-euro-plastering",
    "w9-charles-lakamp",
  ]) {
    const b = byId.get(id);
    assert.notEqual(b.license.status, "active", id);
    assert.equal(b.status, "hold", id);
  }
  assert.equal(W9.filter((b) => b.status === "hold").length, 7);

  // Plumbing-side licences without C-36 are called out, never quietly accepted.
  const euro = byId.get("w9-euro-plumbing-inc-dba-general-contractor");
  assert.deepEqual(euro.license.classes, ["B"]);
  assert.ok(euro.flags.some((f) => /NO C-36/.test(f.text)));
  assert.ok(sfr.flags.some((f) => /B only and no C-36/.test(f.text)));

  // Multi-trade coverage: the pattern this project needs, still unpromoted.
  const multi = licensed.filter(
    (b) => b.license.classes.includes("B") && b.license.classes.includes("C36"),
  );
  assert.deepEqual(
    multi.map((b) => b.license.number).sort(),
    ["1013565", "341277", "373337", "786183"],
  );
  assert.equal(multi.filter((b) => b.master).length, 0);
  assert.equal(W9.filter((b) => b.master).length, 0);

  // Only identity-matched, attributable excerpts became reviews.
  const w9Reviews = data.reviews.filter((r) => r.business.startsWith("w9-"));
  assert.deepEqual(
    w9Reviews.map((r) => r.id),
    ["R122", "R123", "R124", "R125", "R126", "R127", "R128"],
  );
  for (const r of w9Reviews) {
    assert.equal(r.exactTask, false, r.id);
    assert.equal(r.identity, "matched", r.id);
    assert.equal(r.checkedAt, "2026-09-12", r.id);
    assert.equal(sources.get(r.source).access, r.access, r.id);
    assert.ok(byId.get(r.business).reviewIds.includes(r.id), r.id);
    assert.equal(r.published, null, `${r.id} month and year only, so no day is invented`);
  }
  const smelly = w9Reviews.filter((r) => r.business === "w9-smelly-mel-s-plumbing-inc");
  assert.equal(smelly.length, 3);
  assert.ok(smelly.some((r) => r.negative), "the 1.0-star/text mismatch stays a negative signal");
  assert.ok(
    byId.get("w9-smelly-mel-s-plumbing-inc").flags.some((f) => /1\.0 of 5/.test(f.text)),
    "the mismatch is flagged on the record too",
  );
  const kevel = byId.get("w9-kevel-home-performance");
  assert.equal(kevel.reviewIds.length, 4);
  assert.ok(kevel.flags.some((f) => /HVAC, energy and insulation/.test(f.text)));
  assert.ok(kevel.flags.some((f) => f.level === "discrepancy" && /claimed or unclaimed/.test(f.text)));

  // Unattributable platform and community extracts stay sources, never reviews.
  for (const id of [345, 346, 347]) {
    assert.equal(sources.get(id).kind, "platform", id);
    assert.match(sources.get(id).note, /NOT attributed|[Uu]nattributable|quarantined/i, id);
  }
  for (const id of [348, 349, 350, 351, 352]) {
    assert.equal(sources.get(id).kind, "community", id);
    assert.match(
      sources.get(id).note,
      /names no business|no business is named|[Uu]nattributable|Task evidence only/i,
      id,
    );
  }
  assert.equal(
    data.reviews.filter((r) => [337, 345, 346, 347, 348, 349, 350, 351, 352].includes(r.source))
      .length,
    0,
    "no review is sourced from a category page, a community thread or caption metadata",
  );
  assert.equal(sources.get(339).kind, "directory");
  assert.match(sources.get(339).note, /never presented as an official Google rating/i);

  // Wave-9 sources are contiguous, official-first, and the wave stays fail-closed.
  const w9Sources = data.sources.filter((s) => s.id >= 306 && s.id <= 352);
  assert.equal(w9Sources.length, 47);
  assert.equal(w9Sources.filter((s) => s.kind === "government").length, 29);
  assert.equal(w9Sources.every((s) => s.checkedAt === "2026-09-12"), true);
  assert.match(
    data.methodology.passes,
    /Pass 19 \(wave 9, Sep 12 2026\):[\s\S]*Pass 20:[\s\S]*Pass 21:/,
  );
  assert.match(data.methodology.governmentSources, /137 distinct license numbers, 17 read in wave 9/);
  assert.deepEqual(data.master, []);
  assert.equal(data.businesses.filter((b) => b.priority).length, 9);
});
