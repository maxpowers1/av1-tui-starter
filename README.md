# av1-tui

A command-line TUI for selecting video files and batch-converting them to AV1.

Also serves as a proving ground for a **reusable agentic coding framework** —
a set of agents, commands, hooks, and documentation patterns that help
agentic coding tools produce high-quality, well-documented work.

## The Framework

This repo includes a tool-agnostic framework for managing decisions, context,
and quality in agentic coding workflows. The core ideas:

- **Layered context model** — information stored at the right cache level
  (see `docs/CONTEXT_GUIDE.md`)
- **Decision tracking** — ADR files + a scannable decision log with implications
- **Session continuity** — handoff notes bridge sessions without blowing up
  the context window
- **Quality gates** — QA agent, pre-commit hooks, framework health checks

## Structure

```
.
├── CLAUDE.md                          # Project context file (L0 — always loaded)
├── MEMORY.md                          # Auto-captured learnings (L1)
├── .claude/                           # Agent tool config (remap for your tool)
│   ├── agents/
│   │   ├── qa.md                      # QA agent (framework + domain checks)
│   │   ├── decision-reviewer.md       # Decision tracking auditor
│   │   └── framework-health.md        # Framework maintenance auditor
│   └── commands/
│       ├── plan.md                    # /plan — architecture plan before implementing
│       ├── handoff.md                 # /handoff — session handoff note
│       ├── new-decision.md            # /new-decision — create an ADR
│       ├── audit-decisions.md         # /audit-decisions — check for drift
│       ├── qa.md                      # /qa — run QA agent
│       └── health.md                  # /health — run framework health agent
├── .githooks/
│   └── pre-commit                     # ruff lint + format (automatic)
├── docs/
│   ├── CONTEXT_GUIDE.md               # Cache hierarchy model + tool mapping
│   ├── HANDOFF.md                     # Session handoff note (L2, ephemeral)
│   ├── FRAMEWORK_DIAGRAM.md           # Visual diagrams (Mermaid)
│   ├── GLOSSARY.md                    # All terms and acronyms
│   ├── adr/
│   │   ├── TEMPLATE.md                # ADR template
│   │   └── 0001-*.md ... 0004-*.md    # Architecture decisions
│   └── decisions/
│       ├── DECISION_LOG.md            # Scannable index with implications (L2)
│       ├── PROTOCOL.md                # When and how to record decisions
│       ├── COMMIT_CONVENTION.md       # Git commit format with decision trailers
│       └── EXPERIMENT_NOTES.md        # Findings from the decision-tracking experiment
└── src/                               # AV1 TUI app (domain code)
```

## Getting Started

1. Clone this repo
2. Install dev dependencies: `uv sync`
3. Set up the pre-commit hook: `git config core.hooksPath .githooks`
4. Open the project with your agentic coding tool
5. Read `docs/CONTEXT_GUIDE.md` to understand the layered context model
6. Use the commands:
   - `/plan` before implementing
   - `/new-decision` when you make a non-trivial choice
   - `/qa` before committing
   - `/handoff` before ending a session
   - `/health` periodically to check framework integrity

## Adapting for Another Project

The framework is tool-agnostic. To use it in a new project:

1. Copy the `docs/` directory, `MEMORY.md`, and your tool's config equivalent
2. Remap agent/command definitions to your tool's format
   (see the Tool Mapping table in `docs/CONTEXT_GUIDE.md`)
3. Customize the project context file for your project
4. Replace domain-specific QA checks in the QA agent
5. Start recording decisions with `/new-decision`
