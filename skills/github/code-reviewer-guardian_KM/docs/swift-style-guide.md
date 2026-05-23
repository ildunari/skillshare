
# Swift Style Guide (Synthesis)

- Follow Swift.org API Design Guidelines.
- Types: UpperCamelCase; functions/vars: lowerCamelCase; Booleans prefixed with is/has/should.
- Prefer structs for value semantics; classes for reference semantics/identity.
- Use guard for early exits; prefer immutable lets.
- Avoid force unwrap/try/cast; use optionals and throws responsibly.
- One type per file; keep files/fns short and focused.
