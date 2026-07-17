# KMS Answer Workflow

## Use this skill for

- architecture questions already covered by the KMS
- project conventions and prior decisions
- "what do we already know?" prompts
- reuse of structured knowledge across turns

## Retrieval sequence

1. Start with `kms_build_context_pack` using a compact query.
2. If the pack is too thin, broaden with `kms_search`.
3. Read the strongest candidate pages with `kms_read_page`.
4. If the answer still looks incomplete, inspect raw notes only as a fallback.
5. If the KMS looks inconsistent, run `kms_find_conflicts`.

## Answer shape

- lead with the answer
- mention whether the source is project, global, or both
- include 1-3 concrete page citations
- mention uncertainty if the KMS appears stale, conflicting, or sparse

## Avoid

- answering from memory alone when the KMS should be checked
- promoting or rewriting pages in the same step unless the user asked for maintenance too
- citing raw notes as primary evidence when a compiled page already exists
