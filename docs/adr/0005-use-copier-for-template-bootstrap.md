# ADR-0005: Use Copier for Template Bootstrap

## Status
Accepted

## Date
2026-04-05

## TL;DR
New projects are bootstrapped via Copier with archetype selection (python, dotnet, generic); framework files copy verbatim, project files are customized via Jinja2 prompts.

## Context
The agentic coding framework needs a way to bootstrap new projects. A user
should be able to create a new repo, select their tech stack, and get a
fully configured project with decision tracking, QA agents, session handoff,
and pre-commit hooks — all customized for their language and ecosystem.

The template engine needs to handle: variable substitution in file contents,
conditional file inclusion (e.g., pyproject.toml only for Python), archetype
selection (python/dotnet/generic), and post-generation tasks (git init, hook
setup).

## Options Considered

### Option A: Copier
- **Pros:**
  - Native conditional file inclusion (Jinja2 in filenames)
  - Multi-stage prompts (questions conditional on previous answers)
  - `copier update` can pull template changes into existing projects
  - YAML config with comments
  - Same Jinja2 engine as Cookiecutter
- **Cons:**
  - Less market awareness than Cookiecutter
  - Smaller community, fewer examples
- **Effort:** Low — similar complexity to Cookiecutter

### Option B: Cookiecutter
- **Pros:**
  - Widely known, large community
  - Many existing examples to reference
  - Stable, mature project
- **Cons:**
  - No native conditional file inclusion (requires post-gen hook workarounds)
  - No multi-stage prompts (all variables flat)
  - No template update mechanism
  - JSON config (no comments)
- **Effort:** Low, but conditional logic is clunkier

### Option C: Shell script
- **Pros:**
  - Zero dependencies
  - Maximum flexibility
  - Simple to understand
- **Cons:**
  - No templating engine — manual string substitution
  - Cross-platform issues (Windows)
  - Reinventing the wheel
- **Effort:** Medium — more code for less capability

## Decision
Use **Copier**. The framework template will evolve over time, and Copier's
native conditional files, branching prompts, and optional update mechanism
are the right primitives for a multi-archetype template that grows. The
smaller community is acceptable because the template structure is simple
enough not to need extensive community support.

## Consequences

### Positive
- Clean archetype selection with conditional prompts per language
- Language-specific files included/excluded without hack workarounds
- Future option for existing projects to pull framework updates
- YAML config is more readable and self-documenting

### Negative
- Users must install Copier (`uv tool install copier`)
- Less Googleable than Cookiecutter when troubleshooting

### Risks
- If Copier is abandoned, the template is still just files + Jinja2 —
  could be migrated to Cookiecutter or a shell script with moderate effort.

## Related
- Related ADRs: ADR-0004 (layered context model — defines what gets templated)
- Relevant commits: (will be filled by the commit recording this decision)
- Discussion: Evaluated during framework bootstrap design session

## Provenance
- **Decided by:** human+agent
- **Session context:** User chose Copier over Cookiecutter after reviewing
  comparative analysis of template engines. Key factor was native conditional
  file inclusion and the potential for template updates.
