<!-- Deep reference: anti-patterns. Not auto-loaded. -->
<!-- Access via: grep -A N "SECTION_HEADER" references/deep/anti-patterns.md -->
# Anti-Patterns & Dos/Don'ts


---

## AI-Slop Indicators

### 1. Three Identical Cards in a Centered Row

**Why It's Bad:**
- Creates a predictable, template-like appearance instantly recognizable as AI-generated
- Lacks visual hierarchy and rhythm
- Treats all content as equally important (which is rarely true)
- The symmetry feels static and lifeless
- Every SaaS landing page uses this exact pattern

**The Problem in Code:**
```jsx
// ❌ ANTI-PATTERN: Generic three-card layout
<div className="grid grid-cols-3 gap-8 max-w-6xl mx-auto">
  <div className="bg-white p-6 rounded-xl shadow-md">
    <Icon />
    <h3>Feature 1</h3>
    <p>Description</p>
  </div>
  <div className="bg-white p-6 rounded-xl shadow-md">
    <Icon />
    <h3>Feature 2</h3>
    <p>Description</p>
  </div>
  <div className="bg-white p-6 rounded-xl shadow-md">
    <Icon />
    <h3>Feature 3</h3>
    <p>Description</p>
  </div>
</div>
```

**Better Alternative: Asymmetric Bento Grid**

Bento grids became a major trend in 2024 because they break the monotony of uniform cards while maintaining organization.

```jsx
// ✅ BETTER: Bento grid with varied sizing and hierarchy
<div className="grid grid-cols-12 grid-rows-3 gap-4 max-w-7xl mx-auto">
  {/* Hero feature - takes up more space */}
  <div className="col-span-7 row-span-2 bg-gradient-to-br from-blue-50 to-indigo-100 p-8 rounded-3xl">
    <div className="flex flex-col h-full justify-between">
      <div>
        <h3 className="text-3xl font-bold mb-4">Primary Feature</h3>
        <p className="text-lg text-gray-700">
          This gets the most attention with larger size and prominent placement.
        </p>
      </div>
      <img src="/feature-demo.png" alt="Feature demo" className="mt-6 rounded-lg" />
    </div>
  </div>

  {/* Secondary features - varied sizes */}
  <div className="col-span-5 row-span-1 bg-white p-6 rounded-2xl border border-gray-200">
    <h4 className="text-xl font-semibold mb-2">Feature Two</h4>
    <p className="text-gray-600">Shorter, supporting content.</p>
  </div>

  <div className="col-span-5 row-span-2 bg-gradient-to-br from-purple-50 to-pink-50 p-6 rounded-2xl">
    <h4 className="text-xl font-semibold mb-3">Feature Three</h4>
    <p className="text-gray-600 mb-4">Vertical card with different aspect ratio.</p>
    <div className="space-y-2">
      <div className="flex items-center gap-2">
        <CheckIcon className="w-5 h-5 text-purple-600" />
        <span>Benefit one</span>
      </div>
      <div className="flex items-center gap-2">
        <CheckIcon className="w-5 h-5 text-purple-600" />
        <span>Benefit two</span>
      </div>
    </div>
  </div>

  {/* Accent features */}
  <div className="col-span-4 row-span-1 bg-amber-50 p-4 rounded-xl">
    <h5 className="font-semibold">Quick Stat</h5>
    <p className="text-2xl font-bold text-amber-600">10x faster</p>
  </div>

  <div className="col-span-3 row-span-1 bg-green-50 p-4 rounded-xl text-center">
    <div className="text-4xl mb-2">⚡</div>
    <p className="text-sm font-medium">Lightning Fast</p>
  </div>
</div>
```

**Real-World Examples:**
- **Apple** (apple.com) - Product pages use asymmetric grids with varying content sizes
- **Linear** (linear.app) - Hero section uses a sophisticated bento layout
- **Notion** (notion.so) - Features page breaks the three-card mold with dynamic sizing

**Key Principles:**
1. Create visual hierarchy through size variation
2. Use 12-column grid for flexibility
3. Let important content breathe with more space
4. Mix aspect ratios (wide, tall, square)
5. Use background colors/gradients to create zones

---

### 2. Purple/Violet Gradients on White Backgrounds

**Why It's Bad:**
- Directly traces back to Tailwind's default `bg-indigo-500` in component examples
- Became so overused that "AI purple" is now a documented phenomenon
- Signals zero design thinking or brand consideration
- Creates instant "template" recognition

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: Default purple gradient
<button className="bg-gradient-to-r from-purple-500 to-indigo-600 text-white px-6 py-3 rounded-lg">
  Get Started
</button>

<div className="bg-gradient-to-br from-purple-100 to-indigo-100 p-12 rounded-2xl">
  <h2>Hero Section</h2>
</div>
```

**Better Alternative: Context-Specific Color Systems**

Choose colors based on your brand, industry, and emotional intent—not defaults.

```jsx
// ✅ BETTER: Industry-appropriate color palette

// Example 1: Financial/Trust (Blues & Greens)
const FinancialTheme = () => (
  <button className="bg-gradient-to-r from-emerald-600 to-teal-600 text-white px-6 py-3 rounded-lg
    hover:from-emerald-700 hover:to-teal-700 transition-all duration-200">
    Open Account
  </button>
);

// Example 2: Creative/Bold (Warm Sunset)
const CreativeTheme = () => (
  <div className="bg-gradient-to-br from-orange-500 via-red-500 to-pink-600 p-12 rounded-2xl text-white">
    <h2 className="text-4xl font-bold">Unleash Your Creativity</h2>
  </div>
);

// Example 3: Health/Wellness (Soft Natural Tones)
const WellnessTheme = () => (
  <div className="bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 p-12 rounded-3xl
    border border-green-100">
    <h2 className="text-3xl font-semibold text-green-900">Your Health Journey</h2>
  </div>
);

// Example 4: Tech/Modern (High Contrast Monochrome with Accent)
const TechTheme = () => (
  <div className="bg-gradient-to-br from-gray-900 to-gray-800 p-12 rounded-2xl
    border border-gray-700 relative overflow-hidden">
    {/* Accent glow */}
    <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/20 blur-3xl rounded-full" />
    <h2 className="text-3xl font-bold text-white relative z-10">Next-Gen Platform</h2>
  </div>
);
```

**Strategic Color Selection Framework:**

```jsx
// Create a semantic color system
const colorSystem = {
  // Base: Brand identity colors
  brand: {
    primary: 'from-[#FF6B35] to-[#F7931E]', // Your actual brand colors
    secondary: 'from-[#004E89] to-[#1A659E]',
  },

  // Contextual: Use colors that match intent
  states: {
    success: 'from-green-500 to-emerald-600',
    warning: 'from-amber-500 to-orange-600',
    error: 'from-red-500 to-rose-600',
    info: 'from-blue-500 to-cyan-600',
  },

  // Emotional: Choose based on desired feeling
  mood: {
    energetic: 'from-orange-500 via-red-500 to-pink-600',
    calm: 'from-blue-400 to-cyan-300',
    professional: 'from-slate-700 to-gray-800',
    playful: 'from-yellow-400 via-pink-400 to-purple-500',
  }
};

// Usage with CSS variables for easy theming
const ThemedButton = ({ variant = 'primary' }) => (
  <button
    className={`bg-gradient-to-r ${colorSystem.brand[variant]}
      text-white px-6 py-3 rounded-lg
      shadow-lg shadow-${variant}-500/30
      hover:shadow-xl hover:shadow-${variant}-500/40
      transition-all duration-300`}>
    Call to Action
  </button>
);
```

**2024 Color Trends (Beyond Purple):**
- **Burnt Orange + Olive Green** - Retro 70s warmth
- **Deep Navy + Coral** - Modern nautical
- **Charcoal + Lime** - Tech-forward
- **Rust + Sand** - Desert minimalism
- **Forest Green + Gold** - Luxury organic

---

### 3. Inter, Roboto, or System Fonts as the Only Typeface

**Why It's Bad:**
- These are "safe" defaults that appear in thousands of tutorials
- Zero personality or brand voice
- Signals no typographic thinking
- Makes your site blend into the background

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: Default font with no character
<style jsx>{`
  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }

  h1, h2, h3 {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
  }
`}</style>
```

**Better Alternative: Strategic Font Pairing**

High-contrast pairings create visual interest and hierarchy.

```jsx
// ✅ BETTER: Display + Body pairing with personality

// Example 1: Editorial/Content-Heavy Site
const EditorialFonts = () => (
  <>
    <style jsx>{`
      @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Sans+3:wght@300;400;600&display=swap');

      h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        font-weight: 900;
        letter-spacing: -0.02em;
      }

      body, p {
        font-family: 'Source Sans 3', sans-serif;
        font-weight: 400;
        line-height: 1.7;
      }
    `}</style>

    <h1 className="text-6xl mb-4">Elegant Headlines</h1>
    <p className="text-lg text-gray-700">Clean, readable body text that doesn't compete.</p>
  </>
);

// Example 2: Tech/Startup
const TechFonts = () => (
  <>
    <style jsx>{`
      @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&family=JetBrains+Mono:wght@400;500&display=swap');

      h1, h2 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        letter-spacing: -0.03em;
      }

      code, pre, .monospace {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 500;
      }
    `}</style>

    <h1 className="text-5xl mb-6">Build the Future</h1>
    <code className="monospace text-sm">npm install next-gen-tech</code>
  </>
);

// Example 3: Bold/Modern
const ModernFonts = () => (
  <>
    <style jsx>{`
      @import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Work+Sans:wght@300;400;600&display=swap');

      h1, h2, h3 {
        font-family: 'Archivo Black', sans-serif;
        text-transform: uppercase;
        letter-spacing: 0.02em;
      }

      body {
        font-family: 'Work Sans', sans-serif;
        font-weight: 400;
      }
    `}</style>

    <h1 className="text-7xl tracking-tight">IMPACT</h1>
    <p className="text-base font-light">Supporting text with light weight for contrast.</p>
  </>
);

// Example 4: Luxury/Premium
const LuxuryFonts = () => (
  <>
    <style jsx>{`
      @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;600&family=Montserrat:wght@400;500&display=swap');

      h1, h2 {
        font-family: 'Cormorant Garamond', serif;
        font-weight: 600;
        font-size: clamp(2rem, 5vw, 4rem);
      }

      body {
        font-family: 'Montserrat', sans-serif;
        font-weight: 400;
        letter-spacing: 0.03em;
      }
    `}</style>

    <h1 className="text-6xl italic">Timeless Elegance</h1>
    <p className="text-sm uppercase tracking-widest">Refined Details</p>
  </>
);
```

**Font Pairing Principles:**

```jsx
// Contrast is key - Mix these dimensions:
const typographySystem = {
  contrast: {
    // 1. Serif + Sans-Serif
    editorial: {
      heading: 'font-serif',  // Playfair, Crimson, Lora
      body: 'font-sans',      // Source Sans, Work Sans
    },

    // 2. Display + Mono
    technical: {
      heading: 'font-display', // Space Grotesk, Clash Display
      code: 'font-mono',       // JetBrains Mono, Fira Code
    },

    // 3. Weight Contrast (same family)
    minimal: {
      heading: 'font-sans font-black',  // 900 weight
      body: 'font-sans font-light',     // 300 weight
    },
  },

  // Use extreme weights, not middle ground
  weights: {
    ultraLight: 'font-extralight', // 200
    light: 'font-light',           // 300
    bold: 'font-bold',             // 700
    black: 'font-black',           // 900
    // Avoid: font-normal (400), font-semibold (600)
  },

  // Size jumps should be dramatic
  scale: {
    hero: 'text-7xl',      // 4.5rem
    h1: 'text-5xl',        // 3rem
    h2: 'text-3xl',        // 1.875rem
    body: 'text-base',     // 1rem
    small: 'text-sm',      // 0.875rem
    // 3x+ jumps, not 1.5x
  }
};
```

**Real-World Examples:**
- **Stripe** - Uses custom "Stripe Sans" with carefully tuned weights
- **GitHub** - Mona Sans (display) + SF Mono (code)
- **Airbnb** - Cereal (custom, friendly rounded sans-serif)

