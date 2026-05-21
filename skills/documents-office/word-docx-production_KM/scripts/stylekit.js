'use strict';

/**
 * stylekit.js
 *
 * Gap 1 fix: translate the human-readable JSON style specs (pt / inches / multiples)
 * into executable docx-js styles (half-points / twips / 240ths).
 *
 * The goal is that an agent never does unit conversions by hand.
 */

const fs = require("fs");
const path = require("path");

function assertNumber(name, value) {
  if (typeof value !== "number" || Number.isNaN(value) || !Number.isFinite(value)) {
    throw new Error(`${name} must be a finite number. Got: ${JSON.stringify(value)}`);
  }
}

function ptToHalfPoints(pt) {
  assertNumber("pt", pt);
  // docx expects font sizes in half-points
  return Math.round(pt * 2);
}

function ptToTwips(pt) {
  assertNumber("pt", pt);
  // 1 pt = 20 twips
  return Math.round(pt * 20);
}

function inToTwips(inches) {
  assertNumber("inches", inches);
  // 1 in = 1440 twips
  return Math.round(inches * 1440);
}

function multipleTo240(multiple) {
  assertNumber("line_spacing_multiple", multiple);
  // Word line spacing "auto" uses 240ths of a line.
  return Math.round(multiple * 240);
}

function stripHash(hex) {
  if (typeof hex !== "string") return hex;
  const h = hex.trim();
  if (!h) return h;
  return h.startsWith("#") ? h.slice(1) : h;
}

function normalizeHexColor(hex) {
  const h = stripHash(hex);
  if (typeof h !== "string") return undefined;
  const up = h.trim().toUpperCase();
  if (/^[0-9A-F]{6}$/.test(up)) return up;
  return undefined;
}

function humanizeStyleName(styleId) {
  if (typeof styleId !== "string" || !styleId) return styleId;

  // Split acronym boundaries: "UILabel" -> "UI Label"
  let s = styleId.replace(/([A-Z])([A-Z][a-z])/g, "$1 $2");

  // Split lower->upper and lower->digit: "BodyCompact" -> "Body Compact", "Heading1" -> "Heading 1"
  s = s.replace(/([a-z])([A-Z0-9])/g, "$1 $2");

  // Improve common tokens
  s = s.replace(/\bUI\b/g, "UI");

  return s.trim();
}

function loadJson(filePath) {
  const raw = fs.readFileSync(filePath, "utf8");
  try {
    return JSON.parse(raw);
  } catch (e) {
    throw new Error(`Failed to parse JSON at ${filePath}: ${e.message}`);
  }
}

function resolveBundledSpecPath(nameOrAlias) {
  const aliases = {
    academic: "academic_manuscript_generic",
    business: "business_report_modern",
    technical: "technical_report_engineering",
  };
  const resolvedName = aliases[nameOrAlias] || nameOrAlias;
  return path.resolve(__dirname, "..", "assets", "style-specs", `${resolvedName}.json`);
}

function loadBundledStyleSpec(nameOrAlias) {
  const p = resolveBundledSpecPath(nameOrAlias);
  if (!fs.existsSync(p)) {
    throw new Error(
      `Unknown style spec "${nameOrAlias}". Expected a bundled spec at: ${p}`
    );
  }
  return loadJson(p);
}

function resolveColor(spec, colorRefOrHex) {
  if (!colorRefOrHex) return undefined;

  // Named colors reference spec.colors
  if (typeof colorRefOrHex === "string" && spec.colors && spec.colors[colorRefOrHex]) {
    colorRefOrHex = spec.colors[colorRefOrHex];
  }

  // A literal "#RRGGBB" or "RRGGBB"
  const hex = normalizeHexColor(colorRefOrHex);
  if (hex) return hex;

  return undefined;
}

function chooseFontFamily(fontRecord) {
  if (!fontRecord || typeof fontRecord !== "object") return undefined;
  const family = fontRecord.family;
  const fallbacks = Array.isArray(fontRecord.fallback) ? fontRecord.fallback : [];
  if (typeof family !== "string" || !family.trim()) return undefined;

  // The sandbox often lacks Aptos/Aptos Display; prefer declared fallbacks if present.
  if (/^Aptos(\s+Display)?$/i.test(family.trim()) && fallbacks.length > 0) {
    return fallbacks[0];
  }
  return family.trim();
}

function resolveFontFamily(spec, familyRef) {
  // familyRef can be:
  // - undefined (use body)
  // - "heading" / "body" / "mono" (lookup spec.fonts)
  // - literal font family ("Times New Roman")
  if (!spec.fonts || typeof spec.fonts !== "object") {
    return typeof familyRef === "string" ? familyRef : undefined;
  }

  const bodyFont = chooseFontFamily(spec.fonts.body) || "Calibri";

  if (!familyRef) return bodyFont;

  if (typeof familyRef === "string" && spec.fonts[familyRef]) {
    return chooseFontFamily(spec.fonts[familyRef]) || bodyFont;
  }

  if (typeof familyRef === "string") return familyRef;

  return bodyFont;
}

