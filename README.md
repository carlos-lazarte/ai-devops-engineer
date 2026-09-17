# AI DevOps Engineer — Community Edition

AI DevOps Engineer is a local-first AI/SRE operations platform that connects **knowledge, observability, incident correlation, evidence-first investigation and human-controlled action**.

> **Community Edition 3.14.0** — public-repository release automation, GitHub Pages product landing page and reproducible Community distribution.

## What you can do today

```text
Telemetry → Event Correlation → Incident Candidate
                         ↓
             Automated Investigation
                         ↓
          Evidence + Hypotheses + Unknowns
                         ↓
                Operational Dashboard
                         ↓
                 Human Approval Boundary
```

The public reference runtime is deliberately conservative: infrastructure connectors are read-only and production execution is disabled.

## 5-minute local demo

```bash
./65_PUBLIC_DEMO_GITHUB_COMMUNITY_EDITION/demo/run_demo.sh
```

No model API key is required for the deterministic demo.

## Docker

```bash
docker compose -f docker-compose.community.yml up --build
```

Then open `http://localhost:8080/`.

## Repository

Source and release material are published at:

`https://github.com/carlos-lazarte/ai-devops-engineer`

## Product path

Community is the public reference implementation. Future Pro/Enterprise capabilities are described as roadmap/customer-discovery scope; they are not represented as currently available features.

## Safety model

```text
Evidence → Reasoning → Planning → Policy / Identity → Human Approval → Execution → Verification
```

The model is not the authorization layer. Connector credentials do not grant remediation permission.

## License

Community Edition source is packaged under Apache-2.0. Review dependency licenses before redistribution. Project name and branding remain separate from the software license.

## Status

Reference implementation and product-development base. Validate deployment-specific security, capacity, compliance and integrations before production use.
