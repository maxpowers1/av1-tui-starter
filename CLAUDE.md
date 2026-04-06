# Project: av1-tui

## What This Is
A command-line TUI tool that lets you browse a file system, select video files,
and batch-convert them to AV1. Also a proving ground for an agentic coding
framework — see `docs/CONTEXT_GUIDE.md` for the context-layer model.

## Tech Stack
- Python 3.12+
- TUI framework: **Textual** (see ADR-0002)
- AV1 encoder: **ab-av1** (see ADR-0003)
- pytest, ruff, mypy (dev tools)

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
- Every significant design choice gets an ADR (see Decision Tracking)

## Decision Tracking
Decisions live in markdown ADR files (primary) with git trailers as audit trail
(see ADR-0004, `docs/CONTEXT_GUIDE.md`). Use `/new-decision` to create an ADR.

**Current decisions:** See `docs/decisions/DECISION_LOG.md` for the full index.

## Project Conventions
- snake_case for Python files and functions
- Type hints on all function signatures
- Docstrings on public functions
- Tests mirror source structure: `src/foo.py` → `tests/test_foo.py`
- All subprocess calls use list-form args, never shell=True with interpolation
- All file paths use `pathlib.Path`
- Run `/qa` before committing any feature or refactor
- Pre-commit hook enforces ruff lint + format (setup: `git config core.hooksPath .githooks`)

## Available Agents and Commands
- `/plan` — sketch an architecture plan before implementing (checks against existing ADRs)
- `/handoff` — write a session handoff note before ending a session
- `/new-decision` — create an ADR + commit with decision trailers
- `/audit-decisions` — cross-reference ADRs and decision log for gaps
- `/qa` — run the QA agent (tests, types, lint, encoding safety, ADR compliance)
- `/health` — check the framework itself (context budget, decision log quality, structural integrity)
- `decision-reviewer` subagent — audits decision tracking for gaps
- `qa` subagent — full QA sweep with structured report
- `framework-health` subagent — framework maintenance audit

## Context Budget
Keep this file under 100 lines. Extract details into `docs/` and reference them
here. See `docs/CONTEXT_GUIDE.md` for the full context-layer model.

## Files to Read on Session Start
- `docs/HANDOFF.md` — previous session's handoff note (check if anything is in progress)
- `docs/decisions/DECISION_LOG.md` — scan for decision implications (L2 cache)
- Only open individual ADRs when working on code they affect (L3 cache)
- `MEMORY.md` — auto-loaded by Claude Code (L1 cache)
