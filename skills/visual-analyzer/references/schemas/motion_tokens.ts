/**
 * Motion Token Schema v1.0
 *
 * Hybrid schema merging:
 * - Agent's clean discriminated union types (MotionTrigger, Easing, MotionValue)
 * - Pro's operational fields (reducedMotion, platformSpring, evidence.keyframes, libraryGuess)
 *
 * Design principles:
 * - Tokens are specs, not prose. Every token is implementable.
 * - Confidence + evidence on every field so the agentic loop knows what to re-measure.
 * - Static token references (colorToken, spacingToken) link to the screenshot module's output.
 * - Platform-native hints stored alongside abstract params for faithful codegen.
 */

// ─── Triggers ────────────────────────────────────────────────────────────────

export type MotionTrigger =
  | { type: "load"; scope?: "screen" | "component" }
  | { type: "route"; action: "push" | "pop" | "replace"; fromRoute?: string; toRoute?: string }
  | { type: "click"; elementId: string }
  | { type: "hover"; elementId: string }
  | { type: "focus"; elementId: string }
  | { type: "toggle"; stateFrom?: string; stateTo?: string; elementId: string }
  | { type: "scroll"; containerId?: string; timeline?: ScrollTimelineSpec }
  | { type: "gesture"; kind: GestureSpec }
  | { type: "media"; event: "play" | "pause" | "end" | "load" }
  | { type: "unknown"; description?: string };

export type ScrollTimelineSpec =
  | { mode: "triggered"; start: ViewportPosition; end?: ViewportPosition }
  | { mode: "scrubbed"; axis?: "x" | "y"; start: ViewportPosition; end: ViewportPosition; scrollRangePx?: number }
  | { mode: "snap"; snapPoints: number[] }
  | { mode: "parallax"; rate: number };

export type ViewportPosition = {
  type: "viewport";
  at: number; // 0..1 (0 = top/left, 1 = bottom/right)
};

export type GestureSpec =
  | { type: "drag"; axis: "x" | "y" | "both"; bounds?: { minPx: number; maxPx: number } }
  | { type: "swipe"; axis: "x" | "y"; thresholdPx?: number }
  | { type: "pinch"; minScale?: number; maxScale?: number }
  | { type: "longPress"; durationMs?: number }
  | { type: "pullToRefresh" };

// ─── Timing & Easing ────────────────────────────────────────────────────────

export type Easing =
  | { type: "linear" }
  | { type: "cubic-bezier"; x1: number; y1: number; x2: number; y2: number; presetName?: string }
  | { type: "spring"; params: SpringParams }
  | { type: "steps"; steps: number; jumpTerm?: "start" | "end" | "both" | "none" }
  | { type: "named"; name: string } // "easeOut", "fastOutSlowIn", etc — for when you can label but not fit
  | { type: "unknown"; guess?: string };

export type SpringParams = {
  // Canonical physical params
  stiffness?: number;
  damping?: number;
  mass?: number;
  initialVelocity?: number;

  // Platform-native mappings (from Pro — critical for faithful codegen)
  platformHints?: {
    ios?: { response?: number; dampingFraction?: number };
    android?: { dampingRatio?: number; stiffness?: number };
    framerMotion?: { stiffness?: number; damping?: number; mass?: number };
    reactSpring?: { tension?: number; friction?: number; mass?: number };
  };

  presetName?: string; // "bouncy", "snappy", "default", etc.
};

export type Timing = {
  durationMs: number;
  delayMs?: number;
  easing: Easing;
  iterations?: number | "infinite";
  direction?: "normal" | "reverse" | "alternate" | "alternate-reverse";
  fillMode?: "none" | "forwards" | "backwards" | "both";
};

// ─── Values & Properties ────────────────────────────────────────────────────

export type MotionValue =
  | { kind: "number"; value: number; unit?: "px" | "%" | "deg" | "vw" | "vh" | "rem" }
  | { kind: "colorToken"; token: string }  // refs static design token
  | { kind: "spacingToken"; token: string }
  | { kind: "radiusToken"; token: string }
  | { kind: "opacity"; value: number }     // 0..1
  | { kind: "color"; hex: string }         // raw fallback when no token match
  | { kind: "transform"; value: string };  // raw CSS transform string

export type MotionProperty =
  | "opacity"
  | "transform.translateX"
  | "transform.translateY"
  | "transform.scale"
  | "transform.scaleX"
  | "transform.scaleY"
  | "transform.rotate"
  | "filter.blur"
  | "backgroundColor"
  | "color"
  | "borderColor"
  | "borderRadius"
  | "shadow.elevation"
  | "width"
  | "height"
  | "layout.bounds"  // shared element / layout animation
  | "clipPath"
  | "custom";

