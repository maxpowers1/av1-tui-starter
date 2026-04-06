# Framework Diagrams

## Session Lifecycle

How a session flows from start to finish, and where agents/commands/hooks fire.

```mermaid
flowchart TD
    START([Session Start]) --> READ_HANDOFF["Read HANDOFF.md
    What did the last session leave behind?"]
    READ_HANDOFF --> READ_LOG["Read DECISION_LOG.md
    Scan implications, not full ADRs"]
    READ_LOG --> READ_MEMORY["Read MEMORY.md
    User prefs, cross-session learnings"]
    READ_MEMORY --> WORK{Work Loop}

    WORK --> PLAN["/plan — Sketch approach,
    check against existing ADRs,
    identify decisions needed"]
    PLAN --> IMPLEMENT["Implement
    Human + agent collaboration"]
    IMPLEMENT --> DECISION{"Made a
    non-trivial
    choice?"}
    DECISION -->|Yes| NEW_DECISION["/new-decision
    Creates ADR + updates DECISION_LOG"]
    NEW_DECISION --> QA
    DECISION -->|No| QA

    QA["/qa — Tests, types, lint,
    domain checks, ADR compliance"]
    QA --> QA_PASS{Pass?}
    QA_PASS -->|No| IMPLEMENT
    QA_PASS -->|Yes| COMMIT

    COMMIT[git commit] --> HOOK[["Pre-commit hook
    ruff check + format
    Automatic, seconds"]]
    HOOK --> HOOK_PASS{Pass?}
    HOOK_PASS -->|No| FIX_LINT[Fix lint/format] --> COMMIT
    HOOK_PASS -->|Yes| COMMITTED([Commit lands])

    COMMITTED --> MORE{More work?}
    MORE -->|Yes| WORK
    MORE -->|No| HANDOFF["/handoff
    Write HANDOFF.md for next session"]
    HANDOFF --> END([Session End])

    style PLAN fill:#50b87a,stroke:#333,color:#000
    style HOOK fill:#e8a735,stroke:#333,color:#000
    style QA fill:#4a90d9,stroke:#333,color:#fff
    style NEW_DECISION fill:#50b87a,stroke:#333,color:#000
    style HANDOFF fill:#9b6fc3,stroke:#333,color:#fff
```

## Feature Workflow

What happens when a developer is asked to add a new feature — from request
to landed code. Shows which cache layers, commands, and hooks fire at each step.

```mermaid
flowchart TD
    REQUEST(["Feature request:
    'Add batch queue for encoding'"])

    REQUEST --> CONTEXT

    subgraph CONTEXT["1. Gather Context"]
        direction TB
        C1["CLAUDE.md (L0) — already loaded
        Conventions, architecture principles"]
        C2["MEMORY.md (L1) — already loaded
        User prefs (e.g. always use uv)"]
        C3["HANDOFF.md (L2) — read once
        Is anything in-progress that overlaps?"]
        C4["DECISION_LOG.md (L2) — scan implications
        Any existing decisions that constrain this?"]
        C1 --> C2 --> C3 --> C4
    end

    CONTEXT --> PLAN_CMD

    subgraph PLAN_CMD["2. /plan"]
        direction TB
        P1["Clarify scope with the developer"]
        P2["Check DECISION_LOG for constraints
        e.g. ADR-0003: must shell out to ab-av1"]
        P3["Sketch approach with file paths
        src/queue.py, src/worker.py, tests/..."]
        P4["Flag decisions that need recording
        e.g. concurrency model, error strategy"]
        P5["Estimate scope: S/M/L"]
        P1 --> P2 --> P3 --> P4 --> P5
    end

    PLAN_CMD --> NEED_ADR{"Plan surfaced
    decisions?"}

    NEED_ADR -->|Yes| ADR_FIRST["/new-decision
    Record before implementing
    e.g. ADR-0006: use asyncio task group"]
    NEED_ADR -->|No| BUILD

    ADR_FIRST --> BUILD

    subgraph BUILD["3. Implement"]
        direction TB
        B1["Write code
        Human + agent collaboration"]
        B2["Follow conventions from CLAUDE.md
        Type hints, pathlib, list-form subprocess"]
        B3["Read ADRs only if touching
        code they affect (L3, on demand)"]
        B1 --> B2 --> B3
    end

    BUILD --> MID_DECISION{"Made a
    non-trivial
    choice during
    implementation?"}

    MID_DECISION -->|Yes| MID_ADR["/new-decision
    Record it now, not later"]
    MID_DECISION -->|No| QA_CMD

    MID_ADR --> QA_CMD

    subgraph QA_CMD["4. /qa"]
        direction TB
        Q1["Tests — uv run pytest"]
        Q2["Types — uv run mypy"]
        Q3["Lint — uv run ruff check"]
        Q4["Domain checks — subprocess safety,
        encoding patterns"]
        Q5["ADR compliance — any unrecorded
        decisions in recent changes?"]
        Q1 --> Q2 --> Q3 --> Q4 --> Q5
    end

    QA_CMD --> QA_RESULT{All pass?}
    QA_RESULT -->|No| FIX["Fix issues"] --> QA_CMD
    QA_RESULT -->|Yes| GIT_COMMIT

    subgraph GIT_COMMIT["5. Commit"]
        direction TB
        GC1["git add (specific files)"]
        GC2["git commit with descriptive message
        + decision trailers if applicable"]
        GC3[["Pre-commit hook fires
        ruff check + ruff format
        Seconds, automatic"]]
        GC1 --> GC2 --> GC3
    end

    GIT_COMMIT --> HOOK_OK{Hook pass?}
    HOOK_OK -->|No| FIX_LINT["Fix lint/format"] --> GIT_COMMIT
    HOOK_OK -->|Yes| LANDED

    LANDED([Commit lands]) --> MORE{More work
    on this feature?}
    MORE -->|Yes| BUILD
    MORE -->|No| DONE

    subgraph DONE["6. Wrap Up"]
        direction TB
        D1["Feature complete"]
        D2["/handoff — write session note
        What was done, what to watch"]
        D1 --> D2
    end

    style CONTEXT fill:#50b87a,stroke:#2d7a4f,color:#000
    style PLAN_CMD fill:#50b87a,stroke:#2d7a4f,color:#000
    style BUILD fill:#e0e0e0,stroke:#999,color:#000
    style QA_CMD fill:#4a90d9,stroke:#2c5f99,color:#fff
    style GIT_COMMIT fill:#e8a735,stroke:#b07d1a,color:#000
    style DONE fill:#9b6fc3,stroke:#6b3f93,color:#fff
    style ADR_FIRST fill:#50b87a,stroke:#2d7a4f,color:#000
    style MID_ADR fill:#50b87a,stroke:#2d7a4f,color:#000
```

