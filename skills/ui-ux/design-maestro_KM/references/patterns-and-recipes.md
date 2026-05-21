# UI Patterns & Data Viz Recipes

> Compressed pattern index. Each entry gives decision guidance. Run the grep command for full implementation code.

## 1. Hero Sections

| Pattern | When to Use | Key Technique |
|---|---|---|
| Editorial (text-focused) | Content-first sites, blogs | Large display font, tight leading, generous whitespace |
| Split-Screen | Product + description side by side | 7/5 or 5/7 column split (never 6/6) |
| Video Background | Immersive landing pages | `object-fit: cover`, muted autoplay, dark overlay for text contrast |
| Asymmetric/Bento Grid | Portfolio, creative | CSS Grid with `grid-template-areas`, varied cell sizes |
| Parallax | Storytelling, scroll-heavy | `transform: translateZ()` with perspective parent, or CSS scroll-driven |

**Anti-slop:** Avoid centered-everything. Left-align body text. Vary element sizes. Use a real image, not a gradient blob.

⤷ `grep -A 60 "#### 1.1 Editorial Hero" references/deep/ui-patterns.md`
⤷ `grep -A 60 "#### 1.4 Asymmetric" references/deep/ui-patterns.md`

## 2. Navigation

| Pattern | When to Use | Key Technique |
|---|---|---|
| Command Palette (⌘K) | Power-user apps, dashboards | cmdk library, fuzzy search, keyboard-first |
| Mega Menu | E-commerce, content-heavy | Grid layout in dropdown, group by category, images optional |
| Sidebar (App Shell) | SaaS, dashboards, tools | Collapsible, icon-only mode, `sticky` positioning |
| Mobile Drawer/Sheet | Any mobile nav | Bottom sheet (not hamburger top-left), spring animation |
| Sticky Header | Most sites | `backdrop-filter: blur()` + reduced height on scroll |

⤷ `grep -A 120 "#### 2.1 Command Palette" references/deep/ui-patterns.md`
⤷ `grep -A 80 "#### 2.4 Mobile Navigation" references/deep/ui-patterns.md`

## 3. Card Layouts

| Pattern | When to Use | Key Technique |
|---|---|---|
| Bento Grid | Feature showcase, portfolio | CSS Grid, mixed `col-span`/`row-span`, featured item larger |
| Masonry | Image galleries, Pinterest-style | CSS `columns` or `masonry` (experimental), JS fallback |
| Glass Card | Over images/gradients | `backdrop-filter: blur(16px)`, border `white/10`, subtle shadow |
| Horizontal Scroll | Mobile-first content, carousels | `scroll-snap-type: x mandatory`, `overscroll-behavior: contain` |
| Skeleton Loading Card | Any card that loads async | Shimmer gradient animation on placeholder shapes |

**Anti-slop:** Never three identical cards in a row. Vary sizes. Feature one card. Use bento grid.

⤷ `grep -A 100 "#### 3.1 Bento Grid" references/deep/ui-patterns.md`

## 4. Dashboard Layouts

| Pattern | When to Use | Key Technique |
|---|---|---|
| Sidebar + Main | Most SaaS dashboards | Collapsible sidebar, CSS Grid `grid-template-columns: auto 1fr` |
| Dense Data | Analytics, monitoring | Compact spacing, small text, high information density |
| Settings Page | User preferences, admin | Grouped sections with anchored sidebar nav |

⤷ `grep -A 120 "#### 4.1 Sidebar" references/deep/ui-patterns.md`

## 5. Data Display

| Pattern | When to Use | Key Technique |
|---|---|---|
| Responsive Table → Cards | Tables that must work on mobile | Table on desktop, stacked cards on mobile via media query |
| TanStack Table | Sortable/filterable/paginated data | Column defs, `useReactTable` hook, virtual rows for 1000+ |
| Timeline | Activity history, changelog | Vertical line with alternating sides or left-aligned dots |
| Kanban Board | Task management, workflows | DnD Kit, column containers, drag handles |

⤷ `grep -A 80 "#### 5.1 Responsive Table" references/deep/ui-patterns.md`
⤷ `grep -A 120 "#### 5.4 Kanban Board" references/deep/ui-patterns.md`

## 6. Form Patterns

| Pattern | When to Use | Key Technique |
|---|---|---|
| Inline Validation | Any form | Validate on blur, show error below field, `aria-describedby` |
| Multi-Step Wizard | Complex flows (signup, checkout) | Step indicator, animated transitions, save progress per step |
| Autocomplete/Combobox | Search, selection from list | Radix Combobox or cmdk, keyboard navigation, debounced search |
| File Upload DnD | Document upload, image upload | `onDragOver`/`onDrop`, preview thumbnails, progress indicator |

⤷ `grep -A 120 "#### 6.2 Multi-Step" references/deep/ui-patterns.md`

## 7. Commerce & Marketing

| Pattern | When to Use | Key Technique |
|---|---|---|
| Pricing Toggle | SaaS pricing pages | Monthly/annual toggle, highlight recommended, vary card sizes |
| Testimonial Grid | Social proof | Mixed sizes, quotes + avatars, subtle borders not cards |
| FAQ Accordion | Support, product pages | `<details>`/`<summary>` or Radix Accordion, smooth height animation |
| CTA Section | Conversion points | Contrasting background, single clear action, urgency without desperation |

