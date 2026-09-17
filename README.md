# AI DevOps Engineer — Community Edition

AI DevOps Engineer is a local-first AI/SRE operations platform that connects **knowledge, observability, incident correlation, evidence-first investigation and human-controlled action**.

> **Community Edition 3.15.1** — patch release aligning the public landing configuration with the canonical repository and release version.

## What you can do today

```text
Telemetry
   ↓
Event Correlation
   ↓
Incident Candidate
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

## Public repository and release flow

The release tooling is under `66_PUBLIC_REPOSITORY_RELEASE_AUTOMATION_LANDING_PAGE/`.

```bash
make public-check
make release-check
make site-check
make package
```

GitHub Releases are created by `.github/workflows/release.yml` when a semantic version tag such as `v3.15.1` is pushed. The landing page is deployed by `.github/workflows/pages.yml`. A separate release workflow can publish the Community container to GHCR.

See `66_PUBLIC_REPOSITORY_RELEASE_AUTOMATION_LANDING_PAGE/docs/Public-Repository-Blueprint.md` and `66_PUBLIC_REPOSITORY_RELEASE_AUTOMATION_LANDING_PAGE/docs/PUBLICATION-CHECKLIST.md` for the publication sequence.

## Product landing page

The static landing page source is in `66_PUBLIC_REPOSITORY_RELEASE_AUTOMATION_LANDING_PAGE/site/`.

## Repository map

- `00_START_HERE/` — orientation and workflows
- `15_AI_FOR_DEVOPS/` — AI/SRE operating model
- `24_RAG_SEMANTIC_RETRIEVAL/` — RAG
- `35_RUNTIME/` — executable local runtime
- `51_DIGITAL_TWIN_INCIDENT_SIMULATION/` — deterministic simulation
- `58_AUTONOMOUS_INCIDENT_DETECTION_CORRELATION/` — incident correlation
- `59_EVENT_DRIVEN_AGENT_TRIGGERING_INCIDENT_COMMANDER/` — event-driven commander
- `61_REAL_TELEMETRY_EVENT_INGESTION/` — telemetry ingestion
- `62_PRODUCTION_OBSERVABILITY_CONNECTORS/` — bounded connectors
- `63_AUTOMATED_INCIDENT_INVESTIGATION/` — evidence-first investigation
- `64_INVESTIGATION_UI_OPERATIONAL_DASHBOARD/` — operational UI
- `65_PUBLIC_DEMO_GITHUB_COMMUNITY_EDITION/` — public demo and contribution tooling
- `66_PUBLIC_REPOSITORY_RELEASE_AUTOMATION_LANDING_PAGE/` — public release, Pages and product site

## Safety model

```text
Evidence
   ↓
Reasoning
   ↓
Planning
   ↓
Policy / Identity
   ↓
Human Approval
   ↓
Execution
   ↓
Verification
```

The model is not the authorization layer. A connector's credentials do not grant remediation permission.

## Community Edition vs. future commercial editions

Community is the public reference product. Future commercial editions may add enterprise authentication, deployment profiles, integrations, support and other capabilities. See `65_PUBLIC_DEMO_GITHUB_COMMUNITY_EDITION/docs/Community-vs-Enterprise.md`.

## Contributing

Read `COMMUNITY.md`, `GOVERNANCE.md`, `CODE_OF_CONDUCT.md` and `CONTRIBUTING.md` before opening a pull request.

## License

Community Edition source is packaged under Apache-2.0. Review dependency licenses before redistribution. The project name and branding remain separate from the software license.

## Status

This repository is a reference implementation and product-development base. Validate deployment-specific security, capacity, compliance and integrations in the target environment before production use.
