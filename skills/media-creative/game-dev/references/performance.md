# Performance Optimization Reference

## Frame Budget

- **60 fps** = 16.67ms total per frame
- **30 fps** = 33.33ms total per frame

Budget breakdown (60fps):
- JavaScript (game logic): 8-10ms
- Rendering: 4-6ms
- Browser overhead: 2-3ms

## Mobile Performance

### Battery Efficiency
- Offer 30fps mode for mobile
- Pause simulation when tab hidden
- Reduce particles/effects on low-end devices
- Use Page Visibility API

```javascript
let targetFPS = 60;
const STEP_60 = 1/60;
const STEP_30 = 1/30;

function enableLowPowerMode() {
  targetFPS = 30;
}

// Adjust step based on target FPS
const STEP = targetFPS === 60 ? STEP_60 : STEP_30;
```

### Throttle Detection
```javascript
// Measure frame time
let frameStart = performance.now();
function measureFrame() {
  const now = performance.now();
  const frameTime = now - frameStart;
  frameStart = now;
  
  if (frameTime > 20) { // Slower than 50fps
    // Reduce quality
    maxParticles = 100;
  }
}
```

## Canvas Optimization

### Layered Canvases
```javascript
// Static background
const bgCanvas = document.createElement('canvas');
const bgCtx = bgCanvas.getContext('2d');
// Draw background once
drawBackground(bgCtx);

// Game layer
function render(ctx) {
  ctx.drawImage(bgCanvas, 0, 0); // Blit static BG
  drawDynamic(ctx); // Draw moving sprites
}
```

### Dirty Rectangles
Only redraw changed regions (best for sparse updates):
```javascript
const dirtyRects = [];

function markDirty(x, y, w, h) {
  dirtyRects.push({x, y, w, h});
}

function render(ctx) {
  for (const rect of dirtyRects) {
    ctx.clearRect(rect.x, rect.y, rect.w, rect.h);
    // Redraw only this region
    drawRegion(ctx, rect);
  }
  dirtyRects.length = 0;
}
```

### Batch Draw Calls
Minimize state changes:
```javascript
// ✅ Good: Group by texture/style
ctx.fillStyle = '#f00';
for (const enemy of enemies) {
  ctx.fillRect(enemy.x, enemy.y, 32, 32);
}

ctx.fillStyle = '#0f0';
for (const pickup of pickups) {
  ctx.fillRect(pickup.x, pickup.y, 16, 16);
}

// ❌ Bad: Interleaved state changes
for (const entity of allEntities) {
  ctx.fillStyle = entity.color; // State change every iteration
  ctx.fillRect(entity.x, entity.y, entity.w, entity.h);
}
```

## Memory Management

### Avoid Allocations in Hot Paths
```javascript
// ✅ Good: Reuse vector
const tempVec = {x: 0, y: 0};
function normalize(v) {
  const len = Math.hypot(v.x, v.y) || 1;
  tempVec.x = v.x / len;
  tempVec.y = v.y / len;
  return tempVec;
}

// ❌ Bad: Allocate every call
function normalize(v) {
  const len = Math.hypot(v.x, v.y) || 1;
  return {x: v.x / len, y: v.y / len}; // GC pressure
}
```

### Array Management
```javascript
// ✅ Good: Reuse arrays
const enemies = [];
function removeEnemy(id) {
  const idx = enemies.findIndex(e => e.id === id);
  if (idx >= 0) enemies.splice(idx, 1);
}

// Better: Mark inactive and filter periodically
function removeEnemy(id) {
  const e = enemies.find(e => e.id === id);
  if (e) e.active = false;
}

function cleanup() {
  enemies = enemies.filter(e => e.active); // Every 60 frames
}
```

## Asset Loading

### Off-Thread Decoding
```javascript
// Images
async function loadImage(url) {
  const res = await fetch(url);
  const blob = await res.blob();
  return await createImageBitmap(blob);
}

// Audio
const audioCtx = new AudioContext();
async function loadSound(url) {
  const res = await fetch(url);
  const buf = await res.arrayBuffer();
  return await audioCtx.decodeAudioData(buf);
}
```

## Profiling

### Chrome DevTools
1. Open Performance tab
2. Record gameplay session
3. Look for:
   - Long frames (>16.67ms)
   - GC pauses (yellow triangles)
   - Expensive functions (wide bars)

### Custom Markers
```javascript
function update(dt) {
  performance.mark('update-start');
  // ... game logic ...
  performance.mark('update-end');
  performance.measure('update', 'update-start', 'update-end');
}

// View in Performance timeline
```

### FPS Counter
```javascript
let frames = 0;
let lastFPSUpdate = performance.now();

function showFPS() {
  frames++;
  const now = performance.now();
  if (now - lastFPSUpdate >= 1000) {
    console.log(`FPS: ${frames}`);
    frames = 0;
    lastFPSUpdate = now;
  }
}
```

## Audio Performance

### Pool Audio Nodes
```javascript
const audioCtx = new AudioContext();
const gainPool = [];

function getGainNode() {
  return gainPool.pop() || audioCtx.createGain();
}

function releaseGainNode(node) {
  node.gain.value = 1;
  gainPool.push(node);
}
```

### Autoplay Policies
```javascript
// Resume on first user gesture
canvas.addEventListener('pointerup', () => {
  audioCtx.resume();
}, {once: true});
```
