# Paper.js: Vector Animation and Generative Graphics

> Scriptable vector graphics on HTML5 Canvas. Crisp at any resolution, immediate-mode rendering with retained object model, built-in hit testing, and smooth animation. Best for: generative art, interactive diagrams, data visualization with custom rendering, and any 2D graphic that benefits from resolution-independent vector quality.

## Contents
- When to Use (vs PIXI, D3, p5, Canvas2D) → CDN Setup for Artifacts
- Core Concepts: Items/Scene Graph → Paths → Styling/Gradients
- Animation: onFrame → Segment Animation → Shape Morphing → Growing/Drawing Paths
- Interaction: Mouse/Touch Events → Hit Testing
- Generative Art: Concentric Rings → Organic Blobs → Boolean Path Ops → Click-to-Regenerate
- Performance: Canvas Resolution → Item Count Limits → Optimization → Reduced Motion

---

## When to Use

| Scenario | Use Paper.js? |
|---|---|
| Generative vector art (mandalas, organic forms, geometric compositions) | Yes — its sweet spot |
| Interactive diagrams with click/hover on shapes | Yes — built-in hit testing |
| Smooth 2D path animation (morphing, growing, flowing) | Yes |
| Data visualization needing custom rendering beyond chart libs | Yes |
| High-particle-count systems (5K+) | No — use PIXI.js or WebGL |
| 3D anything | No — use Three.js |
| Simple UI animation (hover, toggle, reveal) | No — use CSS or Framer Motion |
| Scroll-driven effects | No — use CSS scroll-driven or GSAP |
| Pixel manipulation, image filters | No — use raw Canvas2D or WebGL |

### Paper.js vs alternatives

| Tool | Rendering | Object model | Best for |
|---|---|---|---|
| **Paper.js** | Canvas2D (vector quality) | Retained (scene graph) | Vector art, path operations, interactive shapes |
| **PIXI.js** | WebGL (GPU-accelerated) | Retained (display list) | High-performance 2D sprites, particles, game graphics |
| **D3.js** | SVG (DOM) | DOM manipulation | Data-driven documents, standard chart types |
| **p5.js** | Canvas2D (immediate) | None (redraw each frame) | Creative coding, sketches, learning |
| **Raw Canvas2D** | Canvas2D | None | Full control, pixel manipulation |

Paper.js is the right choice when you need the *intersection* of: crisp vectors, scriptable path operations (boolean, offset, smooth), an object model you can query/manipulate, and animation.

---

## CDN Setup for Artifacts

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/paper.js/0.12.18/paper-full.min.js"></script>

<canvas id="canvas" resize></canvas>

<script type="text/paperscript" canvas="canvas">
  // PaperScript mode — Point, Path, etc. available globally
  // Operators work on points: point1 + point2
</script>
```

Or JavaScript mode (more explicit, works better in complex setups):

```html
<script>
  paper.setup(document.getElementById("canvas"));

  const { Path, Point, Color, Group, view, project } = paper;

  // ... create items

  view.onFrame = function(event) {
    // Animation loop — event.time, event.delta, event.count
  };
</script>
```

**Use JavaScript mode in artifacts** — PaperScript's operator overloading requires a special script parser that can conflict with artifact sandbox CSP. JavaScript mode is more predictable.

---

## Core Concepts

### Items and the scene graph

Everything visible is an `Item` in a tree. `project.activeLayer` is the root.

```js
const circle = new Path.Circle({
  center: view.center,
  radius: 50,
  fillColor: "#a78bfa",
  strokeColor: "#7c3aed",
  strokeWidth: 2
});

// Items are immediately rendered and part of the scene graph
circle.position = new Point(200, 300);
circle.opacity = 0.8;
circle.rotation = 45;
circle.scale(1.5);

// Grouping
const group = new Group([circle, anotherPath]);
group.position = view.center;
```

### Paths

Paths are Paper.js's core primitive — sequences of segments with handles (cubic bezier control points).

```js
// Predefined shapes
const rect = new Path.Rectangle({ point: [50, 50], size: [200, 100], radius: 12 });
const ellipse = new Path.Ellipse({ point: [50, 50], size: [200, 100] });
const star = new Path.Star({ center: view.center, points: 8, radius1: 30, radius2: 60 });
const arc = new Path.Arc({ from: [0, 0], through: [50, -30], to: [100, 0] });
const line = new Path.Line({ from: [0, 0], to: [100, 100] });

