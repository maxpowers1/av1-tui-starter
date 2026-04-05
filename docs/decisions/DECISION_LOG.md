# Decision Log

The "at a glance" index for all decisions. This is Layer 2 in the context
hierarchy (see `docs/CONTEXT_GUIDE.md`) — read this instead of opening every
ADR. The **Implication** column tells you what a decision means for daily work.

| Date | Decision | Implication | ADR | Commit | Decided By |
|------|----------|-------------|-----|--------|------------|
| 2026-04-04 | ~~Use dual-track decision recording~~ | ~~Superseded by ADR-0004~~ | [ADR-0001](../adr/0001-use-dual-track-decision-recording.md) | — | human+claude-code |
| 2026-04-04 | Choose Textual as TUI framework | Use reactive widget model, DirectoryTree/SelectionList/ProgressBar built-ins, CSS-based styling, async-first subprocess handling | [ADR-0002](../adr/0002-choose-textual-as-tui-framework.md) | — | human+claude-code |
| 2026-04-04 | Use ab-av1 as encoding backend | Shell out to `ab-av1 auto-encode`; parse its progress output; users must install ab-av1 + compatible ffmpeg separately | [ADR-0003](../adr/0003-use-ab-av1-as-encoding-backend.md) | — | human+claude-code |
| 2026-04-04 | Use layered context model for decisions | Markdown ADRs are primary; git trailers are audit trail not co-equal track; info layered by access cost (see CONTEXT_GUIDE.md) | [ADR-0004](../adr/0004-layered-context-model.md) | — | human+claude-code |

---

## How to use this log

**For agents:** Read this file at session start (L2 cache). The Implication
column should answer most questions. Only open the linked ADR (L3) when you
need full rationale — e.g., when you're changing code affected by that decision.

**For humans:** Scan the table when you need to remember what was decided.
Click through to the ADR for full context.

## Maintenance rules
- Every ADR gets a row here with a meaningful Implication
- Every `decision:` commit trailer gets a row here
- If the Implication column doesn't save you from opening the ADR, rewrite it
- If sources disagree, note it in `docs/decisions/EXPERIMENT_NOTES.md`
