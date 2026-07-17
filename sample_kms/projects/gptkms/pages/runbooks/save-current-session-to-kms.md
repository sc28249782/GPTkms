---
title: Save current session to KMS
type: runbook
scope: project
status: active
tags:
  - session
  - memory
  - workflow
sources:
  - raw/2026-07-17-work-history-summary.md
last_reviewed: 2026-07-17
confidence: high
---

Use this flow when you want to preserve the current working session into GPTkms:

1. Write a raw session summary into `raw/`.
2. Create or update the project pages that represent the durable knowledge from that session.
3. Update the project log and index if new durable pages were added.
4. Promote only the reusable parts into global memory.

The helper script `scripts/save_session_to_kms.py` can create the raw source file quickly from a title and a content file.

