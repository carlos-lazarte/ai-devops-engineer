# Skill Package Format

A Skill package is an immutable archive containing at minimum:

```text
skill.yaml
README.md
CHANGELOG.md
contracts/
templates/
prompts/
policies/
evaluation/
tests/
checksums.sha256
signature metadata
```

The package must not contain credentials, live environment state, local `.env` files, or mutable caches.

## Reproducibility

The package should be generated from a clean checkout. Generated artifacts are checksummed; the release manifest records the source revision and package digest.
