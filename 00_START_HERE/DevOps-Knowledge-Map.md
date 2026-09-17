---
type: map
domain: devops
status: active
tags:
  - knowledge-map
  - devops
---

# DevOps Knowledge Map

```text
DEVOPS
├── Linux
├── Networking
├── Containers
│   └── Kubernetes
├── Cloud
├── Infrastructure as Code
├── Configuration Management
├── CI/CD
├── Observability
├── SRE
├── Security
├── Databases
├── Storage
└── AI for DevOps
    ├── LLM usage
    ├── Prompt engineering
    ├── Incident analysis
    ├── RAG
    ├── Agents
    └── MCP
```

## Cross-domain relationships

- Kubernetes ↔ Networking ↔ Observability
- Terraform ↔ Cloud ↔ Security
- CI/CD ↔ Kubernetes ↔ Git
- Incidents ↔ Observability ↔ SRE ↔ Postmortems
- AI ↔ Troubleshooting ↔ Documentation ↔ Runbooks

Use this page as the entry point for future links, not as a replacement for detailed notes.


## Knowledge Graph & Context Intelligence

The Vault can be indexed as a derived graph. Use `48_KNOWLEDGE_GRAPH_CONTEXT_INTELLIGENCE/` to build a deterministic graph from Markdown links and to create graph-aware context packets for AI workflows.

```text
Task
 ↓
Graph + lexical retrieval
 ↓
Relevant knowledge / evidence
 ↓
Relevant Skills
 ↓
Policy + provenance
 ↓
Context Packet
```
