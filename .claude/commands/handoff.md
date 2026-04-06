Write a session handoff note to `docs/HANDOFF.md` for whoever (human or agent)
picks up this project next.

You already have context from this session — use it. Don't ask me to summarize
what we did; you were here.

## Steps

1. Review what happened this session:
   - What files were changed (check git status/diff)
   - What was accomplished
   - What was started but not finished
   - Any decisions made that might not have ADRs yet

2. Write `docs/HANDOFF.md` using this structure:

```markdown
# Session Handoff

**Updated:** [today's date]
**By:** [human, agent, or human+agent]

## Completed
- (what was finished — be specific about files and features)

## In Progress
- (anything started but not done, with enough context to resume without
  re-reading the whole conversation. Include branch names, file paths,
  and what the next step is.)

## Next Steps
- (prioritized list of what should happen next)

## Watch Out
- (gotchas, failed approaches, things that almost broke, non-obvious
  context that would save the next session time)

## Unrecorded Decisions
- (any choices made this session that don't have ADRs yet — the next
  session should decide whether they need one)
```

3. Show me the handoff note before writing it — I may want to add context
   you don't have (e.g., "I'm handing this to a teammate" or "I'll pick
   this up tomorrow").

## Rules
- **Overwrite** the file, don't append. This is a "current state" note,
  not a log.
- Be concise. The next session will read this cold — respect their context
  budget.
- If there's nothing in progress and no next steps, say so. An empty
  handoff is fine; a dishonest one isn't.
- Anything worth remembering permanently should go in memory or an ADR,
  not here. This file is ephemeral.
