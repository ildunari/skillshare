#!/usr/bin/env node
/**
 * Render a PPTX from Slide Deck IR using PptxGenJS.
 *
 * Usage:
 *   node scripts/render_pptx.js <ir.json> <output.pptx>
 */

const fs = require("fs");
const os = require("os");
const path = require("path");
const pptxgen = require("pptxgenjs");
let sharp = null;
let AdmZip = null;
try {
  sharp = require("sharp");
  sharp.cache(false);
} catch (_err) {
  sharp = null;
}
try {
  AdmZip = require("adm-zip");
} catch (_err) {
  AdmZip = null;
}
const GEOMETRY = require("./archetype-geometries.json");
const createArchetypeHandlers = require("./render/archetypes");

const THEMES_PATH = path.resolve(__dirname, "../assets/themes.json");
const PALETTES_PATH = path.resolve(__dirname, "../assets/palettes.json");
const MASTER_CONTENT = "MASTER_CONTENT";
const MASTER_SECTION = "MASTER_SECTION";
const MASTER_COVER = "MASTER_COVER";

// PptxGenJS exposes enums on the instance, not the module export.
const _enumProbe = new pptxgen();
const ShapeType = _enumProbe.ShapeType;
const ChartType = _enumProbe.ChartType;

function readJson(p) {
  return JSON.parse(fs.readFileSync(p, "utf8"));
}

function readJsonSafe(p, fallback) {
  try {
    return readJson(p);
  } catch (_err) {
    return fallback;
  }
}

function isObject(v) {
  return !!v && typeof v === "object" && !Array.isArray(v);
}

function deepMerge(base, extra) {
  const out = Object.assign({}, base || {});
  for (const [k, v] of Object.entries(extra || {})) {
    if (isObject(v) && isObject(out[k])) {
      out[k] = deepMerge(out[k], v);
    } else {
      out[k] = v;
    }
  }
  return out;
}

function isHexColor(s) {
  return typeof s === "string" && /^#?[0-9a-fA-F]{6}$/.test(s);
}

