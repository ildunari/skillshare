# Skill Blocklist

List skill slugs here when they should be treated as hands-off by cleanup actions.

Rules:
- One slug per line
- Use the canonical skill directory name
- Lines starting with `#` are comments
- Bullet lines like `- skill-name` also work

What the cleanup skill should do:
- still include these skills in discovery and reporting
- mark them as protected in action and delete/archive outputs
- avoid recommending merge, rewrite, archive, or delete by default

Suggested uses:
- foundational skills you do not want auto-touched
- migration-pointer skills you want to keep intact for compatibility
- high-risk skills you want surfaced but not modified automatically

Examples:
- using-superpowers
- skillshare
- skill-lib-cleanup
