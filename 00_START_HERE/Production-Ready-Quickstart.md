---
type: reference
domain: operations
status: active
---
# Production-Ready Quickstart

Start with:

1. [[29_PRODUCTION_READINESS/Production-Readiness-Matrix]]
2. [[29_PRODUCTION_READINESS/Production-Release-Checklist]]
3. [[30_AUTOMATION/README]]

Then run:

```bash
python3 30_AUTOMATION/validate_vault.py --root .
make test
```

The release is designed to fail closed around unsafe tool access and to keep production execution disabled by default.