---

### 4. Centered-Everything Layouts with Uniform Spacing

**Why It's Bad:**
- Creates static, lifeless composition
- No visual flow or reading path
- Everything competes for equal attention
- Feels like a wireframe, not a designed page

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: Everything centered, uniform spacing
<div className="text-center space-y-8 max-w-4xl mx-auto px-4">
  <h1 className="text-4xl font-bold">Headline</h1>
  <p className="text-lg">Description text</p>
  <button>Call to Action</button>

  <div className="grid grid-cols-3 gap-8 mt-8">
    <div className="p-6">Feature 1</div>
    <div className="p-6">Feature 2</div>
    <div className="p-6">Feature 3</div>
  </div>

  <div className="mt-8">
    <h2 className="text-3xl font-bold">Another Section</h2>
    <p className="mt-8">More content</p>
  </div>
</div>
```

**Better Alternative: Rhythm and Varied Spacing**

Create visual rhythm with intentional spacing variation.

```jsx
// ✅ BETTER: Dynamic spacing with rhythm system
const SpacingRhythm = () => {
  // Define a spacing scale with intentional variation
  const rhythm = {
    xs: '0.5rem',   // 8px
    sm: '1rem',     // 16px
    md: '2rem',     // 32px
    lg: '4rem',     // 64px
    xl: '8rem',     // 128px
    '2xl': '12rem', // 192px
  };

  return (
    <div className="max-w-6xl mx-auto px-4">
      {/* Hero - asymmetric, left-aligned */}
      <section className="grid grid-cols-12 gap-8 min-h-screen items-center">
        <div className="col-span-7">
          {/* Tight heading group */}
          <div className="space-y-2">
            <p className="text-sm uppercase tracking-wider text-gray-500">Product</p>
            <h1 className="text-7xl font-bold leading-none">
              Build Something
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-cyan-600">
                Remarkable
              </span>
            </h1>
          </div>

          {/* Larger gap before description */}
          <p className="text-xl text-gray-600 mt-8 max-w-lg">
            Description with breathing room, not crammed against the headline.
          </p>

          {/* Even larger gap before CTA */}
          <div className="flex gap-4 mt-12">
            <button className="px-8 py-4 bg-black text-white rounded-lg">
              Get Started
            </button>
            <button className="px-8 py-4 border-2 border-gray-300 rounded-lg">
              Watch Demo
            </button>
          </div>
        </div>

        <div className="col-span-5">
          <img src="/hero-image.png" alt="Product" className="rounded-2xl" />
        </div>
      </section>

      {/* Generous whitespace between sections */}
      <div className="h-32" />

      {/* Features - varied layout, not centered */}
      <section>
        <div className="max-w-2xl mb-16">
          <h2 className="text-5xl font-bold mb-4">Features that matter</h2>
          <p className="text-xl text-gray-600">
            Left-aligned content creates a natural reading flow.
          </p>
        </div>

        {/* Staggered feature cards */}
        <div className="space-y-24">
          {/* Feature 1 - Image left */}
          <div className="grid grid-cols-2 gap-16 items-center">
            <img src="/feature-1.png" className="rounded-2xl" />
            <div>
              <h3 className="text-3xl font-bold mb-4">Lightning Fast</h3>
              <p className="text-lg text-gray-600 mb-6">
                Detailed explanation with proper spacing.
              </p>
              <ul className="space-y-3">
                <li className="flex items-center gap-3">
                  <CheckIcon className="w-6 h-6 text-green-600" />
                  <span>Benefit one</span>
                </li>
                <li className="flex items-center gap-3">
                  <CheckIcon className="w-6 h-6 text-green-600" />
                  <span>Benefit two</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Feature 2 - Image right (alternating) */}
          <div className="grid grid-cols-2 gap-16 items-center">
            <div>
              <h3 className="text-3xl font-bold mb-4">Secure by Default</h3>
              <p className="text-lg text-gray-600">
                Alternating layout creates visual interest.
              </p>
            </div>
            <img src="/feature-2.png" className="rounded-2xl" />
          </div>
        </div>
      </section>
    </div>
  );
};
```

**Spacing System with Intention:**

```jsx
// Create a spacing scale that encodes meaning
const spacing = {
  // Tight relationships (same thought/group)
  tight: {
    label: 'space-y-1',      // Label + input
    heading: 'space-y-2',    // Heading + subheading
    listItems: 'space-y-2',  // List items
  },

  // Related but distinct
  related: {
    paragraph: 'space-y-4',  // Paragraphs in same section
    features: 'space-y-6',   // Feature items
  },

  // Section separation
  sections: {
    small: 'space-y-12',     // Related sections
    medium: 'space-y-24',    // Different topics
    large: 'space-y-32',     // Major divisions
  },

  // Breathing room
  isolated: {
    cta: 'mt-16',            // Important call-to-action
    hero: 'mb-32',           // After hero before content
  }
};

// Example usage
const WellSpacedLayout = () => (
  <div>
    {/* Tight group */}
    <div className="space-y-1">
      <label className="text-sm font-medium">Email</label>
      <input type="email" className="w-full p-3 border rounded-lg" />
    </div>

    {/* Larger gap to next group */}
    <div className="mt-8 space-y-4">
      <h2 className="text-3xl font-bold">Section Title</h2>
      <p>First paragraph with related content.</p>
      <p>Second paragraph, still related.</p>
    </div>

    {/* Major section break */}
    <div className="mt-24">
      <h2 className="text-3xl font-bold">New Topic</h2>
    </div>
  </div>
);
```

---

### 5. Generic SaaS Template Structure

**Why It's Bad:**
- Hero → Features → Testimonials → CTA is the most overused flow on the internet
- Treats every product as identical
- Ignores unique storytelling opportunities
- Users scroll past it because they've seen it 1000 times

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: Cookie-cutter SaaS template
<main>
  <HeroSection />
  <FeaturesGrid />
  <TestimonialsCarousel />
  <PricingTable />
  <FinalCTA />
</main>
```

**Better Alternative: Narrative-Driven Structure**

Build your page structure around your unique value story.

```jsx
// ✅ BETTER: Problem-Agitate-Solution Structure
const ProblemAgitateSolutionLayout = () => (
  <main>
    {/* 1. Hook with the problem */}
    <section className="min-h-screen flex items-center bg-gray-50">
      <div className="max-w-4xl mx-auto px-4">
        <h1 className="text-6xl font-bold mb-8">
          Managing projects shouldn't feel like a project
        </h1>
        <p className="text-2xl text-gray-600 mb-12">
          You're drowning in Slack messages, lost updates, and context-switching hell.
        </p>
        <video autoPlay muted loop className="rounded-2xl shadow-2xl">
          <source src="/problem-demo.mp4" />
        </video>
      </div>
    </section>

    {/* 2. Agitate - make it hurt */}
    <section className="py-32 bg-white">
      <div className="max-w-6xl mx-auto px-4">
        <h2 className="text-4xl font-bold mb-16 text-center">
          The hidden cost of bad tools
        </h2>

        <div className="grid grid-cols-3 gap-8">
          <StatCard
            number="2.5 hours"
            label="Wasted daily on status updates"
          />
          <StatCard
            number="$10,000"
            label="Lost per project to miscommunication"
          />
          <StatCard
            number="67%"
            label="Of teams feel out of sync"
          />
        </div>
      </div>
    </section>

    {/* 3. Solution - the reveal */}
    <section className="py-32 bg-gradient-to-br from-blue-50 to-cyan-50">
      <div className="max-w-4xl mx-auto px-4 text-center">
        <h2 className="text-5xl font-bold mb-6">
          What if everyone just... knew?
        </h2>
        <p className="text-xl text-gray-600 mb-12">
          Introducing [Product]: The workspace that thinks for you
        </p>
        <img src="/solution-hero.png" className="rounded-2xl shadow-2xl" />
      </div>
    </section>

    {/* 4. How it works - proof */}
    <section className="py-32">
      <FeatureShowcase />
    </section>

    {/* 5. Social proof - but contextual */}
    <section className="py-32 bg-gray-50">
      <div className="max-w-6xl mx-auto px-4">
        <h2 className="text-4xl font-bold mb-4 text-center">
          Loved by teams who ship
        </h2>
        <p className="text-center text-gray-600 mb-16">
          Not just testimonials - real results
        </p>

        <CaseStudyGrid />
      </div>
    </section>

    {/* 6. Final push */}
    <section className="py-32 bg-black text-white">
      <div className="max-w-3xl mx-auto text-center px-4">
        <h2 className="text-5xl font-bold mb-8">
          Stop managing. Start building.
        </h2>
        <button className="px-12 py-6 bg-white text-black text-xl font-semibold rounded-xl">
          Try it free - no card required
        </button>
      </div>
    </section>
  </main>
);
```

**Alternative Narrative Structures:**

```jsx
// Structure 1: Comparison-based
const ComparisonLayout = () => (
  <>
    <HeroSection />
    <BeforeAfterComparison />  {/* Visual side-by-side */}
    <WhyWeBuiltThis />         {/* Founder story */}
    <HowItWorks />
    <Pricing />
  </>
);

// Structure 2: Use-case driven
const UseCaseLayout = () => (
  <>
    <HeroSection />
    <RoleSelector />           {/* Choose your path */}
    <UseCaseDeepDive />        {/* Personalized content */}
    <IntegrationsShowcase />
    <GetStarted />
  </>
);

// Structure 3: Product-led (let them try first)
const ProductLedLayout = () => (
  <>
    <InteractiveDemo />        {/* Try it immediately */}
    <ResultsFromDemo />        {/* "Here's what you just did" */}
    <DeepDiveFeatures />
    <Pricing />
    <FAQ />
  </>
);
```

---

### 6. Cookie-Cutter Pricing Cards

**Why It's Bad:**
- Every pricing page looks identical: three columns, "Popular" badge, checkmark lists
- Doesn't differentiate your offering
- Ignores creative opportunities to show value
- Users gloss over it because the format is exhausted

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: Generic pricing cards
<div className="grid grid-cols-3 gap-8 max-w-6xl mx-auto">
  <div className="border rounded-xl p-8">
    <h3 className="text-2xl font-bold">Starter</h3>
    <div className="text-4xl font-bold my-4">$9<span className="text-lg">/mo</span></div>
    <ul className="space-y-2">
      <li>✓ Feature 1</li>
      <li>✓ Feature 2</li>
      <li>✓ Feature 3</li>
    </ul>
    <button className="w-full mt-6 py-3 border rounded-lg">Get Started</button>
  </div>
  {/* Repeat 2 more times */}
</div>
```

**Better Alternative: Value-Focused Pricing Design**

```jsx
// ✅ BETTER: Pricing that tells a story

