# Responsive Design Reference

## Canvas Scaling Strategies

### Virtual Canvas + Letterbox (Recommended)
Render at fixed "design resolution", scale to fit screen:

```javascript
const VIRTUAL_W = 360;
const VIRTUAL_H = 640;

const vCanvas = document.createElement('canvas');
vCanvas.width = VIRTUAL_W;
vCanvas.height = VIRTUAL_H;
const vCtx = vCanvas.getContext('2d');

function render(displayCtx, displayW, displayH) {
  // Draw game to virtual canvas at design resolution
  vCtx.fillStyle = '#000';
  vCtx.fillRect(0, 0, VIRTUAL_W, VIRTUAL_H);
  // ... draw game ...
  
  // Scale to display with letterboxing
  const scale = Math.min(displayW / VIRTUAL_W, displayH / VIRTUAL_H);
  const drawW = VIRTUAL_W * scale;
  const drawH = VIRTUAL_H * scale;
  const dx = (displayW - drawW) / 2;
  const dy = (displayH - drawH) / 2;
  
  displayCtx.clearRect(0, 0, displayW, displayH);
  displayCtx.imageSmoothingEnabled = false; // Pixel-perfect
  displayCtx.drawImage(vCanvas, 0, 0, VIRTUAL_W, VIRTUAL_H,
                       dx, dy, drawW, drawH);
}
```

### Pixel-Perfect Scaling
Integer scaling for crisp pixel art:

```javascript
function renderPixelPerfect(displayCtx, displayW, displayH) {
  const scale = Math.max(1, Math.floor(Math.min(
    displayW / VIRTUAL_W,
    displayH / VIRTUAL_H
  )));
  
  const drawW = VIRTUAL_W * scale;
  const drawH = VIRTUAL_H * scale;
  const dx = Math.floor((displayW - drawW) / 2);
  const dy = Math.floor((displayH - drawH) / 2);
  
  displayCtx.imageSmoothingEnabled = false;
  displayCtx.drawImage(vCanvas, 0, 0, VIRTUAL_W, VIRTUAL_H,
                       dx, dy, drawW, drawH);
}
```

## Device Pixel Ratio (DPR)

Handle high-DPI displays (Retina, etc):

```javascript
function setupCanvas(canvas) {
  const rect = canvas.parentElement.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  
  // Set backing size to CSS size × DPR
  canvas.width = Math.round(rect.width * dpr);
  canvas.height = Math.round(rect.height * dpr);
  
  // Set CSS size
  canvas.style.width = rect.width + 'px';
  canvas.style.height = rect.height + 'px';
  
  // Scale context
  const ctx = canvas.getContext('2d');
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  
  return ctx;
}
```

## Mobile UI Patterns

### Safe Area Insets (Notches)
```css
:root {
  --safe-top: env(safe-area-inset-top);
  --safe-bottom: env(safe-area-inset-bottom);
  --safe-left: env(safe-area-inset-left);
  --safe-right: env(safe-area-inset-right);
}

.hud-top {
  position: fixed;
  top: calc(8px + var(--safe-top));
  left: calc(8px + var(--safe-left));
}

.hud-bottom-right {
  position: fixed;
  right: calc(8px + var(--safe-right));
  bottom: calc(8px + var(--safe-bottom));
}
```

### Touch Targets
Minimum sizes for touchable elements:

- **iOS**: 44pt × 44pt (≈44px at 1x)
- **Android**: 48dp × 48dp (≈48px at 1x)
- **Spacing**: 8-12px between targets

```javascript
// Virtual joystick sizing
const JOYSTICK_RADIUS = 64; // Large enough for thumb

// Button sizing
const BUTTON_SIZE = 48;
const BUTTON_SPACING = 12;
```

### Dynamic Viewport Height
Handle mobile address bars:

```css
html, body {
  height: 100dvh; /* Dynamic viewport height */
  width: 100dvw;
}
```

## Orientation Handling

### Lock Orientation (Fullscreen Only)
```javascript
async function lockLandscape() {
  try {
    await screen.orientation.lock('landscape');
  } catch (e) {
    console.warn('Orientation lock not supported');
  }
}

// Only works in fullscreen
button.addEventListener('click', async () => {
  await canvas.requestFullscreen();
  await lockLandscape();
});
```

### Detect Orientation
```javascript
function getOrientation() {
  return window.innerWidth > window.innerHeight ? 'landscape' : 'portrait';
}

window.addEventListener('resize', () => {
  const orientation = getOrientation();
  console.log('Now in', orientation);
  // Adjust UI layout
});
```

## Input Coordinates

### Convert Screen to Virtual Coordinates
```javascript
function screenToVirtual(screenX, screenY, canvas) {
  const rect = canvas.getBoundingClientRect();
  const scale = Math.min(rect.width / VIRTUAL_W, rect.height / VIRTUAL_H);
  const offsetX = (rect.width - VIRTUAL_W * scale) / 2;
  const offsetY = (rect.height - VIRTUAL_H * scale) / 2;
  
  return {
    x: (screenX - rect.left - offsetX) / scale,
    y: (screenY - rect.top - offsetY) / scale
  };
}
```

## Testing Breakpoints

Test at these common widths:
- **Mobile**: 320px, 375px, 414px
- **Tablet**: 768px, 1024px
- **Desktop**: 1280px, 1920px

Use Chrome DevTools Device Mode:
1. Open DevTools (F12)
2. Toggle Device Toolbar (Ctrl+Shift+M)
3. Select device or set custom dimensions
4. Enable touch simulation
5. Throttle CPU (4x slowdown) for mobile testing

## Fullscreen API

```javascript
async function toggleFullscreen(element) {
  if (!document.fullscreenElement) {
    await element.requestFullscreen();
  } else {
    await document.exitFullscreen();
  }
}

document.addEventListener('fullscreenchange', () => {
  if (document.fullscreenElement) {
    console.log('Entered fullscreen');
  } else {
    console.log('Exited fullscreen');
  }
});
```

## CSS for Games

```css
/* Base setup */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100dvh;
  overflow: hidden;
  background: #000;
}

/* Canvas styling */
canvas {
  display: block;
  touch-action: none; /* CRITICAL for touch games */
  image-rendering: pixelated; /* For pixel art */
  /* image-rendering: auto; /* For smooth graphics */
}

/* UI overlays */
.ui-overlay {
  position: fixed;
  pointer-events: none; /* Let touches pass through */
}

.ui-button {
  pointer-events: auto; /* Re-enable for buttons */
  cursor: pointer;
}
```
