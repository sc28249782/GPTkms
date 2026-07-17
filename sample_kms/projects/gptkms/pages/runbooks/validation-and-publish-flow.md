---
title: Validation and publish flow
type: runbook
scope: project
status: active
tags:
  - validation
  - publishing
  - workflow
sources:
  - raw/2026-07-17-work-history-summary.md
last_reviewed: 2026-07-17
confidence: high
---

Use this flow before publishing meaningful updates to GPTkms:

1. Run `scripts/validate_repo.py`.
2. Run `scripts/smoke_test.py`.
3. Run the browser smoke test.
4. Run the browser demo validation flow.
5. Review the Git status for unintended files.
6. Commit focused changes with a clear message.
7. Push to `main` only when the working tree is clean and the validations pass.

In Codex environments where Node is not on PATH, use `scripts/run_browser_smoke.ps1`.

