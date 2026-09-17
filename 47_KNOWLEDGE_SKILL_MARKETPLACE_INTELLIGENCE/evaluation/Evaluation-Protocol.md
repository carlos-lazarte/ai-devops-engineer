# Evaluation Protocol

The golden set checks whether the intended Skill ranks first for representative tasks. It does not prove that the selected Skill will solve the task correctly.

Run:

```bash
PYTHONPATH=47_KNOWLEDGE_SKILL_MARKETPLACE_INTELLIGENCE python3 -m pytest -q 47_KNOWLEDGE_SKILL_MARKETPLACE_INTELLIGENCE/tests
```

For every candidate, record:

- score
- matched terms
- environment compatibility
- lifecycle status
- policy decision

Future embedding-backed discovery must preserve the same result schema and provenance fields so regressions remain comparable.
