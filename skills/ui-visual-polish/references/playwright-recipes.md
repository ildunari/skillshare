# Playwright MCP Recipes

Patterns for reliable, token-efficient UI iteration.

## Viewport switching

Desktop:
```js
async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 720 });
  return { ok: true };
}
```

Mobile:
```js
async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  return { ok: true };
}
```

## SPA settle wait

```js
async ({ page }) => {
  await page.waitForLoadState("domcontentloaded");
  try {
    await page.waitForLoadState("networkidle", { timeout: 1500 });
  } catch (e) {
    // ignore: network never fully idles on many SPAs
  }
  await page.waitForTimeout(200);
  return { ok: true };
}
```

## Element-focused screenshots

By selector:
```js
async ({ page }) => {
  const sel = "REPLACE_ME";
  const out = ".ui-visual-polish/element.png";
  await page.locator(sel).first().screenshot({ path: out });
  return { saved: out };
}
```

By role + text:
```js
async ({ page }) => {
  const out = ".ui-visual-polish/cta.png";
  const cta = page.getByRole("button").filter({ hasText: /get started|sign up|start/i }).first();
  await cta.screenshot({ path: out });
  return { saved: out };
}
```

## Highlight overlay (debugging)

Injects a pink outline to confirm you're targeting the right element:

```js
async ({ page }) => {
  const selector = "REPLACE_ME";
  await page.evaluate((sel) => {
    const el = document.querySelector(sel);
    if (!el) return;
    el.setAttribute("data-vdi-highlight", "true");
    const styleId = "vdi-highlight-style";
    if (!document.getElementById(styleId)) {
      const st = document.createElement("style");
      st.id = styleId;
      st.textContent = `
        [data-vdi-highlight="true"] {
          outline: 3px solid rgba(255, 0, 120, 0.8) !important;
          outline-offset: 3px !important;
        }
      `;
      document.head.appendChild(st);
    }
  }, selector);
  return { ok: true };
}
```

## Baseline pulse check

Quick page-level metrics:
```js
() => {
  const d = document.documentElement;
  return {
    url: location.href,
    title: document.title,
    vw: innerWidth,
    vh: innerHeight,
    overflowX: d.scrollWidth - d.clientWidth,
    overflowY: d.scrollHeight - d.clientHeight,
  };
}
```

## Best practices

- Prefer `browser_evaluate` returning numbers + short strings over full snapshots.
- Keep candidate lists to top 5–10 items.
- Save screenshots to disk and report paths rather than inlining.
- Use one tab and reuse it; only open extra tabs for comparing routes.
