'use strict';

/**
 * tablekit.js
 *
 * Gap 2 fix: ready-to-use table builders with sane professional defaults.
 *
 * Word tables are easy to make ugly. This module bakes in:
 * - light horizontal rules (no vertical gridlines by default)
 * - header row shading + repeat-on-each-page headers
 * - numeric alignment
 * - consistent cell padding
 * - optional caption + notes blocks
 */

const docx = require("docx");
const stylekit = require("./stylekit");

// ---------------------------------
// Internal helpers
// ---------------------------------

function asArray(x) {
  if (x === undefined || x === null) return [];
  return Array.isArray(x) ? x : [x];
}

function isDocxInstance(obj, ctorName) {
  return obj && typeof obj === "object" && obj.constructor && obj.constructor.name === ctorName;
}

function coerceText(value) {
  if (value === null || value === undefined) return "";
  if (typeof value === "number") return Number.isFinite(value) ? String(value) : "";
  return String(value);
}

function twipsFromPaddingPt(paddingPt) {
  // Table margins use DXA (twips)
  if (!paddingPt || typeof paddingPt !== "object") return undefined;
  const out = {};
  if (typeof paddingPt.top === "number") out.top = stylekit.ptToTwips(paddingPt.top);
  if (typeof paddingPt.bottom === "number") out.bottom = stylekit.ptToTwips(paddingPt.bottom);
  if (typeof paddingPt.left === "number") out.left = stylekit.ptToTwips(paddingPt.left);
  if (typeof paddingPt.right === "number") out.right = stylekit.ptToTwips(paddingPt.right);
  if (!Object.keys(out).length) return undefined;
  return { marginUnitType: docx.WidthType.DXA, ...out };
}

function border(style, color, size) {
  return { style, color, size };
}

function buildBorderPreset(presetName, { lineColor = "C7C7C7", strongColor = "7F7F7F" } = {}) {
  const p = String(presetName || "").toLowerCase().trim();

  // OOXML border size is 1/8pt. size=4 => 0.5pt. size=2 => 0.25pt.
  const LIGHT = border(docx.BorderStyle.SINGLE, lineColor, 2);
  const HAIRLINE = border(docx.BorderStyle.SINGLE, lineColor, 1);
  const STRONG = border(docx.BorderStyle.SINGLE, strongColor, 4);
  const NONE = border(docx.BorderStyle.NONE, "auto", 0);

  if (p === "full_grid" || p === "grid") {
    return {
      tableBorders: {
        top: LIGHT,
        bottom: LIGHT,
        left: LIGHT,
        right: LIGHT,
        insideHorizontal: LIGHT,
        insideVertical: LIGHT,
      },
      headerCellBottomBorder: LIGHT,
      bodyCellTopBorder: undefined,
    };
  }

  if (p === "light_horizontal") {
    return {
      tableBorders: {
        top: NONE,
        bottom: STRONG,
        left: NONE,
        right: NONE,
        insideHorizontal: HAIRLINE,
        insideVertical: NONE,
      },
      headerCellBottomBorder: STRONG,
      bodyCellTopBorder: undefined,
    };
  }

  // Default: minimal horizontal rules (APA-ish)
  return {
    tableBorders: {
      top: STRONG,
      bottom: STRONG,
      left: NONE,
      right: NONE,
      insideHorizontal: HAIRLINE,
      insideVertical: NONE,
    },
    headerCellBottomBorder: STRONG,
    bodyCellTopBorder: undefined,
  };
}

function defaultTableStyleKey(spec) {
  const keys = spec.tableStyles && typeof spec.tableStyles === "object" ? Object.keys(spec.tableStyles) : [];
  return keys.length ? keys[0] : undefined;
}

function resolveTableStyle(spec, styleKey) {
  if (!spec.tableStyles || typeof spec.tableStyles !== "object") return undefined;
  const key = styleKey || defaultTableStyleKey(spec);
  if (!key) return undefined;
  return { key, def: spec.tableStyles[key] };
}

function makeCellParagraph(text, { styleId, run, alignment } = {}) {
  const runs = run ? [new docx.TextRun({ text, ...run })] : [new docx.TextRun({ text })];
  return new docx.Paragraph({
    style: styleId,
    alignment,
    children: runs,
  });
}

function coerceCellChildren(value, { paragraphStyleId, run, alignment } = {}) {
  // Valid TableCell children are Paragraph or Table.
  if (isDocxInstance(value, "Paragraph") || isDocxInstance(value, "Table")) return [value];

  // Allow arrays of Paragraph/Table, or arrays of plain values.
  if (Array.isArray(value)) {
    const out = [];
    for (const item of value) {
      if (isDocxInstance(item, "Paragraph") || isDocxInstance(item, "Table")) {
        out.push(item);
      } else {
        out.push(makeCellParagraph(coerceText(item), { styleId: paragraphStyleId, run, alignment }));
      }
    }
    return out.length ? out : [makeCellParagraph("", { styleId: paragraphStyleId, run, alignment })];
  }

  return [makeCellParagraph(coerceText(value), { styleId: paragraphStyleId, run, alignment })];
}

