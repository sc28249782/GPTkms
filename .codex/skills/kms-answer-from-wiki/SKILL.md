---
name: kms-answer-from-wiki
description: Answer questions from the local GPTKMS knowledge base before falling back to raw notes or general reasoning. Use when Codex needs to explain project conventions, architecture decisions, reusable patterns, prior findings, or any repo-specific knowledge that may already exist in the KMS. Trigger especially for prompts about "what do we already know", "search memory", "answer from wiki", "use the KMS", or when a future turn should reuse prior structured knowledge instead of rediscovering it.
---

# Kms Answer From Wiki

Use the KMS as the first retrieval layer for repo and cross-project knowledge.

Prefer compiled pages under `pages/` over raw notes under `raw/`. Use raw notes only when the compiled pages are missing, thin, or contradicted.

Read [references/workflow.md](references/workflow.md) when you need the detailed retrieval sequence or answer shape.

## Workflow

1. Call `kms_get_active_context` if the active bases or write policies are unclear.
2. Call `kms_build_context_pack` with a short query that matches the user's actual need.
3. If the pack is empty or weak, call `kms_search` with a broader query.
4. Read the most relevant page or pages with `kms_read_page`.
5. Answer from the compiled pages first and cite the page paths.
6. If the KMS looks stale or incomplete, say so clearly and only then fall back to raw notes or general reasoning.

## Rules

- Start with `kms_build_context_pack` unless the user already gave an exact `base_id` and `page_path`.
- Prefer project pages over global pages when both speak to the same question.
- Treat duplicate-title or broken-link findings as signals that the answer may need caution.
- Keep answers compact: summary first, then the most relevant citations.
- Do not write new memory just because the KMS was useful; writing belongs to separate maintenance workflows.

## Answer shape

- One short answer paragraph or list.
- Mention whether the answer came from project scope, global scope, or both.
- Include concrete citations like `projects/gptkms/pages/decisions/prototype-scope.md`.

## When to escalate

If the KMS returns conflicting pages, run `kms_find_conflicts` and explain the uncertainty instead of pretending the memory is settled.
