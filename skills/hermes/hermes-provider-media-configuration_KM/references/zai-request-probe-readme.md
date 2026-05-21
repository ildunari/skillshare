# Z.ai / Ralph request-dump probe

Use this when GLM/Z.ai appears to fail only during heavy Hermes agent/browser runs.

```bash
python3 scripts/zai_request_probe.py
```

The script intentionally does not print API keys. It checks:

- model catalog reachability
- tiny GLM-5.1 completion
- GLM-5.1 with `thinking.disabled`
- GLM-5-turbo with `thinking.disabled`
- a moderate/large prompt with tools

Treat this as a provider health probe only. If it passes but Hermes BrowserAgent still fails, inspect BrowserAgent env/config and request dumps before blaming Z.ai.
