import { test, expect } from "@playwright/test";
import { readFileSync } from "node:fs";

// Counts derive from the reviewed dataset so waves never silently desync the UI.
const data = JSON.parse(
  readFileSync(new URL("../../data/research.json", import.meta.url)),
);
const TOTAL = data.businesses.length;
const ACTIVE = data.businesses.filter(
  (b) => b.license?.status === "active",
).length;
const OUTER_ACTIVE = data.businesses.filter(
  (b) => b.area === "outer" && b.license?.status === "active",
).length;
const REVIEWS = data.reviews.length;
const SHORTLIST = data.businesses.filter((b) => b.priority).length;
const THUMBTACK = data.reviews.filter((r) => r.platform === "Thumbtack").length;
const COST_CAUTION = data.reviews.filter(
  (r) => r.platform === "Thumbtack" && r.theme === "Cost caution",
).length;
const FLAGS = data.businesses.reduce((n, b) => n + b.flags.length, 0);

// Ancestor-based clipping heuristics are unreliable here: .candidate, .hero and
// .panel all use overflow:hidden, and zero-width absolutely positioned boxes can
// widen the scroll area without a usable rect. So find the culprit empirically -
// hide a subtree, re-measure documentElement.scrollWidth, and descend into
// whichever subtree actually changes it.
const overflowProbe = (page) =>
  page.evaluate(() => {
    const wide = () => document.documentElement.scrollWidth;
    const base = wide();
    const limit = document.documentElement.clientWidth;
    if (base <= window.innerWidth)
      return { base, limit, innerWidth: window.innerWidth, path: [] };
    const path = [];
    let nodes = [...document.body.children];
    for (let depth = 0; depth < 12 && nodes.length; depth++) {
      const next = [];
      for (const n of nodes) {
        const prev = n.style.display;
        n.style.display = "none";
        const after = wide();
        n.style.display = prev;
        if (after < base) {
          const r = n.getBoundingClientRect();
          path.push(
            `d${depth} <${n.tagName.toLowerCase()}${n.id ? `#${n.id}` : ""} class="${
              typeof n.className === "string" ? n.className : ""
            }"> hiding=>${after} rect=${Math.round(r.left)}..${Math.round(
              r.right,
            )}x${Math.round(r.width)} pos=${getComputedStyle(n).position} :: ${
              (n.textContent || "").trim().replace(/\s+/g, " ").slice(0, 45)
            }`,
          );
          next.push(...n.children);
        }
      }
      if (!next.length) break;
      nodes = next;
    }
    return { base, limit, innerWidth: window.innerWidth, path };
  });

test("summary renders evidence-based shortlist with no browser errors", async ({
  page,
}) => {
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: "Find the right expertise." }),
  ).toBeVisible();
  await expect(page.locator(".candidate")).toHaveCount(SHORTLIST);
  await expect(page.locator(".stat-value").nth(0)).toContainText(String(TOTAL));
  await expect(page.locator(".stat-value").nth(1)).toContainText(String(ACTIVE));
  await expect(page.locator(".stat-value").nth(3)).toContainText("0");
  await page.locator('[data-detail="fast-response"]').first().click();
  await expect(page.getByRole("dialog")).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "Claim-by-claim evidence" }),
  ).toBeVisible();
  await expect(page.getByRole("dialog")).toContainText(
    "replaced the internal mechanism for a bathtub drain",
  );
  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).not.toBeVisible();
  expect(errors).toEqual([]);
});
test("summary surfaces both shortlist tiers and the official permit panel", async ({
  page,
}) => {
  await page.goto("/");
  await expect(page.locator(".candidate")).toHaveCount(SHORTLIST);
  await expect(
    page.getByRole("heading", {
      name: "Credential additions from the latest pass",
    }),
  ).toBeVisible();
  await expect(
    page.getByRole("heading", {
      name: /Permits and inspections are part of this scope/,
    }),
  ).toBeVisible();
  await expect(page.locator(".compliance-facts li")).toHaveCount(
    data.compliance.facts.length,
  );
  // Derive the link assertions from the dataset so the spec cannot drift from
  // the labels the compliance block actually carries.
  expect(data.compliance.officialLinks.length).toBeGreaterThan(2);
  for (const l of data.compliance.officialLinks) {
    expect(l.url).toMatch(/^https:\/\/(www\.)?(sf\.gov|dbiweb02\.sfgov\.org)\//);
    // Scoped to the action row: the inline [S175] citation points at the same
    // official URL, so an unscoped selector hits strict-mode.
    await expect(
      page.locator(`.compliance .dialog-actions a[href="${l.url}"]`),
    ).toBeVisible();
  }
  await expect(page.locator(".compliance .notice")).toHaveCount(
    data.compliance.notRetrieved.length,
  );
  await expect(page.locator("#snapshot-date")).toContainText("2026");
});
test("audit page shows the verification ladder with correct tier counts", async ({
  page,
}) => {
  await page.goto("/#audit");
  await expect(
    page.getByRole("heading", { name: "Verification ladder" }),
  ).toBeVisible();
  const ladder = page.locator(".table-wrap table").nth(0).locator("tbody tr");
  await expect(ladder).toHaveCount(3);
  await expect(ladder.nth(0).locator("td").nth(2)).toHaveText(
    String(data.businesses.filter((b) => b.license).length),
  );
  await expect(
    page.getByRole("heading", { name: "CSLB credential checks" }),
  ).toBeVisible();
  await expect(
    page.locator(".table-wrap table").nth(1).locator("tbody tr"),
  ).toHaveCount(data.businesses.filter((b) => b.license).length);
});
test("directory searches, filters, resets and exports source-linked CSV", async ({
  page,
}) => {
  await page.goto("/#directory");
  await expect(page.locator("tbody tr")).toHaveCount(TOTAL);
  await page
    .getByRole("searchbox", { name: "Search businesses" })
    .fill("fast response");
  await expect(page.locator("tbody tr")).toHaveCount(1);
  const downloadPromise = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export visible CSV" }).click();
  const download = await downloadPromise;
  expect(download.suggestedFilename()).toBe("sunset-repair-candidates.csv");
  await page.getByRole("searchbox", { name: "Search businesses" }).fill("");
  await page
    .getByRole("button", { name: "Qualified master", exact: true })
    .click();
  await expect(
    page.getByRole("heading", {
      name: "No businesses have passed every gate.",
    }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Show all candidates" }).click();
  await page.getByLabel("Active license checked only").check();
  await expect(page.locator("tbody tr")).toHaveCount(ACTIVE);
  await page.getByLabel("Filter by service area").selectOption("outer");
  await expect(page.locator("tbody tr")).toHaveCount(OUTER_ACTIVE);
});
test("comparison is bounded at 3 and opens a working dialog", async ({
  page,
}) => {
  await page.goto("/#directory");
  for (const id of ["fast-response", "genteel", "heises"])
    await page.locator(`[data-compare="${id}"]`).check();
  await page.locator('[data-compare="works"]').click();
  await expect(page.locator('[data-compare="works"]')).not.toBeChecked();
  await expect(
    page.getByRole("status").filter({ hasText: "Compare up to three" }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Compare evidence" }).click();
  await expect(
    page.getByRole("heading", { name: "Compare candidates" }),
  ).toBeVisible();
  await expect(page.locator(".compare-grid .panel")).toHaveCount(3);
  await page.keyboard.press("Escape");
  await page.getByRole("button", { name: "Clear", exact: true }).click();
  await expect(page.locator("#compare-bar")).not.toBeVisible();
});
test("review filters, flags and method routes work", async ({ page }) => {
  await page.goto("/#reviews");
  await expect(page.locator(".review-card")).toHaveCount(REVIEWS);
  await page.getByLabel("Filter review platform").selectOption("Thumbtack");
  await expect(page.locator(".review-card")).toHaveCount(THUMBTACK);
  await page.getByLabel("Filter review theme").selectOption("Cost caution");
  await expect(page.locator(".review-card")).toHaveCount(COST_CAUTION);
  await page.getByRole("link", { name: "Verification & flags" }).click();
  await expect(page.locator(".flag-item")).toHaveCount(FLAGS);
  await expect(
    page.getByRole("heading", { name: "CSLB credential checks" }),
  ).toBeVisible();
  await page.getByRole("link", { name: "Research method" }).click();
  await expect(
    page.getByRole("heading", { name: "Qualified master: strict admission" }),
  ).toBeVisible();
});
test("mobile navigation, layout and accessible modal work", async ({
  page,
}) => {
  test.setTimeout(90_000);
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: "Find the right expertise." }),
  ).toBeVisible();
  const summaryProbe = await overflowProbe(page);
  expect(
    summaryProbe.path,
    `summary overflow ${JSON.stringify(summaryProbe)}`,
  ).toEqual([]);
  await page.locator('[data-detail="fast-response"]').first().click();
  await expect(page.getByRole("dialog")).toBeVisible();
  await page.getByRole("button", { name: "Close details" }).click();
  await page.getByRole("link", { name: /Business directory/ }).click();
  await expect(page.locator("tbody tr")).toHaveCount(TOTAL);
  const directoryProbe = await overflowProbe(page);
  expect(
    directoryProbe.path,
    `directory overflow ${JSON.stringify(directoryProbe)}`,
  ).toEqual([]);
});
test("business deep links work and do not call external resources", async ({
  page,
}) => {
  const external = [];
  page.on("request", (req) => {
    if (!req.url().startsWith("http://127.0.0.1:4173"))
      external.push(req.url());
  });
  await page.goto("/#directory/fast-response");
  await expect(page.getByRole("dialog")).toBeVisible();
  expect(external).toEqual([]);
});

test("relative assets load correctly beneath the GitHub project path", async ({
  page,
}) => {
  await page.route("**/BathTubOverflowSF/**", async (route) => {
    const url = route.request().url().replace("/BathTubOverflowSF/", "/");
    const response = await route.fetch({ url });
    await route.fulfill({ response });
  });
  await page.goto("/BathTubOverflowSF/#directory");
  await expect(page.locator("tbody tr")).toHaveCount(TOTAL);
  await page.getByRole("link", { name: "Decision summary" }).click();
  await expect(page.locator(".candidate")).toHaveCount(SHORTLIST);
});

test("preview exposes public assets, not repository internals", async ({
  request,
}) => {
  for (const path of [
    "/.git/config",
    "/README.md",
    "/scripts/check_sources.py",
    "/node_modules/",
  ]) {
    const response = await request.get(path);
    expect(response.status()).toBe(404);
  }
  expect((await request.get("/data/research.json")).status()).toBe(200);
});
