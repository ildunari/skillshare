# Visual Heuristics Cheat Sheet

These are *signals* to guide iteration, not "tests".

## Triage: what to fix first

1. **Overlap/collisions** (text on text, fixed header covering content)
2. **Horizontal overflow** (mobile killer)
3. **Containers/gutters** (edge-to-edge content, sections don't align)
4. **Inconsistent spacing rhythm** (cards/stacks don't match)
5. **Weak hierarchy / CTA** (nothing leads the eye)

## Tailwind-aware cues

If you see utilities like `sm:`, `md:`, `space-y-*`, `gap-*`, `max-w-*`, `px-*`, `mx-auto`, assume Tailwind.

Default Tailwind posture:
- Fix spacing by editing **parent utilities** (`space-y-*`, `gap-*`) instead of sprinkling random child margins.
- Fix alignment/width with **container wrappers** (`mx-auto max-w-* px-*`) instead of hard-coded widths.
- Reuse the existing spacing scale in that file/section.

See `tailwind-fix-patterns.md` for concrete recipes.

## Layout red flags (high priority)

### Overlap / collisions
**Smells**
- Text sits on top of text
- Cards overlap each other
- Sticky header covers the first section
- Dropdowns/menus clip behind other sections

**Common fixes**
- Remove negative margins
- Avoid absolute positioning for layout
- Add top padding to account for fixed headers
- Fix stacking context (`z-index`) only if needed

### Horizontal overflow (mobile killer)
**Smells**
- Any horizontal scroll on mobile
- A URL/code/token forces a line wider than viewport
- Images/SVGs exceed container width
- Flex children refuse to shrink

**Common fixes**
- `min-width: 0` on flex children (Tailwind: `min-w-0`)
- Allow wrapping: `flex-wrap`
- Long text: `overflow-wrap:anywhere` (Tailwind: `break-words` / `break-all` sparingly)
- Constrain media: `max-width: 100%` (Tailwind: `max-w-full h-auto`)

## Spacing rhythm

### Inconsistent stack gaps
**Smells**
- Headings too close to body text in one section, too far in another
- Cards in a grid have different internal spacing
- Vertical rhythm changes randomly at breakpoints

**Common fixes**
- Put spacing on the parent:
  - Tailwind: `space-y-4` / `gap-4` and remove child margins
  - CSS: normalize `margin-block` and use `gap` where possible
- Normalize card padding:
  - Tailwind: `p-4` vs `p-6` (pick one per card type)
  - CSS: consistent `padding` token

## Containers & alignment

### No gutters / edge-to-edge content
**Smells**
- Text touches the viewport edge on mobile
- Sections aren't aligned to a common left/right gutter

**Common fixes**
- Tailwind: `mx-auto max-w-7xl px-4 sm:px-6 lg:px-8`
- If using Tailwind `container`: add `mx-auto px-4 sm:px-6 lg:px-8`
- CSS: set `max-width` + `margin: 0 auto` + consistent horizontal padding

### Too-wide text blocks
**Smells**
- Paragraphs span the whole screen on desktop
- Hard to scan (no focal width)

**Common fixes**
- Tailwind: `max-w-prose mx-auto` (or `max-w-2xl`/`max-w-3xl`) + gutters
- CSS: `max-width: 65ch; margin-inline:auto; padding-inline: ...;`

## Hierarchy & CTA emphasis

### Heading doesn't lead
**Smells**
- H1 looks like body text
- Multiple competing "bold" things

**Common fixes**
- Increase heading size/weight; tune line-height
- Add breathing room above/below the heading
- Reduce emphasis of secondary text (weight/opacity)

### CTA doesn't pop
Prefer "composition" fixes first:
- More whitespace around the CTA
- Larger tap target / padding
- Subtle depth (`shadow-sm`/`shadow-md`)

Only change colors if it truly blends into the background, and reuse existing palette tokens.

## Responsiveness quick checks

- Tap targets: buttons/links should be ≥40px tall
- Rows that should wrap do wrap on mobile
- Images and tables scale down without horizontal scroll
