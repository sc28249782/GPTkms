# Publishing Checklist

## Local state

As of 2026-07-17, the local repository is prepared with:

- initialized Git repository
- default branch `main`
- initial commit created

Current initial commit:

- `9f89933` `Initial GPTkms prototype`

## Create the GitHub repository

Create a new repository on GitHub:

- owner: `sc28249782`
- repository name: `GPTkms`
- visibility: public or private, depending on your preference

Suggested description:

`Local-first KMS for Codex and ChatGPT Work using markdown, MCP, and workflow skills.`

## Connect the local repo

```powershell
git remote add origin https://github.com/sc28249782/GPTkms.git
git push -u origin main
```

## First post-push checks

1. Open the repository page and confirm `README.md` renders correctly.
2. Check that `docs/` links are visible and useful.
3. Confirm GitHub Actions starts the CI workflow.
4. Confirm the sample KMS tree is included.
5. Confirm the `.codex/skills` folders are present.

## Suggested first release shape

Suggested first tag:

- `v0.1.0-alpha`

Suggested meaning:

- working prototype
- public for feedback
- not yet stable as a long-term public API

## Suggested release notes outline

### Highlights

- markdown-first KMS layout
- MCP stdio server
- project/global memory split
- retrieval and promotion workflows
- lint and conflict checks
- Codex skill examples

### Known limitations

- no plugin wrapper yet
- no global-page merge/update flow yet
- CI is still lightweight
- broader multi-project validation is still pending

## Next release targets

For `v0.2.0`:

- merge/update flow for existing global pages
- stronger overlap/conflict heuristics
- better context-pack ranking
- cleaner install/bootstrap flow

