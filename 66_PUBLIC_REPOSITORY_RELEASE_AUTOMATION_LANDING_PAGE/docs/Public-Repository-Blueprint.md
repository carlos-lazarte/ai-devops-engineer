# Public Repository Blueprint

## Target repository

Recommended repository name: `ai-devops-engineer`

The v3.14 package does **not** create or publish a GitHub repository automatically. The target repository must be created in the user's GitHub account or organization, then this distribution can be pushed to it.

## Recommended structure

```text
ai-devops-engineer/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
├── 00_START_HERE/ ... 65_PUBLIC_DEMO_GITHUB_COMMUNITY_EDITION/
├── 66_PUBLIC_REPOSITORY_RELEASE_AUTOMATION_LANDING_PAGE/
├── site/
├── README.md
├── LICENSE
├── SECURITY.md
└── VERSION
```

## First publication

```bash
cd ai-devops-engineer
git init
git add .
git commit -m "chore: publish AI DevOps Engineer Community Edition v3.14.0"
git branch -M main
git remote add origin https://github.com/OWNER/REPO.git
git push -u origin main
```

Then enable GitHub Pages with **GitHub Actions** as the publishing source. The included Pages workflow deploys the `site/` directory.

## Before making the repository public

Run:

```bash
make public-check
make test
make demo
make release-check
```

Review the generated `dist/` archive, secrets scan output, dependency licenses and trademark/branding terms before publication.

## Security boundary

Public distribution does not imply production authorization:

```text
GitHub
  ↓
Community source
  ↓
Runtime
  ↓
Policy / Identity
  ↓
Human approval
  ↓
Execution
```

The Community Edition remains read-only at infrastructure connectors and does not enable autonomous production remediation.