const ValueBasedPricing = () => (
  <section className="max-w-7xl mx-auto px-4 py-24">
    {/* 1. Lead with value, not price */}
    <div className="text-center mb-16">
      <h2 className="text-5xl font-bold mb-4">
        Pricing that scales with your success
      </h2>
      <p className="text-xl text-gray-600">
        Pay for what you use, not what you might use
      </p>
    </div>

    {/* 2. Interactive pricing calculator */}
    <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-3xl p-12 mb-16">
      <h3 className="text-3xl font-bold mb-8">Calculate your price</h3>

      <div className="space-y-8">
        <div>
          <label className="text-lg font-medium mb-2 block">
            Team size: <span className="text-blue-600 font-bold">15 people</span>
          </label>
          <input
            type="range"
            min="1"
            max="100"
            className="w-full"
          />
        </div>

        <div>
          <label className="text-lg font-medium mb-2 block">
            Monthly projects: <span className="text-blue-600 font-bold">12</span>
          </label>
          <input
            type="range"
            min="1"
            max="50"
            className="w-full"
          />
        </div>

        <div className="bg-white rounded-2xl p-8 mt-8">
          <div className="flex justify-between items-center">
            <div>
              <p className="text-gray-600">Your estimated monthly cost</p>
              <p className="text-6xl font-bold">$249<span className="text-2xl text-gray-500">/mo</span></p>
            </div>
            <button className="px-8 py-4 bg-black text-white rounded-xl text-lg font-semibold">
              Start Free Trial
            </button>
          </div>

          <div className="mt-8 pt-8 border-t grid grid-cols-3 gap-6">
            <div>
              <p className="text-3xl font-bold">$16.60</p>
              <p className="text-sm text-gray-600">per user/month</p>
            </div>
            <div>
              <p className="text-3xl font-bold">Unlimited</p>
              <p className="text-sm text-gray-600">storage & integrations</p>
            </div>
            <div>
              <p className="text-3xl font-bold">24/7</p>
              <p className="text-sm text-gray-600">priority support</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    {/* 3. Comparison table (NOT cards) */}
    <div className="bg-white rounded-3xl border-2 border-gray-200 overflow-hidden">
      <table className="w-full">
        <thead>
          <tr className="bg-gray-50">
            <th className="text-left p-6 font-semibold">Features</th>
            <th className="text-center p-6">
              <div className="text-lg font-semibold">Starter</div>
              <div className="text-3xl font-bold mt-2">$49</div>
              <div className="text-sm text-gray-600">per month</div>
            </th>
            <th className="text-center p-6 bg-blue-50 relative">
              <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full">
                MOST POPULAR
              </div>
              <div className="text-lg font-semibold">Professional</div>
              <div className="text-3xl font-bold mt-2">$149</div>
              <div className="text-sm text-gray-600">per month</div>
            </th>
            <th className="text-center p-6">
              <div className="text-lg font-semibold">Enterprise</div>
              <div className="text-3xl font-bold mt-2">Custom</div>
              <div className="text-sm text-gray-600">contact us</div>
            </th>
          </tr>
        </thead>
        <tbody>
          <FeatureRow feature="Team members" values={["5", "20", "Unlimited"]} />
          <FeatureRow feature="Projects" values={["10", "100", "Unlimited"]} />
          <FeatureRow feature="Storage" values={["50GB", "500GB", "Unlimited"]} />
          <FeatureRow feature="Integrations" values={["Basic", "All", "Custom"]} />
          <FeatureRow feature="Support" values={["Email", "Priority", "Dedicated"]} />
        </tbody>
      </table>
    </div>

    {/* 4. Social proof integrated */}
    <div className="mt-16 text-center">
      <p className="text-gray-600 mb-4">Trusted by 10,000+ teams</p>
      <div className="flex justify-center gap-12 opacity-60">
        <CompanyLogo name="Google" />
        <CompanyLogo name="Microsoft" />
        <CompanyLogo name="Shopify" />
      </div>
    </div>
  </section>
);

const FeatureRow = ({ feature, values }) => (
  <tr className="border-t">
    <td className="p-4 font-medium">{feature}</td>
    <td className="p-4 text-center">{values[0]}</td>
    <td className="p-4 text-center bg-blue-50/50">{values[1]}</td>
    <td className="p-4 text-center">{values[2]}</td>
  </tr>
);
```

**Alternative Pricing Approaches:**

```jsx
// Option 1: Feature-based toggle
const FeatureBasedPricing = () => (
  <div className="max-w-4xl mx-auto">
    <h2 className="text-4xl font-bold mb-8">Build your perfect plan</h2>

    <div className="space-y-4 mb-8">
      <PricingToggle feature="Advanced Analytics" price="+$29/mo" />
      <PricingToggle feature="API Access" price="+$49/mo" />
      <PricingToggle feature="White Label" price="+$99/mo" />
      <PricingToggle feature="Priority Support" price="+$39/mo" />
    </div>

    <div className="bg-gray-100 rounded-2xl p-8">
      <div className="flex justify-between items-center">
        <div>
          <p className="text-sm text-gray-600">Your monthly total</p>
          <p className="text-5xl font-bold">$167</p>
        </div>
        <button className="px-8 py-4 bg-black text-white rounded-xl">
          Continue
        </button>
      </div>
    </div>
  </div>
);

// Option 2: Usage-based (like Vercel)
const UsageBasedPricing = () => (
  <div className="max-w-5xl mx-auto">
    <h2 className="text-4xl font-bold mb-4">Pay for what you use</h2>
    <p className="text-xl text-gray-600 mb-12">
      Start free, scale as you grow
    </p>

    <div className="grid grid-cols-2 gap-8">
      <div className="border-2 border-gray-200 rounded-2xl p-8">
        <h3 className="text-2xl font-bold mb-4">Hobby</h3>
        <div className="text-5xl font-bold mb-6">$0</div>

        <div className="space-y-4 mb-8">
          <UsageLine metric="100 GB" label="Bandwidth" />
          <UsageLine metric="1,000" label="API Calls" />
          <UsageLine metric="10" label="Team Members" />
        </div>

        <p className="text-sm text-gray-600 mb-4">Then pay per use:</p>
        <ul className="text-sm space-y-2 text-gray-600">
          <li>• $0.10 per extra GB</li>
          <li>• $0.001 per API call</li>
          <li>• $5 per team member</li>
        </ul>
      </div>

      <div className="border-2 border-blue-600 rounded-2xl p-8 relative">
        <div className="absolute -top-3 left-8 bg-blue-600 text-white text-xs font-bold px-3 py-1 rounded-full">
          BEST VALUE
        </div>
        <h3 className="text-2xl font-bold mb-4">Pro</h3>
        <div className="text-5xl font-bold mb-6">$20<span className="text-2xl text-gray-500">/mo</span></div>

        <div className="space-y-4 mb-8">
          <UsageLine metric="1 TB" label="Bandwidth" />
          <UsageLine metric="100,000" label="API Calls" />
          <UsageLine metric="Unlimited" label="Team Members" />
        </div>

        <p className="text-sm text-gray-600 mb-4">Overage rates:</p>
        <ul className="text-sm space-y-2 text-gray-600">
          <li>• $0.05 per extra GB (50% off)</li>
          <li>• $0.0005 per API call (50% off)</li>
        </ul>
      </div>
    </div>
  </div>
);
```

**Real-World Examples:**
- **Linear** - Simple, transparent pricing with clear value metrics
- **Vercel** - Usage-based with visual charts
- **Notion** - Feature-based calculator
- **Figma** - Per-editor pricing with clear team examples

---

### 7. Overuse of rounded-xl on Everything

**Why It's Bad:**
- Applying the same border radius everywhere creates visual monotony
- No hierarchy or intentionality
- Modern design uses varied corner treatments strategically

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: Same radius everywhere
<div className="rounded-xl">
  <img className="rounded-xl" />
  <button className="rounded-xl">Click</button>
  <input className="rounded-xl" />
  <div className="rounded-xl">Card</div>
</div>
```

**Better Alternative: Strategic Border Radius System**

```jsx
// ✅ BETTER: Intentional radius scale

const borderRadius = {
  // Scale based on element size and importance
  none: 'rounded-none',     // 0px - Tables, data grids
  sm: 'rounded-sm',         // 2px - Small buttons, inputs
  base: 'rounded-md',       // 6px - Default buttons, cards
  lg: 'rounded-lg',         // 8px - Feature cards
  xl: 'rounded-xl',         // 12px - Modal dialogs
  '2xl': 'rounded-2xl',     // 16px - Hero sections
  '3xl': 'rounded-3xl',     // 24px - Large marketing blocks
  full: 'rounded-full',     // 9999px - Pills, avatars
};

const StrategicBorderRadius = () => (
  <div className="space-y-8">
    {/* Hero section: Large, soft radius */}
    <section className="bg-gradient-to-br from-blue-50 to-cyan-50 p-16 rounded-3xl">
      <h1 className="text-6xl font-bold">Large container = larger radius</h1>
    </section>

    {/* Feature cards: Medium radius */}
    <div className="grid grid-cols-3 gap-6">
      <div className="bg-white border-2 border-gray-200 p-6 rounded-2xl">
        <h3 className="text-xl font-bold mb-2">Feature Card</h3>
        <p>Medium radius for cards</p>
      </div>
    </div>

    {/* Buttons: Smaller, proportional radius */}
    <div className="flex gap-4">
      <button className="px-6 py-3 bg-black text-white rounded-lg">
        Large Button (rounded-lg)
      </button>
      <button className="px-4 py-2 bg-gray-200 rounded-md">
        Small Button (rounded-md)
      </button>
    </div>

    {/* Form inputs: Subtle radius */}
    <input
      type="text"
      className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg
        focus:border-blue-500 focus:outline-none"
      placeholder="Inputs get lg for consistency"
    />

    {/* Data table: Sharp corners */}
    <table className="w-full border-2 border-gray-200 rounded-none">
      <thead className="bg-gray-50">
        <tr>
          <th className="p-4 text-left">Data tables stay sharp</th>
          <th className="p-4 text-left">Value</th>
        </tr>
      </thead>
      <tbody>
        <tr className="border-t">
          <td className="p-4">No radius needed here</td>
          <td className="p-4">100%</td>
        </tr>
      </tbody>
    </table>

    {/* Avatar: Full circle */}
    <div className="flex items-center gap-4">
      <img src="/avatar.jpg" className="w-12 h-12 rounded-full" />
      <div>
        <p className="font-semibold">User Name</p>
        <span className="inline-block px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full">
          Active
        </span>
      </div>
    </div>
  </div>
);
```

**Mixed Radius Strategy:**

```jsx
// Combine different radius values for visual interest
const MixedRadiusCard = () => (
  <div className="bg-white border-2 border-gray-200 rounded-2xl overflow-hidden">
    {/* Image: Sharp top corners (overflow-hidden handles this) */}
    <img src="/hero.jpg" className="w-full h-48 object-cover" />

    {/* Content: Inherits parent's rounded bottom */}
    <div className="p-6">
      <h3 className="text-2xl font-bold mb-4">Mixed Approach</h3>

      {/* Tags: Full pill shape */}
      <div className="flex gap-2 mb-4">
        <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
          Design
        </span>
        <span className="px-3 py-1 bg-purple-100 text-purple-800 text-sm rounded-full">
          Development
        </span>
      </div>

      {/* Button: Medium radius */}
      <button className="w-full py-3 bg-black text-white rounded-lg">
        Learn More
      </button>
    </div>
  </div>
);
```

**Real-World Examples:**
- **Apple** - Very subtle 4-6px radius on most UI elements, larger on product cards
- **Stripe** - Varies from 4px (buttons) to 12px (cards) to 24px (hero sections)
- **Linear** - Consistent 8px on most elements, larger on modals

---

### 8. Meaningless Decorative Gradients and Blobs

**Why It's Bad:**
- Random blobs and gradients serve no purpose
- Make pages feel busy without adding value
- Distract from actual content
- Scream "I used a template"

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: Random decorative elements
<section className="relative">
  {/* Meaningless blob 1 */}
  <div className="absolute top-0 right-0 w-96 h-96 bg-purple-500/20 blur-3xl rounded-full" />

  {/* Meaningless blob 2 */}
  <div className="absolute bottom-0 left-0 w-96 h-96 bg-blue-500/20 blur-3xl rounded-full" />

  {/* Content lost in the noise */}
  <div className="relative z-10">
    <h1>Content here</h1>
  </div>
</section>
```

**Better Alternative: Purposeful Decorative Elements**

```jsx
// ✅ BETTER: Intentional visual elements that serve a purpose

// 1. Directional emphasis (guides eye to CTA)
const DirectionalGradient = () => (
  <section className="relative overflow-hidden bg-black text-white py-32">
    {/* Gradient that points to the CTA */}
    <div className="absolute inset-0 bg-gradient-to-br from-blue-600/30 via-transparent to-transparent" />
    <div className="absolute bottom-0 right-0 w-[600px] h-[600px]
      bg-gradient-radial from-cyan-500/20 to-transparent
      blur-2xl" />

    <div className="relative z-10 max-w-4xl mx-auto px-4">
      <h1 className="text-7xl font-bold mb-8">
        Ship faster than ever
      </h1>
      <p className="text-2xl text-gray-300 mb-12">
        The gradient naturally leads your eye here →
      </p>
      <button className="px-12 py-6 bg-white text-black text-xl font-semibold rounded-xl">
        Get Started
      </button>
    </div>
  </section>
);

