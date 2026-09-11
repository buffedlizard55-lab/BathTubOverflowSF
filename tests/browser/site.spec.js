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

// Instead of a bare boolean, report the elements that actually overflow the
// viewport so a layout regression names its own cause in the CI log. Elements
// inside a scroll container (the mobile nav rail, .table-wrap) are off-screen
// but do NOT widen the page, so they are reported separately as clipped.
const overflowReport = (page) =>
  page.evaluate(() => {
    const limit = document.documentElement.clientWidth;
    const clipped = (el) => {
      for (let n = el.parentElement; n; n = n.parentElement)
        if (getComputedStyle(n).overflowX !== "visible") return true;
      return false;
    };
    const describe = (el, r) =>
      `<${el.tagName.toLowerCase()} class="${
        typeof el.className === "string" ? el.className : ""
      }" pos=${getComputedStyle(el).position}> right=${Math.round(
        r.right,
      )} w=${Math.round(r.width)} :: ${
        (el.textContent || "").trim().replace(/\s+/g, " ").slice(0, 40)
      }`;
    const rows = [...document.querySelectorAll("body *")]
      .map((el) => ({ el, r: el.getBoundingClientRect() }))
      .filter(({ r }) => r.right > limit + 0.5 && r.width > 0);
    return {
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: limit,
      innerWidth: window.innerWidth,
      bodyScrollWidth: document.body.scrollWidth,
      page: rows.filter(({ el }) => !clipped(el)).slice(0, 10).map(({ el, r }) => describe(el, r)),
      clipped: rows.filter(({ el }) => clipped(el)).length,
    };
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
  await expect(
    page.getByRole("link", { name: /Apply for a plumbing or mechanical permit/ }),
  ).toBeVisible();
  await expect(page.getByRole("link", { name: /SF DBI Permit Services/ })).toBeVisible();
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
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: "Find the right expertise." }),
  ).toBeVisible();
  const overflow = await overflowReport(page);
  console.log(`MOBILE LAYOUT ${globalThis.location?.hash || ""} ${JSON.stringify(overflow)}`);
  expect(overflow.page).toEqual([]);
  expect(overflow.scrollWidth).toBeLessThanOrEqual(overflow.innerWidth);
  await page.locator('[data-detail="fast-response"]').first().click();
  await expect(page.getByRole("dialog")).toBeVisible();
  await page.getByRole("button", { name: "Close details" }).click();
  await page.getByRole("link", { name: /Business directory/ }).click();
  await expect(page.locator("tbody tr")).toHaveCount(TOTAL);
  const overflow = await overflowReport(page);
  console.log(`MOBILE LAYOUT ${globalThis.location?.hash || ""} ${JSON.stringify(overflow)}`);
  expect(overflow.page).toEqual([]);
  expect(overflow.scrollWidth).toBeLessThanOrEqual(overflow.innerWidth);
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
