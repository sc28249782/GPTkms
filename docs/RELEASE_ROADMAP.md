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

- merge/update flow for existing global pages
- richer conflict detection
- better link normalization
- higher-quality context packing
- structured source ingestion templates

### v0.3.0

Packaging and distribution:

- plugin wrapper around MCP + skills
- friendlier install flow
- opinionated default KMS root bootstrap
- starter templates for new projects

### v0.4.0

Operational maturity:

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

Prove reuse across at least two different projects.

### Milestone C

Package the system as a plugin-oriented distribution.

### Milestone D

Lock the public API and publish the first stable release.

## Open questions

- Should the long-term install target be plugin-first or MCP-first?
- How should global page merging behave when a page already exists?
- What is the right default ranking logic for context packs across multiple bases?
- Should raw source ingestion support structured metadata schemas from the start?

