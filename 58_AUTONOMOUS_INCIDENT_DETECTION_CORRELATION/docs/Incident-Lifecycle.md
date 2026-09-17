# Incident Candidate Lifecycle

```text
NEW
 ↓
CORRELATING
 ↓
CANDIDATE
 ├──────────────→ SUPPRESSED
 ├──────────────→ MERGED
 ↓
TRIAGED
 ↓
INVESTIGATING
 ↓
CLOSED
```

`CANDIDATE` means a correlation exists but incident confirmation is not established.

`SUPPRESSED` is policy-driven noise handling. `MERGED` records that a candidate was folded into another candidate while preserving provenance.
