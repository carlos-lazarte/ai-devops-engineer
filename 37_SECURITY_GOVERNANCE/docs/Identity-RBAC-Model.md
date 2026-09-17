# Identity & RBAC Model

| Role | Primary purpose | Maximum baseline risk |
|---|---|---|
| viewer | knowledge retrieval | low |
| analyst | analysis and draft generation | medium |
| operator | approved change proposals | high |

The role is a request attribute supplied by the authenticated integration layer. The policy engine must not trust role claims that have not been validated by an external identity provider in a production deployment.
