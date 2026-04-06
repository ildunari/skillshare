'use strict';

/**
 * listkit.js
 *
 * Gap 8 fix: list numbering configs + a small manager to prevent numbering bugs.
 *
 * docx-js "footgun": list counters reset or collide when reference/instance isn't handled carefully.
 *
 * Usage:
 *   const { Document, Packer } = require("docx");
 *   const { ListManager, defaultNumberingConfig } = require("./scripts/listkit");
 *
 *   const lists = new ListManager(); // has lists.config for Document
 *   const steps = lists.numbered();  // new independent list instance
 *   const bullets = lists.bullets();
 *
 *   const doc = new Document({ numbering: { config: lists.config }, ... });
 *   const p = lists.item(steps, "First step");
 */

const docx = require("docx");
const stylekit = require("./stylekit");

function defaultNumberingConfig() {
  // Indentation values are in twips.
  const indent = (leftIn, hangingIn) => ({
    indent: {
      left: stylekit.inToTwips(leftIn),
      hanging: stylekit.inToTwips(hangingIn),
    },
  });

  const baseSpacing = {
    spacing: {
      before: 0,
      after: stylekit.ptToTwips(3),
      line: stylekit.multipleTo240(1.15),
      lineRule: docx.LineRuleType.AUTO,
    },
  };

  const bulletLevels = [
    {
      level: 0,
      format: docx.LevelFormat.BULLET,
      text: "•",
      alignment: docx.AlignmentType.LEFT,
      style: { paragraph: { ...indent(0.5, 0.25), ...baseSpacing } },
    },
    {
      level: 1,
      format: docx.LevelFormat.BULLET,
      text: "–",
      alignment: docx.AlignmentType.LEFT,
      style: { paragraph: { ...indent(0.75, 0.25), ...baseSpacing } },
    },
    {
      level: 2,
      format: docx.LevelFormat.BULLET,
      text: "•",
      alignment: docx.AlignmentType.LEFT,
      style: { paragraph: { ...indent(1.0, 0.25), ...baseSpacing } },
    },
  ];

  const numberedLevels = [
    {
      level: 0,
      format: docx.LevelFormat.DECIMAL,
      text: "%1.",
      alignment: docx.AlignmentType.LEFT,
      style: { paragraph: { ...indent(0.5, 0.25), ...baseSpacing } },
    },
    {
      level: 1,
      format: docx.LevelFormat.LOWER_LETTER,
      text: "%2)",
      alignment: docx.AlignmentType.LEFT,
      style: { paragraph: { ...indent(0.75, 0.25), ...baseSpacing } },
    },
    {
      level: 2,
      format: docx.LevelFormat.LOWER_ROMAN,
      text: "%3.",
      alignment: docx.AlignmentType.LEFT,
      style: { paragraph: { ...indent(1.0, 0.25), ...baseSpacing } },
    },
  ];

  const legalLevels = [
    {
      level: 0,
      format: docx.LevelFormat.DECIMAL,
      text: "%1.",
      isLegalNumberingStyle: true,
      alignment: docx.AlignmentType.LEFT,
      style: { paragraph: { ...indent(0.5, 0.25), ...baseSpacing } },
    },
    {
      level: 1,
      format: docx.LevelFormat.DECIMAL,
      text: "%1.%2.",
      isLegalNumberingStyle: true,
      alignment: docx.AlignmentType.LEFT,
      style: { paragraph: { ...indent(0.75, 0.25), ...baseSpacing } },
    },
    {
      level: 2,
      format: docx.LevelFormat.LOWER_LETTER,
      text: "(%3)",
      alignment: docx.AlignmentType.LEFT,
      style: { paragraph: { ...indent(1.0, 0.25), ...baseSpacing } },
    },
    {
      level: 3,
      format: docx.LevelFormat.LOWER_ROMAN,
      text: "(%4)",
      alignment: docx.AlignmentType.LEFT,
      style: { paragraph: { ...indent(1.25, 0.25), ...baseSpacing } },
    },
  ];

  const checkboxLevels = [
    {
      level: 0,
      format: docx.LevelFormat.BULLET,
      text: "☐",
      alignment: docx.AlignmentType.LEFT,
      style: { paragraph: { ...indent(0.5, 0.25), ...baseSpacing } },
    },
    {
      level: 1,
      format: docx.LevelFormat.BULLET,
      text: "☐",
      alignment: docx.AlignmentType.LEFT,
      style: { paragraph: { ...indent(0.75, 0.25), ...baseSpacing } },
    },
  ];

  return [
    { reference: "list-bullets", levels: bulletLevels },
    { reference: "list-numbered", levels: numberedLevels },
    { reference: "list-legal", levels: legalLevels },
    { reference: "list-checkbox", levels: checkboxLevels },
  ];
}

class ListManager {
  constructor(config = defaultNumberingConfig()) {
    this.config = config;
    this._nextInstanceByRef = new Map();
  }

  _allocInstance(reference) {
    const next = this._nextInstanceByRef.get(reference) ?? 0;
    this._nextInstanceByRef.set(reference, next + 1);
    return next;
  }

  bullets() {
    const reference = "list-bullets";
    return { type: "bullets", reference, instance: this._allocInstance(reference) };
  }

  numbered() {
    const reference = "list-numbered";
    return { type: "numbered", reference, instance: this._allocInstance(reference) };
  }

  legal() {
    const reference = "list-legal";
    return { type: "legal", reference, instance: this._allocInstance(reference) };
  }

  checkboxes() {
    const reference = "list-checkbox";
    return { type: "checkboxes", reference, instance: this._allocInstance(reference) };
  }

  /**
   * Create one list item paragraph.
   * @param {{reference:string, instance:number}} list
   * @param {string|any[]} childrenOrText
   * @param {object} options
   */
  item(list, childrenOrText, options = {}) {
    const style = options.styleId || "Body";
    const level = options.level ?? 0;

    let children = [];
    if (typeof childrenOrText === "string") {
      children = [new docx.TextRun({ text: childrenOrText })];
    } else if (Array.isArray(childrenOrText)) {
      children = childrenOrText;
    } else if (childrenOrText) {
      children = [childrenOrText];
    }

    return new docx.Paragraph({
      style,
      children,
      numbering: {
        reference: list.reference,
        level,
        instance: list.instance,
      },
      widowControl: options.widowControl,
    });
  }
}

module.exports = {
  defaultNumberingConfig,
  ListManager,
};