### Cache Layers Accessed During a Feature

Shows when each layer is read and why — most features never need to go past L2.

```mermaid
flowchart LR
    subgraph ALWAYS["Automatic — No Cost"]
        direction TB
        A_L0["L0: CLAUDE.md
        Conventions, principles, pointers
        Read: always"]
        A_L1["L1: MEMORY.md
        User prefs, learned patterns
        Read: always"]
    end

    subgraph ONCE["Read Once Per Feature"]
        direction TB
        O_L2A["L2: HANDOFF.md
        Read: at session start
        Why: check for overlap"]
        O_L2B["L2: DECISION_LOG.md
        Read: during /plan
        Why: check constraints via implications"]
    end

    subgraph ON_DEMAND["Only If Needed"]
        direction TB
        D_L3["L3: Individual ADR files
        Read: only if touching affected code
        Why: full rationale for a specific choice"]
        D_L4["L4: Git log
        Read: rarely, for audit trail
        Why: who changed what, when"]
        D_L5["L5: Code + comments
        Read: during implementation
        Why: understand existing behavior"]
    end

    ALWAYS ==>|"/plan triggers"| ONCE
    ONCE -.->|"only if relevant"| ON_DEMAND

    style ALWAYS fill:#50b87a,stroke:#2d7a4f,color:#000
    style ONCE fill:#4a90d9,stroke:#2c5f99,color:#fff
    style ON_DEMAND fill:#9b6fc3,stroke:#6b3f93,color:#fff
```

## Context Cache Hierarchy

Where information lives, ordered by access cost. Each layer contains enough
to decide whether to go deeper.

```mermaid
flowchart LR
    subgraph L0["Layer 0 — Always Loaded"]
        CLAUDE["CLAUDE.md (~65 lines)
        Project identity
        Conventions
        Pointers"]
    end

    subgraph L1["Layer 1 — Always Loaded"]
        MEMORY["MEMORY.md (~50 lines)
        User preferences
        Cross-session learnings"]
    end

    subgraph L2["Layer 2 — One Read Away"]
        HANDOFF_F["HANDOFF.md (ephemeral)
        Last session's state"]
        DLOG["DECISION_LOG.md
        Decision + Implication table"]
    end

    subgraph L3["Layer 3 — Two Reads Away"]
        ADR["ADR Files
        Full rationale, options,
        trade-offs, consequences"]
        DOCS["Detailed Docs
        PROTOCOL.md
        CONTEXT_GUIDE.md"]
    end

    subgraph L4["Layer 4 — Query On Demand"]
        GIT["Git Log
        Immutable audit trail
        When, who, what commit"]
    end

    subgraph L5["Layer 5 — Read On Demand"]
        CODE["Code + Comments
        Source of truth for
        what exists now"]
    end

    L0 --> L1 --> L2 --> L3 --> L4 --> L5

    style L0 fill:#50b87a,stroke:#2d7a4f,color:#000
    style L1 fill:#6ec98f,stroke:#2d7a4f,color:#000
    style L2 fill:#4a90d9,stroke:#2c5f99,color:#fff
    style L3 fill:#7baae0,stroke:#2c5f99,color:#000
    style L4 fill:#9b6fc3,stroke:#6b3f93,color:#fff
    style L5 fill:#b590d1,stroke:#6b3f93,color:#000
```

