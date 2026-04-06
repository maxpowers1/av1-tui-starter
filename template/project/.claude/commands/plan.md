Before implementing, create an architecture plan for the work we're about to do.

## Steps

1. **Clarify scope.** Restate what we're building or changing in one sentence.
   If it's ambiguous, ask me before proceeding.

2. **Check constraints.** Read `docs/decisions/DECISION_LOG.md` and check
   whether any active decisions affect this work. List them. If the plan
   would contradict an existing ADR, flag it — we either need to work within
   the constraint or supersede the ADR.

3. **Sketch the approach.** Produce a plan with:
   - **Files to create or modify** (be specific — paths, not vague descriptions)
   - **Order of operations** (what to build first, what depends on what)
   - **Key choices** — any forks where we'll need to pick between options.
     For each, briefly state the options and your recommendation.

4. **Identify what needs an ADR.** If the plan involves non-trivial choices
   (new dependency, new pattern, architectural trade-off), list them. These
   should become `/new-decision` calls before or during implementation.

5. **Call out risks.** What could go wrong? What are the unknowns? What would
   make us want to revisit this plan mid-implementation?

6. **Estimate scope.** Roughly: is this a single commit, a few commits, or a
   multi-session effort? If multi-session, suggest natural breakpoints.

## Output format

```
## Plan: [one-line description]

### Constraints from existing decisions
- ADR-NNNN: [what it means for this work]

### Approach
1. [step]
2. [step]
...

### Files
- Create: [path] — [purpose]
- Modify: [path] — [what changes]

### Decisions needed
- [ ] [choice that needs an ADR]

### Risks
- [risk and mitigation]

### Scope
[single commit / few commits / multi-session]
[natural breakpoints if multi-session]
```

## Rules
- Don't implement anything yet. Plan only.
- Keep it concrete — file paths, not abstractions.
- If I disagree with part of the plan, I'll say so and we'll iterate before
  building anything.
- Once we agree on the plan, I'll say "go" and we switch to implementation.