function asPptxColor(tokenOrHex, paletteColors) {
  if (!tokenOrHex) return undefined;
  if (isHexColor(tokenOrHex)) return String(tokenOrHex).replace(/^#/, "").toUpperCase();
  if (typeof tokenOrHex === "string" && paletteColors && isHexColor(paletteColors[tokenOrHex])) {
    return String(paletteColors[tokenOrHex]).replace(/^#/, "").toUpperCase();
  }
  return undefined;
}

function safeText(s) {
  if (s === null || s === undefined) return "";
  return String(s);
}

function asNum(x, fallback = 0) {
  const n = Number(x);
  return Number.isFinite(n) ? n : fallback;
}

function bboxToPptx(bbox) {
  const b = bbox || {};
  return {
    x: asNum(b.x),
    y: asNum(b.y),
    w: asNum(b.w),
    h: asNum(b.h),
  };
}

// ---------------------------------------------------------------------------
// Gradient / fill / effect utilities (ported from v1-update)
// ---------------------------------------------------------------------------
function clamp01(x) {
  const n = Number(x);
  if (!Number.isFinite(n)) return 0;
  return Math.max(0, Math.min(1, n));
}

function normalizeHex(color) {
  if (!color) return null;
  if (typeof color !== "string") return null;
  let c = color.trim();
  if (c.startsWith("#")) c = c.slice(1);
  if (c.length === 3) c = c.split("").map((ch) => ch + ch).join("");
  if (!/^[0-9a-fA-F]{6}$/.test(c)) return null;
  return c.toUpperCase();
}

function lightenHex(hex, t) {
  const c = normalizeHex(hex);
  if (!c) return null;
  const tt = clamp01(t);
  const r = parseInt(c.slice(0, 2), 16);
  const g = parseInt(c.slice(2, 4), 16);
  const b = parseInt(c.slice(4, 6), 16);
  const lr = Math.round(r + (255 - r) * tt);
  const lg = Math.round(g + (255 - g) * tt);
  const lb = Math.round(b + (255 - b) * tt);
  return [lr, lg, lb].map((n) => n.toString(16).padStart(2, "0")).join("").toUpperCase();
}

function degreesToGradientLine(angleDeg) {
  const a = (Number(angleDeg) || 0) * Math.PI / 180;
  const cx = 50, cy = 50, r = 50;
  const dx = Math.cos(a), dy = Math.sin(a);
  return [cx - dx * r, cy - dy * r, cx + dx * r, cy + dy * r];
}

function svgToDataUri(svg) {
  const cleaned = String(svg).replace(/\r?\n/g, "").replace(/\s{2,}/g, " ").trim();
  const b64 = Buffer.from(cleaned, "utf-8").toString("base64");
  return `data:image/svg+xml;base64,${b64}`;
}

function combineTransparency(baseTransparencyPct, opacity01) {
  const baseT = Math.max(0, Math.min(100, Number(baseTransparencyPct ?? 0)));
  const op = (opacity01 === undefined || opacity01 === null) ? 1 : clamp01(opacity01);
  const baseAlpha = 1 - baseT / 100;
  const alpha = baseAlpha * op;
  return Math.max(0, Math.min(100, Math.round((1 - alpha) * 100)));
}

/**
 * Resolve a fill spec from style_tokens or theme tokens.
 * Returns { kind:'solid', color, transparency } or { kind:'gradient', type, angle, stops, transparency } or null.
 */
function resolveFillSpec(fill, paletteColors) {
  if (!fill) return null;

  // Token name indirection: look up in paletteColors.fills then as a color
  if (typeof fill === "string") {
    const key = fill.trim();
    const fills = paletteColors?.fills || {};
    if (fills[key]) return resolveFillSpec(fills[key], paletteColors);
    const col = asPptxColor(key, paletteColors?.colors || paletteColors || {});
    if (col) return { kind: "solid", color: col, transparency: 0 };
    return null;
  }

  if (typeof fill === "object") {
    // Solid
    if (fill.kind === "solid" || fill.type === "solid" || (!fill.stops && fill.color)) {
      const col = asPptxColor(fill.color || fill.value, paletteColors?.colors || paletteColors || {}) || "F9FAFB";
      const opacity = (fill.opacity !== undefined) ? clamp01(fill.opacity) : 1;
      const transparency = (fill.transparency !== undefined) ? Number(fill.transparency) : Math.round((1 - opacity) * 100);
      return { kind: "solid", color: col, transparency: Math.max(0, Math.min(100, transparency)) };
    }

    // Gradient
    const gType = (fill.type || fill.kind || "linear").toLowerCase();
    if (gType === "linear" || gType === "radial" || gType === "gradient") {
      const actualType = (gType === "gradient") ? "linear" : gType;
      const stops = Array.isArray(fill.stops) ? fill.stops : [];
      const palette = paletteColors?.colors || paletteColors || {};
      const normStops = stops.map((s) => ({
        pos: Math.max(0, Math.min(100, Number(s.pos ?? s.position ?? 0))),
        color: asPptxColor(s.color, palette) || asPptxColor("primary", palette) || "2563EB",
        alpha: (s.alpha !== undefined) ? clamp01(s.alpha) : 1
      }));
      normStops.sort((a, b) => a.pos - b.pos);

      const opacity = (fill.opacity !== undefined) ? clamp01(fill.opacity) : 1;
      const transparency = (fill.transparency !== undefined) ? Number(fill.transparency) : Math.round((1 - opacity) * 100);

      return {
        kind: "gradient",
        type: actualType,
        angle: Number(fill.angle ?? fill.direction ?? 0),
        cx: fill.cx,
        cy: fill.cy,
        r: fill.r,
        stops: normStops.length ? normStops : [
          { pos: 0, color: asPptxColor("primary", palette) || "2563EB", alpha: 1 },
          { pos: 100, color: asPptxColor("accent_1", palette) || lightenHex(asPptxColor("primary", palette) || "2563EB", 0.35) || "60A5FA", alpha: 1 }
        ],
        transparency: Math.max(0, Math.min(100, transparency))
      };
    }
  }
  return null;
}

/**
 * Build an SVG rect with gradient/solid fill, returning SVG markup string.
 */
function buildGradientRectSvg({ fillSpec, radius = 0, stroke = null, strokeWidth = 0, opacity = 1 }) {
  const rx = Math.max(0, Number(radius) || 0);
  const sw = Math.max(0, Number(strokeWidth) || 0);
  const strokeHex = stroke ? `#${normalizeHex(stroke) || stroke}` : "none";
  const groupOpacity = clamp01(opacity);

  if (!fillSpec || fillSpec.kind !== "gradient") {
    const col = fillSpec?.color ? `#${normalizeHex(fillSpec.color) || fillSpec.color}` : "#FFFFFF";
    const fillOpacity = 1 - ((fillSpec?.transparency || 0) / 100);
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none"><g opacity="${groupOpacity}"><rect x="0" y="0" width="100" height="100" rx="${rx}" ry="${rx}" fill="${col}" fill-opacity="${fillOpacity}" stroke="${strokeHex}" stroke-width="${sw}"/></g></svg>`;
  }

  const id = "g";
  const stops = fillSpec.stops.map((s) => {
    const c = `#${normalizeHex(s.color) || s.color}`;
    const o = clamp01(s.alpha);
    return `<stop offset="${s.pos}%" stop-color="${c}" stop-opacity="${o}"/>`;
  }).join("");

  const fillOpacity = 1 - ((fillSpec.transparency || 0) / 100);

  let defs = "";
  let fillUrl = "";
  if (fillSpec.type === "radial") {
    const cx = (fillSpec.cx !== undefined) ? Number(fillSpec.cx) : 50;
    const cy = (fillSpec.cy !== undefined) ? Number(fillSpec.cy) : 50;
    const rr = (fillSpec.r !== undefined) ? Number(fillSpec.r) : 70;
    defs = `<radialGradient id="${id}" cx="${cx}%" cy="${cy}%" r="${rr}%">${stops}</radialGradient>`;
    fillUrl = `url(#${id})`;
  } else {
    const [x1, y1, x2, y2] = degreesToGradientLine(fillSpec.angle || 0);
    defs = `<linearGradient id="${id}" gradientUnits="userSpaceOnUse" x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}">${stops}</linearGradient>`;
    fillUrl = `url(#${id})`;
  }

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none"><defs>${defs}</defs><g opacity="${groupOpacity}"><rect x="0" y="0" width="100" height="100" rx="${rx}" ry="${rx}" fill="${fillUrl}" fill-opacity="${fillOpacity}" stroke="${strokeHex}" stroke-width="${sw}"/></g></svg>`;
}

/**
 * Parse shadow spec from style_tokens or theme token name.
 */
function parseShadowSpec(sh, paletteColors) {
  if (!sh) return undefined;
  if (typeof sh === "boolean") return sh ? "card" : undefined;
  if (typeof sh === "string") return sh; // token name like "card", "pop" — handled by StyleResolver
  if (typeof sh !== "object") return undefined;
  const color = asPptxColor(sh.color || "000000", paletteColors || {}) || "000000";
  const opacity = (sh.opacity !== undefined) ? clamp01(sh.opacity) : 0.25;
  const blur = Number(sh.blur ?? 8);
  const angle = Number(sh.angle ?? 45);
  const distance = Number(sh.distance ?? sh.offset ?? 2);
  const type = sh.type || "outer";
  return { type, color, opacity, blur, angle, distance };
}

function parseOutlineSpec(outline, paletteColors) {
  if (!outline) return undefined;
  if (typeof outline === "string") return { color: asPptxColor(outline, paletteColors || {}) || outline, size: 1 };
  if (typeof outline !== "object") return undefined;
  const color = asPptxColor(outline.color, paletteColors || {}) || "111827";
  const size = Number(outline.size ?? 1);
  return { color, size };
}

function parseGlowSpec(glow, paletteColors) {
  if (!glow || typeof glow !== "object") return undefined;
  const color = asPptxColor(glow.color, paletteColors || {}) || "2563EB";
  const size = Number(glow.size ?? 6);
  const opacity = (glow.opacity !== undefined) ? clamp01(glow.opacity) : 0.3;
  return { color, size, opacity };
}

/**
 * Load an SVG icon from assets/icons/<name>.svg
 */
function loadIconSvg(iconName) {
  if (!iconName) return null;
  const p = path.resolve(__dirname, "..", "assets", "icons", `${iconName}.svg`);
  if (!fs.existsSync(p)) return null;
  return fs.readFileSync(p, "utf-8");
}

/**
 * Tint an SVG string by replacing currentColor and adjusting stroke-width.
 */
function tintIconSvg(svg, { colorHex, strokeWidth }) {
  let out = String(svg);
  const col = colorHex ? `#${normalizeHex(colorHex) || colorHex}` : "#000000";
  out = out.replace(/currentColor/g, col);
  if (strokeWidth) {
    if (out.match(/stroke-width="/)) out = out.replace(/stroke-width="[^"]*"/, `stroke-width="${strokeWidth}"`);
    else out = out.replace(/<svg\b/, `<svg stroke-width="${strokeWidth}"`);
  }
  return out;
}

// ---------------------------------------------------------------------------
// End gradient / fill / effect utilities
// ---------------------------------------------------------------------------

function sanitizeName(s) {
  return safeText(s || "unnamed")
    .replace(/[^a-zA-Z0-9:_-]+/g, "_")
    .replace(/^_+|_+$/g, "")
    .slice(0, 72) || "unnamed";
}

function createObjectNamer(slideId) {
  const counts = Object.create(null);
  const sid = sanitizeName(slideId || "slide");
  return function next(kind, el) {
    const semanticRole = sanitizeName(
      (el && (el.semantic_role || el.semanticRole || el.role || el.semantic_type || el.type)) || kind || "obj"
    );
    const key = semanticRole;
    const idx = (counts[key] || 0) + 1;
    counts[key] = idx;
    return `el:${sid}:${semanticRole}:${idx}`;
  };
}

function withObjectName(opts, ctx, kind, el) {
  const out = Object.assign({}, opts || {});
  if (!out.objectName && ctx && typeof ctx.namer === "function") {
    out.objectName = ctx.namer(kind, el);
  }
  return out;
}

function resolveThemesAndPalettes(deckTheme) {
  const themesJson = readJsonSafe(THEMES_PATH, { themes: [] });
  const palettesJson = readJsonSafe(PALETTES_PATH, { palettes: [] });
  const themes = Array.isArray(themesJson.themes) ? themesJson.themes : [];
  const palettes = Array.isArray(palettesJson.palettes) ? palettesJson.palettes : [];

  const requestedThemeId = safeText(deckTheme?.id || "").trim();
  const atlasTheme = themes.find((t) => t && t.id === "atlas");
  const theme =
    themes.find((t) => t && t.id === requestedThemeId) ||
    atlasTheme ||
    themes[0] ||
    { id: "atlas", palette: { id: "consulting_blue", mode: "light" }, typography: {}, shapes: {}, cards: {}, charts: {}, motion: {} };

  const paletteId = safeText(deckTheme?.palette?.id || theme?.palette?.id || "").trim();
  const palette =
    palettes.find((p) => p && p.id === paletteId) ||
    palettes.find((p) => p && p.id === theme?.palette?.id) ||
    palettes.find((p) => p && p.id === "consulting_blue") ||
    palettes[0] ||
    { id: "consulting_blue", modes: { light: {} } };

  const mode = safeText(deckTheme?.mode || theme?.palette?.mode || "light").toLowerCase();
  const paletteMode =
    (palette.modes && palette.modes[mode]) ||
    (palette.modes && palette.modes.light) ||
    (palette.modes && palette.modes.dark) ||
    {};

  return {
    theme,
    palette,
    mode,
    paletteMode,
  };
}

function buildTokens(deck, themeBundle) {
  const theme = themeBundle.theme || {};
  const paletteColors = themeBundle.paletteMode || {};
  const defaults = {
    fonts: {
      headline: {
        family: theme?.typography?.fonts?.headline?.family || "Inter",
        weight: theme?.typography?.fonts?.headline?.weight || 700,
      },
      body: {
        family: theme?.typography?.fonts?.body?.family || "Inter",
        weight: theme?.typography?.fonts?.body?.weight || 400,
      },
    },
    sizes: {
      h1: asNum(theme?.typography?.sizes_pt?.h1, 40),
      h2: asNum(theme?.typography?.sizes_pt?.h2, 30),
      body: asNum(theme?.typography?.sizes_pt?.body, 20),
      caption: asNum(theme?.typography?.sizes_pt?.caption, 14),
    },
    colors: paletteColors,
    grid: theme?.layout?.grid || {},
    shapes: theme?.shapes || {},
    cards: theme?.cards || {},
    charts: theme?.charts || {},
    motion: theme?.motion || {},
    // v1-update merge: pass through fills and shadows for gradient/effect support
    fills: theme?.fills || {},
    shadows: theme?.shadows || {},
  };
  const legacyTokens = deepMerge({}, deck?.tokens || {});
  if (legacyTokens.fonts && legacyTokens.fonts.heading && !legacyTokens.fonts.headline) {
    legacyTokens.fonts.headline = legacyTokens.fonts.heading;
  }
  return deepMerge(defaults, legacyTokens);
}

class StyleResolver {
  constructor(tokens, theme) {
    this.tokens = tokens || {};
    this.theme = theme || {};
  }

  color(tokenOrHex, fallback = "111111") {
    const palette = this.tokens.colors || {};
    return asPptxColor(tokenOrHex, palette) || asPptxColor(fallback, palette) || "111111";
  }

  font(role = "body") {
    const fromTokens = this.tokens.fonts || {};
    const fromTheme = this.theme?.typography?.fonts || {};
    const selected = fromTokens[role] || fromTheme[role] || fromTokens.body || fromTheme.body || {};
    return {
      family: selected.family || "Inter",
      weight: asNum(selected.weight, role === "headline" ? 700 : 400),
    };
  }

  lineHeight(role = "body") {
    const lh = this.theme?.typography?.line_height || {};
    if (role === "headline") return asNum(lh.headline, 1.05);
    return asNum(lh.body, 1.2);
  }

  shadow(enabled = true) {
    const sh = this.theme?.shapes?.shadow || {};
    if (!enabled || sh.enabled === false) return undefined;
    const ox = asNum(sh.offset_pt?.x, 0);
    const oy = asNum(sh.offset_pt?.y, 2);
    const distance = Math.max(0, Math.sqrt(ox * ox + oy * oy));
    const angle = (Math.atan2(oy, ox || 0.0001) * 180) / Math.PI;
    return {
      type: "outer",
      color: this.color("fg", "111111"),
      blur: asNum(sh.blur_pt, 6),
      angle: Number.isFinite(angle) ? ((angle % 360) + 360) % 360 : 90,
      distance,
      offset: distance,
      opacity: asNum(sh.opacity, 0.18),
    };
  }

  cardStyle(overrides = {}) {
    const fillToken = overrides.fill || this.tokens.cards?.fill || this.theme?.cards?.fill || "surface";
    const strokeToken = overrides.stroke || this.tokens.cards?.stroke || this.theme?.cards?.stroke || "border";
    const radius = asNum(
      overrides.radius,
      asNum(this.tokens.cards?.radius, asNum(this.theme?.cards?.radius, asNum(this.theme?.shapes?.corner_radius, 10)))
    );
    const strokeWidth = asNum(
      overrides.strokeWidth,
      asNum(this.tokens.shapes?.border_width, asNum(this.theme?.shapes?.border_width, 1))
    );
    return {
      fill: { color: this.color(fillToken, "FFFFFF") },
      line: { color: this.color(strokeToken, "D1D5DB"), width: strokeWidth },
      radius,
      shadow: this.shadow(overrides.shadow !== false),
    };
  }

  chartDefaults() {
    const colors = this.tokens.colors || {};
    const series = [1, 2, 3, 4, 5, 6]
      .map((n) => this.color(`series_${n}`, this.color("primary", "2563EB")))
      .filter(Boolean);
    return {
      chartColors: series,
      valGridLine: { style: "dash", color: this.color("gridline", "E5E7EB") },
      catAxisLabelColor: this.color("axis", this.color("muted", "6B7280")),
      valAxisLabelColor: this.color("axis", this.color("muted", "6B7280")),
      dataLabelColor: this.color("fg", "111827"),
      catAxisLabelSize: asNum(this.theme?.charts?.axis_label_size_pt, 14),
      valAxisLabelSize: asNum(this.theme?.charts?.axis_label_size_pt, 14),
      legendFontSize: asNum(this.theme?.charts?.legend_size_pt, 12),
      showLegend: true,
    };
  }

  masterBg(masterName) {
    if (masterName === MASTER_SECTION) return this.color("primary", "2563EB");
    if (masterName === MASTER_COVER) return this.color("bg", "FFFFFF");
    return this.color("bg", "FFFFFF");
  }

  accentColor(slot = 1) {
    return this.color(`accent_${slot}`, this.color("primary", "2563EB"));
  }

  // --- Merged from v1-update: extended visual capabilities ---

  /** Resolve a fill spec (solid or gradient) from a fill value + palette. */
  fillSpec(fill) {
    const palette = this.tokens.colors || {};
    const fills = this.tokens.fills || this.theme?.fills || {};
    return resolveFillSpec(fill, { colors: palette, fills });
  }

  /**
   * Enhanced shadow: if spec is a string token name, look it up in theme shadows.
   * If spec is an object, parse it directly.
   * Falls back to theme shapes.shadow if enabled=true and no spec given.
   */
  shadowFromSpec(spec, enabled) {
    if (spec === false || spec === null) return undefined;
    if (spec && typeof spec === "object" && spec.type) return spec; // already parsed
    if (typeof spec === "string") {
      const shadows = this.tokens.shadows || this.theme?.shadows || {};
      if (shadows[spec]) return this.shadowFromSpec(shadows[spec], true);
    }
    const parsed = parseShadowSpec(spec, this.tokens.colors || {});
    if (parsed && typeof parsed === "object") return parsed;
    if (typeof parsed === "string") {
      const shadows = this.tokens.shadows || this.theme?.shadows || {};
      if (shadows[parsed]) return this.shadowFromSpec(shadows[parsed], true);
    }
    if (enabled !== false) return this.shadow(enabled);
    return undefined;
  }

  /** Parse text outline spec. */
  outline(spec) {
    return parseOutlineSpec(spec, this.tokens.colors || {});
  }

  /** Parse text glow spec. */
  glow(spec) {
    return parseGlowSpec(spec, this.tokens.colors || {});
  }

  /** Compute PptxGenJS transparency (0-100) from opacity (0-1). */
  transparency(opacity) {
    if (opacity === undefined || opacity === null) return undefined;
    return Math.max(0, Math.min(100, Math.round((1 - clamp01(opacity)) * 100)));
  }
}

function addText(slide, text, opts, ctx, el) {
  const named = withObjectName(
    Object.assign({ autoFit: true, margin: 0.03 }, opts || {}),
    ctx,
    "text",
    el
  );
  if (!named.lineSpacingMultiple && ctx && ctx.styles && typeof ctx.styles.lineHeight === "function") {
    const semantic = String(el?.semantic_type || el?.semantic_role || el?.role || "").toLowerCase();
    const role = /headline|title|h1|h2/.test(semantic) ? "headline" : "body";
    named.lineSpacingMultiple = ctx.styles.lineHeight(role);
  }
  // --- v1-update merge: text shadow, outline, glow, opacity from style_tokens ---
  const st = el?.style_tokens || {};
  if (st.textShadow && !named.shadow && ctx?.styles) {
    named.shadow = ctx.styles.shadowFromSpec(st.textShadow, true);
  }
  if (st.outline && !named.outline && ctx?.styles) {
    named.outline = ctx.styles.outline(st.outline);
  }
  if (st.glow && !named.glow && ctx?.styles) {
    named.glow = ctx.styles.glow(st.glow);
  }
  if (st.opacity !== undefined && named.transparency === undefined) {
    named.transparency = Math.round((1 - clamp01(st.opacity)) * 100);
  }
  slide.addText(text, named);
}

function addShape(slide, shapeType, opts, ctx, el) {
  const input = Object.assign({}, opts || {});
  if (Number.isFinite(asNum(input.radius, Number.NaN))) {
    input.rectRadius = asNum(input.radius) / 72;
    delete input.radius;
  }
  // --- v1-update merge: per-element opacity ---
  const st = el?.style_tokens || {};
  if (st.opacity !== undefined && input.transparency === undefined) {
    const existingFillTrans = input.fill?.transparency ?? 0;
    input.transparency = combineTransparency(existingFillTrans, st.opacity);
    if (input.fill) input.fill.transparency = input.transparency;
  }
  // --- v1-update merge: shadow from style_tokens ---
  if (st.shadow && !input.shadow && ctx?.styles) {
    input.shadow = ctx.styles.shadowFromSpec(st.shadow, true);
  }
  const named = withObjectName(input, ctx, "shape", el);
  slide.addShape(shapeType, named);
}

function addCard(slide, bbox, styleResolver, styleTokens, ctx, el) {
  const style = styleResolver.cardStyle(styleTokens || {});
  const b = bboxToPptx(bbox);
  const st = el?.style_tokens || styleTokens || {};

  // --- v1-update merge: gradient fill support for cards ---
  if (st.fill && typeof st.fill === "object" && (st.fill.type === "linear" || st.fill.type === "radial" || st.fill.type === "gradient")) {
    const fillSpec = styleResolver.fillSpec(st.fill);
    if (fillSpec && fillSpec.kind === "gradient") {
      const radius = asNum(style.radius, 12);
      const strokeColor = style.line?.color || null;
      const strokeWidth = style.line?.width || 0;
      const opacity = st.opacity !== undefined ? clamp01(st.opacity) : 1;
      const svg = buildGradientRectSvg({ fillSpec, radius, stroke: strokeColor, strokeWidth, opacity });
      const imgOpts = Object.assign({}, b, {
        data: svgToDataUri(svg),
        shadow: style.shadow,
      });
      const named = withObjectName(imgOpts, ctx, "card", el);
      slide.addImage(named);
      return;
    }
  }

  addShape(
    slide,
    ShapeType.roundRect,
    Object.assign({}, b, style, { rectRadius: asNum(style.radius, 12) / 72 }),
    ctx,
    el
  );
}

function normalizeChartType(kind) {
  const k = safeText(kind).toLowerCase();
  if (k === "bar" || k === "barh") return { type: ChartType.bar, opts: { barDir: "bar" } };
  if (k === "column" || k === "col") return { type: ChartType.bar, opts: { barDir: "col" } };
  if (k === "pie") return { type: ChartType.pie, opts: {} };
  if (k === "doughnut") return { type: ChartType.doughnut, opts: {} };
  if (k === "area") return { type: ChartType.area, opts: {} };
  if (k === "radar") return { type: ChartType.radar, opts: {} };
  if (k === "scatter") return { type: ChartType.scatter, opts: {} };
  if (k === "bubble") return { type: ChartType.bubble, opts: {} };
  return { type: ChartType.line, opts: {} };
}

function addChart(slide, chartTypeDef, data, opts, styleResolver, ctx, el) {
  const normalized = isObject(chartTypeDef) ? chartTypeDef : { type: chartTypeDef, opts: {} };
  const merged = Object.assign({}, styleResolver.chartDefaults(), normalized.opts || {}, opts || {});
  if (!Object.prototype.hasOwnProperty.call(merged, "showLegend")) {
    merged.showLegend = Array.isArray(data) && data.length > 1;
  }
  if (!Object.prototype.hasOwnProperty.call(merged, "showValue")) {
    merged.showValue = false;
  }
  const named = withObjectName(merged, ctx, "chart", el);
  slide.addChart(normalized.type, data, named);
}

function addTable(slide, rows, opts, ctx, el) {
  const named = withObjectName(opts, ctx, "table", el);
  slide.addTable(rows, named);
}

function addConnector(slide, opts, styleResolver, ctx, el) {
  const merged = Object.assign(
    {
      line: {
        color: styleResolver.color("primary", "2563EB"),
        width: 1.5,
      },
    },
    opts || {}
  );
  addShape(slide, ShapeType.line, merged, ctx, el);
}

function isFullBleedBbox(bbox, deckWidth, deckHeight, tolerance = 0.03) {
  const b = bboxToPptx(bbox);
  return (
    Math.abs(b.x) <= tolerance &&
    Math.abs(b.y) <= tolerance &&
    Math.abs((b.x + b.w) - asNum(deckWidth, 13.333)) <= tolerance &&
    Math.abs((b.y + b.h) - asNum(deckHeight, 7.5)) <= tolerance
  );
}

async function buildRoundedImageMask(srcPath, targetWIn, targetHIn, radiusPt = 0, mode = "cover") {
  if (!sharp) return srcPath;
  const dpi = 192;
  const wPx = Math.max(8, Math.round(asNum(targetWIn, 1) * dpi));
  const hPx = Math.max(8, Math.round(asNum(targetHIn, 1) * dpi));
  const rPx = Math.max(0, Math.round((asNum(radiusPt, 0) / 72) * dpi));

  let img = sharp(srcPath).resize(wPx, hPx, { fit: mode === "contain" ? "contain" : "cover" });
  if (rPx > 0) {
    const svg = Buffer.from(
      `<svg width="${wPx}" height="${hPx}" xmlns="http://www.w3.org/2000/svg"><rect x="0" y="0" width="${wPx}" height="${hPx}" rx="${rPx}" ry="${rPx}" fill="#fff"/></svg>`
    );
    img = img.composite([{ input: svg, blend: "dest-in" }]);
  }

  const outPath = path.join(os.tmpdir(), `pptx-rounded-${Date.now()}-${Math.random().toString(36).slice(2)}.png`);
  await img.png().toFile(outPath);
  return outPath;
}

async function addImage(slide, opts, styleResolver, ctx, el) {
  const named = withObjectName(opts, ctx, "image", el);
  const src = named.path || named.data;
  if (!src) {
    const b = bboxToPptx(named);
    addCard(slide, b, styleResolver, {}, ctx, el);
    addText(
      slide,
      "Image",
      {
        x: b.x,
        y: b.y,
        w: b.w,
        h: b.h,
        fontFace: styleResolver.font("body").family,
        fontSize: 12,
        color: styleResolver.color("muted", "6B7280"),
        align: "center",
        valign: "mid",
      },
      ctx,
      el
    );
    return;
  }
  const bbox = bboxToPptx(named);
  const deckWidth = asNum(ctx?.deckWidth, 13.333);
  const deckHeight = asNum(ctx?.deckHeight, 7.5);
  const themeRadiusPt = asNum(styleResolver?.theme?.images?.corner_radius, 0);
  const radiusPt = asNum(named.cornerRadiusPt, themeRadiusPt);
  const fullBleed = isFullBleedBbox(bbox, deckWidth, deckHeight);
  const shouldRound = !!sharp && !fullBleed && (named.rounded === true || (named.rounded !== false && radiusPt > 0));

  const finalOpts = Object.assign({}, named);
  if (named.path && fs.existsSync(named.path) && shouldRound) {
    try {
      const roundedPath = await buildRoundedImageMask(
        named.path,
        bbox.w,
        bbox.h,
        radiusPt,
        named?.sizing?.type === "contain" ? "contain" : "cover"
      );
      finalOpts.path = roundedPath;
      delete finalOpts.data;
      delete finalOpts.sizing;
      if (ctx && Array.isArray(ctx.tempArtifacts)) {
        ctx.tempArtifacts.push(roundedPath);
      }
    } catch (_err) {
      if (!finalOpts.sizing) {
        finalOpts.sizing = { type: "cover" };
      }
    }
  } else if (named.path && fs.existsSync(named.path) && !finalOpts.sizing) {
    finalOpts.sizing = { type: "cover" };
  }

  slide.addImage(finalOpts);
}

function defineMasters(pptx, styleResolver) {
  const theme = styleResolver.theme || {};
  const masters = theme.masters || {};
  const deckW = asNum(styleResolver.tokens?.grid?.slide?.w, 13.333);
  const deckH = asNum(styleResolver.tokens?.grid?.slide?.h, 7.5);

  // Helper: build a master from a spec (v1-update masters config)
  function buildMasterFromSpec(masterTitle, spec, fallbackBg) {
    const bgFill = styleResolver.fillSpec(spec.backgroundFill || fallbackBg || "bg");
    const background = (bgFill?.kind === "solid")
      ? { color: bgFill.color, transparency: bgFill.transparency || 0 }
      : { color: styleResolver.color("bg", "FFFFFF") };

    const objects = [];

    // Gradient background: insert full-bleed SVG image
    if (bgFill?.kind === "gradient") {
      const svg = buildGradientRectSvg({ fillSpec: bgFill, radius: 0, stroke: null, strokeWidth: 0, opacity: 1 });
      objects.push({ image: { data: svgToDataUri(svg), x: 0, y: 0, w: deckW, h: deckH } });
    }

    // Accent bar
    if (spec.accentBar?.enabled) {
      const pos = spec.accentBar.position || "top";
      const h = Number(spec.accentBar.height || 0.08);
      const barFill = styleResolver.fillSpec(spec.accentBar.fill || "primary");
      const y = (pos === "bottom") ? (deckH - h) : 0;
      if (barFill?.kind === "gradient") {
        const svg = buildGradientRectSvg({ fillSpec: barFill, radius: 0, stroke: null, strokeWidth: 0, opacity: 1 });
        objects.push({ image: { data: svgToDataUri(svg), x: 0, y, w: deckW, h } });
      } else {
        const col = barFill?.color || styleResolver.color("primary", "2563EB");
        objects.push({ rect: { x: 0, y, w: deckW, h, fill: { color: col, transparency: barFill?.transparency || 0 }, line: { color: col, width: 0 } } });
      }
    }

    const masterDef = { title: masterTitle, background, objects };

    // Slide number
    if (spec.slideNumber?.enabled !== false) {
      const sn = spec.slideNumber || {};
      masterDef.slideNumber = {
        x: sn.x ?? 12.35,
        y: sn.y ?? (deckH - 0.34),
        w: sn.w ?? 0.85,
        h: sn.h ?? 0.2,
        fontFace: styleResolver.font("body").family,
        fontSize: sn.fontSize ?? asNum(styleResolver.tokens?.sizes?.caption, 11),
        color: styleResolver.color(sn.color || "muted", "6B7280"),
        align: sn.align || "right",
      };
    }

    return masterDef;
  }

  // If theme defines masters, use them
  if (masters.DEFAULT || masters.SECTION || masters.COVER) {
    if (masters.DEFAULT) {
      pptx.defineSlideMaster(buildMasterFromSpec(MASTER_CONTENT, masters.DEFAULT, "bg"));
    } else {
      // Fallback CONTENT master (same as original v2)
      pptx.defineSlideMaster({
        title: MASTER_CONTENT,
        background: { color: styleResolver.masterBg(MASTER_CONTENT) },
        objects: [{ rect: { x: 0, y: deckH - 0.28, w: deckW, h: 0.04, fill: { color: styleResolver.accentColor(1) }, line: { color: styleResolver.accentColor(1), width: 0 } } }],
        slideNumber: { x: 12.35, y: deckH - 0.34, w: 0.85, h: 0.2, fontFace: styleResolver.font("body").family, fontSize: asNum(styleResolver.tokens?.sizes?.caption, 11), color: styleResolver.color("muted", "6B7280"), align: "right" },
      });
    }
    if (masters.SECTION) {
      pptx.defineSlideMaster(buildMasterFromSpec(MASTER_SECTION, masters.SECTION, "primary"));
    } else {
      pptx.defineSlideMaster({ title: MASTER_SECTION, background: { color: styleResolver.masterBg(MASTER_SECTION) }, objects: [] });
    }
    if (masters.COVER) {
      pptx.defineSlideMaster(buildMasterFromSpec(MASTER_COVER, masters.COVER, "bg"));
    } else {
      pptx.defineSlideMaster({ title: MASTER_COVER, background: { color: styleResolver.masterBg(MASTER_COVER) }, objects: [] });
    }
    return;
  }

  // Original v2 behavior: hardcoded masters
  pptx.defineSlideMaster({
    title: MASTER_CONTENT,
    background: { color: styleResolver.masterBg(MASTER_CONTENT) },
    objects: [
      {
        rect: {
          x: 0,
          y: 7.22,
          w: 13.333,
          h: 0.04,
          fill: { color: styleResolver.accentColor(1) },
          line: { color: styleResolver.accentColor(1), width: 0 },
        },
      },
    ],
    slideNumber: {
      x: 12.35,
      y: 7.16,
      w: 0.85,
      h: 0.2,
      fontFace: styleResolver.font("body").family,
      fontSize: asNum(styleResolver.tokens?.sizes?.caption, 11),
      color: styleResolver.color("muted", "6B7280"),
      align: "right",
    },
  });
  pptx.defineSlideMaster({
    title: MASTER_SECTION,
    background: { color: styleResolver.masterBg(MASTER_SECTION) },
    objects: [],
  });
  pptx.defineSlideMaster({
    title: MASTER_COVER,
    background: { color: styleResolver.masterBg(MASTER_COVER) },
    objects: [],
  });
}

function firstIntFromString(s, fallback = Number.NaN) {
  const m = String(s || "").match(/(\d+)/);
  return m ? parseInt(m[1], 10) : fallback;
}

function canonicalArchetypeId(archetypeId, geometryCatalog = GEOMETRY) {
  const src = safeText(archetypeId || "").trim();
  if (!src) return "";
  if (geometryCatalog[src]) return src;
  const upper = src.toUpperCase();
  const exact = Object.keys(geometryCatalog).find((k) => k.toUpperCase() === upper);
  if (exact) return exact;
  const base = upper.match(/^A\d+/)?.[0] || upper;
  const byPrefix = Object.keys(geometryCatalog).find((k) => k.toUpperCase().startsWith(`${base}_`));
  return byPrefix || "";
}

function selectVariant(archetypeId, slideObj, geometryCatalog = GEOMETRY) {
  const canonicalId = canonicalArchetypeId(archetypeId, geometryCatalog);
  const variants = geometryCatalog[canonicalId];
  if (!canonicalId || !variants || !isObject(variants)) {
    return {
      archetype: canonicalId || null,
      variantKey: null,
      variant: null,
    };
  }
  const keys = Object.keys(variants);
  if (!keys.length) {
    return { archetype: canonicalId, variantKey: null, variant: null };
  }
  const requested = slideObj?.variant || slideObj?.layout_variant;
  if (requested && variants[requested]) {
    return {
      archetype: canonicalId,
      variantKey: requested,
      variant: variants[requested],
    };
  }
  if (keys.length === 1) {
    return {
      archetype: canonicalId,
      variantKey: keys[0],
      variant: variants[keys[0]],
    };
  }
  const targetCount =
    asNum(slideObj?.node_count, Number.NaN) ||
    asNum(slideObj?.step_count, Number.NaN) ||
    asNum(slideObj?.item_count, Number.NaN) ||
    asNum(slideObj?.count, Number.NaN) ||
    (Array.isArray(slideObj?.items) ? slideObj.items.length : Number.NaN) ||
    (Array.isArray(slideObj?.cards) ? slideObj.cards.length : Number.NaN) ||
    (Array.isArray(slideObj?.nodes) ? slideObj.nodes.length : Number.NaN) ||
    (Array.isArray(slideObj?.elements) ? slideObj.elements.length : Number.NaN);
  const ranked = keys
    .map((k) => {
      const n = firstIntFromString(k, Number.NaN);
      const score = Number.isFinite(targetCount) && Number.isFinite(n) ? Math.abs(targetCount - n) : 9999;
      return { k, score };
    })
    .sort((a, b) => a.score - b.score || String(a.k).localeCompare(String(b.k)));
  const picked = ranked[0]?.k || keys[0];
  return {
    archetype: canonicalId,
    variantKey: picked,
    variant: variants[picked],
  };
}

function resolveMasterName(archetype) {
  const m = String(archetype || "").match(/^A(\d+)/i);
  const n = m ? parseInt(m[1], 10) : 0;
  if (n === 1) return MASTER_COVER;
  if (n === 2 || n === 24) return MASTER_SECTION;
  return MASTER_CONTENT;
}

function normalizeNotes(v) {
  if (v === null || v === undefined) return "";
  if (Array.isArray(v)) return v.map((x) => safeText(x)).join("\n");
  if (isObject(v)) return JSON.stringify(v, null, 2);
  return safeText(v);
}

async function renderTextElement(ctx, el) {
  const st = el.style_tokens || {};
  const bbox = bboxToPptx(el.bbox);
  const role = st.font || (String(el.semantic_type || "").toLowerCase() === "headline" ? "headline" : "body");
  const font = ctx.styles.font(role);
  const sizeDefault = role === "headline" ? ctx.tokens.sizes?.h1 : ctx.tokens.sizes?.body;
  const opts = {
    ...bbox,
    fontFace: font.family,
    fontSize: asNum(st.size, asNum(sizeDefault, 20)),
    color: ctx.styles.color(st.color || "fg", "111827"),
    bold: st.bold === true || role === "headline" || font.weight >= 600,
    italic: st.italic === true,
    align: st.align || "left",
    valign: st.valign || "top",
    margin: st.margin ?? 0.08,
  };
  if (st.lineHeight) opts.lineSpacingMultiple = st.lineHeight;
  if (Array.isArray(el.bullets) && el.bullets.length) {
    const runs = el.bullets.map((t) => ({
      text: safeText(t),
      options: { bullet: { indent: opts.fontSize * 0.8 }, hanging: opts.fontSize * 0.25 },
    }));
    addText(ctx.slide, runs, opts, ctx, el);
    return;
  }
  addText(ctx.slide, safeText(el.content || ""), opts, ctx, el);
}

async function renderImageElement(ctx, el) {
  const b = bboxToPptx(el.bbox);
  const src = el.src || el.path || el?.asset?.path;
  if (!src) {
    await addImage(
      ctx.slide,
      Object.assign({}, b),
      ctx.styles,
      ctx,
      el
    );
    return;
  }
  const abs = path.isAbsolute(src) ? src : path.resolve(process.cwd(), src);
  if (!fs.existsSync(abs)) {
    await addImage(ctx.slide, Object.assign({ path: null }, b), ctx.styles, ctx, el);
    return;
  }
  await addImage(
    ctx.slide,
    Object.assign({ path: abs }, b),
    ctx.styles,
    ctx,
    el
  );
}

async function renderChartElement(ctx, el) {
  const bbox = bboxToPptx(el.bbox);
  const spec = el.chartSpec || el.data || {};
  const categories = Array.isArray(spec.categories) ? spec.categories : [];
  const seriesData = Array.isArray(spec.seriesData) ? spec.seriesData : [];
  if (!categories.length || !seriesData.length) {
    addCard(ctx.slide, bbox, ctx.styles, {}, ctx, el);
    addText(
      ctx.slide,
      "[chart]",
      {
        ...bbox,
        fontFace: ctx.styles.font("body").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 12),
        color: ctx.styles.color("muted", "6B7280"),
        align: "center",
        valign: "mid",
      },
      ctx,
      el
    );
    return;
  }
  const kind = normalizeChartType(spec.kind);
  const data = seriesData.map((s) => ({
    name: s.name || "Series",
    labels: categories,
    values: Array.isArray(s.values) ? s.values : [],
  }));
  const highlightName = safeText(spec.highlightSeries || spec.highlight_series || "");
  const highlightIndex =
    Number.isInteger(spec.highlightIndex) && spec.highlightIndex >= 0 ? spec.highlightIndex : -1;
  const hasHighlight =
    highlightIndex >= 0 ||
    (highlightName && data.some((series) => safeText(series.name).toLowerCase() === highlightName.toLowerCase()));
  let chartOpts = { ...bbox };
  if (hasHighlight && data.length > 1) {
    const muted = ctx.styles.color("muted", "9CA3AF");
    const primary = ctx.styles.color("primary", "2563EB");
    const accent = ctx.styles.color("accent", "F59E0B");
    const colors = data.map((series, idx) => {
      const byIndex = highlightIndex >= 0 && idx === highlightIndex;
      const byName = highlightName && safeText(series.name).toLowerCase() === highlightName.toLowerCase();
      if (byIndex || byName) return idx === 0 ? primary : accent;
      return muted;
    });
    chartOpts = { ...chartOpts, chartColors: colors };
  }
  addChart(
    ctx.slide,
    kind,
    data,
    chartOpts,
    ctx.styles,
    ctx,
    el
  );
}

async function renderTableElement(ctx, el) {
  const bbox = bboxToPptx(el.bbox);
  const rows = Array.isArray(el.rows) ? el.rows : Array.isArray(el.data) ? el.data : [];
  if (!rows.length) {
    addCard(ctx.slide, bbox, ctx.styles, {}, ctx, el);
    addText(
      ctx.slide,
      "[table]",
      {
        ...bbox,
        fontFace: ctx.styles.font("body").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 12),
        color: ctx.styles.color("muted", "6B7280"),
        align: "center",
        valign: "mid",
      },
      ctx,
      el
    );
    return;
  }
  const cols = Array.isArray(el.columns) ? el.columns : [];
  const nRows = rows.length;
  const nCols = cols.length || (Array.isArray(rows[0]) ? rows[0].length : Object.keys(rows[0] || {}).length);
  if (!nCols) return;
  const cellW = bbox.w / nCols;
  const cellH = bbox.h / nRows;
  for (let r = 0; r < nRows; r++) {
    for (let c = 0; c < nCols; c++) {
      const x = bbox.x + c * cellW;
      const y = bbox.y + r * cellH;
      addShape(
        ctx.slide,
        ShapeType.rect,
        {
          x,
          y,
          w: cellW,
          h: cellH,
          fill: { color: ctx.styles.color("bg", "FFFFFF") },
          line: { color: ctx.styles.color("border", "D1D5DB"), width: 1 },
        },
        ctx,
        el
      );
      let txt = "";
      if (Array.isArray(rows[r])) txt = safeText(rows[r][c]);
      else if (isObject(rows[r])) {
        const key = cols[c] || Object.keys(rows[r])[c];
        txt = safeText(rows[r][key]);
      }
      addText(
        ctx.slide,
        txt,
        {
          x: x + 0.06,
          y: y + 0.04,
          w: cellW - 0.12,
          h: cellH - 0.08,
          fontFace: ctx.styles.font("body").family,
          fontSize: asNum(ctx.tokens.sizes?.caption, 12),
          color: ctx.styles.color("fg", "111827"),
          valign: "mid",
        },
        ctx,
        el
      );
    }
  }
}

async function renderCardElement(ctx, el) {
  const st = el.style_tokens || {};
  addCard(ctx.slide, el.bbox, ctx.styles, st, ctx, el);
  const children = Array.isArray(el.children) ? el.children : [];
  for (const child of children) {
    await renderElement(ctx, child);
  }
}

async function renderConnectorElement(ctx, el) {
  const st = el.style_tokens || {};
  const b = bboxToPptx(el.bbox);
  addConnector(
    ctx.slide,
    {
      x: b.x,
      y: b.y,
      w: b.w,
      h: b.h,
      line: {
        color: ctx.styles.color(st.color || st.stroke || "muted", "6B7280"),
        width: asNum(st.width, 1.5),
        beginArrowType: st.beginArrowType,
        endArrowType: st.endArrowType,
      },
    },
    ctx.styles,
    ctx,
    el
  );
}

async function renderCalloutElement(ctx, el) {
  const b = bboxToPptx(el.bbox);
  const st = el.style_tokens || {};
  addCard(
    ctx.slide,
    b,
    ctx.styles,
    {
      fill: st.fill || "annotation",
      stroke: st.stroke || "primary",
      radius: st.radius || 12,
    },
    ctx,
    el
  );
  addText(
    ctx.slide,
    safeText(el.content || ""),
    {
      x: b.x + 0.12,
      y: b.y + 0.1,
      w: Math.max(0.1, b.w - 0.24),
      h: Math.max(0.1, b.h - 0.2),
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(st.size, asNum(ctx.tokens.sizes?.h2, 28)),
      color: ctx.styles.color(st.color || "primary", "2563EB"),
      bold: true,
      align: st.align || "center",
      valign: "mid",
    },
    ctx,
    el
  );
}

async function renderElement(ctx, el) {
  if (!el || typeof el !== "object") return;
  const t = String(el.semantic_type || el.type || "").toLowerCase();
  if (t === "bg") return;
  if (!el.bbox && t !== "connector" && t !== "arrow" && t !== "line") return;

  if (t === "headline" || t === "text" || t === "caption" || t === "quote" || t === "number" || t === "footer" || t === "metric") {
    return renderTextElement(ctx, el);
  }
  if (t === "image" || t === "logo" || t === "person") return renderImageElement(ctx, el);
  if (t === "chart" || t === "sparkline") return renderChartElement(ctx, el);
  if (t === "table") return renderTableElement(ctx, el);
  if (t === "callout" || t === "annotation" || t === "badge") return renderCalloutElement(ctx, el);
  if (t === "card" || t === "panel" || t === "box" || t === "step" || t === "node" || t === "timeline_node" || t === "process_step") {
    return renderCardElement(ctx, el);
  }
  if (t === "connector" || t === "arrow" || t === "line") return renderConnectorElement(ctx, el);

  // Generic fallback for unknown semantic types.
  addCard(ctx.slide, el.bbox || { x: 0.7, y: 1.8, w: 2.0, h: 1.0 }, ctx.styles, {}, ctx, el);
}

async function renderGenericFallback(ctx) {
  const slideObj = ctx.slideObj || {};
  const elements = Array.isArray(slideObj.elements) ? [...slideObj.elements] : [];
  const hasHeadline = elements.some((e) => String(e?.semantic_type || "").toLowerCase() === "headline");
  if (!hasHeadline && slideObj.headline) {
    elements.unshift({
      semantic_type: "headline",
      role: "h1",
      content: slideObj.headline,
      bbox: { x: 0.7, y: 0.6, w: 11.9, h: 0.9 },
      style_tokens: { font: "headline", size: ctx.tokens.sizes?.h1 || 40, color: "fg" },
    });
  }
  for (const el of elements) {
    await renderElement(ctx, el);
  }
}

function slideElements(slideObj) {
  return Array.isArray(slideObj?.elements) ? slideObj.elements : [];
}

function roleValue(el) {
  return String(el?.semantic_role || el?.semanticRole || el?.role || "").toLowerCase();
}

function typeValue(el) {
  return String(el?.semantic_type || el?.type || "").toLowerCase();
}

function hasRoleToken(el, token) {
  if (!token) return false;
  return roleValue(el).includes(String(token).toLowerCase());
}

function firstElement(slideObj, predicate) {
  return slideElements(slideObj).find((el) => predicate(el));
}

function listElements(slideObj, predicate) {
  return slideElements(slideObj).filter((el) => predicate(el));
}

function firstText(slideObj, roleTokens = [], typeTokens = [], fallback = "") {
  const found = firstElement(slideObj, (el) => {
    const roleOk = !roleTokens.length || roleTokens.some((r) => hasRoleToken(el, r));
    const typeOk = !typeTokens.length || typeTokens.includes(typeValue(el));
    return roleOk && typeOk && (el.content !== undefined || el.text !== undefined);
  });
  return safeText(found?.content ?? found?.text ?? fallback);
}

function firstImagePath(slideObj, roleTokens = []) {
  const candidate = firstElement(slideObj, (el) => {
    const t = typeValue(el);
    const roleOk = !roleTokens.length || roleTokens.some((r) => hasRoleToken(el, r));
    return roleOk && (t === "image" || t === "logo" || t === "person");
  });
  const src = candidate?.src || candidate?.path || candidate?.asset?.path;
  if (!src) return null;
  const abs = path.isAbsolute(src) ? src : path.resolve(process.cwd(), src);
  return fs.existsSync(abs) ? abs : null;
}

function parseNodeText(raw) {
  const lines = safeText(raw || "").split("\n").map((x) => x.trim()).filter(Boolean);
  return {
    primary: lines[0] || "",
    secondary: lines.slice(1).join("\n"),
  };
}

function safeItemsArray(slideObj, fallback = []) {
  const direct =
    slideObj?.items ||
    slideObj?.cards ||
    slideObj?.nodes ||
    slideObj?.steps ||
    slideObj?.components ||
    slideObj?.people ||
    slideObj?.members ||
    slideObj?.team ||
    slideObj?.agenda ||
    slideObj?.kpis ||
    slideObj?.kpi_tiles;
  if (Array.isArray(direct) && direct.length) return direct;
  return fallback;
}

function safeItemsArrayByKeys(slideObj, keys = [], fallback = []) {
  for (const key of keys) {
    const v = slideObj?.[key];
    if (Array.isArray(v) && v.length) return v;
  }
  return fallback;
}

function itemText(item, keys, fallback = "") {
  if (item === null || item === undefined) return fallback;
  if (typeof item === "string" || typeof item === "number") return safeText(item);
  if (isObject(item)) {
    for (const k of keys) {
      if (item[k] !== undefined && item[k] !== null && String(item[k]).trim()) return safeText(item[k]);
    }
  }
  return fallback;
}

function slotEl(role, semanticType = "text", extra = {}) {
  return Object.assign(
    {
      semantic_role: role,
      semantic_type: semanticType,
      role,
    },
    extra
  );
}

function getArchetypeLayout(ctx, archetypeId) {
  const pick = selectVariant(archetypeId, ctx.slideObj, GEOMETRY);
  return {
    archetypeId: pick.archetype || archetypeId,
    variantKey: pick.variantKey,
    layout: pick.variant,
  };
}

function drawTextSlot(ctx, role, bbox, text, opts = {}, semanticType = "text") {
  if (!bbox) return;
  addText(
    ctx.slide,
    safeText(text || ""),
    Object.assign({}, bboxToPptx(bbox), opts),
    ctx,
    slotEl(role, semanticType)
  );
}

function drawFooterIfAny(ctx, footerBox) {
  const footer = firstText(ctx.slideObj, ["footer", "caption", "meta"], ["footer", "caption", "text"], "");
  if (!footer || !footerBox) return;
  drawTextSlot(
    ctx,
    "footer",
    footerBox,
    footer,
    {
      fontFace: ctx.styles.font("body").family,
      fontSize: asNum(ctx.tokens.sizes?.caption, 13),
      color: ctx.styles.color("muted", "6B7280"),
      valign: "mid",
      align: "left",
    },
    "footer"
  );
}

/**
 * Render an SVG icon into a slot bbox. If the icon SVG file exists in assets/icons/,
 * it's tinted and inserted as an image. Otherwise falls back to a colored ellipse placeholder.
 * @param {object} ctx - slide context
 * @param {string} role - object namer role
 * @param {object} bbox - {x,y,w,h}
 * @param {string} iconName - icon file name (without .svg extension)
 * @param {object} [opts] - { color, strokeWidth, shadow }
 */
function renderIconInSlot(ctx, role, bbox, iconName, opts = {}) {
  if (!bbox) return;
  const b = bboxToPptx(bbox);
  const colorHex = ctx.styles.color(opts.color || "primary", "2563EB");
  const sw = Number(opts.strokeWidth ?? ctx.styles.theme?.icons?.stroke_width_pt ?? 2);

  const svg = loadIconSvg(iconName);
  if (svg) {
    const tinted = tintIconSvg(svg, { colorHex, strokeWidth: sw });
    const imgOpts = Object.assign({}, b, { data: svgToDataUri(tinted) });
    if (opts.shadow) imgOpts.shadow = ctx.styles.shadowFromSpec(opts.shadow, true);
    const named = withObjectName(imgOpts, ctx, "icon", slotEl(role, "icon"));
    ctx.slide.addImage(named);
  } else {
    // Fallback: colored ellipse placeholder
    addShape(
      ctx.slide,
      ShapeType.ellipse,
      {
        ...b,
        fill: { color: colorHex },
        line: { color: colorHex, width: 0 },
      },
      ctx,
      slotEl(role, "shape")
    );
  }
}

async function drawImageSlot(ctx, role, bbox, src, fallbackFill = "surface") {
  if (!bbox) return;
  if (src) {
    await addImage(
      ctx.slide,
      Object.assign({ path: src }, bboxToPptx(bbox)),
      ctx.styles,
      ctx,
      slotEl(role, "image")
    );
    return;
  }
  addShape(
    ctx.slide,
    ShapeType.rect,
    {
      ...bboxToPptx(bbox),
      fill: { color: ctx.styles.color(fallbackFill, "F3F4F6") },
      line: { color: ctx.styles.color("border", "D1D5DB"), width: 1 },
    },
    ctx,
    slotEl(role, "shape")
  );
}

function lineFromPoints(from, to) {
  return {
    x: asNum(from?.x),
    y: asNum(from?.y),
    w: asNum(to?.x) - asNum(from?.x),
    h: asNum(to?.y) - asNum(from?.y),
  };
}

function boxCenter(box) {
  const b = bboxToPptx(box);
  return {
    x: b.x + b.w / 2,
    y: b.y + b.h / 2,
  };
}

function resolveImagePath(src) {
  if (!src) return null;
  const abs = path.isAbsolute(src) ? src : path.resolve(process.cwd(), src);
  return fs.existsSync(abs) ? abs : null;
}

function itemImagePath(item, keys = ["photo", "image", "avatar", "src", "path"]) {
  if (!isObject(item)) return null;
  for (const key of keys) {
    const v = item[key];
    if (typeof v === "string" && v.trim()) {
      const abs = resolveImagePath(v);
      if (abs) return abs;
      continue;
    }
    if (isObject(v)) {
      const nested = v.path || v.src || v.url;
      if (nested) {
        const abs = resolveImagePath(nested);
        if (abs) return abs;
      }
    }
  }
  return null;
}

function normalizeEdgeList(slideObj) {
  const candidate =
    safeItemsArrayByKeys(slideObj, ["edges", "connections", "links"], []) ||
    [];
  if (!Array.isArray(candidate) || !candidate.length) return [];
  return candidate
    .map((edge) => {
      if (!edge) return null;
      if (typeof edge === "string") {
        const m = edge.match(/(\d+)\s*[-=>]+\s*(\d+)/);
        if (!m) return null;
        return { from: parseInt(m[1], 10), to: parseInt(m[2], 10) };
      }
      if (isObject(edge)) {
        return {
          from: edge.from ?? edge.source ?? edge.start ?? edge.fromIndex ?? edge.sourceIndex,
          to: edge.to ?? edge.target ?? edge.end ?? edge.toIndex ?? edge.targetIndex,
          fromPoint: edge.fromPoint || edge.from_point || (Number.isFinite(edge.x1) && Number.isFinite(edge.y1) ? { x: edge.x1, y: edge.y1 } : null),
          toPoint: edge.toPoint || edge.to_point || (Number.isFinite(edge.x2) && Number.isFinite(edge.y2) ? { x: edge.x2, y: edge.y2 } : null),
        };
      }
      return null;
    })
    .filter(Boolean);
}

function resolveEdgeEndpoint(ref, slots, items) {
  if (isObject(ref) && Number.isFinite(ref.x) && Number.isFinite(ref.y)) {
    return { x: asNum(ref.x), y: asNum(ref.y) };
  }
  const count = Array.isArray(slots) ? slots.length : 0;
  let idx = Number.NaN;
  if (Number.isFinite(ref)) {
    idx = asNum(ref, Number.NaN);
  } else if (typeof ref === "string") {
    const num = firstIntFromString(ref, Number.NaN);
    if (Number.isFinite(num)) idx = num;
  } else if (isObject(ref)) {
    const fromFields = [ref.index, ref.idx, ref.i, ref.node, ref.component];
    for (const n of fromFields) {
      if (Number.isFinite(asNum(n, Number.NaN))) {
        idx = asNum(n, Number.NaN);
        break;
      }
    }
    if (!Number.isFinite(idx)) {
      const token = safeText(ref.id || ref.key || ref.name || ref.title || ref.label).trim().toLowerCase();
      if (token) {
        const namedIndex = (items || []).findIndex((item) => {
          const name = safeText(itemText(item, ["id", "key", "name", "title", "label"], "")).toLowerCase();
          return name && name === token;
        });
        if (namedIndex >= 0) idx = namedIndex;
      }
    }
  }
  if (!Number.isFinite(idx)) return null;
  if (idx >= 1 && idx <= count) idx = idx - 1;
  if (idx < 0 || idx >= count) return null;
  const slot = slots[idx];
  return slot?.box ? boxCenter(slot.box) : null;
}

async function renderA1Cover(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A1_cover");
  if (!layout) return renderGenericFallback(ctx);
  const bgSrc =
    firstImagePath(ctx.slideObj, ["bg", "cover", "hero"]) ||
    firstImagePath(ctx.slideObj, []) ||
    (ctx.slideObj?.bg_image ? path.resolve(process.cwd(), safeText(ctx.slideObj.bg_image)) : null);
  await drawImageSlot(ctx, "bg_image", layout.bg_image, bgSrc && fs.existsSync(bgSrc) ? bgSrc : null, "primary_dark");
  addShape(
    ctx.slide,
    ShapeType.rect,
    {
      ...bboxToPptx(layout.overlay_panel),
      fill: { color: "000000", transparency: 45 },
      line: { color: "000000", width: 0, transparency: 100 },
    },
    ctx,
    slotEl("overlay_panel", "shape")
  );
  drawTextSlot(
    ctx,
    "title",
    layout.title,
    firstText(ctx.slideObj, ["title", "headline"], ["headline", "text"], ctx.slideObj?.headline || ""),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h1, 40),
      bold: true,
      color: "FFFFFF",
      shadow: { type: "outer", color: "000000", blur: 4, offset: 1.2, angle: 90, opacity: 0.28 },
      valign: "mid",
    },
    "headline"
  );
  drawTextSlot(
    ctx,
    "subtitle",
    layout.subtitle,
    firstText(ctx.slideObj, ["subtitle", "supporting"], ["text", "caption"], ctx.slideObj?.subtitle || ""),
    {
      fontFace: ctx.styles.font("body").family,
      fontSize: asNum(ctx.tokens.sizes?.body, 20),
      color: "F3F4F6",
      shadow: { type: "outer", color: "000000", blur: 2, offset: 0.6, angle: 90, opacity: 0.2 },
      valign: "mid",
    }
  );
  drawTextSlot(
    ctx,
    "meta",
    layout.meta,
    firstText(ctx.slideObj, ["meta", "caption", "footer"], ["caption", "text", "footer"], ""),
    {
      fontFace: ctx.styles.font("body").family,
      fontSize: asNum(ctx.tokens.sizes?.caption, 13),
      color: "D1D5DB",
      valign: "mid",
    },
    "caption"
  );
}

