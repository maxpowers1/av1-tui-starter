# Experiment Notes: Markdown ADRs vs Git Log for Decision Tracking

## Hypothesis
Markdown ADR files will be more useful for *resuming context* (starting a new
Claude Code session), while git commit trailers will be more useful for
*querying history* (when did we decide X, who decided it).

## Evaluation Criteria

### 1. Session Resume Quality
When Claude Code starts a new session and reads CLAUDE.md + ADRs, how quickly
does it get up to speed? Compare this with sessions where it's told to read
git log instead.

**Observations:**
- 2026-04-04: A second Claude Code instance (acting as framework advisor) read
  CLAUDE.md → ADRs → DECISION_LOG to get up to speed. Never queried git log.
  Markdown was the natural entry point for session resume.

### 2. Decision Discovery
When you need to find out "why do we do X this way?", which path gets you
the answer faster?

**Observations:**
- 2026-04-04: DECISION_LOG (with Implication column) answered most "what does
  this mean?" questions without opening the ADR. Git log was never consulted
  for discovery — you'd have to already know a decision exists to grep for it.

### 3. Creation Friction
Which method do you (or Claude Code) actually use consistently? Does one
get skipped when you're in flow?

**Observations:**
- 2026-04-04: All 3 initial decisions have complete ADR files but `—` in the
  Commit column of DECISION_LOG. The git trailer side was skipped even though
  `/new-decision` was designed to create both. Markdown survived; git didn't.

### 4. Accuracy Over Time
Do the ADR files drift from reality? Do commit messages get lazy?

**Observations:**
- 2026-04-04: ADR files were successfully updated in-place (TL;DR lines added)
  during a framework refactor. This would be impossible with commit messages —
  they're immutable. Decisions evolve as understanding sharpens; a mutable
  medium is better for the "why."

### 5. Agent Effectiveness
Can Claude Code *create* good ADRs? Can it write good decision-trailers
in commits? Which does it do more reliably?

**Observations:**
- 2026-04-04: When a Claude Code instance designed a context system for agents,
  it organically placed markdown at accessible layers (L2-L3) and git at the
  audit layer (L4). The agent's tool affordances favor file reads over git
  queries — file-based storage is the path of least resistance.

### 6. Cross-Reference Integrity
Do the ADR files and commit trailers stay in sync? What breaks first?

**Observations:**
- 2026-04-04: Git side broke first. Three decisions, zero commit trailers.
  The drift happened on day one, before any time pressure or laziness could
  be blamed. The dual-track overhead was enough to kill the git side.

## Running Tally

| Criterion | Markdown ADR Wins | Git Log Wins | Tie | Notes |
|-----------|-------------------|--------------|-----|-------|
| Session Resume | x | | | Agent never queried git for context |
| Discovery | x | | | DECISION_LOG + Implication column was sufficient |
| Friction | x | | | Git trailers skipped on all 3 decisions |
| Accuracy | x | | | Markdown is mutable; commits are frozen |
| Agent Effectiveness | x | | | Agent naturally built a file-first hierarchy |
| Cross-Reference | x | | | Git side drifted on day one |

## Conclusions

Reached early — after 3 decisions and one framework-design session, not the
planned 10-15.

### The question was wrong

The experiment framed markdown and git as competing approaches. The finding is
that they serve different access patterns and belong at different layers of a
context hierarchy:

- **Markdown** (ADR files, DECISION_LOG) is the right home for **decision
  content** — the "what was decided and why." It's structured, mutable,
  indexable, and naturally accessible to agents via file reads.
- **Git** (commit trailers, log) is the right home for **decision audit** —
  the "when, by whom, and alongside what code change." It's immutable,
  timestamped, and tied to specific diffs.

These aren't competing — they're different cache levels. See `docs/CONTEXT_GUIDE.md`
for the full model.

### Why it resolved so fast

1. **Friction kills.** Even with automation (`/new-decision`), the git side
   got skipped. Two artifacts per decision is one too many when you're in flow.
2. **Agent affordances favor files.** Claude Code reads files naturally and
   queries git reactively. A system designed for agents will put files first.
3. **Mutability matters for "why."** Understanding of a decision sharpens over
   time. An immutable medium (commit messages) can't accommodate that.

### What changes

ADR-0001 (dual-track recording) is superseded by ADR-0004 (layered context
model). Git trailers remain useful as audit metadata but are no longer a
co-equal decision track. The `/new-decision` command should still generate a
good commit message with trailers, but the ADR file is the primary artifact.
