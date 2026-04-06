# Git Commit Convention for Decision Tracking

## Purpose
This convention encodes decisions directly into git history so we can test
whether `git log` can serve as a viable alternative (or complement) to
markdown ADR files.

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

decision: <decision-summary>
alternatives: <what-else-was-considered>
rationale: <why-this-choice>
adr: <ADR-number-if-one-exists>
decided-by: <human|agent|human+agent>
```

### Types
- `feat` — new feature
- `fix` — bug fix
- `refactor` — restructuring without behavior change
- `docs` — documentation only
- `test` — adding or updating tests
- `chore` — build, tooling, config
- `decision` — a commit whose PRIMARY purpose is recording a decision
  (may have no code changes, just docs)

### The `decision:` trailer
This is the key field. It should be a single sentence that captures the choice.
Git trailers are machine-parseable, so we can later extract them with:

```bash
git log --format='%H %s' --grep='decision:'
```

Or more precisely:
```bash
git log --format='%(trailers:key=decision,valueonly)' --grep='decision:'
```

## Examples

### A feature commit that includes a decision
```
feat(api): add health check endpoint

Implemented /health endpoint returning 200 with version info.

decision: Use a simple GET /health over a more complex readiness/liveness split
alternatives: Separate /ready and /live endpoints (k8s style)
rationale: Toy app doesn't need k8s-style probes; one endpoint is sufficient
adr: ADR-0002
decided-by: agent
```

### A pure decision commit (no code changes)
```
decision(db): choose SQLite for data storage

No code changes. Recording the decision to use SQLite as the
data store for this proving ground application.

decision: Use SQLite over PostgreSQL for zero-infrastructure simplicity
alternatives: PostgreSQL, in-memory dicts
rationale: Focus is on testing decision workflows, not database patterns
adr: ADR-0001
decided-by: human+agent
```

## Querying Decisions from Git

### List all decisions
```bash
git log --grep='decision:' --oneline
```

### Show full decision context
```bash
git log --grep='decision:' --format='%n--- %h %ad ---%n%B' --date=short
```

### Extract just the decision trailers
```bash
git log --grep='decision:' --format='%h | %(trailers:key=decision,valueonly)'
```

### Decisions by a specific actor
```bash
git log --grep='decided-by: agent' --oneline
```

### Decisions in a date range
```bash
git log --grep='decision:' --after='2026-04-01' --before='2026-04-30' --oneline
```

## Comparison Notes
At the end of the experiment, answer these questions:

1. **Discoverability:** Was it easier to find a decision via `git log --grep` or
   by scanning `docs/adr/`?
2. **Context richness:** Did the ADR markdown or the commit body provide better
   context when you returned to a decision weeks later?
3. **Friction:** Which felt like less overhead to create — an ADR file or a
   well-structured commit message?
4. **Drift:** Did one method stay more up-to-date than the other?
5. **Agent compatibility:** Could the coding agent use one more effectively than
   the other when resuming sessions?
