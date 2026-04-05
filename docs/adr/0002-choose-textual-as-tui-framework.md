# ADR-0002: Choose Textual as the TUI Framework

## Status
Accepted

## Date
2026-04-04

## Context
The av1-tui tool needs a terminal UI framework that supports three core
interactions: file browser navigation, multi-select for choosing video files,
and a progress bar for encoding feedback. The TUI must also work well with
long-running subprocesses (ffmpeg) that report progress asynchronously.

Three candidates were evaluated: Textual, urwid, and raw curses.

## Options Considered

### Option A: Textual
- **Pros:**
  - Built-in `DirectoryTree` widget (file browser out of the box)
  - Built-in `SelectionList` widget (multi-select out of the box)
  - Built-in `ProgressBar` widget
  - Async-first design (`asyncio`) — natural fit for subprocess management
  - CSS-like styling and responsive layout system
  - Actively maintained by the Textualize team
  - Strong documentation and growing ecosystem
- **Cons:**
  - Heavier dependency (~10 MB)
  - Relatively newer, less battle-tested than curses
- **Effort:** Low — all three required widgets exist as built-ins

### Option B: urwid
- **Pros:**
  - Mature library (since ~2004)
  - Lighter weight than Textual
  - Has a `ProgressBar` widget
- **Cons:**
  - No built-in file browser — would need custom build on `TreeWidget`
  - No built-in multi-select — would need custom implementation on `ListBox`
  - Less active development in recent years
  - Dated documentation
  - Manual event loop wiring for async subprocess integration
- **Effort:** Medium — some widgets exist, others need custom building

### Option C: Raw curses
- **Pros:**
  - Zero dependencies (Python standard library)
  - Maximum control over rendering
  - Smallest footprint
- **Cons:**
  - File browser, multi-select, and progress bar all built from scratch
  - No layout system — manual `addstr` positioning
  - Cross-platform issues (especially Windows/ncurses availability)
  - Significant development effort and error-prone
- **Effort:** High — everything from scratch

## Decision
Use **Textual**. It provides all three required widgets as built-ins
(DirectoryTree, SelectionList, ProgressBar), eliminating weeks of custom widget
development. Its async-first architecture is the right primitive for running
ffmpeg subprocesses with real-time progress reporting. The ~10 MB dependency
cost is acceptable for a desktop CLI tool that already depends on ffmpeg.

## Consequences

### Positive
- File browser, multi-select, and progress bar available immediately
- Async subprocess management is idiomatic, not bolted on
- CSS-like theming makes UI iteration fast
- Active maintenance reduces risk of bit rot

### Negative
- Adds a non-trivial dependency to what could otherwise be a stdlib-only tool
- Team members need to learn Textual's reactive/widget model
- Textual's API is still evolving — minor breaking changes between versions possible

### Risks
- If Textualize reduces maintenance, we'd be locked into a framework with
  custom abstractions. Mitigation: the TUI is a skin over separated encoding
  logic (see Architecture Principles), so swapping frameworks is feasible.

## Related
- Related ADRs: ADR-0001 (dual-track decision recording)
- Relevant commits: (will be filled by the commit recording this decision)
- Discussion: Evaluated in Claude Code session, 2026-04-04

## Provenance
- **Decided by:** human+claude-code
- **Session context:** User requested framework evaluation for file browsing, multi-select, and progress bar requirements. Claude Code provided comparative analysis; user confirmed Textual.
