# Skill Discovery Policy

Discovery may use task text, requested environment, domain, risk, and explicit capability requirements. Discovery must not use secrets or privileged credentials.

## Ranking signals

The reference score is a weighted sum of:

- capability term overlap
- skill name/domain overlap
- task-description overlap
- environment compatibility
- required-tool availability
- lifecycle status

Scores are only used to order candidates; they are not authorization decisions.

## Policy outcomes

- `eligible`: candidate can proceed to compatibility/dependency checks.
- `blocked`: candidate is excluded by policy.
- `incompatible`: candidate cannot satisfy declared platform/environment requirements.
- `dependency_failed`: candidate requires an unavailable or incompatible dependency.