// ─── Keyframes & Tracks ─────────────────────────────────────────────────────

export type Keyframe = {
  t: number;         // 0..1 normalized time
  value: MotionValue;
  easing?: Easing;   // per-segment easing (between this keyframe and next)
};

export type MotionTrack = {
  targetId: string;
  targetPart?: string;  // "icon", "label", "container", "indicator", etc.
  property: MotionProperty;
  customProperty?: string; // when property === "custom"

  // Simple from→to OR rich keyframes (use one)
  from?: MotionValue;
  to?: MotionValue;
  keyframes?: Keyframe[];

  timing: Timing;

  confidence?: {
    overall: number;
    fields?: Partial<Record<
      "targetId" | "property" | "from" | "to" | "durationMs" | "delayMs" | "easing",
      number
    >>;
  };
};

// ─── Orchestration ──────────────────────────────────────────────────────────

export type Orchestration =
  | { kind: "single" }
  | { kind: "parallel"; groupId: string }
  | { kind: "sequence"; groupId: string; order: number }
  | {
      kind: "stagger";
      groupId: string;
      eachDelayMs: number;
      direction?: "forward" | "reverse" | "center-out";
      order?: "dom" | "custom";
      customOrder?: string[];
    }
  | {
      kind: "timeline";
      groupId: string;
      labels?: Record<string, number>; // named time offsets
    };

// ─── Library Fingerprint (from Pro — probability distribution) ──────────────

export type LibraryGuess = {
  cssTransition?: number;
  cssKeyframes?: number;
  waapi?: number;
  gsap?: number;
  framerMotion?: number;
  reactSpring?: number;
  swiftUI?: number;
  compose?: number;
  lottie?: number;
  rive?: number;
  custom?: number;
};

// ─── Evidence & Confidence ──────────────────────────────────────────────────

export type Evidence = {
  videoSegment: { startSec: number; endSec: number };
  sampledFps?: number;
  measurementMethod?: "point_tracking" | "optical_flow" | "frame_diff" | "codec_mv" | "gemini_only" | "instrumented";
  // From Pro: store sampled progress curve for re-fitting
  progressCurve?: Array<{ tNorm: number; progress: number }>;
  fitResidual?: number;  // RMS error of easing fit
  notes?: string[];
};

// ─── Accessibility ──────────────────────────────────────────────────────────

export type ReducedMotionStrategy = {
  strategy: "remove" | "crossfade" | "shorten" | "simplify";
  maxDurationMs?: number;
  fallbackEasing?: Easing;
};

// ─── The Token ──────────────────────────────────────────────────────────────

export type MotionToken = {
  id: string;
  name?: string;
  screenId?: string;

  trigger: MotionTrigger;
  orchestration?: Orchestration;
  tracks: MotionTrack[];

  // From Pro: probability distribution over likely implementation
  libraryGuess?: LibraryGuess;

  overallConfidence: number;
  evidence?: Evidence;

  // From Pro: accessibility
  reducedMotion?: ReducedMotionStrategy;

  notes?: string;
};

// ─── Motion Taxonomy Categories ─────────────────────────────────────────────
// (from Agent's 10-category system — used for classification/routing)

export type MotionCategory =
  | "entrance_exit"        // fade, slide, scale, blur, mask
  | "state_transition"     // color, size, elevation, shape
  | "navigation"           // route push/pop, shared element
  | "scroll_linked"        // parallax, reveal, scrub, snap, sticky
  | "micro_interaction"    // press, hover, toggle, ripple, focus, validation
  | "loading_progress"     // spinner, skeleton, shimmer, progress bar
  | "gesture_physics"      // drag, swipe, inertia, spring settle, bounce
  | "ambient"              // background gradients, particles, loops
  | "text_number"          // count-up, typewriter, character morph
  | "media"                // image crossfade, blur-up, poster transition
  | "unknown";

// ─── Top-Level Spec ─────────────────────────────────────────────────────────

export type MotionSpec = {
  version: "1.0";
  sourceVideo?: {
    uri?: string;
    durationSec?: number;
    fps?: number;
    resolution?: { width: number; height: number };
  };
  platformGuess?: {
    value: "web" | "ios" | "android" | "desktop" | "design_tool" | "unknown";
    confidence: number;
    cues: string[];
  };
  tokens: MotionToken[];
  // Global orchestration groups (for cross-token coordination)
  groups?: Array<{
    groupId: string;
    name?: string;
    category: MotionCategory;
    tokenIds: string[];
  }>;
};
