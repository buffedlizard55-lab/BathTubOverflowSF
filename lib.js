export const escapeHTML = (value) =>
  String(value ?? "").replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
export function filterBusinesses(
  items,
  { query = "", status = "all", area = "all", license = false } = {},
) {
  const q = query.trim().toLocaleLowerCase();
  return items.filter(
    (b) =>
      (!q ||
        [b.name, b.areaText, ...b.claims.map((c) => c.text)]
          .join(" ")
          .toLocaleLowerCase()
          .includes(q)) &&
      (status === "all" ||
        (status === "shortlist"
          ? Boolean(b.priority)
          : status === "master"
            ? b.master
            : b.status === status)) &&
      (area === "all" || b.area === area) &&
      (!license || b.license?.status === "active"),
  );
}
export function csvCell(value) {
  let s = String(value ?? "");
  if (/^[\s]*[=+@-]/.test(s)) s = "'" + s;
  return '"' + s.replaceAll('"', '""') + '"';
}
export function toCSV(items, sources) {
  const rows = [
    [
      "Business",
      "Trade",
      "Research status",
      "Qualified master",
      "Area evidence",
      "License",
      "License classes",
      "License status",
      "License expires",
      "Checked",
      "Website",
      "Phone",
      "Discovery source",
      "Evidence and caveats",
    ],
  ];
  for (const b of items)
    rows.push([
      b.name,
      b.trade || "",
      b.status,
      b.master ? "yes" : "no",
      b.areaText,
      b.license?.number,
      b.license?.classes?.join(" / "),
      b.license?.status || "unchecked",
      b.license?.expires,
      b.checkedAt,
      b.website,
      b.phone,
      sources.find((s) => s.id === b.claims[0].source)?.url,
      [
        ...b.claims.map(
          (c) =>
            `${c.field}: ${c.text} [${c.source}] ${sources.find((s) => s.id === c.source)?.url}`,
        ),
        ...b.gaps,
        ...b.flags.map((f) => f.text),
      ].join(" | "),
    ]);
  return "\uFEFF" + rows.map((row) => row.map(csvCell).join(",")).join("\r\n");
}
// CSLB classifications this project stores, and the classification set each
// declared trade must actually hold. A record may never be promoted on a
// classification that does not cover the work it would be hired for.
export const ALLOWED_CLASSES = [
  // B-2 Residential Remodeling is a distinct CSLB classification, read directly
  // on license 1120735 in wave 9. It is listed separately rather than folded
  // into B, because a residential-remodeling license does not carry the same
  // scope as a general building license.
  "B-2",
  // C-29 Masonry and C-54 Tile were first read directly in wave 10, on licences
  // 863410 and 489739. Neither covers plumbing or drywall, so both are stored
  // with their own trade label and held as documented scope exclusions instead
  // of being mapped onto a classification that would overstate their scope.
  "C29",
  "C54",
  "C36",
  "C12",
  "C27",
  "C39",
  "C45",
  "C-9",
  "C35",
  "C-4",
  "C4",
  "C10",
  "C16",
  "C20",
  "C42",
  "C22",
  "C-2",
  "C33",
  "C38",
  "C43",
  "C-7",
  "C15",
  "D34",
  "D39",
  "D56",
  "B",
  "A",
];
export const TRADE_CLASSES = {
  plumbing: [["C36"]],
  drywall: [["C-9"], ["B"]],
  plaster: [["C35"], ["B"]],
  finish: [["C-9"], ["C35"], ["B"]],
  general: [["B"]],
  engineering: [["A"]],
  "multi-trade": [["B", "C36"]],
  // Wave 10 scope exclusions: a masonry or tile licence is a real licence and a
  // real trade, but it cannot self-perform either of the two trades this project
  // needs, so neither can ever satisfy a plumbing or drywall requirement.
  "masonry": [["C29"]],
  "tile": [["C54"]],
  // Licence 917252, read directly in wave 10, carries C-9 drywall and C36
  // plumbing on one active licence: the only single licence in the corpus that
  // covers both trades this project requires. It is labelled for what it is
  // rather than folded into multi-trade, which only asserts B + C36.
  "plumbing-and-drywall": [["C-9", "C36"]],
  // Wave 11 preserves real CSLB classifications that do not cover the
  // project's required plumbing-plus-drywall combination. These labels are
  // intentionally non-promotable scope exclusions, not guessed trades.
  "scope-exclusion": [["A"], ["B"], ["C12"], ["C20"], ["C27"], ["C39"], ["C43"], ["C45"]],
  // A registry-only lead asserts no classification at all, so no class set can
  // satisfy it and such a record can never reach the promotion gate.
  "registry-lead": [],
};
export const TRADE_LABELS = {
  plumbing: "Plumbing (C-36)",
  drywall: "Drywall (C-9)",
  plaster: "Lathing & plaster (C-35)",
  finish: "Finish / patch",
  general: "General building (B)",
  engineering: "General engineering (A)",
  "multi-trade": "Multi-trade",
  masonry: "Masonry (C-29) · scope excluded",
  tile: "Tile (C-54) · scope excluded",
  "scope-exclusion": "Other CSLB class · plumbing/drywall scope excluded",
  "plumbing-and-drywall": "Plumbing (C-36) + drywall (C-9) on one licence",
  "registry-lead": "Registry lead · classification not read",
};
export function licenseSupportsTrade(b) {
  const classes = b.license?.classes;
  if (!classes?.length) return false;
  if (!classes.every((c) => ALLOWED_CLASSES.includes(c))) return false;
  // A record without a declared trade is only acceptable on the wave 1-5
  // convention, where every stored license carried C36.
  const combos = b.trade ? TRADE_CLASSES[b.trade] : [["C36"]];
  if (!combos) return false;
  return combos.some((need) => need.every((c) => classes.includes(c)));
}
export function mayPromote(b) {
  return (
    b.license?.status === "active" &&
    licenseSupportsTrade(b) &&
    b.area === "outer" &&
    b.exactMatch === true &&
    b.insuranceVerified === true &&
    b.scopeConfirmed === true &&
    !b.flags.some((f) => f.level === "hold")
  );
}
export function evidenceCounts(data) {
  return {
    total: data.businesses.length,
    active: data.businesses.filter((b) => b.license?.status === "active")
      .length,
    inactive: data.businesses.filter(
      (b) => b.license && b.license.status !== "active",
    ).length,
    unchecked: data.businesses.filter((b) => !b.license).length,
    master: data.businesses.filter((b) => b.master).length,
    flags: data.businesses.filter((b) => b.flags.length).length,
    holds: data.businesses.filter((b) =>
      ["hold", "excluded"].includes(b.status),
    ).length,
    reviews: data.reviews.length,
    waves: (data.waves || []).length,
    // Licence detail pages only. CSLB's area-search form was also read directly
    // but returns no contractor data (POST-only results page), so counting it
    // would overstate the number of licence pages this project has read.
    cslbReads: new Set(
      data.sources
        .filter(
          (s) =>
            s.access === "page" &&
            /cslb\.ca\.gov.*LicenseDetail\.aspx\?LicNum=\d+/.test(s.url),
        )
        .map((s) => s.url.match(/LicNum=(\d+)/)[1]),
    ).size,
    registryOnly: data.businesses.filter(
      (b) =>
        !b.license &&
        b.claims.some(
          (c) => c.field === "Registry" && /Registry-recorded/.test(c.text),
        ),
    ).length,
    outerVerified: data.businesses.filter(
      (b) => b.area === "outer" && b.license?.status === "active",
    ).length,
  };
}