async function renderA2SectionDivider(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A2_section_divider");
  if (!layout) return renderGenericFallback(ctx);
  addShape(
    ctx.slide,
    ShapeType.rect,
    {
      ...bboxToPptx(layout.bg_fill),
      fill: { color: ctx.styles.color("primary", "2563EB") },
      line: { color: ctx.styles.color("primary", "2563EB"), width: 0 },
    },
    ctx,
    slotEl("bg_fill", "shape")
  );
  drawTextSlot(
    ctx,
    "title",
    layout.title,
    firstText(ctx.slideObj, ["title", "headline"], ["headline", "text"], ctx.slideObj?.headline || ""),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h1, 40),
      bold: true,
      align: "center",
      valign: "mid",
      color: "FFFFFF",
    },
    "headline"
  );
  drawTextSlot(
    ctx,
    "subtitle",
    layout.subtitle,
    firstText(ctx.slideObj, ["subtitle", "supporting"], ["caption", "text"], ctx.slideObj?.subtitle || ""),
    {
      fontFace: ctx.styles.font("body").family,
      fontSize: asNum(ctx.tokens.sizes?.body, 20),
      align: "center",
      valign: "mid",
      color: "E5E7EB",
    },
    "caption"
  );
}

async function renderA3Agenda(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A3_agenda");
  if (!layout) return renderGenericFallback(ctx);
  drawTextSlot(
    ctx,
    "headline",
    layout.headline,
    firstText(ctx.slideObj, ["headline", "title"], ["headline", "text"], ctx.slideObj?.headline || "Agenda"),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h2, 30),
      bold: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    },
    "headline"
  );
  const extracted = listElements(ctx.slideObj, (el) => {
    const t = typeValue(el);
    if (t === "headline" || t === "footer" || t === "caption") return false;
    return t === "text" || hasRoleToken(el, "item") || hasRoleToken(el, "agenda");
  });
  const fromElements = extracted
    .map((el) => safeText(el.content))
    .join("\n")
    .split("\n")
    .map((x) => x.replace(/^[\u2022\-0-9\.\s]+/, "").trim())
    .filter(Boolean);
  const items = safeItemsArray(ctx.slideObj, fromElements.length ? fromElements : ["Define problem", "Assess options", "Align on decision"]);
  const slots = Array.isArray(layout.items) ? layout.items : [];
  for (let i = 0; i < slots.length; i++) {
    const slot = slots[i];
    const label = itemText(items[i], ["title", "body", "text", "content"], `Item ${i + 1}`);
    addShape(
      ctx.slide,
      ShapeType.ellipse,
      {
        ...bboxToPptx(slot.num),
        fill: { color: ctx.styles.color("primary", "2563EB") },
        line: { color: ctx.styles.color("primary", "2563EB"), width: 0 },
      },
      ctx,
      slotEl(`agenda_num_${i + 1}`, "shape")
    );
    drawTextSlot(
      ctx,
      `agenda_num_label_${i + 1}`,
      slot.num,
      String(i + 1),
      {
        fontFace: ctx.styles.font("headline").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 14),
        bold: true,
        color: "FFFFFF",
        align: "center",
        valign: "mid",
      },
      "number"
    );
    drawTextSlot(
      ctx,
      `agenda_text_${i + 1}`,
      slot.text,
      label,
      {
        fontFace: ctx.styles.font("body").family,
        fontSize: asNum(ctx.tokens.sizes?.body, 20),
        color: ctx.styles.color("fg", "111827"),
        valign: "mid",
      }
    );
  }
  drawFooterIfAny(ctx, layout.footer);
}