**Anti-slop:** Don't use three identical pricing cards. Highlight recommended plan. Add a toggle. Vary visual weight.

⤷ `grep -A 120 "#### 7.1 Pricing Table" references/deep/ui-patterns.md`

## 8. States

| Pattern | When to Use | Key Technique |
|---|---|---|
| Skeleton Screen | Any async content | CSS shimmer gradient animation, match content layout shape |
| Empty State | No data yet, first-use | Illustration + description + single CTA. Never blank. |
| Toast Notifications | Feedback, confirmations | Bottom-right stack, auto-dismiss, swipe-to-dismiss on mobile |
| Progress Indicators | File uploads, multi-step | Linear bar with easing, or circular for compact UI |

⤷ `grep -A 80 "#### 8.1 Skeleton Loading" references/deep/ui-patterns.md`

## 9. Overlay Patterns

| Pattern | When to Use | Key Technique |
|---|---|---|
| Modal/Dialog | Confirmations, focused tasks | Radix Dialog, focus trap, `Escape` to close, backdrop click |
| Sheet/Drawer | Mobile nav, filters, panels | Bottom sheet on mobile, side sheet on desktop, spring animation |
| Popover | Tooltips, menus, pickers | Radix Popover + Floating UI, anchor positioning |
| Context Menu | Right-click actions | Radix ContextMenu, nested submenus, keyboard nav |

⤷ `grep -A 80 "#### 9.1 Modal" references/deep/ui-patterns.md`

---

## 10. Micro-Copy as Design

Words are UI components. Generic copy is the text equivalent of `rounded-xl shadow-md` on everything.

### Button labels

Use action verbs that describe what happens. Never generic labels.

| Bad | Good | Why |
|---|---|---|
| Submit | Save changes | Tells the user what will happen |
| OK | Create project | Specific to the action |
| Yes | Delete account | Matches the question |
| Cancel | Keep editing | States the alternative outcome |

### Empty states

Not just "illustration + CTA." The copy determines whether the user feels invited or blamed.

| Bad | Good |
|---|---|
| No data found | No projects yet — create your first one |
| 0 results | We couldn't find anything matching "xyz." Try broadening your search. |
| Empty | You're all caught up. Nice work. |

### Error messages

Tell the user what happened **AND** what to do:

| Bad | Good |
|---|---|
| Invalid input | Password must be 8+ characters with a number |
| Error 500 | We couldn't reach the server — check your connection and try again |
| Something went wrong | Your file is too large (max 10MB). Try compressing it first. |

### Placeholder text

Show helpful examples, not descriptions:

| Bad | Good |
|---|---|
| Enter search query | Search by name, email, or ID... |
| Type here | What would you like to build? |
| Input value | e.g., acme-corp-2024 |

### Confirmation dialogs

Verb-based buttons that describe the action. Never "OK / Cancel" for destructive operations.

- **Delete:** "Delete project" / "Keep project"
- **Discard:** "Discard changes" / "Continue editing"
- **Leave page:** "Leave without saving" / "Stay on page"

### Loading copy

Context-specific messages that show the system is doing real work:

| Bad | Good |
|---|---|
| Loading... | Analyzing your document... |
| Please wait | Searching 2.4M records... |
| Processing | Generating your report (3 of 5 sections)... |

---

## Data Visualization

### Decision Framework
| Need | Tool | When |
|---|---|---|
| Standard charts (bar, line, area, pie) | Recharts | Most dashboards |
| Custom/complex viz (force graphs, sankey, treemaps) | visx (d3 primitives for React) | Advanced/custom |
| Full control, non-React | D3.js directly | Bespoke visualizations |
| Tiny inline charts | Custom SVG sparklines | Tables, cards, metrics |
| Maps | react-simple-maps | Choropleth, point maps |

### Key Patterns
| Pattern | Grep Target |
|---|---|
| Gradient area chart (Recharts) | `grep -A 60 "### Custom Shape Example" references/deep/data-viz.md` |
| Force graph (visx + d3-force) | `grep -A 100 "### Force Graph Pattern" references/deep/data-viz.md` |
| SVG sparkline component | `grep -A 70 "### Lightweight Sparkline" references/deep/data-viz.md` |
| Animated progress ring | `grep -A 70 "### Animated Progress Ring" references/deep/data-viz.md` |
| Choropleth map | `grep -A 60 "### Choropleth Map" references/deep/data-viz.md` |
| Live streaming chart | `grep -A 50 "### WebSocket + Chart" references/deep/data-viz.md` |
| Dashboard grid layout | `grep -A 50 "### Dashboard Layout Grid" references/deep/data-viz.md` |

### Color in Data Viz
- **Sequential** (single variable): Single hue, light→dark (Blues, Greens)
- **Diverging** (deviation from center): Two hues with neutral midpoint (Red→White→Blue)
- **Categorical** (groups): Distinct hues, max 8-10 (beyond that use shape/pattern)
- **Colorblind-safe:** Avoid red+green. Use blue+orange. IBM Design palette. Add patterns/textures as redundant encoding.

⤷ Full color palettes and implementation: `grep -A 80 "## 8. Color in Data" references/deep/data-viz.md`
