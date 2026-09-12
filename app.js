import {
  escapeHTML as e,
  filterBusinesses,
  toCSV,
  evidenceCounts,
  TRADE_LABELS,
} from "./lib.js";
const main = document.querySelector("#main"),
  dialog = document.querySelector("dialog");
let data,
  page = "summary",
  selected = new Set(),
  filters = { query: "", status: "all", area: "all", license: false },
  reviewFilters = { query: "", platform: "all", theme: "all" };
const fmtDate = (iso) =>
  new Date(`${iso}T12:00:00Z`).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    timeZone: "UTC",
  });
// Two same-month snapshot dates read as a range, so the directory meta line
// stays short enough for a 390px viewport.
const snapshotLabel = () => {
  const ds = data.researchDates;
  if (ds.length < 2) return fmtDate(ds[0]);
  const a = new Date(`${ds[0]}T12:00:00Z`),
    b = new Date(`${ds[ds.length - 1]}T12:00:00Z`);
  const mon = a.toLocaleDateString("en-US", { month: "short", timeZone: "UTC" });
  return a.getUTCFullYear() === b.getUTCFullYear() &&
    a.getUTCMonth() === b.getUTCMonth()
    ? `${mon} ${a.getUTCDate()}\u2013${b.getUTCDate()}, ${b.getUTCFullYear()}`
    : `${fmtDate(ds[0])} and ${fmtDate(ds[ds.length - 1])}`;
};
const LICENSE_STATUS = {
  active: ["✓ Active", ""],
  expired: ["! License expired", "red"],
  canceled: ["✕ License canceled", "red"],
  cancelled: ["✕ License canceled", "red"],
  suspended: ["⛔ License suspended", "red"],
  inactive: ["! License inactive", "red"],
};
const accessLabels = {
  page: "Page read",
  "search-extract": "Indexed extract only",
  "blocked-with-search-extract": "Direct access blocked · indexed extract",
  redirect: "Identity-changing redirect",
  "expired-site": "Website expired",
};
const areaLabels = {
  outer: "Outer Sunset stated",
  sunset: "Sunset / citywide stated",
  sf: "SF / Bay Area stated",
  unknown: "Coverage unconfirmed",
  outside: "Outside-area concern",
};
const statusLabels = {
  research: "Research candidate",
  hold: "On hold",
  excluded: "Scope excluded",
};
function source(id) {
  return data.sources.find((s) => s.id === id);
}
function business(id) {
  return data.businesses.find((b) => b.id === id);
}
function ext(url, label, cls = "") {
  return `<a class="${cls}" href="${e(url)}" target="_blank" rel="noopener noreferrer">${label}</a>`;
}
function cite(id) {
  const s = source(id);
  return ext(s.url, `[${id}]`, "cite");
}
function citations(ids) {
  return [...new Set(ids)].map(cite).join(" ");
}
function badge(text, type = "") {
  return `<span class="badge ${type}">${text}</span>`;
}
function licenseBadge(b) {
  if (!b.license) return badge("License unchecked", "gray");
  const [label, type] = LICENSE_STATUS[b.license.status] || [
    `! ${b.license.status}`,
    "red",
  ];
  return badge(label, type);
}
function tradeBadge(b) {
  return b.trade ? badge(e(TRADE_LABELS[b.trade] || b.trade), "gray") : "";
}
function statusBadge(b) {
  return badge(
    statusLabels[b.status],
    b.status === "hold" ? "amber" : b.status === "excluded" ? "red" : "gray",
  );
}
function heading(kicker, title, description, action = "") {
  return `<div class="page-heading"><div><div class="eyebrow">${kicker}</div><h1>${title}</h1><p>${description}</p></div>${action}</div>`;
}
function notice(text) {
  return `<div class="notice"><span class="notice-icon" aria-hidden="true">i</span><p>${text}</p></div>`;
}
function stats() {
  const c = evidenceCounts(data);
  return `<div class="stats"><div class="stat"><span class="stat-label">Businesses discovered</span><div class="stat-value">${c.total}<small>/ ${c.waves} waves</small></div><div class="stat-note">Unique research records, not approved hires</div></div><div class="stat"><span class="stat-label">Active license checks</span><div class="stat-value">${c.active}<small>CSLB records</small></div><div class="stat-note">${c.cslbReads} license pages read directly · ${c.inactive} expired, suspended, canceled, inactive or revoked</div></div><div class="stat"><span class="stat-label">Review excerpts retained</span><div class="stat-value">${c.reviews}<small>selected evidence</small></div><div class="stat-note">Partial sample · not all published reviews</div></div><div class="stat"><span class="stat-label">Fully qualified master list</span><div class="stat-value">${c.master}<small>approved entries</small></div><div class="stat-note">Exact-task evidence remains unverified</div></div></div>`;
}
function mapArt() {
  return `<div class="hero-art" aria-hidden="true"><svg viewBox="0 0 420 280" preserveAspectRatio="xMidYMid slice"><defs><pattern id="grid" width="29" height="23" patternUnits="userSpaceOnUse" patternTransform="rotate(-13)"><path d="M0 0H29V23" fill="none" stroke="#c7d5bb" stroke-width="1.4"/></pattern></defs><path d="M0 0H420V280H0Z" fill="#e1ead9"/><path d="M90 0Q128 65 82 130T46 280H0V0Z" fill="#cbdcd2"/><path d="M115 0Q146 70 107 147T74 280H420V0Z" fill="url(#grid)"/><path d="M22 7Q53 71 20 118M42 22Q70 85 42 133M20 179Q40 222 15 268" fill="none" stroke="#b5cdc2" stroke-width="1.2"/><path d="M137 34L420 3V53L128 83Z" fill="#c0d2b2"/><path d="M124 91L420 37M96 200L420 139" stroke="#f6f8ee" stroke-width="5"/><circle cx="224" cy="153" r="55" fill="#b5cbb2" opacity=".28"/><circle cx="224" cy="153" r="39" fill="none" stroke="#749878" stroke-dasharray="3 5"/><path d="M224 121c-12 0-21 9-21 21 0 16 21 35 21 35s21-19 21-35c0-12-9-21-21-21Z" fill="#24604a"/><circle cx="224" cy="141" r="7" fill="#f4e9ca"/><rect x="155" y="192" width="140" height="31" rx="5" fill="#fbfcf7"/><text x="225" y="212" font-size="11" font-family="sans-serif" fill="#32563f" text-anchor="middle" letter-spacing="1">OUTER SUNSET</text><text x="28" y="212" transform="rotate(-90 28 212)" font-size="8" font-family="sans-serif" fill="#6e9180" letter-spacing="2">PACIFIC OCEAN</text></svg><div class="map-caption">NEIGHBORHOOD FOCUS · ILLUSTRATIVE MAP</div></div>`;
}
function card(b) {
  const rv = data.reviews.find((r) => r.business === b.id),
    ids = [
      b.claims[0].source,
      b.claims.find((c) => c.field === "Coverage")?.source,
      b.license?.source,
      rv?.source,
    ].filter(Boolean);
  return `<article class="candidate"><div class="candidate-body"><div class="candidate-top"><span class="rank">DIAGNOSTIC CALL <b>${String(b.priority).padStart(2, "0")}</b></span>${tradeBadge(b)}${licenseBadge(b)}</div><h3>${e(b.name)}</h3><p class="area">↳ ${e(b.areaText)} ${cite(b.claims.find((c) => c.field === "Coverage")?.source || b.claims[0].source)}</p><div class="label">WHY CONSIDER THEM</div><p class="reason">${e(b.rationale)} ${citations(ids)}</p><p class="caveat">No confirmed seized-overflow extraction case. Not cleared for booking.</p></div><div class="candidate-bottom"><button class="button-secondary button-small" data-detail="${b.id}">View evidence <span>↗</span></button>${b.website ? ext(b.website, "Official site ↗", "text-link") : ext(source(b.license?.source || b.claims[0].source).url, "Primary record ↗", "text-link")}</div></article>`;
}
function compliancePanel() {
  const c = data.compliance;
  if (!c) return "";
  const s = source(c.sourceId);
  return `<section class="panel compliance"><div class="compliance-head"><div><div class="eyebrow">OFFICIAL CITY REQUIREMENTS · VERIFIED ${fmtDate(c.checkedAt)}</div><h3>Permits and inspections are part of this scope, not an afterthought</h3><p>${e(c.jurisdiction)} ${cite(c.sourceId)}</p></div>${badge(s?.access === "page" ? "Official page read directly" : "Official source", s?.access === "page" ? "" : "amber")}</div><ul class="compliance-facts">${c.facts
    .map((f) => `<li>${e(f)}</li>`)
    .join("")}</ul><p class="compliance-position">${e(c.position)}</p><p class="compliance-why">${e(c.why)}</p><div class="dialog-actions">${c.officialLinks
    .map((l) => ext(l.url, e(l.label) + " ↗", "button-secondary"))
    .join("")}</div>${c.notRetrieved
    .map(
      (n) =>
        `<div class="notice"><p><strong>${e(n.label)}</strong> — ${e(n.note)} ${ext(n.url, "Open the code section ↗", "text-link")}</p></div>`,
    )
    .join("")}</section>`;
}
function renderSummary() {
  const short = data.businesses
      .filter((b) => b.priority)
      .sort((a, b) => a.priority - b.priority),
    tierA = short.filter((b) => b.priority <= 5),
    tierB = short.filter((b) => b.priority > 5);
  main.innerHTML = `${heading("THE DECISION BRIEF", "Find the right expertise.", "A repair-first shortlist for the Outer Sunset, with the evidence—and the gaps—in plain sight.", '<button class="button-secondary no-print" id="print-summary">↓ Print brief</button>')}
<section class="hero"><div class="hero-content"><div class="eyebrow">PRESERVE FIRST. REPLACE ONLY IF NECESSARY.</div><h1>A careful repair starts<br>with a better-informed choice.</h1><p>Prioritize an experienced diagnostic plumber for a stuck bathtub overflow mechanism. Start with the least invasive viable approach, not a promise that replacement can be avoided.</p><div class="hero-links"><a class="button" href="#directory">Explore ${data.businesses.length} businesses <span>→</span></a><a href="#method">How we evaluate the evidence ↗</a></div></div>${mapArt()}</section>${stats()}
${notice("<strong>Shortlist ≠ fully verified fit.</strong> These are candidates for a diagnostic conversation, not approved hires. No reviewed source proves successful extraction of this exact seized mechanism without opening walls. Unresolved entries remain outside the qualified master list.")}
<section><div class="section-heading"><div><h2>Start with this call order</h2><p>Editorial call order based on task proximity, service-area evidence and direct credential checks.</p></div><a class="text-link" href="#directory">All candidates →</a></div><div class="shortlist">${tierA
    .map(card)
    .join("")}</div></section>
${tierB.length ? `<section><div class="section-heading"><div><h2>Credential additions from the latest pass</h2><p>Added on a stricter basis than calls 01–05: each holds an active license whose CSLB page <em>itself</em> records a 94122 Outer Sunset business address, and each carries the classification its trade requires. Same caveats apply — none is cleared for booking.</p></div><a class="text-link" href="#audit">Verification ledger →</a></div><div class="shortlist">${tierB
      .map(card)
      .join("")}</div></section>` : ""}
${compliancePanel()}
<div class="summary-bottom"><section class="panel"><h3>Before authorizing any work</h3><p>Suggested decision gates—not a do-it-yourself repair procedure.</p><ol class="steps"><li><span class="step-num">1</span><div><strong>Confirm the right technician</strong><p>Ask for prior seized trip-lever / plunger jobs, the access method used, and experience preserving older assemblies.</p></div></li><li><span class="step-num">2</span><div><strong>Set a clear stop point</strong><p>Request diagnosis and a written repair-first scope. Require separate approval before opening a wall or replacing hidden piping.</p></div></li><li><span class="step-num">3</span><div><strong>Match the trade to the work</strong><p>Confirm which license classification covers each part: C-36 for pipe work, C-9 or C-35 for the ceiling patch, and who frames and installs any access panel.</p></div></li><li><span class="step-num">4</span><div><strong>Recheck credentials and closeout</strong><p>Confirm the contracting entity, current insurance, area coverage, permit and inspection responsibility, testing and restoration responsibilities.</p></div></li></ol></section><section class="panel"><h3>Important findings, not buried</h3><div class="mini-flag"><strong>Two licenses suspended on one bond date</strong><p>All-Point Solutions Plumbing (950265) and F C Company (1022789) both read as “License is under Contractors Bond Suspension”, and both show a contractor's bond with Hudson Insurance Company carrying a cancellation date of 09/01/2026. All-Point's CSLB address is 1651 42nd Avenue, 94122. A suspended license cannot lawfully contract. ${cite(business("w6-all-point-solutions-plumbing-co").license.source)} ${cite(business("w6-f-c-company").license.source)}</p></div><div class="mini-flag"><strong>Mr. Rooter's Judah Street entity lapsed in 2018</strong><p>CSLB reads B R Troika Incorporated dba Mr Rooter Plumbing (812845) at 2341 Judah, 94122 as expired 09/30/2018 and “not able to contract”. That is a second lapsed C-36 behind the same brand, alongside SDP Plumbing Inc (1016070, expired 07/31/2024). The registry also records two spellings and two Judah Street numbers for it. ${cite(business("w6-b-r-troika-incorporated-dba-mr-rooter-plumbing").license.source)}</p></div><div class="mini-flag"><strong>Right address, wrong classification</strong><p>Gorman Pipeline Inc (898289) is active at 1518 27th Ave, 94122 — but the CSLB page shows A (General Engineering) only, with sewer-construction workers-compensation codes and no C-36. It is recorded as a scope exclusion so it is not mistaken for a plumber. ${cite(business("w6-gorman-pipeline-inc").license.source)}</p></div><div class="mini-flag"><strong>Marketing that does not match the regulator</strong><p>RS Dynamic Builders publishes CSLB# 1130530 and lists “Sunset” in its service area, but CSLB records B (General Building) only — no C-36 and no C-9 — issued 12/16/2024 with no covered employees. Its own structured data gives streetAddress “123 Main Street” against CSLB's 909 Ocean View Ave, and a 415 phone against CSLB's 650 number. ${cite(business("w6-r-s-dynamic-builders-inc").license.source)} ${cite(191)}</p></div><div class="mini-flag"><strong>Registry history is not present operation</strong><p>West Cork Plumbing (900309), Flow Masters Plumbing (966337) and Moonlight Plumbing (976543) each hold Outer Sunset permit histories in the official registry, yet CSLB now records Novato, Daly City and Yucca Valley addresses. Moonlight's license also expires 09/30/2026, nineteen days after the check. ${cite(150)} ${cite(160)}</p></div><div class="mini-flag"><strong>Franchise site live · license expired</strong><p>Mr. Rooter of San Francisco advertises 266 reviews at 4.8/5, but the local franchisee's C36 (SDP Plumbing Inc) expired 07/31/2024 per direct CSLB check. A brand site is not a license. ${cite(business("mr-rooter-sf").license.source)} ${cite(business("mr-rooter-sf").claims[0].source)}</p></div><div class="mini-flag"><strong>Believed out of business · Master Rooter</strong><p>BBB lists this long-time 38th Ave firm as believed out of business; its Yelp sample is 1.6★/26 unclaimed, and the SF registry links it to Metro Rooter/Simovich at 1526 Irving St. ${cite(business("master-rooter").claims[1].source)} ${cite(business("master-rooter").claims[0].source)}</p></div><div class="mini-flag"><strong>License reissued · 5 Star Plumbing</strong><p>CSLB notes license 996627 was reissued to another entity on 11/17/2025, and the registry shows similarly named firms. Confirm the exact legal entity before contracting. ${cite(business("five-star").license.source)}</p></div><div class="mini-flag"><strong>License concern · Plumbing Pure</strong><p>Listed license 1017368 was expired when checked; another active license was not established. ${cite(business("plumbing-pure").license.source)}</p></div><div class="mini-flag"><strong>Review identity changed · Thumbtack</strong><p>The former Plumbing Pure profile now redirects to Legato. Historical reviews are not merged across businesses. ${cite(data.sources.find((s) => s.access === "redirect").id)}</p></div><div class="mini-flag"><strong>Scope mismatch · Precision Rooter</strong><p>Indexed business description says no plumbing repairs. Direct Yelp access was blocked. ${cite(business("precision-rooter").claims[0].source)}</p></div><div class="mini-flag"><strong>Review naming the wrong person · rejected</strong><p>An indexed excerpt praising “Singh” appeared on the Jose HandyMan Services listing. Because the reviewer's name does not match the business, it was rejected rather than attached — the same index-text-bleed pattern flagged in wave 4. ${cite(178)}</p></div><a class="text-link" href="#audit">See verification & all flags →</a></section></div>`;
  document.querySelector("#print-summary").onclick = () => window.print();
}
function renderDirectory() {
  main.innerHTML = `${heading("THE RESEARCH DIRECTORY", `${data.businesses.length} leads. Every gap visible.`, "Search the discovery pool, inspect source-backed claims, and compare up to three businesses. Only entries passing all evidence gates can enter the qualified master list.", '<button id="export" class="button-secondary">↓ Export visible CSV</button>')}
<div class="filters" aria-label="Candidate status">${[
    ["all", "All candidates"],
    ["shortlist", "Diagnostic shortlist"],
    ["master", "Qualified master"],
    ["hold", "On hold"],
    ["excluded", "Scope excluded"],
  ]
    .map(
      ([v, l]) =>
        `<button class="filter-pill ${filters.status === v ? "active" : ""}" data-status="${v}" aria-pressed="${filters.status === v}">${l}</button>`,
    )
    .join(
      "",
    )}<label class="checkbox-label"><input id="active-license" type="checkbox" ${filters.license ? "checked" : ""}> Active license checked only</label></div>
<div class="toolbar"><label class="search"><span aria-hidden="true">⌕</span><input id="business-search" type="search" placeholder="Search business name, services or evidence…" aria-label="Search businesses" value="${e(filters.query)}"></label><select id="area-filter" aria-label="Filter by service area"><option value="all">All service-area evidence</option>${Object.entries(
    areaLabels,
  )
    .map(
      ([v, l]) =>
        `<option value="${v}" ${filters.area === v ? "selected" : ""}>${l}</option>`,
    )
    .join("")}</select></div>
<div id="directory-results"></div>`;
  document.querySelector("#business-search").oninput = (ev) => {
    filters.query = ev.target.value;
    directoryResults();
  };
  document.querySelector("#area-filter").onchange = (ev) => {
    filters.area = ev.target.value;
    directoryResults();
  };
  document.querySelector("#active-license").onchange = (ev) => {
    filters.license = ev.target.checked;
    directoryResults();
  };
  document.querySelectorAll("[data-status]").forEach(
    (btn) =>
      (btn.onclick = () => {
        filters.status = btn.dataset.status;
        renderDirectory();
      }),
  );
  document.querySelector("#export").onclick = () =>
    download(
      toCSV(filterBusinesses(data.businesses, filters), data.sources),
      "sunset-repair-candidates.csv",
      "text/csv;charset=utf-8",
    );
  directoryResults();
}
function directoryResults() {
  const items = filterBusinesses(data.businesses, filters);
  document.querySelector("#directory-results").innerHTML =
    `<div class="result-meta" role="status"><span>${items.length} of ${data.businesses.length} research records</span><span>Snapshot · ${snapshotLabel()}</span></div>${items.length ? `<div class="table-wrap"><table class="directory-table"><thead><tr><th><span class="small">Compare</span></th><th>BUSINESS / EVIDENCE</th><th>SERVICE AREA</th><th>CREDENTIAL CHECK</th><th>RESEARCH STATUS</th><th>DETAILS</th></tr></thead><tbody>${items.map((b) => `<tr><td><input class="table-check" type="checkbox" aria-label="Compare ${e(b.name)}" data-compare="${b.id}" ${selected.has(b.id) ? "checked" : ""}></td><td><button class="row-name" data-detail="${b.id}">${e(b.name)}</button>${b.priority ? ` <span class="badge">Call ${String(b.priority).padStart(2, "0")}</span>` : ""}<p>${e(b.claims[0].text)} ${cite(b.claims[0].source)}</p></td><td>${badge(areaLabels[b.area], b.area === "outer" ? "" : b.area === "outside" ? "amber" : "gray")}<p>${e(b.areaText)}</p></td><td>${licenseBadge(b)} ${tradeBadge(b)}<p>${b.license ? `#${b.license.number} · ${e(b.license.classes.join(", "))} ${cite(b.license.source)}` : "No CSLB page read for this record"}</p></td><td>${statusBadge(b)}<p>${b.reviewIds.length ? `${b.reviewIds.length} review excerpt${b.reviewIds.length === 1 ? "" : "s"}` : "No review sample retained"}${b.flags.length ? ` · ${b.flags.length} flag${b.flags.length === 1 ? "" : "s"}` : ""}</p></td><td><button class="button-secondary button-small" data-detail="${b.id}" aria-label="View ${e(b.name)}">View ↗</button></td></tr>`).join("")}</tbody></table></div>` : `<div class="empty"><h3>${filters.status === "master" ? "No businesses have passed every gate." : "No candidates match these filters."}</h3><p>${filters.status === "master" ? "This is intentional. Missing exact-task evidence is not replaced with an assumed qualification." : "Try a broader search or reset the filters."}</p><button class="button-secondary" id="reset-filters">Show all candidates</button></div>`}`;
  document.querySelector("#reset-filters")?.addEventListener("click", () => {
    filters = { query: "", status: "all", area: "all", license: false };
    renderDirectory();
  });
}
function reviewCard(r) {
  const b = business(r.business);
  return `<article class="review-card"><div class="review-head"><button class="row-name" data-detail="${b.id}">${e(b.name)}</button>${badge(e(r.platform), r.platform === "Business site" ? "gray" : "")}</div><span>${badge(e(r.theme), r.negative ? "amber" : "gray")}</span><blockquote>“${e(r.quote)}”</blockquote><div class="review-meta">${e(r.author)} · ${e(r.published || "Publication date not available")} ${cite(r.source)}</div><div class="review-analysis"><div class="label">WHAT THIS ACTUALLY SUPPORTS</div><p>${e(r.analysis)}</p></div><div class="review-foot">${badge(r.access === "page" ? "Visible page sample" : "Indexed extract only", r.access === "page" ? "gray" : "amber")}${ext(source(r.source).url, "Open original source ↗", "text-link")}</div></article>`;
}
function renderReviews() {
  const platformCount = (name) => data.reviews.filter((r) => r.platform === name).length;
  main.innerHTML = `${heading("READ THE EVIDENCE", "Relevant words. Not just stars.", `${data.reviews.length} short review excerpts retained from the accessible sample. Every interpretation is tied to its source; all remain customer accounts, not verified technical outcomes.`)}
${notice("<strong>Not an all-review aggregation.</strong> Yelp and Reddit direct access was blocked on tested pages. Google’s review panel did not load. Thumbtack exposes a partial sample. Business-hosted testimonials are labeled separately; no blended star score is calculated.")}
<div class="coverage-grid"><div class="coverage-card"><h3>Yelp</h3>${badge("Limited access", "amber")}<p>${platformCount("Yelp")} excerpts retained from indexed business profiles and snippets; no complete Yelp review corpus was read.</p></div><div class="coverage-card"><h3>Thumbtack</h3>${badge("Partial sample")}<p>${platformCount("Thumbtack")} excerpts retained from accessible profiles. Historical identity redirect remains quarantined.</p></div><div class="coverage-card"><h3>Reddit</h3>${badge("Indexed anecdote", "amber")}<p>${platformCount("Reddit")} excerpts retained from search extracts. Direct thread access was blocked on tested pages.</p></div><div class="coverage-card"><h3>Google</h3>${badge("Review panel unavailable", "amber")}<p>Official profile links located, but no original Google review corpus was retrieved.</p></div></div>
<div class="toolbar"><label class="search"><span aria-hidden="true">⌕</span><input type="search" id="review-search" aria-label="Search review evidence" placeholder="Search excerpts or businesses…" value="${e(reviewFilters.query)}"></label><select id="review-platform" aria-label="Filter review platform"><option value="all">All platforms</option>${[...new Set(data.reviews.map((r) => r.platform))].map((p) => `<option ${reviewFilters.platform === p ? "selected" : ""}>${e(p)}</option>`).join("")}</select><select id="review-theme" aria-label="Filter review theme"><option value="all">All evidence themes</option>${[...new Set(data.reviews.map((r) => r.theme))].map((t) => `<option ${reviewFilters.theme === t ? "selected" : ""}>${e(t)}</option>`).join("")}</select></div><div id="review-results"></div>`;
  document.querySelector("#review-search").oninput = (ev) => {
    reviewFilters.query = ev.target.value;
    reviewResults();
  };
  document.querySelector("#review-platform").onchange = (ev) => {
    reviewFilters.platform = ev.target.value;
    reviewResults();
  };
  document.querySelector("#review-theme").onchange = (ev) => {
    reviewFilters.theme = ev.target.value;
    reviewResults();
  };
  reviewResults();
}
function reviewResults() {
  const q = reviewFilters.query.toLowerCase();
  const rows = data.reviews.filter(
    (r) =>
      (reviewFilters.platform === "all" ||
        r.platform === reviewFilters.platform) &&
      (reviewFilters.theme === "all" || r.theme === reviewFilters.theme) &&
      [r.quote, r.analysis, business(r.business).name]
        .join(" ")
        .toLowerCase()
        .includes(q),
  );
  document.querySelector("#review-results").innerHTML =
    `<div class="result-meta" role="status">${rows.length} of ${data.reviews.length} retained excerpts · none establishes exact-task success</div><div class="review-grid">${rows.map(reviewCard).join("")}</div>${!rows.length ? '<div class="empty"><h3>No excerpts match.</h3><p>Try another keyword, platform or theme.</p></div>' : ""}`;
}
function flagHTML(b, f) {
  return `<article class="flag-item"><div>${badge(f.level === "hold" ? "Booking / scope hold" : f.level === "gap" ? "Evidence gap" : "Source discrepancy", f.level === "hold" ? "red" : "amber")}</div><div><button class="row-name" data-detail="${b.id}">${e(b.name)}</button><p>${e(f.text)} ${citations(f.sources)}</p></div></article>`;
}
function renderAudit() {
  const flags = data.businesses
    .flatMap((b) => b.flags.map((f) => ({ b, f })))
    .sort(
      (a, b) => (a.f.level === "hold" ? 0 : 1) - (b.f.level === "hold" ? 0 : 1),
    );
  main.innerHTML = `${heading("THE VERIFICATION LEDGER", "Evidence you can trace.", "Direct registry checks are distinct from business marketing, platform posts and directory leads. A license check never certifies a specific repair outcome.")} ${stats()}
<div class="section-heading"><div><h2>Irregularities & unresolved evidence</h2><p>Not all flags are wrongdoing. Conflicting dates, redirects and expired websites require caution.</p></div></div><div class="flag-list">${flags.map(({ b, f }) => flagHTML(b, f)).join("")}</div>
${(() => {
    const c = evidenceCounts(data);
    const read = data.businesses.filter((b) => b.license).length;
    const ladder = [
      ["Regulator read", "CSLB license detail page read directly on cslb.ca.gov", read, "Establishes legal entity, classification, status, expiry, bond and workers-compensation lines at the check date. Never establishes a repair outcome."],
      ["Official registry", "SF DBI “Plumbing Permits Contacts” open data (k6kv-9kix)", c.registryOnly, "Recorded firm name, CSLB number, business address and permit-row count. Historical rows with no in-dataset dates: never proof of present operation, and never a license status."],
      ["Directory / marketing", "Indexed Yelp, BBB, BuildZoom and Angi extracts, company sites, and Thumbtack category and pro pages read directly", c.total - read - c.registryOnly, "Names, ratings, badges, service-area statements and short review excerpts. Discovery only — a platform badge is not a license."],
    ];
    return `<div class="section-heading"><div><h2>Verification ladder</h2><p>Every record sits on exactly one of these evidence levels. Higher levels are rarer and say less about workmanship than they appear to.</p></div><span class="badge gray">${c.total} records</span></div><div class="table-wrap"><table><thead><tr><th>EVIDENCE LEVEL</th><th>SOURCE TYPE</th><th>RECORDS</th><th>WHAT IT CAN AND CANNOT PROVE</th></tr></thead><tbody>${ladder.map(([a, b_, n, d]) => `<tr><td><strong>${a}</strong></td><td>${b_}</td><td>${n}</td><td>${d}</td></tr>`).join("")}</tbody></table></div>${notice("<strong>Cross-check result for wave 6.</strong> Three independent third parties (the company site footer, BBB and BuildZoom) all published CSLB #1057063 for Caledonia Plastering &amp; Stucco, and the direct CSLB read confirmed that number, the legal name, the 1551 Judah Street 94122 address and the 08/31/2027 expiry. Wave 4’s Repipe Champions number did <em>not</em> survive the same test. A third-party license number is therefore always treated as a lead until CSLB is read. <strong>Wave 7 follow-up.</strong> That same Caledonia record was removed from the call order and placed on hold after its Thumbtack profile was read directly and published a negative review alleging refused corrections and a bathroom exhaust covered with plaster, alongside the platform’s own “this pro can’t do your job” response for its stated ZIP. Corroborating a license number proves identity and classification; it says nothing about conduct, and a 4.9 rating is not treated as cancelling out a specific allegation. Wave 7 also corrected a wave-6 review attribution in place after a direct read showed the stored quote belonged to a different reviewer than the stored author.")}`;
  })()}
<div class="section-heading"><div><h2>CSLB credential checks</h2><p>Direct CSLB reads dated ${snapshotLabel()}. Current status may change at any time; insurance coverage must match the work.</p></div></div><div class="table-wrap"><table><thead><tr><th>BUSINESS / LEGAL ENTITY</th><th>LICENSE</th><th>STATUS AT CHECK</th><th>EXPIRATION</th></tr></thead><tbody>${data.businesses
    .filter((b) => b.license)
    .map(
      (b) =>
        `<tr><td><strong>${e(b.name)}</strong><p>${e(b.license.entity)}</p>${tradeBadge(b)}</td><td>#${b.license.number} ${cite(b.license.source)}<p>${b.license.classes.join(" · ")}</p></td><td>${licenseBadge(b)}<p>${b.license.checkedAt}</p></td><td>${b.license.expires}</td></tr>`,
    )
    .join("")}</tbody></table></div>
<div class="section-heading"><div><h2>Source register</h2><p>${data.sources.length} evidence references · duplicated URLs may represent different evidence roles, not independent corroboration.</p></div><a class="text-link" href="./data/research.json" download>Download evidence JSON ↓</a></div><div class="source-list">${data.sources.map((s) => `<details class="source-item" id="source-${s.id}"><summary><strong>[${s.id}] ${e(s.title)}</strong>${badge(e(accessLabels[s.access] || s.access), s.access === "page" ? "gray" : "amber")}</summary><p>${ext(s.url, e(s.url))}</p><p>Role: ${e(s.kind)} · Checked ${s.checkedAt}${s.note ? `<br>${e(s.note)}` : ""}</p></details>`).join("")}</div>`;
}
function renderMethod() {
  const counts = evidenceCounts(data);
  main.innerHTML = `${heading("HOW THIS WORKS", "Evidence first. Assumptions out.", "A transparent, conservative research system. Built to help a decision-maker ask the right questions—not to manufacture certainty.")}
<div class="method-grid"><section class="panel"><h3>What “verified” means here</h3><p><strong>Registry fact:</strong> a direct CSLB record supports legal identity, classification and license status at the recorded date. The regulator does not certify this job’s feasibility.</p><p><strong>Business claim:</strong> a company’s own site supports what it advertises, including service area and scope. That is not independent proof of workmanship or availability.</p><p><strong>Customer account:</strong> an original-platform review is evidence that a statement was published, not proof that the job happened exactly as described.</p><p><strong>Discovery only:</strong> directory or search results establish a lead to investigate. They cannot make a contractor eligible for the master list.</p></section><section class="panel"><h3>Qualified master: strict admission</h3><p>All five gates must be supported before promotion. Currently <strong>0 of ${data.businesses.length}</strong> entries pass every gate.</p><ol>${data.methodology.promotionGates.map((g) => `<li>${e(g)}</li>`).join("")}</ol><p>Unverified does not mean unqualified. It means this research has not established the claim.</p></section><section class="panel span-two"><h3>The research workflow</h3><div class="rule"><b>01</b><div><strong>Discover without assuming</strong><p>Find candidate names through local search, Yelp, Thumbtack, Reddit and business sites. Keep each discovery wave's unique records separate from the qualified master.</p></div></div><div class="rule"><b>02</b><div><strong>Resolve the entity</strong><p>Match business name, published site, phone and CSLB legal identity when available. Hold redirects and ambiguous profiles; never merge reviews just because names look similar.</p></div></div><div class="rule"><b>03</b><div><strong>Attach claims to evidence</strong><p>Store source URL, access mode, checked date, supporting excerpt and interpretation. Missing publication dates stay missing. A neighbor’s account-verification year is not a review date.</p></div></div><div class="rule"><b>04</b><div><strong>Classify relevance, not sentiment scores</strong><p>Look for tub mechanisms, diagnostic options, careful repairs, clean work and cost cautions. Generic drain cleaning, trenchless sewer work and faucet replacement never become proof of seized overflow extraction.</p></div></div><div class="rule"><b>05</b><div><strong>Check the classification, not just the status</strong><p>An active license is only useful if its classification covers the work. Wave 6 records an active A (General Engineering) licensee at an Outer Sunset address as a scope exclusion, an active B-only licensee as a booking hold, and two contractors’ bond suspensions — none of which a status-only check would have caught.</p></div></div><div class="rule"><b>06</b><div><strong>Verify the rules of the jurisdiction</strong><p>Permit and inspection requirements are read from the City’s own service page, not from contractor blogs or forum advice, and are reproduced on the decision brief with official links. Where the exemption text itself was not retrieved, the site says so instead of paraphrasing it.</p></div></div><div class="rule"><b>07</b><div><strong>Monitor without silently approving</strong><p>The source-audit workflow checks allowed registered URLs, redirects and retained quotations on pushes. Its weekly trigger becomes active once the workflow exists on the repository’s default branch. It produces an artifact with changed, blocked or missing evidence. It does not overwrite reviewed findings, approve candidates or invent inaccessible reviews.</p></div></div></section><section class="panel"><h3>Limits of this research pass</h3><p><strong>Initial automated monitor:</strong> 45 URLs attempted; 44 skipped because robots policy could not be established, one DNS failure, zero pages retrieved. This is separate from the curated web-research checks. It is not successful re-verification.</p><ul><li>${counts.total} businesses discovered across ${counts.waves} waves; ${counts.cslbReads} distinct CSLB license detail pages read directly on cslb.ca.gov. ${counts.active} records show an active license and ${counts.inactive} show expired, canceled, suspended, inactive or revoked records — every lapsed record is held, not hidden. ${counts.unchecked} records are discovery-level with no regulator read at all.</li>
<li>Wave 6 (Sep 11, 2026) raised the floor: 22 of its 50 records carry a CSLB page read directly, including 14 active licenses, 13 of them at an address the regulator itself records as 94122 rather than as marketing copy claimed.</li><li>Wave 7 (Sep 11, 2026) added 50 records through three channels kept deliberately separate: 12 CSLB license detail pages read directly (one active C-36 whose CSLB page records a 94122 address, the rest expired, inactive or revoked and every one held), 20 registry-only 94122 leads queried straight from the City’s permit dataset by firm ZIP, and 20 Thumbtack drywall listings read directly. Its follow-up pass read two Thumbtack pro profiles and two grouped registry re-queries and applied them to seven PRE-EXISTING records rather than counting them twice: an expired C-36 attached to a wave-1 row, a corroborating CSLB re-read on a wave-2 row, and four dated drywall-ceiling reviews on a wave-5 row whose platform C-9 credential publishes no readable CSLB number. ${counts.outerVerified} records directory-wide now combine an active license with an Outer Sunset (94122) address recorded by the regulator itself.</li>
<li>The official SF DBI plumbing-permit registry contains plumbing-permit contacts only, so no drywall, plaster or handyman firm can be discovered through it. The finish trades came from indexed directories and company sites, which is weaker evidence and is labelled as such.</li>
<li>Third-party license numbers (BuildZoom, BBB, company footers) are treated as leads and then re-read on CSLB. In wave 6 all three corroborated #1057063; in wave 4 the Repipe Champions number resolved to a different entity entirely. No third-party number is stored as a license fact without a CSLB read.</li><li>${counts.reviews} short excerpts retained, not all reviews read. Sampling is targeted and not representative.</li><li>No direct Google review corpus retrieved; company-hosted Google excerpts remain testimonials.</li><li>The SF DBI registry rows are historical permit records without in-dataset dates; they prove a recorded address and license linkage, never present operation.</li><li>Blocked Yelp and Reddit pages are not bypassed. Search extracts may be stale. Several long-established Outer Sunset shops have let licenses lapse — every expired record is held, not hidden.</li><li>Review identities, transaction authenticity, current pricing and availability are not independently verified.</li><li>No guaranteed no-opening solution. The actual mechanism and materials require professional diagnosis.</li></ul></section><section class="panel"><h3>Privacy & responsible use</h3><p>This public site contains only a generalized repair objective and public business research. No property address, occupant information, access instructions or private project notes are stored.</p><p>No contact forms are submitted, businesses messaged or appointments booked. Opening a source link is your choice; links use no-referrer protection.</p>
<p>Any plumbing, drywall, ceiling or structural work in San Francisco — especially work affecting an occupied or in-law unit — is the property owner's responsibility and must be performed by licensed contractors in line with San Francisco Department of Building Inspection requirements. This research verifies public credentials; it is not a substitute for permits or an on-site professional assessment.</p><p>There are no third-party analytics, embedded maps, external fonts or tracking scripts. Comparison selections stay in memory and reset when the page reloads.</p><p>Automated audits respect robots exclusions, stop on access barriers and never represent an HTTP success as factual verification.</p></section><section class="panel span-two"><h3>Reproducible and portable</h3><p>The complete dataset includes field-level citations, short evidence excerpts, reviewer attribution, dates, flags and explicit gaps. CSV exports include source URLs. Code tests validate unique identities, references, dates, review assignments and master-list admission rules.</p><div class="dialog-actions"><a class="button-secondary" href="./data/research.json" download>Download research JSON ↓</a>${ext("https://github.com/buffedlizard55-lab/BathTubOverflowSF", "Open source repository ↗", "button-secondary")}</div></section></div>`;
}
function detail(b) {
  document.querySelector("#detail-content").innerHTML =
    `<div class="dialog-header"><div class="eyebrow">CANDIDATE EVIDENCE FILE · ${e(b.id.toUpperCase())}</div>${statusBadge(b)} <span>${licenseBadge(b)}</span><h2 id="dialog-title">${e(b.name)}</h2><p>Not admitted to the qualified master list · Last researched ${fmtDate(b.checkedAt)}${b.trade ? ` · ${e(TRADE_LABELS[b.trade] || b.trade)}` : ""}</p><div class="dialog-actions">${b.website ? ext(b.website, "Business website ↗", "button") + cite(b.websiteSource) : badge("Official website not established", "amber")}${b.phone ? `<a class="button-secondary" href="tel:+1${b.phone.replaceAll("-", "")}">${e(b.phone)}</a>${cite(b.phoneSource)}` : ""}<button class="button-secondary" data-toggle-compare="${b.id}">${selected.has(b.id) ? "Remove from" : "Add to"} comparison</button></div>${b.website && source(b.websiteSource).kind !== "business" ? '<p class="small">Website link comes from a directory or profile; current official ownership has not been verified.</p>' : ""}</div><div class="dialog-body">
${b.flags.length ? `<section><h3>Flags to review</h3>${b.flags.map((f) => `<div class="notice"><p>${e(f.text)} ${citations(f.sources)}</p></div>`).join("")}</section>` : ""}
${b.nextStep ? `<section><h3>Suggested next step</h3><p class="small">${e(b.nextStep)}</p></section>` : ""}
<section><h3>Claim-by-claim evidence</h3>${b.claims.map((c) => `<div class="evidence-row"><div class="label">${e(c.field)}</div><p>${e(c.text)} ${cite(c.source)}</p><blockquote>Supporting excerpt: “${e(c.excerpt)}”</blockquote>${badge(e(accessLabels[source(c.source).access]), source(c.source).access === "page" ? "gray" : "amber")}</div>`).join("")}</section>
${b.license ? `<section><h3>Legal entity & credential snapshot</h3><p class="small">${e(b.license.entity)}<br>License #${b.license.number} · ${e(b.license.classes.join(", "))} · Expires ${b.license.expires} ${cite(b.license.source)}</p><p class="small">Recheck current status, bond and insurance details in the full CSLB record before contracting. No independent workmanship certification is implied.</p></section>` : ""}
<section><h3>Review evidence (${b.reviewIds.length})</h3>${b.reviewIds.length ? b.reviewIds.map((id) => reviewCard(data.reviews.find((r) => r.id === id))).join("") : '<p class="small">No individual review evidence was retained for this entry. This is a research gap, not a negative review finding.</p>'}</section>
${b.platformLinks.length ? `<section><h3>Platform links for inspection</h3><p class="small">Links located from cited sources; the complete review corpus has not been read.</p><div class="dialog-actions">${b.platformLinks.map((p) => ext(p.url, e(p.label) + " ↗", "button-secondary") + cite(p.source)).join("")}</div></section>` : ""}
<section><h3>What remains unknown</h3><ul class="gap-list">${b.gaps.map((g) => `<li>${e(g)}</li>`).join("")}</ul></section></div>`;
  if (!dialog.open) dialog.showModal();
  dialog.scrollTop = 0;
}
function showComparison() {
  document.querySelector("#detail-content").innerHTML =
    `<div class="dialog-header"><div class="eyebrow">SIDE-BY-SIDE EVIDENCE</div><h2 id="dialog-title">Compare candidates</h2><p>Different evidence levels are not interchangeable. None is fully qualified for the exact task.</p></div><div class="dialog-body"><div class="compare-grid">${[
      ...selected,
    ]
      .map((id) => {
        const b = business(id);
        return `<section class="panel"><h3>${e(b.name)}</h3><p>${statusBadge(b)}</p>${licenseBadge(b)}<p>${b.license ? cite(b.license.source) : "Not checked"}</p><div class="label">COVERAGE</div><p>${e(b.areaText)} ${cite(b.claims.find((c) => c.field === "Coverage")?.source || b.claims[0].source)}</p><div class="label">REVIEW EVIDENCE</div><p>${b.reviewIds.length} retained excerpt(s). No exact-task proof.</p><div class="label">BLOCKERS / GAPS</div><p>${e(
          b.flags
            .filter((f) => f.level === "hold")
            .map((f) => f.text)
            .join(" ") || b.gaps[0],
        )}</p><button class="button-secondary button-small" data-detail="${b.id}">Full evidence ↗</button></section>`;
      })
      .join("")}</div></div>`;
  if (!dialog.open) dialog.showModal();
}
function updateCompare() {
  const bar = document.querySelector("#compare-bar");
  bar.hidden = !selected.size;
  bar.innerHTML = `<span>${selected.size} of 3 selected</span><button id="open-comparison" ${selected.size < 2 ? "disabled" : ""}>Compare evidence →</button><button class="clear" id="clear-comparison">Clear</button>`;
  document
    .querySelectorAll("[data-compare]")
    .forEach((c) => (c.checked = selected.has(c.dataset.compare)));
  document.querySelector("#open-comparison").onclick = showComparison;
  document.querySelector("#clear-comparison").onclick = () => {
    selected.clear();
    updateCompare();
  };
}
function toggleCompare(id) {
  if (selected.has(id)) selected.delete(id);
  else if (selected.size < 3) selected.add(id);
  else toast("Compare up to three businesses. Remove one first.");
  updateCompare();
}
let toastTimer;
function toast(text) {
  const t = document.querySelector("#toast");
  t.textContent = text;
  t.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => (t.hidden = true), 4500);
}
function download(content, name, type) {
  const url = URL.createObjectURL(new Blob([content], { type }));
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  toast("Source-linked export downloaded.");
}
function route() {
  const hash = location.hash.slice(1) || "summary";
  const [view, id] = hash.split("/");
  page = ["summary", "directory", "reviews", "audit", "method"].includes(view)
    ? view
    : "summary";
  document.querySelectorAll("[data-nav]").forEach((a) => {
    a.classList.toggle("active", a.dataset.nav === page);
    if (a.dataset.nav === page) a.setAttribute("aria-current", "page");
    else a.removeAttribute("aria-current");
  });
  if (dialog.open) dialog.close();
  ({
    summary: renderSummary,
    directory: renderDirectory,
    reviews: renderReviews,
    audit: renderAudit,
    method: renderMethod,
  })[page]();
  updateCompare();
  if (id && business(id)) detail(business(id));
  window.scrollTo(0, 0);
}
document.addEventListener("click", (ev) => {
  const d = ev.target.closest("[data-detail]");
  if (d) {
    detail(business(d.dataset.detail));
    return;
  }
  const c = ev.target.closest("[data-toggle-compare]");
  if (c) {
    toggleCompare(c.dataset.toggleCompare);
    c.textContent = `${selected.has(c.dataset.toggleCompare) ? "Remove from" : "Add to"} comparison`;
  }
});
document.addEventListener("change", (ev) => {
  if (ev.target.matches("[data-compare]"))
    toggleCompare(ev.target.dataset.compare);
});
document.querySelector(".dialog-close").onclick = () => dialog.close();
dialog.addEventListener("click", (ev) => {
  if (ev.target === dialog) {
    const rect = dialog.getBoundingClientRect();
    if (
      ev.clientX < rect.left ||
      ev.clientX > rect.right ||
      ev.clientY < rect.top ||
      ev.clientY > rect.bottom
    )
      dialog.close();
  }
});
try {
  const response = await fetch("./data/research.json");
  if (!response.ok) throw new Error("Research dataset is unavailable.");
  data = await response.json();
  const navCount = document.querySelector(".nav-count");
  if (navCount) navCount.textContent = data.businesses.length;
  const snap = document.querySelector("#snapshot-date");
  if (snap) {
    snap.dateTime = data.researchedAt;
    snap.textContent = fmtDate(data.researchedAt);
  }
  route();
  window.addEventListener("hashchange", route);
} catch (error) {
  main.innerHTML = `<div class="empty"><h1>Research could not load</h1><p>${e(error.message)}</p><p>Please reload or open the <a href="./data/research.json">source dataset</a>.</p></div>`;
}
