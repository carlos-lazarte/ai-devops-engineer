# Skill Lifecycle

## States

```text
draft → candidate → verified → published → installed → deprecated → retired
```

A `published` skill has passed the publisher gate. A platform may still reject installation because of local policy, compatibility, environment, or trust requirements.

## Required gates

### Candidate → Verified
- manifest schema valid
- contract complete
- dependency declarations valid
- tools referenced by allowlist
- no forbidden capability
- unit tests pass
- evaluation threshold pass

### Verified → Published
- immutable package created
- checksum generated
- signature generated/attached
- release metadata complete

### Published → Installed
- signature trusted
- compatibility accepted
- policy accepted
- dependencies available
- target environment allowed

## Deprecation
A deprecated Skill remains installable only when local policy allows it. New production installations should normally be blocked after the deprecation deadline.