## Agent and Command Map

What each tool does and when it fires.

```mermaid
flowchart TB
    subgraph COMMANDS["Slash Commands — User Invoked"]
        CMD_PLAN["/plan — Architecture plan before implementing"]
        CMD_HANDOFF["/handoff — Write session handoff note"]
        CMD_DECISION["/new-decision — Create ADR + DECISION_LOG row"]
        CMD_QA["/qa — Full QA sweep"]
        CMD_HEALTH["/health — Framework maintenance audit"]
        CMD_AUDIT["/audit-decisions — Cross-reference audit"]
    end

    subgraph AGENTS["Subagents — Focused Workers"]
        AGENT_QA["qa agent (lightweight)
        Tests, types, lint
        Domain checks, ADR compliance"]
        AGENT_DR["decision-reviewer (lightweight)
        Finds unrecorded decisions
        Checks ADR/log sync"]
        AGENT_FH["framework-health (lightweight)
        Context budget, log quality
        Structural integrity"]
    end

    subgraph HOOKS["Git Hooks — Automatic"]
        HOOK_PC[".githooks/pre-commit
        ruff check + format
        Staged .py files only"]
    end

    subgraph FILES["Files They Touch"]
        HANDOFF_MD["docs/HANDOFF.md"]
        ADR_DIR["docs/adr/NNNN-*.md"]
        DECISION_LOG["docs/decisions/DECISION_LOG.md"]
        EXPERIMENT["docs/decisions/EXPERIMENT_NOTES.md"]
    end

    CMD_PLAN -->|reads| DECISION_LOG
    CMD_HANDOFF -->|overwrites| HANDOFF_MD
    CMD_DECISION -->|creates| ADR_DIR
    CMD_DECISION -->|adds row| DECISION_LOG
    CMD_QA -->|invokes| AGENT_QA
    CMD_HEALTH -->|invokes| AGENT_FH
    AGENT_FH -->|reads| DECISION_LOG
    AGENT_FH -->|reads| ADR_DIR
    AGENT_FH -->|reads| HANDOFF_MD
    CMD_AUDIT -->|uses| AGENT_DR
    CMD_AUDIT -->|appends findings| EXPERIMENT
    AGENT_DR -->|reads| ADR_DIR
    AGENT_DR -->|reads| DECISION_LOG
    HOOK_PC -.->|blocks commit if fail| COMMITNODE([git commit])

    style COMMANDS fill:#50b87a,stroke:#2d7a4f,color:#000
    style AGENTS fill:#4a90d9,stroke:#2c5f99,color:#fff
    style HOOKS fill:#e8a735,stroke:#b07d1a,color:#000
    style FILES fill:#e0e0e0,stroke:#999,color:#000
```

## Bootstrap: New Project Setup

How a new developer goes from zero to a fully configured project.

