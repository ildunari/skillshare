# Mobile, Audio & Shipping

> Touch input, audio autoplay, accessibility, networking, and platform concerns.

## Mobile Input

### Touch Delay Fix
```css
canvas { touch-action: manipulation; } /* Eliminates 300ms tap delay */
```
For games needing full control: `touch-action: none` and handle all touch via Pointer Events.

### Pointer Events (Unified Input)
```javascript
canvas.addEventListener('pointerdown', e => {
  e.preventDefault();
  canvas.setPointerCapture(e.pointerId); // Track even outside canvas
  // Use e.clientX, e.clientY, e.pointerId for multi-touch
});
```

**Always use Pointer Events** over Touch Events or Mouse Events. They unify mouse, touch, and pen with one API.

### Virtual Controls
- Joystick: Track pointer delta from initial touch point, normalize to unit circle, apply dead zone (15-20%)
- Buttons: Fixed position, ≥44px touch targets, visual feedback on press
- Safe area insets: `env(safe-area-inset-bottom)` for notch devices

⤷ Full mobile input: `grep -A 80 "mobile\|Mobile\|touch\|Touch" references/deep/run-10-shipping-platform.md`

## Audio

### Autoplay Unlock (Mandatory)
Browsers block audio until user gesture. The universal pattern:

```javascript
const audioCtx = new AudioContext();
const unlock = () => {
  if (audioCtx.state === 'suspended') audioCtx.resume();
  document.removeEventListener('pointerdown', unlock);
  document.removeEventListener('keydown', unlock);
};
document.addEventListener('pointerdown', unlock);
document.addEventListener('keydown', unlock);
```

### Sound Effect Playback
```javascript
// Decode once at load
const buffer = await audioCtx.decodeAudioData(arrayBuffer);

// Play many times (zero allocation per play)
function playSound(buffer, volume = 1, pitch = 1) {
  const src = audioCtx.createBufferSource();
  const gain = audioCtx.createGain();
  src.buffer = buffer;
  src.playbackRate.value = pitch;
  gain.gain.value = volume;
  src.connect(gain).connect(audioCtx.destination);
  src.start();
}
```

**Pitch variation:** `pitch = 0.9 + Math.random() * 0.2` prevents repetitive sound fatigue.

### Mute When Hidden
```javascript
document.addEventListener('visibilitychange', () => {
  if (document.hidden) audioCtx.suspend();
  else audioCtx.resume();
});
```

⤷ Full audio patterns: `grep -A 60 "audio\|Audio\|WebAudio" references/deep/run-10-shipping-platform.md`

## Accessibility (WCAG 2.2 AA Baseline)

**Non-negotiable for games/sims:**
- Color-blind friendly palettes (don't use red/green as only differentiator)
- Keyboard navigation for all menus and UI
- `prefers-reduced-motion`: disable screen shake, reduce particles, pause auto-animations
- `prefers-color-scheme`: support dark/light modes
- Sufficient contrast (4.5:1 for text)
- ARIA labels on interactive controls
- Pause functionality accessible via keyboard

```javascript
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (reduceMotion) { shakeEnabled = false; particleCap = 50; }
```

⤷ Full accessibility guide: `grep -A 60 "accessibility\|WCAG\|a11y" references/deep/run-10-shipping-platform.md`

## Performance Profiling

### Frame Budget
- 60fps = 16.67ms per frame
- 30fps = 33.33ms per frame (acceptable mobile target)
- **Budget split:** Physics 4ms, rendering 8ms, AI/other 2ms, overhead 2ms

### Chrome DevTools
1. Performance tab → record gameplay → look for long frames
2. CPU throttle 4× to simulate mobile
3. Memory tab → check for growing heap (leak indicator)

### Common Performance Killers
1. **GC pauses** — Use object pools, SoA typed arrays, avoid `new` in hot loops
2. **Overdraw** — Sort transparent objects front-to-back, cull offscreen
3. **Texture switches** — Use atlas/texture arrays, batch by material
4. **Readback** — `gl.readPixels()` stalls GPU. Avoid in hot path.

⤷ Full profiling guide: `grep -A 80 "performance\|Performance\|profil" references/deep/run-10-shipping-platform.md`

## Networking (Overview)

For multiplayer, the architecture is:
1. **WebTransport** (preferred) or WebSocket for transport
2. **Client prediction:** Apply inputs locally immediately
3. **Server reconciliation:** When server state arrives, replay un-acked inputs
4. **Entity interpolation:** Render other players between received snapshots

**WebTransport advantages over WebSocket:** Unreliable datagrams (no head-of-line blocking), multiple streams, built on QUIC.

This is a deep topic — for serious multiplayer, consider dedicated netcode libraries.

⤷ Networking details: `grep -A 60 "network\|multiplayer\|WebTransport" references/deep/run-10-shipping-platform.md`

## iOS Safari Gotchas

- No native fullscreen API (use `<meta name="apple-mobile-web-app-capable">` for PWA)
- AudioContext starts suspended (always use unlock pattern)
- `devicePixelRatio` can be 3 — cap canvas backing resolution to avoid GPU memory issues
- CSS `vh` doesn't account for Safari's dynamic toolbar — use `dvh` or `window.innerHeight`
