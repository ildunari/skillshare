#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const DEFAULT_PRESETS = {
  agent_polished: {
    description: "Recommended default for agent usage: QA on, animation pass on, auto-build animations off for reliability.",
    skipPreflight: false,
    skipAnimations: false,
    autoAnimations: false,
    strictPreflight: false,
    visionQa: false,
  },
  agent_polished_animated: {
    description: "Curated animation mode: keep animation injector on, avoid risky auto-targeting unless explicitly enabled.",
    skipPreflight: false,
    skipAnimations: false,
    autoAnimations: false,
    strictPreflight: false,
    visionQa: false,
  },
  agent_strict: {
    description: "Maximum safety mode: fail fast on any preflight hard-fail.",
    skipPreflight: false,
    skipAnimations: false,
    autoAnimations: false,
    strictPreflight: true,
    visionQa: false,
  },
  agent_fast: {
    description: "Fast draft mode: skip preflight checks and animation injection.",
    skipPreflight: true,
    skipAnimations: true,
    autoAnimations: false,
    strictPreflight: false,
    visionQa: false,
  },
};

function usage() {
  console.error(
    "Usage: node scripts/pipeline.js <ir.json> <output.pptx> [--preset <name>] [--skip-preflight] [--skip-animations] [--auto-animations] [--strict-preflight] [--vision-qa]"
  );
  console.error("Preset names: agent_polished (default), agent_polished_animated, agent_strict, agent_fast");
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, `'\\''`)}'`;
}

function loadPresetMap(presetsPath) {
  let userPresets = {};
  if (fs.existsSync(presetsPath)) {
    try {
      const parsed = JSON.parse(fs.readFileSync(presetsPath, "utf8"));
      if (parsed && typeof parsed === "object" && !Array.isArray(parsed)) {
        userPresets = parsed;
      }
    } catch (error) {
      console.warn(`[pipeline] Warning: failed to parse presets file: ${presetsPath}`);
    }
  }
  return { ...DEFAULT_PRESETS, ...userPresets };
}

function resolvePreset(presets, presetName) {
  const preset = presets[presetName];
  if (!preset || typeof preset !== "object") {
    const names = Object.keys(presets).sort().join(", ");
    throw new Error(`Unknown preset '${presetName}'. Available presets: ${names}`);
  }
  return {
    skipPreflight: !!preset.skipPreflight,
    skipAnimations: !!preset.skipAnimations,
    autoAnimations: !!preset.autoAnimations,
    strictPreflight: !!preset.strictPreflight,
    visionQa: !!preset.visionQa,
  };
}

function runStep(name, command) {
  console.log(`[pipeline] Starting: ${name}`);
  execSync(command, { stdio: "inherit" });
  console.log(`[pipeline] Completed: ${name}`);
}

function runPythonStep(name, scriptPath, args, options = {}) {
  const failOnError = options.failOnError !== false;
  if (!fs.existsSync(scriptPath)) {
    console.warn(`[pipeline] Warning: missing script, skipping ${name}: ${scriptPath}`);
    return { ok: true, skipped: true };
  }

  const cmd = ["python3", shellQuote(scriptPath), ...args.map(shellQuote)].join(" ");
  try {
    runStep(name, cmd);
    return { ok: true, skipped: false };
  } catch (error) {
    const code = Number.isInteger(error && error.status) ? error.status : 1;
    if (failOnError) {
      throw error;
    }
    console.warn(`[pipeline] Warning: ${name} exited with code ${code}; continuing (use --strict-preflight to fail).`);
    return { ok: false, skipped: false, code };
  }
}

function runOptionalPythonHook(name, scriptPath, args = []) {
  if (!fs.existsSync(scriptPath)) {
    console.warn(`[pipeline] Warning: optional hook unavailable, skipping ${name}: ${scriptPath}`);
    return { ok: false, skipped: true };
  }
  return runPythonStep(name, scriptPath, args, { failOnError: false });
}