// Freeform path
const path = new Path();
path.add(new Point(50, 50));
path.add(new Point(100, 30));
path.add(new Point(150, 80));
path.smooth(); // Convert sharp corners to smooth curves
path.closed = true;
```

### Styling

```js
path.fillColor = new Color(0.6, 0.35, 0.85, 0.7); // RGBA
path.strokeColor = "#e2e8f0";
path.strokeWidth = 1.5;
path.strokeCap = "round";
path.strokeJoin = "round";
path.dashArray = [8, 4]; // dashed line
path.shadowColor = new Color(0, 0, 0, 0.15);
path.shadowBlur = 12;
path.shadowOffset = new Point(0, 4);
path.blendMode = "multiply"; // screen, overlay, multiply, etc.
```

Gradients:

```js
path.fillColor = {
  gradient: {
    stops: [
      [new Color("#7dd3fc"), 0],
      [new Color("#a78bfa"), 0.5],
      [new Color("#fb7185"), 1]
    ],
    radial: true
  },
  origin: path.bounds.topLeft,
  destination: path.bounds.bottomRight
};
```

---

## Animation

### The `onFrame` handler

```js
view.onFrame = function(event) {
  // event.time — seconds since start
  // event.delta — seconds since last frame
  // event.count — frame count

  circle.position.x = view.center.x + Math.sin(event.time * 2) * 100;
  circle.rotation += event.delta * 30; // degrees per second
  circle.fillColor.hue += event.delta * 20; // color cycling
};
```

### Animating path segments

Paper.js paths have individually addressable segments with positions and handles:

```js
const wave = new Path();
for (let i = 0; i <= 20; i++) {
  wave.add(new Point(i * 40, 200));
}
wave.strokeColor = "#7dd3fc";
wave.strokeWidth = 2;

view.onFrame = function(event) {
  for (let i = 0; i < wave.segments.length; i++) {
    const seg = wave.segments[i];
    const sin = Math.sin(event.time * 3 + i * 0.5);
    seg.point.y = 200 + sin * 30;
  }
  wave.smooth(); // Recalculate bezier handles for smooth curve
};
```

### Morphing between shapes

```js
const shape1 = new Path.Circle({ center: view.center, radius: 80, insert: false });
const shape2 = new Path.Star({ center: view.center, points: 6, radius1: 40, radius2: 90, insert: false });

// Both need same segment count for smooth morphing
// Resample if needed:
const target = shape1.clone();
target.fillColor = "#a78bfa";

view.onFrame = function(event) {
  const t = (Math.sin(event.time) + 1) / 2; // 0–1 oscillation
  for (let i = 0; i < target.segments.length; i++) {
    const p1 = shape1.segments[i].point;
    const p2 = shape2.segments[i % shape2.segments.length].point;
    target.segments[i].point = p1.multiply(1 - t).add(p2.multiply(t));
  }
  target.smooth();
};
```

### Growing / drawing paths

```js
const path = new Path({
  strokeColor: "#fb7185",
  strokeWidth: 2,
  strokeCap: "round"
});

view.onFrame = function(event) {
  if (event.count % 3 === 0) { // Every 3rd frame
    const angle = event.time * 2;
    const r = 50 + event.time * 10;
    path.add(new Point(
      view.center.x + Math.cos(angle) * r,
      view.center.y + Math.sin(angle) * r
    ));
    path.smooth();

    // Limit trail length
    if (path.segments.length > 200) {
      path.removeSegment(0);
    }
  }
};
```

---

## Interaction

### Mouse/touch events on the view

```js
const tool = new Tool();

tool.onMouseMove = function(event) {
  // event.point — current position (Paper.js Point)
  // event.delta — movement since last event
  // event.downPoint — where mouse was pressed
  spotlight.position = event.point;
};

tool.onMouseDown = function(event) {
  // Click handling
};

tool.onMouseDrag = function(event) {
  // Drag handling
  path.add(event.point);
};
```

**Touch support:** Paper.js Tool events handle touch automatically — `onMouseMove` fires for `touchmove`, `onMouseDown` for `touchstart`. No separate touch handling needed for basic interaction. For multi-touch, access `event.event` (the native event) and check `touches`.

### Hit testing

```js
tool.onMouseMove = function(event) {
  const hitResult = project.hitTest(event.point, {
    segments: true,
    stroke: true,
    fill: true,
    tolerance: 5
  });

  if (hitResult) {
    hitResult.item.selected = true; // Visual feedback
  }
};
```

---

## Generative Art Patterns

### Concentric ring composition

```js
const palette = ["#7dd3fc", "#a78bfa", "#fb7185", "#fbbf24", "#34d399"];

