/**
 * style-dictionary.config.mjs — SD v4 with DTCG 2025.10 input
 *
 * Key SD v4 changes from v3:
 *   - hooks.formats (not "format")
 *   - hooks.transforms uses "filter" (not "matcher"), "transform" (not "transformer")
 *   - DTCG $value/$type/$description supported natively
 *   - sd-transforms v1.x for SD v4 (v2.x is SD v5, incompatible)
 *
 * Outputs: CSS custom properties, Tailwind theme, SwiftUI extensions, Compose objects, SCSS
 */

const config = {
  source: ["tokens/**/*.json"],

  // ── Custom hooks ──────────────────────────────────────────────────
  hooks: {
    transforms: {
      "dtcg/color-hex": {
        type: "value",
        filter: (token) => token.$type === "color" || token.type === "color",
        transform: (token) => {
          const val = token.$value ?? token.value;
          if (typeof val === "string" && val.startsWith("#")) {
            return val.toUpperCase();
          }
          return val;
        },
      },

      "dtcg/dimension-px": {
        type: "value",
        filter: (token) => token.$type === "dimension" || token.type === "dimension",
        transform: (token) => {
          const val = token.$value ?? token.value;
          if (typeof val === "number") return `${val}px`;
          if (typeof val === "string" && !val.endsWith("px") && !val.endsWith("rem") && !val.endsWith("em")) {
            return `${val}px`;
          }
          return val;
        },
      },

      "dtcg/shadow-css": {
        type: "value",
        filter: (token) => token.$type === "shadow" || token.type === "shadow",
        transform: (token) => {
          const v = token.$value ?? token.value;
          if (typeof v === "object") {
            const { offsetX = "0px", offsetY = "0px", blur = "0px", spread = "0px", color = "#000" } = v;
            return `${offsetX} ${offsetY} ${blur} ${spread} ${color}`;
          }
          return v;
        },
      },

      "dtcg/gradient-css": {
        type: "value",
        filter: (token) => token.$type === "gradient" || token.type === "gradient",
        transform: (token) => {
          const v = token.$value ?? token.value;
          if (typeof v === "object" && Array.isArray(v.stops)) {
            const stops = v.stops.map((s) => `${s.color} ${s.position}`).join(", ");
            if (v.type === "radial") {
              const center = v.center || "center";
              return `radial-gradient(circle at ${center}, ${stops})`;
            }
            const angle = v.angle || "180deg";
            return `linear-gradient(${angle}, ${stops})`;
          }
          return v;
        },
      },

      "dtcg/typography-shorthand": {
        type: "value",
        filter: (token) => token.$type === "typography" || token.type === "typography",
        transform: (token) => {
          const v = token.$value ?? token.value;
          if (typeof v === "object") {
            return JSON.stringify(v);
          }
          return v;
        },
      },

      "swift/color": {
        type: "value",
        filter: (token) => token.$type === "color" || token.type === "color",
        transform: (token) => {
          const hex = (token.$value ?? token.value).replace("#", "");
          const r = parseInt(hex.substring(0, 2), 16) / 255;
          const g = parseInt(hex.substring(2, 4), 16) / 255;
          const b = parseInt(hex.substring(4, 6), 16) / 255;
          const a = hex.length === 8 ? parseInt(hex.substring(6, 8), 16) / 255 : 1.0;
          return `Color(red: ${r.toFixed(3)}, green: ${g.toFixed(3)}, blue: ${b.toFixed(3)}, opacity: ${a.toFixed(3)})`;
        },
      },

      "swift/dimension": {
        type: "value",
        filter: (token) => token.$type === "dimension" || token.type === "dimension",
        transform: (token) => {
          const val = token.$value ?? token.value;
          const num = typeof val === "string" ? parseFloat(val) : val;
          return `CGFloat(${num})`;
        },
      },

      "compose/color": {
        type: "value",
        filter: (token) => token.$type === "color" || token.type === "color",
        transform: (token) => {
          const hex = (token.$value ?? token.value).replace("#", "");
          return `Color(0xFF${hex.toUpperCase().substring(0, 6)})`;
        },
      },

      "compose/dimension": {
        type: "value",
        filter: (token) => token.$type === "dimension" || token.type === "dimension",
        transform: (token) => {
          const val = token.$value ?? token.value;
          const num = typeof val === "string" ? parseFloat(val) : val;
          return `${num}.dp`;
        },
      },
    },

    formats: {
      "custom/css-vars": ({ dictionary }) => {
        const lines = [":root {"];
        dictionary.allTokens.forEach((token) => {
          const name = token.path.join("-");
          lines.push(`  --${name}: ${token.value};`);
        });
        lines.push("}");
        return lines.join("\n");
      },

      "custom/tailwind": ({ dictionary }) => {
        const theme = {};
        dictionary.allTokens.forEach((token) => {
          const name = token.path.join("-");
          theme[name] = `var(--${name})`;
        });
        return `/** @type {import('tailwindcss').Config} */\nmodule.exports = {\n  theme: {\n    extend: ${JSON.stringify(theme, null, 6)}\n  }\n};\n`;
      },

      "custom/swiftui": ({ dictionary }) => {
        const lines = [
          "import SwiftUI",
          "",
          "extension Color {",
        ];
        dictionary.allTokens
          .filter((t) => (t.$type || t.type) === "color")
          .forEach((token) => {
            const name = token.path.join("_").replace(/-/g, "_");
            lines.push(`    static let ${name} = ${token.value}`);
          });
        lines.push("}");
        lines.push("");
        lines.push("extension CGFloat {");
        dictionary.allTokens
          .filter((t) => (t.$type || t.type) === "dimension")
          .forEach((token) => {
            const name = token.path.join("_").replace(/-/g, "_");
            lines.push(`    static let ${name} = ${token.value}`);
          });
        lines.push("}");
        return lines.join("\n");
      },

      "custom/compose": ({ dictionary }) => {
        const lines = [
          "package com.design.tokens",
          "",
          "import androidx.compose.ui.graphics.Color",
          "import androidx.compose.ui.unit.dp",
          "import androidx.compose.ui.unit.sp",
          "",
          "object Tokens {",
        ];
        dictionary.allTokens.forEach((token) => {
          const name = token.path.join("_").replace(/-/g, "_");
          lines.push(`    val ${name} = ${token.value}`);
        });
        lines.push("}");
        return lines.join("\n");
      },

      "custom/scss-vars": ({ dictionary }) => {
        const lines = [];
        dictionary.allTokens.forEach((token) => {
          const name = token.path.join("-");
          lines.push(`$${name}: ${token.value};`);
        });
        return lines.join("\n");
      },
    },
  },

  // ── Platforms ──────────────────────────────────────────────────────
  platforms: {
    css: {
      transformGroup: "css",
      transforms: [
        "dtcg/color-hex",
        "dtcg/dimension-px",
        "dtcg/shadow-css",
        "dtcg/gradient-css",
      ],
      buildPath: "dist/css/",
      files: [
        {
          destination: "tokens.css",
          format: "custom/css-vars",
        },
      ],
    },

    tailwind: {
      transforms: [
        "dtcg/color-hex",
        "dtcg/dimension-px",
        "dtcg/shadow-css",
      ],
      buildPath: "dist/tailwind/",
      files: [
        {
          destination: "tokens.cjs",
          format: "custom/tailwind",
        },
      ],
    },

    swift: {
      transforms: ["swift/color", "swift/dimension"],
      buildPath: "dist/swift/",
      files: [
        {
          destination: "Tokens.swift",
          format: "custom/swiftui",
        },
      ],
    },

    compose: {
      transforms: ["compose/color", "compose/dimension"],
      buildPath: "dist/compose/",
      files: [
        {
          destination: "Tokens.kt",
          format: "custom/compose",
        },
      ],
    },

    scss: {
      transforms: [
        "dtcg/color-hex",
        "dtcg/dimension-px",
        "dtcg/shadow-css",
      ],
      buildPath: "dist/scss/",
      files: [
        {
          destination: "_tokens.scss",
          format: "custom/scss-vars",
        },
      ],
    },
  },
};

export default config;
