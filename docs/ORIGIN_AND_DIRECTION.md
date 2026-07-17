# Origin And Direction

## Background

GPTkms started from a practical question:

How can Codex or ChatGPT Work keep useful long-term memory across projects without turning memory into an opaque black box?

The direction taken here is intentionally simple:

- keep memory on disk
- keep it readable
- keep it reviewable
- keep the runtime interface separate from the storage

## Influences

This project is inspired by:

- the LLM Wiki direction associated with Andrej Karpathy
- the knowledge-base and KMS implementation ideas documented in thClaws

The shared theme is that durable AI memory should be maintained knowledge, not just retained chat context.

## Core bet

The core bet of GPTkms is that a good memory system for coding agents should be:

- markdown-first
- provenance-aware
- scoped between project and global knowledge
- exposed through tools instead of hidden prompt stuffing

## Design direction

In practical terms, this means:

1. markdown pages are the durable layer
2. raw notes remain separate from compiled knowledge
3. MCP is the operational interface
4. skills teach when to retrieve, when to promote, and when to stay cautious

## Near-term direction

The next stage is not more infrastructure for its own sake.

The next stage is proving that this workflow stays useful when:

- the KMS spans multiple repos
- global pages need merging instead of only creation
- retrieval needs better ranking and conflict handling
- the system is packaged for easier reuse

