
# Performance Review Checklist

- [ ] No N+1 queries or repeated expensive work in loops
- [ ] Long-lived formatters/caches reused
- [ ] Large images resized/decoded off main thread
- [ ] Instruments profile included for critical flows
- [ ] Memory growth monitored; no retain cycles