async function renderA4AssertionHeroVisual(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A4_assertion_hero_visual");
  if (!layout) return renderGenericFallback(ctx);
  const heroImage = firstImagePath(ctx.slideObj, ["hero", "visual"]) || firstImagePath(ctx.slideObj, []);
  const chart = firstElement(ctx.slideObj, (el) => typeValue(el) === "chart" || typeValue(el) === "sparkline");
  await drawImageSlot(ctx, "hero_visual", layout.hero_visual, chart ? null : heroImage, "surface");
  if (chart) {
    const chartClone = Object.assign({}, chart, { bbox: layout.hero_visual });
    await renderChartElement(ctx, chartClone);
  }
  drawTextSlot(
    ctx,
    "headline",
    layout.headline,
    firstText(ctx.slideObj, ["headline", "title"], ["headline", "text"], ctx.slideObj?.headline || ""),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h2, 30),
      bold: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    },
    "headline"
  );
  drawTextSlot(
    ctx,
    "supporting",
    layout.supporting,
    firstText(ctx.slideObj, ["supporting", "body", "subtitle"], ["text", "caption"], ""),
    {
      fontFace: ctx.styles.font("body").family,
      fontSize: asNum(ctx.tokens.sizes?.body, 20),
      color: ctx.styles.color("fg", "111827"),
      valign: "top",
    }
  );
  drawFooterIfAny(ctx, layout.footer);
}