// 2. Content framing (highlights important area)
const ContentFraming = () => (
  <section className="relative py-32">
    {/* Frame the testimonial */}
    <div className="absolute inset-0 flex items-center justify-center">
      <div className="w-[800px] h-[400px] bg-gradient-to-r from-yellow-400/10 via-orange-400/10 to-red-400/10
        blur-3xl" />
    </div>

    <div className="relative z-10 max-w-3xl mx-auto text-center">
      <blockquote className="text-3xl font-serif italic mb-8">
        "This product changed how we work"
      </blockquote>
      <cite className="text-lg text-gray-600">— Real Customer</cite>
    </div>
  </section>
);

// 3. Section separation (marks major transitions)
const SectionSeparator = () => (
  <>
    <section className="py-32 bg-white">
      <h2>Light Section</h2>
    </section>

    {/* Gradient transition zone */}
    <div className="h-48 bg-gradient-to-b from-white via-blue-50 to-blue-100" />

    <section className="py-32 bg-blue-100">
      <h2>Colored Section</h2>
    </section>
  </>
);

// 4. Interactive hover effect (responds to user)
const InteractiveGradient = () => {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  return (
    <div
      className="relative h-screen"
      onMouseMove={(e) => {
        setMousePosition({
          x: (e.clientX / window.innerWidth) * 100,
          y: (e.clientY / window.innerHeight) * 100,
        });
      }}
    >
      {/* Follows cursor */}
      <div
        className="absolute w-[600px] h-[600px] bg-gradient-radial from-blue-500/30 to-transparent blur-3xl
          transition-transform duration-500"
        style={{
          left: `${mousePosition.x}%`,
          top: `${mousePosition.y}%`,
          transform: 'translate(-50%, -50%)',
        }}
      />

      <div className="relative z-10 flex items-center justify-center h-full">
        <h1 className="text-6xl font-bold">Move your cursor</h1>
      </div>
    </div>
  );
};

// 5. Branded accent (reinforces brand colors)
const BrandedAccent = () => (
  <section className="relative bg-gray-900 text-white py-32">
    {/* Subtle brand color glow on edges */}
    <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-blue-500 to-transparent" />
    <div className="absolute bottom-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-blue-500 to-transparent" />

    {/* Corner accents */}
    <div className="absolute top-0 left-0 w-32 h-32 bg-gradient-to-br from-blue-500/20 to-transparent" />
    <div className="absolute bottom-0 right-0 w-32 h-32 bg-gradient-to-tl from-blue-500/20 to-transparent" />

    <div className="relative z-10 max-w-4xl mx-auto px-4">
      <h2 className="text-5xl font-bold">Subtle brand reinforcement</h2>
    </div>
  </section>
);
```

**Principles for Decorative Elements:**
1. **Purpose** - Should guide attention, frame content, or mark transitions
2. **Restraint** - One or two per section maximum
3. **Subtlety** - Low opacity (10-30%)
4. **Coordination** - Match brand colors or contextual meaning

---

### 9. Icons from a Single Set with No Customization

**Why It's Bad:**
- Using Heroicons/Lucide/Feather without any customization is instantly recognizable
- Makes your product look like everyone else's
- Misses opportunity to reinforce brand
- Icons often don't match your specific use case

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: Generic icon set, no customization
import { CheckIcon, XMarkIcon, UserIcon } from '@heroicons/react/24/outline';

<div className="flex items-center gap-2">
  <CheckIcon className="w-6 h-6" />
  <span>Feature included</span>
</div>
```

**Better Alternative: Customized Icon Strategy**

```jsx
// ✅ BETTER: Mixed icon approach with customization

// 1. Custom accent color system
const ThemedIcon = ({ icon: Icon, variant = 'primary' }) => {
  const styles = {
    primary: 'text-blue-600 bg-blue-100',
    success: 'text-green-600 bg-green-100',
    warning: 'text-amber-600 bg-amber-100',
    error: 'text-red-600 bg-red-100',
  };

  return (
    <div className={`${styles[variant]} p-3 rounded-xl inline-flex`}>
      <Icon className="w-6 h-6" />
    </div>
  );
};

// Usage
<ThemedIcon icon={CheckCircleIcon} variant="success" />

// 2. Custom illustrations for key features
const FeatureList = () => (
  <div className="space-y-6">
    <div className="flex items-start gap-4">
      {/* Custom SVG instead of generic icon */}
      <svg className="w-12 h-12 text-blue-600" viewBox="0 0 48 48" fill="none">
        <path d="M24 4L4 14v14c0 12.15 8.41 23.5 20 26 11.59-2.5 20-13.85 20-26V14L24 4z"
          fill="currentColor" opacity="0.2" />
        <path d="M20 25l-4-4 2.83-2.83L20 19.34l8.17-8.17L31 14z"
          fill="currentColor" />
      </svg>

      <div>
        <h3 className="text-xl font-bold mb-2">Bank-Level Security</h3>
        <p className="text-gray-600">
          Custom icon communicates trust better than generic shield
        </p>
      </div>
    </div>
  </div>
);

// 3. Duotone treatment for depth
const DuotoneIcon = ({ icon: Icon }) => (
  <div className="relative inline-block">
    {/* Base layer */}
    <Icon className="w-8 h-8 text-blue-200 absolute" />
    {/* Top layer offset */}
    <Icon className="w-8 h-8 text-blue-600 relative translate-x-0.5 translate-y-0.5" />
  </div>
);

// 4. Animated icons for interactive elements
const AnimatedIcon = ({ icon: Icon, isActive }) => (
  <Icon className={`w-6 h-6 transition-all duration-300 ${
    isActive
      ? 'text-blue-600 scale-110 rotate-12'
      : 'text-gray-400 scale-100'
  }`} />
);

// 5. Mix icon styles strategically
const MixedIconStrategy = () => (
  <div className="space-y-8">
    {/* Use outlined for navigation/UI */}
    <nav className="flex gap-4">
      <HomeIcon className="w-6 h-6" />
      <UserIcon className="w-6 h-6" />
      <CogIcon className="w-6 h-6" />
    </nav>

    {/* Use solid for status/confirmation */}
    <div className="flex items-center gap-2">
      <CheckCircleIcon className="w-5 h-5 text-green-600" />
      <span>Task completed</span>
    </div>

    {/* Use custom illustrations for marketing */}
    <div className="w-64 h-64">
      <CustomIllustration />
    </div>
  </div>
);

// 6. Icon + gradient background for feature blocks
const GradientIconBlock = ({ icon: Icon, title, description }) => (
  <div className="relative group">
    <div className="absolute inset-0 bg-gradient-to-br from-blue-500 to-purple-600
      opacity-10 group-hover:opacity-20 transition-opacity rounded-2xl" />

    <div className="relative p-6">
      <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600
        rounded-xl flex items-center justify-center mb-4">
        <Icon className="w-6 h-6 text-white" />
      </div>

      <h3 className="text-xl font-bold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  </div>
);
```

**Icon Strategy Checklist:**
- [ ] Color icons based on context (not all same color)
- [ ] Add background shapes for important icons
- [ ] Mix solid/outline strategically
- [ ] Consider custom illustrations for key features
- [ ] Animate interactive icons
- [ ] Ensure icons match brand personality (rounded vs sharp)

---

### 10. Uniform shadow-md on All Elevated Elements

**Why It's Bad:**
- One shadow value doesn't convey hierarchy
- Everything appears at the same "elevation"
- Doesn't guide user attention
- Ignores the subtle depth cues users expect

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: Same shadow everywhere
<div className="shadow-md">Card</div>
<button className="shadow-md">Button</button>
<div className="shadow-md">Modal</div>
<img className="shadow-md" />
```

**Better Alternative: Elevation System**

```jsx
// ✅ BETTER: Strategic elevation scale

const elevation = {
  // Base content (on surface)
  flat: 'shadow-none',

  // Subtle lift (cards, inputs)
  low: 'shadow-sm shadow-gray-200/50',

  // Default elevation (buttons, dropdowns)
  medium: 'shadow-md shadow-gray-300/60',

  // Important elements (modals, popovers)
  high: 'shadow-xl shadow-gray-400/40',

  // Maximum emphasis (toasts, notifications)
  highest: 'shadow-2xl shadow-gray-500/50',
};

const ElevationSystem = () => (
  <div className="space-y-12 p-12 bg-gray-50">
    {/* Level 0: Flat on surface */}
    <div className="bg-white p-6 rounded-lg">
      <p>No shadow - sits flat on the page</p>
    </div>

    {/* Level 1: Subtle lift */}
    <div className="bg-white p-6 rounded-lg shadow-sm shadow-gray-200/50">
      <p>Subtle shadow - content cards</p>
    </div>

    {/* Level 2: Clear elevation */}
    <div className="bg-white p-6 rounded-lg shadow-md shadow-gray-300/60">
      <button className="px-6 py-3 bg-blue-600 text-white rounded-lg">
        Button with medium elevation
      </button>
    </div>

    {/* Level 3: Floating */}
    <div className="bg-white p-6 rounded-xl shadow-xl shadow-gray-400/40">
      <h3 className="text-xl font-bold mb-2">Modal Dialog</h3>
      <p>High elevation for overlays</p>
    </div>

    {/* Level 4: Highest layer */}
    <div className="bg-white p-6 rounded-xl shadow-2xl shadow-gray-500/50
      border-2 border-green-500">
      <p className="font-semibold text-green-800">
        Success toast - maximum elevation
      </p>
    </div>
  </div>
);

// Colored shadows for emphasis
const ColoredShadows = () => (
  <div className="flex gap-8">
    {/* Primary action - blue glow */}
    <button className="px-8 py-4 bg-blue-600 text-white rounded-xl
      shadow-lg shadow-blue-500/50
      hover:shadow-xl hover:shadow-blue-500/60
      transition-all duration-300">
      Primary Action
    </button>

    {/* Danger action - red glow */}
    <button className="px-8 py-4 bg-red-600 text-white rounded-xl
      shadow-lg shadow-red-500/50
      hover:shadow-xl hover:shadow-red-500/60">
      Delete
    </button>

    {/* Success - green glow */}
    <div className="px-6 py-4 bg-green-50 text-green-800 rounded-xl
      shadow-md shadow-green-500/30">
      ✓ Success message
    </div>
  </div>
);

// Interactive elevation (changes on hover)
const InteractiveShadow = () => (
  <div className="grid grid-cols-3 gap-6">
    <div className="bg-white p-6 rounded-xl
      shadow-sm shadow-gray-200/50
      hover:shadow-lg hover:shadow-gray-300/60
      hover:-translate-y-1
      transition-all duration-300 cursor-pointer">
      <h3 className="font-bold mb-2">Hover Me</h3>
      <p className="text-sm text-gray-600">Shadow increases on interaction</p>
    </div>
  </div>
);

// Context-aware shadows (dark mode)
const DarkModeShadows = () => (
  <div className="bg-gray-900 p-12">
    {/* In dark mode, use glows instead of shadows */}
    <div className="bg-gray-800 p-6 rounded-xl
      ring-1 ring-gray-700
      shadow-lg shadow-black/50">
      <p className="text-white">
        Dark mode uses rings + subtle black shadow
      </p>
    </div>

    {/* Accent glow for emphasis */}
    <button className="mt-6 px-6 py-3 bg-blue-600 text-white rounded-lg
      shadow-lg shadow-blue-500/30
      ring-1 ring-blue-400/20">
      Glowing button in dark mode
    </button>
  </div>
);
```

**Material Design 3 Elevation Reference:**

```jsx
// Based on Material Design elevation system
const materialElevation = {
  // Surface level
  level0: 'shadow-none',

  // Raised
  level1: 'shadow-[0_1px_2px_rgba(0,0,0,0.05)]',
  level2: 'shadow-[0_2px_4px_rgba(0,0,0,0.06)]',
  level3: 'shadow-[0_4px_8px_rgba(0,0,0,0.07)]',
  level4: 'shadow-[0_8px_16px_rgba(0,0,0,0.08)]',
  level5: 'shadow-[0_16px_32px_rgba(0,0,0,0.09)]',
};
```

---

---

---

## Accessibility Failures

### 1. Insufficient Color Contrast (WCAG Standards)

**Why It's Bad:**
- Makes content unreadable for users with low vision or color blindness
- Fails WCAG 2.2 Level AA compliance (required for many organizations)
- Gray text on white backgrounds is the most common violation

**WCAG Requirements:**
- **Normal text:** Minimum 4.5:1 contrast ratio
- **Large text (18pt+ or 14pt+ bold):** Minimum 3:1 contrast ratio
- **Level AAA:** 7:1 for normal text, 4.5:1 for large text

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: Common contrast failures
<p className="text-gray-400">
  This has 2.8:1 contrast on white - fails WCAG AA
</p>

<button className="bg-gray-200 text-gray-500">
  Button text barely visible (1.9:1)
</button>

<a href="#" className="text-blue-300">
  Link too light (2.4:1)
</a>
```