```mermaid
flowchart TD
    DEV([Developer]) --> INSTALL["Install Copier
    pip install copier (or uvx)"]
    INSTALL --> RUN["copier copy https://github.com/your-org/agentic-framework my-project"]

    RUN --> PROMPT_NAME["Prompt: project_name
    e.g. my-cool-app"]
    PROMPT_NAME --> PROMPT_DESC["Prompt: project_description
    One-line summary"]
    PROMPT_DESC --> PROMPT_AUTHOR["Prompt: author
    (optional, default blank)"]
    PROMPT_AUTHOR --> PROMPT_ARCH{"Prompt: archetype?"}

    PROMPT_ARCH -->|Python| PY_PROMPTS["Prompt: python_version (3.12)
    Prompt: python_package_name (auto)"]
    PROMPT_ARCH -->|.NET| DN_PROMPTS["Prompt: dotnet_version (8.0)"]
    PROMPT_ARCH -->|Generic| GEN_SKIP["No extra prompts"]

    PY_PROMPTS --> RENDER
    DN_PROMPTS --> RENDER
    GEN_SKIP --> RENDER

    subgraph RENDER["Template Rendering"]
        direction TB
        JINJA["Render 6 Jinja templates
        CLAUDE.md, README.md,
        pre-commit hook, QA agent,
        FRAMEWORK_VERSION.md,
        DECISION_LOG.md"]
        STATIC["Copy 16 static files
        Agents, commands, docs,
        MEMORY.md, CONTEXT_GUIDE.md,
        GLOSSARY.md, PROTOCOL.md ..."]
        JINJA ~~~ STATIC
    end

    RENDER --> POST

    subgraph POST["Post-Generation Tasks"]
        direction TB
        T1["chmod +x .githooks/pre-commit"] --> T2["git init"]
        T2 --> T3["git config core.hooksPath .githooks"]
        T3 --> T4["git add ."]
        T4 --> T5["git commit -m 'Initial project
        from agentic-coding-framework v0.1.0'"]
    end

    POST --> READY

    subgraph READY["Ready to Work"]
        direction TB
        R1["22 files, git initialized,
        hooks active, version stamped"]
        R2["Open with agentic coding tool"]
        R3["Agent reads CLAUDE.md (L0)
        and MEMORY.md (L1) automatically"]
        R4["Run /plan to start first feature"]
        R1 --> R2 --> R3 --> R4
    end

    style PROMPT_ARCH fill:#4a90d9,stroke:#2c5f99,color:#fff
    style PY_PROMPTS fill:#50b87a,stroke:#2d7a4f,color:#000
    style DN_PROMPTS fill:#4a90d9,stroke:#2c5f99,color:#fff
    style GEN_SKIP fill:#e0e0e0,stroke:#999,color:#000
    style RENDER fill:#e8a735,stroke:#b07d1a,color:#000
    style POST fill:#9b6fc3,stroke:#6b3f93,color:#fff
    style READY fill:#50b87a,stroke:#2d7a4f,color:#000
```

### What Gets Generated (by archetype)

```mermaid
flowchart LR
    subgraph SHARED["Shared Across All Archetypes (16 static files)"]
        direction TB
        AG["Agents
        decision-reviewer.md
        framework-health.md"]
        CMD["Commands
        /plan, /handoff, /new-decision
        /audit-decisions, /qa, /health"]
        DOCS["Docs
        CONTEXT_GUIDE.md
        FRAMEWORK_DIAGRAM.md
        GLOSSARY.md, HANDOFF.md"]
        DEC["Decisions
        PROTOCOL.md
        COMMIT_CONVENTION.md"]
        ADR["ADR
        TEMPLATE.md"]
        MEM["MEMORY.md"]
    end

    subgraph PYTHON["Python Archetype"]
        direction TB
        PY_CLAUDE["CLAUDE.md
        Python 3.12+, pytest, ruff, mypy
        snake_case, type hints, docstrings"]
        PY_HOOK["pre-commit
        ruff check + ruff format
        via uv"]
        PY_QA["QA Agent
        uv run pytest
        uv run mypy
        uv run ruff check"]
        PY_README["README.md
        uv sync"]
    end

    subgraph DOTNET[".NET Archetype"]
        direction TB
        DN_CLAUDE["CLAUDE.md
        .NET 8.0, xUnit
        PascalCase, XML docs"]
        DN_HOOK["pre-commit
        dotnet format --verify-no-changes"]
        DN_QA["QA Agent
        dotnet test
        dotnet build /warnaserror
        dotnet format"]
        DN_README["README.md
        dotnet restore"]
    end

    subgraph GENERIC["Generic Archetype"]
        direction TB
        GN_CLAUDE["CLAUDE.md
        (fill in your tech stack)
        (add your conventions)"]
        GN_HOOK["pre-commit
        placeholder — add your checks"]
        GN_QA["QA Agent
        placeholder commands
        customize per language"]
        GN_README["README.md
        (see your package manager)"]
    end

    SHARED --- PYTHON
    SHARED --- DOTNET
    SHARED --- GENERIC

    style SHARED fill:#e0e0e0,stroke:#999,color:#000
    style PYTHON fill:#50b87a,stroke:#2d7a4f,color:#000
    style DOTNET fill:#4a90d9,stroke:#2c5f99,color:#fff
    style GENERIC fill:#9b6fc3,stroke:#6b3f93,color:#fff
```

## Decision Recording Flow

What happens when you run `/new-decision`.

```mermaid
sequenceDiagram
    participant H as Human
    participant CC as Coding Agent
    participant FS as Filesystem
    participant G as Git

    H->>CC: /new-decision
    CC->>FS: Read docs/adr/ (find next number)
    CC->>FS: Read docs/adr/TEMPLATE.md
    CC->>H: What is the decision? Options considered?
    H->>CC: Decision context
    CC->>FS: Write docs/adr/NNNN-title.md
    CC->>FS: Add row to DECISION_LOG.md
    CC->>H: Here is the commit message — review?
    H->>CC: Looks good
    CC->>G: git add + commit (with decision trailer)
    Note over G: Pre-commit hook runs ruff check + format
    G-->>CC: Commit succeeds
    CC->>H: Done. ADR-NNNN created.
```
