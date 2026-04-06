Audit the decision tracking system for gaps and drift.

Use the `decision-reviewer` subagent to:

1. List all ADR files in `docs/adr/` (excluding TEMPLATE.md)
2. Read `docs/decisions/DECISION_LOG.md`
3. Cross-reference the two:
   - ADRs missing from the decision log
   - Decision log rows with weak or missing Implication columns
   - ADRs missing a TL;DR section
4. Scan code for unrecorded decisions (implicit choices without ADRs)
5. Check for stale ADRs that no longer match the implementation
6. Produce a structured checklist report
