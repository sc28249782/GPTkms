---
title: Browser automation smoke-test pattern
type: concept
scope: global
status: active
tags:
  - browser
  - playwright
  - validation
  - codex
sources:
  - projects/gptkms/pages/concepts/browser-automation-integration.md
last_reviewed: 2026-07-17
confidence: high
promoted_from: projects/gptkms:concepts/browser-automation-integration.md
---

When adding browser automation to a Codex-oriented repository, start with two levels of validation:

1. a minimal browser smoke test that verifies Playwright and Chromium can launch
2. a focused browser flow test that verifies one meaningful UI scenario

This keeps browser automation reproducible without requiring a full external environment on day one.

In constrained Codex environments, it also helps to provide a helper script that runs the browser test with a bundled Node runtime when `node` is not on PATH.

