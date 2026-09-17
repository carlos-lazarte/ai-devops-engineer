---
type: architecture
domain: ai-devops
difficulty: advanced
status: active
tags:
  - evaluation
  - rag
  - agent
---
# Evaluation Architecture

The evaluator is split into independent dimensions so a good score in one area cannot hide a failure in another.

## Dimensions

1. Retrieval quality
2. Evidence provenance
3. Reasoning structure
4. Safety / policy compliance
5. Memory quality
6. Reliability behavior

```text
Test Case
  ├── retrieval
  ├── grounding
  ├── structure
  ├── safety
  ├── memory
  └── reliability
          ↓
       Evaluator
          ↓
      Threshold Gate
```

## Important distinction

The evaluator measures an implementation against explicit criteria. It does not establish that a model is generally correct or safe in all environments.
