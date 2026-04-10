<!-- Deep reference: UI patterns. Not auto-loaded. -->
<!-- Access via: grep -A N "SECTION_HEADER" references/deep/ui-patterns.md -->
# UI Pattern Library

## 1. HERO SECTIONS

### Overview
Hero sections are the first visual element users encounter and serve as the critical "first impression" zone. Modern hero sections (2024-2025) emphasize bold typography, immersive visuals, and clear value propositions with minimal cognitive load.

### What Makes a Great Implementation

**Great implementations have:**
- **Bold, impactful typography** with oversized headings (typically 48-96px on desktop)
- **Clear value proposition** communicated in < 5 seconds
- **Visual hierarchy** that guides eye movement to CTA
- **Performance-optimized media** (lazy loading, proper image formats)
- **Responsive design** that works on all screen sizes
- **Strategic white space** to prevent overwhelming users
- **Accessible contrast ratios** (WCAG AA minimum: 4.5:1 for text)

**Best-in-class examples:**
- **Vercel.com**: Minimalist with gradient text, strong typography, instant clarity
- **Linear.app**: Dark mode excellence, animated background gradients, keyboard-first design
- **Stripe.com**: Clean, product-focused with subtle animations on scroll
- **Apple.com**: Masterclass in bento grid heroes with product showcase

### Common Mistakes

1. **Too much text**: Walls of text kill engagement. Aim for 10-15 words max in headline.
2. **Slow-loading media**: Large unoptimized images/videos hurt Core Web Vitals
3. **Unclear CTA**: Multiple competing CTAs or buried buttons
4. **Poor mobile adaptation**: Desktop-first thinking that breaks on mobile
5. **Overanimation**: Distracting animations that delay user action
6. **Low contrast**: Light text on light backgrounds (accessibility failure)

### Pattern Types & Code Examples

#### 1.1 Editorial Hero (Text-Focused)

**Best for**: SaaS, content sites, minimalist brands
**Example**: Stripe, Vercel

```jsx
// Editorial Hero - Text-First Design
export function EditorialHero() {
  return (
    <section className="relative bg-white px-6 py-24 sm:py-32 lg:px-8">
      <div className="mx-auto max-w-2xl text-center">
        <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
          Deploy faster with confidence
        </h1>
        <p className="mt-6 text-lg leading-8 text-gray-600">
          Ship your next project in minutes, not days. Built for developers who value speed and reliability.
        </p>
        <div className="mt-10 flex items-center justify-center gap-x-6">
          <a
            href="#"
            className="rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
          >
            Get started
          </a>
          <a href="#" className="text-sm font-semibold leading-6 text-gray-900">
            View demo <span aria-hidden="true">→</span>
          </a>
        </div>
      </div>
    </section>
  );
}
```

**Key techniques:**
- `max-w-2xl` constrains content width for readability
- `text-4xl sm:text-6xl` responsive typography scaling
- `tracking-tight` reduces letter spacing for impact
- Focus-visible outline for keyboard navigation accessibility

#### 1.2 Split-Screen Hero

**Best for**: Product showcases, apps with visual demos
**Example**: Notion, Figma

```jsx
// Split-Screen Hero - 50/50 Layout
export function SplitScreenHero() {
  return (
    <div className="relative overflow-hidden bg-white">
      <div className="pb-80 pt-16 sm:pb-40 sm:pt-24 lg:pb-48 lg:pt-40">
        <div className="relative mx-auto max-w-7xl px-4 sm:static sm:px-6 lg:px-8">
          <div className="sm:max-w-lg">
            <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
              Build products customers love
            </h1>
            <p className="mt-4 text-xl text-gray-500">
              The all-in-one workspace for your team. Docs, wikis, and projects — together.
            </p>
          </div>
          <div>
            <div className="mt-10">
              {/* CTA Buttons */}
              <a
                href="#"
                className="inline-block rounded-md border border-transparent bg-indigo-600 px-8 py-3 text-center font-medium text-white hover:bg-indigo-700"
              >
                Start for free
              </a>
            </div>
          </div>
        </div>

        {/* Right side - Visual */}
        <div className="absolute inset-x-0 top-0 -z-10 transform-gpu overflow-hidden blur-3xl sm:top-[-20rem]">
          <div className="relative left-1/2 aspect-[1155/678] w-[36.125rem] -translate-x-1/2 rotate-[30deg] bg-gradient-to-tr from-indigo-200 to-purple-400 opacity-30 sm:w-[72.1875rem]" />
        </div>
      </div>
    </div>
  );
}
```

**Key techniques:**
- Absolute positioning for decorative gradient background
- `transform-gpu` enables GPU acceleration for better performance
- `aspect-[1155/678]` maintains aspect ratio
- `-z-10` keeps background behind content

#### 1.3 Video Background Hero

**Best for**: High-budget marketing, brand storytelling
**Example**: Apple product launches

```jsx
// Video Background Hero
export function VideoHero() {
  return (
    <div className="relative h-screen overflow-hidden">
      {/* Video Background */}
      <video
        autoPlay
        loop
        muted
        playsInline
        className="absolute inset-0 w-full h-full object-cover"
      >
        <source src="/hero-video.mp4" type="video/mp4" />
      </video>

      {/* Overlay for readability */}
      <div className="absolute inset-0 bg-black/40" />

      {/* Content */}
      <div className="relative z-10 flex h-full items-center justify-center px-6">
        <div className="text-center">
          <h1 className="text-5xl font-bold tracking-tight text-white sm:text-7xl">
            Experience the future
          </h1>
          <p className="mt-6 text-xl text-gray-200">
            Innovation that changes everything.
          </p>
          <div className="mt-10">
            <button className="rounded-full bg-white px-8 py-3 text-sm font-semibold text-gray-900 shadow-sm hover:bg-gray-100">
              Watch the film
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
```

**Key techniques:**
- `playsInline` prevents fullscreen on mobile
- `object-cover` ensures video fills container
- `bg-black/40` creates 40% opacity overlay
- Relative z-10 ensures content stays above video

**Accessibility note**: Always provide controls for video and ensure text contrast meets WCAG standards.

#### 1.4 Asymmetric/Bento Grid Hero

**Best for**: Feature-rich products, design-forward brands
**Example**: Apple.com, Framer

```jsx
// Asymmetric Bento Hero
export function BentoHero() {
  return (
    <div className="mx-auto max-w-7xl px-6 py-24 sm:py-32 lg:px-8">
      <div className="mx-auto max-w-2xl text-center mb-16">
        <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
          Everything you need in one place
        </h1>
      </div>

      {/* Bento Grid */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-6 lg:gap-8">
        {/* Large feature - spans 4 columns */}
        <div className="relative sm:col-span-4 rounded-2xl bg-gradient-to-br from-purple-500 to-pink-500 p-8 sm:p-12 overflow-hidden h-[400px]">
          <h2 className="text-3xl font-bold text-white">Lightning fast</h2>
          <p className="mt-2 text-purple-100">Deploy in seconds, not hours</p>
          <div className="mt-8">
            {/* Placeholder for product image/screenshot */}
            <div className="rounded-lg bg-white/10 backdrop-blur h-48" />
          </div>
        </div>

        {/* Small feature 1 - spans 2 columns */}
        <div className="sm:col-span-2 rounded-2xl bg-gray-900 p-8 h-[400px]">
          <h3 className="text-xl font-semibold text-white">Analytics</h3>
          <p className="mt-2 text-gray-400">Real-time insights</p>
        </div>

        {/* Small feature 2 */}
        <div className="sm:col-span-2 rounded-2xl bg-blue-600 p-8 h-[300px]">
          <h3 className="text-xl font-semibold text-white">Collaboration</h3>
          <p className="mt-2 text-blue-100">Work together seamlessly</p>
        </div>

        {/* Small feature 3 */}
        <div className="sm:col-span-4 rounded-2xl bg-green-500 p-8 h-[300px]">
          <h3 className="text-xl font-semibold text-white">Security first</h3>
          <p className="mt-2 text-green-100">Enterprise-grade protection</p>
        </div>
      </div>
    </div>
  );
}
```

**Key techniques:**
- `sm:col-span-4` creates asymmetric grid spanning multiple columns
- `backdrop-blur` creates frosted glass effect
- `rounded-2xl` (16px) for modern, soft corners
- Fixed heights prevent layout shift during content load

#### 1.5 Parallax Hero

**Best for**: Storytelling sites, creative agencies

```jsx
// Parallax Hero with scroll effect
import { useEffect, useState } from 'react';

export function ParallaxHero() {
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="relative h-screen overflow-hidden">
      {/* Background layer - moves slower */}
      <div
        className="absolute inset-0 bg-gradient-to-br from-blue-500 to-purple-600"
        style={{ transform: `translateY(${scrollY * 0.5}px)` }}
      />

      {/* Mid layer - normal speed */}
      <div
        className="absolute inset-0 flex items-center justify-center"
        style={{ transform: `translateY(${scrollY * 0.7}px)` }}
      >
        <h1 className="text-6xl font-bold text-white">Scroll to explore</h1>
      </div>

      {/* Front layer - faster */}
      <div
        className="absolute bottom-10 left-1/2 -translate-x-1/2"
        style={{ transform: `translateY(${scrollY * 1.2}px)` }}
      >
        <button className="rounded-full bg-white px-6 py-3 text-gray-900 shadow-lg">
          Get started
        </button>
      </div>
    </div>
  );
}
```

**Performance note**: Use `transform` for animations (GPU-accelerated) instead of `top`/`left` (causes reflow).

### Best Practices Summary (2025)

- Use **bold typography** (48-96px headings)
- Keep headlines **under 10-15 words**
- Show **product/interface** in context
- Add **social proof** early (logos, user count)
- Use **high-contrast** colors (4.5:1 minimum)
- Optimize images with **WebP/AVIF** formats
- Implement **lazy loading** for below-fold content
- Design **mobile-first**, enhance for desktop

