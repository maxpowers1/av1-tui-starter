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

    WORK --> IMPLEMENT["Implement
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

    style HOOK fill:#e8a735,stroke:#333,color:#000
    style QA fill:#4a90d9,stroke:#333,color:#fff
    style NEW_DECISION fill:#50b87a,stroke:#333,color:#000
    style HANDOFF fill:#9b6fc3,stroke:#333,color:#fff
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
        CMD_HANDOFF["/handoff — Write session handoff note"]
        CMD_DECISION["/new-decision — Create ADR + DECISION_LOG row"]
        CMD_QA["/qa — Full QA sweep"]
        CMD_AUDIT["/audit-decisions — Cross-reference audit"]
    end

    subgraph AGENTS["Subagents — Focused Workers"]
        AGENT_QA["qa agent (sonnet)
        Tests, types, lint
        Domain checks, ADR compliance"]
        AGENT_DR["decision-reviewer agent (sonnet)
        Finds unrecorded decisions
        Checks ADR/log sync"]
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

    CMD_HANDOFF -->|overwrites| HANDOFF_MD
    CMD_DECISION -->|creates| ADR_DIR
    CMD_DECISION -->|adds row| DECISION_LOG
    CMD_QA -->|invokes| AGENT_QA
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

## Decision Recording Flow

What happens when you run `/new-decision`.

```mermaid
sequenceDiagram
    participant H as Human
    participant CC as Claude Code
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
