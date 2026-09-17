# Example Context Packet

```yaml
request:
  task: "Diagnose a Kubernetes node that is NotReady"
  question: "What should be checked first?"

constraints:
  environment: "production-like"
  action_mode: "diagnostic-only"

knowledge:
  - source_path: 16_TROUBLESHOOTING/Troubleshooting-Kubernetes-Node-NotReady.md
    heading: First checks
    score: 0.91
    content: "..."

  - source_path: 17_RUNBOOKS/Runbook-Kubernetes-Node-Recovery.md
    heading: Evidence collection
    score: 0.87
    content: "..."

unknowns:
  - exact node condition
  - kubelet health
  - recent maintenance activity

required_output:
  - facts
  - evidence-backed hypotheses
  - missing evidence
  - diagnostic next steps

provenance: true
```
