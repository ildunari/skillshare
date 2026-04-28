---
name: hermes-webui-mobile-evaluation
description: Use when evaluating, installing, testing, or adapting nesquena/hermes-webui for phone or small-screen Hermes use. Trigger when the user asks whether Hermes WebUI works on iPhone/mobile, wants a Telegram replacement via browser/PWA, or wants to compare Hermes WebUI against the Telegram Mini App/native iOS options.
targets: [hermes-default, hermes-gpt]
---

# Hermes WebUI mobile evaluation

Use this when checking whether `nesquena/hermes-webui` is a good phone interface for Hermes or when deciding whether to deploy/fork it.

## Known read

Hermes WebUI is better treated as a full browser/PWA control surface than as a minimal phone chat client. It has serious mobile support, but it preserves a lot of CLI/WebUI parity, so the phone UI can feel dense.

Good fit:
- managing Hermes from a browser or Home Screen PWA
- sessions, tasks, skills, memory, spaces/profiles, settings, workspace files
- a hackable vanilla JS + Python web UI with no frontend build step

Less ideal fit:
- quick daily “talk to Hermes” flow replacing Telegram
- voice-first interaction
- ultra-simple one-handed chat UI

Default recommendation: test it as a richer phone control panel, but keep or build a narrower mobile-first chat surface for daily phone use.

## Fast evaluation workflow

1. Clone a temporary copy instead of guessing from the README.

```bash
rm -rf /tmp/hermes-webui
git clone --depth 1 https://github.com/nesquena/hermes-webui.git /tmp/hermes-webui
```

2. Inspect mobile-specific code paths.

Useful files:
- `/tmp/hermes-webui/static/style.css`
- `/tmp/hermes-webui/static/index.html`
- `/tmp/hermes-webui/static/boot.js`
- `/tmp/hermes-webui/tests/test_mobile_layout.py`

Search for:
- `@media(max-width:900px)` and `@media(max-width:640px)`
- `100dvh`
- `safe-area-inset-*`
- `.sidebar.mobile-open`
- `.rightpanel.mobile-open`
- `.composer-footer`
- `pointer:coarse`

3. Run the real server if possible, not just `python -m http.server`. The static file path can mislead because relative `/static/...` imports and server routes matter.

```bash
cd /tmp/hermes-webui
HERMES_WEBUI_PORT=9192 HERMES_WEBUI_HOST=127.0.0.1 python3 server.py
curl -i -s --max-time 5 http://127.0.0.1:9192/ | sed -n '1,10p'
```

If you start it in the background, kill it after the review.

4. Use browser/CDP mobile emulation for a quick structural check.

Set an iPhone-like viewport, e.g. `390x844` with device scale factor 3, then evaluate layout metrics:

```js
(()=>{
  const sels=['.rail','.sidebar','.rightpanel','.composer-footer','.composer-box','.app-titlebar','.main','.layout'];
  let out={vw:innerWidth,vh:innerHeight,scrollW:document.documentElement.scrollWidth,bodyScrollW:document.body.scrollWidth};
  for (const sel of sels){
    const e=document.querySelector(sel);
    if(e){
      const cs=getComputedStyle(e), r=e.getBoundingClientRect();
      out[sel]={display:cs.display, position:cs.position, left:Math.round(r.left), right:Math.round(r.right), width:Math.round(r.width), height:Math.round(r.height), overflowX:cs.overflowX};
    }
  }
  return out;
})()
```

What good looked like in April 2026 at `390x844`:
- `.rail` is `display: none`
- `.sidebar` is `position: fixed`, width about `280px`, off-canvas left until opened
- `.rightpanel` is `position: fixed`, width about `300px`, off-canvas right until opened
- `.main` is full viewport width and `overflow-x: hidden`
- document/body scroll width stays at viewport width, so no page-level horizontal overflow
- composer remains visible, but has many controls packed into the footer

## Mobile quality signals found

Hermes WebUI already includes explicit mobile safeguards:
- dynamic viewport height (`100dvh`) for mobile browser chrome
- off-canvas mobile sidebar under 640px
- right file/workspace panel as mobile slide-over
- mobile overlay for tap-to-close behavior
- rail hidden on phones
- composer chips reduced to icon-only controls
- 44px-ish touch target rules
- textarea font-size safeguards against iOS zoom-on-focus
- `pointer:coarse` logic for mobile Enter/newline behavior
- a dedicated `tests/test_mobile_layout.py` static regression suite

## UX judgment

Give the user a clear distinction:

- “Does it scale down?” → yes, much better than expected.
- “Is it the best daily phone chat UI?” → not really; it is dense because it carries full Hermes control-panel functionality.

If the user wants a Telegram replacement, recommend one of two paths:
1. deploy Hermes WebUI behind Tailscale/Funnel as a Home Screen PWA for management-heavy use
2. build or keep a slimmer mobile-first chat/voice UI for daily use, borrowing WebUI’s drawer and composer patterns where useful

## Pitfalls

- Do not judge mobile behavior from a static `python -m http.server` view alone; missing server behavior can make the layout look broken or overly expanded.
- Do not confuse “responsive and fits” with “native-feeling phone UX.” Hermes WebUI fits, but it is still a dense power-user web app.
- Avoid presenting the App Store app named “Hermes Agent” as related unless verified. The generic App Store app observed in April 2026 appeared unrelated to Nous Hermes Agent.
