---
title: Promotion candidate memory pattern
type: concept
scope: project
status: candidate
tags:
  - promotion
  - memory
  - cross-project
sources:
  - raw/2026-07-17-bootstrap-note.md
last_reviewed: 2026-07-17
confidence: medium
---

Cross-project memory should not be written directly into the global base by default.

Instead, candidate knowledge should first be refined inside the project base, then
promoted with provenance once it is clearly reusable beyond the project.
