Audit the decision tracking system for gaps and drift:

1. List all ADR files in `docs/adr/` (excluding TEMPLATE.md)
2. List all `decision:` trailers from `git log --grep='decision:'`
3. Read `docs/decisions/DECISION_LOG.md`
4. Cross-reference all three sources
5. Report:
   - ADRs missing from the decision log
   - Git decisions missing from the decision log
   - Decision log entries missing an ADR or commit reference
   - Any contradictions between sources
6. Append findings to `docs/decisions/EXPERIMENT_NOTES.md` under the relevant observation section
