# Lottie and Rive Reference

> Designer-authored animation assets. Lottie for linear vector playback; Rive for stateful, interactive graphics.

---

## When to Use

| Scenario | Tool |
|---|---|
| Designer-authored motion graphics (After Effects export) | Lottie / dotLottie |
| Animated icons, loading indicators, decorative loops | Lottie |
| Interactive graphics that respond to user input with state machines | Rive |
| Stateful characters, game-like UI elements | Rive |
| Simple UI transitions (hover, toggle, reveal) | Neither — use CSS/WAAPI |

---

## Lottie / dotLottie

### Formats
- **Lottie JSON** — standard format exported from After Effects via Bodymovin or similar
- **dotLottie (.lottie)** — compressed container (ZIP/Deflate) wrapping one or more Lottie animations + assets. Smaller files, additional capabilities.

### dotlottie-web (recommended renderer)

```html
<canvas id="lottieCanvas" width="480" height="480"></canvas>
```

```js
import { DotLottie } from "@lottiefiles/dotlottie-web";
// Or for worker-based rendering (offloads to Web Worker):
import { DotLottieWorker } from "@lottiefiles/dotlottie-web";

const player = new DotLottieWorker({
  canvas: document.getElementById("lottieCanvas"),
  src: "/animations/hero.lottie",
  autoplay: true,
  loop: true
});

// Control
player.play();
player.pause();
player.stop();
player.setSpeed(1.5);
player.setDirection(-1); // reverse
player.setSegment([120, 180]); // play frame range
```

Worker-based rendering offloads to a Web Worker, freeing the main thread. Use it when performance matters.

### React integration

```jsx
// @lottiefiles/dotlottie-react
import { DotLottieReact } from "@lottiefiles/dotlottie-react";

function Animation() {
  const [dotLottie, setDotLottie] = useState(null);

  return (
    <DotLottieReact
      src="/animations/hero.lottie"
      loop
      autoplay
      dotLottieRefCallback={setDotLottie}
    />
  );
}
```

### CDN for HTML artifacts

```html
<script src="https://cdn.jsdelivr.net/npm/@lottiefiles/dotlottie-web@latest/dist/dotlottie-player.js"></script>
```

### Reduced motion for Lottie
- Set `autoplay: false`
- Show a static meaningful frame (first frame or a key pose)
- Provide explicit user-triggered playback controls
- Don't rely on animation-only communication of state

### Performance gotchas
- Large or many concurrent Lottie instances cause CPU/GPU pressure and jank
- dotLottie Worker rendering exists specifically to mitigate this
- Keep instances to a minimum in view — lazy-load off-screen animations
- dotlottie-web requires: WebAssembly + Canvas 2D + Fetch (Workers/OffscreenCanvas optional)

---

## Rive

### What it is
Rive is a design+runtime tool for interactive, stateful graphics. The key differentiator vs Lottie: **state machines** that allow graphics to respond to user input, data changes, and application state at runtime — not just play/pause/seek on a timeline.

### When to choose Rive over Lottie
- Animation needs to respond to user input (hover states, click states, drag)
- You need branching logic (state A → state B based on condition)
- Interactive characters or game-like UI elements
- Multi-state toggles, loaders with success/error states

### When to choose Lottie over Rive
- Linear playback from design tools (no interactivity)
- Existing After Effects pipeline
- Simple animated icons/illustrations
- You need the broadest ecosystem compatibility

### Basic Rive integration

```html
<canvas id="rive-canvas" width="400" height="400"></canvas>
```

```js
import { Rive } from "@rive-app/canvas";

const rive = new Rive({
  src: "/animations/character.riv",
  canvas: document.getElementById("rive-canvas"),
  autoplay: true,
  stateMachines: "main",  // name of state machine in Rive file
  onLoad: () => {
    // Access state machine inputs
    const inputs = rive.stateMachineInputs("main");
    const hoverInput = inputs.find(i => i.name === "isHovering");

    document.getElementById("rive-canvas").addEventListener("pointerenter", () => {
      hoverInput.value = true;
    });
    document.getElementById("rive-canvas").addEventListener("pointerleave", () => {
      hoverInput.value = false;
    });
  }
});
```

### Reduced motion for Rive
- Disable autoplay; show a static default state
- State machine inputs can still function (interactive states change without animation transitions)
- Provide equivalent information through non-motion cues

---

## Hybrid Reality: Lottie + Code Animation

Production sites commonly use multiple animation approaches together. A Codrops case study ("Flim") shows the pattern:

- **Lottie** for "baked" designer-authored animations (complex motion graphics)
- **GSAP** for UI choreography (page transitions, scroll-driven sequences)
- **Physics engine** for interaction (drag, throw, collision)

Don't force one tool to do everything. Match the tool to the motion type.