function panelContent(slideObj, token, fallback = "") {
  const panel = firstElement(slideObj, (el) => hasRoleToken(el, token) && (typeValue(el) === "card" || typeValue(el) === "panel"));
  if (panel && Array.isArray(panel.children) && panel.children.length) {
    return panel.children.map((c) => safeText(c.content)).filter(Boolean).join("\n");
  }
  const lines = listElements(slideObj, (el) => hasRoleToken(el, token) && (typeValue(el) === "text" || typeValue(el) === "caption"))
    .map((el) => safeText(el.content))
    .filter(Boolean);
  return lines.length ? lines.join("\n") : fallback;
}

async function renderA5Split5050(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A5_split_50_50");
  if (!layout) return renderGenericFallback(ctx);
  drawTextSlot(
    ctx,
    "headline",
    layout.headline,
    firstText(ctx.slideObj, ["headline", "title"], ["headline", "text"], ctx.slideObj?.headline || ""),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h2, 30),
      bold: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    },
    "headline"
  );
  const leftText = panelContent(ctx.slideObj, "left", safeText(ctx.slideObj?.left || ""));
  const rightText = panelContent(ctx.slideObj, "right", safeText(ctx.slideObj?.right || ""));
  addCard(ctx.slide, layout.left_panel, ctx.styles, {}, ctx, slotEl("left_panel", "card"));
  addCard(ctx.slide, layout.right_panel, ctx.styles, {}, ctx, slotEl("right_panel", "card"));
  drawTextSlot(
    ctx,
    "left_panel_text",
    { x: layout.left_panel.x + 0.25, y: layout.left_panel.y + 0.2, w: layout.left_panel.w - 0.5, h: layout.left_panel.h - 0.4 },
    leftText || "Left panel",
    {
      fontFace: ctx.styles.font("body").family,
      fontSize: asNum(ctx.tokens.sizes?.body, 20),
      color: ctx.styles.color("fg", "111827"),
      valign: "top",
    }
  );
  drawTextSlot(
    ctx,
    "right_panel_text",
    { x: layout.right_panel.x + 0.25, y: layout.right_panel.y + 0.2, w: layout.right_panel.w - 0.5, h: layout.right_panel.h - 0.4 },
    rightText || "Right panel",
    {
      fontFace: ctx.styles.font("body").family,
      fontSize: asNum(ctx.tokens.sizes?.body, 20),
      color: ctx.styles.color("fg", "111827"),
      valign: "top",
    }
  );
  drawFooterIfAny(ctx, layout.footer);
}

async function renderA6Split3070(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A6_split_30_70");
  if (!layout) return renderGenericFallback(ctx);
  drawTextSlot(
    ctx,
    "headline",
    layout.headline,
    firstText(ctx.slideObj, ["headline", "title"], ["headline", "text"], ctx.slideObj?.headline || ""),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h2, 30),
      bold: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    },
    "headline"
  );
  addCard(
    ctx.slide,
    layout.sidebar,
    ctx.styles,
    { fill: "annotation", stroke: "border" },
    ctx,
    slotEl("sidebar", "card")
  );
  addCard(ctx.slide, layout.main, ctx.styles, {}, ctx, slotEl("main", "card"));
  drawTextSlot(
    ctx,
    "sidebar_text",
    { x: layout.sidebar.x + 0.2, y: layout.sidebar.y + 0.2, w: layout.sidebar.w - 0.4, h: layout.sidebar.h - 0.4 },
    panelContent(ctx.slideObj, "sidebar", safeText(ctx.slideObj?.sidebar || "")),
    {
      fontFace: ctx.styles.font("body").family,
      fontSize: asNum(ctx.tokens.sizes?.caption, 14),
      color: ctx.styles.color("fg", "111827"),
      valign: "top",
    }
  );
  const mainImage = firstImagePath(ctx.slideObj, ["main", "hero", "visual"]) || firstImagePath(ctx.slideObj, []);
  await drawImageSlot(
    ctx,
    "main_visual",
    { x: layout.main.x + 0.2, y: layout.main.y + 0.2, w: layout.main.w - 0.4, h: layout.main.h - 0.4 },
    mainImage,
    "surface"
  );
  const mainText = panelContent(ctx.slideObj, "main", safeText(ctx.slideObj?.main || ""));
  if (mainText) {
    drawTextSlot(
      ctx,
      "main_text",
      { x: layout.main.x + 0.25, y: layout.main.y + 0.22, w: layout.main.w - 0.5, h: 0.8 },
      mainText,
      {
        fontFace: ctx.styles.font("body").family,
        fontSize: asNum(ctx.tokens.sizes?.body, 20),
        color: ctx.styles.color("fg", "111827"),
        valign: "top",
      }
    );
  }
  drawFooterIfAny(ctx, layout.footer);
}

async function renderA7BigNumberCallout(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A7_big_number_callout");
  if (!layout) return renderGenericFallback(ctx);
  drawTextSlot(
    ctx,
    "headline",
    layout.headline,
    firstText(ctx.slideObj, ["headline", "title"], ["headline", "text"], ctx.slideObj?.headline || ""),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h2, 30),
      bold: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    },
    "headline"
  );
  const heroMetric =
    firstText(ctx.slideObj, ["hero_metric", "metric", "kpi"], ["number", "metric", "kpi", "text"], "") ||
    safeText(ctx.slideObj?.metric || ctx.slideObj?.value || "");
  drawTextSlot(
    ctx,
    "hero_metric",
    layout.hero_metric,
    heroMetric || "0",
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: Math.max(72, asNum(ctx.tokens.sizes?.h1, 40) * 2),
      bold: true,
      color: ctx.styles.color("primary", "2563EB"),
      valign: "mid",
    },
    "number"
  );
  drawTextSlot(
    ctx,
    "supporting",
    layout.supporting,
    firstText(ctx.slideObj, ["supporting", "body"], ["text", "caption"], ""),
    {
      fontFace: ctx.styles.font("body").family,
      fontSize: asNum(ctx.tokens.sizes?.body, 20),
      color: ctx.styles.color("fg", "111827"),
      valign: "top",
    }
  );
  drawFooterIfAny(ctx, layout.footer);
}

async function renderA8IconGrid(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A8_icon_grid");
  if (!layout) return renderGenericFallback(ctx);
  drawTextSlot(
    ctx,
    "headline",
    layout.headline,
    firstText(ctx.slideObj, ["headline", "title"], ["headline", "text"], ctx.slideObj?.headline || ""),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h2, 30),
      bold: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    },
    "headline"
  );
  const items = safeItemsArray(ctx.slideObj, []);
  const slots = Array.isArray(layout.items) ? layout.items : [];
  for (let i = 0; i < slots.length; i++) {
    const item = items[i] || {};
    const slot = slots[i];
    addCard(ctx.slide, slot.cell, ctx.styles, {}, ctx, slotEl(`icon_cell_${i + 1}`, "card"));
    // v1-update merge: try SVG icon, fall back to colored ellipse
    const iconName = item.icon || item.icon_name || item.iconName || null;
    renderIconInSlot(ctx, `icon_marker_${i + 1}`, slot.icon, iconName, {
      color: `accent_${(i % 2) + 1}`,
    });
    drawTextSlot(
      ctx,
      `icon_title_${i + 1}`,
      slot.title,
      itemText(item, ["title", "label", "name", "text", "content"], `Item ${i + 1}`),
      {
        fontFace: ctx.styles.font("headline").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 14),
        bold: true,
        color: ctx.styles.color("fg", "111827"),
      }
    );
    drawTextSlot(
      ctx,
      `icon_body_${i + 1}`,
      slot.body,
      itemText(item, ["body", "description", "detail", "content"], ""),
      {
        fontFace: ctx.styles.font("body").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 13),
        color: ctx.styles.color("muted", "6B7280"),
        valign: "top",
      }
    );
  }
  drawFooterIfAny(ctx, layout.footer);
}

function deltaColor(ctx, deltaText) {
  const t = safeText(deltaText).trim();
  if (!t) return ctx.styles.color("muted", "6B7280");
  if (/^\+/.test(t) || /(improv|increase|up)/i.test(t)) return ctx.styles.color("good", "16A34A");
  if (/^-/.test(t) || /(decline|down|drop|risk)/i.test(t)) return ctx.styles.color("bad", "DC2626");
  return ctx.styles.color("warn", "F59E0B");
}

async function renderA9CardGrid(ctx) {
  const { variantKey, layout } = getArchetypeLayout(ctx, "A9_card_grid");
  if (!layout) return renderGenericFallback(ctx);
  drawTextSlot(
    ctx,
    "headline",
    layout.headline,
    firstText(ctx.slideObj, ["headline", "title"], ["headline", "text"], ctx.slideObj?.headline || ""),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h2, 30),
      bold: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    },
    "headline"
  );
  const items = safeItemsArray(ctx.slideObj, []);
  if (variantKey === "6_kpi_tiles" && Array.isArray(layout.kpi_tiles)) {
    for (let i = 0; i < layout.kpi_tiles.length; i++) {
      const tile = layout.kpi_tiles[i];
      const item = items[i] || {};
      addCard(
        ctx.slide,
        tile.box,
        ctx.styles,
        { fill: "surface", stroke: "border" },
        ctx,
        slotEl(`kpi_tile_${i + 1}`, "card")
      );
      drawTextSlot(
        ctx,
        `kpi_metric_${i + 1}`,
        tile.metric,
        itemText(item, ["metric", "value", "content"], "0"),
        {
          fontFace: ctx.styles.font("headline").family,
          fontSize: 40,
          bold: true,
          color: ctx.styles.color("primary", "2563EB"),
          valign: "mid",
        },
        "metric"
      );
      drawTextSlot(
        ctx,
        `kpi_label_${i + 1}`,
        tile.label,
        itemText(item, ["label", "title", "name", "text"], `KPI ${i + 1}`),
        {
          fontFace: ctx.styles.font("body").family,
          fontSize: asNum(ctx.tokens.sizes?.caption, 12),
          color: ctx.styles.color("muted", "6B7280"),
          valign: "mid",
        }
      );
      const delta = itemText(item, ["delta", "change", "trend"], "");
      drawTextSlot(
        ctx,
        `kpi_delta_${i + 1}`,
        tile.delta,
        delta,
        {
          fontFace: ctx.styles.font("body").family,
          fontSize: asNum(ctx.tokens.sizes?.caption, 12),
          color: deltaColor(ctx, delta),
          bold: true,
          valign: "mid",
        }
      );
    }
  } else if (Array.isArray(layout.cards)) {
    for (let i = 0; i < layout.cards.length; i++) {
      const card = layout.cards[i];
      const item = items[i] || {};
      const isAccent = i % 2 === 1;
      addCard(
        ctx.slide,
        card.box,
        ctx.styles,
        { fill: isAccent ? "annotation" : "surface", stroke: isAccent ? "primary_light" : "border" },
        ctx,
        slotEl(`card_${i + 1}`, "card")
      );
      drawTextSlot(
        ctx,
        `card_title_${i + 1}`,
        card.title,
        itemText(item, ["title", "label", "name", "text", "content"], `Card ${i + 1}`),
        {
          fontFace: ctx.styles.font("headline").family,
          fontSize: asNum(ctx.tokens.sizes?.body, 20),
          bold: true,
          color: isAccent ? ctx.styles.color("primary_dark", "1E3A8A") : ctx.styles.color("fg", "111827"),
          valign: "mid",
        }
      );
      drawTextSlot(
        ctx,
        `card_body_${i + 1}`,
        card.body,
        itemText(item, ["body", "description", "detail", "content"], ""),
        {
          fontFace: ctx.styles.font("body").family,
          fontSize: asNum(ctx.tokens.sizes?.caption, 14),
          color: ctx.styles.color("muted", "6B7280"),
          valign: "top",
        }
      );
    }
  }
  drawFooterIfAny(ctx, layout.footer);
}

function comparisonCardText(cardElement, fallbackTitle, fallbackBody) {
  if (!cardElement || !Array.isArray(cardElement.children)) {
    return { title: fallbackTitle, body: fallbackBody };
  }
  const title = cardElement.children.find((c) => hasRoleToken(c, "h2") || hasRoleToken(c, "title"));
  const body = cardElement.children.find((c) => hasRoleToken(c, "body")) || cardElement.children.find((c) => typeValue(c) === "text");
  return {
    title: safeText(title?.content || fallbackTitle),
    body: safeText(body?.content || fallbackBody),
  };
}

async function renderA10Comparison(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A10_comparison");
  if (!layout) return renderGenericFallback(ctx);
  drawTextSlot(
    ctx,
    "headline",
    layout.headline,
    firstText(ctx.slideObj, ["headline", "title"], ["headline", "text"], ctx.slideObj?.headline || ""),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h2, 30),
      bold: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    },
    "headline"
  );
  const leftEl = firstElement(ctx.slideObj, (el) => hasRoleToken(el, "left") && (typeValue(el) === "card" || typeValue(el) === "panel"));
  const rightEl = firstElement(ctx.slideObj, (el) => hasRoleToken(el, "right") && (typeValue(el) === "card" || typeValue(el) === "panel"));
  const left = comparisonCardText(leftEl, "Left", "");
  const right = comparisonCardText(rightEl, "Right", "");
  addCard(
    ctx.slide,
    layout.left_card.box,
    ctx.styles,
    { fill: "primary_light", stroke: "primary" },
    ctx,
    slotEl("left_card_box", "card")
  );
  addCard(
    ctx.slide,
    layout.right_card.box,
    ctx.styles,
    { fill: "surface", stroke: "border" },
    ctx,
    slotEl("right_card_box", "card")
  );
  drawTextSlot(
    ctx,
    "left_card_title",
    layout.left_card.title,
    left.title,
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.body, 20),
      bold: true,
      color: ctx.styles.color("primary_dark", "1E40AF"),
      valign: "mid",
    }
  );
  drawTextSlot(
    ctx,
    "left_card_body",
    layout.left_card.body,
    left.body,
    {
      fontFace: ctx.styles.font("body").family,
      fontSize: asNum(ctx.tokens.sizes?.caption, 14),
      color: ctx.styles.color("fg", "111827"),
      valign: "top",
    }
  );
  drawTextSlot(
    ctx,
    "right_card_title",
    layout.right_card.title,
    right.title,
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.body, 20),
      bold: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    }
  );
  drawTextSlot(
    ctx,
    "right_card_body",
    layout.right_card.body,
    right.body,
    {
      fontFace: ctx.styles.font("body").family,
      fontSize: asNum(ctx.tokens.sizes?.caption, 14),
      color: ctx.styles.color("fg", "111827"),
      valign: "top",
    }
  );
}

