#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

fail=0

# Forbidden generated or local state. Python/test caches are ignored because CI and local test runs may create them.
while IFS= read -r p; do
  echo "FORBIDDEN FILE: $p"
  fail=1
done < <(find . -type f \
  \( -name '.env' -o -name 'local.db' -o -name 'audit.jsonl' \) \
  -not -path './.git/*' \
  -not -path '*/.venv/*' \
  -not -path '*/runtime-data/*' \
  -print)

# Common credential signatures. Variable names alone are allowed; populated credential material is not.
if grep -RIE --exclude-dir=.git --exclude-dir=.venv --exclude='*.md' --exclude='public-check.sh' \
  -n '(sk-ant-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16})' . >/tmp/aiops-secret-scan.out 2>/dev/null; then
  cat /tmp/aiops-secret-scan.out
  fail=1
fi

# Ensure the public release has the expected control files.
for required in README.md LICENSE NOTICE COMMUNITY.md SECURITY.md SUPPORT.md GOVERNANCE.md ROADMAP.md VERSION 65_PUBLIC_DEMO_GITHUB_COMMUNITY_EDITION/demo/run_demo.sh docker-compose.community.yml .github/workflows/community-ci.yml .github/workflows/release.yml .github/workflows/pages.yml 66_PUBLIC_REPOSITORY_RELEASE_AUTOMATION_LANDING_PAGE/site/index.html release-manifest.json; do
  [[ -e "$required" ]] || { echo "MISSING: $required"; fail=1; }
done

# Version is validated generically so the public check remains reusable across releases.
version="$(cat VERSION)"
[[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+([-.][0-9A-Za-z.-]+)?$ ]] || { echo "VERSION mismatch: $version"; fail=1; }

if [[ $fail -ne 0 ]]; then
  echo "PUBLIC CHECK: FAIL"
  exit 1
fi

echo "PUBLIC CHECK: PASS"
