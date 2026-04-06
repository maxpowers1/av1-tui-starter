# Glossary

Terms and acronyms used in this framework. Separated into **framework terms**
(reusable across any project) and **project terms** (specific to this codebase).

---

## Framework Terms

These apply to any project using this agentic coding framework.

### Acronyms

| Term | Definition |
|------|-----------|
| **ADR** | Architecture Decision Record. A markdown file documenting a significant design choice — the context, options considered, what was decided, and why. Lives in `docs/adr/`. |
| **L0–L5** | Cache layers in the context hierarchy. L0 (always loaded, cheapest) through L5 (read on demand, most expensive). See `docs/CONTEXT_GUIDE.md`. |
| **QA** | Quality Assurance. In this framework, a subagent that runs tests, linting, type checks, and ADR compliance before commits. |
| **TL;DR** | Too Long; Didn't Read. A one-sentence summary at the top of each ADR capturing the decision and its daily-work implication. |
| **CLI** | Command-Line Interface. A program operated via terminal commands rather than a graphical UI. |

### Concepts

| Term | Definition |
|------|-----------|
| **Cache hierarchy** | The organizing principle of this framework. Information is stored in layers (L0–L5) ordered by access cost, like CPU cache. Each layer contains enough to decide whether to go deeper. See `docs/CONTEXT_GUIDE.md`. |
| **Session handoff** | A note written at the end of a work session (`/handoff`) capturing what was done, what's in progress, and what the next session needs to know. Stored in `docs/HANDOFF.md`, overwritten each time. |
| **Provenance** | A record of who or what made a decision. One of: `human` (human decided, agent transcribed), `claude-code` (agent decided, human approved), or `human+claude-code` (collaborative). Captured in ADR files and git trailers. |
| **Implication** | A column in DECISION_LOG.md describing what a decision means for daily coding work. The key that lets agents skip reading the full ADR 80% of the time. |
| **Git trailers** | Machine-parseable key-value metadata in git commit messages. Used as an audit trail for decisions. Example: `decision: Use Textual as TUI framework`. Queryable via `git log --grep`. |
| **Architecture plan** | A structured sketch of an approach created before implementation via `/plan`. Checks against existing ADRs, identifies files to touch, flags decisions that need recording, and estimates scope. Not persisted — lives in the session. |
| **Slash command** | A user-invoked operation in Claude Code (e.g., `/plan`, `/qa`, `/new-decision`, `/handoff`). Defined in `.claude/commands/`. Runs in the current session's context. |
| **Subagent** | A focused worker agent spun up by Claude Code to handle a specific task (e.g., QA checks, decision auditing). Defined in `.claude/agents/`. Runs in its own context with limited tools. |
| **Pre-commit hook** | A script that runs automatically before every `git commit`. In this framework, it enforces fast lint and format checks. Lives in `.githooks/`. |
| **Framework checks** | QA checks that are reusable across any project: tests pass, types check, lint clean, ADR compliance. Contrast with domain checks. |
| **Domain checks** | QA checks specific to a project's problem space (e.g., encoding safety for a video tool, API auth for a web service). Customized per project in the QA agent. |
| **Drift** | When documentation diverges from the actual implementation over time. A key risk for any decision-tracking system. |
| **Context budget** | The finite amount of information that can be loaded into an agent's context window. The cache hierarchy exists to manage this budget efficiently. |
| **Unrecorded decision** | A design choice made in code without a corresponding ADR. Treated as a QA finding in this framework — every non-trivial choice should be traceable. |
| **Anti-pattern** | A documented misuse of the framework. Examples: duplicating data across cache layers, putting rationale in L0, reading all ADRs at session start. See `docs/CONTEXT_GUIDE.md`. |
| **Audit trail** | The immutable record of when decisions were made and by whom. In this framework, git history serves as the audit trail (L4). |

### Files

| File | Role | Cache Layer |
|------|------|-------------|
| **CLAUDE.md** | Project identity, conventions, pointers to deeper context | L0 — always loaded |
| **MEMORY.md** | User preferences, cross-session learnings | L1 — always loaded |
| **HANDOFF.md** | Previous session's state (ephemeral, overwritten each session) | L2 — one read away |
| **DECISION_LOG.md** | Scannable index of all decisions with implications | L2 — one read away |
| **ADR files** (`docs/adr/NNNN-*.md`) | Full decision rationale, options, trade-offs | L3 — two reads away |
| **CONTEXT_GUIDE.md** | Documents the cache hierarchy model itself | L3 — reference doc |
| **PROTOCOL.md** | Decision recording rules and workflow | L3 — reference doc |
| **FRAMEWORK_DIAGRAM.md** | Visual diagrams of session lifecycle and agent map | L3 — reference doc |
| **COMMIT_CONVENTION.md** | Git commit message format with decision trailers | L3 — reference doc |

---

## Project Terms

These are specific to the av1-tui application. Replace them when adapting the
framework for a different project.

| Term | Definition |
|------|-----------|
| **AV1** | An open, royalty-free video codec. The encoding target for this tool. |
| **ab-av1** | A Rust CLI tool that performs VMAF-targeted AV1 encoding. This project shells out to it as its encoding backend (see ADR-0003). |
| **VMAF** | Video Multimethod Assessment Fusion. A perceptual video quality metric developed by Netflix. ab-av1 uses it to find the optimal encoding quality. |
| **CRF** | Constant Rate Factor. A quality parameter for video encoding — lower means higher quality. ab-av1's `auto-encode` searches for the optimal CRF to hit a VMAF target. |
| **SVT-AV1** | Scalable Video Technology for AV1. The primary AV1 encoder used by ab-av1. |
| **TUI** | Terminal User Interface. A text-based graphical interface that runs in a terminal. This project uses the Textual framework for its TUI (see ADR-0002). |
| **Textual** | A Python TUI framework by Textualize. Provides built-in widgets (DirectoryTree, SelectionList, ProgressBar) and an async-first, CSS-styled architecture. |
| **Encoding safety** | Domain-specific QA checks: subprocess list-form args, pathlib paths, exit code handling, no file clobbering, no full-file memory reads. |
