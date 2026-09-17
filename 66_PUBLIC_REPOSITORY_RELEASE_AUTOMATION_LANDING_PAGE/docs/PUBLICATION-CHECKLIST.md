# Publication Checklist — v3.14.0

This checklist turns the package into a real public GitHub repository. It does not publish anything by itself.

## 1. Create the repository

Recommended name: `ai-devops-engineer`. Set the repository to **Public** when you are ready to expose the Community Edition.

## 2. Configure the repository URL

```bash
python3 66_PUBLIC_REPOSITORY_RELEASE_AUTOMATION_LANDING_PAGE/scripts/configure_repo.py OWNER/REPO
```

Also replace the OCI source label in `35_RUNTIME/Dockerfile` if desired.

## 3. Validate locally

```bash
make validate
make test
make public-check
make release-check
make site-check
make demo
```

## 4. First push

```bash
git init
git add .
git commit -m "chore: publish Community Edition v3.14.0"
git branch -M main
git remote add origin https://github.com/OWNER/REPO.git
git push -u origin main
```

## 5. GitHub Pages

Open **Settings → Pages** and select **GitHub Actions** as the publishing source. The `pages.yml` workflow deploys the static `site/` directory.

## 6. Release

```bash
git tag -a v3.14.0 -m "AI DevOps Engineer v3.14.0"
git push origin v3.14.0
```

The release workflow validates the tag/version match, runs release-aligned tests, builds the ZIP/checksum and creates the GitHub Release.

## 7. Container registry

The container workflow publishes the Community runtime to GHCR when a GitHub Release is published. After the first package publication, review the package visibility and set it to public only when the Community distribution is intended to be publicly pullable.

## 8. Final public review

Check the public repository for: secrets, customer data, internal hostnames, private URLs, accidental generated state, unsupported product claims, dependency licenses and branding/trademark language.
