#!/usr/bin/env python3
"""Probe Z.ai/GLM without printing secrets.

Loads GLM/ZAI keys from active env or ~/.hermes/.env and sends small direct
OpenAI-compatible requests to Z.ai. Useful when Hermes BrowserAgent/Ralph sees
429s: if this passes, inspect Hermes/browser request shape before blaming auth.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

for env_path in [Path.home() / ".hermes/.env"]:
    if env_path.exists():
        for line in env_path.read_text(errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

API_KEY = os.getenv("GLM_API_KEY") or os.getenv("ZAI_API_KEY") or os.getenv("Z_AI_API_KEY")
BASE = os.getenv("ZAI_BASE_URL", "https://api.z.ai/api/coding/paas/v4").rstrip("/")


def request(path: str, body: dict | None = None) -> dict:
    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, headers=headers)
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            text = response.read().decode("utf-8", "replace")
            return {"ok": True, "status": response.status, "seconds": round(time.time() - start, 2), "preview": text[:700]}
    except urllib.error.HTTPError as exc:
        return {
            "ok": False,
            "status": exc.code,
            "seconds": round(time.time() - start, 2),
            "preview": exc.read().decode("utf-8", "replace")[:1000],
            "headers": {k: v for k, v in exc.headers.items() if k.lower() in {"retry-after", "x-ratelimit-limit", "x-ratelimit-remaining", "x-ratelimit-reset"}},
        }
    except Exception as exc:
        return {"ok": False, "error_type": type(exc).__name__, "error": str(exc), "seconds": round(time.time() - start, 2)}


def chat(model: str, content: str, *, thinking: dict | None = None, max_tokens: int = 256, tools: list | None = None) -> dict:
    body = {"model": model, "messages": [{"role": "user", "content": content}], "max_tokens": max_tokens, "stream": False}
    if thinking is not None:
        body["thinking"] = thinking
    if tools:
        body["tools"] = tools
    return request("/chat/completions", body)


def main() -> int:
    if not API_KEY:
        print(json.dumps({"ok": False, "error": "missing GLM_API_KEY/ZAI_API_KEY/Z_AI_API_KEY"}, indent=2))
        return 1
    tools = [{"type": "function", "function": {"name": "noop", "description": "No-op", "parameters": {"type": "object", "properties": {}}}}]
    large = "browser verification tactics " * 4000
    results = {
        "base": BASE,
        "models": request("/models"),
        "glm_5_1_tiny": chat("glm-5.1", "Reply exactly ok", max_tokens=256),
        "glm_5_1_thinking_disabled": chat("glm-5.1", "Reply exactly ok", thinking={"type": "disabled"}, max_tokens=256),
        "glm_5_turbo_thinking_disabled": chat("glm-5-turbo", "Reply exactly ok", thinking={"type": "disabled"}, max_tokens=256),
        "glm_5_1_large_tools": chat("glm-5.1", "Reply exactly ok after reading:\n" + large, max_tokens=256, tools=tools),
    }
    print(json.dumps(results, indent=2))
    return 0 if all(v.get("ok", True) for k, v in results.items() if isinstance(v, dict)) else 2


if __name__ == "__main__":
    raise SystemExit(main())
