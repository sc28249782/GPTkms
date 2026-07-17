---
name: kms-promote-session-insights
description: Promote reusable project insights into the global GPTKMS knowledge base with provenance and restraint. Use when a session or project page has produced a stable pattern, workflow, preference, or architectural lesson that is likely to be reused across projects. Trigger for prompts like "save this for later", "promote to global memory", "make this reusable", or when Codex has just distilled a project-specific lesson that deserves durable cross-project memory.
---

# Kms Promote Session Insights

Use this skill to turn project-scoped learning into curated global memory.

Keep the promotion bar high. Most notes should stay local until they prove reusable.

Read [references/promotion-guide.md](references/promotion-guide.md) when you need the full decision checklist or promotion template.

## Workflow

1. Identify the candidate page in project scope.
2. Confirm that it is reusable beyond the current repo.
3. Run `kms_find_conflicts` if a similar global concept may already exist.
4. Promote with `kms_promote_candidate`.
5. Use a target page path and title that match the global taxonomy.
6. Add a short promotion note that explains why the insight is globally reusable.

## Promote only when true

- The page captures a reusable pattern, not just a one-off project detail.
- The lesson is understandable without the original chat transcript.
- The page has enough provenance to trust later.
- The title and tags will make sense to a future project.

## Do not promote when false

- The insight only matters to one client or repo.
- The page is still exploratory, contradictory, or weakly sourced.
- The same concept already exists globally and only needs a small update.

## Preferred output

- State the source project page.
- State the chosen global target page.
- State why the insight cleared the promotion bar.
- Include any conflict check result if one was needed.
