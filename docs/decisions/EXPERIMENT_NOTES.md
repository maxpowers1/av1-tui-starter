# Experiment Notes: Markdown ADRs vs Git Log for Decision Tracking

## Hypothesis
Markdown ADR files will be more useful for *resuming context* (starting a new
Claude Code session), while git commit trailers will be more useful for
*querying history* (when did we decide X, who decided it).

## Evaluation Criteria

### 1. Session Resume Quality
When Claude Code starts a new session and reads CLAUDE.md + ADRs, how quickly
does it get up to speed? Compare this with sessions where it's told to read
git log instead.

**Observations:**
- (record here as you go)

### 2. Decision Discovery
When you need to find out "why do we do X this way?", which path gets you
the answer faster?

**Observations:**
-

### 3. Creation Friction
Which method do you (or Claude Code) actually use consistently? Does one
get skipped when you're in flow?

**Observations:**
-

### 4. Accuracy Over Time
Do the ADR files drift from reality? Do commit messages get lazy?

**Observations:**
-

### 5. Agent Effectiveness
Can Claude Code *create* good ADRs? Can it write good decision-trailers
in commits? Which does it do more reliably?

**Observations:**
-

### 6. Cross-Reference Integrity
Do the ADR files and commit trailers stay in sync? What breaks first?

**Observations:**
-

## Running Tally

| Criterion | Markdown ADR Wins | Git Log Wins | Tie | Notes |
|-----------|-------------------|--------------|-----|-------|
| Session Resume | | | | |
| Discovery | | | | |
| Friction | | | | |
| Accuracy | | | | |
| Agent Effectiveness | | | | |
| Cross-Reference | | | | |

## Conclusions
(Fill in when you have enough data points — aim for at least 10-15 decisions)
