import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

// Render smoke test. The site is plain ES modules with no build step, so this
// exercises the real template code against a hand-rolled DOM stub instead of
// adding jsdom as a dependency. Its job is narrow but strict: every route must
// render without throwing and without leaking `undefined`, `NaN`,
// `[object Object]` or an unresolved citation into the markup.
const data = JSON.parse(
  readFileSync(new URL("../data/research.json", import.meta.url)),
);

class El {
  constructor(tag = "div") {
    this.tagName = tag.toUpperCase();
    this.dataset = {};
    this.style = {};
    this.hidden = false;
    this.checked = false;
    this.open = false;
    this._html = "";
    this.textContent = "";
    this.classList = {
      toggle() {},
      add() {},
      remove() {},
      contains: () => false,
    };
  }
  set innerHTML(v) {
    this._html = v;
  }
  get innerHTML() {
    return this._html;
  }
  setAttribute() {}
  removeAttribute() {}
  addEventListener() {}
  appendChild(c) {
    return c;
  }
  remove() {}
  click() {}
  focus() {}
  select() {}
  setSelectionRange() {}
  getBoundingClientRect() {
    return { left: 0, right: 1, top: 0, bottom: 1 };
  }
  closest() {
    return null;
  }
  matches() {
    return false;
  }
  querySelector() {
    return new El();
  }
  querySelectorAll() {
    return list([]);
  }
  showModal() {
    this.open = true;
  }
  close() {
    this.open = false;
  }
}
const list = (items) => Object.assign(items, { forEach: Array.prototype.forEach.bind(items) });
const els = new Map();
const el = (key) => {
  if (!els.has(key)) els.set(key, new El());
  return els.get(key);
};
const listeners = {};
globalThis.document = {
  querySelector: (sel) => el(sel),
  querySelectorAll: () => list([]),
  createElement: (tag) => new El(tag),
  addEventListener: (type, fn) => {
    listeners[type] = fn;
  },
  body: new El("body"),
  documentElement: new El("html"),
};
globalThis.window = {
  addEventListener: (type, fn) => {
    listeners[type] = fn;
  },
  scrollTo() {},
  print() {},
};
globalThis.location = { hash: "" };
globalThis.history = { replaceState() {}, pushState() {} };
globalThis.fetch = async () => ({ ok: true, json: async () => data });
globalThis.Blob = class {
  constructor() {
    return {};
  }
};
const realURL = globalThis.URL;
globalThis.URL = Object.assign((...a) => new realURL(...a), realURL, {
  createObjectURL: () => "blob:stub",
  revokeObjectURL() {},
});

await import("../app.js");
const main = el("#main");

const BAD = [
  /undefined/,
  /NaN/,
  /\[object Object\]/,
  /\$\{/,
  />null</,
  /cite\(/,
];
async function render(hash) {
  globalThis.location.hash = hash;
  listeners.hashchange?.();
  // The directory renders its table into a separate container, so both roots
  // are concatenated before the leak scan.
  return main.innerHTML + el("#directory-results").innerHTML;
}

test("app boots, wires the hashchange router and renders the summary", async () => {
  assert.equal(typeof listeners.hashchange, "function");
  const html = await render("#summary");
  assert.match(html, /Find the right expertise\./);
  assert.equal(el(".nav-count").textContent, data.businesses.length);
  assert.match(el("#snapshot-date").textContent, /Sep 11, 2026/);
  assert.equal(el("#snapshot-date").dateTime, data.researchedAt);
  const cards = html.match(/data-detail="[^"]+"/g) || [];
  assert.equal(cards.length, data.businesses.filter((b) => b.priority).length);
  for (const p of BAD) assert.equal(p.test(html), false, `${hash()} matched ${p}`);
});
function hash() {
  return globalThis.location.hash;
}

for (const view of ["directory", "reviews", "audit", "method"])
  test(`#${view} renders every record without leaking unresolved values`, async () => {
    const html = await render(`#${view}`);
    assert.ok(html.length > 2000, `${view} rendered suspiciously little`);
    for (const p of BAD)
      assert.equal(p.test(html), false, `${view} output matched ${p}`);
    if (view === "directory") {
      assert.equal(
        (html.match(/data-detail=/g) || []).length,
        data.businesses.length * 2,
        "expected a name button and a view button per record",
      );
      assert.match(html, /Active license checked only/);
      assert.match(html, /Snapshot · Sep 10–11, 2026/);
    }
    if (view === "audit") {
      const numbers = [
        ...new Set(
          data.businesses.filter((b) => b.license).map((b) => `#${b.license.number}`),
        ),
      ];
      for (const n of numbers)
        assert.ok(html.includes(n), `CSLB credential table is missing ${n}`);
      assert.match(html, /Verification ladder/);
      assert.match(html, /License suspended/);
      // wave-7 follow-up: the corroborated-but-now-held record is explained,
      // and the platform pages read directly are named in the ladder
      assert.match(html, /Wave 7 follow-up/);
      assert.match(html, /removed from the call order and placed on hold/);
      assert.match(html, /Thumbtack category and pro pages read directly/);
      assert.match(html, /corrected a wave-6 review attribution in place/);
    }
    if (view === "method") {
      assert.match(html, /70 distinct CSLB license detail pages/);
      assert.match(html, /7 waves/);
      // the live totals must not be attributed to a single wave's bullet
      assert.match(html, /Wave 7 \(Sep 11, 2026\)/);
      assert.match(html, /14 records directory-wide now combine an active license/);
      assert.match(html, /inactive or revoked records/);

    }
  });

test("compliance panel quotes only the official City page", async () => {
  const html = await render("#summary");
  assert.match(html, /OFFICIAL CITY REQUIREMENTS/);
  for (const fact of data.compliance.facts)
    assert.ok(html.includes(fact.replace(/[&<>"']/g, (m) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[m])), fact);
  assert.match(html, /sf\.gov\/apply-plumbing-and-mechanical-permit/);
  assert.match(html, /NOT\s+retrieved/);
});

test("suspended, canceled and expired licenses render a red badge, never a green one", async () => {
  const html = await render("#audit");
  for (const [status, label] of [
    ["expired", "License expired"],
    ["canceled", "License canceled"],
    ["suspended", "License suspended"],
  ]) {
    assert.equal(data.businesses.some((b) => b.license?.status === status), true, status);
    assert.ok(html.includes(label), `${status} badge missing`);
  }
  assert.equal(/✓ Active<\/span>[^<]*<span class="badge red">/.test(html), false);
});

test("every shortlisted trade shows a classification label", async () => {
  const html = await render("#summary");
  for (const label of ["Plumbing (C-36)", "Lathing &amp; plaster (C-35)"])
    assert.ok(html.includes(label), label);
});

test("business deep links open a detail dialog with source-linked evidence", async () => {
  await render("#directory/w6-caledonia-plastering-stucco-inc");
  const html = el("#detail-content").innerHTML;
  assert.ok(el("dialog").open);
  assert.match(html, /Claim-by-claim evidence/);
  assert.match(html, /1057063/);
  assert.match(html, /lath and plaster/);
  assert.equal(/undefined/.test(html), false);
});
