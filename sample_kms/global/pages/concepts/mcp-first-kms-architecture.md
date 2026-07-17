---
title: MCP-first KMS architecture
type: concept
scope: global
status: draft
tags:
  - mcp
  - kms
  - architecture
sources:
  - raw/2026-07-17-kms-session-summary.md
last_reviewed: 2026-07-17
confidence: medium
---

Use MCP as the runtime integration layer for the KMS, not the plugin itself.

The durable knowledge should stay in markdown files. Plugins are valuable later for
distribution, discovery, and optional connectors, but they should not be the only
source of truth.