function inferNumericColumns(rows, columnCount) {
  // Heuristic: a column is numeric if >60% of non-empty cells parse as numbers.
  const counts = Array.from({ length: columnCount }, () => ({ numeric: 0, nonEmpty: 0 }));
  for (const row of rows) {
    for (let i = 0; i < columnCount; i++) {
      const v = row[i];
      if (v === null || v === undefined) continue;
      const s = String(v).trim();
      if (!s) continue;
      counts[i].nonEmpty += 1;
      // Remove common symbols for currency/percent.
      const cleaned = s.replace(/[%,$]/g, "").replace(/,/g, "");
      if (cleaned && !Number.isNaN(Number(cleaned))) counts[i].numeric += 1;
    }
  }
  return counts.map((c) => c.nonEmpty > 0 && c.numeric / c.nonEmpty >= 0.6);
}

// ---------------------------------
// Public API
// ---------------------------------

/**
 * Create a caption paragraph (TableCaption style by default).
 *
 * @param {object|string} specOrName - style spec object OR bundled name ('business'|'academic'|'technical')
 * @param {string} captionText - e.g. "Table 1. Baseline characteristics."
 * @param {object} opts
 */
function makeTableCaption(specOrName, captionText, opts = {}) {
  const spec = typeof specOrName === "string" ? stylekit.loadBundledStyleSpec(specOrName) : specOrName;
  const styleId = opts.styleId || (spec.paragraphStyles?.TableCaption ? "TableCaption" : "Body");
  return stylekit.paragraph(spec, styleId, captionText, { keepNext: true });
}

/**
 * Create a notes block beneath a table (small font, compact spacing).
 */
function makeTableNotes(specOrName, notes, opts = {}) {
  const spec = typeof specOrName === "string" ? stylekit.loadBundledStyleSpec(specOrName) : specOrName;
  const styleId =
    opts.styleId ||
    (spec.paragraphStyles?.BodyCompact ? "BodyCompact" : spec.paragraphStyles?.FigureCaption ? "FigureCaption" : "Body");

  return asArray(notes).map((n) => stylekit.paragraph(spec, styleId, String(n), { spacing: { before: 0, after: stylekit.ptToTwips(3) } }));
}

/**
 * Build a professional data table.
 *
 * @param {object|string} specOrName
 * @param {object} options
 * @returns {{ table: any, blocks: any[] }}
 */
function makeDataTable(specOrName, options) {
  const spec = typeof specOrName === "string" ? stylekit.loadBundledStyleSpec(specOrName) : specOrName;

  const {
    caption,
    notes,
    styleKey,
    headers,
    rows,
    columnTypes,
    columnWidthsTwips,
    widthPct = 100,
    repeatHeader = true,
    cantSplitRows = true,
    bandedRows,
    alignment = docx.AlignmentType.CENTER,
  } = options || {};

  if (!Array.isArray(headers) || headers.length === 0) throw new Error("makeDataTable: headers[] is required.");
  if (!Array.isArray(rows)) throw new Error("makeDataTable: rows[] is required.");

  const tStyle = resolveTableStyle(spec, styleKey);
  const tDef = tStyle?.def || {};
  const baseFontSizePt = tDef.font?.size_pt ?? 10.5;
  const baseRun = {
    font: stylekit.resolveFontFamily(spec, tDef.font?.family || "body"),
    size: stylekit.ptToHalfPoints(baseFontSizePt),
    color: stylekit.resolveColor(spec, "mutedText") || "000000",
  };

  const cellMargins = twipsFromPaddingPt(tDef.cell_padding_pt) || twipsFromPaddingPt({ top: 5, bottom: 5, left: 6, right: 6 });

  const borderPresetName = tDef.borders || "minimal_horizontal";
  const borders = buildBorderPreset(borderPresetName);

  const headerFill = stylekit.resolveColor(spec, tDef.header_row?.shading) || stylekit.resolveColor(spec, spec.colors?.tableHeaderFill) || "EDEDED";
  const headerBold = tDef.header_row?.bold !== false;

  const doBanded = typeof bandedRows === "boolean" ? bandedRows : tDef.banded_rows === true || tDef.table_look?.bandedRows === true;
  const bandFill = stylekit.resolveColor(spec, spec.colors?.lightFill) || "F7F7F7";

  // Convert rows to array-of-arrays
  const normalizedRows = rows.map((r) => (Array.isArray(r) ? r : headers.map((h) => r[h])));
  const isNumeric = Array.isArray(columnTypes)
    ? columnTypes.map((t) => String(t).toLowerCase() === "number")
    : inferNumericColumns(normalizedRows, headers.length);

  const headerCells = headers.map((h) => {
    const p = makeCellParagraph(coerceText(h), {
      styleId: options.headerParagraphStyleId || (spec.paragraphStyles?.Body ? "Body" : undefined),
      run: { ...baseRun, bold: headerBold },
      alignment: docx.AlignmentType.LEFT,
    });

    return new docx.TableCell({
      shading: { type: docx.ShadingType.CLEAR, color: "auto", fill: headerFill },
      borders: {
        bottom: borders.headerCellBottomBorder,
      },
      children: [p],
      verticalAlign: docx.VerticalAlignTable.CENTER,
    });
  });

  const bodyRows = normalizedRows.map((row, rowIdx) => {
    const cells = row.map((v, colIdx) => {
      const align = isNumeric[colIdx] ? docx.AlignmentType.RIGHT : docx.AlignmentType.LEFT;
      const children = coerceCellChildren(v, {
        paragraphStyleId: options.bodyParagraphStyleId || (spec.paragraphStyles?.Body ? "Body" : undefined),
        run: baseRun,
        alignment: align,
      });

      const shading = doBanded && rowIdx % 2 === 1 ? { type: docx.ShadingType.CLEAR, color: "auto", fill: bandFill } : undefined;

      return new docx.TableCell({
        shading,
        children,
        verticalAlign: docx.VerticalAlignTable.CENTER,
      });
    });

    return new docx.TableRow({
      children: cells,
      cantSplit: cantSplitRows,
    });
  });

  const tableRows = [
    new docx.TableRow({
      children: headerCells,
      tableHeader: repeatHeader,
      cantSplit: true,
    }),
    ...bodyRows,
  ];

  const table = new docx.Table({
    rows: tableRows,
    width: { size: widthPct, type: docx.WidthType.PERCENTAGE },
    columnWidths: Array.isArray(columnWidthsTwips) && columnWidthsTwips.length === headers.length ? columnWidthsTwips : undefined,
    margins: cellMargins,
    borders: borders.tableBorders,
    alignment,
    layout: Array.isArray(columnWidthsTwips) ? docx.TableLayoutType.FIXED : docx.TableLayoutType.AUTOFIT,
  });

  const blocks = [];
  if (caption) blocks.push(makeTableCaption(spec, caption));
  blocks.push(table);
  if (notes) blocks.push(...makeTableNotes(spec, notes));

  return { table, blocks };
}

