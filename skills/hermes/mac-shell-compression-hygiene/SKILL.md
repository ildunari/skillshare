---
name: hermes-mac-shell-compression-hygiene
description: Diagnose and fix noisy non-interactive Mac Studio shells used by Hermes/SSH, especially bashrc readline warnings, blocked direnv .envrc messages, SSH channel noise triage, and Hermes compression threshold warnings. Use when Kosta shows shell startup warnings like bind line editing not enabled, direnv .envrc is blocked, or Hermes auto-lowers compression threshold.
version: 0.1.0
author: Hermes Agent
license: MIT
targets: [hermes-default, hermes-gpt]
---

# Hermes Mac shell + compression hygiene

Use this when a Hermes/SSH command succeeds but the output is polluted by shell startup warnings, or when Hermes warns that the compression model context is smaller than the configured threshold.

## What the common warnings mean

- `bind: warning: line editing not enabled` means `.bashrc` loaded readline keybindings in a non-interactive shell. Common culprits: fzf key bindings, bash-completion, Atuin, or hand-written `bind` calls.
- `direnv: error ... .envrc is blocked` means the repo `.envrc` has not been allowlisted. It does not necessarily mean the command failed.
- `channel X: open failed: connect failed: open failed` is usually SSH forwarding/tunnel noise from the client side. Do not treat it as a Hermes failure unless the failing forwarded port was part of the task.
- `Compression model (...) context is ... but threshold was ...` means compression would trigger after the compression model can no longer fit the context. Fix the config permanently instead of relying on the per-session auto-lowered threshold.

## Fix `.bashrc` readline noise safely

Do not remove interactive conveniences. Gate them behind `[[ $- == *i* ]]` so they still load in real terminals but not in script/SSH command shells.

Typical safe shape:

```bash
if [[ $- == *i* ]] && command -v direnv >/dev/null 2>&1; then
  eval "$(direnv hook bash)"
fi

if [[ $- == *i* ]] && command -v zoxide >/dev/null 2>&1; then
  eval "$(zoxide init bash)"
fi

if [[ $- == *i* ]]; then
  if [ -n "${HOMEBREW_PREFIX:-}" ] && [ -r "${HOMEBREW_PREFIX}/opt/fzf/shell/completion.bash" ]; then
    . "${HOMEBREW_PREFIX}/opt/fzf/shell/completion.bash"
  fi
  if [ -n "${HOMEBREW_PREFIX:-}" ] && [ -r "${HOMEBREW_PREFIX}/opt/fzf/shell/key-bindings.bash" ]; then
    . "${HOMEBREW_PREFIX}/opt/fzf/shell/key-bindings.bash"
  fi
  if [ -n "${HOMEBREW_PREFIX:-}" ] && [ -r "${HOMEBREW_PREFIX}/etc/profile.d/bash_completion.sh" ]; then
    . "${HOMEBREW_PREFIX}/etc/profile.d/bash_completion.sh"
  fi
fi
```

Also gate Atuin. It emits a large bash integration containing `bind` calls:

```bash
if [[ $- == *i* ]] && command -v atuin >/dev/null 2>&1; then
  eval "$(atuin init bash)"
fi
```

If a `bind` warning persists, trace the startup once:

```bash
bash -lx -c 'true' 2>/tmp/bash_trace.txt || true
grep -n "bind" /tmp/bash_trace.txt | tail -20
```

This identifies the sourced integration that still runs in non-interactive shells.

## Fix blocked direnv for Hermes repo

Only allow `.envrc` after reading it. For the Hermes repo, the observed `.envrc` watches project files and runs `use flake`.

```bash
cd ~/.hermes/hermes-agent
sed -n '1,120p' .envrc
direnv allow
```

Verify:

```bash
cd ~/.hermes/hermes-agent
direnv status | grep -E 'Found RC path|Found RC allowed'
```

## Fix Hermes compression warning permanently

For GPT profile on this Mac Studio, edit:

```text
~/.hermes/profiles/gpt/config.yaml
```

Set threshold to `0.90` when the main context is 300,000 and the compression model fits 272,000 tokens:

```yaml
compression:
  threshold: 0.90
```

This triggers compression at 270,000 tokens, below the compression model limit.

Optional: keep the auxiliary compression model explicit if needed:

```yaml
auxiliary:
  compression:
    provider: auto
    model: gpt-5.4-mini
    timeout: 120
```

Do not guess context lengths. Read the active profile config and verify the math.

## Verification

Before saying the issue is fixed, run:

```bash
out=$(bash -lc 'cd ~/.hermes/hermes-agent && true' 2>&1); ec=$?; printf '%s' "$out"; printf '\nEXIT=%s\n' "$ec"; test -z "$out"
```

Expected: no output before `EXIT=0`, and `test -z "$out"` passes.

Verify compression math:

```bash
python3 - <<'PY'
import yaml
from pathlib import Path
p = Path('/Users/Kosta/.hermes/profiles/gpt/config.yaml')
data = yaml.safe_load(p.read_text())
threshold = data['compression']['threshold']
main_ctx = data['model']['context_length']
print('threshold', threshold)
print('main_context', main_ctx)
print('trigger_tokens', int(main_ctx * threshold))
print('under_272000', int(main_ctx * threshold) <= 272000)
PY
```

Expected for current GPT profile: threshold `0.9`, trigger tokens `270000`, under limit `True`.

## Pitfalls

- Do not gate all of `.bashrc` behind interactivity; environment variables and aliases may still be expected. Gate only shell integrations that install hooks/completions/keybindings.
- Do not run `direnv allow` blindly on unknown repos. Read `.envrc` first.
- Do not interpret successful gateway restart output as failed just because SSH/channel warnings appeared above it. Look for the command’s own success/failure lines.
- Compression threshold is per profile. Fix `~/.hermes/profiles/gpt/config.yaml` for GPT; the default profile has its own config.