function resolveExistingPath(candidates) {
  for (const candidate of candidates) {
    if (candidate && fs.existsSync(candidate)) return candidate;
  }
  return null;
}

function main() {
  const argv = process.argv.slice(2);
  const positional = [];
  const overrides = {
    skipPreflight: null,
    skipAnimations: null,
    autoAnimations: null,
    strictPreflight: null,
    visionQa: null,
  };
  let presetName = process.env.PPTX_AGENT_PRESET || "agent_polished";

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--preset") {
      const name = argv[i + 1];
      if (!name || name.startsWith("--")) {
        console.error("[pipeline] --preset requires a preset name");
        usage();
        process.exit(1);
      }
      presetName = name;
      i += 1;
      continue;
    }
    if (arg === "--skip-preflight") {
      overrides.skipPreflight = true;
      continue;
    }
    if (arg === "--skip-animations") {
      overrides.skipAnimations = true;
      continue;
    }
    if (arg === "--auto-animations") {
      overrides.autoAnimations = true;
      continue;
    }
    if (arg === "--strict-preflight") {
      overrides.strictPreflight = true;
      continue;
    }
    if (arg === "--vision-qa") {
      overrides.visionQa = true;
      continue;
    }
    if (arg.startsWith("--")) {
      console.error(`[pipeline] Unknown flag: ${arg}`);
      usage();
      process.exit(1);
    }
    positional.push(arg);
  }

  if (positional.length !== 2) {
    usage();
    process.exit(1);
  }

  const [irPathInput, outputPathInput] = positional;
  const irPath = path.resolve(process.cwd(), irPathInput);
  const outputPath = path.resolve(process.cwd(), outputPathInput);
  const animTempOut = path.join(
    path.dirname(outputPath),
    `.${path.basename(outputPath)}.anim-${Date.now()}-${Math.random().toString(36).slice(2)}.pptx`
  );

  const scriptsDir = __dirname;
  const preflightIrPath = path.resolve(scriptsDir, "preflight_ir.py");
  const renderPptxPath = path.resolve(scriptsDir, "render_pptx.js");
  const injectAnimationsPath = path.resolve(scriptsDir, "inject_animations.py");
  const preflightPptxPath = path.resolve(scriptsDir, "preflight_pptx.py");
  const renderThumbnailsPath = path.resolve(scriptsDir, "render_thumbnails.py");
  const assetPlanningPath = path.resolve(scriptsDir, "asset_planning.py");
  const visionQaPath = resolveExistingPath([
    path.resolve(scriptsDir, "vision_qa.py"),
    path.resolve(scriptsDir, "vision_qa_pptx.py"),
    path.resolve(scriptsDir, "vision_critique.py"),
  ]);
  const themesPath = path.resolve(__dirname, "../assets/themes.json");
  const palettesPath = path.resolve(__dirname, "../assets/palettes.json");
  const presetsPath = path.resolve(__dirname, "../assets/agent-presets.json");
  const presetMap = loadPresetMap(presetsPath);
  let options;

  try {
    options = resolvePreset(presetMap, presetName);
  } catch (error) {
    console.error(`[pipeline] ${error.message}`);
    usage();
    process.exit(1);
  }
  for (const key of Object.keys(overrides)) {
    if (overrides[key] !== null) {
      options[key] = overrides[key];
    }
  }
  console.log(`[pipeline] Preset: ${presetName}`);

  const runId = `${Date.now()}-${Math.random().toString(36).slice(2)}`;
  const assetPlanReportPath = path.join(path.dirname(outputPath), `.${path.basename(outputPath)}.asset-plan-${runId}.json`);
  const visionReportPath = path.join(path.dirname(outputPath), `.${path.basename(outputPath)}.vision-${runId}.json`);
  const thumbnailsDir = path.join(path.dirname(outputPath), `.${path.basename(outputPath)}.thumbnails-${runId}`);
  let hasAssetPlanReport = false;
  let hasThumbnails = false;

  try {
    if (options.skipPreflight) {
      console.log("[pipeline] Skipping: preflight_ir.py (--skip-preflight)");
    } else {
      const preflightArgs = [irPath];
      if (fs.existsSync(themesPath)) {
        preflightArgs.push("--themes", themesPath);
      }
      if (fs.existsSync(palettesPath)) {
        preflightArgs.push("--palettes", palettesPath);
      }
      runPythonStep("preflight_ir.py", preflightIrPath, preflightArgs, { failOnError: options.strictPreflight });
    }

    const assetPlanningResult = runOptionalPythonHook("asset_planning.py", assetPlanningPath, [irPath, "--out", assetPlanReportPath]);
    hasAssetPlanReport = assetPlanningResult.ok && fs.existsSync(assetPlanReportPath);
    if (assetPlanningResult.skipped || !hasAssetPlanReport) {
      console.warn("[pipeline] Warning: asset-planning stage did not produce a report; continuing render path.");
    }

    runStep(
      "render_pptx.js",
      ["node", shellQuote(renderPptxPath), shellQuote(irPath), shellQuote(outputPath)].join(" ")
    );

    if (options.skipAnimations) {
      console.log("[pipeline] Skipping: inject_animations.py (--skip-animations)");
    } else {
      runPythonStep("inject_animations.py", injectAnimationsPath, [
        outputPath,
        "--ir",
        irPath,
        "--out",
        animTempOut,
        ...(options.autoAnimations ? ["--auto"] : []),
      ]);
      if (fs.existsSync(animTempOut)) {
        fs.renameSync(animTempOut, outputPath);
      }
    }

    if (options.visionQa) {
      const thumbResult = runOptionalPythonHook("render_thumbnails.py", renderThumbnailsPath, [
        outputPath,
        thumbnailsDir,
        "--manifest",
        `${thumbnailsDir}.manifest.json`,
      ]);
      hasThumbnails = thumbResult.ok && fs.existsSync(thumbnailsDir);
      if (!hasThumbnails) {
        console.warn("[pipeline] Warning: vision QA requested but thumbnails were not generated.");
      }

      if (visionQaPath) {
        const visionArgs = [outputPath, "--ir", irPath, "--out", visionReportPath];
        if (hasThumbnails) {
          visionArgs.push("--thumbnails-dir", thumbnailsDir);
        }
        runOptionalPythonHook(path.basename(visionQaPath), visionQaPath, visionArgs);
      } else {
        console.warn("[pipeline] Warning: vision QA hook script not found (expected vision_qa.py/vision_qa_pptx.py/vision_critique.py).");
      }
    }

    if (options.skipPreflight) {
      console.log("[pipeline] Skipping: preflight_pptx.py (--skip-preflight)");
    } else {
      const preflightPptxArgs = [outputPath];
      if (hasAssetPlanReport) {
        preflightPptxArgs.push("--asset-plan-report", assetPlanReportPath);
      }
      if (options.visionQa) {
        preflightPptxArgs.push("--vision-report", visionReportPath, "--thumbnails-dir", thumbnailsDir);
      }
      runPythonStep("preflight_pptx.py", preflightPptxPath, preflightPptxArgs, { failOnError: options.strictPreflight });
    }
  } catch (error) {
    const code = Number.isInteger(error && error.status) ? error.status : 1;
    console.error(`[pipeline] Failed with exit code ${code}`);
    process.exit(code);
  } finally {
    if (fs.existsSync(animTempOut)) {
      fs.unlinkSync(animTempOut);
    }
    if (fs.existsSync(assetPlanReportPath)) {
      fs.unlinkSync(assetPlanReportPath);
    }
    if (fs.existsSync(visionReportPath)) {
      fs.unlinkSync(visionReportPath);
    }
    if (fs.existsSync(`${thumbnailsDir}.manifest.json`)) {
      fs.unlinkSync(`${thumbnailsDir}.manifest.json`);
    }
    if (fs.existsSync(thumbnailsDir)) {
      fs.rmSync(thumbnailsDir, { recursive: true, force: true });
    }
  }
}

main();
