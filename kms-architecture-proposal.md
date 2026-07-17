# KMS Architecture Proposal for Codex / ChatGPT Work

## Goal

Build a long-term memory and knowledge management system for ChatGPT Work / Codex that:

- follows the LLM Wiki pattern
- works across multiple projects
- stays readable and editable as plain files
- can be used from Codex desktop, Codex CLI, and ChatGPT Work where possible

## Recommendation

Use a hybrid architecture:

1. `MCP server` as the core runtime for knowledge access and mutation
2. `plugin` as the distribution and UX layer for Work mode / desktop installation
3. `local markdown wiki` as the source of truth

Short version:

- If you want portable, cross-project memory with first-class tool access, choose `MCP server`.
- If you want easy installation, workspace sharing, and optional connectors/UI, wrap that MCP server in a `plugin`.
- Do not make the plugin the only source of truth. Keep the wiki on disk.

## Why this is the right split

### Why MCP should be the core

MCP is the right place for KMS logic because it is where Codex and ChatGPT consume tools and external context.

That lets us expose operations like:

- `kms_list_bases`
- `kms_attach_project`
- `kms_search`
- `kms_read_page`
- `kms_write_page`
- `kms_append_note`
- `kms_ingest_source`
- `kms_lint`
- `kms_promote_fact`
- `kms_query_memory`

This maps well to a living wiki model where the agent updates compiled knowledge over time instead of re-retrieving raw context every turn.

### Why plugin should not be the core

A plugin is best treated as packaging:

- installable in supported ChatGPT/Codex surfaces
- can bundle skills
- can bundle connectors
- can bundle MCP servers

That makes plugins excellent for adoption and reuse, but not ideal as the deepest storage/runtime abstraction for knowledge itself.

### Why files should remain the source of truth

The Karpathy-style approach works best when the durable artifact is plain markdown that both humans and agents can inspect.

Keep these properties:

- git-friendly
- grep-friendly
- no mandatory vector DB
- easy backup/export
- easy cross-linking
- easy manual correction

## Proposed architecture

### Layer 1: Storage

Use a file-backed wiki with two scopes:

- global/user scope
- project scope

Suggested layout:

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
  projects/
    <project-slug>/
      index.md
      log.md
      pages/
      raw/
      inbox/
      snapshots/
  links/
    project-map.json
    aliases.json
