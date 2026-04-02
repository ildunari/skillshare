'use strict';

/**
 * coverkit.js
 *
 * Gap 3 fix: cover/title page system using only constructs that survive
 * Word round-trips (no floating textboxes).
 *
 * Implementation strategy:
 * - Use a 2-row, 1-column table that fills the page content area.
 * - Row 1: Title block (vertically centered).
 * - Row 2: Metadata block (bottom-aligned).
 *
 * This avoids brittle "spacing hacks" and plays nicely with PDF rendering.
 */

const docx = require("docx");
const stylekit = require("./stylekit");
const tablekit = require("./tablekit");

// -------------------------------
// Header / footer helpers
// -------------------------------

function headerFooterContent(v) {
  if (!v) return null;
  if (typeof v === "string") return v;
  if (typeof v === "object" && typeof v.content === "string") return v.content;
  return String(v);
}

function textWithPageFields(template) {
  const tokens = String(template || "")
    .split(/(\{PAGE\}|\{NUMPAGES\}|\{TOTAL_PAGES\})/g)
    .filter(Boolean);

  const children = [];
  for (const t of tokens) {
    if (t === "{PAGE}") children.push(docx.PageNumber.CURRENT);
    else if (t === "{NUMPAGES}" || t === "{TOTAL_PAGES}") children.push(docx.PageNumber.TOTAL_PAGES);
    else children.push(t);
  }
  return children;
}

function buildHeader(spec) {
  const h = spec.headersFooters?.running_header;
  if (!h) return new docx.Header({ children: [] });

  return new docx.Header({
    children: [
      new docx.Paragraph({
        style: spec.paragraphStyles?.Header ? "Header" : undefined,
        alignment: docx.AlignmentType.RIGHT,
        children: [new docx.TextRun({ children: textWithPageFields(h) })],
      }),
    ],
  });
}

function buildFooter(spec) {
  const f = spec.headersFooters?.footer;
  // Default: centered page number
  if (!f) {
    return new docx.Footer({
      children: [
        new docx.Paragraph({
          alignment: docx.AlignmentType.CENTER,
          children: [new docx.TextRun({ children: [docx.PageNumber.CURRENT] })],
        }),
      ],
    });
  }

  return new docx.Footer({
    children: [
      new docx.Paragraph({
        alignment: docx.AlignmentType.CENTER,
        children: [new docx.TextRun({ children: textWithPageFields(f) })],
      }),
    ],
  });
}

// -------------------------------
// Cover layout
// -------------------------------

function computeContentHeightTwips(sectionProps) {
  const pageH = sectionProps?.page?.size?.height;
  const margin = sectionProps?.page?.margin || {};
  const top = margin.top || 0;
  const bottom = margin.bottom || 0;
  if (typeof pageH !== "number") return 12000;
  return Math.max(1, pageH - top - bottom);
}

