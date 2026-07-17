# Installation Guide

## Requirements

- Python 3.12+
- Git
- A Codex environment if you want to use the bundled skills directly

## Option 1: Run with the bundled Codex Python

```powershell
& 'C:\Users\sc282\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  'E:\My Projects\GPTkms\scripts\run_server.py'
```

## Option 2: Run with your own Python

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python scripts/smoke_test.py
python scripts/run_server.py
```

## Optional environment variables

- `GPTKMS_ROOT`
- `GPTKMS_PROJECT_DIR`

If omitted, the prototype uses:

- `sample_kms` as the KMS root
- the current repository as the active project directory

## Codex MCP example

```toml
[mcp_servers.gptkms]
command = "python"
args = ["E:\\My Projects\\GPTkms\\scripts\\run_server.py"]

[mcp_servers.gptkms.env]
GPTKMS_ROOT = "E:\\My Projects\\GPTkms\\sample_kms"
GPTKMS_PROJECT_DIR = "E:\\My Projects\\GPTkms"
```

## Skill validation

If you want to validate the included skills:

```powershell
python -m pip install PyYAML
python scripts/validate_repo.py
```
