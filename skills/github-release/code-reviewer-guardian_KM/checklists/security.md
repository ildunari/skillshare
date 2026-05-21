
# Security Review Checklist

- [ ] ATS enforced; no broad NSAllowsArbitraryLoads
- [ ] Crypto: use CryptoKit/Swift Crypto; no MD5/SHA1
- [ ] Keychain items use restrictive accessibility
- [ ] No secrets in code; configuration via secure channels
- [ ] WebViews hardened (allowlists, contentMode, JS policy)
