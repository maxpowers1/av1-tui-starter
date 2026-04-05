# av1-tui

A command-line TUI for selecting video files and batch-converting them to AV1.

Also serves as a proving ground for evaluating two approaches to tracking code
decisions made by agentic coding systems (Claude Code, etc.):

1. **Markdown ADR files** — structured documents in `docs/adr/`
2. **Git commit trailers** — machine-parseable metadata in commit messages

## The Question

> Is it better to keep decision memory in markdown files, in the git log, or both?

This repo is the experiment to find out.

## Structure

```
.
├── CLAUDE.md                          # Project context for Claude Code
├── MEMORY.md                          # Auto-captured learnings
├── .claude/
│   ├── agents/
│   │   └── decision-reviewer.md       # Subagent: audits decision tracking
│   └── commands/
│       ├── new-decision.md            # /new-decision — create an ADR
│       └── audit-decisions.md         # /audit-decisions — check for drift
├── docs/
│   ├── adr/
│   │   ├── TEMPLATE.md                # ADR template
│   │   └── 0001-use-dual-track-*.md   # First ADR (about the process itself)
│   └── decisions/
│       ├── COMMIT_CONVENTION.md       # Git commit format for decisions
│       ├── DECISION_LOG.md            # Flat index of all decisions
│       └── EXPERIMENT_NOTES.md        # Observations comparing approaches
└── src/                               # AV1 TUI app
```

## Getting Started

1. Clone this repo
2. Open it with Claude Code: `claude`
3. Start building — you'll immediately face decisions like:
   - Which TUI framework? (Textual, curses, rich)
   - Which AV1 encoder? (SVT-AV1 via ffmpeg, rav1e, libaom)
   - How to handle file selection UX?
   - Encoding presets and defaults?
   - Concurrency model for batch jobs?
   - Progress reporting strategy?
4. Use `/new-decision` whenever you face a choice
5. Periodically run `/audit-decisions` to check for drift
6. Record observations in `docs/decisions/EXPERIMENT_NOTES.md`

## Expected Outcomes

After 10-15 decisions, you should be able to answer:
- Which approach has lower friction?
- Which is more useful when Claude Code resumes a session?
- Which stays more accurate over time?
- Is the dual-track approach worth the overhead, or should you pick one?
