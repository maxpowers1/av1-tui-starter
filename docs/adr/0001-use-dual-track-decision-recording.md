# ADR-0001: Use Dual-Track Decision Recording (Markdown + Git Trailers)

## Status
Accepted

## Date
2026-04-04

## Context
We're building an AV1 encoding TUI and using it as a proving ground to evaluate
how agentic coding tools (Claude Code, etc.) should track the decisions they
make during development.

The core question: should decisions live in standalone markdown files, in git
commit metadata, or both? We need to pick a tracking approach before we start
making actual technical decisions about the app.

## Options Considered

### Option A: Markdown ADRs only (`docs/adr/`)
- **Pros:** Rich context, easy for agents to read at session start, human-friendly,
  editable after the fact
- **Cons:** Extra file to create (friction), can drift from reality if not maintained,
  not tied to specific code changes
- **Effort:** Low per-ADR, but requires discipline

### Option B: Git commit trailers only (`decision:` trailers)
- **Pros:** Zero extra files, decision is tied to the exact code change, queryable
  with `git log --grep`, inherently versioned
- **Cons:** Commit messages are immutable (can't update if understanding evolves),
  limited space for context, harder for agents to bulk-read at session start
- **Effort:** Low — just a longer commit message

### Option C: Both (dual-track)
- **Pros:** We get the benefits of both and can empirically compare them, gives us
  redundancy, forces us to articulate decisions twice (which may improve clarity)
- **Cons:** Double the work, risk of the two sources drifting apart, more process
  overhead for a small project
- **Effort:** Medium — mitigated by Claude Code slash commands that create both

## Decision
Use dual-track (Option C) because the entire point of this project is to
evaluate which approach works better. We'll run both in parallel and score them
against criteria in `docs/decisions/EXPERIMENT_NOTES.md`. The `/new-decision`
slash command reduces the friction by creating both artifacts in one flow.

If the experiment shows one approach is clearly superior, we'll drop the other
and record that as a new ADR that supersedes this one.

## Consequences

### Positive
- We get real data on both approaches instead of guessing
- The slash commands make dual-track nearly as easy as single-track
- If they drift apart, the drift itself is useful experimental data

### Negative
- Slightly more overhead per decision
- Risk of "process fatigue" on a small project
- The decision-reviewer subagent adds another moving part

### Risks
- We might get so focused on the decision-tracking process that we forget to
  actually build the AV1 tool. Mitigated by keeping this lightweight.

## Related
- `docs/decisions/COMMIT_CONVENTION.md` — the git trailer format
- `docs/decisions/EXPERIMENT_NOTES.md` — where we score the two approaches
- `.claude/commands/new-decision.md` — slash command that creates both artifacts

## Provenance
- **Decided by:** human+claude-code
- **Session context:** Initial project setup, evaluating decision-tracking patterns
