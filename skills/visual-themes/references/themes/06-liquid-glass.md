## 6. Liquid Glass

> Apple iOS 26 translucency — frosted depth, refraction, layered blur.

**Best for:** Modern UI artifacts, settings panels, interactive tools, app mockups, control dashboards, preference editors.

### Color Palette

| Role | Color | Hex | Usage |
|---|---|---|---|
| Background | Ultra Light | `#F5F5F7` | Apple-style light grey. Nearly white. |
| Glass Surface | Frosted White | `rgba(255,255,255,0.72)` | Translucent panels. Always with backdrop-filter. |
| Glass Border | Light Refraction | `rgba(255,255,255,0.5)` | 1px border on glass elements — catches "light." |
| Primary | System Blue | `#007AFF` | Interactive elements, toggles, links. |
| Secondary | System Grey | `#8E8E93` | Labels, secondary text, inactive states. |
| Accent | Subtle Rainbow | gradient | Faint rainbow refraction at glass edges (very subtle). |
| Text | Near Black | `#1D1D1F` | Primary text. Apple system dark. |
| Subtext | Mid Grey | `#86868B` | Secondary text, descriptions. |

### Typography
- **Display:** SF Pro Display (fallback: Plus Jakarta Sans 600) — Apple's system language
- **Body:** SF Pro Text (fallback: DM Sans) — optimized for readability at small sizes
- **Mono:** SF Mono (fallback: Geist Mono) — technical values, code

### Visual Style
- **Backdrop Blur:** Every floating panel uses `backdrop-filter: blur(20px) saturate(1.8)`. This is the defining effect. Glass panels sit over rich backgrounds and blur what's behind them.
- **Layered Depth:** 3+ depth levels: background content → frosted panel → elevated element. Each layer adds more blur and opacity.
- **Refraction Edge:** Glass panels get a 1px top/left border in semi-transparent white (`rgba(255,255,255,0.5)`) to simulate light catching a glass edge.
- **Vibrancy:** `saturate(1.8)` on the backdrop filter makes colors behind glass richer, not washed out. This is key to the iOS look.
- **Shadows:** Soft, diffused. `0 8px 32px rgba(0,0,0,0.08)`. No hard edges.

### Animation Philosophy
- **Easing:** Apple springs — `cubic-bezier(0.2, 0.8, 0.2, 1)` or spring with `stiffness: 300, damping: 30`. Responsive, slightly bouncy.
- **Timing:** Fast. 250-350ms for most transitions. Apple's UI is crisp and immediate.
- **Motion Character:** Fluid, responsive, layered. Elements feel like glass panes sliding over each other.
- **Physics:** Light spring physics. Elements overshoot slightly and settle. Parallax between layers on scroll.

### Signature Animations
1. **Glass Slide** — Panels enter by sliding up from below with backdrop blur fading in simultaneously (blur goes from 0 to 20px over 300ms).
2. **Depth Parallax** — On scroll or mouse move, background and foreground layers shift at different rates (background: 0.3x, foreground: 1x), creating depth.
3. **Toggle Morph** — Boolean toggles slide their thumb with spring physics, and the track color crossfades via `color-mix()`.
4. **Blur Focus** — When a modal/overlay opens, background blur increases from 0 → 20px with content fading to 0.6 opacity. Reverses on close.
5. **Refraction Shimmer** — On hover, glass panel border briefly shows a rainbow shimmer (animated conic-gradient, 600ms, once).

### UI Components
- **Buttons:** Rounded (12px). Primary: system blue fill, white text. Secondary: glass fill (`rgba(255,255,255,0.72)`) with backdrop blur. Hover: darken 5%. Active: `scale(0.97)`.
- **Sliders:** iOS-style. Track is rounded pill (4px tall, grey fill, blue for active portion). Thumb is white circle (28px) with soft shadow.
- **Cards:** Glass panels. `backdrop-filter: blur(20px) saturate(1.8)`. `rgba(255,255,255,0.72)` fill. 1px refraction border. `border-radius: 16px`. Generous padding (20px).
- **Tooltips:** Compact glass pill. Dark variant: `rgba(0,0,0,0.72)` with white text and blur backdrop.
- **Dividers:** 1px `rgba(0,0,0,0.06)`. Or no dividers — spacing alone.

### Dark Mode Variant

Liquid Glass has a full dark mode — not an afterthought, a first-class variant. This IS native iOS dark mode. This is its home.

#### Structural Color Map
| Role | Light (native) | Dark (variant) | Notes |
|---|---|---|---|
| Page background | `#F5F5F7` Ultra Light | `#000000` True Black | Apple uses true black for OLED — pixel-off black saves battery |
| Glass surface | `rgba(255,255,255,0.72)` | `rgba(44,44,46,0.72)` | Dark frosted glass — still translucent, still blurred |
| Glass border | `rgba(255,255,255,0.5)` | `rgba(255,255,255,0.1)` | Refraction edge dimmed — light catches less on dark glass |
| Border (solid) | `rgba(0,0,0,0.06)` dividers | `rgba(255,255,255,0.06)` | Inverted separator opacity |
| Primary text | `#1D1D1F` Near Black | `#F5F5F7` System White | Apple's system colors — not pure white, slightly warm |
| Secondary text | `#86868B` Mid Grey | `#98989D` Lifted Grey | Slightly brighter for dark backgrounds |
| Subtext | `#8E8E93` System Grey | `#8E8E93` (unchanged) | Apple's grey is calibrated for both modes |

#### Accent Shifts
| Element | Light (native) | Dark (variant) | Reason |
|---|---|---|---|
| System Blue | `#007AFF` | `#007AFF` (unchanged) | Apple's blue is constant across modes by design |
| Subtle Rainbow refraction | gradient at 10% | gradient at 6% | Refraction shimmer more subtle on dark glass |
| Interactive glow | none | `0 0 20px rgba(0,122,255,0.1)` | Interactive elements gain faint blue aura on dark |

#### Shadow & Depth Adaptation
- Light: Soft diffused shadows — `0 8px 32px rgba(0,0,0,0.08)` — glass panels float above surface
- Dark: Shadows invisible against black. Replace with luminance-based depth: elevated glass surfaces use slightly lighter `rgba()` fills. Active elements gain subtle blue glow: `0 0 20px rgba(0,122,255,0.08)`. The `backdrop-filter: blur(20px) saturate(1.8)` is MORE dramatic on dark — frosted glass effect truly shines when blurring dark content

#### Texture & Grain Adaptation
- Light: No grain — pure glass clarity
- Dark: No grain. Dark glass is even cleaner. The `saturate(1.8)` on backdrop-filter makes colors behind dark glass richer and more vibrant. Glass transparency reveals more depth on dark backgrounds — the layering system becomes more visible, not less

#### Dark Mode Rules
- True `#000000` black background — Apple uses pixel-off black for OLED power savings. This is one of the rare themes where pure black is correct
- `backdrop-filter: blur(20px) saturate(1.8)` produces its most beautiful results on dark — frosted dark glass is the signature iOS look
- Glass surface alpha stays at `0.72` — same translucency, different fill color. The blur does the heavy lifting
- Text is `#F5F5F7` (Apple system white) — NOT pure `#FFFFFF`. Slightly warm for eye comfort
- "Native iOS dark mode. This is its home"

### Mobile Notes
- **Critical:** `backdrop-filter` is the most expensive CSS property. On older mobile devices, reduce blur to 10px and drop saturate.
- Reduce glass layers to 2 maximum (background + one glass panel).
- Test on Safari — `-webkit-backdrop-filter` prefix still needed.
- This theme is inherently iOS-native, so mobile is the primary target.