```

Suggested Windows-friendly default:

```text
%USERPROFILE%\.gptkms\
```

Inside each repo, optionally keep a thin local attachment file:

```text
.codex/kms.json
```

Example:

```json
{
  "project_id": "billing-api",
  "attached_bases": [
    "global",
    "projects/billing-api"
  ],
  "write_policy": {
    "global": "curated",
    "project": "auto"
  }
}
```

### Layer 2: Knowledge model

Follow the LLM Wiki pattern with three logical zones:

1. `raw/` for immutable source material
2. `pages/` for compiled wiki pages
3. `schema/instructions` for how the agent should ingest, query, and maintain the wiki

Each base should have:

- `index.md` for table of contents
- `log.md` for chronological changes
- `pages/` for stable knowledge pages
- `raw/` for imported evidence
- `inbox/` for uncategorized captures

### Layer 3: MCP server

The MCP server should own:

- base discovery
- project attachment
- search/read/write tools
- source ingestion
- maintenance workflows
- access policy
- conflict handling

Suggested tool surface:

```text
kms_list_bases
kms_get_active_context
kms_attach_base
kms_detach_base
kms_search
kms_read_page
kms_read_raw
kms_create_page
kms_update_page
kms_append_log
kms_ingest_source
kms_extract_candidates
kms_promote_candidate
kms_lint_links
kms_find_conflicts
kms_build_context_pack
```

Useful MCP server behavior:

- rank project-local pages first, then global pages
- return compact summaries first and expand on demand
- include citations to page paths and headings
- separate "raw evidence" from "compiled knowledge"
- require stronger confirmation before writing to global memory

### Layer 4: Skills

Use skills for workflows, not storage.

Examples:

- `kms-ingest-source`
- `kms-answer-from-wiki`
- `kms-promote-session-insights`
- `kms-project-bootstrap`
- `kms-weekly-lint`

The skill tells Codex when and how to use the MCP tools.

### Layer 5: Plugin

Wrap the skills plus optional MCP config in a plugin when you want:

- one-click-ish installation
- workspace sharing
- discoverability in supported surfaces
- optional future connectors or app UI

The plugin can bundle:

- skills
- MCP server definition
- optional hooks
- optional connector/app pieces later

## Cross-project design

This is the main requirement, so make it explicit.

### Use two memory scopes

#### 1. Global memory

For durable facts that should survive beyond one repo:

- user preferences
- tool setup knowledge
- recurring troubleshooting patterns
- architecture patterns
- reusable research summaries
- vendor notes

#### 2. Project memory

For repo- or client-specific facts:

- domain model notes
- architecture decisions
- deployment quirks
- glossaries
- runbooks
- meeting summaries

### Promotion policy

Not every project note should become global memory.

Use a promotion rule:

- project note starts local
- only promote to global if reused across 2+ projects or clearly user-level

This prevents global memory from becoming noisy.

### Attach model

When Codex opens a repo:

1. read `.codex/kms.json` if present
2. attach the project base
3. also attach selected global bases
4. optionally attach topical shared bases like `product`, `ops`, or `research`

That gives cross-project reuse without losing project boundaries.

## Suggested write policies

Use different write strictness by scope:

- `project base`: allow semi-automatic writes
- `global base`: require curation, approval, or promotion workflow

Suggested modes:

- `auto`: safe append/update in project wiki
- `review`: write draft page or candidate facts first
- `manual`: only write when explicitly requested

## Minimal viable implementation

### Phase 1

Build only these:

- file-backed wiki layout
- MCP server
- search/read/write tools
- one project attachment file
- one skill for "answer from wiki"
- one skill for "ingest source into wiki"

Do not start with:

- embeddings
- vector DB
- graph DB
- custom UI
- aggressive auto-writing to global memory

### Phase 2

Add:

- promotion workflow from project to global
- lint/conflict detection
- session-to-memory summarization
- better ranking and context packing

### Phase 3

Optionally add:

- plugin packaging
- connectors to Drive/Notion/Slack/GitHub
- app UI for browsing knowledge
- scheduled maintenance jobs

## Answer to plugin vs MCP

If forced to choose only one:

- choose `MCP server`

Because:

- it is the true runtime integration point for tools and context
- it works naturally with Codex desktop and CLI
- it maps directly to cross-project knowledge operations
- it keeps storage and behavior under your control

Use `plugin` when:

- you want easier install/distribution
- you want ChatGPT Work users to discover and enable it more easily
- you want to bundle skills and optional connectors around the same KMS

Best practical answer:

- `MCP-first, plugin-second`

## Concrete build plan

1. Create a local file-backed KMS root outside any single repo
2. Define the markdown schema and page taxonomy
3. Implement an MCP server over that file store
4. Add project attachment config in each repo
5. Add 2-3 skills that teach Codex how to query and maintain the KMS
6. Test with two unrelated projects
7. Only then package it as a plugin

## Good defaults

### File conventions

- markdown only for durable pages
- YAML frontmatter for metadata
- stable page IDs or slugs
- explicit `sources:` and `last_reviewed:` fields

Example frontmatter:

```yaml
---
title: Retry pattern for flaky MCP calls
type: concept
scope: global
sources:
  - projects/billing-api/raw/session-2026-07-17.md
last_reviewed: 2026-07-17
confidence: medium
tags:
  - mcp
  - reliability
---
```

### Retrieval conventions

- search index and titles first
- then narrow to candidate pages
- then read only relevant sections
- prefer compiled pages over raw notes
- fall back to raw evidence when confidence is low

### Maintenance conventions

- every write updates `log.md`
- keep raw sources immutable
- allow page rewrites, but preserve provenance
- add a lint pass for broken links, duplicate pages, and unsupported claims

## Risks to avoid

### 1. Treating chat transcripts as memory directly

Transcript archives are not the memory layer. They are raw material.

### 2. Writing everything into one giant global wiki

This causes noise and lowers trust quickly.

### 3. Letting the model rewrite raw evidence

Raw sources should stay immutable.

### 4. Starting with embeddings-first architecture

For this use case, compiled markdown memory is the higher-leverage first step.

### 5. No promotion gate

Without a gate, "cross-project memory" becomes accidental contamination.

## Final recommendation

Build the system as:

- `local markdown wiki` for durable knowledge
- `MCP server` for access and mutation
- `skills` for repeatable workflows
- `plugin` for packaging and wider reuse

In one sentence:

Use a Karpathy-style file-based wiki as the memory, expose it through an MCP server, and package it as a plugin only after the core knowledge workflow is stable.
