# Themes & Typography

> Visual themes for simulations/games/interactive artifacts + curated font system for all projects.

## Visual Themes

Apply these to simulations, games, generative art, and interactive artifacts.

> **Additional curated themes** are available in the **visual-design-lab** skill. That skill now combines the old design-theme-library packs with screenshot-to-token extraction and broader design-system guidance. The 5 themes below are quick-access favorites for common simulation types. For themed work, load visual-design-lab alongside this file.

### 1. Alchemist's Journal
**Best for:** Reaction-diffusion, slime mold, organic simulations
- **BG:** Cream/Vellum `#FDF6E3` | **Ink:** Charcoal `#2F3337` | **Accents:** Gold `#D4AF37`, Copper `#4B7F52`
- Paper grain overlay via SVG feTurbulence. Serif typography (Garamond/Caslon). Brass-instrument UI (thin gold lines).

### 2. Ethereal Porcelain
**Best for:** Fluid dynamics, smoke/fire, Mandelbulb fractals
- **BG:** Soft Slate `#E6E8EA` | **Main:** Porcelain White `#FFF` | **Highlights:** Kintsugi Gold `#C5A059` | **Shadows:** Cool Grey `#8A9597`
- Subsurface scattering look (milk-in-water). Gold for chaos/high-vorticity. Studio softbox lighting simulation.

### 3. Anthropic Serenity
**Best for:** Strange attractors, particle systems
- **BG:** Warm Beige `#F0EBE3` | **Particles:** Sienna `#C15F3C` → Coral `#E8B49C` | **Deep:** Forest `#3F4E4F`
- Matte particles (no glitter). 0.5x physics speed for majesty. Inter/Söhne typography. Watercolor-wash overlap blending.

### 4. Opalescent Daydream
**Best for:** N-body gravity, orbital mechanics
- **BG:** Ghost White `#F8F9FA` or Lavender `#E6E6FA` | **Elements:** Holographic gradient (Cyan→Magenta→Yellow shifting by velocity)
- Chromatic aberration at edges. Soft bokeh particles. Screen/Add blend mode. Silver `#C0C0C0` UI.

### 5. Gouache & Clay
**Best for:** Voronoi, Delaunay, terrain generation
- **BG:** Terracotta `#E07A5F` or Sage `#81B29A` | **Elements:** Eggshell `#F4F1DE`, Blue-Black `#3D405B` | **Accent:** Ochre `#F2CC8F`
- Zero gloss/matte. Rough edges (hand-cut paper look). Hard directional drop shadows (4px offset, no blur) for 2.5D effect.

## Font System

### Banned Defaults
Never use as sole typeface: Inter, Roboto, Open Sans, Lato, Montserrat, Poppins, Nunito, Raleway, Source Sans Pro.

### Display/Headline Fonts
| Font | Personality | Best For |
|---|---|---|
| Space Grotesk | Geometric, techy, distinctive | Tech/SaaS, developer tools |
| Outfit | Warm, modern, approachable | Lifestyle, startups |
| Plus Jakarta Sans | Refined, professional | Design systems, SaaS |
| Sora | Contemporary, futuristic | Web3, modern tech |
| Bricolage Grotesque | Creative, editorial quirk | Creative agencies, editorial |
| Fraunces | Elegant, variable "wonky" axis | Luxury, e-commerce |
| DM Serif Display | Dramatic, high-contrast | Editorial, professional |
| Playfair Display | Classic sophistication | Editorial, luxury |
| Instrument Sans | Modern, condensed energy | Dashboards, dense UI |
| Syne | Bold, artistic, geometric | Portfolios, creative |

### Body Fonts
| Font | Personality | Best For |
|---|---|---|
| DM Sans | Clean, readable (#1 Typewolf 2026) | Universal, SaaS |
| Figtree | Warm, crisp | Friendly products |
| Manrope | Geometric, distinctive | Tech products |
| Albert Sans | Scandinavian minimalism | Clean, minimal UIs |
| Work Sans | Versatile neutral | Editorial, e-commerce |
| Spectral | Optimized digital serif | Long-form reading |
| Libre Franklin | Reliable, professional | Corporate, serious |

### Monospace Fonts
JetBrains Mono (developer credibility) · IBM Plex Mono (corporate) · Fira Code (ligatures) · Space Mono (quirky) · Geist Mono (modern, Vercel)

### Accent Fonts
Caveat (handwritten) · Instrument Serif (contemporary) · Cormorant (refined) · Newsreader (editorial) · Literata (e-reading)

## 10 Curated Pairings

| # | Display + Body | Aesthetic | Best For |
|---|---|---|---|
| 1 | Space Grotesk + DM Sans | Technical Precision | Tech startups, SaaS |
| 2 | Playfair Display + Work Sans | Editorial Luxury | Magazines, luxury brands |
| 3 | Bricolage Grotesque + Spectral | Sophisticated Editorial | Creative publications |
| 4 | Instrument Sans + Instrument Serif | Design System Harmony | Dashboards, tools |
| 5 | Outfit + Figtree | Warm Approachable | Consumer products, lifestyle |
| 6 | JetBrains Mono + Plus Jakarta Sans | Technical Polish | Developer tools, docs |
| 7 | Fraunces + Albert Sans | Elegant Contemporary | E-commerce, brand sites |
| 8 | DM Serif Display + DM Sans | Professional Editorial | Business, corporate |
| 9 | Sora + Manrope | Neo-Grotesque Minimal | Modern tech, Web3 |
| 10 | Cormorant + Libre Franklin | Classic Refined | Finance, law, luxury |

## Project-Type Quick Picks

| Project Type | Full Stack (Display + Body + Mono) |
|---|---|
| Tech Startup / SaaS | Space Grotesk + DM Sans + JetBrains Mono |
| Editorial / Content | Playfair Display + Work Sans + Caveat (accent) |
| E-Commerce / Lifestyle | Outfit + Figtree + Cormorant (accent) |
| Developer Tools | JetBrains Mono + Plus Jakarta Sans |
| Creative Agency | Syne + Albert Sans + Instrument Serif (accent) |
| Finance / Professional | DM Serif Display + Libre Franklin + IBM Plex Mono |
| Minimal / Scandinavian | Instrument Sans + Albert Sans |

### Font Loading Rules

- Always `font-display: swap` or `optional`.
- Always `font-optical-sizing: auto` — variable fonts with an `opsz` axis automatically adjust stroke contrast at different sizes. One font looks better at both 12px and 72px. No reason to ever disable this.
- Preload critical fonts used above the fold.

⤷ Full font details, weights, Fontshare alternatives: `cat references/deep/font-research.md`