for (let ring = 0; ring < 8; ring++) {
  const radius = 40 + ring * 35;
  const count = 8 + ring * 4;

  for (let i = 0; i < count; i++) {
    const angle = (i / count) * Math.PI * 2;
    const x = view.center.x + Math.cos(angle) * radius;
    const y = view.center.y + Math.sin(angle) * radius;

    const dot = new Path.Circle({
      center: new Point(x, y),
      radius: 2 + Math.random() * 4,
      fillColor: palette[(ring + i) % palette.length]
    });
    dot.opacity = 0.4 + Math.random() * 0.4;
  }
}
```

### Organic blob with noise

```js
function noisyCircle(center, radius, segments, time, noiseScale) {
  const path = new Path();
  for (let i = 0; i < segments; i++) {
    const angle = (i / segments) * Math.PI * 2;
    // Simple pseudo-noise using sin combinations
    const n = Math.sin(angle * 3 + time) * 0.15
            + Math.sin(angle * 5 - time * 0.7) * 0.1
            + Math.sin(angle * 7 + time * 1.3) * 0.05;
    const r = radius * (1 + n * noiseScale);
    path.add(new Point(
      center.x + Math.cos(angle) * r,
      center.y + Math.sin(angle) * r
    ));
  }
  path.closed = true;
  path.smooth();
  return path;
}
```

### Boolean path operations

Paper.js can union, intersect, subtract, exclude, and divide paths — powerful for generative compositions:

```js
const a = new Path.Circle({ center: [200, 200], radius: 60 });
const b = new Path.Circle({ center: [240, 200], radius: 60 });

const united = a.unite(b);       // union
const intersected = a.intersect(b); // overlap region
const subtracted = a.subtract(b);  // a minus b
const excluded = a.exclude(b);     // XOR

// Remove originals, keep result
a.remove();
b.remove();
united.fillColor = "#a78bfa";
```

### Click to regenerate composition

```js
function generate() {
  // Clear existing
  project.activeLayer.removeChildren();

  // Build new composition
  const palette = ["#7dd3fc", "#a78bfa", "#fb7185", "#fbbf24"];
  for (let ring = 0; ring < 8; ring++) {
    const radius = 40 + ring * 35;
    const count = 8 + ring * 4;
    for (let i = 0; i < count; i++) {
      const angle = (i / count) * Math.PI * 2 + Math.random() * 0.3;
      new Path.Circle({
        center: new Point(
          view.center.x + Math.cos(angle) * radius,
          view.center.y + Math.sin(angle) * radius
        ),
        radius: 2 + Math.random() * 5,
        fillColor: palette[(ring + i) % palette.length],
        opacity: 0.3 + Math.random() * 0.5
      });
    }
  }
}

// Initial generation
generate();

// Click anywhere to regenerate
const tool = new Tool();
tool.onMouseDown = function() { generate(); };
```

---

## Performance Considerations

### Canvas resolution

```js
// Paper.js handles DPR automatically with the `resize` attribute on canvas
// For manual control:
const canvas = document.getElementById("canvas");
const dpr = Math.min(devicePixelRatio, 2);
canvas.width = window.innerWidth * dpr;
canvas.height = window.innerHeight * dpr;
paper.setup(canvas);
view.viewSize = new Size(window.innerWidth, window.innerHeight);
```

### Item count limits

Paper.js redraws the entire canvas each frame via Canvas2D. Performance scales with item count and path complexity.

| Item count | Performance |
|---|---|
| < 500 paths | 60fps, no concerns |
| 500–2000 paths | 60fps with simple paths, monitor complex ones |
| 2000–5000 paths | May drop frames; group static items into CompoundPaths or rasterize |
| 5000+ paths | Consider PIXI.js or WebGL instead |

### Optimization techniques

```js
// Rasterize static complex groups
const raster = complexGroup.rasterize({ resolution: 72 * dpr, insert: true });
complexGroup.remove(); // Remove vector originals

// Use CompoundPath for many same-styled paths
const compound = new CompoundPath({
  children: manyPaths,
  fillColor: "#7dd3fc"
}); // One draw call instead of many

// Reduce segment counts with path.simplify()
detailedPath.simplify(2.5); // tolerance in points
```

---

## Reduced Motion

Paper.js generative art is typically ornamental. Under reduced motion:

```js
const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (prefersReduced) {
  // Generate the composition statically (no onFrame)
  generateComposition();
  view.draw();
  // Don't set view.onFrame — canvas is static
} else {
  generateComposition();
  view.onFrame = function(event) {
    updateAnimation(event);
  };
}
```

For interactive pieces, keep interaction (click to regenerate, hover to highlight) but remove continuous animation.

---

## Resize Handling

```js
view.onResize = function(event) {
  // event.size — new view size
  // event.delta — size change
  // Reposition centered elements:
  centeredGroup.position = view.center;
};
```

The `resize` attribute on the canvas element enables automatic canvas resizing. `view.onResize` fires after the resize so you can reposition/regenerate content.
