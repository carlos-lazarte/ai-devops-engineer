# Agent Memory & Stateful Operations

Version 1.8.0 adds a controlled memory layer for the AI DevOps system.

## Memory classes

- **Working memory**: state for one execution; short-lived and not promoted automatically.
- **Episodic memory**: historical incidents, decisions, and outcomes; retained with explicit lifecycle metadata.
- **Semantic memory**: curated knowledge promoted into the Vault/RAG layer after human review.

The design explicitly prevents historical observations from silently becoming permanent operating rules.

## State lifecycle

```text
TASK_CREATED
   ↓
CONTEXT_BUILT
   ↓
ANALYSIS_IN_PROGRESS
   ↓
PROPOSAL_READY
   ↓
AWAITING_APPROVAL
   ↓
APPROVED / REJECTED
   ↓
EXECUTED (when an external execution layer explicitly permits it)
   ↓
VERIFIED
   ↓
CLOSED
   ↓
EPISODIC_MEMORY_CANDIDATE
   ↓
HUMAN_REVIEW
   ↓
SEMANTIC_PROMOTION (optional)
```

## Safety boundary

Memory is evidence and context, not authorization. Policy, identity and approval layers remain authoritative.

The reference implementation in `store/` is local-only and uses SQLite. It does not execute operational commands or connect to production systems.
