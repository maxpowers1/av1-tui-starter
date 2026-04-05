# Decision Log

A flat, chronological record of every decision. This is the "at a glance" view.
For full context, see the linked ADR or commit.

<!-- Format: Date | Decision | Source | Decided By -->

| Date | Decision | ADR | Commit | Decided By |
|------|----------|-----|--------|------------|
| 2026-04-04 | Use dual-track decision recording (markdown ADRs + git trailers) | [ADR-0001](../adr/0001-use-dual-track-decision-recording.md) | — | human+claude-code |
| 2026-04-04 | Choose Textual as the TUI framework | [ADR-0002](../adr/0002-choose-textual-as-tui-framework.md) | — | human+claude-code |
| 2026-04-04 | Use ab-av1 as the AV1 encoding backend | [ADR-0003](../adr/0003-use-ab-av1-as-encoding-backend.md) | — | human+claude-code |

---

## How to use this log

### For humans
Scan this table when you need to remember what was decided. Click through to
the ADR for full context.

### For Claude Code
When starting a session, read this file to understand the current state of
decisions. If you see a gap (a decision was made but not logged here), flag it.

### Maintenance rules
- Every ADR gets a row here
- Every `decision:` commit trailer gets a row here
- If the two sources disagree, that's a finding for the experiment — note it
  in `docs/decisions/EXPERIMENT_NOTES.md`
