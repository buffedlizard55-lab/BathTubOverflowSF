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
      "Research status",
      "Qualified master",
      "Area evidence",
      "License",
      "License status",
      "Checked",
      "Website",
      "Discovery source",
      "Evidence and caveats",
    ],
  ];
  for (const b of items)
    rows.push([
      b.name,
      b.status,
      b.master ? "yes" : "no",
      b.areaText,
      b.license?.number,
      b.license?.status || "unchecked",
      b.checkedAt,
      b.website,
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
export function mayPromote(b) {
  return (
    b.license?.status === "active" &&
    b.license.classes.includes("C36") &&
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
    master: data.businesses.filter((b) => b.master).length,
    flags: data.businesses.filter((b) => b.flags.length).length,
    holds: data.businesses.filter((b) =>
      ["hold", "excluded"].includes(b.status),
    ).length,
    reviews: data.reviews.length,
  };
}
