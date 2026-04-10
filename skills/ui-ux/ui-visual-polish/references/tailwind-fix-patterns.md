# Tailwind Fix Patterns

Opinionated "good default" moves when the project is Tailwind-heavy. Prefer adjusting existing utilities over adding new custom CSS.

## 1) Vertical rhythm: stop sprinkling random margins

### Smell
- A vertical stack feels uneven
- Children have a grab-bag of `mt-*`/`mb-*` values
- Spacing breaks between mobile/desktop

### Fix
Put spacing on the **parent**, not each child.

- Simple column stack: `space-y-4` (or `space-y-6`) on parent, remove child margins
- Responsive rhythm: `space-y-6 md:space-y-8` for big sections, `space-y-3 md:space-y-4` for dense card content
- If children are conditionally rendered: use `flex flex-col gap-4` instead

## 2) Rows and grids: use `gap-*` not margin hacks

### Smell
- A row of cards has inconsistent spacing
- A flex row uses child `mr-*`/`ml-*` values
- Things collapse at certain breakpoints

### Fix
- Flex row: `flex flex-wrap gap-4` (or `gap-6`)
- Grid: `grid gap-4 sm:grid-cols-2 lg:grid-cols-3`
- Different horizontal vs vertical: `gap-x-6 gap-y-8`

## 3) Container widths + gutters

### Smell
- Content runs edge-to-edge with no gutters
- Text blocks are too wide
- Sections aren't aligned

### Fix
- Wide app/landing: `mx-auto max-w-7xl px-4 sm:px-6 lg:px-8`
- Medium content: `mx-auto max-w-5xl px-4 sm:px-6`
- Text-heavy blocks: `mx-auto max-w-prose px-4`
- If using Tailwind `container`: add `container mx-auto px-4 sm:px-6 lg:px-8`

## 4) Card spacing

### Smell
- Cards feel cramped
- Card padding varies across a list

### Fix
- Normalize padding: `p-6` for primary cards, `p-4` for compact
- Internal rhythm: `space-y-3` or `gap-3`
- Common skeleton: `rounded-xl border border-slate-200 bg-white p-6 shadow-sm`

## 5) Mobile overflow

### Smell
- Horizontal scroll on mobile
- Long text/code forces layout wider
- Flex children refuse to shrink

### Fix
- On flex children with text: `min-w-0`
- Long text: `break-words` or `break-all` (sparingly)
- Images/SVG: `max-w-full h-auto`

## 6) CTA "pop" without random color changes

Prefer **size + whitespace + hierarchy** first:
- More room: `mt-6` on the group, or increase surrounding `space-y-*`
- Larger tap target: `px-5 py-3` instead of tiny paddings
- Subtle depth: `shadow-sm` / `shadow-md`

Safe button default: `inline-flex items-center justify-center rounded-md px-5 py-3 font-medium shadow-sm`

Only adjust colors if it truly blends; prefer existing brand hues.

## 7) Spacing token guide

- Tight UI: `gap-3` / `space-y-3` / `p-4`
- Standard UI: `gap-4` / `space-y-4` / `p-6`
- Airy landing: `gap-6` / `space-y-6` / `py-16` sections

Pick a rhythm and apply it consistently within each region.
