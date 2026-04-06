# Context Guide: Where Information Lives

This project uses a layered context system — like a CPU cache hierarchy — to
give agents and humans the right amount of information at the right time.

**Core principle:** Each layer contains enough to decide whether to go deeper,
and no more.

## The Layers

### Layer 0 — CLAUDE.md (always loaded)
**Cost:** ~100-150 lines, always in context window.
**Contains:** Project identity, active conventions, agent/command inventory,
pointers to deeper layers.
**Rule:** If it doesn't affect every session, it doesn't belong here. No
rationale, no history, no protocol details — just "what" and "where to look."

### Layer 1 — MEMORY.md index (always loaded)
**Cost:** ~50 lines, always in context window.
**Contains:** One-line pointers to memory files. User preferences, experiment
observations, cross-session continuity.
**Rule:** Each entry is a hook — enough to decide if the memory file is relevant.
Dereference only when needed.

### Layer 2 — DECISION_LOG.md, HANDOFF.md, Memory files (one read away)
**Cost:** One tool call to read.
**Contains:** Decision summaries with *implications* (what it means for daily
work), session handoff notes, memory file content.
**Rule:** A row in DECISION_LOG should give you enough context to skip the full
ADR 80% of the time. HANDOFF.md is ephemeral — it tells you what the last
session left behind. Read it at session start, then treat it as stale.

### Layer 3 — ADR files + detailed docs (two reads away)
**Cost:** Find via index, then read. Two tool calls.
**Contains:** Full decision context — options considered, trade-offs, consequences,
provenance.
**Rule:** Only read when you need the "why" behind a specific decision, or when
you're touching code directly affected by that decision.

### Layer 4 — Git log (query-based)
**Cost:** Requires a targeted query. Expensive to scan broadly.
**Contains:** Commit history, `decision:` trailers, audit trail.
**Rule:** Never read proactively. Query when you need "when did we change X" or
"who decided Y." The decision-reviewer agent uses this layer; most sessions
don't need to.

### Layer 5 — Code + inline comments (read on demand)
**Cost:** Read when working on specific files.
**Contains:** The implementation itself. `# See ADR-0003` comments create links
back to Layer 3.
**Rule:** Code is the source of truth for *what exists now*. ADRs are the source
of truth for *why it exists*.

## How to Use This When Adding Information

Ask yourself: **who needs this, and when?**

| If the information is... | Put it in... | Example |
|--------------------------|-------------|---------|
| A rule every session must follow | CLAUDE.md (L0) | "All paths use pathlib.Path" |
| A user preference or cross-session learning | Memory file (L1-2) | "User prefers uv over pip" |
| A decision summary + daily-work implication | DECISION_LOG.md (L2) | "Textual as TUI → use reactive model" |
| What the last session left behind | HANDOFF.md (L2) | "File browser done, encoding screen in progress" |
| Full decision rationale with options | ADR file (L3) | "Why Textual over urwid and curses" |
| A historical fact about when/who | Git trailers (L4) | "decided-by: human+agent" |
| A pointer from code to its rationale | Code comment (L5) | `# See ADR-0002` |

## How to Use This When Looking for Information

| If you need to know... | Start at... | Go deeper if... |
|------------------------|------------|-----------------|
| What conventions to follow | CLAUDE.md (L0) | — |
| What the last session was doing | HANDOFF.md (L2) | — |
| What was decided and what it means | DECISION_LOG.md (L2) | You need the full "why" → ADR (L3) |
| Why a specific decision was made | ADR file (L3) | — |
| When something changed or who did it | Git log (L4) | — |
| What the code actually does now | Code (L5) | You need the "why" → L3 via comment link |

## Anti-Patterns

- **Duplicating data across layers.** If CLAUDE.md has a decisions table AND
  DECISION_LOG.md has the same table, they will drift. One should point to
  the other.
- **Putting rationale in L0.** CLAUDE.md should say *what*, not *why*. The
  "why" lives in ADRs (L3).
- **Reading ADRs at session start.** Scan DECISION_LOG (L2) instead. Only
  open an ADR when you're working on code it affects.
- **Storing ephemeral state in memory.** Memory is for cross-session context.
  Use tasks/plans for in-session tracking.
- **Ignoring the implication column.** "Use Textual" is not enough. "Use
  Textual → reactive model, DirectoryTree widget, CSS-based styling" tells
  an agent what it actually means for implementation.

## Tool Mapping

This framework is tool-agnostic. The concepts map to any agentic coding tool:

| Framework concept | Claude Code | Cursor | Generic |
|-------------------|-------------|--------|---------|
| Project context file (L0) | `CLAUDE.md` | `.cursorrules` | Tool-specific root config |
| Agent definitions | `.claude/agents/` | Custom rules | Tool-specific agent config |
| Slash commands | `.claude/commands/` | Custom rules | Tool-specific command config |
| Memory / learnings | `MEMORY.md` (auto-loaded) | Notepad | Persistent scratchpad |
| Model weight: lightweight | `sonnet` | Default model | Fast, cheap, good for focused tasks |
| Model weight: heavy reasoning | `opus` | Advanced model | Expensive, good for architecture |

The decision tracking system (ADRs, DECISION_LOG, git trailers), the cache
hierarchy, the session lifecycle, and the QA/audit agents are fully
tool-agnostic. Only the config file locations and model names need remapping.

## For Template Users

When adapting this framework for a new project:

1. Copy this file as-is — the layers are project-agnostic.
2. Rename/move the project context file if your tool uses a different name.
3. Customize the project context file for your project's identity and conventions.
4. Remap agent and command definitions to your tool's config format.
5. Populate DECISION_LOG.md with your first decisions.
6. Write ADRs using `docs/adr/TEMPLATE.md` for non-trivial choices.
7. Let memory accumulate naturally — don't pre-populate it.
