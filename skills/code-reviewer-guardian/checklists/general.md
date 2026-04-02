
# General Code Review Checklist

- [ ] No force unwraps/tries/casts in production paths
- [ ] Meaningful names; avoid abbreviations
- [ ] Functions small & single responsibility
- [ ] Maintainable error handling (no swallowed errors)
- [ ] Tests present and passing; coverage thresholds met
- [ ] Linting and formatting clean
- [ ] Sensitive data not logged
- [ ] No excessive diff noise (unrelated reformatting)
