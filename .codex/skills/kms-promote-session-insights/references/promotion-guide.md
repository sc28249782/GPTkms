# KMS Promotion Guide

## Promotion bar

Promote only when the candidate is:

- reusable across more than one project
- understandable without chat-only context
- specific enough to help later
- backed by a project page rather than only a raw transcript

## Recommended sequence

1. Find the project page that contains the distilled insight.
2. Check whether a similar global page already exists.
3. Run `kms_find_conflicts` if overlap is plausible.
4. Choose a stable global page path and clear title.
5. Promote with `kms_promote_candidate`.
6. Add a concise note explaining why the insight is globally reusable now.

## Good promotion targets

- retry or error-handling patterns
- reusable architecture decisions
- stable tool usage patterns
- user-level working preferences

## Bad promotion targets

- one-off bug details
- client-specific facts
- temporary rollout notes
- pages that still contain unresolved contradictions
