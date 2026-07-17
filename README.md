# GPTkms

GPTkms is a local-first Knowledge Management System for Codex and ChatGPT Work.

It follows a simple idea:

- keep durable knowledge in plain markdown
- expose that knowledge through an MCP server
- separate project memory from global memory
- use skills to teach retrieval and promotion workflows

The project is inspired by the [LLM Wiki direction from Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and the implementation ideas documented in [thClaws](https://github.com/thClaws/thClaws).

## Why this exists

Most AI workflows forget too much and over-rely on raw conversation history.

GPTkms tries to solve that by treating long-term memory as a maintained knowledge base instead of a pile of transcripts. The goal is to make memory:

- inspectable
- editable
- portable
- cross-project
- compatible with Codex workflows

## Positioning

GPTkms sits between simple persistent-memory tools and full personal knowledge systems.

In practical terms:

- it is more structured and curated than a flat memory layer
- it is more operational and agent-facing than a second-brain app like Obsidian
- it is built from Codex-native primitives such as MCP and skills, rather than replacing them

For the longer comparison, see [docs/POSITIONING_AND_LANDSCAPE.md](docs/POSITIONING_AND_LANDSCAPE.md).

## Current status

This repository is an early working prototype.

Already implemented:

- file-backed markdown KMS layout
- MCP stdio server
- global and project scopes
- search, read, write, ingest, promotion, lint, and conflict tools
- two Codex workflow skills
- Playwright-based browser automation scaffold
- browser-facing KMS demo page
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

- [docs/kms-schema-and-mcp-spec.md](docs/kms-schema-and-mcp-spec.md): implementation-oriented schema and tool contract
- [docs/INSTALLATION.md](docs/INSTALLATION.md): installation and local run guide
- [docs/BROWSER_AUTOMATION.md](docs/BROWSER_AUTOMATION.md): Playwright and Chromium setup for repo-local browser automation
- [docs/ORIGIN_AND_DIRECTION.md](docs/ORIGIN_AND_DIRECTION.md): project background and design direction
- [docs/POSITIONING_AND_LANDSCAPE.md](docs/POSITIONING_AND_LANDSCAPE.md): how GPTkms differs from adjacent memory approaches
- [docs/PUBLISHING_CHECKLIST.md](docs/PUBLISHING_CHECKLIST.md): final steps for creating the GitHub repo and publishing
- [docs/RELEASE_ROADMAP.md](docs/RELEASE_ROADMAP.md): proposed release path
- [sample_kms](sample_kms): sample knowledge base for smoke tests
- [src/gptkms_mcp/server.py](src/gptkms_mcp/server.py): MCP protocol and tool dispatch
- [src/gptkms_mcp/kms_store.py](src/gptkms_mcp/kms_store.py): file-backed storage and quality checks
- [.codex/skills/kms-answer-from-wiki](.codex/skills/kms-answer-from-wiki): retrieval-first workflow skill
- [.codex/skills/kms-promote-session-insights](.codex/skills/kms-promote-session-insights): promotion workflow skill
- [.codex/skills/kms-save-session-to-kms](.codex/skills/kms-save-session-to-kms): workflow skill for preserving the current session into project KMS
- [demo/index.html](demo/index.html): static browser demo for KMS-shaped content
- [tests/browser-smoke.mjs](tests/browser-smoke.mjs): browser automation smoke test using Playwright

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

For a fuller setup guide, see [docs/INSTALLATION.md](docs/INSTALLATION.md).

## Browser automation

This repo now includes a small Playwright scaffold for browser automation.

Quick commands:

```powershell
npm install
npm run browser:install
npm run browser:smoke
npm run browser:demo
```

If `node` is not on PATH in Codex, use:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_browser_smoke.ps1
```

For details, see [docs/BROWSER_AUTOMATION.md](docs/BROWSER_AUTOMATION.md).

## Demo

The repository includes a small browser-facing demo at [demo/index.html](demo/index.html).

It shows:

- KMS-style entries with scope and citations
- client-side search over project and global memory
- a simple UI flow that Playwright can validate

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
npm run browser:smoke
npm run browser:demo
```

## Saving session knowledge

To preserve the current work into project memory:

1. save a raw session summary
2. update durable project pages
3. promote only reusable knowledge into global memory

You can use [scripts/save_session_to_kms.py](scripts/save_session_to_kms.py) to create the raw session source quickly.

In Codex environments without `node` on PATH, replace the last command with:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_browser_smoke.ps1
```

## Roadmap

Short version:

- improve merge/update workflows for global pages
- package the MCP server and skills as a reusable plugin
- test against more than one real project
- stabilize the public tool contract

For the fuller release plan, see [docs/RELEASE_ROADMAP.md](docs/RELEASE_ROADMAP.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
