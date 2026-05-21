# Backup model host routing — Qwopus to Gaming PC — 2026-05-09

Session signal: Kosta asked to “change the use from using our studio to using gaming pc for qwopus for the backup models,” while also wanting a unified direct provider surface that includes image-generation models.

## Durable lesson

For backup/local model routing, do not assume the Mac Studio is the preferred host just because Hermes is running there. When Qwopus or backup models are mentioned, check whether Kosta wants the Gaming PC endpoint instead. In this session, the desired direction was Gaming PC for Qwopus backup models, not Studio.

## Safe workflow

1. Locate the active provider/model config for the relevant profiles (`default`, `gpt`, BrowserAgent, media/image-gen if included). Do not edit from memory.
2. Search for Qwopus, backup model names, Studio hostnames/IPs, and Gaming PC/Tailscale endpoints across profile configs, `.env` files, provider registries, gateway env, and any unified provider directory.
3. Change provider/base URL/model as a unit. Avoid leaving model names pointed at a stale Studio base URL.
4. Keep image generation direct if the user asked for image-gen models to be included in the unified surface; do not route image tools through a backup LLM endpoint unless the config explicitly supports that provider.
5. Verify with a small non-spend provider smoke test where possible, then a tiny model call against the exact `HERMES_HOME`/profile being changed.

## Reporting

Say which profile(s) changed, which endpoint class now owns Qwopus backup models (Gaming PC), and what smoke test proved it. Do not print API keys or tokens from `.env` while showing evidence.