**Better Alternative: WCAG-Compliant Colors**

```jsx
// ✅ BETTER: Properly contrasted text

// Tailwind gray scale with contrast ratios on white:
const contrastRatios = {
  'text-gray-300': '2.8:1', // ❌ FAIL
  'text-gray-400': '3.4:1', // ❌ FAIL (barely passes for large text)
  'text-gray-500': '4.7:1', // ✅ PASS AA normal text
  'text-gray-600': '6.2:1', // ✅ PASS AAA normal text
  'text-gray-700': '8.6:1', // ✅ PASS AAA+
  'text-gray-800': '11.4:1', // ✅ PASS AAA++
  'text-gray-900': '15.3:1', // ✅ PASS AAA+++
};

const AccessibleText = () => (
  <div className="bg-white p-8 space-y-4">
    {/* Body text: Use gray-700 or darker */}
    <p className="text-gray-700 text-base">
      Body text with 8.6:1 contrast - easily readable
    </p>

    {/* Secondary text: Minimum gray-600 */}
    <p className="text-gray-600 text-sm">
      Secondary text at 6.2:1 - passes AAA
    </p>

    {/* Links: Ensure sufficient contrast AND underline */}
    <a href="#" className="text-blue-700 underline hover:text-blue-800">
      Link with 7.4:1 contrast (blue-700)
    </a>

    {/* Buttons: High contrast text */}
    <button className="px-6 py-3 bg-blue-600 text-white rounded-lg">
      White on blue-600 = 8.6:1 ✓
    </button>

    {/* Disabled state: Still needs 4.5:1 minimum */}
    <button className="px-6 py-3 bg-gray-300 text-gray-600 rounded-lg" disabled>
      Disabled but still readable (4.7:1)
    </button>
  </div>
);

// Color system with contrast ratios baked in
const ColorSystem = {
  text: {
    primary: 'text-gray-900',     // 15.3:1 - highest contrast
    secondary: 'text-gray-700',   // 8.6:1 - body text
    tertiary: 'text-gray-600',    // 6.2:1 - muted text
    // Never use: gray-400 (3.4:1), gray-300 (2.8:1) for text
  },

  links: {
    default: 'text-blue-700',     // 7.4:1
    hover: 'text-blue-800',       // 9.3:1
    visited: 'text-purple-700',   // 7.1:1
  },

  buttons: {
    primary: 'bg-blue-600 text-white',   // 8.6:1
    secondary: 'bg-gray-700 text-white', // 11.1:1
    danger: 'bg-red-600 text-white',     // 7.9:1
  },

  status: {
    success: 'text-green-700',    // 6.8:1
    warning: 'text-amber-700',    // 6.1:1
    error: 'text-red-700',        // 7.2:1
    info: 'text-blue-700',        // 7.4:1
  },
};

// Testing contrast in code
const contrastCheck = (foreground, background) => {
  // Use a library like 'color-contrast' or build with luminance calculation
  // Return true if passes WCAG AA (4.5:1)
};
```

**Dark Mode Contrast:**

```jsx
// ✅ Dark mode requires different contrast considerations
const DarkModeContrast = () => (
  <div className="bg-gray-900 p-8 space-y-4">
    {/* White at 87% opacity (not 100%) */}
    <p className="text-white/87 text-base">
      Primary text at 87% opacity prevents glare
    </p>

    {/* Secondary at 60% */}
    <p className="text-white/60 text-sm">
      Secondary text at 60% opacity (still passes 7:1)
    </p>

    {/* Links need even more contrast in dark mode */}
    <a href="#" className="text-blue-400 underline">
      Blue-400 on gray-900 = 8.2:1 ✓
    </a>

    {/* Buttons: Test every combination */}
    <button className="px-6 py-3 bg-blue-500 text-white rounded-lg">
      Blue-500 on gray-900 background
    </button>
  </div>
);

// Dark mode color system
const darkModeColors = {
  text: {
    primary: 'text-white/87',     // ~14:1 contrast
    secondary: 'text-white/60',   // ~7:1 contrast
    tertiary: 'text-white/40',    // ~4.5:1 contrast (minimum)
  },

  links: {
    default: 'text-blue-400',     // 8.2:1
    hover: 'text-blue-300',       // 10.4:1
  },

  surfaces: {
    background: 'bg-gray-900',    // #0f172a or #0a0a0a
    elevated: 'bg-gray-800',      // Lighter for elevation
    dialog: 'bg-gray-700',        // Even lighter for modals
  },
};
```

**Tools for Testing:**
- **WebAIM Contrast Checker**: https://webaim.org/resources/contrastchecker/
- **Chrome DevTools**: Built-in contrast checker in color picker
- **Stark Plugin (Figma)**: Design-time contrast validation
- **axe DevTools**: Automated accessibility testing

---

### 2. Missing Focus Indicators

**Why It's Bad:**
- Keyboard users can't tell where they are on the page
- Fails WCAG 2.4.7 (Focus Visible) - Level AA
- Makes forms and navigation unusable for many users

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: No focus indicator or removed outline
<button className="outline-none">Click me</button>

<input type="text" className="focus:outline-none" />

<a href="#" className="no-underline focus:no-underline">Link</a>
```

**Better Alternative: Clear Focus Indicators**

```jsx
// ✅ BETTER: Visible, high-contrast focus states

const AccessibleFocus = () => (
  <div className="space-y-6 p-8">
    {/* Button: Ring-based focus indicator */}
    <button className="px-6 py-3 bg-blue-600 text-white rounded-lg
      focus:outline-none
      focus:ring-4 focus:ring-blue-300
      transition-shadow">
      Button with ring focus
    </button>

    {/* Input: Underline + ring */}
    <input
      type="text"
      placeholder="Email address"
      className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg
        focus:outline-none
        focus:border-blue-600
        focus:ring-4 focus:ring-blue-100
        transition-all"
    />

    {/* Link: Underline + background */}
    <a href="#"
      className="text-blue-700 underline
        focus:outline-none
        focus:bg-blue-50 focus:outline-2 focus:outline-offset-2 focus:outline-blue-600
        px-1 py-0.5 rounded">
      Link with background focus
    </a>

    {/* Card: Border highlight */}
    <div
      tabIndex="0"
      className="p-6 bg-white border-2 border-gray-200 rounded-xl
        focus:outline-none
        focus:border-blue-600
        focus:shadow-lg focus:shadow-blue-100
        transition-all cursor-pointer">
      <h3 className="font-bold">Interactive Card</h3>
      <p className="text-gray-600">Tab to focus this element</p>
    </div>

    {/* Icon button: Circular focus */}
    <button
      aria-label="Settings"
      className="p-3 text-gray-600 rounded-full
        hover:bg-gray-100
        focus:outline-none
        focus:ring-4 focus:ring-blue-300">
      <CogIcon className="w-6 h-6" />
    </button>
  </div>
);

// Skip link for keyboard navigation
const SkipLink = () => (
  <a href="#main-content"
    className="sr-only focus:not-sr-only
      fixed top-4 left-4 z-50
      px-6 py-3 bg-blue-600 text-white rounded-lg
      focus:outline-none focus:ring-4 focus:ring-blue-300">
    Skip to main content
  </a>
);

// Focus-visible (only show focus for keyboard, not mouse)
const FocusVisible = () => (
  <button className="px-6 py-3 bg-blue-600 text-white rounded-lg
    focus:outline-none
    focus-visible:ring-4 focus-visible:ring-blue-300">
    Keyboard focus only (not mouse click)
  </button>
);
```

**Global Focus Styles:**

```jsx
// Add to global CSS for consistent focus across site
const globalFocusStyles = `
  /* Remove default outline */
  *:focus {
    outline: none;
  }

  /* Add consistent focus-visible ring */
  *:focus-visible {
    outline: 2px solid #3b82f6; /* blue-600 */
    outline-offset: 2px;
  }

  /* Button-specific focus */
  button:focus-visible {
    outline: none;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.3); /* blue-600 at 30% */
  }

  /* Input-specific focus */
  input:focus-visible,
  textarea:focus-visible,
  select:focus-visible {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
  }

  /* Link-specific focus */
  a:focus-visible {
    outline: 2px solid #3b82f6;
    outline-offset: 4px;
    border-radius: 2px;
  }
`;
```

**WCAG 2.4.11 (Focus Appearance - Level AAA):**
```jsx
// Level AAA requirements (stricter):
// - Focus indicator must be at least 2px thick
// - Must have 3:1 contrast against adjacent colors
// - Must encompass entire focused element or be visible on all sides

const AAA_Focus = () => (
  <button className="px-6 py-3 bg-blue-600 text-white rounded-lg
    focus:outline-none
    focus-visible:outline-2
    focus-visible:outline-offset-2
    focus-visible:outline-blue-900">
    AAA-compliant focus (2px thick, 3:1 contrast)
  </button>
);
```

---

### 3. No Keyboard Navigation

**Why It's Bad:**
- Users can't operate your site with Tab, Enter, Arrow keys
- Fails WCAG 2.1.1 (Keyboard) - Level A
- Breaks for screen reader users, motor disability users, and power users

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: Click-only interactions
<div onClick={() => setOpen(true)}>
  Click me
</div>

<div className="cursor-pointer" onClick={handleClick}>
  This isn't keyboard accessible
</div>
```

**Better Alternative: Full Keyboard Support**

```jsx
// ✅ BETTER: Keyboard-accessible components

// 1. Use semantic HTML (gets keyboard support for free)
const SemanticHTML = () => (
  <>
    <button onClick={() => setOpen(true)}>
      Keyboard accessible by default
    </button>

    <a href="/page">
      Links are focusable and trigger on Enter
    </a>
  </>
);

// 2. Add keyboard handlers to div-based components
const KeyboardAccessibleDiv = ({ onClick, children }) => {
  const handleKeyDown = (e) => {
    // Trigger on Enter or Space
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      onClick();
    }
  };

  return (
    <div
      role="button"
      tabIndex={0}
      onClick={onClick}
      onKeyDown={handleKeyDown}
      className="cursor-pointer focus:ring-4 focus:ring-blue-300 rounded-lg p-4">
      {children}
    </div>
  );
};

// 3. Custom dropdown with full keyboard support
const AccessibleDropdown = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [focusedIndex, setFocusedIndex] = useState(0);
  const items = ['Option 1', 'Option 2', 'Option 3'];

  const handleKeyDown = (e) => {
    switch (e.key) {
      case 'Enter':
      case ' ':
        e.preventDefault();
        setIsOpen(!isOpen);
        break;
      case 'Escape':
        setIsOpen(false);
        break;
      case 'ArrowDown':
        e.preventDefault();
        setFocusedIndex((prev) => Math.min(prev + 1, items.length - 1));
        break;
      case 'ArrowUp':
        e.preventDefault();
        setFocusedIndex((prev) => Math.max(prev - 1, 0));
        break;
      default:
        break;
    }
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        onKeyDown={handleKeyDown}
        aria-expanded={isOpen}
        aria-haspopup="listbox"
        className="px-4 py-2 border-2 border-gray-300 rounded-lg
          focus:outline-none focus:ring-4 focus:ring-blue-300">
        Select option
      </button>

      {isOpen && (
        <ul
          role="listbox"
          className="absolute mt-2 w-full bg-white border-2 border-gray-200 rounded-lg shadow-lg">
          {items.map((item, index) => (
            <li
              key={item}
              role="option"
              aria-selected={index === focusedIndex}
              className={`px-4 py-2 cursor-pointer
                ${index === focusedIndex ? 'bg-blue-100' : 'hover:bg-gray-100'}`}
              onClick={() => {
                console.log('Selected:', item);
                setIsOpen(false);
              }}>
              {item}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

// 4. Modal with focus trap
const AccessibleModal = ({ isOpen, onClose, children }) => {
  const modalRef = useRef(null);

  useEffect(() => {
    if (!isOpen) return;

    // Focus first focusable element
    const focusableElements = modalRef.current?.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstElement = focusableElements?.[0];
    firstElement?.focus();

    // Trap focus inside modal
    const handleTab = (e) => {
      if (e.key !== 'Tab') return;

      const lastElement = focusableElements[focusableElements.length - 1];

      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          e.preventDefault();
          lastElement.focus();
        }
      } else {
        if (document.activeElement === lastElement) {
          e.preventDefault();
          firstElement.focus();
        }
      }
    };

    document.addEventListener('keydown', handleTab);
    return () => document.removeEventListener('keydown', handleTab);
  }, [isOpen]);

  // Close on Escape
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') onClose();
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      return () => document.removeEventListener('keydown', handleEscape);
    }
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div
        ref={modalRef}
        role="dialog"
        aria-modal="true"
        className="bg-white rounded-xl p-8 max-w-md w-full">
        {children}

        <button
          onClick={onClose}
          className="mt-6 px-6 py-3 bg-gray-200 rounded-lg
            focus:outline-none focus:ring-4 focus:ring-blue-300">
          Close
        </button>
      </div>
    </div>
  );
};
```

