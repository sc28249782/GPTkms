# Positioning And Landscape

## Why this document exists

Many projects now try to solve persistent memory for coding agents.

GPTkms should be clear about what it is, what it is not, and where it fits relative to adjacent tools for Codex and ChatGPT Work.

## Short positioning

GPTkms is a markdown-first KMS for Codex and ChatGPT Work that emphasizes:

- durable knowledge over raw transcript retention
- explicit project and global scopes
- promotion workflows instead of flat memory accumulation
- human-readable files
- MCP as the runtime interface
- skills as the workflow layer

## What GPTkms is not

GPTkms is not primarily:

- a vector database product
- a chat transcript archive
- an opaque hidden-memory layer
- a general PKM application
- a finished plugin product yet

## The surrounding landscape

### 1. Official Codex building blocks

OpenAI already provides the main primitives for this kind of system:

- MCP for tool and context integration
- skills for reusable workflows
- project guidance and memory-related workflow patterns

These are the official foundations that GPTkms builds on.

GPTkms is not a replacement for these primitives. It is a composition of them into a durable knowledge workflow.

### 2. Persistent memory MCP tools

There are already community and ecosystem projects for persistent memory around Codex-style agents.

Examples include:

- Basic Memory
- codex-mem
- ai-memory
- other memory-oriented MCP servers and shared memory layers

These tools prove there is real demand for long-term memory in coding-agent workflows.

### 3. PKM and second-brain tools

Tools like Obsidian are strong at human-facing note-taking and long-term personal knowledge management.

GPTkms is closer to an agent-facing operational memory layer than a full second-brain application.

## Where GPTkms differs

### Markdown-first plus scoped memory

Many memory systems focus on recall. GPTkms focuses on memory structure:

- `project` memory for local context
- `global` memory for reusable context

This makes cross-project reuse safer and easier to reason about.

### Promotion as a first-class concept

GPTkms assumes most knowledge should begin local and only later move global.

That is different from flat memory accumulation, where everything gets dumped into one shared layer.

### Raw evidence separate from compiled knowledge

GPTkms keeps:

- `raw/` for evidence and captured notes
- `pages/` for distilled knowledge

This makes later review, editing, and trust much easier.

### Skills plus KMS, not KMS alone

GPTkms is not just storage.

It also defines behavior through skills such as:

- answer from wiki
- promote session insights
- save current session to KMS

That gives Codex a workflow model, not just a memory bucket.

### A bridge toward second-brain tools

GPTkms is also designed to eventually connect with tools like Obsidian without turning the KMS into a general-purpose PKM app.

The likely long-term model is:

- human-facing second brain in Obsidian
- agent-facing operational memory in GPTkms

## Practical comparison

### Compared with memory MCP servers

GPTkms is more opinionated about:

- markdown structure
- project/global scope
- promotion workflows
- knowledge curation

### Compared with plain Codex skills

GPTkms adds:

- persistent file-backed knowledge
- promotion rules
- reusable KMS content across sessions

### Compared with Obsidian

GPTkms is less of a writing environment and more of an operational memory system for agents.

Obsidian is better for:

- broad thinking
- note-taking
- personal knowledge exploration

GPTkms is better for:

- agent retrieval
- Codex workflows
- durable machine-usable project memory

## Working thesis

The working thesis of GPTkms is:

Persistent memory for Codex becomes more trustworthy when it is readable, scoped, curated, and workflow-aware.

## Current implication for the roadmap

This positioning suggests the right order of work is:

1. improve the core KMS workflow
2. improve automation around capture, update, and promotion
3. package the workflow for easier adoption
4. only then deepen second-brain integrations