function coverLayoutTable(spec, cover, sectionProps) {
  const contentHeight = computeContentHeightTwips(sectionProps);

  const titleStyle = cover.titleStyleId || (spec.paragraphStyles?.Title ? "Title" : "Heading1");
  const subtitleStyle = cover.subtitleStyleId || (spec.paragraphStyles?.Subtitle ? "Subtitle" : "Body");
  const metaStyle =
    cover.metaStyleId ||
    (spec.paragraphStyles?.BodyCompact ? "BodyCompact" : spec.paragraphStyles?.Body ? "Body" : undefined);

  const titleParas = [];
  if (cover.title) titleParas.push(stylekit.paragraph(spec, titleStyle, String(cover.title)));
  if (cover.subtitle) titleParas.push(stylekit.paragraph(spec, subtitleStyle, String(cover.subtitle)));

  // Metadata table (key-value)
  const metaRows = Array.isArray(cover.metaRows) ? cover.metaRows : [];
  const metaBlocks = [];
  if (metaRows.length) {
    const { table } = tablekit.makeKeyValueTable(spec, {
      rows: metaRows,
      styleId: metaStyle,
      keyWidthPct: cover.metaKeyWidthPct ?? 30,
      valueWidthPct: cover.metaValueWidthPct ?? 70,
      keyBold: true,
      cellPaddingPt: { top: 2, bottom: 2, left: 0, right: 0 },
    });
    metaBlocks.push(table);
  }

  if (cover.metaParagraphs) {
    metaBlocks.push(...cover.metaParagraphs);
  }

  const row1Height = Math.round(contentHeight * 0.68);
  const row2Height = Math.max(1, contentHeight - row1Height);

  const titleCell = new docx.TableCell({
    children: titleParas.length ? titleParas : [new docx.Paragraph({ text: "" })],
    verticalAlign: docx.VerticalAlignTable.CENTER,
  });

  const metaCell = new docx.TableCell({
    children: metaBlocks.length ? metaBlocks : [new docx.Paragraph({ text: "" })],
    verticalAlign: docx.VerticalAlignTable.BOTTOM,
  });

  return new docx.Table({
    width: { size: 100, type: docx.WidthType.PERCENTAGE },
    layout: docx.TableLayoutType.FIXED,
    borders: { top: { style: docx.BorderStyle.NONE, size: 0, color: "auto" }, bottom: { style: docx.BorderStyle.NONE, size: 0, color: "auto" }, left: { style: docx.BorderStyle.NONE, size: 0, color: "auto" }, right: { style: docx.BorderStyle.NONE, size: 0, color: "auto" }, insideHorizontal: { style: docx.BorderStyle.NONE, size: 0, color: "auto" }, insideVertical: { style: docx.BorderStyle.NONE, size: 0, color: "auto" } },
    rows: [
      new docx.TableRow({
        height: { value: row1Height, rule: docx.HeightRule.ATLEAST },
        children: [titleCell],
        cantSplit: true,
      }),
      new docx.TableRow({
        height: { value: row2Height, rule: docx.HeightRule.ATLEAST },
        children: [metaCell],
        cantSplit: true,
      }),
    ],
  });
}

/**
 * Build two sections:
 * - cover section (no header/footer by default)
 * - body section (header/footer + optional page numbering reset)
 *
 * @param {object|string} specOrName
 * @param {object} cover - cover page content
 * @param {object} body - { children: [...] }
 */
function makeCoverAndBodySections(specOrName, cover, body) {
  const spec = typeof specOrName === "string" ? stylekit.loadBundledStyleSpec(specOrName) : specOrName;

  const coverProps = stylekit.buildSectionProperties(spec);
  const bodyProps = stylekit.buildSectionProperties(spec);

  // Common default: restart numbering at 1 for the body, while the cover is unnumbered.
  const restart = cover.restartPageNumbering !== false;
  if (restart) {
    bodyProps.page.pageNumbers = { start: 1 };
  }

  const coverHasHeaderFooter = cover.includeHeaderFooter === true;
  const coverHeaders = coverHasHeaderFooter ? { default: buildHeader(spec) } : { default: new docx.Header({ children: [] }) };
  const coverFooters = coverHasHeaderFooter ? { default: buildFooter(spec) } : { default: new docx.Footer({ children: [] }) };

  const coverChildren = [];
  coverChildren.push(coverLayoutTable(spec, cover, coverProps));
  coverChildren.push(new docx.Paragraph({ children: [new docx.PageBreak()] }));

  const bodyChildren = Array.isArray(body?.children) ? body.children : [];

  const sections = [
    {
      properties: { ...coverProps, titlePage: true },
      headers: coverHeaders,
      footers: coverFooters,
      children: coverChildren,
    },
    {
      properties: bodyProps,
      headers: { default: buildHeader(spec) },
      footers: { default: buildFooter(spec) },
      children: bodyChildren,
    },
  ];

  return sections;
}

module.exports = {
  makeCoverAndBodySections,
};
