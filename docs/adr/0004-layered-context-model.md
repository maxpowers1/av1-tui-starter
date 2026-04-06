# ADR-0004: Use a Layered Context Model for Decision Storage

## Status
Accepted

## Date
2026-04-04

## TL;DR
Decisions live in markdown (ADR files + DECISION_LOG) as the primary source; git trailers are an audit trail, not a co-equal track. Information is layered by access cost, like a CPU cache.

## Context
ADR-0001 established dual-track decision recording — every decision in both a
markdown ADR file and a git commit trailer — as an experiment to compare the
two approaches. After 3 decisions and one framework-design session, the
experiment produced a clear outcome earlier than expected.

Key findings (full details in `docs/decisions/EXPERIMENT_NOTES.md`):

1. **Git trailers were skipped on all 3 decisions.** Even with `/new-decision`
   automation, the Commit column in DECISION_LOG is `—` across the board.
2. **An agent instance designing a context system for agents organically
   placed markdown at accessible layers and git at the bottom.** Agent tool
   affordances favor file reads over git queries.
3. **Markdown is mutable; commits are not.** Decisions were updated in-place
   (TL;DR lines added) during a refactor — impossible with commit messages.
4. **The real question isn't "markdown vs git" but "what goes where."** They
   serve different access patterns and belong at different cache levels.

## Options Considered

### Option A: Continue dual-track (status quo from ADR-0001)
- **Pros:** More data might change the outcome
- **Cons:** The git side is already not being maintained; continuing adds
  overhead for a track that isn't being used
- **Effort:** Medium — ongoing discipline tax

### Option B: Markdown-only (drop git trailers entirely)
- **Pros:** Simplest; one artifact per decision
- **Cons:** Loses the audit trail ("when was this committed, alongside what
  code change"); git trailers are low-cost when they happen organically
- **Effort:** Low

### Option C: Layered model (markdown primary, git as audit trail)
- **Pros:** Each medium does what it's good at — markdown for structured,
  mutable decision content; git for immutable timestamps and code-change
  coupling. Formalizes the cache hierarchy that emerged naturally.
- **Cons:** Slightly more nuanced than "just use markdown"
- **Effort:** Low — we already built the model; this just names it

## Decision
Use the **layered context model** (Option C). Information is stored at the
layer matching its access pattern:

| Layer | Storage | Contains | Access cost |
|-------|---------|----------|-------------|
| L0 | CLAUDE.md | Project identity, conventions, pointers | Always loaded |
| L1 | MEMORY.md | Cross-session learnings, user preferences | Always loaded |
| L2 | DECISION_LOG.md | Decision + implication (one-line each) | One file read |
| L3 | ADR files | Full rationale, options, trade-offs | Find via index + read |
| L4 | Git log | When/who/what-code-changed audit trail | Query on demand |
| L5 | Code + comments | Implementation with `# See ADR-NNNN` links | Read on demand |

**Markdown ADR files** are the primary source of truth for decision content.
**Git commit trailers** are encouraged (good commit messages are always good)
but are an audit trail, not a co-equal track. Missing a trailer is not a
tracking failure.

See `docs/CONTEXT_GUIDE.md` for the full model including lookup tables and
anti-patterns.

## Consequences

### Positive
- Eliminates the friction of maintaining two co-equal artifacts per decision
- Aligns with how agents actually access information (file reads > git queries)
- Makes the context budget explicit — each layer has a cost and a purpose
- Formalizes a model that is project-agnostic and reusable as a template

### Negative
- Git history becomes less self-documenting for decisions (but was already
  failing at this under dual-track)
- Teams that prefer git-centric workflows may find this less natural

### Risks
- The DECISION_LOG Implication column becomes load-bearing — if implications
  are vague, agents will over-read ADRs and waste context. Mitigation: the
  QA agent checks ADR compliance including implication quality.

## Related
- Supersedes: ADR-0001 (dual-track decision recording)
- References: `docs/CONTEXT_GUIDE.md`, `docs/decisions/EXPERIMENT_NOTES.md`
- Implements: The cache hierarchy model proposed during framework design

## Provenance
- **Decided by:** human+agent
- **Session context:** A second agent instance was brought in to evaluate
  the framework's meta-design. While restructuring the context system, the
  agent naturally built a file-first cache hierarchy, revealing that the
  dual-track experiment had an outcome. Human confirmed and directed the
  conclusion to be recorded.
