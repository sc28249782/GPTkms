---
title: Browser automation integration
type: concept
scope: project
status: active
tags:
  - browser
  - playwright
  - demo
sources:
  - raw/2026-07-17-work-history-summary.md
last_reviewed: 2026-07-17
confidence: high
---

GPTkms includes a repo-local browser automation layer based on Playwright and Chromium.

The current browser layer has two purposes:

- verify that browser automation is available in a reproducible way
- demonstrate KMS-shaped content in a browser-facing UI

Implementation pieces:

- `package.json` for Playwright dependency management
- `tests/browser-smoke.mjs` for a minimal runtime check
- `tests/demo-browser.mjs` for validating the demo flow
- `scripts/run_browser_smoke.ps1` for Codex environments without Node on PATH
- `demo/index.html` as a static demo interface

