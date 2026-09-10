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
const THUMBTACK = data.reviews.filter((r) => r.platform === "Thumbtack").length;
const COST_CAUTION = data.reviews.filter(
  (r) => r.platform === "Thumbtack" && r.theme === "Cost caution",
).length;
const FLAGS = data.businesses.reduce((n, b) => n + b.flags.length, 0);
test("summary renders evidence-based shortlist with no browser errors", async ({
  page,
}) => {
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: "Find the right expertise." }),
  ).toBeVisible();
  await expect(page.locator(".candidate")).toHaveCount(5);
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
  await page.getByLabel("Active C-36 checked only").check();
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
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
  await page.locator('[data-detail="fast-response"]').first().click();
  await expect(page.getByRole("dialog")).toBeVisible();
  await page.getByRole("button", { name: "Close details" }).click();
  await page.getByRole("link", { name: /Business directory/ }).click();
  await expect(page.locator("tbody tr")).toHaveCount(TOTAL);
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
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
  await expect(page.locator(".candidate")).toHaveCount(5);
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
