import { chromium } from "playwright";

const html = `
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>GPTkms Browser Smoke Test</title>
  </head>
  <body>
    <main>
      <h1 id="title">GPTkms Browser Smoke Test</h1>
      <p id="status">browser automation ready</p>
    </main>
  </body>
</html>
`;

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.goto(`data:text/html,${encodeURIComponent(html)}`);

const title = await page.locator("#title").textContent();
const status = await page.locator("#status").textContent();

console.log(
  JSON.stringify(
    {
      title,
      status,
      ok: title === "GPTkms Browser Smoke Test" && status === "browser automation ready",
    },
    null,
    2
  )
);

await browser.close();

