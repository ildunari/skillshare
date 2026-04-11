## 6. Synthesis: theme schema + 15 theme proposals

### 6.1 A practical theme schema for AI-assisted generation

Theme generation becomes reliable when the AI fills a structured schema rather than improvising. Each theme is expressed as:

```json
{
  "meta": { "name": "ThemeName", "mood": ["..."], "density": "medium" },
  "color": {
    "space": "oklch",
    "neutrals": { "bg": "L≈0.96 C≈0.01", "surface": "L≈0.93 C≈0.01", "text": "L≈0.12 C≈0.02" },
    "accents": { "primary": "h≈220 mid-chroma", "secondary": "h≈30 low-chroma" },
    "semantics": { "success": "...", "warning": "...", "danger": "..." },
    "states": { "hoverDeltaL": "-0.03", "activeDeltaL": "-0.06" }
  },
  "type": {
    "body": { "style": "humanist sans", "axes": ["wght","opsz"], "defaultWght": 420 },
    "display": { "style": "editorial serif", "axes": ["wght"], "tracking": "tight" },
    "data": { "style": "tabular-friendly sans/mono", "features": ["tnum","ss01"] },
    "scale": { "ratio": 1.2, "base": "1rem", "fluid": true }
  },
  "layout": { "unit": 4, "scale": [4,8,12,16,24,32,48] },
  "shape": { "radius": { "sm": 6, "md": 12, "lg": 20 }, "border": "crisp" },
  "motion": {
    "durationsMs": { "micro": 120, "ui": 220, "nav": 380 },
    "easing": { "micro": "cubic-bezier(...)", "nav": "spring-like linear()" },
    "reducedMotion": { "strategy": "fade/instant", "disableAmbient": true }
  },
  "material": { "grain": "subtle", "gloss": "matte", "shaderBg": false },
  "dataviz": {
    "categorical": "10 colors",
    "sequential": "single-hue",
    "diverging": "two-hue",
    "grid": "low-ink"
  }
}
```