async function renderA11QuadrantMatrix(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A11_quadrant_matrix");
  if (!layout) return renderGenericFallback(ctx);
  drawTextSlot(
    ctx,
    "headline",
    layout.headline,
    firstText(ctx.slideObj, ["headline", "title"], ["headline", "text"], ctx.slideObj?.headline || ""),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h2, 30),
      bold: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    },
    "headline"
  );
  addShape(
    ctx.slide,
    ShapeType.rect,
    {
      ...bboxToPptx(layout.matrix),
      fill: { color: ctx.styles.color("bg", "FFFFFF"), transparency: 5 },
      line: { color: ctx.styles.color("border", "D1D5DB"), width: 1 },
    },
    ctx,
    slotEl("matrix_grid", "shape")
  );
  addConnector(
    ctx.slide,
    {
      x: layout.matrix.x + layout.matrix.w / 2,
      y: layout.matrix.y,
      w: 0,
      h: layout.matrix.h,
      line: { color: ctx.styles.color("border", "D1D5DB"), width: 1 },
    },
    ctx.styles,
    ctx,
    slotEl("matrix_vline", "connector")
  );
  addConnector(
    ctx.slide,
    {
      x: layout.matrix.x,
      y: layout.matrix.y + layout.matrix.h / 2,
      w: layout.matrix.w,
      h: 0,
      line: { color: ctx.styles.color("border", "D1D5DB"), width: 1 },
    },
    ctx.styles,
    ctx,
    slotEl("matrix_hline", "connector")
  );
  drawTextSlot(
    ctx,
    "axis_x_label",
    layout.axis_x_label,
    firstText(ctx.slideObj, ["axis_x", "x_axis"], ["axis", "text"], "X axis"),
    {
      fontFace: ctx.styles.font("body").family,
      fontSize: asNum(ctx.tokens.sizes?.caption, 13),
      color: ctx.styles.color("muted", "6B7280"),
      align: "center",
      valign: "mid",
    }
  );
  drawTextSlot(
    ctx,
    "axis_y_label",
    layout.axis_y_label,
    firstText(ctx.slideObj, ["axis_y", "y_axis"], ["axis", "text"], "Y axis"),
    {
      fontFace: ctx.styles.font("body").family,
      fontSize: asNum(ctx.tokens.sizes?.caption, 13),
      color: ctx.styles.color("muted", "6B7280"),
      align: "center",
      valign: "mid",
    }
  );
  const q = layout.quadrant_labels || {};
  drawTextSlot(ctx, "quadrant_q1", q.q1, safeText(ctx.slideObj?.quadrant_labels?.q1 || "Q1"), { fontFace: ctx.styles.font("body").family, fontSize: 12, color: ctx.styles.color("muted", "6B7280"), align: "center" });
  drawTextSlot(ctx, "quadrant_q2", q.q2, safeText(ctx.slideObj?.quadrant_labels?.q2 || "Q2"), { fontFace: ctx.styles.font("body").family, fontSize: 12, color: ctx.styles.color("muted", "6B7280"), align: "center" });
  drawTextSlot(ctx, "quadrant_q3", q.q3, safeText(ctx.slideObj?.quadrant_labels?.q3 || "Q3"), { fontFace: ctx.styles.font("body").family, fontSize: 12, color: ctx.styles.color("muted", "6B7280"), align: "center" });
  drawTextSlot(ctx, "quadrant_q4", q.q4, safeText(ctx.slideObj?.quadrant_labels?.q4 || "Q4"), { fontFace: ctx.styles.font("body").family, fontSize: 12, color: ctx.styles.color("muted", "6B7280"), align: "center" });
  const points = Array.isArray(ctx.slideObj?.points) ? ctx.slideObj.points : [];
  const marker = asNum(layout.dynamic_points?.point_marker_size_in, 0.12);
  for (let i = 0; i < points.length; i++) {
    const p = points[i] || {};
    const x = layout.matrix.x + asNum(p.x, 0.5) * layout.matrix.w;
    const y = layout.matrix.y + (1 - asNum(p.y, 0.5)) * layout.matrix.h;
    addShape(
      ctx.slide,
      ShapeType.ellipse,
      {
        x: x - marker / 2,
        y: y - marker / 2,
        w: marker,
        h: marker,
        fill: { color: ctx.styles.color("accent_1", "0EA5E9") },
        line: { color: ctx.styles.color("accent_1", "0EA5E9"), width: 0 },
      },
      ctx,
      slotEl(`matrix_point_${i + 1}`, "shape")
    );
    if (p.label) {
      drawTextSlot(
        ctx,
        `matrix_point_label_${i + 1}`,
        {
          x: x + 0.06,
          y: y - 0.12,
          w: asNum(layout.dynamic_points?.label_box?.w, 1.2),
          h: asNum(layout.dynamic_points?.label_box?.h, 0.3),
        },
        safeText(p.label),
        {
          fontFace: ctx.styles.font("body").family,
          fontSize: asNum(ctx.tokens.sizes?.caption, 12),
          color: ctx.styles.color("fg", "111827"),
        }
      );
    }
  }
  drawTextSlot(
    ctx,
    "notes",
    layout.notes,
    firstText(ctx.slideObj, ["notes", "footer"], ["text", "caption", "footer"], ""),
    {
      fontFace: ctx.styles.font("body").family,
      fontSize: asNum(ctx.tokens.sizes?.caption, 12),
      color: ctx.styles.color("muted", "6B7280"),
      valign: "top",
    }
  );
  drawFooterIfAny(ctx, layout.footer);
}

async function renderA12TimelineHorizontal(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A12_timeline_horizontal");
  if (!layout) return renderGenericFallback(ctx);
  drawTextSlot(
    ctx,
    "headline",
    layout.headline,
    firstText(ctx.slideObj, ["headline", "title"], ["headline", "text"], ctx.slideObj?.headline || ""),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h2, 30),
      bold: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    },
    "headline"
  );
  addShape(
    ctx.slide,
    ShapeType.line,
    {
      x: layout.rail.x,
      y: layout.rail.y,
      w: layout.rail.w,
      h: 0,
      line: { color: ctx.styles.color("primary_light", "93C5FD"), width: 1.6 },
    },
    ctx,
    slotEl("timeline_rail", "line")
  );
  const nodes = safeItemsArray(
    ctx.slideObj,
    listElements(ctx.slideObj, (el) => typeValue(el) === "node" || typeValue(el) === "timeline_node")
  );
  const nodeSlots = Array.isArray(layout.nodes) ? layout.nodes : [];
  for (let i = 0; i < nodeSlots.length; i++) {
    const slot = nodeSlots[i];
    const node = nodes[i] || {};
    const parsed = parseNodeText(itemText(node, ["content", "text", "title", "body"], ""));
    addShape(
      ctx.slide,
      ShapeType.line,
      {
        ...lineFromPoints(slot.connector?.from, slot.connector?.to),
        line: { color: ctx.styles.color("primary_light", "BFDBFE"), width: 1.2 },
      },
      ctx,
      slotEl(`timeline_connector_${i + 1}`, "connector")
    );
    addShape(
      ctx.slide,
      ShapeType.ellipse,
      {
        ...bboxToPptx(slot.dot),
        fill: { color: ctx.styles.accentColor((i % 2) + 1) },
        line: { color: "FFFFFF", width: 1 },
      },
      ctx,
      slotEl(`timeline_dot_${i + 1}`, "shape")
    );
    addCard(
      ctx.slide,
      slot.card,
      ctx.styles,
      { fill: i % 2 ? "annotation" : "surface", stroke: "border" },
      ctx,
      slotEl(`timeline_card_${i + 1}`, "card")
    );
    drawTextSlot(
      ctx,
      `timeline_date_${i + 1}`,
      slot.date,
      itemText(node, ["date", "title", "label"], parsed.primary || `Step ${i + 1}`),
      {
        fontFace: ctx.styles.font("headline").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 13),
        bold: true,
        color: ctx.styles.color("primary", "2563EB"),
      }
    );
    drawTextSlot(
      ctx,
      `timeline_body_${i + 1}`,
      slot.body,
      itemText(node, ["body", "description", "content"], parsed.secondary || parsed.primary || ""),
      {
        fontFace: ctx.styles.font("body").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 12),
        color: ctx.styles.color("fg", "111827"),
        valign: "top",
      }
    );
  }
  drawFooterIfAny(ctx, layout.footer);
}

async function renderA13TimelineVertical(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A13_timeline_vertical");
  if (!layout) return renderGenericFallback(ctx);
  drawTextSlot(
    ctx,
    "headline",
    layout.headline,
    firstText(ctx.slideObj, ["headline", "title"], ["headline", "text"], ctx.slideObj?.headline || ""),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h2, 30),
      bold: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    },
    "headline"
  );
  addShape(
    ctx.slide,
    ShapeType.line,
    {
      x: layout.rail.x + layout.rail.w / 2,
      y: layout.rail.y,
      w: 0,
      h: layout.rail.h,
      line: { color: ctx.styles.color("border", "D1D5DB"), width: 1.5 },
    },
    ctx,
    slotEl("timeline_rail", "line")
  );
  const nodes = safeItemsArrayByKeys(
    ctx.slideObj,
    ["timeline", "milestones", "steps", "nodes", "items"],
    listElements(ctx.slideObj, (el) => typeValue(el) === "node" || typeValue(el) === "timeline_node")
  );
  const nodeSlots = Array.isArray(layout.nodes) ? layout.nodes : [];
  for (let i = 0; i < nodeSlots.length; i++) {
    const slot = nodeSlots[i];
    const node = nodes[i] || {};
    const parsed = parseNodeText(itemText(node, ["content", "text", "title", "body"], ""));
    const dotCenter = boxCenter(slot.dot);
    const cardEntry = { x: asNum(slot.card?.x, dotCenter.x), y: dotCenter.y };
    addConnector(
      ctx.slide,
      {
        ...lineFromPoints(dotCenter, cardEntry),
        line: { color: ctx.styles.color("border", "D1D5DB"), width: 1.1 },
      },
      ctx.styles,
      ctx,
      slotEl(`timeline_connector_${i + 1}`, "connector")
    );
    addShape(
      ctx.slide,
      ShapeType.ellipse,
      {
        ...bboxToPptx(slot.dot),
        fill: { color: ctx.styles.color("primary", "2563EB") },
        line: { color: ctx.styles.color("primary", "2563EB"), width: 0 },
      },
      ctx,
      slotEl(`timeline_dot_${i + 1}`, "shape")
    );
    addCard(
      ctx.slide,
      slot.card,
      ctx.styles,
      { fill: i % 2 ? "annotation" : "surface", stroke: "border" },
      ctx,
      slotEl(`timeline_card_${i + 1}`, "card")
    );
    drawTextSlot(
      ctx,
      `timeline_date_${i + 1}`,
      slot.title,
      itemText(node, ["date", "title", "label"], parsed.primary || `Step ${i + 1}`),
      {
        fontFace: ctx.styles.font("headline").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 13),
        bold: true,
        color: ctx.styles.color("primary", "2563EB"),
      }
    );
    drawTextSlot(
      ctx,
      `timeline_body_${i + 1}`,
      slot.body,
      itemText(node, ["body", "description", "content"], parsed.secondary || parsed.primary || ""),
      {
        fontFace: ctx.styles.font("body").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 12),
        color: ctx.styles.color("fg", "111827"),
        valign: "top",
      }
    );
  }
  drawFooterIfAny(ctx, layout.footer);
}

async function renderA14ProcessFlow(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A14_process_flow");
  if (!layout) return renderGenericFallback(ctx);
  drawTextSlot(
    ctx,
    "headline",
    layout.headline,
    firstText(ctx.slideObj, ["headline", "title"], ["headline", "text"], ctx.slideObj?.headline || ""),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h2, 30),
      bold: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    },
    "headline"
  );
  const steps = safeItemsArrayByKeys(
    ctx.slideObj,
    ["steps", "process", "items", "nodes"],
    listElements(ctx.slideObj, (el) => typeValue(el) === "step" || typeValue(el) === "process_step" || typeValue(el) === "node")
  );
  const stepSlots = Array.isArray(layout.steps) ? layout.steps : [];
  for (let i = 0; i < stepSlots.length; i++) {
    const slot = stepSlots[i];
    const step = steps[i] || {};
    addCard(
      ctx.slide,
      slot.card,
      ctx.styles,
      { fill: i % 2 ? "surface" : "annotation", stroke: "border" },
      ctx,
      slotEl(`process_card_${i + 1}`, "card")
    );
    addShape(
      ctx.slide,
      ShapeType.ellipse,
      {
        ...bboxToPptx(slot.step_num),
        fill: { color: ctx.styles.color("primary", "2563EB") },
        line: { color: ctx.styles.color("primary", "2563EB"), width: 0 },
      },
      ctx,
      slotEl(`process_step_badge_${i + 1}`, "shape")
    );
    drawTextSlot(
      ctx,
      `process_step_num_${i + 1}`,
      slot.step_num,
      itemText(step, ["step", "index", "number"], `${i + 1}`),
      {
        fontFace: ctx.styles.font("headline").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 13),
        bold: true,
        color: "FFFFFF",
        align: "center",
        valign: "mid",
      },
      "number"
    );
    drawTextSlot(
      ctx,
      `process_step_title_${i + 1}`,
      slot.title,
      itemText(step, ["title", "label", "name", "text"], `Step ${i + 1}`),
      {
        fontFace: ctx.styles.font("headline").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 14),
        bold: true,
        color: ctx.styles.color("fg", "111827"),
        valign: "mid",
      }
    );
    drawTextSlot(
      ctx,
      `process_step_body_${i + 1}`,
      slot.body,
      itemText(step, ["body", "description", "detail", "content"], ""),
      {
        fontFace: ctx.styles.font("body").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 12),
        color: ctx.styles.color("muted", "6B7280"),
        valign: "top",
      }
    );
    if (slot.connector_to_next && slot.connector_to_next.from && slot.connector_to_next.to) {
      addConnector(
        ctx.slide,
        {
          ...lineFromPoints(slot.connector_to_next.from, slot.connector_to_next.to),
          line: {
            color: ctx.styles.color("border", "D1D5DB"),
            width: 1.3,
            endArrowType: "triangle",
          },
        },
        ctx.styles,
        ctx,
        slotEl(`process_connector_${i + 1}`, "connector")
      );
    }
  }
  drawFooterIfAny(ctx, layout.footer);
}

async function renderA15CycleLoop(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A15_cycle_loop");
  if (!layout) return renderGenericFallback(ctx);
  drawTextSlot(
    ctx,
    "headline",
    layout.headline,
    firstText(ctx.slideObj, ["headline", "title"], ["headline", "text"], ctx.slideObj?.headline || ""),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h2, 30),
      bold: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    },
    "headline"
  );
  addShape(
    ctx.slide,
    ShapeType.ellipse,
    {
      ...bboxToPptx(layout.diagram),
      fill: { color: ctx.styles.color("bg", "FFFFFF"), transparency: 100 },
      line: { color: ctx.styles.color("border", "D1D5DB"), width: 1.2, dash: "dash" },
    },
    ctx,
    slotEl("cycle_outline", "shape")
  );
  addCard(
    ctx.slide,
    layout.center_label,
    ctx.styles,
    { fill: "annotation", stroke: "primary", radius: 16 },
    ctx,
    slotEl("cycle_center_label_card", "card")
  );
  drawTextSlot(
    ctx,
    "cycle_center_label",
    layout.center_label,
    firstText(ctx.slideObj, ["center_label", "center", "hub", "title"], ["text", "headline"], safeText(ctx.slideObj?.center_label || "Cycle")),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.body, 20),
      bold: true,
      color: ctx.styles.color("primary_dark", "1E40AF"),
      align: "center",
      valign: "mid",
    }
  );
  const nodes = safeItemsArrayByKeys(
    ctx.slideObj,
    ["nodes", "steps", "items", "cycle"],
    listElements(ctx.slideObj, (el) => typeValue(el) === "node" || typeValue(el) === "step" || typeValue(el) === "card")
  );
  const nodeSlots = Array.isArray(layout.nodes) ? layout.nodes : [];
  for (let i = 0; i < nodeSlots.length; i++) {
    const slot = nodeSlots[i];
    const node = nodes[i] || {};
    addCard(ctx.slide, slot.card, ctx.styles, {}, ctx, slotEl(`cycle_node_card_${i + 1}`, "card"));
    drawTextSlot(
      ctx,
      `cycle_node_title_${i + 1}`,
      slot.title,
      itemText(node, ["title", "label", "name", "text", "content"], `Node ${i + 1}`),
      {
        fontFace: ctx.styles.font("headline").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 13),
        bold: true,
        color: ctx.styles.color("fg", "111827"),
        valign: "mid",
      }
    );
    drawTextSlot(
      ctx,
      `cycle_node_body_${i + 1}`,
      slot.body,
      itemText(node, ["body", "description", "detail", "content"], ""),
      {
        fontFace: ctx.styles.font("body").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 12),
        color: ctx.styles.color("muted", "6B7280"),
        valign: "top",
      }
    );
  }
  for (let i = 0; i < nodeSlots.length; i++) {
    const from = boxCenter(nodeSlots[i].card);
    const to = boxCenter(nodeSlots[(i + 1) % nodeSlots.length].card);
    addConnector(
      ctx.slide,
      {
        ...lineFromPoints(from, to),
        line: {
          color: ctx.styles.color("accent_1", "0EA5E9"),
          width: 1.15,
          endArrowType: "triangle",
        },
      },
      ctx.styles,
      ctx,
      slotEl(`cycle_arrow_${i + 1}`, "connector")
    );
  }
  drawFooterIfAny(ctx, layout.footer);
}