function resolveFontSizePt(spec, sizePt) {
  if (typeof sizePt === "number") return sizePt;
  // Fall back to body size when omitted.
  const body = spec.fonts && spec.fonts.body;
  if (body && typeof body.size_pt === "number") return body.size_pt;
  return 11;
}

function shadingFill(spec, fillRefOrHex) {
  const hex = resolveColor(spec, fillRefOrHex) || normalizeHexColor(fillRefOrHex);
  return hex || normalizeHexColor("F2F2F2") || "F2F2F2";
}

function buildRunPropsFromFontSpec(spec, fontSpec = {}, { allowMissingSize = false } = {}) {
  const run = {};

  // Font family
  const familyRef = fontSpec.family;
  const fontFamily = resolveFontFamily(spec, familyRef);
  if (fontFamily) run.font = fontFamily;

  // Font size
  const sizePt = resolveFontSizePt(spec, fontSpec.size_pt);
  if (!allowMissingSize || typeof fontSpec.size_pt === "number") {
    run.size = ptToHalfPoints(sizePt);
  }

  // Weight / style
  if (fontSpec.bold === true) run.bold = true;
  if (fontSpec.italic === true) run.italics = true;

  return run;
}

function buildIndent(spec, styleDef = {}) {
  const indent = {};

  const leftIn = styleDef.left_indent_in;
  const rightIn = styleDef.right_indent_in;
  const firstLineIn = styleDef.first_line_indent_in;
  const hangingIn = styleDef.hanging_indent_in;

  if (typeof leftIn === "number") indent.left = inToTwips(leftIn);
  if (typeof rightIn === "number") indent.right = inToTwips(rightIn);
  if (typeof firstLineIn === "number") indent.firstLine = inToTwips(firstLineIn);

  if (typeof hangingIn === "number") {
    const hangingTwips = inToTwips(hangingIn);
    // Word usually expects left indent too for a hanging indent to behave as expected.
    if (indent.left === undefined) indent.left = hangingTwips;
    indent.hanging = hangingTwips;
  }

  return Object.keys(indent).length ? indent : undefined;
}

function buildSpacing(spec, styleDef = {}) {
  const spacing = {};

  if (typeof styleDef.space_before_pt === "number") spacing.before = ptToTwips(styleDef.space_before_pt);
  if (typeof styleDef.space_after_pt === "number") spacing.after = ptToTwips(styleDef.space_after_pt);

  if (typeof styleDef.line_spacing_multiple === "number") {
    const docx = require("docx");
    spacing.line = multipleTo240(styleDef.line_spacing_multiple);
    spacing.lineRule = docx.LineRuleType.AUTO;
  }

  return Object.keys(spacing).length ? spacing : undefined;
}

function resolveAlignment(alignment) {
  if (!alignment) return undefined;
  const docx = require("docx");
  const a = String(alignment).toLowerCase().trim();
  if (a === "left") return docx.AlignmentType.LEFT;
  if (a === "center") return docx.AlignmentType.CENTER;
  if (a === "right") return docx.AlignmentType.RIGHT;
  if (a === "justify") return docx.AlignmentType.JUSTIFIED;
  return undefined;
}

function buildParagraphStyleOptions(spec, styleId, styleDef = {}) {
  const paragraph = {};

  const alignment = resolveAlignment(styleDef.alignment);
  if (alignment) paragraph.alignment = alignment;

  const spacing = buildSpacing(spec, styleDef);
  if (spacing) paragraph.spacing = spacing;

  const indent = buildIndent(spec, styleDef);
  if (indent) paragraph.indent = indent;

  if (styleDef.keep_with_next === true) paragraph.keepNext = true;
  if (styleDef.keep_together === true) paragraph.keepLines = true;

  if (typeof styleDef.outline_level === "number") {
    // style spec uses 1-based levels; docx uses 0-based outlineLevel.
    paragraph.outlineLevel = Math.max(0, Math.round(styleDef.outline_level) - 1);
  }

  // Paragraph shading (e.g., CodeBlock background)
  if (styleDef.shading) {
    const docx = require("docx");
    paragraph.shading = {
      type: docx.ShadingType.CLEAR,
      color: "auto",
      fill: shadingFill(spec, styleDef.shading),
    };
  }

  return paragraph;
}

function buildParagraphRunOptions(spec, styleDef = {}) {
  const run = buildRunPropsFromFontSpec(spec, styleDef.font || {}, { allowMissingSize: false });

  const color = resolveColor(spec, styleDef.color);
  if (color) run.color = color;

  return run;
}

function buildCharacterRunOptions(spec, styleDef = {}) {
  const run = buildRunPropsFromFontSpec(spec, styleDef.font || {}, { allowMissingSize: true });

  // simple toggles
  if (styleDef.bold === true) run.bold = true;
  if (styleDef.italic === true) run.italics = true;

  if (styleDef.shading) {
    const docx = require("docx");
    run.shading = {
      type: docx.ShadingType.CLEAR,
      color: "auto",
      fill: shadingFill(spec, styleDef.shading),
    };
  }

  const color = resolveColor(spec, styleDef.color);
  if (color) run.color = color;

  return run;
}