/**
 * Build a key-value table (2-column, no gridlines) – useful for cover pages or metadata blocks.
 *
 * @param {object|string} specOrName
 * @param {object} options
 * @returns {{ table: any, blocks: any[] }}
 */
function makeKeyValueTable(specOrName, options) {
  const spec = typeof specOrName === "string" ? stylekit.loadBundledStyleSpec(specOrName) : specOrName;
  const {
    caption,
    rows,
    keyWidthPct = 28,
    valueWidthPct = 72,
    styleId = spec.paragraphStyles?.BodyCompact ? "BodyCompact" : "Body",
    keyBold = true,
    cellPaddingPt = { top: 2, bottom: 2, left: 0, right: 0 },
  } = options || {};

  if (!Array.isArray(rows) || rows.length === 0) throw new Error("makeKeyValueTable: rows[] is required.");

  const cellMargins = twipsFromPaddingPt(cellPaddingPt) || undefined;

  const tableRows = rows.map(([k, v]) => {
    const keyP = makeCellParagraph(coerceText(k), {
      styleId,
      run: { bold: keyBold },
      alignment: docx.AlignmentType.LEFT,
    });

    const valChildren = coerceCellChildren(v, {
      paragraphStyleId: styleId,
      run: {},
      alignment: docx.AlignmentType.LEFT,
    });

    return new docx.TableRow({
      children: [
        new docx.TableCell({
          width: { size: keyWidthPct, type: docx.WidthType.PERCENTAGE },
          margins: cellMargins,
          children: [keyP],
        }),
        new docx.TableCell({
          width: { size: valueWidthPct, type: docx.WidthType.PERCENTAGE },
          margins: cellMargins,
          children: valChildren,
        }),
      ],
      cantSplit: true,
    });
  });

  const table = new docx.Table({
    rows: tableRows,
    width: { size: 100, type: docx.WidthType.PERCENTAGE },
    borders: {
      top: { style: docx.BorderStyle.NONE, size: 0, color: "auto" },
      bottom: { style: docx.BorderStyle.NONE, size: 0, color: "auto" },
      left: { style: docx.BorderStyle.NONE, size: 0, color: "auto" },
      right: { style: docx.BorderStyle.NONE, size: 0, color: "auto" },
      insideHorizontal: { style: docx.BorderStyle.NONE, size: 0, color: "auto" },
      insideVertical: { style: docx.BorderStyle.NONE, size: 0, color: "auto" },
    },
    layout: docx.TableLayoutType.FIXED,
  });

  const blocks = [];
  if (caption) blocks.push(makeTableCaption(spec, caption));
  blocks.push(table);
  return { table, blocks };
}

module.exports = {
  makeTableCaption,
  makeTableNotes,
  makeDataTable,
  makeKeyValueTable,
};
