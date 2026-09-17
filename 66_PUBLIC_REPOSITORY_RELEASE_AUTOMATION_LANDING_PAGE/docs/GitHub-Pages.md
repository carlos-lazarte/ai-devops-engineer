# GitHub Pages

The landing page is static and lives in `66_PUBLIC_REPOSITORY_RELEASE_AUTOMATION_LANDING_PAGE/site/`. The included workflow uploads that directory as a GitHub Pages artifact and deploys it.

GitHub documents GitHub Pages deployment through custom GitHub Actions workflows using `actions/configure-pages`, `actions/upload-pages-artifact`, and `actions/deploy-pages`.

## Enablement

1. Push the repository to GitHub.
2. Open repository **Settings → Pages**.
3. Set the publishing source to **GitHub Actions**.
4. Push to `main`; the workflow deploys the site.

Before publication, replace the placeholder repository URL in `site/config.js` with the actual `https://github.com/OWNER/REPO` URL.