**Keyboard Navigation Patterns:**

```jsx
// Common keyboard shortcuts to implement
const keyboardPatterns = {
  navigation: {
    Tab: 'Move forward through focusable elements',
    'Shift + Tab': 'Move backward',
    Enter: 'Activate links and buttons',
    Space: 'Activate buttons, toggle checkboxes',
    Escape: 'Close modals, menus, dialogs',
  },

  menus: {
    ArrowDown: 'Next menu item',
    ArrowUp: 'Previous menu item',
    Home: 'First menu item',
    End: 'Last menu item',
    Enter: 'Select item and close menu',
  },

  tabs: {
    ArrowRight: 'Next tab',
    ArrowLeft: 'Previous tab',
    Home: 'First tab',
    End: 'Last tab',
  },

  dialogs: {
    Escape: 'Close dialog',
    Tab: 'Cycle through elements (trapped)',
  },
};
```

---

### 4. Missing Alt Text and ARIA Labels

**Why It's Bad:**
- Screen readers can't describe images to blind users
- Interactive elements have no accessible names
- Fails WCAG 1.1.1 (Non-text Content) - Level A

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: Missing or poor alt text
<img src="/product.jpg" />
<img src="/logo.png" alt="logo" />
<button><IconTrash /></button>
<div onClick={handleClick}>X</div>
```

**Better Alternative: Descriptive Text**

```jsx
// ✅ BETTER: Proper alt text and ARIA labels

// 1. Informative images: Describe what's shown
<img
  src="/product-iphone.jpg"
  alt="iPhone 15 Pro in titanium blue color showing the Dynamic Island and triple camera system"
/>

// 2. Decorative images: Empty alt (screen reader skips)
<img
  src="/decorative-blob.svg"
  alt=""
  role="presentation"
/>

// 3. Functional images: Describe the action
<button>
  <img
    src="/icon-save.svg"
    alt="Save document"
  />
</button>

// 4. Icon buttons: Use aria-label
<button
  aria-label="Delete item"
  className="p-2 rounded-lg hover:bg-red-100">
  <TrashIcon className="w-5 h-5 text-red-600" />
</button>

// 5. Complex images: Use aria-describedby for long descriptions
<figure>
  <img
    src="/chart-revenue.png"
    alt="Revenue growth chart for Q4 2024"
    aria-describedby="chart-description"
  />
  <figcaption id="chart-description">
    Bar chart showing monthly revenue from October to December 2024.
    October: $50k, November: $75k, December: $120k, demonstrating
    140% growth over the quarter.
  </figcaption>
</figure>

// 6. Form inputs: Associate labels
<div className="space-y-2">
  <label htmlFor="email" className="font-medium">
    Email address
  </label>
  <input
    id="email"
    type="email"
    aria-required="true"
    aria-invalid={hasError}
    aria-describedby={hasError ? 'email-error' : undefined}
    className="w-full px-4 py-3 border rounded-lg"
  />
  {hasError && (
    <p id="email-error" className="text-red-600 text-sm" role="alert">
      Please enter a valid email address
    </p>
  )}
</div>

// 7. Custom controls: Full ARIA support
<div
  role="slider"
  aria-label="Volume"
  aria-valuemin="0"
  aria-valuemax="100"
  aria-valuenow={volume}
  tabIndex={0}
  onKeyDown={handleKeyDown}
  className="relative h-2 bg-gray-200 rounded-full">
  <div
    className="absolute h-full bg-blue-600 rounded-full"
    style={{ width: `${volume}%` }}
  />
</div>

// 8. Status messages: Use role="status" or role="alert"
<div role="status" aria-live="polite" className="text-green-600">
  Changes saved successfully
</div>

<div role="alert" aria-live="assertive" className="text-red-600">
  Error: Connection lost
</div>
```

**ARIA Checklist:**
- [ ] All images have alt text (or alt="" if decorative)
- [ ] Icon-only buttons have aria-label
- [ ] Form inputs have associated `<label>` elements
- [ ] Error messages use aria-describedby and role="alert"
- [ ] Custom controls have appropriate ARIA roles
- [ ] Loading states use aria-busy="true"
- [ ] Hidden content uses aria-hidden="true"

---

### 5. Animations Without Reduced-Motion Support

**Why It's Bad:**
- Causes nausea, vertigo, and migraines for users with vestibular disorders
- Fails WCAG 2.3.3 (Animation from Interactions) - Level AAA
- No respect for user's system preference

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: Always-on animations
<div className="animate-bounce">
  Bouncing forever
</div>

<div className="transition-all duration-500 hover:scale-110 hover:rotate-6">
  Dramatic hover effect
</div>
```

**Better Alternative: Respect prefers-reduced-motion**

```jsx
// ✅ BETTER: Conditional animations

// 1. CSS approach (use @media query)
const reducedMotionCSS = `
  /* Full animation by default */
  .animated-element {
    animation: slide-in 0.5s ease-out;
    transition: all 0.3s ease-in-out;
  }

  /* Disable for users who prefer reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .animated-element {
      animation: none;
      transition: none;
    }

    /* Still allow opacity transitions (less jarring) */
    .animated-element {
      transition: opacity 0.2s ease-in-out;
    }
  }
`;

// 2. Tailwind utilities with motion-safe
const ResponsiveAnimation = () => (
  <>
    {/* Only animates if user allows motion */}
    <div className="motion-safe:animate-bounce">
      Bounces only if motion is safe
    </div>

    <div className="motion-safe:transition-all motion-safe:duration-300
      hover:motion-safe:scale-105">
      Scales on hover (motion-safe)
    </div>

    {/* Or use motion-reduce to turn OFF animations */}
    <div className="animate-spin motion-reduce:animate-none">
      Loading spinner
    </div>
  </>
);

// 3. React Hook to detect preference
const useReducedMotion = () => {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    setPrefersReducedMotion(mediaQuery.matches);

    const handleChange = (e) => setPrefersReducedMotion(e.matches);
    mediaQuery.addEventListener('change', handleChange);

    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  return prefersReducedMotion;
};

// Usage
const ConditionalAnimation = () => {
  const prefersReducedMotion = useReducedMotion();

  return (
    <motion.div
      initial={{ opacity: 0, y: prefersReducedMotion ? 0 : 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: prefersReducedMotion ? 0.01 : 0.5,
        ease: 'easeOut',
      }}>
      Content fades in (with motion) or appears instantly (reduced motion)
    </motion.div>
  );
};

// 4. Framer Motion with reduced motion support
const MotionComponent = () => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{
        duration: 0.5,
        ease: 'easeOut',
      }}
      // Automatically respects prefers-reduced-motion
      variants={{
        // Framer Motion handles this internally
      }}>
      Content
    </motion.div>
  );
};

// 5. Safe animations (always okay even with reduced motion)
const SafeAnimations = () => (
  <div>
    {/* Opacity transitions are generally safe */}
    <div className="opacity-0 hover:opacity-100 transition-opacity duration-200">
      Fade in/out
    </div>

    {/* Color changes are safe */}
    <button className="bg-blue-600 hover:bg-blue-700 transition-colors duration-200">
      Color transition
    </button>

    {/* Avoid: Large movements, rotations, scaling */}
  </div>
);
```

**Motion Guidelines:**
```jsx
// Safe for reduced motion:
const safeTransitions = {
  opacity: 'opacity changes',
  color: 'color transitions',
  small: 'movements < 5px',
};

// Reduce or remove:
const problematicAnimations = {
  parallax: 'Multiple layers moving at different speeds',
  rotation: 'Spinning, tilting elements',
  scale: 'Growing/shrinking dramatically',
  movement: 'Large position changes (> 20px)',
  infinite: 'Any infinite animation',
};

// Implementation
const AdaptiveAnimation = ({ children }) => {
  const shouldAnimate = !useReducedMotion();

  return shouldAnimate ? (
    <motion.div
      initial={{ y: 20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}>
      {children}
    </motion.div>
  ) : (
    <div style={{ opacity: 1 }}>{children}</div>
  );
};
```

---

### 6. Touch Targets Too Small (<44px)

**Why It's Bad:**
- Mobile users can't accurately tap buttons and links
- Especially difficult for users with motor disabilities
- Fails WCAG 2.5.5 (Target Size) - Level AAA
- WCAG 2.5.8 (Target Size Minimum - 24px) - Level AA

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: Tiny tap targets
<button className="px-2 py-1 text-sm">
  12px × 20px button - way too small
</button>

<a href="#" className="text-sm">
  Link with default size (< 44px)
</a>
```

**Better Alternative: Adequate Touch Targets**

```jsx
// ✅ BETTER: Minimum 44×44px touch targets

// Button sizing
const TouchFriendlyButtons = () => (
  <div className="space-y-4">
    {/* Minimum size: 44×44px (WCAG 2.5.5 AAA) */}
    <button className="min-w-[44px] min-h-[44px] px-6 py-3 bg-blue-600 text-white rounded-lg">
      Standard Button
    </button>

    {/* Small visual size, but large tap area */}
    <button className="relative inline-flex items-center justify-center
      text-sm px-4 py-2 bg-gray-200 rounded-lg
      before:content-[''] before:absolute before:inset-[-8px]
      before:cursor-pointer">
      Visual: 32px, Tap area: 48px
    </button>

    {/* Icon button: Pad to 44px minimum */}
    <button
      aria-label="Delete"
      className="w-12 h-12 flex items-center justify-center
        rounded-lg hover:bg-red-100">
      <TrashIcon className="w-5 h-5 text-red-600" />
    </button>
  </div>
);

// Link spacing
const TouchFriendlyLinks = () => (
  <nav className="space-y-4">
    {/* Add padding to increase tap area */}
    <a href="#" className="inline-block py-3 text-blue-700 underline">
      Link with adequate tap height (44px+)
    </a>

    {/* Navigation links: Full 44px height */}
    <ul className="space-y-2">
      <li>
        <a href="#" className="block py-3 px-4 hover:bg-gray-100 rounded-lg">
          Navigation Link
        </a>
      </li>
    </ul>
  </nav>
);

// Form controls
const TouchFriendlyInputs = () => (
  <div className="space-y-4">
    {/* Inputs: Minimum 44px height */}
    <input
      type="text"
      className="w-full h-12 px-4 border-2 border-gray-300 rounded-lg"
      placeholder="Input with 48px height"
    />

    {/* Checkbox: Larger tap target */}
    <label className="flex items-center gap-3 cursor-pointer py-2">
      <input
        type="checkbox"
        className="w-6 h-6 cursor-pointer"
      />
      <span className="text-base">Checkbox option</span>
    </label>

    {/* Radio buttons: Adequate spacing */}
    <div className="space-y-3">
      <label className="flex items-center gap-3 cursor-pointer py-2">
        <input type="radio" name="option" className="w-6 h-6" />
        <span>Option A</span>
      </label>
      <label className="flex items-center gap-3 cursor-pointer py-2">
        <input type="radio" name="option" className="w-6 h-6" />
        <span>Option B</span>
      </label>
    </div>
  </div>
);

