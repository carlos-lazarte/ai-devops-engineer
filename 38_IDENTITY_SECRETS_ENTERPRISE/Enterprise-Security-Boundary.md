# Enterprise Security Boundary

The boundary is explicit:

```text
Obsidian Vault
  ├── knowledge
  ├── procedures
  └── public/reference configuration

          X no secrets X

Enterprise Control Plane
  ├── identity
  ├── policy
  ├── secret manager
  ├── audit
  └── runtime credentials
```

This separation reduces the chance that sensitive operational material is ingested into RAG indexes or model prompts.
