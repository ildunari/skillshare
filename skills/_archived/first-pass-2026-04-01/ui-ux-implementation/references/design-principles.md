# Research-backed design principles (with citations)

This file preserves the core research-backed philosophy from the original UI/UX critic agent — and translates it into implementation-relevant guidance.

## Core stance

1. **Research over opinions**
   - Tie recommendations to observed user behavior and usability research.
2. **Distinctive over generic**
   - Avoid template aesthetics unless the user explicitly wants that.
3. **Practical over aspirational**
   - Prefer changes that improve comprehension, navigation, and task success *now*.
4. **Accessibility as a baseline**
   - WCAG AA is not optional; it’s table stakes.

---

## Attention & scanning patterns

### F-pattern scanning (eyetracking)

Users often scan text-heavy pages in an F-shaped pattern: top line(s) first, then down the left side. This holds across time and still appears on mobile.  
Sources:
- NN/g original: https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content-discovered/
- NN/g updated explainer: https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/

Related: people **scan more than they read**. In NN/g studies, **79%** of users scanned new pages and only **16%** read word-by-word.
Source: https://www.nngroup.com/articles/how-users-read-on-the-web/


**Implementation implications**
- Put the most important content first.
- Use meaningful headings and subheadings (scannability).
- Don’t bury critical info on the far right of wide layouts.

### Horizontal attention leans left

Eyetracking research shows people spend disproportionately more viewing time on the left side of the screen (classic ~69/30 split in earlier research; updated study found an even stronger skew on wider screens).  
Sources:
- NN/g updated: https://www.nngroup.com/articles/horizontal-attention-leans-left/
- NN/g original: https://www.nngroup.com/articles/horizontal-attention-original-research/

**Implementation implications**
- Keep primary navigation and key content left-aligned.
- Avoid center-aligning body text.
- Use the right rail for secondary content.

---

## Banner blindness (ad-like elements get ignored)

Users ignore elements that resemble ads, are near ads, or appear in “ad locations.”  
Sources:
- NN/g: https://www.nngroup.com/articles/banner-blindness-old-and-new-findings/
- Related classic term: Benway & Lane (1998) coined “banner blindness” in early web studies (commonly cited origin).

**Implementation implications**
- Don’t style critical content like an ad (animated promos, banner-like blocks).
- Avoid placing primary CTAs in banner-like regions at the top with “promo” styling.
- Use clear, content-like hierarchy for real actions.

---

## Recognition over recall (Jakob’s Law / conventions)

Users prefer interfaces that work like the ones they already know. Breaking conventions costs learning time and increases error risk.  
Source:
- NN/g video: https://www.nngroup.com/videos/jakobs-law-internet-ux/
- Related overview: https://www.nngroup.com/articles/end-of-web-design/

**Implementation implications**
- Keep core patterns conventional (nav, forms, search).
- “Creative” belongs in typography/layout texture — not in hiding navigation.

---

## Interaction laws you can actually use

### Fitts’s Law (target size + distance)

Bigger, closer targets are faster and less error-prone to click/tap.  
Source:
- NN/g: https://www.nngroup.com/articles/fitts-law/

**Implementation implications**
- Ensure touch targets are large enough and spaced.
- Group related actions close to what they affect.

### Hick’s Law (choice overload)

More choices → slower decisions. Combine with grouping and progressive disclosure.  
Source:
- NN/g: https://www.nngroup.com/videos/hicks-law-long-menus/

**Implementation implications**
- Don’t dump 12 filter toggles into one panel with equal weight.
- Group, prioritize, and progressively disclose.

---

## Mobile behavior (thumb reach + ergonomics)

Field research on how people hold phones commonly reports ~49% one-handed use and varied grips.  
Sources:
- Steven Hoober on UXmatters: https://www.uxmatters.com/mt/archives/2013/02/how-do-users-really-hold-mobile-devices.php
- Smashing Magazine summary: https://www.smashingmagazine.com/2016/09/the-thumb-zone-designing-for-mobile-users/

**Implementation implications**
- Put primary actions in easy reach on mobile when appropriate.
- Don’t rely on top-corner-only controls for critical actions.


### Mobile-first is data-driven

Global usage data frequently shows **mobile around (or above) ~50% of web traffic worldwide**, meaning a “desktop-first then shrink” approach is risky for many products.
Source (interactive chart): https://gs.statcounter.com/platform-market-share/desktop-mobile/worldwide/

---

## Carousels & auto-rotating UI (usually bad)

Auto-forwarding carousels reduce visibility and control; users can’t read before content changes; it also harms accessibility.  
Source:
- NN/g: https://www.nngroup.com/articles/auto-forwarding/

**Implementation implications**
- Avoid auto-rotating content for critical messaging.
- If you must use a carousel, make it user-controlled and accessible.

---

## First impressions happen fast (credibility risk)

Research suggests visual appeal judgments can occur extremely quickly (often cited ~50ms).  
Source:
- Lindgaard et al. (2006), DOI: 10.1080/01449290500330448

**Implementation implications**
- Typography, spacing, and color coherence matter immediately.
- A “generic template” can signal low credibility/effort in seconds.

---

# Practical heuristics to apply during implementation

## Layout & hierarchy

- Left-align paragraphs and navigation; reserve center-align for short headlines only.
- Use big hierarchy jumps (size/weight) to show structure.
- Keep line length comfortable (avoid ultra-wide paragraphs).
- Use whitespace to separate “chapters” of the page.

## Forms

- Labels visible (don’t rely on placeholder).
- Inline errors with clear text + `aria-describedby`.
- Don’t validate on every keystroke unless it’s helpful and non-annoying.

## Motion

- Animate for feedback/state transitions, not for decoration.
- Keep UI transitions fast (usually 150–250ms).
- Respect `prefers-reduced-motion`.

See: [animations.md](animations.md)

---

# Anti-patterns to call out (and replace)

## Generic SaaS aesthetic
- Default fonts (Inter/Roboto)
- Three-column “features” grids everywhere
- Purple gradients + blob backgrounds
- Cards as the only layout tool

## Trendy-but-bad
- Glassmorphism everywhere (readability + contrast issues)
- Parallax for no reason (motion sickness + perf)
- Tiny body text (accessibility failure)
- Neumorphism (low-contrast nightmare)

## Accessibility sins
- No keyboard support
- No focus indicator
- Color as the only indicator
- Touch targets too small

---

# Evidence-based critique format (use in audits)

```md
**[Issue Name]**
- What’s wrong:
- Why it matters:
- Research backing: (URL/principle)
- Fix: (specific, with code)
- Priority: Critical/High/Medium/Low
```
