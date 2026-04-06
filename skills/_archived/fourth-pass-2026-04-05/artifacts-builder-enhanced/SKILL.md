---
name: artifacts-builder-enhanced
description: Use when building a complex claude.ai HTML artifact that needs multiple coordinated UI sections, app-like state, routing, or a component stack such as React, Tailwind CSS, or shadcn/ui. Trigger on requests for interactive tools, dashboards, multi-screen experiences, or polished app-style artifacts that must ship as a bundled HTML artifact. Do not use for simple static or single-file HTML/JSX artifacts.
license: Complete terms in LICENSE.txt
---

# Artifacts Builder

To build powerful frontend claude.ai artifacts, follow these steps:
1. Initialize the frontend repo using `scripts/init-artifact.sh`
2. Develop your artifact by editing the generated code
3. Bundle all code into a single HTML file using `scripts/bundle-artifact.sh`
4. Display artifact to user
5. (Optional) Test the artifact

**Stack**: React 18 + TypeScript + Vite + Parcel (bundling) + Tailwind CSS + shadcn/ui

## Design & Style Guidelines

VERY IMPORTANT: To avoid what is often referred to as "AI slop", avoid using excessive centered layouts, purple gradients, uniform rounded corners, and Inter font.

## Responsive Design Guidelines

**CRITICAL**: All artifacts must be fully responsive and work seamlessly across desktop, tablet, and mobile devices.

### Mobile-First Approach

Always design with a mobile-first mindset, then enhance for larger screens:

```tsx
// ✅ Good: Mobile-first responsive design
<div className="w-full px-4 md:w-1/2 md:px-8 lg:w-1/3 lg:px-12">
  <h1 className="text-2xl md:text-3xl lg:text-4xl">Title</h1>
</div>

// ❌ Bad: Fixed widths, no responsive breakpoints
<div className="w-96 px-12">
  <h1 className="text-4xl">Title</h1>
</div>
```

### Tailwind Responsive Utilities

Use Tailwind's responsive breakpoints consistently:
- `sm:` - 640px and up (small tablets)
- `md:` - 768px and up (tablets)
- `lg:` - 1024px and up (laptops)
- `xl:` - 1280px and up (desktops)
- `2xl:` - 1536px and up (large desktops)

### Common Responsive Patterns

**Layout adaptations:**
```tsx
{/* Stack on mobile, grid on desktop */}
<div className="flex flex-col md:flex-row gap-4">
  <aside className="w-full md:w-64">Sidebar</aside>
  <main className="flex-1">Content</main>
</div>

{/* Responsive grid */}
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>
```

**Typography scaling:**
```tsx
<h1 className="text-xl sm:text-2xl md:text-3xl lg:text-4xl">
  Responsive Heading
</h1>
```

**Spacing adjustments:**
```tsx
<div className="p-4 md:p-6 lg:p-8">
  <div className="space-y-4 md:space-y-6">
    {/* Content with responsive spacing */}
  </div>
</div>
```

**Hiding/showing elements:**
```tsx
{/* Hide on mobile, show on desktop */}
<div className="hidden md:block">Desktop only content</div>

{/* Show on mobile, hide on desktop */}
<div className="block md:hidden">Mobile only content</div>
```

### Touch-Friendly Interactions

**Minimum touch target sizes:**
- Buttons: `min-h-11` (44px) for comfortable tapping
- Interactive elements: Adequate spacing with `gap-2` or `gap-3`

```tsx
// ✅ Good: Touch-friendly button
<Button className="min-h-11 px-6 text-base">
  Click Me
</Button>

// ❌ Bad: Too small for touch
<Button className="h-6 px-2 text-xs">
  Click Me
</Button>
```

### Testing Requirements

Before delivering any artifact, verify:
- ✅ Layout works on mobile (320px), tablet (768px), and desktop (1024px+)
- ✅ No horizontal scrolling on narrow screens
- ✅ Text is readable without zooming
- ✅ Interactive elements are touch-friendly (44px minimum)
- ✅ Images and media scale appropriately
- ✅ Navigation is usable on all screen sizes

### shadcn/ui Components

Most shadcn/ui components are responsive by default, but verify:
- Dialogs and modals adapt to small screens
- Tables scroll horizontally on mobile if needed
- Dropdowns and popovers don't extend beyond viewport

**Example: Responsive table**
```tsx
<div className="w-full overflow-x-auto">
  <Table className="min-w-[600px]">
    {/* Table content */}
  </Table>
</div>
```



## Quick Start

### Step 1: Initialize Project

Run the initialization script to create a new React project:
```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

This creates a fully configured project with:
- ✅ React + TypeScript (via Vite)
- ✅ Tailwind CSS 3.4.1 with shadcn/ui theming system
- ✅ Path aliases (`@/`) configured
- ✅ 40+ shadcn/ui components pre-installed
- ✅ All Radix UI dependencies included
- ✅ Parcel configured for bundling (via .parcelrc)
- ✅ Node 18+ compatibility (auto-detects and pins Vite version)

### Step 2: Develop Your Artifact

To build the artifact, edit the generated files. See **Common Development Tasks** below for guidance.

### Step 3: Bundle to Single HTML File

To bundle the React app into a single HTML artifact:
```bash
bash scripts/bundle-artifact.sh
```

This creates `bundle.html` - a self-contained artifact with all JavaScript, CSS, and dependencies inlined. This file can be directly shared in Claude conversations as an artifact.

**Requirements**: Your project must have an `index.html` in the root directory.

**What the script does**:
- Installs bundling dependencies (parcel, @parcel/config-default, parcel-resolver-tspaths, html-inline)
- Creates `.parcelrc` config with path alias support
- Builds with Parcel (no source maps)
- Inlines all assets into single HTML using html-inline

### Step 4: Share Artifact with User

Finally, share the bundled HTML file in conversation with the user so they can view it as an artifact.

### Step 5: Testing/Visualizing the Artifact (Optional)

Note: This is a completely optional step. Only perform if necessary or requested.

To test/visualize the artifact, use available tools (including other Skills or built-in tools like Playwright or Puppeteer). In general, avoid testing the artifact upfront as it adds latency between the request and when the finished artifact can be seen. Test later, after presenting the artifact, if requested or if issues arise.

## Reference

- **shadcn/ui components**: https://ui.shadcn.com/docs/components
