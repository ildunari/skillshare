## 5. Generative aesthetics & data visualization

### 5.1 Controlled randomness: why some generative art is beautiful and most isn't

Generative art looks beautiful when randomness is controlled by constraints, composition rules, and probability distributions that produce a coherent family of outputs. Tyler Hobbs (creator of *Fidenza*) is unusually explicit about this:

**Long-form generativism:** The algorithm must produce aesthetically high-quality results for *every* possible input seed, without human curation. This requires:
- A "probability landscape" biased toward good composition (defining constraints like "lines never overlap at acute angles")
- **Systemic variation:** Randomize the rules or the flow (e.g., change the underlying vector field driving particles) rather than randomizing individual parameters

**Probability distributions as artistic tools:** Replace uniform randomness with Gaussian, Poisson, or custom distributions to simulate naturalistic variation. This is the key distinction between amateur scripts and professional generative art.

**Theme-design translation:** A "generative theme" needs a bounded parameter space (any seed looks on-brand) and a clear hierarchy (ambient background never competes with content).

**References:**
- Hobbs on randomness: https://www.tylerxhobbs.com/words/randomness-in-the-composition-of-artwork
- Hobbs on probability distributions: https://www.tylerxhobbs.com/words/probability-distributions-for-algorithmic-artists
- Hobbs on color arrangement: https://www.tylerxhobbs.com/words/color-arrangment-in-generative-art

### 5.2 Procedural building blocks for theme-level ambient visuals

#### Noise and fractal noise (fBM)

Noise creates organic variation — grain, clouds, marbling, subtle shimmer. A single layer is too smooth; **fractional Brownian Motion (fBM)** layers multiple octaves of noise, each at higher frequency and lower amplitude, mimicking natural fractal geometry found in clouds and landscapes. In GLSL shaders, fBM is essential for grain and grit textures that prevent digital gradients from looking plastic.

For UI use: keep amplitude low, prefer static or very slow motion, render once to a texture when possible.

Book of Shaders: Noise (https://thebookofshaders.com/11/), fBM (https://thebookofshaders.com/13/)

#### Flow fields

Flow fields use a grid of vectors (often derived from noise) to guide drawing agents. Creates "painterly" strokes or organic curves that feel fluid and intentional. Used extensively by Hobbs and Matt DesLauriers.

Le Random editorial on generative systems: https://www.lerandom.art/editorial/demystifying-generative-systems

#### Domain warping

Feed the output of a noise function back into the input of another. Produces marble-like, swirling distortions — excellent non-distracting background layers for dashboards.

#### Signed Distance Functions (SDFs) for UI

SDFs are mathematical descriptions of shapes (returning distance from any point to the surface). Increasingly used for resolution-independent, GPU-rendered 2D UI elements:

- Infinite resolution (crisp curves at any zoom)
- Algorithmic styling (buttons that morph shape or have liquid borders)
- Soft shadows, rounded corners, and glows calculated per-pixel on the GPU
- `smin` functions (Inigo Quilez) enable "gooey" organic blending between elements

SDFs are a genuinely underexplored technique for theme-level visual identity — currently niche but has significant potential for themes that need to feel "living" or organic.

### 5.3 Theming data visualization: identity vs integrity

Dashboards and charts impose constraints most UI themes ignore:

- **Multiple scale types needed:** Categorical, sequential, diverging — each with different perceptual requirements.
- **Encoding must remain truthful:** Color represents data, not just brand.
- **Legibility beats vibe** in dense contexts — but you can still be beautiful.

#### The chart-art spectrum

Nadieh Bremer and Shirley Wu operate on a spectrum between Data Art (emotional, abstract, custom forms) and Functional Viz (instant readability, standard chart types). For dashboards, the goal is "Elevated Functionality" — standard chart types for clarity, but with generative textures on bars or soft noise-driven glow for active states that align with the visual theme.

#### Rigorous color for data (the HCL imperative)

A common failure: using a brand's RGB palette directly for data encoding, producing "confetti" charts where colors have unequal perceptual weight. Leading tools like Datawrapper emphasize building data palettes in perceptual color spaces:

- **Sequential scales:** Vary primarily in luminance. Interpolate in OKLCH to avoid muddy transitions.
- **Categorical scales:** Distinct hues with similar luminance/chroma so no category is visually dominant by accident.
- **Diverging scales:** Two hue endpoints meeting at a neutral midpoint.

Tools like **Leonardo** (Adobe) and **Chroma.js** generate palettes based on target contrast ratios, ensuring dark mode themes maintain the same perceptual data distinctions as light mode.

**References:**
- Datawrapper on sequential vs diverging: https://www.datawrapper.de/blog/diverging-vs-sequential-color-scales
- Datawrapper on color scale selection: https://www.datawrapper.de/blog/which-color-scale-to-use-in-data-vis
- Datawrapper deep guide: https://www.datawrapper.de/blog/colors-for-data-vis-style-guides
- Observable crafting data colors: https://observablehq.com/blog/crafting-data-colors
- Urban Institute style guide: https://urbaninstitute.github.io/graphics-styleguide/

#### Accessibility beyond color in charts

Never rely on color alone. Pair color with shape, stroke style, patterning, or direct labels. **Textures.js** (for D3) or custom GLSL shaders generate hatching, stippling, and patterns dynamically — "Project A" is blue with 45° hatching, "Project B" is orange with stippling. Always apply the same contrast discipline to axis labels, legends, and tooltips as to UI text.

### 5.4 Practitioners bridging data and art

- Nadieh Bremer (Visual Cinnamon): https://www.visualcinnamon.com/
- Shirley Wu: https://www.shirleywu.studio/
- Data Sketches: https://www.datasketch.es/
- Matt DesLauriers: https://www.mattdesl.com/

### 5.5 Technical implementation for generative themes

| Component | Tool/Technique | Purpose |
|-----------|---------------|---------|
| Noise generation | Simplex / OpenSimplex | Organic textures, better than Perlin (fewer artifacts, lower complexity in higher dimensions) |
| Color palettes | OKLCH / Leonardo / Chroma.js | Perceptually uniform data and theme scales |
| Texture generation | fBM (Fractal Brownian Motion) | Natural, paper-like, or cloud-like detail |
| UI rendering | 2D SDFs (Signed Distance Fields) | Resolution-independent shapes, soft shadows, glows |
| WebGL framework | React Three Fiber (R3F) | Declarative GPU rendering in React |
| Mass rendering | InstancedMesh (Three.js) | 100,000+ items with single draw call for scatterplots |
| Optimization | OffscreenCanvas + Web Workers | Decouple visual rendering from main thread |
| Accessibility | Textures.js / SVG patterns | Dual-encoding data (color + texture) |

**Seeded randomness:** Use a seeded PRNG for all generative elements. A user's dashboard should look consistent every time they log in, building a sense of place rather than changing randomly on every refresh.