// Spacing between targets (WCAG 2.5.8)
const AdequateSpacing = () => (
  <div>
    {/* Bad: Targets too close */}
    <div className="flex gap-1">
      <button className="w-10 h-10">A</button>
      <button className="w-10 h-10">B</button>
    </div>

    {/* Good: 8px+ spacing OR targets ≥ 44px */}
    <div className="flex gap-2">
      <button className="w-12 h-12 bg-gray-200 rounded-lg">A</button>
      <button className="w-12 h-12 bg-gray-200 rounded-lg">B</button>
    </div>
  </div>
);
```

**Touch Target Utilities:**

```jsx
// Tailwind config for touch targets
module.exports = {
  theme: {
    extend: {
      minHeight: {
        'touch': '44px',
        'touch-large': '48px',
      },
      minWidth: {
        'touch': '44px',
        'touch-large': '48px',
      },
    },
  },
};

// Usage
<button className="min-h-touch min-w-touch px-6 bg-blue-600 text-white rounded-lg">
  Touch-friendly button
</button>
```

---

---

---

## Performance Anti-Patterns

### 1. Layout Thrashing (Animating width/height vs transform)

**Why It's Bad:**
- Animating `width`, `height`, `top`, `left` forces expensive reflows
- Browser must recalculate layout for entire page
- Causes janky animations (drops below 60fps)
- Hurts mobile performance dramatically

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: Animating layout properties
<div className="w-0 hover:w-full transition-all duration-300">
  Animating width causes reflow
</div>

<div className="h-0 group-hover:h-auto transition-all">
  Height animation = layout thrashing
</div>

<style jsx>{`
  .sidebar {
    width: 0;
    transition: width 0.3s;
  }

  .sidebar.open {
    width: 300px;
  }
`}</style>
```

**Better Alternative: Transform and Opacity**

```jsx
// ✅ BETTER: Use transform (GPU-accelerated)

// Slide animation: translate instead of left/right
const SlideIn = () => (
  <div className="translate-x-full opacity-0
    animate-slide-in">
    Slides in using transform
  </div>
);

// Tailwind animation config
const animations = `
  @keyframes slide-in {
    from {
      transform: translateX(100%);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }

  .animate-slide-in {
    animation: slide-in 0.3s ease-out forwards;
  }
`;

// Expand/collapse: scale instead of height
const ExpandCollapse = ({ isOpen }) => (
  <div className={`transform origin-top transition-all duration-300 ${
    isOpen
      ? 'scale-y-100 opacity-100'
      : 'scale-y-0 opacity-0 pointer-events-none'
  }`}>
    <div className="p-6">
      Content here - no layout thrashing
    </div>
  </div>
);

// Sidebar: translate instead of width
const Sidebar = ({ isOpen }) => (
  <aside className={`fixed top-0 left-0 h-full w-80 bg-white
    shadow-2xl transform transition-transform duration-300 ${
    isOpen ? 'translate-x-0' : '-translate-x-full'
  }`}>
    <nav className="p-6">
      Navigation links
    </nav>
  </aside>
);

// Modal: scale + opacity instead of display toggle
const Modal = ({ isOpen }) => (
  <div className={`fixed inset-0 flex items-center justify-center
    transition-all duration-200 ${
    isOpen
      ? 'opacity-100 scale-100'
      : 'opacity-0 scale-95 pointer-events-none'
  }`}>
    <div className="bg-white rounded-2xl p-8 shadow-2xl">
      Modal content
    </div>
  </div>
);

// Loading skeleton: opacity instead of visibility
const Skeleton = ({ isLoading }) => (
  <div className={`bg-gray-200 rounded-lg h-24
    transition-opacity duration-300 ${
    isLoading ? 'opacity-100' : 'opacity-0'
  }`}>
    <div className="animate-pulse" />
  </div>
);
```

**Performance Comparison:**

```jsx
// Properties and their performance impact
const cssPerformance = {
  cheap: {
    // GPU-accelerated, no reflow
    transform: 'translateX(), translateY(), scale(), rotate()',
    opacity: '0 to 1',
  },

  expensive: {
    // Triggers layout recalculation
    width: 'Any change',
    height: 'Any change',
    top: 'Position changes',
    left: 'Position changes',
    margin: 'Spacing changes',
    padding: 'Internal spacing',
  },

  moderate: {
    // Triggers repaint but not reflow
    color: 'Text and fill colors',
    backgroundColor: 'Background colors',
    boxShadow: 'Shadow changes',
  },
};

// Best practice: Use will-change for animations
const OptimizedAnimation = () => (
  <div className="will-change-transform transition-transform duration-300
    hover:scale-105">
    Browser pre-optimizes this animation
  </div>
);
```

**Measuring Performance:**

```jsx
// Chrome DevTools: Performance tab → Enable "Paint flashing"
// Green = repaint, Red = reflow (avoid red!)

// React DevTools Profiler
import { Profiler } from 'react';

const ProfiledComponent = () => (
  <Profiler id="Component" onRender={(id, phase, actualDuration) => {
    if (actualDuration > 16) {
      console.warn(`${id} took ${actualDuration}ms (>16ms = janky)`);
    }
  }}>
    <YourComponent />
  </Profiler>
);
```

---

### 2. Unoptimized Font Loading

**Why It's Bad:**
- FOIT (Flash of Invisible Text) - text hidden while font loads
- FOUT (Flash of Unstyled Text) - jarring font swap
- Blocks rendering, hurts LCP (Largest Contentful Paint)

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: Blocking font load
<link
  href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=block"
  rel="stylesheet"
/>

// Or: No font-display strategy
@import url('https://fonts.googleapis.com/css2?family=Roboto');
```

**Better Alternative: font-display Strategy**

```jsx
// ✅ BETTER: Non-blocking font load with fallback

// 1. Use font-display: swap (most common)
<link
  href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap"
  rel="stylesheet"
/>

// Shows fallback immediately, swaps when font loads
// Prevents FOIT, minimal FOUT

// 2. Preload critical fonts
<head>
  {/* Preload for fastest LCP */}
  <link
    rel="preload"
    href="/fonts/inter-var.woff2"
    as="font"
    type="font/woff2"
    crossOrigin="anonymous"
  />

  {/* Self-hosted font with font-display */}
  <style>{`
    @font-face {
      font-family: 'Inter';
      src: url('/fonts/inter-var.woff2') format('woff2');
      font-weight: 100 900;
      font-display: swap;
    }
  `}</style>
</head>

// 3. Optimized Google Fonts loading (Next.js)
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  preload: true,
  // Only load weights you need
  weight: ['400', '600', '700'],
  // Variable font is better (one file, all weights)
  variable: '--font-inter',
});

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="font-sans">{children}</body>
    </html>
  );
}

// 4. font-display strategies compared
const fontDisplayStrategies = {
  swap: {
    // ✅ Best for most sites
    behavior: 'Show fallback immediately, swap when loaded',
    pros: 'No FOIT, fast rendering',
    cons: 'Slight layout shift on swap',
    use: 'Body text, most content',
  },

  optional: {
    // ⚡ Best for performance
    behavior: 'Show fallback, only swap if font loads FAST (<100ms)',
    pros: 'No layout shift if slow',
    cons: 'May never show custom font',
    use: 'Non-critical text, slow connections',
  },

  fallback: {
    behavior: 'Show fallback, 3s swap window',
    pros: 'Balance of swap & performance',
    cons: 'Complex behavior',
    use: 'Specialized cases',
  },

  block: {
    // ❌ Avoid
    behavior: 'Hide text until font loads (3s timeout)',
    pros: 'No FOUT',
    cons: 'FOIT, terrible UX',
    use: 'Never',
  },
};

// 5. Fallback font matching
// Reduce layout shift by matching fallback metrics
const fontStack = `
  font-family: 'Inter', -apple-system, BlinkMacSystemFont,
    'Segoe UI', 'Helvetica Neue', Arial, sans-serif;

  /* Size adjust to match Inter */
  @font-face {
    font-family: 'Inter Fallback';
    src: local('Arial');
    size-adjust: 107%; /* Make Arial match Inter's size */
    ascent-override: 90%;
    descent-override: 22%;
  }
`;

// 6. Subset fonts (only include characters you need)
// https://fonts.google.com/specimen/Inter?subset=latin
<link
  href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap&subset=latin"
  rel="stylesheet"
/>

// Even better: Self-host and use glyphhanger to subset
// glyphhanger https://yoursite.com --subset=*.woff2
```

**Font Loading Performance Checklist:**
- [ ] Use `font-display: swap` or `optional`
- [ ] Preload critical fonts
- [ ] Self-host fonts when possible (avoid Google Fonts redirect)
- [ ] Use variable fonts (fewer files)
- [ ] Subset fonts (only include needed characters)
- [ ] Match fallback font metrics to reduce layout shift

---

### 3. No Lazy Loading for Below-Fold Content

**Why It's Bad:**
- Loads all images immediately, even those not visible
- Wastes bandwidth, especially on mobile
- Slows initial page load
- Hurts LCP and CLS metrics

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: All images load immediately
<img src="/hero-large.jpg" />
<img src="/feature-1.jpg" />
<img src="/feature-2.jpg" />
<img src="/footer-image.jpg" /> {/* Way below fold */}
```

**Better Alternative: Native Lazy Loading**

```jsx
// ✅ BETTER: Lazy load below-fold images

// 1. Native browser lazy loading
const LazyImages = () => (
  <>
    {/* Above fold: Eager load */}
    <img
      src="/hero.jpg"
      alt="Hero image"
      loading="eager"
      fetchPriority="high"
      className="w-full"
    />

    {/* Below fold: Lazy load */}
    <img
      src="/feature-1.jpg"
      alt="Feature one"
      loading="lazy"
      className="w-full"
    />

    <img
      src="/feature-2.jpg"
      alt="Feature two"
      loading="lazy"
      className="w-full"
    />
  </>
);

// 2. Next.js Image component (automatic optimization)
import Image from 'next/image';

const OptimizedImages = () => (
  <>
    {/* Above fold: priority */}
    <Image
      src="/hero.jpg"
      alt="Hero"
      width={1920}
      height={1080}
      priority
      sizes="100vw"
    />

    {/* Below fold: auto lazy load */}
    <Image
      src="/feature.jpg"
      alt="Feature"
      width={800}
      height={600}
      sizes="(max-width: 768px) 100vw, 50vw"
    />
  </>
);

// 3. Lazy load with Intersection Observer (custom solution)
const LazyImage = ({ src, alt, ...props }) => {
  const [imageSrc, setImageSrc] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const imgRef = useRef();

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          setImageSrc(src);
          observer.disconnect();
        }
      },
      { rootMargin: '100px' } // Load 100px before entering viewport
    );

    if (imgRef.current) {
      observer.observe(imgRef.current);
    }

    return () => observer.disconnect();
  }, [src]);

  return (
    <div ref={imgRef} className="relative">
      {/* Placeholder while loading */}
      {!isLoaded && (
        <div className="absolute inset-0 bg-gray-200 animate-pulse" />
      )}

      {imageSrc && (
        <img
          src={imageSrc}
          alt={alt}
          onLoad={() => setIsLoaded(true)}
          className={`transition-opacity duration-300 ${
            isLoaded ? 'opacity-100' : 'opacity-0'
          }`}
          {...props}
        />
      )}
    </div>
  );
};

// 4. Lazy load components (React.lazy)
const HeavyComponent = lazy(() => import('./HeavyComponent'));

const App = () => (
  <Suspense fallback={<Skeleton />}>
    <HeavyComponent />
  </Suspense>
);

// 5. Lazy load on user interaction
const VideoModal = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button onClick={() => setIsOpen(true)}>Watch Video</button>

      {isOpen && (
        <Modal>
          {/* Video only loads when modal opens */}
          <video src="/large-video.mp4" controls autoPlay />
        </Modal>
      )}
    </>
  );
};
```

