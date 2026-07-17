import { chromium } from "playwright";
import { pathToFileURL } from "node:url";
import path from "node:path";

const demoPath = path.resolve("demo/index.html");
const demoUrl = pathToFileURL(demoPath).href;

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.goto(demoUrl);

await page.locator("#query").fill("promotion");

const resultCount = await page.locator(".card").count();
const firstTitle = await page.locator(".card .title").first().textContent();
const summary = await page.locator("#summary").textContent();

console.log(
  JSON.stringify(
    {
      resultCount,
      firstTitle,
      summary,
      ok:
        resultCount >= 2 &&
        summary?.includes('Query: "promotion"') &&
        firstTitle?.length > 0,
    },
    null,
    2
  )
);

await browser.close();

