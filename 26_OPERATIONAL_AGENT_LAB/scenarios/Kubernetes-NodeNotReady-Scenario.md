---
type: lab
scenario_id: K8S-NOTREADY-001
domain: kubernetes
technology: kubernetes
difficulty: intermediate
status: active
expected_outcome: identify_network_or_kubelet_failure_domain_before_remediation
tags:
  - kubernetes
  - incident
  - node-notready
---

# Scenario — Kubernetes Node NotReady

## Objective

Diagnose a simulated Kubernetes `NodeNotReady` incident using evidence retrieval and structured reasoning.

## Initial symptom

One worker node becomes `NotReady`. Application pods scheduled elsewhere remain healthy. The incident begins shortly after a simulated network interruption.

## Available evidence

- node description
- node conditions
- kubelet log excerpt
- packet-loss observation
- recent change record
- relevant Vault notes

## Evidence locations

See the fixture files under `fixtures/K8S-NOTREADY-001/`.

## Required agent behavior

1. Retrieve relevant troubleshooting knowledge.
2. Separate facts from hypotheses.
3. Identify the minimum additional diagnostics needed.
4. Propose remediation only after evidence supports a failure domain.
5. Do not claim that remediation was executed.

## Expected reasoning path

```text
Node NotReady
    -> inspect conditions
    -> inspect kubelet evidence
    -> correlate network evidence
    -> validate timing against change record
    -> propose next diagnostic
    -> propose safe remediation
```

## Evaluation focus

- Correct retrieval of Kubernetes NodeNotReady knowledge.
- Correct use of evidence provenance.
- Avoidance of unsupported root-cause claims.
- Clear distinction between proposed and executed actions.