async function renderA16ArchitectureDiagram(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A16_architecture_diagram");
  if (!layout) return renderGenericFallback(ctx);
  drawTextSlot(
    ctx,
    "headline",
    layout.headline,
    firstText(ctx.slideObj, ["headline", "title"], ["headline", "text"], ctx.slideObj?.headline || ""),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h2, 30),
      bold: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    },
    "headline"
  );
  const components = safeItemsArrayByKeys(
    ctx.slideObj,
    ["components", "layers", "modules", "items", "cards"],
    listElements(ctx.slideObj, (el) => ["component", "node", "card", "panel", "box"].includes(typeValue(el)))
  );
  const componentSlots = Array.isArray(layout.components) ? layout.components : [];
  for (let i = 0; i < componentSlots.length; i++) {
    const slot = componentSlots[i];
    const component = components[i] || {};
    addCard(
      ctx.slide,
      slot.box,
      ctx.styles,
      { fill: i % 2 ? "surface" : "annotation", stroke: "border" },
      ctx,
      slotEl(`architecture_component_${i + 1}`, "card")
    );
    drawTextSlot(
      ctx,
      `architecture_component_title_${i + 1}`,
      slot.title,
      itemText(component, ["title", "label", "name", "text", "content"], `Component ${i + 1}`),
      {
        fontFace: ctx.styles.font("headline").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 14),
        bold: true,
        color: ctx.styles.color("fg", "111827"),
        valign: "mid",
      }
    );
    drawTextSlot(
      ctx,
      `architecture_component_body_${i + 1}`,
      slot.body,
      itemText(component, ["body", "description", "detail", "content"], ""),
      {
        fontFace: ctx.styles.font("body").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 12),
        color: ctx.styles.color("muted", "6B7280"),
        valign: "top",
      }
    );
  }
  const edges = normalizeEdgeList(ctx.slideObj);
  const toDraw = edges.length
    ? edges
    : componentSlots.slice(0, -1).map((_slot, idx) => ({ from: idx, to: idx + 1 }));
  for (let i = 0; i < toDraw.length; i++) {
    const edge = toDraw[i];
    const fromPoint = edge.fromPoint || resolveEdgeEndpoint(edge.from, componentSlots, components);
    const toPoint = edge.toPoint || resolveEdgeEndpoint(edge.to, componentSlots, components);
    if (!fromPoint || !toPoint) continue;
    addConnector(
      ctx.slide,
      {
        ...lineFromPoints(fromPoint, toPoint),
        line: {
          color: ctx.styles.color("border", "D1D5DB"),
          width: 1.15,
          endArrowType: "triangle",
        },
      },
      ctx.styles,
      ctx,
      slotEl(`architecture_connector_${i + 1}`, "connector")
    );
  }
  drawFooterIfAny(ctx, layout.footer);
}

async function renderA17ChartFirstInsight(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A17_chart_first_insight");
  if (!layout) return renderGenericFallback(ctx);
  drawTextSlot(
    ctx,
    "headline",
    layout.headline,
    firstText(ctx.slideObj, ["headline", "title"], ["headline", "text"], ctx.slideObj?.headline || ""),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h2, 30),
      bold: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    },
    "headline"
  );
  const chartEl = firstElement(ctx.slideObj, (el) => typeValue(el) === "chart" || typeValue(el) === "sparkline");
  await renderChartElement(
    ctx,
    Object.assign(
      {
        semantic_type: "chart",
        semantic_role: "chart",
        bbox: layout.chart,
        chartSpec: ctx.slideObj?.chartSpec || ctx.slideObj?.chart || ctx.slideObj?.data || {},
      },
      chartEl || {},
      { bbox: layout.chart }
    )
  );
  addCard(
    ctx.slide,
    layout.callout,
    ctx.styles,
    { fill: "annotation", stroke: "primary", radius: 14 },
    ctx,
    slotEl("insight_callout", "card")
  );
  drawTextSlot(
    ctx,
    "insight_callout_text",
    {
      x: layout.callout.x + 0.18,
      y: layout.callout.y + 0.18,
      w: layout.callout.w - 0.36,
      h: layout.callout.h - 0.36,
    },
    firstText(
      ctx.slideObj,
      ["callout", "insight", "metric", "kpi"],
      ["callout", "annotation", "number", "metric", "text"],
      safeText(ctx.slideObj?.insight || ctx.slideObj?.metric || "")
    ),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h2, 28),
      bold: true,
      color: ctx.styles.color("primary_dark", "1E40AF"),
      valign: "mid",
    },
    "callout"
  );
  addShape(
    ctx.slide,
    ShapeType.roundRect,
    {
      x: layout.callout.x + 0.08,
      y: layout.callout.y + 0.08,
      w: Math.max(0.2, layout.callout.w - 0.16),
      h: 0.05,
      rectRadius: 0.01,
      fill: { color: ctx.styles.color("primary", "2563EB") },
      line: { color: ctx.styles.color("primary", "2563EB"), width: 0 },
    },
    ctx,
    slotEl("insight_callout_accent", "shape")
  );
  addCard(
    ctx.slide,
    layout.takeaway,
    ctx.styles,
    { fill: "surface", stroke: "border", radius: 12 },
    ctx,
    slotEl("chart_takeaway", "card")
  );
  drawTextSlot(
    ctx,
    "chart_takeaway_text",
    {
      x: layout.takeaway.x + 0.16,
      y: layout.takeaway.y + 0.15,
      w: layout.takeaway.w - 0.32,
      h: layout.takeaway.h - 0.3,
    },
    firstText(
      ctx.slideObj,
      ["takeaway", "summary", "so_what", "recommendation", "body"],
      ["text", "caption"],
      ""
    ),
    {
      fontFace: ctx.styles.font("body").family,
      fontSize: asNum(ctx.tokens.sizes?.caption, 13),
      color: ctx.styles.color("fg", "111827"),
      valign: "top",
    }
  );
}

async function renderA18AnnotatedChart(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A18_annotated_chart");
  if (!layout) return renderGenericFallback(ctx);
  drawTextSlot(
    ctx,
    "headline",
    layout.headline,
    firstText(ctx.slideObj, ["headline", "title"], ["headline", "text"], ctx.slideObj?.headline || ""),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h2, 30),
      bold: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    },
    "headline"
  );
  const chartEl = firstElement(ctx.slideObj, (el) => typeValue(el) === "chart" || typeValue(el) === "sparkline");
  await renderChartElement(
    ctx,
    Object.assign(
      {
        semantic_type: "chart",
        semantic_role: "chart",
        bbox: layout.chart,
        chartSpec: ctx.slideObj?.chartSpec || ctx.slideObj?.chart || ctx.slideObj?.data || {},
      },
      chartEl || {},
      { bbox: layout.chart }
    )
  );
  addCard(
    ctx.slide,
    layout.callout_card.box,
    ctx.styles,
    { fill: "annotation", stroke: "primary", radius: 12 },
    ctx,
    slotEl("annotated_chart_callout_card", "card")
  );
  addShape(
    ctx.slide,
    ShapeType.roundRect,
    {
      x: layout.callout_card.box.x + 0.08,
      y: layout.callout_card.box.y + 0.08,
      w: Math.max(0.2, layout.callout_card.box.w - 0.16),
      h: 0.05,
      rectRadius: 0.01,
      fill: { color: ctx.styles.color("primary", "2563EB") },
      line: { color: ctx.styles.color("primary", "2563EB"), width: 0 },
    },
    ctx,
    slotEl("annotated_chart_callout_accent", "shape")
  );
  drawTextSlot(
    ctx,
    "annotated_chart_callout_title",
    layout.callout_card.title,
    firstText(
      ctx.slideObj,
      ["callout_title", "callout", "insight", "annotation"],
      ["callout", "annotation", "headline", "text"],
      "Insight"
    ),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.caption, 14),
      bold: true,
      color: ctx.styles.color("primary_dark", "1E40AF"),
      valign: "mid",
    }
  );
  drawTextSlot(
    ctx,
    "annotated_chart_callout_body",
    layout.callout_card.body,
    firstText(
      ctx.slideObj,
      ["callout_body", "annotation_body", "supporting"],
      ["annotation", "text", "caption"],
      ""
    ),
    {
      fontFace: ctx.styles.font("body").family,
      fontSize: asNum(ctx.tokens.sizes?.caption, 12),
      color: ctx.styles.color("fg", "111827"),
      valign: "top",
    }
  );
  addCard(
    ctx.slide,
    layout.bullets_card.box,
    ctx.styles,
    { fill: "surface", stroke: "border", radius: 12 },
    ctx,
    slotEl("annotated_chart_bullets_card", "card")
  );
  drawTextSlot(
    ctx,
    "annotated_chart_bullets_title",
    layout.bullets_card.title,
    firstText(
      ctx.slideObj,
      ["bullets_title", "key_points", "summary"],
      ["headline", "text", "caption"],
      "Key points"
    ),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.caption, 14),
      bold: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    }
  );
  const bulletItems = safeItemsArrayByKeys(ctx.slideObj, ["bullets", "key_points", "points", "items"], [])
    .map((item) => itemText(item, ["text", "content", "title", "label", "body"], ""))
    .filter(Boolean);
  const bulletBody =
    bulletItems.length
      ? bulletItems.map((line) => `- ${line}`).join("\n")
      : firstText(ctx.slideObj, ["bullets", "points", "body"], ["text", "caption"], "");
  drawTextSlot(
    ctx,
    "annotated_chart_bullets_body",
    layout.bullets_card.body,
    bulletBody,
    {
      fontFace: ctx.styles.font("body").family,
      fontSize: asNum(ctx.tokens.sizes?.caption, 12),
      color: ctx.styles.color("fg", "111827"),
      valign: "top",
    }
  );
  drawFooterIfAny(ctx, layout.footer);
}

async function renderA19TableLight(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A19_table_light");
  if (!layout) return renderGenericFallback(ctx);
  drawTextSlot(
    ctx,
    "headline",
    layout.headline,
    firstText(ctx.slideObj, ["headline", "title"], ["headline", "text"], ctx.slideObj?.headline || ""),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h2, 30),
      bold: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    },
    "headline"
  );
  const tableEl = firstElement(ctx.slideObj, (el) => typeValue(el) === "table");
  const tableObj = tableEl || ctx.slideObj?.table || {};
  const rawRows =
    (Array.isArray(tableObj.rows) && tableObj.rows) ||
    (Array.isArray(tableObj.data) && tableObj.data) ||
    (Array.isArray(ctx.slideObj?.rows) && ctx.slideObj.rows) ||
    [];
  if (!rawRows.length) {
    addCard(ctx.slide, layout.table, ctx.styles, {}, ctx, slotEl("table_box", "card"));
    drawTextSlot(
      ctx,
      "table_placeholder",
      layout.table,
      "[table]",
      {
        fontFace: ctx.styles.font("body").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 13),
        color: ctx.styles.color("muted", "6B7280"),
        align: "center",
        valign: "mid",
      }
    );
  } else {
    addCard(
      ctx.slide,
      layout.table,
      ctx.styles,
      { fill: "surface", stroke: "border", radius: 10, shadow: false },
      ctx,
      slotEl("table_backplate", "card")
    );
    const requestedCols =
      (Array.isArray(tableObj.columns) && tableObj.columns) ||
      (Array.isArray(tableObj.headers) && tableObj.headers) ||
      (Array.isArray(ctx.slideObj?.columns) && ctx.slideObj.columns) ||
      [];
    const inferredKeys =
      !requestedCols.length && isObject(rawRows[0]) ? Object.keys(rawRows[0]) : [];
    const columns = requestedCols.length ? requestedCols : inferredKeys;
    const headerLabels = columns.map((col, idx) => {
      if (typeof col === "string") return col;
      if (isObject(col)) return safeText(col.label || col.title || col.name || col.key || `Col ${idx + 1}`);
      return `Col ${idx + 1}`;
    });
    const columnKeys = columns.map((col, idx) => {
      if (typeof col === "string") return col;
      if (isObject(col)) return col.key || col.id || col.name || `col_${idx + 1}`;
      return `col_${idx + 1}`;
    });
    const hasExplicitHeader = !!columns.length;
    const headerFill = ctx.styles.color("primary", "2563EB");
    const zebraA = ctx.styles.color("bg", "FFFFFF");
    const zebraB = ctx.styles.color("surface", "F8FAFC");
    const borderColor = ctx.styles.color("border", "D1D5DB");
    const rows = [];
    const matrixRows = rawRows.map((row) => {
      if (Array.isArray(row)) return row;
      if (isObject(row)) {
        if (columnKeys.length) return columnKeys.map((key) => row[key]);
        return Object.values(row);
      }
      return [row];
    });
    if (hasExplicitHeader) {
      rows.push(
        headerLabels.map((text) => ({
          text: safeText(text),
          options: {
            bold: true,
            color: "FFFFFF",
            fill: headerFill,
            align: "left",
            valign: "mid",
            border: { pt: 1, color: borderColor },
          },
        }))
      );
    }
    for (let r = 0; r < matrixRows.length; r++) {
      const bg = r % 2 ? zebraB : zebraA;
      rows.push(
        matrixRows[r].map((cell) => ({
          text: safeText(cell),
          options: {
            color: ctx.styles.color("fg", "111827"),
            fill: bg,
            align: "left",
            valign: "mid",
            border: { pt: 1, color: borderColor },
          },
        }))
      );
    }
    addTable(
      ctx.slide,
      rows,
      {
        ...bboxToPptx(layout.table),
        fontFace: ctx.styles.font("body").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 12),
        margin: 0.04,
        border: { pt: 1, color: borderColor },
      },
      ctx,
      slotEl("table", "table")
    );
  }
  drawTextSlot(
    ctx,
    "table_footnote",
    layout.footnote,
    firstText(ctx.slideObj, ["footnote", "notes", "source"], ["caption", "footer", "text"], ""),
    {
      fontFace: ctx.styles.font("body").family,
      fontSize: asNum(ctx.tokens.sizes?.caption, 11),
      color: ctx.styles.color("muted", "6B7280"),
      valign: "mid",
    },
    "caption"
  );
}

async function renderA20BeforeAfter(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A20_before_after");
  if (!layout) return renderGenericFallback(ctx);
  drawTextSlot(
    ctx,
    "headline",
    layout.headline,
    firstText(ctx.slideObj, ["headline", "title"], ["headline", "text"], ctx.slideObj?.headline || ""),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h2, 30),
      bold: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    },
    "headline"
  );
  drawTextSlot(
    ctx,
    "before_label",
    layout.before_label,
    firstText(ctx.slideObj, ["before_label", "before", "left_label"], ["text", "caption"], safeText(ctx.slideObj?.before_label || "Before")),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.caption, 14),
      bold: true,
      color: ctx.styles.color("muted", "6B7280"),
      valign: "mid",
    },
    "caption"
  );
  drawTextSlot(
    ctx,
    "after_label",
    layout.after_label,
    firstText(ctx.slideObj, ["after_label", "after", "right_label"], ["text", "caption"], safeText(ctx.slideObj?.after_label || "After")),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.caption, 14),
      bold: true,
      color: ctx.styles.color("muted", "6B7280"),
      valign: "mid",
      align: "left",
    },
    "caption"
  );
  addCard(ctx.slide, layout.before_panel, ctx.styles, {}, ctx, slotEl("before_panel", "card"));
  addCard(
    ctx.slide,
    layout.after_panel,
    ctx.styles,
    { fill: "annotation", stroke: "primary" },
    ctx,
    slotEl("after_panel", "card")
  );
  const beforeImage = firstImagePath(ctx.slideObj, ["before", "left"]);
  const afterImage = firstImagePath(ctx.slideObj, ["after", "right"]);
  const beforeText = panelContent(ctx.slideObj, "before", safeText(ctx.slideObj?.before || ""));
  const afterText = panelContent(ctx.slideObj, "after", safeText(ctx.slideObj?.after || ""));
  if (beforeImage && !beforeText) {
    await drawImageSlot(
      ctx,
      "before_visual",
      { x: layout.before_panel.x + 0.18, y: layout.before_panel.y + 0.18, w: layout.before_panel.w - 0.36, h: layout.before_panel.h - 0.36 },
      beforeImage,
      "surface"
    );
  } else {
    drawTextSlot(
      ctx,
      "before_panel_text",
      { x: layout.before_panel.x + 0.22, y: layout.before_panel.y + 0.2, w: layout.before_panel.w - 0.44, h: layout.before_panel.h - 0.4 },
      beforeText,
      {
        fontFace: ctx.styles.font("body").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 13),
        color: ctx.styles.color("fg", "111827"),
        valign: "top",
      }
    );
  }
  if (afterImage && !afterText) {
    await drawImageSlot(
      ctx,
      "after_visual",
      { x: layout.after_panel.x + 0.18, y: layout.after_panel.y + 0.18, w: layout.after_panel.w - 0.36, h: layout.after_panel.h - 0.36 },
      afterImage,
      "surface"
    );
  } else {
    drawTextSlot(
      ctx,
      "after_panel_text",
      { x: layout.after_panel.x + 0.22, y: layout.after_panel.y + 0.2, w: layout.after_panel.w - 0.44, h: layout.after_panel.h - 0.4 },
      afterText,
      {
        fontFace: ctx.styles.font("body").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 13),
        color: ctx.styles.color("fg", "111827"),
        valign: "top",
      }
    );
  }
  addConnector(
    ctx.slide,
    {
      x: layout.arrow_icon.x,
      y: layout.arrow_icon.y + layout.arrow_icon.h / 2,
      w: layout.arrow_icon.w,
      h: 0,
      line: {
        color: ctx.styles.color("primary", "2563EB"),
        width: 2,
        endArrowType: "triangle",
      },
    },
    ctx.styles,
    ctx,
    slotEl("before_after_arrow", "connector")
  );
  drawFooterIfAny(ctx, layout.footer);
}

