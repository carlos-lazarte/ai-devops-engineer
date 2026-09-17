# Marketplace Quickstart

## Validate a Skill

```bash
python 46_SKILL_MARKETPLACE_LIFECYCLE/cli/skillctl.py validate 46_SKILL_MARKETPLACE_LIFECYCLE/skills/kubernetes-troubleshooting/skill.yaml
```

## Reference installation flow

```text
Registry
  ↓
fetch metadata
  ↓
verify signature + checksum
  ↓
compatibility gate
  ↓
policy gate
  ↓
install
  ↓
post-install evaluation
```

The quickstart does not execute package code automatically.
