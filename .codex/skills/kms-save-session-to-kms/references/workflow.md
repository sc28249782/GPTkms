# KMS Save Session Workflow

## Goal

Turn a completed or meaningful work session into:

- one raw project source
- one or more durable project pages
- optional global promotions for reusable knowledge

## Recommended sequence

1. Summarize the session in plain language.
2. Save the summary into `sample_kms/projects/<project-id>/raw/`.
3. Identify which project pages should be created or updated.
4. Update `index.md` and `log.md` if needed.
5. Promote only reusable knowledge into `global/`.

## Helper script

Use:

```powershell
python scripts/save_session_to_kms.py --title "Session title" --content-file path\to\summary.md
```

This creates a raw session source under the active project KMS raw folder.

## Good promotion candidates

- reusable validation flows
- reliable browser automation patterns
- durable architecture decisions
- repeatable KMS maintenance workflows

