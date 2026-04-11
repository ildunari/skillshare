#!/usr/bin/env node
/**
 * build.mjs — Build design tokens for all platforms using Style Dictionary v4.
 *
 * Usage:
 *   node build.mjs                      # Build all platforms
 *   node build.mjs --platform css       # Build CSS only
 *   node build.mjs --source ./tokens    # Custom source directory
 *
 * Requires: npm install style-dictionary@^4
 *
 * For sd-transforms (optional enhanced transforms):
 *   npm install @tokens-studio/sd-transforms@^1  (v1.x for SD v4; NOT v2.x which targets SD v5)
 */

import { readFileSync } from "fs";
import { dirname, resolve } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));

async function build() {
  // Parse args
  const args = process.argv.slice(2);
  const platformArg = args.includes("--platform")
    ? args[args.indexOf("--platform") + 1]
    : null;
  const sourceArg = args.includes("--source")
    ? args[args.indexOf("--source") + 1]
    : null;

  // Dynamic import (fail gracefully if not installed)
  let StyleDictionary;
  try {
    const sd = await import("style-dictionary");
    StyleDictionary = sd.default || sd;
  } catch {
    console.error(
      "Error: style-dictionary not found. Install with: npm install style-dictionary@^4"
    );
    process.exit(1);
  }

  // Load config
  const configModule = await import("./style-dictionary.config.mjs");
  const config = { ...configModule.default };

  // Override source if specified
  if (sourceArg) {
    config.source = [`${sourceArg}/**/*.json`];
  }

  // Create SD instance
  const sd = new StyleDictionary(config);

  // Build
  if (platformArg) {
    console.log(`Building platform: ${platformArg}`);
    await sd.buildPlatform(platformArg);
  } else {
    console.log("Building all platforms...");
    await sd.buildAllPlatforms();
  }

  console.log("✓ Build complete. Output in dist/");
}

build().catch((err) => {
  console.error("Build failed:", err.message);
  process.exit(1);
});