**Content-Visibility for Performance:**

```jsx
// ✅ CSS content-visibility (Chrome/Edge)

// Tells browser to skip rendering until near viewport
const contentVisibilityStyles = `
  .heavy-section {
    content-visibility: auto;
    contain-intrinsic-size: 0 500px; /* Estimated height */
  }
`;

// Usage
<section className="heavy-section py-24">
  {/* Complex content here */}
  <ExpensiveComponent />
</section>

// React component
const LazySection = ({ children }) => (
  <section
    style={{
      contentVisibility: 'auto',
      containIntrinsicSize: '0 500px',
    }}
    className="py-24">
    {children}
  </section>
);
```

---

### 4. Massive Uncompressed Images

**Why It's Bad:**
- 5MB JPEGs destroy mobile performance
- Wastes user data ($$$ on metered connections)
- Slows page load by 3-10+ seconds
- Horrible LCP scores

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: Huge unoptimized images
<img src="/photo-from-camera.jpg" /> {/* 8MB, 4000×3000px */}
<img src="/hero.png" /> {/* PNG for photo (10MB+) */}
```

**Better Alternative: Optimized Images**

```jsx
// ✅ BETTER: Compressed, sized, modern formats

// 1. Use modern formats (WebP/AVIF)
<picture>
  {/* AVIF: Best compression, newest */}
  <source type="image/avif" srcSet="/hero.avif" />

  {/* WebP: Great compression, wide support */}
  <source type="image/webp" srcSet="/hero.webp" />

  {/* JPEG: Fallback */}
  <img src="/hero.jpg" alt="Hero" />
</picture>

// 2. Responsive images (srcset)
<img
  src="/hero-800w.jpg"
  srcSet="
    /hero-400w.jpg 400w,
    /hero-800w.jpg 800w,
    /hero-1200w.jpg 1200w,
    /hero-1600w.jpg 1600w
  "
  sizes="(max-width: 600px) 100vw, (max-width: 1200px) 80vw, 1200px"
  alt="Hero"
/>

// 3. Next.js automatic optimization
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1920}
  height={1080}
  quality={85} // Balance quality/size
  placeholder="blur" // Shows blurred preview
  blurDataURL="data:image/jpeg;base64,..." // Tiny placeholder
/>

// 4. Cloudinary/ImgIX for dynamic optimization
<img
  src="https://res.cloudinary.com/demo/image/upload/w_800,f_auto,q_auto/sample.jpg"
  alt="Optimized"
/>
// w_800: Resize to 800px
// f_auto: Auto format (WebP/AVIF if supported)
// q_auto: Auto quality

// 5. Image compression targets
const imageOptimization = {
  formats: {
    photos: 'Use AVIF → WebP → JPEG (never PNG)',
    graphics: 'Use WebP → PNG (SVG if possible)',
    icons: 'Always SVG',
  },

  sizes: {
    hero: '<200KB (mobile), <500KB (desktop)',
    thumbnail: '<20KB',
    background: '<100KB (can use lower quality)',
  },

  quality: {
    photos: '75-85% (sweet spot)',
    graphics: '85-95% (preserve sharp edges)',
  },

  dimensions: {
    mobile: 'Max 800px wide',
    desktop: 'Max 2000px wide (retina)',
    never: 'Don\'t serve 4000px+ images',
  },
};

// 6. Background images (CSS)
<div
  className="h-96 bg-cover bg-center"
  style={{
    backgroundImage: `
      image-set(
        url('/hero.avif') type('image/avif'),
        url('/hero.webp') type('image/webp'),
        url('/hero.jpg') type('image/jpeg')
      )
    `,
  }}>
  Content
</div>

// 7. Blur-up technique (progressive loading)
const ProgressiveImage = ({ src, placeholder }) => {
  const [isLoaded, setIsLoaded] = useState(false);

  return (
    <div className="relative">
      {/* Tiny blurred placeholder (5-10KB) */}
      <img
        src={placeholder}
        alt=""
        className={`absolute inset-0 w-full h-full object-cover blur-xl
          transition-opacity duration-500 ${isLoaded ? 'opacity-0' : 'opacity-100'}`}
      />

      {/* Full image */}
      <img
        src={src}
        alt="Content"
        onLoad={() => setIsLoaded(true)}
        className="w-full h-full object-cover"
      />
    </div>
  );
};
```

**Image Optimization Checklist:**
- [ ] Use WebP/AVIF with JPEG fallback
- [ ] Compress images (75-85% quality)
- [ ] Size images correctly (max 2x viewport width)
- [ ] Use responsive images (srcset + sizes)
- [ ] Lazy load below-fold images
- [ ] Use CDN with automatic optimization
- [ ] Never use PNG for photos
- [ ] Provide width/height to prevent CLS

---

## Dark Mode Mistakes

### 1. Simply Inverting All Colors

**Why It's Bad:**
- Colors don't translate 1:1 between modes
- Bright colors on dark backgrounds create glare
- Breaks visual hierarchy
- Photos and brand colors look wrong

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: Naive color inversion
<div className="bg-white dark:bg-black text-black dark:text-white">
  <button className="bg-blue-600 dark:bg-blue-400">
    Button looks wrong in dark mode
  </button>
</div>
```

**Better Alternative: Semantic Color System**

```jsx
// ✅ BETTER: Separate color palettes per mode

const colors = {
  light: {
    bg: {
      primary: '#FFFFFF',
      secondary: '#F9FAFB',
      elevated: '#FFFFFF',
    },
    text: {
      primary: '#111827',   // gray-900
      secondary: '#6B7280', // gray-500
      tertiary: '#9CA3AF',  // gray-400
    },
    border: '#E5E7EB',      // gray-200
    accent: {
      blue: '#3B82F6',      // blue-600
      green: '#10B981',     // green-600
      red: '#EF4444',       // red-600
    },
  },

  dark: {
    bg: {
      primary: '#0A0A0A',     // Not pure black
      secondary: '#1A1A1A',
      elevated: '#262626',    // Lighter = higher
    },
    text: {
      primary: 'rgba(255,255,255,0.87)', // Not 100%
      secondary: 'rgba(255,255,255,0.60)',
      tertiary: 'rgba(255,255,255,0.40)',
    },
    border: 'rgba(255,255,255,0.12)',
    accent: {
      blue: '#60A5FA',        // blue-400 (lighter than light mode)
      green: '#34D399',       // green-400
      red: '#F87171',         // red-400
    },
  },
};

// Tailwind config with semantic tokens
module.exports = {
  theme: {
    extend: {
      colors: {
        bg: {
          primary: 'rgb(var(--color-bg-primary) / <alpha-value>)',
          secondary: 'rgb(var(--color-bg-secondary) / <alpha-value>)',
          elevated: 'rgb(var(--color-bg-elevated) / <alpha-value>)',
        },
        text: {
          primary: 'rgb(var(--color-text-primary) / <alpha-value>)',
          secondary: 'rgb(var(--color-text-secondary) / <alpha-value>)',
          tertiary: 'rgb(var(--color-text-tertiary) / <alpha-value>)',
        },
      },
    },
  },
};

// CSS variables (switch per mode)
:root {
  --color-bg-primary: 255 255 255;
  --color-text-primary: 17 24 39;
  --color-border: 229 231 235;
}

.dark {
  --color-bg-primary: 10 10 10;
  --color-text-primary: 255 255 255 / 0.87;
  --color-border: 255 255 255 / 0.12;
}

// Usage
<div className="bg-bg-primary text-text-primary border border-border">
  Automatically adapts to mode
</div>
```

---

### 2. Pure Black (#000) Backgrounds

**Why It's Bad:**
- Creates too much contrast with white text (eye strain)
- Causes "smearing" and "haloing" on OLED screens
- Makes depth/elevation impossible to show
- No room for shadows

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: Pure black
<div className="dark:bg-black">
  Pure black = harsh contrast
</div>
```

**Better Alternative: Deep Charcoal**

```jsx
// ✅ BETTER: Use dark gray (#0a0a0a to #18181b)

const darkModeBackgrounds = {
  github: '#0D1117',      // GitHub dark
  discord: '#36393F',     // Discord dark
  twitter: '#15202B',     // Twitter dark
  material: '#121212',    // Material Design
  recommended: '#0A0A0A', // Very dark but not pure black
};

// Elevation system for dark mode
const DarkElevation = () => (
  <div className="bg-gray-950 min-h-screen"> {/* #0a0a0a */}
    {/* Base surface */}
    <div className="bg-gray-900 p-6"> {/* #171717 */}
      <p className="text-white/87">Surface 0</p>
    </div>

    {/* Elevated card */}
    <div className="bg-gray-800 p-6 mt-4"> {/* #27272a */}
      <p className="text-white/87">Surface 1 (higher = lighter)</p>
    </div>

    {/* Modal */}
    <div className="bg-gray-700 p-6 mt-4"> {/* #3f3f46 */}
      <p className="text-white/87">Surface 2 (highest)</p>
    </div>
  </div>
);
```

---

### 3. Not Reducing Saturation

**Why It's Bad:**
- Highly saturated colors "vibrate" on dark backgrounds
- Creates eye strain and illegibility
- Colors appear neon/garish

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: Same saturation in both modes
<button className="bg-blue-600 dark:bg-blue-600">
  Blue-600 is too vibrant on dark
</button>
```

**Better Alternative: Desaturate in Dark Mode**

```jsx
// ✅ BETTER: Lighter, less saturated colors

const adaptiveColors = {
  light: {
    blue: '#2563EB',   // blue-600 (saturated)
    green: '#16A34A',  // green-600
    red: '#DC2626',    // red-600
  },

  dark: {
    blue: '#60A5FA',   // blue-400 (less saturated, lighter)
    green: '#4ADE80',  // green-400
    red: '#F87171',    // red-400
  },
};

// Implementation
<button className="bg-blue-600 dark:bg-blue-400 text-white">
  Properly adapted button
</button>
```

---

### 4. Same Shadow Strategy

**Why It's Bad:**
- Shadows are invisible on dark backgrounds
- Can't show elevation properly

**The Problem:**
```jsx
// ❌ ANTI-PATTERN: Black shadow in dark mode
<div className="shadow-lg dark:shadow-lg">
  Shadow doesn't work
</div>
```

**Better Alternative: Rings and Glows**

```jsx
// ✅ BETTER: Use rings, borders, or glows in dark mode

<div className="
  shadow-lg
  dark:shadow-none
  dark:ring-1 dark:ring-white/10
  dark:shadow-2xl dark:shadow-black/50">
  Visible elevation in both modes
</div>

// Button glow in dark mode
<button className="
  bg-blue-600 text-white
  shadow-md shadow-blue-500/20
  dark:shadow-lg dark:shadow-blue-400/30">
  Glowing button
</button>
```

---

## Final Checklist: Avoiding Anti-Patterns

### AI-Slop Prevention
- [ ] No uniform three-card layouts
- [ ] Custom color palette (not purple gradients)
- [ ] Font pairing with personality
- [ ] Varied spacing rhythm
- [ ] Custom layout structure
- [ ] Distinctive pricing design
- [ ] Mixed border radius values
- [ ] Purposeful decorative elements
- [ ] Customized icon treatment
- [ ] Varied elevation system

### Accessibility
- [ ] 4.5:1 contrast for text
- [ ] Visible focus indicators
- [ ] Full keyboard navigation
- [ ] Alt text on images
- [ ] ARIA labels on controls
- [ ] Reduced motion support
- [ ] 44×44px touch targets

### Performance
- [ ] Transform/opacity animations (not width/height)
- [ ] font-display: swap
- [ ] Lazy loading below fold
- [ ] Compressed, modern image formats
- [ ] content-visibility for long pages

### Dark Mode
- [ ] Separate color palettes
- [ ] #0a0a0a, not #000000
- [ ] Desaturated accent colors
- [ ] Rings/glows instead of shadows
- [ ] White at 87% opacity
- [ ] Test contrast separately

---

