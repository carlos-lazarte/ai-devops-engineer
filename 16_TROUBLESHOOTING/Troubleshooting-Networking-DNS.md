---
type: troubleshooting
domain: networking
technology: DNS
difficulty: intermediate
severity: medium
status: active
tags: [networking, troubleshooting]
---
# Troubleshooting-Networking-DNS

DNS failures can involve local configuration, resolver reachability, record data, or environment-specific resolution.

## First checks
```bash
getent hosts example.com
nslookup example.com
dig example.com
```

## Evidence
Record resolver, timestamp, queried name, result code, and whether multiple clients are affected.

## Branches
1. Local configuration/search-domain issue.
2. Resolver unreachable.
3. Authoritative record issue.
4. Split-horizon/environment difference.
