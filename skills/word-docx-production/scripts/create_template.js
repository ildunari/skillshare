'use strict';

/**
 * scripts/create_template.js
 *
 * Gap 6 fix: fast creation path.
 *
 * Creates a styled DOCX using the bundled style specs (business/academic/technical),
 * with a cover page, sample sections, lists, a data table, and an optional embedded
 * sample figure.
 *
 * Usage:
 *   node scripts/create_template.js --style business --title "QBR" --subtitle "Q4 FY2025" --authors "Jane Doe; John Smith" --output out.docx
 */

const fs = require("fs");
const path = require("path");
const docx = require("docx");

const stylekit = require("./stylekit");
const tablekit = require("./tablekit");
const coverkit = require("./coverkit");
const { ListManager } = require("./listkit");

function parseArgs(argv) {
  const args = {};
  const rest = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (!next || next.startsWith("-")) {
        args[key] = true;
      } else {
        args[key] = next;
        i++;
      }
    } else if (a.startsWith("-")) {
      const key = a.slice(1);
      const next = argv[i + 1];
      if (!next || next.startsWith("-")) {
        args[key] = true;
      } else {
        args[key] = next;
        i++;
      }
    } else {
      rest.push(a);
    }
  }
  return { args, rest };
}

function splitAuthors(s) {
  if (!s) return [];
  return String(s)
    .split(/[;,]/g)
    .map((x) => x.trim())
    .filter(Boolean);
}

function exists(p) {
  try {
    fs.accessSync(p, fs.constants.R_OK);
    return true;
  } catch {
    return false;
  }
}

function addFigure(spec, styleName) {
  const imgPath = path.join(__dirname, "..", "assets", "sample-figures", `figure_${styleName}.png`);
  if (!exists(imgPath)) return [];

  const data = fs.readFileSync(imgPath);
  // 5.5 in wide at ~96 dpi => ~528px. We'll set a safe width/height in pixels.
  // Word will scale appropriately.
  const img = new docx.ImageRun({
    data,
    transformation: { width: 520, height: 312 },
  });

  const figurePara = new docx.Paragraph({
    alignment: docx.AlignmentType.CENTER,
    children: [img],
  });

  const captionText = styleName === "academic" ? "Figure 1. Example trend across months." : "Figure 1. Example trend (sample figure).";
  const caption = stylekit.paragraph(spec, spec.paragraphStyles?.FigureCaption ? "FigureCaption" : "BodyCompact", captionText, { keepNext: false });

  return [figurePara, caption];
}

function buildBody(spec, styleName, title) {
  const lists = new ListManager();
  const bullets = lists.bullets();
  const steps = lists.numbered();

  const blocks = [];
  blocks.push(stylekit.paragraph(spec, "Heading1", "Overview"));
  blocks.push(
    stylekit.paragraph(
      spec,
      "Body",
      `This document was generated with docx-enhanced (${styleName} style). It demonstrates headings, body text, lists, tables, and an embedded figure.`
    )
  );

  blocks.push(stylekit.paragraph(spec, "Heading2", "Key points"));
  blocks.push(lists.item(bullets, "All paragraph formatting is style-driven (no manual font fiddling).", { styleId: "Body" }));
  blocks.push(lists.item(bullets, "Tables have readable padding, header shading, and repeatable header rows.", { styleId: "Body" }));
  blocks.push(lists.item(bullets, "List numbering uses independent instances to avoid counter collisions.", { styleId: "Body" }));

  blocks.push(stylekit.paragraph(spec, "Heading2", "Example process"));
  blocks.push(lists.item(steps, "Define the document style system (business/academic/technical).", { styleId: "Body" }));
  blocks.push(lists.item(steps, "Write content using semantic styles (Heading1, Body, Quote).", { styleId: "Body" }));
  blocks.push(lists.item(steps, "Run QA (OOXML lint + PDF composition checks).", { styleId: "Body" }));

  blocks.push(stylekit.paragraph(spec, "Heading1", "Example table"));

  const { blocks: tableBlocks } = tablekit.makeDataTable(spec, {
    caption: styleName === "academic" ? "Table 1. Example dataset." : "Table 1. Example dataset (sample).",
    headers: ["Metric", "Value", "Notes"],
    rows: [
      ["Revenue ($M)", 12.3, "FY2025"],
      ["Gross margin (%)", 42.1, "Audited"],
      ["Headcount", 57, "End of Q4"],
    ],
  });
  blocks.push(...tableBlocks);

  blocks.push(stylekit.paragraph(spec, "Heading1", "Example figure"));
  blocks.push(...addFigure(spec, styleName));

  return { blocks, numberingConfig: lists.config };
}

async function main() {
  const { args } = parseArgs(process.argv.slice(2));

  const styleName = (args.style || args.s || "business").toString().toLowerCase();
  const title = args.title || "Document Title";
  const subtitle = args.subtitle || "";
  const authors = splitAuthors(args.authors || args.author || "");
  const output = args.output || args.o || `template_${styleName}.docx`;

  const spec = stylekit.loadBundledStyleSpec(styleName);

  const { blocks: bodyChildren, numberingConfig } = buildBody(spec, styleName, title);

  // Cover metadata
  const date = new Date().toISOString().slice(0, 10);
  let metaRows = [];
  if (styleName === "business") {
    metaRows = [
      ["Prepared for", args.client || "Client Name"],
      ["Prepared by", authors.length ? authors.join(", ") : "Author Name"],
      ["Date", date],
      ["Version", args.version || "1.0"],
    ];
  } else if (styleName === "technical") {
    metaRows = [
      ["Project", args.project || title],
      ["Author(s)", authors.length ? authors.join(", ") : "Author Name"],
      ["Date", date],
      ["Revision", args.revision || "A"],
    ];
  } else {
    metaRows = [
      ["Author(s)", authors.length ? authors.join(", ") : "Author Name"],
      ["Affiliation", args.affiliation || "Institution / Department"],
      ["Date", date],
    ];
  }

  const coverOptions = {
    title,
    subtitle: subtitle || undefined,
    metaRows,
    includeHeaderFooter: styleName === "academic",
    restartPageNumbering: styleName !== "academic",
  };

  const sections = coverkit.makeCoverAndBodySections(spec, coverOptions, { children: bodyChildren });

  const doc = new docx.Document({
    styles: stylekit.buildDocxStyles(spec),
    numbering: { config: numberingConfig },
    sections,
  });

  const buf = await docx.Packer.toBuffer(doc);
  fs.writeFileSync(output, buf);
  process.stdout.write(`Wrote ${output} (${buf.length} bytes)\n`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
