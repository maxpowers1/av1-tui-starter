# Project: av1-tui

## What This Is
A command-line TUI tool that lets you browse a file system, select video files,
and batch-convert them to AV1. This is also a proving ground for evaluating
decision-tracking patterns in agentic coding workflows.

We are explicitly testing: **markdown files vs git log** as the source of truth
for code decisions made during development.

## Tech Stack
- Python 3.12+
- TUI framework: (pending — see ADR-0002 when created)
- AV1 encoder: (pending — see ADR-0003 when created)
- pytest (testing)

## What the Tool Does
1. User launches the TUI
2. Browse/navigate the filesystem
3. Select one or more video files (multi-select)
4. Configure encoding options (preset, quality, output location)
5. Kick off AV1 encoding with progress feedback
6. Handle batch jobs (queue, concurrency, error recovery)

## Architecture Principles
- Single-file entry point, modular internals
- Encoding runs as subprocess (wrapping ffmpeg or standalone encoder)
- TUI and encoding logic are fully separated — the TUI is a skin
- Every significant design choice gets recorded (this is the experiment)

## Decision Tracking Protocol

### When to record a decision
Record an ADR when any of these are true:
- Choosing between two or more viable approaches
- Introducing a new dependency
- Changing an existing pattern
- Making a trade-off (performance vs readability, speed vs quality, etc.)
- Deviating from a convention established in a previous ADR

### Dual-track recording (THE EXPERIMENT)
We maintain decisions in TWO places to compare them:

1. **Markdown ADRs** → `docs/adr/NNNN-title.md` using the template in `docs/adr/TEMPLATE.md`
2. **Git commit messages** → Structured commits using the format in `docs/decisions/COMMIT_CONVENTION.md`

At the end of the experiment, we compare:
- Which was easier to query/search?
- Which had less friction to create?
- Which stayed more accurate over time?
- Which was more useful when resuming a session?

### How to reference decisions
- In code comments: `# See ADR-0003` or `# Decision: <short description>`
- In CLAUDE.md updates: Link to the ADR number
- In commits: Use the `decision:` trailer

## Active Decisions
<!-- This section is a living index. Update it as ADRs are created. -->
| ADR | Title | Status | Date |
|-----|-------|--------|------|
| 0001 | Use dual-track decision recording | Accepted | 2026-04-04 |

## Project Conventions
- snake_case for Python files and functions
- Type hints on all function signatures
- Docstrings on public functions
- Tests mirror source structure: `src/foo.py` → `tests/test_foo.py`

## Context Budget
Keep this file under 150 lines. If it grows beyond that, extract sections into
files under `docs/` and reference them here. The goal is to stay within the
"cheap to load" zone for Claude Code's context window.

## Files to Read on Session Start
- `docs/adr/` — scan for any ADRs marked "Proposed" that need resolution
- `docs/decisions/DECISION_LOG.md` — quick-reference log of all decisions
- `MEMORY.md` — auto-captured learnings (if it exists)
