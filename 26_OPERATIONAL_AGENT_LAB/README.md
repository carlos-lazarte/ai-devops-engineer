---
type: project
domain: ai-devops
status: experimental
tags:
  - ai-agent
  - lab
  - incident-response
  - evaluation
---

# Operational Agent Lab

A safe, reproducible laboratory for testing the AI DevOps agent against simulated incidents.

## Goals

- Test retrieval + reasoning + tool selection together.
- Keep production systems completely out of scope.
- Capture evidence, hypotheses, proposed actions, and validation results.
- Evaluate the agent with repeatable scenarios rather than subjective impressions.

## Safety model

This lab is simulation-only. The included simulator writes files under a lab workspace and does not execute remediation against real infrastructure.

## First scenario

[[scenarios/Kubernetes-NodeNotReady-Scenario]]

## Workflow

[[workflows/Operational-Agent-Evaluation-Workflow]]
