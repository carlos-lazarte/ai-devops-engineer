---
type: workflow
domain: ai-agent
status: active
tags:
  - workflow
  - evaluation
---

# Operational Agent Evaluation Workflow

```text
Scenario
  -> Fixture generation
  -> Context selection
  -> Retrieval
  -> Agent reasoning
  -> Structured response
  -> Human review
  -> Metrics
  -> Evaluation record
```

## Step 1 — Prepare scenario

Use a deterministic fixture set.

## Step 2 — Build context

Include only evidence explicitly available to the agent.

## Step 3 — Retrieve knowledge

Search the Vault for the relevant troubleshooting and runbook content.

## Step 4 — Ask the agent

Require facts, observations, hypotheses, missing evidence, proposed actions, and validation.

## Step 5 — Human review

Check technical correctness and verify that no action is reported as executed unless it actually was.

## Step 6 — Record evaluation

Populate [[../schemas/evaluation-record.yaml]].

## Step 7 — Improve

Update retrieval configuration, prompts, notes, or tool policy based on measured failure modes.
