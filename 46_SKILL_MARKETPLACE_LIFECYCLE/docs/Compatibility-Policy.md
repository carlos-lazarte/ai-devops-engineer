# Skill Compatibility Policy

## Semantic versioning

Skills use `MAJOR.MINOR.PATCH`.

- MAJOR: incompatible contract or tool interface.
- MINOR: backward-compatible capability or content addition.
- PATCH: backward-compatible defect or documentation correction.

## Compatibility dimensions

A platform evaluates:

```text
skill_api_version
platform_api_version
tool_contract_versions
policy_schema_version
evaluation_schema_version
python/runtime constraints
```

## Install rule

Installation proceeds only when all mandatory compatibility checks pass. A version mismatch is not silently ignored.
