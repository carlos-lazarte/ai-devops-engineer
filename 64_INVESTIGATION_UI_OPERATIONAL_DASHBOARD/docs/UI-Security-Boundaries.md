# UI Security Boundaries

- UI is presentation and operator control, not policy authority.
- Browser never receives backend connector credentials.
- Connector access remains read-only.
- Investigation remains plan-only.
- Production execution is disabled in the reference runtime.
- Tenant filters are passed to server-side persistence queries; the UI must not be treated as a tenant-isolation control by itself.
- HTML output is generated from controlled JSON values and escaped before insertion into the DOM.
- Large JSON payloads are collapsed behind a readable detail panel to reduce accidental context overload.
