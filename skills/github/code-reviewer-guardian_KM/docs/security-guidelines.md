
# Security Guidelines (Mobile)

- Enforce ATS (no broad NSAllowsArbitraryLoads). Pin or validate TLS as needed.
- Use CryptoKit/Swift Crypto; avoid MD5/SHA1 and homegrown crypto.
- Store secrets in Keychain with restrictive accessibility (WhenUnlockedThisDeviceOnly).
- Avoid logging PII/secrets; redact.
- Harden WebViews: limit JS, domain allowlists, scheme restrictions.
- Consider MASVS level mapping for mobile security requirements.
