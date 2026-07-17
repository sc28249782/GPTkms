# GPTkms

GPTkms is a local-first Knowledge Management System for Codex and ChatGPT Work.

It follows a simple idea:

- keep durable knowledge in plain markdown
- expose that knowledge through an MCP server
- separate project memory from global memory
- use skills to teach retrieval and promotion workflows

The project is inspired by the LLM Wiki direction from Andrej Karpathy and the implementation ideas documented in thClaws.

## Why this exists

Most AI workflows forget too much and over-rely on raw conversation history.

GPTkms tries to solve that by treating long-term memory as a maintained knowledge base instead of a pile of transcripts. The goal is to make memory:

- inspectable
- editable
- portable
- cross-project
- compatible with Codex workflows

## Current status

This repository is an early working prototype.

Already implemented:

- file-backed markdown KMS layout
- MCP stdio server
- global and project scopes
- search, read, write, ingest, promotion, lint, and conflict tools
- two Codex workflow skills
- sample KMS content for testing

Still in progress:

- plugin packaging
- merge/update flow for existing global pages
- stronger conflict detection
- broader multi-project examples

## Core ideas

### 1. Markdown is the durable memory layer

Compiled knowledge lives in `pages/`.

Raw evidence lives in `raw/`.

This keeps memory readable by both humans and agents.

### 2. MCP is the runtime integration point

The MCP server gives Codex and ChatGPT a structured way to search, read, update, and promote memory.

### 3. Memory has scope

- `global/` is for reusable cross-project knowledge
- `projects/<project-id>/` is for repo-specific knowledge

### 4. Promotion should be curated

Project knowledge should not automatically become global knowledge.

## Repository layout

```text
.
├── .codex/
│   ├── kms.json
│   └── skills/
├── .github/
│   └── workflows/
├── docs/
├── sample_kms/
├── scripts/
└── src/
```

## Included components

- [docs/kms-schema-and-mcp-spec.md](E:\My Projects\GPTkms\docs\kms-schema-and-mcp-spec.md): implementation-oriented schema and tool contract
- [docs/INSTALLATION.md](E:\My Projects\GPTkms\docs\INSTALLATION.md): installation and local run guide
- [docs/ORIGIN_AND_DIRECTION.md](E:\My Projects\GPTkms\docs\ORIGIN_AND_DIRECTION.md): project background and design direction
- [docs/PUBLISHING_CHECKLIST.md](E:\My Projects\GPTkms\docs\PUBLISHING_CHECKLIST.md): final steps for creating the GitHub repo and publishing
- [docs/RELEASE_ROADMAP.md](E:\My Projects\GPTkms\docs\RELEASE_ROADMAP.md): proposed release path
- [sample_kms](E:\My Projects\GPTkms\sample_kms): sample knowledge base for smoke tests
- [src/gptkms_mcp/server.py](E:\My Projects\GPTkms\src\gptkms_mcp\server.py): MCP protocol and tool dispatch
- [src/gptkms_mcp/kms_store.py](E:\My Projects\GPTkms\src\gptkms_mcp\kms_store.py): file-backed storage and quality checks
- [.codex/skills/kms-answer-from-wiki](E:\My Projects\GPTkms\.codex\skills\kms-answer-from-wiki): retrieval-first workflow skill
- [.codex/skills/kms-promote-session-insights](E:\My Projects\GPTkms\.codex\skills\kms-promote-session-insights): promotion workflow skill

## Implemented MCP tools

- `kms_list_bases`
- `kms_get_active_context`
- `kms_search`
- `kms_read_page`
- `kms_create_page`
- `kms_update_page`
- `kms_append_log`
- `kms_ingest_source`
- `kms_promote_candidate`
- `kms_build_context_pack`
- `kms_lint_links`
- `kms_find_conflicts`

## Quick start

Use the bundled Codex Python runtime:

```powershell
& 'C:\Users\sc282\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  'E:\My Projects\GPTkms\scripts\smoke_test.py'
```

Then run the MCP server:

```powershell
& 'C:\Users\sc282\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  'E:\My Projects\GPTkms\scripts\run_server.py'
```

For a fuller setup guide, see [docs/INSTALLATION.md](E:\My Projects\GPTkms\docs\INSTALLATION.md).

## Example Codex MCP config

```toml
[mcp_servers.gptkms]
command = "python"
args = ["E:\\My Projects\\GPTkms\\scripts\\run_server.py"]

[mcp_servers.gptkms.env]
GPTKMS_ROOT = "E:\\My Projects\\GPTkms\\sample_kms"
GPTKMS_PROJECT_DIR = "E:\\My Projects\\GPTkms"
```

## Validation

Useful local checks:

```powershell
python -m py_compile src/gptkms_mcp/server.py src/gptkms_mcp/kms_store.py scripts/smoke_test.py
python scripts/smoke_test.py
python scripts/validate_repo.py
```

## Roadmap

Short version:

- improve merge/update workflows for global pages
- package the MCP server and skills as a reusable plugin
- test against more than one real project
- stabilize the public tool contract

For the fuller release plan, see [docs/RELEASE_ROADMAP.md](E:\My Projects\GPTkms\docs\RELEASE_ROADMAP.md).

## Contributing

See [CONTRIBUTING.md](E:\My Projects\GPTkms\CONTRIBUTING.md).

## License

[MIT](E:\My Projects\GPTkms\LICENSE)