**Sources:**
- [Detachless: Hero Section Best Practices 2025](https://detachless.com/blog/hero-section-web-design-ideas)
- [Awwwards: Hero Section Inspiration](https://www.awwwards.com/inspiration/hero-section-fit-design)
- [Tailwind UI: Hero Sections](https://tailwindcss.com/plus/ui-blocks/marketing/sections/heroes)

---

## 2. NAVIGATION PATTERNS

### Overview
Modern navigation (2024-2025) prioritizes discoverability, speed, and context awareness. Command palettes, mega menus, and persistent sidebars dominate complex applications.

### What Makes a Great Implementation

**Great implementations have:**
- **Keyboard shortcuts** for power users (e.g., ⌘K for command palette)
- **Clear visual hierarchy** with active states
- **Scoped search** based on current context
- **Mobile-first responsive** behavior (hamburger, drawer, bottom nav)
- **Accessible focus management** (Radix UI/Headless UI primitives)
- **Persistent state** across navigation

**Best-in-class examples:**
- **Linear.app**: Command palette (⌘K) as primary interface, keyboard-first
- **Stripe Docs**: Sidebar navigation with clear hierarchy and search
- **GitHub**: Recently added command palette, persistent sidebar
- **Vercel**: Clean header with dropdown menus and search

### Common Mistakes

1. **Overloaded menus**: Too many top-level items (> 7 causes decision paralysis)
2. **Hidden functionality**: Critical actions buried in submenus
3. **Poor mobile UX**: Desktop nav patterns forced onto mobile
4. **No keyboard support**: Mouse-only navigation excludes power users
5. **Inconsistent state**: Active states not clearly indicated
6. **Slow interactions**: Dropdowns with animation lag

### Pattern Types & Code Examples

#### 2.1 Command Palette (⌘K Style)

**Best for**: Complex apps, productivity tools, dashboards
**Example**: Linear, GitHub, VS Code

**Key package: `cmdk` by Paco Coursey (creator of Radix UI)**

```bash
npm install cmdk
```

```jsx
// Command Palette using cmdk
import { Command } from 'cmdk';
import { useState, useEffect } from 'react';
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';

export function CommandPalette() {
  const [open, setOpen] = useState(false);

  // Toggle with ⌘K
  useEffect(() => {
    const down = (e) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((open) => !open);
      }
    };

    document.addEventListener('keydown', down);
    return () => document.removeEventListener('keydown', down);
  }, []);

  return (
    <Command.Dialog
      open={open}
      onOpenChange={setOpen}
      className="fixed inset-0 z-50"
    >
      <div className="fixed inset-0 bg-black/50" onClick={() => setOpen(false)} />

      <div className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-full max-w-2xl">
        <Command className="rounded-lg border border-gray-200 bg-white shadow-2xl">
          <div className="flex items-center border-b px-4">
            <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
            <Command.Input
              placeholder="Type a command or search..."
              className="w-full border-0 bg-transparent py-4 pl-4 text-sm outline-none placeholder:text-gray-400"
            />
          </div>

          <Command.List className="max-h-96 overflow-y-auto p-2">
            <Command.Empty className="py-6 text-center text-sm text-gray-500">
              No results found.
            </Command.Empty>

            <Command.Group heading="Navigation">
              <Command.Item
                onSelect={() => console.log('Home')}
                className="flex cursor-default items-center rounded-md px-3 py-2 text-sm hover:bg-gray-100"
              >
                <span>Go to Home</span>
                <span className="ml-auto text-xs text-gray-400">⌘H</span>
              </Command.Item>
              <Command.Item className="flex cursor-default items-center rounded-md px-3 py-2 text-sm hover:bg-gray-100">
                <span>Go to Projects</span>
                <span className="ml-auto text-xs text-gray-400">⌘P</span>
              </Command.Item>
            </Command.Group>

            <Command.Separator className="my-2 h-px bg-gray-200" />

            <Command.Group heading="Settings">
              <Command.Item className="flex cursor-default items-center rounded-md px-3 py-2 text-sm hover:bg-gray-100">
                <span>Profile Settings</span>
              </Command.Item>
              <Command.Item className="flex cursor-default items-center rounded-md px-3 py-2 text-sm hover:bg-gray-100">
                <span>Team Settings</span>
              </Command.Item>
            </Command.Group>
          </Command.List>
        </Command>
      </div>
    </Command.Dialog>
  );
}
```

**Implementation notes:**
- Use `cmdk` library for best-in-class UX (fuzzy search, keyboard nav)
- Always include keyboard shortcut (⌘K or Ctrl+K)
- Group commands by category
- Show keyboard shortcuts on right side
- Support scoped search (e.g., "issue" scope for issues)

**Advanced: Add fuzzy search**

```jsx
import Fuse from 'fuse.js';

const commands = [
  { id: 1, name: 'Create new file', action: () => {} },
  { id: 2, name: 'Open settings', action: () => {} },
  // ...
];

const [query, setQuery] = useState('');
const fuse = new Fuse(commands, {
  keys: ['name'],
  threshold: 0.3 // 0 = exact match, 1 = match anything
});

const filteredCommands = query === ''
  ? commands
  : fuse.search(query).map(result => result.item);
```

#### 2.2 Mega Menu Navigation

**Best for**: Content-heavy sites, e-commerce, documentation
**Example**: Stripe.com, Tailwind UI

```jsx
// Mega Menu with shadcn/ui NavigationMenu
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
} from "@/components/ui/navigation-menu";

export function MegaMenu() {
  return (
    <NavigationMenu>
      <NavigationMenuList>
        <NavigationMenuItem>
          <NavigationMenuTrigger>Products</NavigationMenuTrigger>
          <NavigationMenuContent>
            <div className="w-[800px] p-4">
              <div className="grid grid-cols-3 gap-4">
                {/* Column 1: Core Features */}
                <div>
                  <h3 className="mb-2 text-sm font-medium text-gray-900">Core Features</h3>
                  <ul className="space-y-2">
                    <li>
                      <NavigationMenuLink className="block rounded-md p-2 hover:bg-gray-100">
                        <div className="text-sm font-medium">Payments</div>
                        <div className="text-xs text-gray-500">Accept online payments</div>
                      </NavigationMenuLink>
                    </li>
                    <li>
                      <NavigationMenuLink className="block rounded-md p-2 hover:bg-gray-100">
                        <div className="text-sm font-medium">Billing</div>
                        <div className="text-xs text-gray-500">Subscription management</div>
                      </NavigationMenuLink>
                    </li>
                  </ul>
                </div>

                {/* Column 2: Advanced Tools */}
                <div>
                  <h3 className="mb-2 text-sm font-medium text-gray-900">Advanced Tools</h3>
                  <ul className="space-y-2">
                    <li>
                      <NavigationMenuLink className="block rounded-md p-2 hover:bg-gray-100">
                        <div className="text-sm font-medium">Connect</div>
                        <div className="text-xs text-gray-500">Marketplace platform</div>
                      </NavigationMenuLink>
                    </li>
                  </ul>
                </div>

                {/* Column 3: Resources */}
                <div className="rounded-lg bg-gray-50 p-4">
                  <h3 className="mb-2 text-sm font-medium">Resources</h3>
                  <p className="text-xs text-gray-600 mb-4">
                    Learn how to integrate and optimize your setup
                  </p>
                  <a href="#" className="text-sm font-medium text-blue-600 hover:text-blue-700">
                    View documentation →
                  </a>
                </div>
              </div>
            </div>
          </NavigationMenuContent>
        </NavigationMenuItem>

        <NavigationMenuItem>
          <NavigationMenuTrigger>Solutions</NavigationMenuTrigger>
          <NavigationMenuContent>
            {/* Similar structure */}
          </NavigationMenuContent>
        </NavigationMenuItem>
      </NavigationMenuList>
    </NavigationMenu>
  );
}
```

**Key techniques:**
- Fixed width (`w-[800px]`) prevents layout shift
- Grid layout for organized content columns
- Promotional sidebar for featured content
- Hover states provide visual feedback

#### 2.3 Sidebar Navigation (App Shell)

**Best for**: Dashboards, admin panels, complex apps
**Example**: Vercel dashboard, Linear

```jsx
// Sidebar Navigation with shadcn/ui Sidebar
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { Home, Inbox, Settings } from "lucide-react";

export function AppSidebar() {
  return (
    <Sidebar>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Application</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <a href="/">
                    <Home />
                    <span>Home</span>
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <a href="/inbox">
                    <Inbox />
                    <span>Inbox</span>
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton asChild>
                  <a href="/settings">
                    <Settings />
                    <span>Settings</span>
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
```

**Collapsible Sidebar Pattern:**

```jsx
import { useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

export function CollapsibleSidebar() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside className={`transition-all duration-300 bg-white border-r ${
      collapsed ? 'w-16' : 'w-64'
    }`}>
      {/* Toggle button */}
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="absolute -right-3 top-9 flex h-6 w-6 items-center justify-center rounded-full border bg-white"
      >
        {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
      </button>

      {/* Navigation items */}
      <nav className="p-4 space-y-2">
        <a href="/" className="flex items-center gap-3 rounded-lg px-3 py-2 hover:bg-gray-100">
          <Home className="h-5 w-5" />
          {!collapsed && <span>Home</span>}
        </a>
        {/* More items */}
      </nav>
    </aside>
  );
}
```

#### 2.4 Mobile Navigation (Sheet/Drawer)

**Best for**: Mobile-first apps, responsive sites
**Example**: shadcn/ui Sheet component

```jsx
// Mobile Menu Sheet
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Menu } from "lucide-react";

export function MobileNav() {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <button className="lg:hidden p-2">
          <Menu className="h-6 w-6" />
        </button>
      </SheetTrigger>
      <SheetContent side="left" className="w-[300px] sm:w-[400px]">
        <nav className="flex flex-col space-y-4">
          <a href="/" className="text-lg font-medium hover:text-gray-600">
            Home
          </a>
          <a href="/about" className="text-lg font-medium hover:text-gray-600">
            About
          </a>
          <a href="/pricing" className="text-lg font-medium hover:text-gray-600">
            Pricing
          </a>
        </nav>
      </SheetContent>
    </Sheet>
  );
}
```

**Full responsive header pattern:**

```jsx
export function ResponsiveHeader() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-white/80 backdrop-blur">
      <div className="container flex h-16 items-center justify-between">
        {/* Logo */}
        <a href="/" className="flex items-center space-x-2">
          <span className="font-bold">Brand</span>
        </a>

        {/* Desktop nav */}
        <nav className="hidden lg:flex items-center space-x-6">
          <a href="/features" className="text-sm font-medium hover:text-gray-600">
            Features
          </a>
          <a href="/pricing" className="text-sm font-medium hover:text-gray-600">
            Pricing
          </a>
          <a href="/docs" className="text-sm font-medium hover:text-gray-600">
            Docs
          </a>
        </nav>

        {/* Mobile nav */}
        <MobileNav />

        {/* CTA */}
        <div className="hidden lg:flex items-center space-x-4">
          <button className="rounded-md bg-indigo-600 px-4 py-2 text-sm text-white">
            Sign up
          </button>
        </div>
      </div>
    </header>
  );
}
```

#### 2.5 Sticky Header with Scroll Behavior

**Pattern**: Header changes appearance on scroll

```jsx
import { useState, useEffect } from 'react';

export function StickyHeader() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header className={`sticky top-0 z-50 transition-all duration-300 ${
      scrolled
        ? 'bg-white/80 backdrop-blur-lg shadow-sm py-3'
        : 'bg-transparent py-6'
    }`}>
      <div className="container mx-auto px-4">
        {/* Header content */}
      </div>
    </header>
  );
}
```

### Best Practices Summary (2025)

- **Implement command palette** for complex apps (⌘K standard)
- **Use Radix UI/Headless UI** primitives for accessibility
- **Limit top-level nav** to 5-7 items
- **Show active states** clearly
- **Support keyboard navigation**
- **Optimize for mobile** (drawer, bottom nav)
- **Add search** for > 20 navigable items
- **Persist sidebar state** (collapsed/expanded)

**Sources:**
- [shadcn/ui: Navigation Menu](https://ui.shadcn.com/docs/components/navigation-menu)
- [cmdk Documentation](https://cmdk.paco.me/)
- [Radix UI: Navigation Menu](https://www.radix-ui.com/primitives/docs/components/navigation-menu)

---

## 3. CARD LAYOUTS

### Overview
Cards are the fundamental building block of modern web layouts. The 2024-2025 trend emphasizes bento grids, glassmorphism, and dense information architecture inspired by Apple's design language.

### What Makes a Great Implementation

**Great implementations have:**
- **CSS Grid with `auto-fit`/`auto-fill`** for responsive layouts
- **`grid-auto-flow: dense`** for bento grids (fills gaps)
- **Consistent spacing** (typically 1rem/16px gaps)
- **Hover states** with subtle elevation changes
- **Skeleton loading** during data fetch
- **Optimized images** (lazy loading, responsive)

**Best-in-class examples:**
- **Apple.com**: Bento grids for product features
- **Pinterest**: Masonry layout (Tailwind doesn't support natively, use columns)
- **Vercel Dashboard**: Clean card grids with hover effects
- **Stripe**: Glass cards with backdrop blur

### Common Mistakes

1. **Fixed-height cards** that break with dynamic content
2. **Inconsistent spacing** between cards
3. **No skeleton states** (jarring content jumps)
4. **Overuse of shadows** (creates visual noise)
5. **Poor image aspect ratios** (stretched/squished images)
6. **Missing hover feedback**

### Pattern Types & Code Examples

#### 3.1 Bento Grid Layout

**Best for**: Feature showcases, dashboards, landing pages
**Key technique**: `grid-auto-flow: dense` fills gaps automatically

```jsx
// Bento Grid - Modern asymmetric layout
export function BentoGrid() {
  return (
    <div className="mx-auto max-w-7xl px-6 py-24">
      <h2 className="text-4xl font-bold text-center mb-12">
        Everything you need
      </h2>

      {/* The key: grid-auto-flow: dense */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4 auto-rows-fr [grid-auto-flow:dense]">

        {/* Large card - spans 2 columns & 2 rows */}
        <div className="md:col-span-2 md:row-span-2 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 p-8 text-white">
          <h3 className="text-2xl font-bold mb-2">Lightning Fast</h3>
          <p className="text-blue-100">Deploy in seconds, not hours</p>
          <div className="mt-8 h-48 rounded-lg bg-white/10 backdrop-blur" />
        </div>

        {/* Small card - 1 column, 1 row */}
        <div className="rounded-2xl bg-gray-100 p-6">
          <h3 className="font-semibold mb-2">Analytics</h3>
          <p className="text-sm text-gray-600">Real-time insights</p>
        </div>

        {/* Medium card - 1 column, 2 rows */}
        <div className="md:row-span-2 rounded-2xl bg-green-50 p-6">
          <h3 className="font-semibold mb-2">Secure</h3>
          <p className="text-sm text-gray-600">Enterprise-grade</p>
        </div>

        {/* Wide card - 2 columns, 1 row */}
        <div className="md:col-span-2 rounded-2xl bg-yellow-50 p-6">
          <h3 className="font-semibold mb-2">Collaboration</h3>
          <p className="text-sm text-gray-600">Work together seamlessly</p>
        </div>

        {/* Small card */}
        <div className="rounded-2xl bg-pink-50 p-6">
          <h3 className="font-semibold mb-2">AI-Powered</h3>
          <p className="text-sm text-gray-600">Smart automation</p>
        </div>
      </div>
    </div>
  );
}
```

**How Bento Grid Works:**
- `grid-auto-flow: dense` tells CSS Grid to fill gaps with smaller items
- Use `col-span-{n}` and `row-span-{n}` to control size
- `auto-rows-fr` ensures all rows have equal height
- Mix sizes for visual interest (1x1, 2x1, 2x2, etc.)

**Advanced: Responsive Bento Grid**

```jsx
export function ResponsiveBentoGrid({ items }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-4 lg:grid-cols-6 gap-4 auto-rows-[200px] [grid-auto-flow:dense]">
      {items.map((item, idx) => {
        // Determine size based on index or item type
        const sizes = [
          'md:col-span-2 md:row-span-2', // Large
          'md:col-span-1 md:row-span-1', // Small
          'md:col-span-2 md:row-span-1', // Wide
          'md:col-span-1 md:row-span-2', // Tall
        ];

        const sizeClass = sizes[idx % sizes.length];

        return (
          <div
            key={item.id}
            className={`rounded-2xl bg-white border border-gray-200 p-6 hover:shadow-lg transition ${sizeClass}`}
          >
            <h3 className="font-semibold mb-2">{item.title}</h3>
            <p className="text-sm text-gray-600">{item.description}</p>
          </div>
        );
      })}
    </div>
  );
}
```

#### 3.2 Masonry Layout (Pinterest-Style)

**Note**: Tailwind doesn't have native masonry. Use CSS `columns` or JS library.

```jsx
// Masonry using Tailwind columns (CSS-only, no JS)
export function MasonryGrid() {
  const items = [
    { id: 1, height: 'h-48', content: 'Item 1' },
    { id: 2, height: 'h-64', content: 'Item 2' },
    { id: 3, height: 'h-32', content: 'Item 3' },
    { id: 4, height: 'h-56', content: 'Item 4' },
    // ... more items
  ];

  return (
    <div className="columns-1 md:columns-2 lg:columns-3 gap-4 space-y-4">
      {items.map((item) => (
        <div
          key={item.id}
          className={`break-inside-avoid rounded-lg bg-gray-100 p-6 ${item.height}`}
        >
          <h3 className="font-semibold">{item.content}</h3>
          <p className="text-sm text-gray-600">Description text here</p>
        </div>
      ))}
    </div>
  );
}
```

**Key properties:**
- `columns-{n}`: Creates column layout
- `break-inside-avoid`: Prevents items from breaking across columns
- `space-y-{n}`: Vertical spacing between items

**Advanced: Image Masonry with Lazy Loading**

```jsx
export function ImageMasonry({ images }) {
  return (
    <div className="columns-1 sm:columns-2 lg:columns-3 xl:columns-4 gap-4">
      {images.map((img) => (
        <div key={img.id} className="break-inside-avoid mb-4">
          <img
            src={img.url}
            alt={img.alt}
            loading="lazy"
            className="w-full rounded-lg hover:opacity-90 transition"
          />
        </div>
      ))}
    </div>
  );
}
```

#### 3.3 Glass Card (Glassmorphism)

**Best for**: Modern, premium UIs
**Example**: Apple, iOS design

```jsx
// Glass Card with backdrop blur
export function GlassCard() {
  return (
    <div className="relative overflow-hidden rounded-2xl">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-pink-400 via-purple-400 to-blue-500 opacity-80" />

      {/* Glass effect */}
      <div className="relative backdrop-blur-xl bg-white/10 border border-white/20 p-8">
        <h3 className="text-2xl font-bold text-white mb-2">
          Premium Feature
        </h3>
        <p className="text-white/90">
          Experience the future of design with glassmorphism
        </p>
        <button className="mt-4 rounded-lg bg-white/20 backdrop-blur px-6 py-2 text-white border border-white/30 hover:bg-white/30">
          Learn more
        </button>
      </div>
    </div>
  );
}
```

**Key techniques:**
- `backdrop-blur-xl` creates frosted glass effect (requires browser support)
- `bg-white/10` creates 10% opacity white background
- `border-white/20` adds subtle border for definition
- Layered approach: gradient background + glass foreground

**Dark mode glass card:**

```jsx
export function DarkGlassCard() {
  return (
    <div className="relative overflow-hidden rounded-2xl">
      <div className="absolute inset-0 bg-gradient-to-br from-gray-900 via-gray-800 to-black" />

      <div className="relative backdrop-blur-xl bg-black/20 border border-gray-700/50 p-8">
        <h3 className="text-2xl font-bold text-white mb-2">
          Dark Glass
        </h3>
        <p className="text-gray-300">
          Subtle and sophisticated
        </p>
      </div>
    </div>
  );
}
```

#### 3.4 Horizontal Scrolling Cards

**Best for**: Product showcases, testimonials
**Example**: Netflix, App Store

```jsx
// Horizontal Scroll Cards
export function HorizontalCards() {
  const products = Array.from({ length: 8 }, (_, i) => ({
    id: i + 1,
    name: `Product ${i + 1}`,
    price: `$${(i + 1) * 10}`
  }));

  return (
    <div className="py-12">
      <h2 className="text-2xl font-bold mb-6 px-6">Featured Products</h2>

      {/* Horizontal scroll container */}
      <div className="overflow-x-auto scrollbar-hide">
        <div className="flex gap-4 px-6 pb-4">
          {products.map((product) => (
            <div
              key={product.id}
              className="flex-none w-64 rounded-lg bg-white border border-gray-200 p-6 hover:shadow-lg transition"
            >
              <div className="aspect-square rounded-lg bg-gray-200 mb-4" />
              <h3 className="font-semibold">{product.name}</h3>
              <p className="text-gray-600">{product.price}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
```

**CSS for hiding scrollbar:**

```css
/* Add to your global CSS */
@layer utilities {
  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }
  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
}
```

**With scroll indicators:**

```jsx
import { useRef, useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

export function ScrollableCards() {
  const scrollRef = useRef(null);
  const [canScrollLeft, setCanScrollLeft] = useState(false);
  const [canScrollRight, setCanScrollRight] = useState(true);

  const checkScroll = () => {
    if (scrollRef.current) {
      const { scrollLeft, scrollWidth, clientWidth } = scrollRef.current;
      setCanScrollLeft(scrollLeft > 0);
      setCanScrollRight(scrollLeft < scrollWidth - clientWidth - 10);
    }
  };

  const scroll = (direction) => {
    if (scrollRef.current) {
      const scrollAmount = direction === 'left' ? -300 : 300;
      scrollRef.current.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    }
  };

  return (
    <div className="relative">
      {canScrollLeft && (
        <button
          onClick={() => scroll('left')}
          className="absolute left-0 top-1/2 -translate-y-1/2 z-10 bg-white rounded-full p-2 shadow-lg"
        >
          <ChevronLeft />
        </button>
      )}

      <div
        ref={scrollRef}
        onScroll={checkScroll}
        className="overflow-x-auto scrollbar-hide flex gap-4 px-6"
      >
        {/* Cards here */}
      </div>

      {canScrollRight && (
        <button
          onClick={() => scroll('right')}
          className="absolute right-0 top-1/2 -translate-y-1/2 z-10 bg-white rounded-full p-2 shadow-lg"
        >
          <ChevronRight />
        </button>
      )}
    </div>
  );
}
```

#### 3.5 Card with Skeleton Loading

**Best for**: Dynamic data, async content

```jsx
// Card with skeleton state
export function CardWithSkeleton({ loading, data }) {
  if (loading) {
    return (
      <div className="rounded-lg border border-gray-200 p-6 animate-pulse">
        <div className="h-48 bg-gray-200 rounded-lg mb-4" />
        <div className="h-6 bg-gray-200 rounded w-3/4 mb-2" />
        <div className="h-4 bg-gray-200 rounded w-1/2" />
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-gray-200 p-6 hover:shadow-lg transition">
      <img
        src={data.image}
        alt={data.title}
        className="h-48 w-full object-cover rounded-lg mb-4"
      />
      <h3 className="text-lg font-semibold mb-2">{data.title}</h3>
      <p className="text-gray-600">{data.description}</p>
    </div>
  );
}
```

**Reusable Skeleton component:**

```jsx
export function Skeleton({ className }) {
  return (
    <div className={`animate-pulse bg-gray-200 rounded ${className}`} />
  );
}

// Usage
export function ProductCardSkeleton() {
  return (
    <div className="rounded-lg border p-6">
      <Skeleton className="h-48 w-full mb-4" />
      <Skeleton className="h-6 w-3/4 mb-2" />
      <Skeleton className="h-4 w-1/2 mb-4" />
      <Skeleton className="h-10 w-full" />
    </div>
  );
}
```

### Best Practices Summary (2025)

- **Use bento grids** for modern, Apple-inspired layouts
- **Implement skeleton states** during loading
- **Add subtle hover effects** (shadow, scale)
- **Optimize images** (WebP, lazy loading)
- **Use CSS Grid** over Flexbox for cards
- **Maintain consistent spacing** (gap-4 or gap-6)
- **Test with variable content** lengths

**Sources:**
- [Tailwind UI: Bento Grids](https://tailwindcss.com/plus/ui-blocks/marketing/sections/bento-grids)
- [BentoGrids.com: Inspiration Gallery](https://bentogrids.com/)
- [Dev.to: Responsive Bento Grid Tutorial](https://dev.to/velox-web/how-to-build-a-responsive-bento-grid-with-tailwind-css-no-masonryjs-3f2c)

---

## 4. DASHBOARD LAYOUTS

### Overview
Modern dashboard layouts (2024-2025) prioritize information density, customization, and responsive behavior. The sidebar+main content pattern dominates.

### What Makes a Great Implementation

**Great implementations have:**
- **Collapsible sidebar** with persistent state
- **Responsive grid** for widgets/cards
- **Dark mode support**
- **Breadcrumbs** for deep navigation
- **Quick actions** toolbar
- **Keyboard shortcuts** (⌘K for search)

**Best-in-class examples:**
- **Linear**: Dense, keyboard-first, beautiful dark mode
- **Vercel Dashboard**: Clean, card-based widgets
- **Stripe Dashboard**: Information-dense with great data viz
- **shadcn/ui Admin Templates**: Modern component library

### Common Mistakes

1. **Too much white space** (wasted screen real estate)
2. **Non-responsive grids** that break on mobile
3. **Cluttered sidebar** with too many items
4. **Missing empty states**
5. **No loading states**
6. **Poor data visualization** (illegible charts)

### Pattern Types & Code Examples

#### 4.1 Sidebar + Main Dashboard

**Best for**: Admin panels, SaaS apps

```jsx
// Dashboard Layout with shadcn/ui
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";

export function DashboardLayout({ children }) {
  return (
    <SidebarProvider>
      <div className="flex min-h-screen">
        <AppSidebar />

        <main className="flex-1">
          {/* Header */}
          <header className="sticky top-0 z-10 flex h-16 items-center gap-4 border-b bg-white px-6">
            <SidebarTrigger />
            <h1 className="text-xl font-semibold">Dashboard</h1>

            {/* Search */}
            <div className="ml-auto flex items-center gap-4">
              <button className="text-sm text-gray-600 hover:text-gray-900">
                ⌘K to search
              </button>
            </div>
          </header>

          {/* Main Content */}
          <div className="p-6">
            {children}
          </div>
        </main>
      </div>
    </SidebarProvider>
  );
}

// Dashboard Content - Widget Grid
export function DashboardContent() {
  return (
    <div className="space-y-6">
      {/* Stats Row */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Revenue" value="$12,345" change="+12.5%" />
        <StatCard title="Users" value="1,234" change="+8.2%" />
        <StatCard title="Sessions" value="5,678" change="-2.1%" />
        <StatCard title="Bounce Rate" value="42%" change="+1.3%" />
      </div>

      {/* Charts Row */}
      <div className="grid gap-4 md:grid-cols-2">
        <ChartCard title="Revenue Over Time" />
        <ChartCard title="User Growth" />
      </div>

      {/* Table */}
      <RecentActivityTable />
    </div>
  );
}

function StatCard({ title, value, change }) {
  const isPositive = change.startsWith('+');

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6">
      <p className="text-sm text-gray-600">{title}</p>
      <p className="text-3xl font-bold mt-2">{value}</p>
      <p className={`text-sm mt-2 ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
        {change} from last month
      </p>
    </div>
  );
}
```

**Advanced: With loading states**

```jsx
export function StatCard({ title, value, change, loading }) {
  if (loading) {
    return (
      <div className="rounded-lg border border-gray-200 bg-white p-6 animate-pulse">
        <div className="h-4 bg-gray-200 rounded w-24 mb-3" />
        <div className="h-8 bg-gray-200 rounded w-32 mb-2" />
        <div className="h-4 bg-gray-200 rounded w-28" />
      </div>
    );
  }

  const isPositive = change.startsWith('+');

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6 hover:shadow-md transition">
      <div className="flex items-center justify-between mb-2">
        <p className="text-sm text-gray-600">{title}</p>
        <TrendingUpIcon className={`h-4 w-4 ${isPositive ? 'text-green-600' : 'text-red-600'}`} />
      </div>
      <p className="text-3xl font-bold">{value}</p>
      <p className={`text-sm mt-2 flex items-center gap-1 ${
        isPositive ? 'text-green-600' : 'text-red-600'
      }`}>
        <span>{change}</span>
        <span className="text-gray-500">from last month</span>
      </p>
    </div>
  );
}
```

#### 4.2 Dense Data Dashboard

**Best for**: Analytics, monitoring tools
**Example**: Grafana, Datadog

```jsx
// Dense Dashboard with compact cards
export function DenseDataDashboard() {
  return (
    <div className="p-4 bg-gray-50 min-h-screen">
      {/* Compact header */}
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-lg font-semibold">System Overview</h1>
        <div className="flex gap-2">
          <select className="text-sm border rounded px-2 py-1">
            <option>Last 24h</option>
            <option>Last 7d</option>
          </select>
        </div>
      </div>

      {/* Tight grid - less spacing for density */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        {/* Compact stat cards */}
        <div className="rounded bg-white border p-3">
          <p className="text-xs text-gray-500">CPU Usage</p>
          <p className="text-2xl font-bold">67%</p>
        </div>
        <div className="rounded bg-white border p-3">
          <p className="text-xs text-gray-500">Memory</p>
          <p className="text-2xl font-bold">4.2 GB</p>
        </div>
        <div className="rounded bg-white border p-3">
          <p className="text-xs text-gray-500">Requests/s</p>
          <p className="text-2xl font-bold">1.2k</p>
        </div>
        <div className="rounded bg-white border p-3">
          <p className="text-xs text-gray-500">Errors</p>
          <p className="text-2xl font-bold text-red-600">23</p>
        </div>
      </div>

      {/* Charts below */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-3 mt-3">
        <div className="rounded bg-white border p-4 h-64">
          <h3 className="text-sm font-medium mb-2">Response Time</h3>
          {/* Chart component here */}
        </div>
        <div className="rounded bg-white border p-4 h-64">
          <h3 className="text-sm font-medium mb-2">Error Rate</h3>
          {/* Chart component here */}
        </div>
      </div>
    </div>
  );
}
```

**Key techniques for dense dashboards:**
- Smaller gaps (gap-3 instead of gap-6)
- Compact padding (p-3 instead of p-6)
- Smaller typography (text-sm, text-xs)
- More items per row (grid-cols-4 on desktop)

#### 4.3 Settings Page Layout

**Best for**: User settings, configuration pages

```jsx
// Settings Page with Sidebar Navigation
export function SettingsLayout() {
  return (
    <div className="flex min-h-screen">
      {/* Settings Sidebar */}
      <aside className="w-64 border-r bg-gray-50 p-6">
        <h2 className="text-lg font-semibold mb-4">Settings</h2>
        <nav className="space-y-1">
          <a href="#" className="block rounded-md px-3 py-2 bg-white border text-sm font-medium">
            Profile
          </a>
          <a href="#" className="block rounded-md px-3 py-2 text-sm text-gray-600 hover:bg-gray-100">
            Account
          </a>
          <a href="#" className="block rounded-md px-3 py-2 text-sm text-gray-600 hover:bg-gray-100">
            Notifications
          </a>
          <a href="#" className="block rounded-md px-3 py-2 text-sm text-gray-600 hover:bg-gray-100">
            Billing
          </a>
        </nav>
      </aside>

      {/* Settings Content */}
      <main className="flex-1 p-8">
        <div className="max-w-2xl">
          <h1 className="text-2xl font-bold mb-2">Profile Settings</h1>
          <p className="text-gray-600 mb-8">
            Manage your profile information and preferences
          </p>

          <div className="space-y-6">
            {/* Form sections */}
            <div>
              <label className="block text-sm font-medium mb-2">Full Name</label>
              <input
                type="text"
                className="w-full rounded-md border border-gray-300 px-4 py-2"
                placeholder="John Doe"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Email</label>
              <input
                type="email"
                className="w-full rounded-md border border-gray-300 px-4 py-2"
                placeholder="john@example.com"
              />
            </div>

            <div className="pt-4 border-t">
              <button className="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
                Save Changes
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
```

**Advanced: Tabbed settings**

```jsx
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export function TabbedSettings() {
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Settings</h1>

      <Tabs defaultValue="profile" className="w-full">
        <TabsList className="mb-8">
          <TabsTrigger value="profile">Profile</TabsTrigger>
          <TabsTrigger value="account">Account</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
          <TabsTrigger value="billing">Billing</TabsTrigger>
        </TabsList>

        <TabsContent value="profile">
          <ProfileSettings />
        </TabsContent>

        <TabsContent value="account">
          <AccountSettings />
        </TabsContent>

        {/* More tabs */}
      </Tabs>
    </div>
  );
}
```

### Best Practices Summary (2025)

- **Use sidebar patterns** for complex navigation
- **Implement collapsible sidebars** (save space)
- **Design for data density** (especially analytics)
- **Add empty/loading states** for all widgets
- **Support keyboard shortcuts** (⌘K)
- **Make grids responsive** (stack on mobile)
- **Use consistent spacing** (gap-4 or gap-6)

**Sources:**
- [Vercel: Dashboard Templates](https://vercel.com/templates/saas)
- [shadcn/ui: Sidebar Component](https://ui.shadcn.com/docs/components/sidebar)
- [Tailwind UI: Application Shells](https://tailwindcss.com/plus/ui-blocks/application-ui/application-shells/stacked)

---

## 5. DATA DISPLAY PATTERNS

### Overview
Data display patterns handle tables, lists, timelines, and complex data structures. The 2024-2025 focus is on mobile-first responsive strategies and accessible, sortable tables.

### What Makes a Great Implementation

**Great implementations have:**
- **Responsive mobile strategy** (cards, not horizontal scroll)
- **Sorting and filtering** built-in
- **Pagination** for large datasets
- **Row selection** with checkboxes
- **Inline actions** (edit, delete)
- **Keyboard navigation** (arrow keys)
- **Virtualization** for 1000+ rows (TanStack Virtual)

**Best-in-class examples:**
- **GitHub**: Complex tables with filters, sorting
- **Linear**: Issues table with keyboard nav, inline editing
- **Notion**: Database views (table, board, timeline)
- **TanStack Table**: Industry-standard React table library

### Common Mistakes

1. **Horizontal scroll on mobile** (bad UX)
2. **No loading states**
3. **Poor column width management**
4. **Missing empty states**
5. **Inaccessible table markup** (no `<thead>`, `<th>`)
6. **No virtualization** for large lists (performance)

### Pattern Types & Code Examples

#### 5.1 Responsive Table (Mobile: Cards)

**Best strategy**: Table on desktop, cards on mobile

```jsx
// Responsive Table - Desktop table, Mobile cards
export function ResponsiveTable({ data }) {
  return (
    <>
      {/* Desktop table */}
      <div className="hidden md:block overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Name
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Email
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data.map((row) => (
              <tr key={row.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {row.name}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {row.email}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="inline-flex rounded-full bg-green-100 px-2 text-xs font-semibold text-green-800">
                    {row.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  <button className="text-blue-600 hover:text-blue-900">Edit</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Mobile cards */}
      <div className="md:hidden space-y-4">
        {data.map((row) => (
          <div key={row.id} className="bg-white border rounded-lg p-4">
            <div className="flex justify-between items-start mb-2">
              <h3 className="font-medium">{row.name}</h3>
              <span className="inline-flex rounded-full bg-green-100 px-2 text-xs font-semibold text-green-800">
                {row.status}
              </span>
            </div>
            <p className="text-sm text-gray-500 mb-3">{row.email}</p>
            <button className="text-sm text-blue-600">Edit</button>
          </div>
        ))}
      </div>
    </>
  );
}
```

**Key techniques:**
- `hidden md:block` hides table on mobile, shows on medium+
- `md:hidden` shows cards only on mobile
- Semantic HTML with proper `<thead>`, `<th>`, `<tbody>`
- `whitespace-nowrap` prevents text wrapping in cells

#### 5.2 TanStack Table (Advanced)

**Best for**: Complex tables with sorting, filtering, pagination
**Library**: `@tanstack/react-table` v8

```bash
npm install @tanstack/react-table
```

```jsx
// TanStack Table with sorting
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  flexRender,
  createColumnHelper,
} from '@tanstack/react-table';
import { useState } from 'react';
import { ArrowUpDown } from 'lucide-react';

const columnHelper = createColumnHelper();

export function TanStackTable({ data }) {
  const [sorting, setSorting] = useState([]);

  const columns = [
    columnHelper.accessor('name', {
      header: ({ column }) => (
        <button
          className="flex items-center gap-2"
          onClick={() => column.toggleSorting()}
        >
          Name
          <ArrowUpDown className="h-4 w-4" />
        </button>
      ),
      cell: info => info.getValue(),
    }),
    columnHelper.accessor('email', {
      header: 'Email',
      cell: info => info.getValue(),
    }),
    columnHelper.accessor('status', {
      header: 'Status',
      cell: info => (
        <span className="inline-flex rounded-full bg-green-100 px-2 text-xs font-semibold text-green-800">
          {info.getValue()}
        </span>
      ),
    }),
    columnHelper.display({
      id: 'actions',
      header: 'Actions',
      cell: props => (
        <button
          onClick={() => console.log('Edit', props.row.original.id)}
          className="text-blue-600 hover:text-blue-900"
        >
          Edit
        </button>
      ),
    }),
  ];

  const table = useReactTable({
    data,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th
                  key={header.id}
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {header.isPlaceholder
                    ? null
                    : flexRender(header.column.columnDef.header, header.getContext())}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id} className="hover:bg-gray-50">
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id} className="px-6 py-4 whitespace-nowrap text-sm">
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

**Advanced: Add filtering and pagination**

```jsx
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
} from '@tanstack/react-table';
import { useState } from 'react';

export function AdvancedTable({ data }) {
  const [sorting, setSorting] = useState([]);
  const [globalFilter, setGlobalFilter] = useState('');

  const table = useReactTable({
    data,
    columns,
    state: {
      sorting,
      globalFilter,
    },
    onSortingChange: setSorting,
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    initialState: {
      pagination: {
        pageSize: 10,
      },
    },
  });

  return (
    <div>
      {/* Search */}
      <div className="mb-4">
        <input
          value={globalFilter ?? ''}
          onChange={e => setGlobalFilter(e.target.value)}
          className="rounded-md border border-gray-300 px-4 py-2"
          placeholder="Search..."
        />
      </div>

      {/* Table */}
      <table className="min-w-full divide-y divide-gray-200">
        {/* ... table content ... */}
      </table>

      {/* Pagination */}
      <div className="flex items-center justify-between mt-4">
        <div className="flex gap-2">
          <button
            onClick={() => table.setPageIndex(0)}
            disabled={!table.getCanPreviousPage()}
            className="px-3 py-1 border rounded disabled:opacity-50"
          >
            {'<<'}
          </button>
          <button
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
            className="px-3 py-1 border rounded disabled:opacity-50"
          >
            {'<'}
          </button>
          <button
            onClick={() => table.nextPage()}
            disabled={!table.getCanNextPage()}
            className="px-3 py-1 border rounded disabled:opacity-50"
          >
            {'>'}
          </button>
          <button
            onClick={() => table.setPageIndex(table.getPageCount() - 1)}
            disabled={!table.getCanNextPage()}
            className="px-3 py-1 border rounded disabled:opacity-50"
          >
            {'>>'}
          </button>
        </div>
        <span className="text-sm text-gray-600">
          Page {table.getState().pagination.pageIndex + 1} of {table.getPageCount()}
        </span>
      </div>
    </div>
  );
}
```

#### 5.3 Timeline View

**Best for**: Activity feeds, project timelines

```jsx
// Timeline View
export function Timeline({ events }) {
  return (
    <div className="flow-root">
      <ul className="-mb-8">
        {events.map((event, idx) => (
          <li key={event.id}>
            <div className="relative pb-8">
              {/* Vertical line */}
              {idx !== events.length - 1 && (
                <span
                  className="absolute left-4 top-4 -ml-px h-full w-0.5 bg-gray-200"
                  aria-hidden="true"
                />
              )}

              <div className="relative flex space-x-3">
                {/* Icon */}
                <div>
                  <span className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center ring-8 ring-white">
                    <svg className="h-5 w-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  </span>
                </div>

                {/* Content */}
                <div className="flex min-w-0 flex-1 justify-between space-x-4 pt-1.5">
                  <div>
                    <p className="text-sm text-gray-500">
                      {event.content}{' '}
                      <a href="#" className="font-medium text-gray-900">
                        {event.target}
                      </a>
                    </p>
                  </div>
                  <div className="whitespace-nowrap text-right text-sm text-gray-500">
                    <time dateTime={event.datetime}>{event.date}</time>
                  </div>
                </div>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

**Advanced: Grouped timeline**

```jsx
export function GroupedTimeline({ events }) {
  // Group events by date
  const grouped = events.reduce((acc, event) => {
    const date = new Date(event.datetime).toLocaleDateString();
    if (!acc[date]) acc[date] = [];
    acc[date].push(event);
    return acc;
  }, {});

  return (
    <div className="space-y-8">
      {Object.entries(grouped).map(([date, dateEvents]) => (
        <div key={date}>
          <h3 className="text-sm font-semibold text-gray-900 mb-4">{date}</h3>
          <div className="space-y-4">
            {dateEvents.map(event => (
              <div key={event.id} className="flex gap-4">
                <div className="flex-shrink-0 w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center">
                  {event.icon}
                </div>
                <div>
                  <p className="text-sm text-gray-900">{event.title}</p>
                  <p className="text-xs text-gray-500">{event.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
```

#### 5.4 Kanban Board

**Best for**: Project management, task tracking

```jsx
// Simple Kanban Board (no drag-drop)
export function KanbanBoard({ columns }) {
  return (
    <div className="flex gap-4 overflow-x-auto pb-4">
      {columns.map((column) => (
        <div key={column.id} className="flex-shrink-0 w-80">
          {/* Column Header */}
          <div className="rounded-t-lg bg-gray-100 px-4 py-3">
            <h3 className="font-semibold flex items-center gap-2">
              {column.title}
              <span className="text-sm text-gray-500">({column.tasks.length})</span>
            </h3>
          </div>

          {/* Tasks */}
          <div className="space-y-2 bg-gray-50 p-4 rounded-b-lg min-h-[200px]">
            {column.tasks.map((task) => (
              <div
                key={task.id}
                className="bg-white rounded-lg border p-4 cursor-move hover:shadow-md transition"
              >
                <h4 className="font-medium mb-2">{task.title}</h4>
                <p className="text-sm text-gray-600 mb-3">{task.description}</p>
                <div className="flex items-center gap-2">
                  <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                    {task.priority}
                  </span>
                  {task.assignee && (
                    <img
                      src={task.assignee.avatar}
                      alt={task.assignee.name}
                      className="h-6 w-6 rounded-full"
                    />
                  )}
                </div>
              </div>
            ))}

            {/* Add task button */}
            <button className="w-full text-left text-sm text-gray-500 hover:text-gray-700 px-4 py-2 rounded-lg hover:bg-white border border-dashed border-gray-300">
              + Add task
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
```

**With drag-and-drop (using @dnd-kit):**

```bash
npm install @dnd-kit/core @dnd-kit/sortable
```

```jsx
import { DndContext, closestCenter } from '@dnd-kit/core';
import { SortableContext, useSortable, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';

function SortableTask({ task }) {
  const { attributes, listeners, setNodeRef, transform, transition } = useSortable({
    id: task.id,
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className="bg-white rounded-lg border p-4 cursor-move hover:shadow-md transition"
    >
      <h4 className="font-medium mb-2">{task.title}</h4>
      <p className="text-sm text-gray-600">{task.description}</p>
    </div>
  );
}

export function DraggableKanban({ columns, onDragEnd }) {
  return (
    <DndContext collisionDetection={closestCenter} onDragEnd={onDragEnd}>
      <div className="flex gap-4 overflow-x-auto pb-4">
        {columns.map((column) => (
          <div key={column.id} className="flex-shrink-0 w-80">
            <div className="rounded-t-lg bg-gray-100 px-4 py-3">
              <h3 className="font-semibold">{column.title}</h3>
            </div>
            <SortableContext items={column.tasks.map(t => t.id)} strategy={verticalListSortingStrategy}>
              <div className="space-y-2 bg-gray-50 p-4 rounded-b-lg min-h-[200px]">
                {column.tasks.map((task) => (
                  <SortableTask key={task.id} task={task} />
                ))}
              </div>
            </SortableContext>
          </div>
        ))}
      </div>
    </DndContext>
  );
}
```

### Best Practices Summary (2025)

- **Use TanStack Table** for advanced tables
- **Mobile strategy**: Cards, not horizontal scroll
- **Add sorting/filtering** for > 20 rows
- **Virtualize** for > 100 rows (TanStack Virtual)
- **Show loading skeletons** during fetch
- **Implement pagination** for large datasets
- **Use semantic HTML** (`<table>`, `<th>`, `<thead>`)

**Sources:**
- [TanStack Table Documentation](https://tanstack.com/table/v8)
- [GitHub: Issue List Patterns](https://github.com/features/issues)
- [Notion: Database Views](https://www.notion.com/)

---

## 6. FORM PATTERNS

### Overview
Modern forms (2024-2025) emphasize inline validation, floating labels, auto-save, and multi-step wizards. Accessibility and user feedback are critical.

### What Makes a Great Implementation

**Great implementations have:**
- **Inline validation** with clear error messages
- **Floating labels** (Material Design style)
- **Auto-save** for long forms
- **Keyboard navigation** (Tab, Enter)
- **Progress indicators** for multi-step
- **Accessible markup** (proper labels, ARIA)
- **Loading states** on submit

**Best-in-class examples:**
- **Stripe Checkout**: Minimal, clear, excellent validation
- **Linear**: Inline editing, keyboard shortcuts
- **Radix UI Forms**: Accessible primitives
- **shadcn/ui Forms**: React Hook Form + Zod

### Common Mistakes

1. **No inline validation** (wait until submit)
2. **Vague error messages** ("Invalid input")
3. **Poor label placement** (not associated with inputs)
4. **No loading state** on submit
5. **Tiny click targets** (< 44px)
6. **No keyboard support**

### Pattern Types & Code Examples

#### 6.1 Form with Inline Validation

**Best practices**: React Hook Form + Zod + shadcn/ui

```bash
npm install react-hook-form zod @hookform/resolvers
```

```jsx
// Form with inline validation
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';

const formSchema = z.object({
  email: z.string().email({ message: 'Invalid email address' }),
  password: z.string().min(8, { message: 'Password must be at least 8 characters' }),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});

export function LoginForm() {
  const form = useForm({
    resolver: zodResolver(formSchema),
    mode: 'onChange', // Validate on change
    defaultValues: {
      email: '',
      password: '',
      confirmPassword: '',
    },
  });

  const onSubmit = async (data) => {
    console.log(data);
    // API call here
  };

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700">
          Email
        </label>
        <input
          id="email"
          type="email"
          {...form.register('email')}
          className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm focus:outline-none focus:ring-1 ${
            form.formState.errors.email
              ? 'border-red-500 focus:border-red-500 focus:ring-red-500'
              : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'
          }`}
        />
        {form.formState.errors.email && (
          <p className="mt-1 text-sm text-red-600">{form.formState.errors.email.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700">
          Password
        </label>
        <input
          id="password"
          type="password"
          {...form.register('password')}
          className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm focus:outline-none focus:ring-1 ${
            form.formState.errors.password
              ? 'border-red-500 focus:border-red-500 focus:ring-red-500'
              : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'
          }`}
        />
        {form.formState.errors.password && (
          <p className="mt-1 text-sm text-red-600">{form.formState.errors.password.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
          Confirm Password
        </label>
        <input
          id="confirmPassword"
          type="password"
          {...form.register('confirmPassword')}
          className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm focus:outline-none focus:ring-1 ${
            form.formState.errors.confirmPassword
              ? 'border-red-500 focus:border-red-500 focus:ring-red-500'
              : 'border-gray-300 focus:border-blue-500 focus:ring-blue-500'
          }`}
        />
        {form.formState.errors.confirmPassword && (
          <p className="mt-1 text-sm text-red-600">{form.formState.errors.confirmPassword.message}</p>
        )}
      </div>

      <button
        type="submit"
        disabled={form.formState.isSubmitting}
        className="w-full rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {form.formState.isSubmitting ? 'Signing in...' : 'Sign in'}
      </button>
    </form>
  );
}
```

**Key techniques:**
- `mode: 'onChange'` validates as user types (can also use `onBlur`)
- Conditional styling based on error state
- `formState.isSubmitting` for loading state
- `refine` for custom validation (password match)

#### 6.2 Multi-Step Form Wizard

**Best for**: Onboarding, complex forms

```jsx
// Multi-step form wizard
import { useState } from 'react';
import { useForm } from 'react-hook-form';

export function MultiStepForm() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    role: '',
  });

  const form = useForm({
    defaultValues: formData,
  });

  const updateField = (field, value) => {
    setFormData({ ...formData, [field]: value });
  };

  const nextStep = async () => {
    // Validate current step
    const isValid = await form.trigger();
    if (isValid) {
      setStep(step + 1);
    }
  };

  const prevStep = () => setStep(step - 1);

  const onSubmit = async (data) => {
    console.log('Final data:', data);
    // Submit to API
  };

  return (
    <div className="max-w-2xl mx-auto p-8">
      {/* Progress bar */}
      <div className="mb-8">
        <div className="flex justify-between mb-2">
          <span className="text-sm font-medium">Step {step} of 3</span>
          <span className="text-sm text-gray-500">{Math.round((step / 3) * 100)}%</span>
        </div>
        <div className="h-2 bg-gray-200 rounded-full">
          <div
            className="h-2 bg-blue-600 rounded-full transition-all duration-300"
            style={{ width: `${(step / 3) * 100}%` }}
          />
        </div>
      </div>

      <form onSubmit={form.handleSubmit(onSubmit)}>
        {/* Step content */}
        {step === 1 && (
          <div className="space-y-4">
            <h2 className="text-2xl font-bold">Personal Information</h2>
            <div>
              <label className="block text-sm font-medium mb-2">Full Name</label>
              <input
                {...form.register('name', { required: 'Name is required' })}
                className="w-full rounded-md border border-gray-300 px-4 py-2"
              />
              {form.formState.errors.name && (
                <p className="mt-1 text-sm text-red-600">{form.formState.errors.name.message}</p>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Email</label>
              <input
                type="email"
                {...form.register('email', {
                  required: 'Email is required',
                  pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                    message: 'Invalid email address'
                  }
                })}
                className="w-full rounded-md border border-gray-300 px-4 py-2"
              />
              {form.formState.errors.email && (
                <p className="mt-1 text-sm text-red-600">{form.formState.errors.email.message}</p>
              )}
            </div>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-4">
            <h2 className="text-2xl font-bold">Company Details</h2>
            <div>
              <label className="block text-sm font-medium mb-2">Company Name</label>
              <input
                {...form.register('company', { required: 'Company is required' })}
                className="w-full rounded-md border border-gray-300 px-4 py-2"
              />
              {form.formState.errors.company && (
                <p className="mt-1 text-sm text-red-600">{form.formState.errors.company.message}</p>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Your Role</label>
              <select
                {...form.register('role', { required: 'Role is required' })}
                className="w-full rounded-md border border-gray-300 px-4 py-2"
              >
                <option value="">Select role</option>
                <option value="developer">Developer</option>
                <option value="designer">Designer</option>
                <option value="manager">Manager</option>
              </select>
              {form.formState.errors.role && (
                <p className="mt-1 text-sm text-red-600">{form.formState.errors.role.message}</p>
              )}
            </div>
          </div>
        )}

        {step === 3 && (
          <div className="space-y-4">
            <h2 className="text-2xl font-bold">Review & Submit</h2>
            <div className="rounded-lg bg-gray-50 p-4 space-y-2">
              <p><strong>Name:</strong> {form.watch('name')}</p>
              <p><strong>Email:</strong> {form.watch('email')}</p>
              <p><strong>Company:</strong> {form.watch('company')}</p>
              <p><strong>Role:</strong> {form.watch('role')}</p>
            </div>
          </div>
        )}

        {/* Navigation buttons */}
        <div className="flex justify-between mt-8">
          <button
            type="button"
            onClick={prevStep}
            disabled={step === 1}
            className="rounded-md border border-gray-300 px-4 py-2 disabled:opacity-50"
          >
            Previous
          </button>
          {step < 3 ? (
            <button
              type="button"
              onClick={nextStep}
              className="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
            >
              Next
            </button>
          ) : (
            <button
              type="submit"
              disabled={form.formState.isSubmitting}
              className="rounded-md bg-green-600 px-4 py-2 text-white hover:bg-green-700 disabled:opacity-50"
            >
              {form.formState.isSubmitting ? 'Submitting...' : 'Submit'}
            </button>
          )}
        </div>
      </form>
    </div>
  );
}
```

**Key techniques:**
- `form.trigger()` validates current fields before progressing
- `form.watch()` reads form values for review step
- Progress bar shows completion percentage
- Conditional rendering based on step

#### 6.3 Autocomplete / Combobox

**Best for**: Search, location pickers
**Component**: Headless UI Combobox

```jsx
// Combobox with search
import { Combobox } from '@headlessui/react';
import { useState } from 'react';
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/react/20/solid';

const people = [
  { id: 1, name: 'Wade Cooper' },
  { id: 2, name: 'Arlene Mccoy' },
  { id: 3, name: 'Devon Webb' },
  { id: 4, name: 'Tom Cook' },
  { id: 5, name: 'Tanya Fox' },
];

export function ComboboxExample() {
  const [selected, setSelected] = useState(people[0]);
  const [query, setQuery] = useState('');

  const filtered =
    query === ''
      ? people
      : people.filter((person) =>
          person.name.toLowerCase().includes(query.toLowerCase())
        );

  return (
    <Combobox value={selected} onChange={setSelected}>
      <div className="relative">
        <div className="relative w-full">
          <Combobox.Input
            className="w-full rounded-md border border-gray-300 py-2 pl-3 pr-10 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            displayValue={(person) => person.name}
            onChange={(event) => setQuery(event.target.value)}
          />
          <Combobox.Button className="absolute inset-y-0 right-0 flex items-center pr-2">
            <ChevronUpDownIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
          </Combobox.Button>
        </div>

        <Combobox.Options className="absolute mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none z-10">
          {filtered.length === 0 && query !== '' ? (
            <div className="relative cursor-default select-none px-4 py-2 text-gray-700">
              Nothing found.
            </div>
          ) : (
            filtered.map((person) => (
              <Combobox.Option
                key={person.id}
                value={person}
                className={({ active }) =>
                  `relative cursor-default select-none py-2 pl-10 pr-4 ${
                    active ? 'bg-blue-600 text-white' : 'text-gray-900'
                  }`
                }
              >
                {({ selected, active }) => (
                  <>
                    <span className={`block truncate ${selected ? 'font-medium' : 'font-normal'}`}>
                      {person.name}
                    </span>
                    {selected && (
                      <span
                        className={`absolute inset-y-0 left-0 flex items-center pl-3 ${
                          active ? 'text-white' : 'text-blue-600'
                        }`}
                      >
                        <CheckIcon className="h-5 w-5" aria-hidden="true" />
                      </span>
                    )}
                  </>
                )}
              </Combobox.Option>
            ))
          )}
        </Combobox.Options>
      </div>
    </Combobox>
  );
}
```

**Key techniques:**
- `displayValue` formats selected value in input
- Filter logic supports fuzzy search
- Absolute positioning for dropdown
- Active and selected states styled differently

#### 6.4 File Upload with Drag-and-Drop

**Best for**: Document uploads, image uploads

```jsx
// File upload with drag-and-drop
import { useState, useCallback } from 'react';
import { Upload, X } from 'lucide-react';

export function FileUpload() {
  const [files, setFiles] = useState([]);
  const [isDragging, setIsDragging] = useState(false);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);

    const droppedFiles = Array.from(e.dataTransfer.files);
    setFiles((prev) => [...prev, ...droppedFiles]);
  }, []);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleFileInput = (e) => {
    const selectedFiles = Array.from(e.target.files);
    setFiles((prev) => [...prev, ...selectedFiles]);
  };

  const removeFile = (index) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <div className="space-y-4">
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`border-2 border-dashed rounded-lg p-12 text-center transition ${
          isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
        }`}
      >
        <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
        <p className="text-sm text-gray-600 mb-2">
          Drag and drop files here, or{' '}
          <label className="text-blue-600 hover:text-blue-700 cursor-pointer font-medium">
            browse
            <input
              type="file"
              multiple
              onChange={handleFileInput}
              className="hidden"
              accept="image/*,.pdf,.doc,.docx"
            />
          </label>
        </p>
        <p className="text-xs text-gray-500">
          Supports: Images, PDF, DOC (Max 10MB per file)
        </p>
      </div>

      {/* File list */}
      {files.length > 0 && (
        <div className="space-y-2">
          <h3 className="text-sm font-medium">Uploaded Files ({files.length})</h3>
          {files.map((file, index) => (
            <div
              key={index}
              className="flex items-center justify-between rounded-lg border p-3 hover:bg-gray-50"
            >
              <div className="flex items-center gap-3 flex-1 min-w-0">
                <div className="flex-shrink-0 w-10 h-10 rounded bg-blue-100 flex items-center justify-center">
                  <Upload className="h-5 w-5 text-blue-600" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate">{file.name}</p>
                  <p className="text-xs text-gray-500">{formatFileSize(file.size)}</p>
                </div>
              </div>
              <button
                onClick={() => removeFile(index)}
                className="flex-shrink-0 ml-3 text-red-600 hover:text-red-700"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
          ))}
        </div>
      )}

      {files.length > 0 && (
        <button className="w-full rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
          Upload {files.length} file{files.length > 1 ? 's' : ''}
        </button>
      )}
    </div>
  );
}
```

**Key techniques:**
- `e.preventDefault()` on dragOver and drop prevents browser default
- `Array.from()` converts FileList to array
- File size formatting for user-friendly display
- `accept` attribute limits file types
- Visual feedback during drag (border color change)

### Best Practices Summary (2025)

- **Use React Hook Form + Zod** for validation
- **Show inline errors** as user types
- **Add loading states** on submit
- **Support keyboard navigation**
- **Use floating labels** for cleaner UI
- **Implement auto-save** for long forms
- **Add progress indicators** for multi-step

**Sources:**
- [React Hook Form Documentation](https://react-hook-form.com/)
- [shadcn/ui: Form Components](https://ui.shadcn.com/docs/components/form)
- [Headless UI: Combobox](https://headlessui.com/react/combobox)

---

## 7. COMMERCE & MARKETING PATTERNS

### Overview
Commerce and marketing patterns include pricing tables, testimonials, CTAs, and feature grids. The 2025 trend is social proof, transparency, and comparison tables.

### What Makes a Great Implementation

**Great implementations have:**
- **Clear pricing tiers** with feature comparison
- **Social proof** (testimonials, logos, stats)
- **Strong CTAs** with contrasting colors
- **FAQ accordions** for common objections
- **Trust signals** (security badges, ratings)

**Best-in-class examples:**
- **Stripe Pricing**: Clean comparison table, toggle annual/monthly
- **Linear**: Minimal, transparent pricing
- **Tailwind UI**: Pre-built marketing sections

### Common Mistakes

1. **Hidden pricing** (forces contact sales)
2. **Too many tiers** (> 4 causes paralysis)
3. **Unclear differentiators** between tiers
4. **Fake testimonials** (stock photos)
5. **Weak CTAs** (vague button text)

### Pattern Types & Code Examples

#### 7.1 Pricing Table with Toggle

**Best for**: SaaS, subscription products

```jsx
// Pricing table with annual/monthly toggle
import { useState } from 'react';
import { Check } from 'lucide-react';

export function PricingTable() {
  const [annual, setAnnual] = useState(true);

  const plans = [
    {
      name: 'Starter',
      priceMonthly: 19,
      priceAnnual: 15,
      description: 'Perfect for individuals and small teams',
      features: ['5 projects', '1,000 subscribers', 'Basic analytics', '48-hour support'],
    },
    {
      name: 'Pro',
      priceMonthly: 49,
      priceAnnual: 39,
      popular: true,
      description: 'For growing businesses',
      features: [
        '25 projects',
        '10,000 subscribers',
        'Advanced analytics',
        '24/7 support',
        'Custom integrations',
      ],
    },
    {
      name: 'Enterprise',
      priceMonthly: 99,
      priceAnnual: 79,
      description: 'For large organizations',
      features: [
        'Unlimited projects',
        'Unlimited subscribers',
        'Premium analytics',
        'Dedicated support',
        'Custom contracts',
        'SLA guarantee',
      ],
    },
  ];

  return (
    <div className="py-24 px-6">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold mb-4">Pricing that grows with you</h2>
          <p className="text-xl text-gray-600">
            Choose an affordable plan packed with the best features
          </p>
        </div>

        {/* Toggle */}
        <div className="flex justify-center items-center gap-4 mb-12">
          <span className={`text-sm font-medium ${annual ? 'text-gray-900' : 'text-gray-500'}`}>
            Annual
          </span>
          <button
            onClick={() => setAnnual(!annual)}
            className={`relative inline-flex h-6 w-11 items-center rounded-full transition ${
              annual ? 'bg-blue-600' : 'bg-gray-200'
            }`}
          >
            <span
              className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                annual ? 'translate-x-6' : 'translate-x-1'
              }`}
            />
          </button>
          <span className={`text-sm font-medium ${!annual ? 'text-gray-900' : 'text-gray-500'}`}>
            Monthly
          </span>
          {annual && (
            <span className="text-sm bg-green-100 text-green-700 px-2 py-1 rounded-full font-medium">
              Save 20%
            </span>
          )}
        </div>

        {/* Pricing cards */}
        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`rounded-2xl border p-8 relative ${
                plan.popular
                  ? 'border-blue-500 shadow-xl scale-105 bg-white'
                  : 'border-gray-200 bg-white'
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                  <span className="bg-blue-500 text-white text-sm px-4 py-1 rounded-full font-medium">
                    Most Popular
                  </span>
                </div>
              )}

              <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
              <p className="text-gray-600 text-sm mb-6">{plan.description}</p>

              <div className="mb-6">
                <div className="flex items-baseline">
                  <span className="text-5xl font-bold">
                    ${annual ? plan.priceAnnual : plan.priceMonthly}
                  </span>
                  <span className="text-gray-500 ml-2">/month</span>
                </div>
                {annual && (
                  <p className="text-sm text-gray-500 mt-1">
                    Billed annually (${plan.priceAnnual * 12}/year)
                  </p>
                )}
              </div>

              <ul className="space-y-3 mb-8">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-start gap-3">
                    <Check className="h-5 w-5 text-green-500 flex-shrink-0 mt-0.5" />
                    <span className="text-gray-600 text-sm">{feature}</span>
                  </li>
                ))}
              </ul>

              <button
                className={`w-full rounded-lg py-3 font-semibold transition ${
                  plan.popular
                    ? 'bg-blue-600 text-white hover:bg-blue-700'
                    : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
                }`}
              >
                Get started
              </button>
            </div>
          ))}
        </div>

        {/* Feature comparison table */}
        <div className="mt-16">
          <h3 className="text-2xl font-bold text-center mb-8">Compare features</h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-4 px-4">Feature</th>
                  {plans.map(plan => (
                    <th key={plan.name} className="text-center py-4 px-4">{plan.name}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                <tr className="border-b">
                  <td className="py-4 px-4">Projects</td>
                  <td className="text-center py-4 px-4">5</td>
                  <td className="text-center py-4 px-4">25</td>
                  <td className="text-center py-4 px-4">Unlimited</td>
                </tr>
                <tr className="border-b">
                  <td className="py-4 px-4">API Access</td>
                  <td className="text-center py-4 px-4"><Check className="h-5 w-5 text-green-500 mx-auto" /></td>
                  <td className="text-center py-4 px-4"><Check className="h-5 w-5 text-green-500 mx-auto" /></td>
                  <td className="text-center py-4 px-4"><Check className="h-5 w-5 text-green-500 mx-auto" /></td>
                </tr>
                {/* More rows */}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
```

**Key techniques:**
- Toggle switch for billing period
- `scale-105` makes popular plan stand out
- Absolute positioning for "Most Popular" badge
- Feature comparison table for detailed analysis

#### 7.2 Testimonial Grid

**Best for**: Social proof, case studies

```jsx
// Testimonial grid
import { Star } from 'lucide-react';

export function TestimonialGrid() {
  const testimonials = [
    {
      id: 1,
      quote: "This product changed how we work. The team collaboration features are unmatched.",
      author: "Sarah Johnson",
      role: "CEO at TechCo",
      avatar: "/avatars/sarah.jpg",
      rating: 5,
    },
    {
      id: 2,
      quote: "Best investment we've made this year. ROI was visible within the first month.",
      author: "Michael Chen",
      role: "CTO at StartupX",
      avatar: "/avatars/michael.jpg",
      rating: 5,
    },
    {
      id: 3,
      quote: "The customer support is incredible. They go above and beyond every time.",
      author: "Emily Davis",
      role: "Product Manager at BigCorp",
      avatar: "/avatars/emily.jpg",
      rating: 5,
    },
  ];

  return (
    <div className="py-24 px-6 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold mb-4">Loved by teams worldwide</h2>
          <p className="text-xl text-gray-600">
            Don't just take our word for it
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {testimonials.map((testimonial) => (
            <div key={testimonial.id} className="bg-white rounded-2xl p-8 shadow-sm hover:shadow-md transition">
              {/* Rating */}
              <div className="flex gap-1 mb-4">
                {[...Array(testimonial.rating)].map((_, i) => (
                  <Star key={i} className="h-5 w-5 fill-yellow-400 text-yellow-400" />
                ))}
              </div>

              {/* Quote */}
              <p className="text-gray-700 mb-6 leading-relaxed">
                "{testimonial.quote}"
              </p>

              {/* Author */}
              <div className="flex items-center gap-3">
                <img
                  src={testimonial.avatar}
                  alt={testimonial.author}
                  className="h-12 w-12 rounded-full object-cover"
                />
                <div>
                  <p className="font-semibold text-gray-900">{testimonial.author}</p>
                  <p className="text-sm text-gray-500">{testimonial.role}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Stats row */}
        <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8">
          <div className="text-center">
            <p className="text-4xl font-bold text-gray-900">10k+</p>
            <p className="text-gray-600 mt-2">Active users</p>
          </div>
          <div className="text-center">
            <p className="text-4xl font-bold text-gray-900">4.9/5</p>
            <p className="text-gray-600 mt-2">Average rating</p>
          </div>
          <div className="text-center">
            <p className="text-4xl font-bold text-gray-900">99.9%</p>
            <p className="text-gray-600 mt-2">Uptime</p>
          </div>
          <div className="text-center">
            <p className="text-4xl font-bold text-gray-900">24/7</p>
            <p className="text-gray-600 mt-2">Support</p>
          </div>
        </div>
      </div>
    </div>
  );
}
```

**Advanced: Testimonial Carousel**

```jsx
import { useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

export function TestimonialCarousel({ testimonials }) {
  const [current, setCurrent] = useState(0);

  const next = () => {
    setCurrent((current + 1) % testimonials.length);
  };

  const prev = () => {
    setCurrent((current - 1 + testimonials.length) % testimonials.length);
  };

  return (
    <div className="relative max-w-4xl mx-auto px-12">
      <div className="text-center">
        <p className="text-2xl text-gray-700 leading-relaxed mb-8">
          "{testimonials[current].quote}"
        </p>
        <div className="flex items-center justify-center gap-3">
          <img
            src={testimonials[current].avatar}
            alt={testimonials[current].author}
            className="h-16 w-16 rounded-full"
          />
          <div className="text-left">
            <p className="font-semibold">{testimonials[current].author}</p>
            <p className="text-sm text-gray-500">{testimonials[current].role}</p>
          </div>
        </div>
      </div>

      <button
        onClick={prev}
        className="absolute left-0 top-1/2 -translate-y-1/2 p-2 rounded-full bg-white shadow-lg hover:bg-gray-50"
      >
        <ChevronLeft className="h-6 w-6" />
      </button>

      <button
        onClick={next}
        className="absolute right-0 top-1/2 -translate-y-1/2 p-2 rounded-full bg-white shadow-lg hover:bg-gray-50"
      >
        <ChevronRight className="h-6 w-6" />
      </button>

      {/* Dots indicator */}
      <div className="flex justify-center gap-2 mt-8">
        {testimonials.map((_, idx) => (
          <button
            key={idx}
            onClick={() => setCurrent(idx)}
            className={`h-2 rounded-full transition-all ${
              idx === current ? 'w-8 bg-blue-600' : 'w-2 bg-gray-300'
            }`}
          />
        ))}
      </div>
    </div>
  );
}
```

#### 7.3 FAQ Accordion

**Best for**: Addressing common questions
**Component**: Radix UI Accordion

```jsx
// FAQ Accordion
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Plus } from 'lucide-react';

export function FAQAccordion() {
  const faqs = [
    {
      question: "How does billing work?",
      answer: "We bill monthly or annually based on your preference. You can cancel anytime with no cancellation fees. All plans include a 14-day free trial.",
    },
    {
      question: "Can I change my plan later?",
      answer: "Yes! You can upgrade or downgrade your plan anytime from your account settings. Changes take effect immediately, and we'll prorate the charges.",
    },
    {
      question: "Do you offer refunds?",
      answer: "We offer a 30-day money-back guarantee for all annual plans. If you're not satisfied, contact our support team for a full refund.",
    },
    {
      question: "What payment methods do you accept?",
      answer: "We accept all major credit cards (Visa, Mastercard, American Express), PayPal, and bank transfers for enterprise plans.",
    },
    {
      question: "Is my data secure?",
      answer: "Yes. We use bank-level encryption (AES-256) for data at rest and TLS 1.3 for data in transit. We're SOC 2 Type II certified and GDPR compliant.",
    },
  ];

  return (
    <div className="max-w-3xl mx-auto py-24 px-6">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-bold mb-4">Frequently Asked Questions</h2>
        <p className="text-xl text-gray-600">
          Everything you need to know about our product
        </p>
      </div>

      <Accordion type="single" collapsible className="space-y-4">
        {faqs.map((faq, idx) => (
          <AccordionItem
            key={idx}
            value={`item-${idx}`}
            className="border border-gray-200 rounded-lg px-6 hover:border-gray-300 transition"
          >
            <AccordionTrigger className="text-left font-semibold hover:no-underline py-6">
              <span className="flex-1">{faq.question}</span>
            </AccordionTrigger>
            <AccordionContent className="text-gray-600 pb-6">
              {faq.answer}
            </AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>

      {/* Still have questions CTA */}
      <div className="mt-12 text-center p-8 bg-gray-50 rounded-2xl">
        <h3 className="text-xl font-semibold mb-2">Still have questions?</h3>
        <p className="text-gray-600 mb-6">
          Can't find the answer you're looking for? Our team is here to help.
        </p>
        <button className="rounded-lg bg-blue-600 px-6 py-3 text-white font-semibold hover:bg-blue-700">
          Contact Support
        </button>
      </div>
    </div>
  );
}
```

**Key techniques:**
- Radix UI Accordion for accessibility
- `type="single"` allows only one open at a time
- Hover effects on items
- Follow-up CTA for unanswered questions

#### 7.4 CTA Section

**Best for**: Homepage, landing pages

```jsx
// Call-to-Action Section
export function CTASection() {
  return (
    <div className="py-24 px-6">
      <div className="max-w-7xl mx-auto">
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-blue-600 to-purple-600 p-12 lg:p-16">
          {/* Background pattern */}
          <div className="absolute inset-0 opacity-10">
            <div className="absolute inset-0" style={{
              backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
            }} />
          </div>

          <div className="relative text-center">
            <h2 className="text-4xl lg:text-5xl font-bold text-white mb-4">
              Ready to get started?
            </h2>
            <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
              Join thousands of teams already using our platform to build better products
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="rounded-lg bg-white px-8 py-4 text-blue-600 font-semibold hover:bg-gray-50 shadow-lg">
                Start free trial
              </button>
              <button className="rounded-lg bg-white/10 backdrop-blur px-8 py-4 text-white font-semibold hover:bg-white/20 border border-white/20">
                Schedule demo
              </button>
            </div>

            <p className="text-white/80 text-sm mt-6">
              No credit card required • 14-day free trial • Cancel anytime
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
```

**Variations:**
- Simple text CTA: Minimal, text-focused
- Image + CTA: Product screenshot alongside
- Video CTA: Background video with overlay
- Split CTA: Different actions for different personas

### Best Practices Summary (2025)

- **Show transparent pricing** (no "contact us")
- **Use social proof** (real testimonials, logos)
- **Add comparison tables** for tiers
- **Implement FAQ accordion** for objections
- **Strong CTAs** (action-oriented: "Start free trial")
- **Trust signals** (security badges, ratings)

**Sources:**
- [Tailwind UI: Pricing Sections](https://tailwindcss.com/plus/ui-blocks/marketing/sections/pricing)
- [Stripe Pricing Page](https://stripe.com/pricing)
- [Radix UI: Accordion](https://www.radix-ui.com/primitives/docs/components/accordion)

---

## 8. LOADING & EMPTY STATES

### Overview
Loading states (skeleton, shimmer, spinner) and empty states prevent user confusion and maintain engagement during async operations.

### What Makes a Great Implementation

**Great implementations have:**
- **Skeleton screens** that match final content
- **Shimmer animation** for perceived performance
- **Helpful empty states** with actionable CTAs
- **Progressive loading** (above-fold first)

**Best-in-class examples:**
- **GitHub**: Skeleton screens for lists
- **Linear**: Shimmer loading for inline updates
- **Stripe**: Empty states with helpful illustrations

### Common Mistakes

1. **Generic spinners** instead of skeletons
2. **Blank screens** during load
3. **Empty states without CTA**
4. **Too much animation** (distracting)

### Pattern Types & Code Examples

#### 8.1 Skeleton Loading

```jsx
// Skeleton screen
export function Skeleton({ className }) {
  return (
    <div className={`animate-pulse bg-gray-200 rounded ${className}`} />
  );
}

// Skeleton Card
export function SkeletonCard() {
  return (
    <div className="rounded-lg border border-gray-200 p-6">
      <Skeleton className="h-48 w-full mb-4" />
      <Skeleton className="h-6 w-3/4 mb-2" />
      <Skeleton className="h-4 w-1/2 mb-4" />
      <div className="flex gap-2">
        <Skeleton className="h-10 w-24" />
        <Skeleton className="h-10 w-24" />
      </div>
    </div>
  );
}

// Use during loading
export function ProductList({ loading, products }) {
  if (loading) {
    return (
      <div className="grid md:grid-cols-3 gap-6">
        {[...Array(6)].map((_, i) => (
          <SkeletonCard key={i} />
        ))}
      </div>
    );
  }

  return (
    <div className="grid md:grid-cols-3 gap-6">
      {products.map((product) => (
        <ProductCard key={product.id} {...product} />
      ))}
    </div>
  );
}
```

**Advanced: Shimmer effect**

```jsx
// Shimmer Skeleton with gradient animation
export function ShimmerSkeleton({ className }) {
  return (
    <div className={`relative overflow-hidden bg-gray-200 rounded ${className}`}>
      <div className="absolute inset-0 -translate-x-full animate-[shimmer_2s_infinite] bg-gradient-to-r from-transparent via-white/50 to-transparent" />
    </div>
  );
}

// Add to tailwind.config.js
module.exports = {
  theme: {
    extend: {
      keyframes: {
        shimmer: {
          '100%': { transform: 'translateX(100%)' },
        },
      },
    },
  },
};
```

**Skeleton for different content types:**

```jsx
// Table skeleton
export function TableSkeleton({ rows = 5 }) {
  return (
    <div className="border rounded-lg overflow-hidden">
      <div className="bg-gray-50 p-4 border-b">
        <div className="flex gap-4">
          <Skeleton className="h-4 w-32" />
          <Skeleton className="h-4 w-24" />
          <Skeleton className="h-4 w-28" />
        </div>
      </div>
      {[...Array(rows)].map((_, i) => (
        <div key={i} className="p-4 border-b last:border-b-0">
          <div className="flex gap-4">
            <Skeleton className="h-4 w-32" />
            <Skeleton className="h-4 w-24" />
            <Skeleton className="h-4 w-28" />
          </div>
        </div>
      ))}
    </div>
  );
}

// Text skeleton
export function TextSkeleton({ lines = 3 }) {
  return (
    <div className="space-y-2">
      {[...Array(lines)].map((_, i) => (
        <Skeleton
          key={i}
          className={`h-4 ${
            i === lines - 1 ? 'w-2/3' : 'w-full'
          }`}
        />
      ))}
    </div>
  );
}
```

#### 8.2 Empty State

```jsx
// Empty state with CTA
import { Inbox, Plus } from 'lucide-react';

export function EmptyState({ title, description, action }) {
  return (
    <div className="text-center py-12">
      <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 mb-4">
        <Inbox className="h-8 w-8 text-gray-400" />
      </div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">
        {title || "No items yet"}
      </h3>
      <p className="text-gray-600 mb-6 max-w-sm mx-auto">
        {description || "Get started by creating your first item"}
      </p>
      <button
        onClick={action}
        className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-white font-semibold hover:bg-blue-700"
      >
        <Plus className="h-5 w-5" />
        Create new
      </button>
    </div>
  );
}
```

**Different empty state variations:**

```jsx
// Search empty state
export function SearchEmptyState({ query }) {
  return (
    <div className="text-center py-12">
      <svg className="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">
        No results found for "{query}"
      </h3>
      <p className="text-gray-600">
        Try adjusting your search or filter to find what you're looking for
      </p>
    </div>
  );
}

// Error empty state
export function ErrorEmptyState({ retry }) {
  return (
    <div className="text-center py-12">
      <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-red-100 mb-4">
        <svg className="h-8 w-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">
        Something went wrong
      </h3>
      <p className="text-gray-600 mb-6">
        We couldn't load your data. Please try again.
      </p>
      <button
        onClick={retry}
        className="rounded-lg border border-gray-300 px-4 py-2 text-gray-700 font-medium hover:bg-gray-50"
      >
        Try again
      </button>
    </div>
  );
}
```

#### 8.3 Toast Notifications

**Library**: `sonner` (best toast library for React)

```bash
npm install sonner
```

```jsx
// Toast notifications using sonner
import { Toaster, toast } from 'sonner';

export function ToastExample() {
  return (
    <>
      <Toaster position="top-right" richColors />

      <div className="space-y-2">
        <button
          onClick={() => toast.success('Profile updated successfully!')}
          className="rounded-md bg-green-600 px-4 py-2 text-white"
        >
          Success Toast
        </button>

        <button
          onClick={() => toast.error('Failed to save changes')}
          className="rounded-md bg-red-600 px-4 py-2 text-white"
        >
          Error Toast
        </button>

        <button
          onClick={() => toast.info('New update available')}
          className="rounded-md bg-blue-600 px-4 py-2 text-white"
        >
          Info Toast
        </button>

        <button
          onClick={() => toast.warning('You are running out of storage')}
          className="rounded-md bg-yellow-600 px-4 py-2 text-white"
        >
          Warning Toast
        </button>
      </div>
    </>
  );
}

// Different toast patterns
toast.success('Success message');
toast.error('Error message');
toast.info('Info message');
toast.warning('Warning message');

// Toast with action
toast.error('Failed to save changes', {
  action: {
    label: 'Retry',
    onClick: () => console.log('Retry clicked'),
  },
});

// Promise toast (auto-updates based on promise state)
toast.promise(
  fetch('/api/data').then(res => res.json()),
  {
    loading: 'Loading...',
    success: (data) => `Data loaded: ${data.title}`,
    error: 'Failed to load data',
  }
);

// Custom duration
toast.success('Quick message', { duration: 1000 });

// Persistent toast (must be manually dismissed)
toast.error('Critical error', { duration: Infinity });
```

**Custom toast styling:**

```jsx
// Custom toast with rich content
toast.custom((t) => (
  <div className="bg-white rounded-lg shadow-lg p-4 flex items-start gap-3 max-w-md">
    <div className="flex-shrink-0 w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
      <svg className="h-6 w-6 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
      </svg>
    </div>
    <div className="flex-1">
      <h4 className="font-semibold text-gray-900">New feature available</h4>
      <p className="text-sm text-gray-600 mt-1">
        Check out our new dashboard redesign
      </p>
    </div>
    <button
      onClick={() => toast.dismiss(t)}
      className="flex-shrink-0 text-gray-400 hover:text-gray-600"
    >
      <X className="h-5 w-5" />
    </button>
  </div>
));
```

#### 8.4 Progress Indicators

```jsx
// Linear progress bar
export function ProgressBar({ value, max = 100 }) {
  const percentage = (value / max) * 100;

  return (
    <div className="w-full">
      <div className="flex justify-between text-sm text-gray-600 mb-2">
        <span>Uploading...</span>
        <span>{percentage.toFixed(0)}%</span>
      </div>
      <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
        <div
          className="h-full bg-blue-600 transition-all duration-300"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

// Circular progress
export function CircularProgress({ value, max = 100, size = 120 }) {
  const percentage = (value / max) * 100;
  const circumference = 2 * Math.PI * 54; // radius = 54
  const offset = circumference - (percentage / 100) * circumference;

  return (
    <div className="relative inline-flex items-center justify-center">
      <svg width={size} height={size} className="transform -rotate-90">
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r="54"
          stroke="currentColor"
          strokeWidth="8"
          fill="none"
          className="text-gray-200"
        />
        {/* Progress circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r="54"
          stroke="currentColor"
          strokeWidth="8"
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          className="text-blue-600 transition-all duration-300"
          strokeLinecap="round"
        />
      </svg>
      <div className="absolute text-2xl font-bold text-gray-900">
        {percentage.toFixed(0)}%
      </div>
    </div>
  );
}
```

### Best Practices Summary (2025)

- **Use skeleton screens** over spinners
- **Add shimmer animation** (`animate-pulse`)
- **Show helpful empty states** with CTAs
- **Match skeleton to final layout**
- **Progressive load** above-fold first
- **Use `sonner`** for toast notifications

**Sources:**
- [Flowbite: Skeleton Components](https://flowbite.com/docs/components/skeleton/)
- [Sonner Documentation](https://sonner.emilkowal.ski/)
- [GitHub Primer: Loading States](https://primer.style/components/)

---

## 9. OVERLAY PATTERNS (Modals, Sheets, Popovers)

### Overview
Overlays include modals (dialogs), sheets (drawers), popovers, and command palettes. Radix UI and Headless UI provide accessible primitives.

### What Makes a Great Implementation

**Great implementations have:**
- **Focus trap** inside modal
- **Esc key closes** overlay
- **Click outside closes** (configurable)
- **Smooth animations** (enter/exit)
- **Scroll lock** on body when open
- **Accessible** (ARIA attributes, focus management)

**Best-in-class examples:**
- **shadcn/ui Dialog**: Clean modal with focus trap
- **Radix UI Popover**: Anchor positioning
- **Headless UI Sheet**: Mobile drawer

### Common Mistakes

1. **No focus management**
2. **Body scrolls** when modal open
3. **No close button**
4. **Poor mobile UX**
5. **Missing animations**

### Pattern Types & Code Examples

#### 9.1 Modal/Dialog

```jsx
// Modal using Radix UI / shadcn/ui
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
} from "@/components/ui/dialog";
import { X } from 'lucide-react';

export function ModalExample() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <button className="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
          Open Modal
        </button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Edit Profile</DialogTitle>
          <DialogDescription>
            Make changes to your profile here. Click save when you're done.
          </DialogDescription>
        </DialogHeader>

        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
            <label htmlFor="name" className="text-right text-sm font-medium">
              Name
            </label>
            <input
              id="name"
              className="col-span-3 rounded-md border px-3 py-2"
              defaultValue="John Doe"
            />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <label htmlFor="email" className="text-right text-sm font-medium">
              Email
            </label>
            <input
              id="email"
              type="email"
              className="col-span-3 rounded-md border px-3 py-2"
              defaultValue="john@example.com"
            />
          </div>
        </div>

        <DialogFooter>
          <DialogTrigger asChild>
            <button className="rounded-md border border-gray-300 px-4 py-2 hover:bg-gray-50">
              Cancel
            </button>
          </DialogTrigger>
          <button className="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
            Save changes
          </button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
```

**Confirmation Dialog:**

```jsx
export function ConfirmDialog({ open, onOpenChange, onConfirm, title, description }) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription>{description}</DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <button
            onClick={() => onOpenChange(false)}
            className="rounded-md border px-4 py-2 hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            onClick={() => {
              onConfirm();
              onOpenChange(false);
            }}
            className="rounded-md bg-red-600 px-4 py-2 text-white hover:bg-red-700"
          >
            Delete
          </button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

// Usage
const [showConfirm, setShowConfirm] = useState(false);

<ConfirmDialog
  open={showConfirm}
  onOpenChange={setShowConfirm}
  onConfirm={() => console.log('Deleted')}
  title="Are you sure?"
  description="This action cannot be undone. This will permanently delete your account."
/>
```

#### 9.2 Sheet/Drawer

```jsx
// Sheet (side drawer) using Radix UI / shadcn/ui
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";

export function SheetExample() {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <button className="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
          Open Drawer
        </button>
      </SheetTrigger>
      <SheetContent side="right" className="w-[400px] sm:w-[540px]">
        <SheetHeader>
          <SheetTitle>Filters</SheetTitle>
          <SheetDescription>
            Refine your search with these filters
          </SheetDescription>
        </SheetHeader>

        <div className="py-6 space-y-6">
          {/* Filter options */}
          <div>
            <label className="block text-sm font-medium mb-2">Category</label>
            <select className="w-full rounded-md border px-3 py-2">
              <option>All</option>
              <option>Electronics</option>
              <option>Clothing</option>
              <option>Books</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Price Range</label>
            <div className="flex gap-2">
              <input
                type="number"
                placeholder="Min"
                className="w-full rounded-md border px-3 py-2"
              />
              <input
                type="number"
                placeholder="Max"
                className="w-full rounded-md border px-3 py-2"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Rating</label>
            <div className="space-y-2">
              {[5, 4, 3, 2, 1].map(rating => (
                <label key={rating} className="flex items-center gap-2">
                  <input type="checkbox" className="rounded" />
                  <span className="text-sm">{rating} stars & up</span>
                </label>
              ))}
            </div>
          </div>
        </div>

        <div className="absolute bottom-0 left-0 right-0 border-t bg-white p-4">
          <div className="flex gap-2">
            <button className="flex-1 rounded-md border px-4 py-2 hover:bg-gray-50">
              Clear
            </button>
            <button className="flex-1 rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
              Apply
            </button>
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
}
```

**Sheet sides:**
- `side="right"` - Default, slides from right
- `side="left"` - Slides from left
- `side="top"` - Slides from top
- `side="bottom"` - Slides from bottom (mobile-friendly)

#### 9.3 Popover

```jsx
// Popover using Radix UI / shadcn/ui
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Calendar } from 'lucide-react';

export function PopoverExample() {
  return (
    <Popover>
      <PopoverTrigger asChild>
        <button className="inline-flex items-center gap-2 rounded-md border px-4 py-2 hover:bg-gray-50">
          <Calendar className="h-4 w-4" />
          Select date
        </button>
      </PopoverTrigger>
      <PopoverContent className="w-80" align="start">
        <div className="space-y-4">
          <h4 className="font-medium">Date Range</h4>
          <div className="space-y-2">
            <div>
              <label className="text-sm text-gray-600">From</label>
              <input type="date" className="w-full rounded-md border px-3 py-2 mt-1" />
            </div>
            <div>
              <label className="text-sm text-gray-600">To</label>
              <input type="date" className="w-full rounded-md border px-3 py-2 mt-1" />
            </div>
          </div>
          <button className="w-full rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
            Apply
          </button>
        </div>
      </PopoverContent>
    </Popover>
  );
}
```

**Tooltip (simplified popover):**

```jsx
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

export function TooltipExample() {
  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <button className="rounded-md border px-4 py-2">
            Hover me
          </button>
        </TooltipTrigger>
        <TooltipContent>
          <p>This is a helpful tooltip</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
}
```

#### 9.4 Context Menu

```jsx
// Context Menu (right-click menu)
import {
  ContextMenu,
  ContextMenuContent,
  ContextMenuItem,
  ContextMenuTrigger,
  ContextMenuSeparator,
} from "@/components/ui/context-menu";
import { Copy, Edit, Trash } from 'lucide-react';

export function ContextMenuExample() {
  return (
    <ContextMenu>
      <ContextMenuTrigger className="rounded-lg border p-8 text-center">
        Right click here
      </ContextMenuTrigger>
      <ContextMenuContent className="w-48">
        <ContextMenuItem className="flex items-center gap-2">
          <Edit className="h-4 w-4" />
          Edit
        </ContextMenuItem>
        <ContextMenuItem className="flex items-center gap-2">
          <Copy className="h-4 w-4" />
          Duplicate
        </ContextMenuItem>
        <ContextMenuSeparator />
        <ContextMenuItem className="flex items-center gap-2 text-red-600">
          <Trash className="h-4 w-4" />
          Delete
        </ContextMenuItem>
      </ContextMenuContent>
    </ContextMenu>
  );
}
```

### Best Practices Summary (2025)

- **Use Radix/Headless UI** for accessibility
- **Implement focus trap** in modals
- **Lock body scroll** when modal open
- **Support Esc key** to close
- **Add smooth animations**
- **Use `sonner`** for toasts
- **Provide close button** (X icon)

**Sources:**
- [shadcn/ui: Dialog Component](https://ui.shadcn.com/docs/components/dialog)
- [Radix UI: Dialog](https://www.radix-ui.com/primitives/docs/components/dialog)
- [Radix UI: Popover](https://www.radix-ui.com/primitives/docs/components/popover)

---

## Conclusion & Implementation Checklist

This comprehensive three-part research report covers 9 major UI pattern categories for React + Tailwind CSS applications (2024-2025).

### Quick Reference Summary

**Part 1** (Heroes, Navigation, Cards):
- Editorial, split-screen, video, bento grid heroes
- Command palettes, mega menus, sidebar nav
- Bento grids, masonry, glass cards

**Part 2** (Dashboards, Data, Forms):
- Sidebar+main layouts, dense dashboards
- Responsive tables, TanStack Table, timelines
- Multi-step forms, inline validation, file upload

**Part 3** (Commerce, States, Overlays):
- Pricing tables, testimonials, FAQ accordions
- Skeleton loading, empty states, toast notifications
- Modals, sheets, popovers, context menus

### Essential Libraries (2025)

**Core UI:**
- shadcn/ui (component library)
- Radix UI (accessible primitives)
- Headless UI (unstyled components)
- Tailwind CSS v3.4+

**Data & Forms:**
- React Hook Form (form state)
- Zod (validation)
- TanStack Table v8 (tables)
- TanStack Virtual (virtualization)

**Utilities:**
- cmdk (command palette)
- sonner (toast notifications)
- Heroicons / Lucide React (icons)

### Implementation Priority

**Phase 1 - Foundation:**
1. Set up Tailwind CSS + shadcn/ui
2. Implement basic hero section
3. Add navigation (responsive header)
4. Create card layouts

**Phase 2 - Functionality:**
5. Build dashboard layout
6. Add data tables (TanStack Table)
7. Implement forms with validation
8. Add loading/empty states

**Phase 3 - Polish:**
9. Create pricing/testimonials
10. Add modals/sheets
11. Implement toast notifications
12. Optimize performance

### Final Recommendations

1. **Start with shadcn/ui** - Provides 50+ components built on Radix UI
2. **Use TypeScript** - Better DX and fewer runtime errors
3. **Implement dark mode** - Use Tailwind's dark: prefix
4. **Test accessibility** - Use axe DevTools, test with keyboard
5. **Optimize images** - Use Next.js Image or responsive images
6. **Monitor performance** - Use Lighthouse, Core Web Vitals

### Real-World Examples Referenced

- **Linear.app**: Command palette, keyboard-first, dark mode
- **Stripe.com**: Pricing, forms, clean design
- **Vercel.com**: Dashboard, hero sections, marketing
- **GitHub.com**: Tables, navigation, data display
- **Apple.com**: Bento grids, product showcases
