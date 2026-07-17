# KMS Schema And MCP Tool Spec

## Design goals

- cross-project reuse
- local-first storage
- human-readable markdown
- explicit separation between raw evidence and compiled knowledge
- safe writes with stronger gates for global memory

## Storage model

```text
<kms-root>/
  global/
    index.md
    log.md
    pages/
      concepts/
      entities/
      workflows/
      people/
      tools/
    raw/
    inbox/
  projects/
    <project-id>/
      index.md
      log.md
      pages/
        concepts/
        decisions/
        runbooks/
        glossaries/
      raw/
      inbox/
      snapshots/
  links/
    project-map.json
    aliases.json
```

## Scope model

### Global scope

Use for:

- reusable patterns
- user-level preferences
- tool setup notes
- cross-project architecture notes

Write policy:

- default `review`
- promotion required from project memory or explicit user intent

### Project scope

Use for:

- project-specific decisions
- repo conventions
- domain notes
- meeting summaries
- operational runbooks

Write policy:

- default `auto`

## Project attachment file

Each repo can include `.codex/kms.json`.

Example:

```json
{
  "project_id": "gptkms",
  "attached_bases": [
    "global",
    "projects/gptkms"
  ],
  "write_policy": {
    "global": "review",
    "projects/gptkms": "auto"
  }
}
```

## Page schema

All durable pages are markdown with lightweight YAML frontmatter.

Example:

```yaml
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
  - raw/2026-07-17-session-summary.md
last_reviewed: 2026-07-17
confidence: medium
---
```

### Required frontmatter

- `title`
- `type`
- `scope`

### Recommended frontmatter

- `status`
- `tags`
- `sources`
- `last_reviewed`
- `confidence`

### Page types

- `concept`
- `entity`
- `workflow`
- `decision`
- `runbook`
- `glossary`
- `source-summary`

## Raw source schema

Raw sources are immutable markdown or text files stored under `raw/`.

Suggested filename:

```text
YYYY-MM-DD-short-slug.md
```

Suggested frontmatter:

```yaml
---
title: Session summary for initial KMS architecture discussion
source_type: session
captured_at: 2026-07-17
scope: project
---
```

## Write rules

### Allowed automatic writes

- append to `log.md`
- create project pages
- update existing project pages
- ingest raw sources

### Writes that should prefer review mode

- create or update global pages
- merge project insights into global knowledge
- rewrite page titles or canonical slugs

## Search and retrieval rules

1. Search attached bases only by default.
2. Rank project pages above global pages.
3. Prefer compiled `pages/` content over `raw/`.
4. Return compact summaries first.
5. Include file citations in every result.

## MCP server contract

The prototype uses the classic MCP JSON-RPC flow with:

- `initialize`
- `tools/list`
- `tools/call`

The server returns `instructions` during initialization so Codex can understand scope and safety rules.

## Tool catalog

### Implemented in the prototype

#### `kms_list_bases`

Purpose:

- list available bases under the KMS root

Input schema:

```json
{
  "type": "object",
  "properties": {},
  "additionalProperties": false
}
```

#### `kms_get_active_context`

Purpose:

- show the current project, attached bases, and write policies

Input schema:

```json
{
  "type": "object",
  "properties": {},
  "additionalProperties": false
}
```

#### `kms_search`

Purpose:

- search page titles and content across attached bases

Input schema:

```json
{
  "type": "object",
  "properties": {
    "query": { "type": "string" },
    "limit": { "type": "integer", "minimum": 1, "maximum": 50 },
    "base_ids": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": ["query"],
  "additionalProperties": false
}
```

#### `kms_read_page`

Purpose:

- read one page by base and relative page path

Input schema:

```json
{
  "type": "object",
  "properties": {
    "base_id": { "type": "string" },
    "page_path": { "type": "string" }
  },
  "required": ["base_id", "page_path"],
  "additionalProperties": false
}
```

#### `kms_create_page`

Purpose:

- create a new page under `pages/`

Input schema:

```json
{
  "type": "object",
  "properties": {
    "base_id": { "type": "string" },
    "page_path": { "type": "string" },
    "frontmatter": { "type": "object" },
    "body": { "type": "string" }
  },
  "required": ["base_id", "page_path", "frontmatter", "body"],
  "additionalProperties": false
}
```

#### `kms_update_page`

Purpose:

- overwrite an existing page under `pages/`

Input schema:

```json
{
  "type": "object",
  "properties": {
    "base_id": { "type": "string" },
    "page_path": { "type": "string" },
    "frontmatter": { "type": "object" },
    "body": { "type": "string" }
  },
  "required": ["base_id", "page_path", "frontmatter", "body"],
  "additionalProperties": false
}
```

#### `kms_append_log`

Purpose:

- append a dated bullet entry to a base log

Input schema:

```json
{
  "type": "object",
  "properties": {
    "base_id": { "type": "string" },
    "entry": { "type": "string" }
  },
  "required": ["base_id", "entry"],
  "additionalProperties": false
}
```

#### `kms_ingest_source`

Purpose:

- create a raw source file in a target base

Input schema:

```json
{
  "type": "object",
  "properties": {
    "base_id": { "type": "string" },
    "source_path": { "type": "string" },
    "title": { "type": "string" },
    "content": { "type": "string" }
  },
  "required": ["base_id", "source_path", "title", "content"],
  "additionalProperties": false
}
```

#### `kms_promote_candidate`

Purpose:

- promote stable project knowledge into global memory with provenance

Input schema:

```json
{
  "type": "object",
  "properties": {
    "source_base_id": { "type": "string" },
    "source_page_path": { "type": "string" },
    "target_page_path": { "type": "string" },
    "title": { "type": "string" },
    "additional_tags": {
      "type": "array",
      "items": { "type": "string" }
    },
    "note": { "type": "string" }
  },
  "required": ["source_base_id", "source_page_path", "target_page_path"],
  "additionalProperties": false
}
```

#### `kms_build_context_pack`

Purpose:

- produce a compact context bundle for agent use in future turns

Input schema:

```json
{
  "type": "object",
  "properties": {
    "query": { "type": "string" },
    "limit": { "type": "integer", "minimum": 1, "maximum": 20 },
    "base_ids": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": ["query"],
  "additionalProperties": false
}
```

Current behavior in the prototype:

- searches attached bases
- prefers project pages first
- returns compact page metadata plus citations
- includes a markdown summary block suitable for reuse in a future prompt

### Planned next tools

#### `kms_lint_links`

Purpose:

- find broken internal markdown links

Input schema:

```json
{
  "type": "object",
  "properties": {
    "base_ids": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "additionalProperties": false
}
```

#### `kms_find_conflicts`

Purpose:

- detect duplicate titles, duplicate bodies, and strongly overlapping pages

Input schema:

```json
{
  "type": "object",
  "properties": {
    "base_ids": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "additionalProperties": false
}
```

## Recommended implementation sequence

1. Run the current stdio prototype against the sample store.
2. Add a skill layer for retrieval and promotion workflows.
3. Move the KMS root outside the repo.
4. Package as a plugin only after the tool surface stabilizes.
