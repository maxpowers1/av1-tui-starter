# Decision Tracking Protocol

## When to Record a Decision

Record an ADR when any of these are true:
- Choosing between two or more viable approaches
- Introducing a new dependency
- Changing an existing pattern
- Making a trade-off (performance vs readability, speed vs quality, etc.)
- Deviating from a convention established in a previous ADR

## Dual-Track Recording (The Experiment)

We maintain decisions in TWO places to compare them:

1. **Markdown ADRs** → `docs/adr/NNNN-title.md` using `docs/adr/TEMPLATE.md`
2. **Git commit messages** → Structured commits using `docs/decisions/COMMIT_CONVENTION.md`

At the end of the experiment we compare:
- Which was easier to query/search?
- Which had less friction to create?
- Which stayed more accurate over time?
- Which was more useful when resuming a session?

See `docs/decisions/EXPERIMENT_NOTES.md` for running observations.

## How to Reference Decisions

| From where | Format |
|------------|--------|
| Code comments | `# See ADR-0003` or `# Decision: <short description>` |
| CLAUDE.md | Link to ADR number |
| Commits | Use `decision:` trailer (see COMMIT_CONVENTION.md) |
| DECISION_LOG.md | Add a row with date, decision, implication, ADR link |

## Recording Workflow

The `/new-decision` command automates both tracks:
1. Creates the ADR file from the template
2. Adds a row to DECISION_LOG.md
3. Drafts a commit with `decision:` trailers
4. Shows you the commit message for review before committing

## Provenance

Every decision records who (or what) made it:
- `human` — human decided, agent just transcribed
- `claude-code` — agent decided, human approved
- `human+claude-code` — collaborative decision

This is captured in both the ADR's Provenance section and the commit's
`decided-by:` trailer.
