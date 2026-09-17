# Ground Truth & Blind Evaluation

Ground truth contains the actual injected fault and expected resolution.

The agent should not receive the ground-truth diagnosis directly.

## Evaluation separation

```text
Ground Truth
     |
     +----> Simulator
     |
     +----> Evaluator
     |
     X----> Agent Context
```

The evaluator compares agent results to ground truth after the run.

This prevents the evaluation from becoming a self-confirming exercise.
