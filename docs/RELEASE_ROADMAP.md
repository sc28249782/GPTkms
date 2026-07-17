# Release Roadmap

## Vision

Turn GPTkms from a prototype into a reusable, cross-project memory layer for Codex and ChatGPT Work.

## Release phases

### v0.1.0

Prototype foundation:

- file-backed markdown KMS
- MCP stdio server
- project/global scope split
- retrieval, promotion, lint, and conflict tools
- first workflow skills

### v0.2.0

Memory maintenance:

- generated JSON build from `sample_kms` for the demo layer
- auto-distill session -> update pages -> optional promote workflow
- merge/update flow for existing global pages
- richer conflict detection
- better link normalization
- higher-quality context packing
- structured source ingestion templates

### v0.3.0

Packaging and distribution:

- plugin wrapper around MCP + skills
- demo and install flow bundled with the plugin-oriented wrapper
- friendlier install flow
- opinionated default KMS root bootstrap
- starter templates for new projects

### v0.4.0

Operational maturity:

- Obsidian integration for second-brain workflows, with GPTkms managing an agent-memory subfolder or a synchronized curated layer
- import/export flow between GPTkms and Obsidian vault structures
- optional Obsidian URI helpers for creating, opening, or appending curated notes
- CI validation matrix
- regression fixtures for search and promotion
- release notes and changelog discipline
- example demos across multiple projects

### v1.0.0

Stable public release:

- stable tool contracts
- documented migration path
- clear compatibility expectations
- tested onboarding flow for new users

## Suggested milestones

### Milestone A

Ship the public prototype repo with working docs and CI.

### Milestone B

Prove reuse across at least two different projects and make session capture/promote workflows feel routine.

### Milestone C

Package the system as a plugin-oriented distribution with easier install and demo flows.

### Milestone D

Add second-brain integrations such as Obsidian without weakening the core KMS model.

### Milestone E

Lock the public API and publish the first stable release.

## Current priority order

1. Replace hardcoded demo content with generated JSON derived from `sample_kms`.
2. Automate the session flow: raw capture -> durable page updates -> optional promotion.
3. Add a plugin wrapper that bundles MCP, skills, and easier install/demo flows.
4. Add Obsidian integration as a second-brain layer on top of the stabilized KMS core.

## Open questions

- Should the long-term install target be plugin-first or MCP-first?
- How should global page merging behave when a page already exists?
- What is the right default ranking logic for context packs across multiple bases?
- Should raw source ingestion support structured metadata schemas from the start?
- Should Obsidian integration share one vault directly, or synchronize only curated GPTkms memory into a dedicated subfolder?
