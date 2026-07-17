# Contributing to GPTkms

Thanks for taking an interest in GPTkms.

## Project intent

GPTkms explores a practical, local-first Knowledge Management System for Codex and ChatGPT Work:

- markdown is the durable memory layer
- MCP is the runtime interface
- skills teach retrieval and promotion workflows
- global memory stays curated

## How to contribute

Useful contribution areas:

- retrieval quality
- conflict detection
- promotion workflows
- plugin packaging
- documentation and examples
- CI and release automation

## Development workflow

1. Fork the repository.
2. Create a short-lived feature branch.
3. Make focused changes.
4. Run the local checks.
5. Open a pull request with a clear explanation of what changed and why.

## Local checks

Use the bundled Python runtime from Codex or your own Python 3.12+ environment.

Recommended checks:

```powershell
python -m py_compile src/gptkms_mcp/server.py src/gptkms_mcp/kms_store.py scripts/smoke_test.py scripts/validate_repo.py
python scripts/smoke_test.py
python scripts/validate_repo.py
```

## Style

- Keep storage human-readable.
- Prefer simple file-backed logic over premature infrastructure.
- Preserve provenance when knowledge moves from project to global scope.
- Keep docs practical and implementation-oriented.

## Pull request guidance

A strong PR should include:

- the problem being solved
- the design tradeoff
- how it was validated
- any limitations or follow-up work
