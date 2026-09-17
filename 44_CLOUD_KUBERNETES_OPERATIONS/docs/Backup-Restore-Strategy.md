---
type: procedure
domain: data-protection
status: active
tags:
  - backup
  - restore
  - kubernetes
---

# Backup and Restore Strategy

## State to protect

- agent memory database
- audit records
- configuration that cannot be reconstructed from Git
- RAG index artifacts if they are treated as state

## Principles

Use application-consistent backups, encrypt backups, document retention, and test restore procedures regularly.

## Recovery objective

Define RPO and RTO per deployment. Do not infer business objectives from technical defaults.

## Verification

A successful backup is not equivalent to a successful recovery. Restore tests must verify integrity, access controls, tenant boundaries and application readiness.
