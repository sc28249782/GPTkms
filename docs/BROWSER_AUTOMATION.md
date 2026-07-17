# Browser Automation

## Why include browser automation

Browser automation is useful for GPTkms when you want to:

- verify web-based KMS flows
- test MCP-connected UI workflows
- automate docs or demo checks
- later connect browser actions to Codex workflows

## Tooling choice

This repository uses Playwright with Chromium for the first browser automation layer.

## Install

If you want a repo-local setup:

```powershell
npm install
npm run browser:install
```

If you are using the bundled Codex runtime and do not have Node on PATH, use the local package manager/runtime available in your environment.

## Smoke test

Run:

```powershell
npm run browser:smoke
```

This opens a simple in-memory page and verifies that Playwright can launch Chromium successfully.

## Demo validation

Run:

```powershell
npm run browser:demo
```

This opens the local `demo/index.html` page, runs a simple search flow, and verifies that KMS-shaped results render in the browser.

If you are in a Codex runtime where `node` is not exposed on PATH, use:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_browser_smoke.ps1
```

## Why the smoke test uses a data URL

The smoke test does not depend on external network access. That keeps it stable and suitable for restricted or sandboxed environments.

## Near-term uses for GPTkms

- demoing browser-assisted KMS retrieval flows
- validating future plugin or app UIs
- regression checks for browser-dependent workflows

## Future direction

Likely next additions:

- browser-based demo scenario for GPTkms
- scripted validation of rendered docs or UI artifacts
- Codex workflow that uses browser automation plus KMS context together
