# Release Automation

The repository follows semantic version tags such as `v3.14.0`. GitHub's release workflow is triggered by a `v*` tag, validates the public distribution, builds the deterministic ZIP, calculates SHA-256, and creates a GitHub Release with the ZIP and checksum as assets. GitHub documents `gh release create` as a supported way to create releases.

## Local release preparation

```bash
python3 66_PUBLIC_REPOSITORY_RELEASE_AUTOMATION_LANDING_PAGE/scripts/release_prepare.py --root .
```

Or:

```bash
make release-check
make package
```

## Publishing a release

After pushing the commit and tag:

```bash
git tag -a v3.14.0 -m "AI DevOps Engineer v3.14.0"
git push origin v3.14.0
```

The release workflow creates the release and uploads:

```text
AI-DevOps-Engineer-Vault-v3.14.0.zip
AI-DevOps-Engineer-Vault-v3.14.0.zip.sha256
```

## Container publication

A separate workflow can publish the Community runtime image to `ghcr.io/OWNER/REPO`. GitHub documents the Container registry and GitHub Actions based image publication flow. The workflow uses the repository's `GITHUB_TOKEN` with `packages: write`.

The image publication workflow is intentionally disabled for non-release branches and tags.

## Action pinning

The reference workflows use maintained major-version action references for readability. For high-assurance enterprise use, pin third-party actions to full commit SHAs and review them during dependency updates. GitHub documents SHA pinning as the immutable reference option.
