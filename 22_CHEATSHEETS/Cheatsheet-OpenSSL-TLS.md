---
type: reference
domain: security
difficulty: beginner
status: active
tags: [cheatsheet, security]
---
# Cheatsheet-OpenSSL-TLS

```bash
openssl s_client -connect host:443 -servername host -showcerts
openssl x509 -in cert.pem -noout -subject -issuer -dates -ext subjectAltName
```

Always review context and impact before running commands in production.
