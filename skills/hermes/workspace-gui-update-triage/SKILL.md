---
name: workspace-gui-update-triage
description: Diagnose and update Hermes GUI/workspace apps on the Mac Studio. Use when the user asks whether Hermes GUIs are installed/enabled, mentions Hermes Workspace, Hermes Desktop, Hermes WebUI/Swift Mac, GUI launch agents, or asks to check/update Hermes desktop/workspace apps. Covers distinguishing running launch agents from merely remembered apps, updating ~/.hermes/hermes-workspace safely, preserving local tweaks with a stash, resolving common workspace merge conflicts, rebuilding, restarting only the workspace launch agent, and checking native macOS release-only apps without installing unless asked.
targets: [hermes-default, hermes-gpt, claude-hermes]
---

# Hermes Workspace / GUI Update Triage

Use this for Mac Studio Hermes GUI checks and updates. The important distinction is **enabled/running** versus **available upstream** versus **remembered from a prior install attempt**.

## What counts as enabled

Treat a GUI as enabled only if there is live local evidence:

- a launch agent such as `ai.hermes.workspace`
- a running GUI/web process
- an installed `.app` bundle under `/Applications`, `/Applications/Coding`, `~/Applications`, `~/LocalDev`, or `~/.hermes`
- a local repo/service wired into launchd

Do not assume Hermes Desktop is installed just because prior sessions mention it. Verify app bundles and launch agents first.

## Discovery commands

```bash
launchctl list | egrep -i 'hermes|workspace|desktop|webui' || true
ps axww -o pid=,comm=,args= | egrep -i 'Hermes|hermes|workspace|webui' | egrep -v 'egrep|hermes gateway' || true

python3 - <<'PY'
from pathlib import Path
bases = [Path('/Applications'), Path('/Applications/Coding'), Path.home()/'Applications', Path.home()/'LocalDev', Path.home()/'.hermes']
for base in bases:
    if not base.exists():
        continue
    for p in base.rglob('*.app'):
        s = str(p).lower()
        if any(x in s for x in ['hermes', 'workspace', 'webui']):
            print(p)
PY
```

For the Workspace service specifically:

```bash
plutil -p ~/Library/LaunchAgents/ai.hermes.workspace.plist
launchctl print gui/$(id -u)/ai.hermes.workspace | egrep 'state =|pid =|last exit code|working directory' || true
```

## Check update availability

### Hermes Workspace

Workspace lives at:

```text
~/.hermes/hermes-workspace
```

Check it like a normal git web app:

```bash
cd ~/.hermes/hermes-workspace
git status --short --branch
git remote -v
git fetch --prune origin
git status --short --branch
git log --oneline HEAD..origin/$(git rev-parse --abbrev-ref HEAD) | head -20
```

If it is behind, update it. Local changes are common; stash them first.

### Hermes Desktop and Swift Mac/WebUI wrappers

These are native release apps, not the Workspace launch agent. Check GitHub releases, but only install/update if there is an existing app bundle or the user asked to install it.

```bash
python3 - <<'PY'
import json, urllib.request
for repo in ['dodo-reach/hermes-desktop', 'hermes-webui/hermes-swift-mac']:
    data = json.load(urllib.request.urlopen(f'https://api.github.com/repos/{repo}/releases/latest', timeout=15))
    print(repo, data.get('tag_name'), data.get('published_at'))
    for asset in data.get('assets', [])[:5]:
        print(' ', asset.get('name'), asset.get('browser_download_url'))
PY
```

If Hermes Desktop is not installed as `/Applications/HermesDesktop.app` or similar, report it as **not currently enabled**, even if a latest release exists.

## Safe Workspace update flow

1. Preserve local changes before pulling.

```bash
cd ~/.hermes/hermes-workspace
git stash push -u -m "pre-workspace-update-$(date +%Y%m%d-%H%M%S)"
```

2. Fast-forward only.

```bash
git pull --ff-only origin main
```

3. Install and build with the repo's lockfile.

```bash
if [ -f pnpm-lock.yaml ]; then
  corepack pnpm install --frozen-lockfile
  corepack pnpm run build
elif [ -f package-lock.json ]; then
  npm ci
  npm run build
else
  npm install
  npm run build
fi
```

4. If the build fails with conflict markers, inspect `git status`. In this repo, stashed local tweaks can auto-apply during/after update and leave `UU` files even after the pull succeeds. Resolve deliberately; do not retry the build blindly.

Common conflict pattern from this machine:

- `src/routes/api/models.ts`: prefer local `BEARER_TOKEN` + `HERMES_API` wiring over stale `HERMES_API_URL` symbols if the current file exports `HERMES_API`.
- `src/routes/api/skills.ts`: preserve dashboard-aware `getCapabilities()`, `dashboardFetch()`, `BEARER_TOKEN`, and `HERMES_API` logic.
- `src/server/gateway-capabilities.ts`: prefer portable chat mode when `/v1/chat/completions` is available; the sessions endpoint alone does not guarantee enhanced streaming.
- `src/screens/chat/components/chat-composer.tsx`: keep the curated `/api/models` picker and `/api/hermes-config` active provider/model fetch.
- `src/screens/dashboard/dashboard-screen.tsx`: watch for duplicate `sessionsAvailable` declarations after merges.

After resolving:

```bash
grep -R '<<<<<<<\|=======\|>>>>>>>' -n src || true
corepack pnpm run build
```

5. Restart only Workspace, not the Telegram/Discord gateways.

```bash
launchctl kickstart -k gui/$(id -u)/ai.hermes.workspace
```

## Verification

Run fresh verification before claiming the GUI is updated:

```bash
cd ~/.hermes/hermes-workspace
python3 - <<'PY'
import json
p=json.load(open('package.json'))
print(p.get('name'), p.get('version'))
PY
git log --oneline -1

curl -sS -m 10 -o /tmp/workspace-root.html -w 'root HTTP %{http_code} bytes %{size_download}
' http://127.0.0.1:3100/
curl -sS -m 10 -o /tmp/workspace-gateway.json -w 'gateway HTTP %{http_code} bytes %{size_download}
' http://127.0.0.1:3100/api/gateway-status
curl -sS -m 10 -o /tmp/workspace-models.json -w 'models HTTP %{http_code} bytes %{size_download}
' http://127.0.0.1:3100/api/models
launchctl print gui/$(id -u)/ai.hermes.workspace | egrep 'state =|pid =|last exit code' || true
```

A good handoff names:

- which GUIs are actually enabled
- which remembered/native GUIs are merely available upstream or absent locally
- Workspace before/after commit or package version
- build result and HTTP status checks
- any retained stash name for rollback insurance

## Pitfalls

- Do not start or restart the Hermes Telegram/Discord gateways while updating Workspace unless the task explicitly requires it.
- Do not install native Hermes Desktop/Swift Mac just because a release exists; checking for updates is not the same as installing a previously absent app.
- Do not treat GitHub release search snippets as proof of local install state.
- Do not drop the pre-update stash until the user confirms the updated Workspace behaves correctly.
