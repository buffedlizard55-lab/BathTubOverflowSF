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
const W7 = data.businesses.filter((b) => b.id.startsWith("w7-"));

test("exactly 351 unique discovery entries across seven waves, no fabricated master approvals", () => {
  assert.equal(data.businesses.length, 351);
  assert.equal(data.schemaVersion, 2);
  assert.deepEqual(data.researchDates, ["2026-09-10", "2026-09-11"]);
  assert.equal(data.researchedAt, "2026-09-11");
  assert.equal(data.waves.length, 7);
  assert.equal(
    data.waves.reduce((n, w) => n + w.count, 0),
    351,
  );
  assert.deepEqual(data.waves[6], {
    wave: 7,
    date: "2026-09-11",
    count: 50,
    cslbReads: 12,
    registryOnly: 20,
    thumbtack: 20,
  });
  for (const field of ["id", "name"])
    assert.equal(
      new Set(data.businesses.map((b) => b[field].trim().toLowerCase())).size,
      351,
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
  assert.equal(evidenceCounts(data).active, 41);
  assert.equal(evidenceCounts(data).inactive, 28);
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
  assert.equal(filterBusinesses(data.businesses, { license: true }).length, 41);
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

test("wave 7 follow-up attaches to pre-existing records instead of double-counting", () => {
  // 50 new records only — the seven follow-up targets are pre-existing ids
  assert.equal(data.businesses.length, 351);
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
  assert.equal(data.reviews.length, 98);
});