function buildDocxStyles(spec) {
  if (!spec || typeof spec !== "object") throw new Error("Style spec must be an object.");
  if (!spec.paragraphStyles || typeof spec.paragraphStyles !== "object") {
    throw new Error('Style spec must include "paragraphStyles".');
  }

  const paragraphStyles = [];
  for (const [styleId, styleDef] of Object.entries(spec.paragraphStyles)) {
    const style = {
      id: styleId,
      name: humanizeStyleName(styleId),
      ...("based_on" in styleDef ? { basedOn: styleDef.based_on } : {}),
      ...("next" in styleDef ? { next: styleDef.next } : {}),
      quickFormat: true,
      run: buildParagraphRunOptions(spec, styleDef),
      paragraph: buildParagraphStyleOptions(spec, styleId, styleDef),
    };
    paragraphStyles.push(style);
  }

  const characterStyles = [];
  if (spec.characterStyles && typeof spec.characterStyles === "object") {
    for (const [styleId, styleDef] of Object.entries(spec.characterStyles)) {
      const style = {
        id: styleId,
        name: humanizeStyleName(styleId),
        quickFormat: true,
        run: buildCharacterRunOptions(spec, styleDef),
      };
      characterStyles.push(style);
    }
  }

  const defaultBodyFamily = resolveFontFamily(spec, "body");
  const defaultBodySizePt = resolveFontSizePt(spec, spec.fonts?.body?.size_pt);
  const defaultBodyColor = resolveColor(spec, "mutedText") || resolveColor(spec, "accent") || "000000";

  return {
    default: {
      document: {
        run: {
          font: defaultBodyFamily,
          size: ptToHalfPoints(defaultBodySizePt),
          color: defaultBodyColor,
        },
      },
    },
    paragraphStyles,
    characterStyles,
  };
}

function pageSizeTwips(pageSizeName) {
  const name = String(pageSizeName || "").toLowerCase().trim();
  // Extend as needed; Letter is the default in this skill.
  if (name === "a4") {
    // A4 = 210mm x 297mm => 8.2677 x 11.6929 in
    return { width: inToTwips(8.2677), height: inToTwips(11.6929) };
  }
  // Letter = 8.5 x 11 in
  return { width: inToTwips(8.5), height: inToTwips(11) };
}

function buildSectionProperties(spec, { includeHeaderFooterMargins = true } = {}) {
  if (!spec.page || typeof spec.page !== "object") throw new Error('Style spec must include "page".');
  const margins = spec.page.margins_in || {};
  const sizeName = spec.page.size || "Letter";

  const sizeTwips = pageSizeTwips(sizeName);

  const margin = {
    top: inToTwips(margins.top ?? 1.0),
    right: inToTwips(margins.right ?? 1.0),
    bottom: inToTwips(margins.bottom ?? 1.0),
    left: inToTwips(margins.left ?? 1.0),
  };

  if (includeHeaderFooterMargins) {
    // Word defaults are 0.5in for header/footer distance; keep it predictable.
    margin.header = inToTwips(0.5);
    margin.footer = inToTwips(0.5);
  }

  return {
    page: {
      size: sizeTwips,
      margin,
    },
  };
}

/**
 * Build a docx-js Document options object:
 *   { styles, sections: [{ properties, children }] }
 */
function createDocxOptions(specOrName, { children = [], sectionPropertiesOverride } = {}) {
  const spec = typeof specOrName === "string" ? loadBundledStyleSpec(specOrName) : specOrName;
  const styles = buildDocxStyles(spec);
  const properties = sectionPropertiesOverride || buildSectionProperties(spec);
  return {
    styles,
    sections: [{ properties, children }],
  };
}

/**
 * Convenience Paragraph helper that auto-applies per-style flags that docx-js cannot encode in styles
 * (e.g., widowControl).
 */
function paragraph(specOrName, styleId, childrenOrText, extraOptions = {}) {
  const docx = require("docx");
  const spec = typeof specOrName === "string" ? loadBundledStyleSpec(specOrName) : specOrName;

  let children = [];
  if (typeof childrenOrText === "string") {
    children = [new docx.TextRun({ text: childrenOrText })];
  } else if (Array.isArray(childrenOrText)) {
    children = childrenOrText;
  } else if (childrenOrText) {
    // single run-like object
    children = [childrenOrText];
  }

  const styleDef = spec.paragraphStyles?.[styleId] || {};
  const widowControl = styleDef.widow_control === true ? true : undefined;

  return new docx.Paragraph({
    style: styleId,
    widowControl,
    children,
    ...extraOptions,
  });
}

module.exports = {
  // loading
  loadBundledStyleSpec,
  resolveBundledSpecPath,

  // conversion
  ptToHalfPoints,
  ptToTwips,
  inToTwips,
  multipleTo240,
  humanizeStyleName,
  resolveColor,
  resolveFontFamily,

  buildDocxStyles,
  buildSectionProperties,

  // high-level helpers
  createDocxOptions,
  paragraph,
};