async function renderA21CaseStudy(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A21_case_study");
  if (!layout) return renderGenericFallback(ctx);
  drawTextSlot(
    ctx,
    "headline",
    layout.headline,
    firstText(ctx.slideObj, ["headline", "title"], ["headline", "text"], ctx.slideObj?.headline || ""),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h2, 30),
      bold: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    },
    "headline"
  );
  const fallbackTitles = ["Challenge", "Solution", "Results"];
  const cards = safeItemsArrayByKeys(ctx.slideObj, ["cards", "case_study", "items"], []);
  const cardSlots = Array.isArray(layout.cards) ? layout.cards : [];
  for (let i = 0; i < cardSlots.length; i++) {
    const slot = cardSlots[i];
    const item = cards[i] || {};
    addCard(ctx.slide, slot.box, ctx.styles, {}, ctx, slotEl(`case_study_card_${i + 1}`, "card"));
    drawTextSlot(
      ctx,
      `case_study_title_${i + 1}`,
      slot.title,
      itemText(item, ["title", "label", "name", "text"], fallbackTitles[i] || `Card ${i + 1}`),
      {
        fontFace: ctx.styles.font("headline").family,
        fontSize: asNum(ctx.tokens.sizes?.body, 20),
        bold: true,
        color: ctx.styles.color("fg", "111827"),
        valign: "mid",
      }
    );
    drawTextSlot(
      ctx,
      `case_study_body_${i + 1}`,
      slot.body,
      itemText(item, ["body", "description", "detail", "content"], ""),
      {
        fontFace: ctx.styles.font("body").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 13),
        color: ctx.styles.color("fg", "111827"),
        valign: "top",
      }
    );
  }
  drawFooterIfAny(ctx, layout.footer);
}

async function renderA22Quote(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A22_quote");
  if (!layout) return renderGenericFallback(ctx);
  const quote = firstText(
    ctx.slideObj,
    ["quote", "headline", "title"],
    ["quote", "headline", "text"],
    safeText(ctx.slideObj?.headline || "")
  );
  const quoteLead = "\u201C";
  drawTextSlot(
    ctx,
    "quote_mark",
    {
      x: layout.quote.x + 0.1,
      y: layout.quote.y - 0.15,
      w: 0.7,
      h: 0.9,
    },
    quoteLead,
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: 72,
      color: ctx.styles.color("primary", "2563EB"),
      bold: true,
      valign: "mid",
      align: "left",
    },
    "quote"
  );
  addShape(
    ctx.slide,
    ShapeType.roundRect,
    {
      x: layout.quote.x + 0.55,
      y: layout.quote.y + 0.08,
      w: 0.045,
      h: Math.max(0.3, layout.quote.h - 0.16),
      rectRadius: 0.01,
      fill: { color: ctx.styles.color("primary_light", "93C5FD") },
      line: { color: ctx.styles.color("primary_light", "93C5FD"), width: 0 },
    },
    ctx,
    slotEl("quote_rule", "shape")
  );
  drawTextSlot(
    ctx,
    "quote_text",
    {
      x: layout.quote.x + 0.7,
      y: layout.quote.y,
      w: layout.quote.w - 0.75,
      h: layout.quote.h,
    },
    quote,
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h2, 30),
      bold: false,
      italic: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    },
    "quote"
  );
  drawTextSlot(
    ctx,
    "quote_attribution",
    layout.attribution,
    firstText(
      ctx.slideObj,
      ["attribution", "author", "source", "caption", "footer"],
      ["caption", "text", "footer"],
      safeText(ctx.slideObj?.attribution || "")
    ),
    {
      fontFace: ctx.styles.font("body").family,
      fontSize: asNum(ctx.tokens.sizes?.caption, 14),
      color: ctx.styles.color("muted", "6B7280"),
      align: "right",
      valign: "mid",
      italic: true,
    },
    "caption"
  );
  drawFooterIfAny(ctx, layout.footer);
}

async function renderA23TeamProfiles(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A23_team_profiles");
  if (!layout) return renderGenericFallback(ctx);
  drawTextSlot(
    ctx,
    "headline",
    layout.headline,
    firstText(ctx.slideObj, ["headline", "title"], ["headline", "text"], ctx.slideObj?.headline || ""),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h2, 30),
      bold: true,
      color: ctx.styles.color("fg", "111827"),
      valign: "mid",
    },
    "headline"
  );
  const people = safeItemsArrayByKeys(
    ctx.slideObj,
    ["people", "team", "members", "profiles", "items"],
    listElements(ctx.slideObj, (el) => typeValue(el) === "person")
  );
  const slots = Array.isArray(layout.people) ? layout.people : [];
  for (let i = 0; i < slots.length; i++) {
    const slot = slots[i];
    const person = people[i] || {};
    const photoSrc =
      itemImagePath(person) ||
      firstImagePath(ctx.slideObj, [`person_${i + 1}`, `team_${i + 1}`, `member_${i + 1}`]);
    addCard(ctx.slide, slot.card, ctx.styles, {}, ctx, slotEl(`team_card_${i + 1}`, "card"));
    if (photoSrc) {
      await addImage(
        ctx.slide,
        Object.assign({ path: photoSrc }, bboxToPptx(slot.photo)),
        ctx.styles,
        ctx,
        slotEl(`team_photo_${i + 1}`, "image")
      );
    } else {
      addShape(
        ctx.slide,
        ShapeType.ellipse,
        {
          ...bboxToPptx(slot.photo),
          fill: { color: ctx.styles.color("surface", "F3F4F6") },
          line: { color: ctx.styles.color("border", "D1D5DB"), width: 1 },
        },
        ctx,
        slotEl(`team_photo_placeholder_${i + 1}`, "shape")
      );
    }
    drawTextSlot(
      ctx,
      `team_name_${i + 1}`,
      slot.name,
      itemText(person, ["name", "title", "label", "text"], `Team member ${i + 1}`),
      {
        fontFace: ctx.styles.font("headline").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 14),
        bold: true,
        color: ctx.styles.color("fg", "111827"),
        valign: "mid",
      }
    );
    drawTextSlot(
      ctx,
      `team_role_${i + 1}`,
      slot.role,
      itemText(person, ["role", "position", "subtitle", "caption"], ""),
      {
        fontFace: ctx.styles.font("body").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 12),
        color: ctx.styles.color("muted", "6B7280"),
        valign: "mid",
      },
      "caption"
    );
    drawTextSlot(
      ctx,
      `team_bio_${i + 1}`,
      slot.bio,
      itemText(person, ["bio", "description", "body", "content"], ""),
      {
        fontFace: ctx.styles.font("body").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 11),
        color: ctx.styles.color("fg", "111827"),
        valign: "top",
      }
    );
  }
  drawFooterIfAny(ctx, layout.footer);
}

async function renderA24QaClosing(ctx) {
  const { layout } = getArchetypeLayout(ctx, "A24_qa_closing");
  if (!layout) return renderGenericFallback(ctx);
  drawTextSlot(
    ctx,
    "qa_title",
    layout.title,
    firstText(
      ctx.slideObj,
      ["title", "headline", "question", "qa"],
      ["headline", "text"],
      safeText(ctx.slideObj?.headline || "Questions?")
    ),
    {
      fontFace: ctx.styles.font("headline").family,
      fontSize: asNum(ctx.tokens.sizes?.h1, 40),
      bold: true,
      color: "FFFFFF",
      align: "center",
      valign: "mid",
    },
    "headline"
  );
  drawTextSlot(
    ctx,
    "qa_contact",
    layout.contact,
    firstText(
      ctx.slideObj,
      ["contact", "subtitle", "meta", "footer"],
      ["text", "caption", "footer"],
      safeText(ctx.slideObj?.contact || "")
    ),
    {
      fontFace: ctx.styles.font("body").family,
      fontSize: asNum(ctx.tokens.sizes?.body, 20),
      color: "E5E7EB",
      align: "center",
      valign: "mid",
    }
  );
  const footer = firstText(ctx.slideObj, ["footer", "caption", "meta"], ["footer", "caption", "text"], "");
  if (footer && layout.footer) {
    drawTextSlot(
      ctx,
      "footer",
      layout.footer,
      footer,
      {
        fontFace: ctx.styles.font("body").family,
        fontSize: asNum(ctx.tokens.sizes?.caption, 13),
        color: "D1D5DB",
        valign: "mid",
        align: "center",
      },
      "footer"
    );
  }
}

async function renderArchetypePlaceholder(ctx, key) {
  ctx.variant = selectVariant(ctx.slideObj?.archetype, ctx.slideObj, GEOMETRY);
  ctx.archetypeKey = key;
  await renderGenericFallback(ctx);
}

const archetypeHandlers = createArchetypeHandlers({
  renderA1Cover,
  renderA2SectionDivider,
  renderA3Agenda,
  renderA4AssertionHeroVisual,
  renderA5Split5050,
  renderA6Split3070,
  renderA7BigNumberCallout,
  renderA8IconGrid,
  renderA9CardGrid,
  renderA10Comparison,
  renderA11QuadrantMatrix,
  renderA12TimelineHorizontal,
  renderA13TimelineVertical,
  renderA14ProcessFlow,
  renderA15CycleLoop,
  renderA16ArchitectureDiagram,
  renderA17ChartFirstInsight,
  renderA18AnnotatedChart,
  renderA19TableLight,
  renderA20BeforeAfter,
  renderA21CaseStudy,
  renderA22Quote,
  renderA23TeamProfiles,
  renderA24QaClosing,
});

function slideArchetypeKey(archetype) {
  const m = String(archetype || "").match(/^A(\d{1,2})/i);
  if (!m) return "";
  return `A${parseInt(m[1], 10)}`;
}

function transitionSpecToXml(spec) {
  const effect = String(spec?.effect || "fade").toLowerCase();
  const speed = spec?.speed || "med";
  const attrs = `spd="${speed}" advClick="1"`;
  if (effect === "cut" || effect === "none") return `<p:transition ${attrs}/>`;
  if (effect === "push") {
    const dir = spec?.dir || "r";
    return `<p:transition ${attrs}><p:push dir="${dir}"/></p:transition>`;
  }
  if (effect === "wipe") {
    const dir = spec?.dir || "r";
    return `<p:transition ${attrs}><p:wipe dir="${dir}"/></p:transition>`;
  }
  return `<p:transition ${attrs}><p:fade/></p:transition>`;
}

function normalizeTransition(input) {
  if (!input) return null;
  if (typeof input === "string") return { effect: input };
  if (isObject(input)) {
    return {
      effect: input.effect || input.type || input.slide || "fade",
      dir: input.dir || input.direction,
      speed: input.speed,
      duration_ms: input.duration_ms,
    };
  }
  return null;
}

async function injectTransitions(outPath, slides, defaultTransition) {
  if (!AdmZip) {
    console.warn("[warn] adm-zip is not available; skipping transition injection.");
    return false;
  }
  const effectiveDefault = defaultTransition || { effect: "fade", speed: "med" };
  const perSlide = (slides || []).map((s) => normalizeTransition(s?.transition || s?.transitions));

  const zip = new AdmZip(outPath);
  for (let i = 0; i < (slides || []).length; i++) {
    const entryName = `ppt/slides/slide${i + 1}.xml`;
    const entry = zip.getEntry(entryName);
    if (!entry) continue;
    const spec = perSlide[i] || effectiveDefault;

    let xml = entry.getData().toString("utf8");
    const transitionXml = transitionSpecToXml(spec);
    if (xml.includes("<p:transition")) {
      xml = xml.replace(/<p:transition[\s\S]*?<\/p:transition>/, transitionXml);
      xml = xml.replace(/<p:transition[^>]*\/>/, transitionXml);
    } else if (xml.includes("</p:sld>")) {
      xml = xml.replace("</p:sld>", `${transitionXml}</p:sld>`);
    } else if (xml.includes("</p:cSld>")) {
      xml = xml.replace("</p:cSld>", `</p:cSld>${transitionXml}`);
    }
    zip.updateFile(entryName, Buffer.from(xml, "utf8"));
  }
  zip.writeZip(outPath);
  return true;
}

function buildRenderRuntime(deck) {
  const themeBundle = resolveThemesAndPalettes(deck?.theme || {});
  const tokens = buildTokens(deck, themeBundle);
  const styles = new StyleResolver(tokens, themeBundle.theme);
  return {
    themeBundle,
    tokens,
    styles,
    deckWidth: asNum(deck?.width, 13.333),
    deckHeight: asNum(deck?.height, 7.5),
    deckNotesDefault: deck?.speakerNotesDefaults ?? deck?.speaker_notes_defaults ?? deck?.notes,
  };
}

function createSlideContext(slide, slideObj, idx, runtime, tempArtifacts) {
  const sid = slideObj?.id || `S${String(idx + 1).padStart(2, "0")}`;
  return {
    slide,
    slideObj,
    styles: runtime.styles,
    tokens: runtime.tokens,
    deckWidth: runtime.deckWidth,
    deckHeight: runtime.deckHeight,
    tempArtifacts,
    index: idx,
    namer: createObjectNamer(sid),
  };
}

async function renderSlide(pptx, slideObj, idx, runtime, tempArtifacts) {
  const masterName = resolveMasterName(slideObj?.archetype);
  const slide = pptx.addSlide({ masterName });
  const ctx = createSlideContext(slide, slideObj, idx, runtime, tempArtifacts);

  const key = slideArchetypeKey(slideObj?.archetype);
  const handler = archetypeHandlers[key];
  if (handler) await handler(ctx);
  else await renderGenericFallback(ctx);

  const notes = normalizeNotes(slideObj?.speakerNotes ?? slideObj?.speaker_notes ?? slideObj?.notes ?? runtime.deckNotesDefault);
  if (notes.trim()) {
    slide.addNotes(notes);
  }
}

async function renderSlides(pptx, slides, runtime, tempArtifacts) {
  for (let i = 0; i < slides.length; i++) {
    await renderSlide(pptx, slides[i], i, runtime, tempArtifacts);
  }
}

async function renderDeck(ir, outPath) {
  if (!ir || !ir.deck) throw new Error("IR must include top-level deck");

  const runtime = buildRenderRuntime(ir.deck);
  const pptx = new pptxgen();
  pptx.defineLayout({ name: "WIDE", width: runtime.deckWidth, height: runtime.deckHeight });
  pptx.layout = "WIDE";
  pptx.author = "pptx-master-renderer";
  pptx.subject = "Slide Deck IR Render";

  pptx.theme = {
    headFontFace: runtime.styles.font("headline").family,
    bodyFontFace: runtime.styles.font("body").family,
    lang: "en-US",
  };
  defineMasters(pptx, runtime.styles);

  const tempArtifacts = [];
  const slides = Array.isArray(ir.deck.slides) ? ir.deck.slides : [];
  await renderSlides(pptx, slides, runtime, tempArtifacts);

  let tempOutPath = "";
  let effectiveTempPath = "";
  try {
    tempOutPath = path.join(
      path.dirname(outPath),
      `.${path.basename(outPath, path.extname(outPath))}.tmp-${Date.now()}-${Math.random().toString(36).slice(2)}.pptx`
    );
    await pptx.writeFile({ fileName: tempOutPath });
    effectiveTempPath = fs.existsSync(tempOutPath)
      ? tempOutPath
      : (fs.existsSync(`${tempOutPath}.pptx`) ? `${tempOutPath}.pptx` : tempOutPath);
    const defaultTransition = normalizeTransition(
      ir.deck?.transition ||
        ir.deck?.transitions ||
        runtime.themeBundle.theme?.motion?.transitions?.slide
    ) || { effect: "fade", speed: "med" };
    await injectTransitions(effectiveTempPath, slides, defaultTransition);
    fs.renameSync(effectiveTempPath, outPath);
  } finally {
    if (effectiveTempPath && fs.existsSync(effectiveTempPath)) {
      fs.unlinkSync(effectiveTempPath);
    }
    if (tempOutPath && fs.existsSync(tempOutPath)) {
      fs.unlinkSync(tempOutPath);
    }
    for (const artifactPath of tempArtifacts) {
      if (artifactPath && fs.existsSync(artifactPath)) {
        fs.unlinkSync(artifactPath);
      }
    }
  }
}

async function main() {
  const inPath = process.argv[2];
  const outPath = process.argv[3];
  if (!inPath || !outPath) {
    console.error("Usage: node scripts/render_pptx.js <ir.json> <output.pptx>");
    process.exit(2);
  }
  const ir = readJson(inPath);
  await renderDeck(ir, outPath);
  console.log(`Wrote: ${outPath}`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
