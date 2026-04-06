// dom-audit-snippets.js
// Use these helpers with Playwright MCP `browser_evaluate`.
// They return small JSON summaries (counts + top examples).

// --- Utility functions ---

function rect(el) {
  const r = el.getBoundingClientRect();
  return { x: r.x, y: r.y, w: r.width, h: r.height, top: r.top, right: r.right, bottom: r.bottom, left: r.left };
}

function area(r) { return Math.max(0, r.w) * Math.max(0, r.h); }

function overlapArea(a, b) {
  const x = Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left));
  const y = Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
  return x * y;
}

function elId(el) {
  const cls = (el.className && typeof el.className === 'string') ? el.className.split(/\s+/).slice(0, 6).join(' ') : null;
  const text = (el.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 60);
  return { tag: el.tagName.toLowerCase(), id: el.id || null, class: cls, text: text || null };
}

function isVisible(el) {
  const cs = getComputedStyle(el);
  if (cs.visibility === 'hidden' || cs.display === 'none' || Number(cs.opacity) === 0) return false;
  const r = el.getBoundingClientRect();
  return r.width >= 4 && r.height >= 4;
}

// --- Tailwind detection ---

function detectTailwindLikely(sampleSize = 200) {
  // Check for Tailwind CSS variables
  const rootStyle = getComputedStyle(document.documentElement);
  let twVars = 0;
  for (let i = 0; i < rootStyle.length; i++) {
    const prop = rootStyle[i];
    if (prop && prop.startsWith('--tw-')) {
      twVars++;
      if (twVars >= 4) break;
    }
  }
  if (twVars >= 4) return { tailwindLikely: true, reason: 'css-vars', twVarCount: twVars };

  // Check for utility class patterns
  const re = /\b(sm:|md:|lg:|xl:|2xl:|space-[xy]-|gap-[xy]-|gap-|max-w-|min-w-|px-|py-|mx-auto|grid|flex)\b/;
  const els = Array.from(document.querySelectorAll('[class]')).slice(0, sampleSize);
  let hits = 0;
  for (const el of els) {
    const cn = el.className;
    if (typeof cn === 'string' && re.test(cn)) hits++;
  }
  return { tailwindLikely: hits >= Math.max(12, Math.floor(els.length * 0.12)), reason: 'class-patterns', classHits: hits, sampled: els.length };
}

const TW_SPACE = [
  { t: '0', px: 0 }, { t: '0.5', px: 2 }, { t: '1', px: 4 }, { t: '1.5', px: 6 },
  { t: '2', px: 8 }, { t: '2.5', px: 10 }, { t: '3', px: 12 }, { t: '3.5', px: 14 },
  { t: '4', px: 16 }, { t: '5', px: 20 }, { t: '6', px: 24 }, { t: '7', px: 28 },
  { t: '8', px: 32 }, { t: '9', px: 36 }, { t: '10', px: 40 }, { t: '12', px: 48 },
  { t: '14', px: 56 }, { t: '16', px: 64 }, { t: '20', px: 80 }, { t: '24', px: 96 },
];

function closestTwSpace(px) {
  const p = Math.max(0, Number(px) || 0);
  let best = TW_SPACE[0];
  let bestErr = Infinity;
  for (const item of TW_SPACE) {
    const err = Math.abs(item.px - p);
    if (err < bestErr) { bestErr = err; best = item; }
  }
  return best;
}

// --- Overflow detection ---

function detectHorizontalOverflow() {
  const doc = document.documentElement;
  const body = document.body;
  const overflow = Math.max(
    doc.scrollWidth - doc.clientWidth,
    body ? (body.scrollWidth - doc.clientWidth) : 0
  );
  return { clientWidth: doc.clientWidth, scrollWidth: doc.scrollWidth, overflowPx: overflow };
}

// Find elements that overflow their own container
function findSelfOverflowingElements(limit = 12) {
  const els = Array.from(document.querySelectorAll('*'))
    .filter(el => {
      if (!isVisible(el)) return false;
      const r = el.getBoundingClientRect();
      if (r.width < 80 || r.height < 18) return false;
      return (el.scrollWidth - el.clientWidth) > 10;
    })
    .slice(0, 400);

  return els.slice(0, limit).map(el => ({
    ...elId(el),
    clientW: el.clientWidth,
    scrollW: el.scrollWidth
  }));
}

// Find elements that extend past the viewport (the actual culprits)
function findOverflowCulprits(limit = 10) {
  const vw = innerWidth;
  const offenders = [];
  for (const el of Array.from(document.querySelectorAll('body *'))) {
    if (!isVisible(el)) continue;
    const r = el.getBoundingClientRect();
    if (r.right > vw + 1 || r.left < -1) {
      offenders.push({
        ...elId(el),
        rect: { left: Math.round(r.left), right: Math.round(r.right), width: Math.round(r.width) },
      });
    }
    if (offenders.length >= limit) break;
  }
  return { vw, offenders };
}

// --- Overlap detection (improved with area calc + parent/child filter) ---

function findOverlaps(maxEls = 60, maxPairs = 18) {
  const candidates = Array.from(document.querySelectorAll('body *'))
    .filter(el => {
      if (!isVisible(el)) return false;
      const r = el.getBoundingClientRect();
      if (r.width < 120 || r.height < 40) return false;
      // Ignore elements fully offscreen
      if (r.bottom < 0 || r.right < 0 || r.top > innerHeight || r.left > innerWidth) return false;
      return true;
    })
    .slice(0, 450);

  const boxes = candidates
    .map(el => ({ el, r: rect(el) }))
    .filter(x => area(x.r) > 5000)
    .sort((a, b) => area(b.r) - area(a.r))
    .slice(0, maxEls);

  const overlaps = [];
  for (let i = 0; i < boxes.length; i++) {
    for (let j = i + 1; j < boxes.length; j++) {
      if (overlaps.length >= maxPairs) break;
      const a = boxes[i], b = boxes[j];
      const oa = overlapArea(a.r, b.r);
      // Ignore tiny overlaps (shadows, hairlines)
      if (oa < 64) continue;
      // Ignore parent/child overlaps (common and usually fine)
      if (a.el.contains(b.el) || b.el.contains(a.el)) continue;
      overlaps.push({
        area: Math.round(oa),
        a: elId(a.el),
        b: elId(b.el)
      });
    }
    if (overlaps.length >= maxPairs) break;
  }
  overlaps.sort((x, y) => y.area - x.area);
  return { scanned: boxes.length, overlapCount: overlaps.length, overlaps };
}

// --- Spacing rhythm + gap heuristics ---

function analyzeVerticalStacks(limit = 10) {
  const parents = Array.from(document.querySelectorAll('main, section, article, div, ul, ol'))
    .filter(el => {
      if (!isVisible(el)) return false;
      const cs = getComputedStyle(el);
      if (!['block', 'flex', 'grid'].includes(cs.display)) return false;
      const kids = Array.from(el.children).filter(isVisible);
      return kids.length >= 4 && kids.length <= 30;
    })
    .slice(0, 250);

  const issues = [];
  for (const p of parents) {
    const kids = Array.from(p.children).filter(isVisible);
    const boxes = kids.map(k => rect(k)).sort((a, b) => a.top - b.top);
    // Check if most children share roughly the same left edge (vertical stack)
    const lefts = boxes.map(b => b.left).sort((a, b) => a - b);
    const leftMedian = lefts[Math.floor(lefts.length / 2)];
    const aligned = boxes.filter(b => Math.abs(b.left - leftMedian) <= 10).length / boxes.length;
    if (aligned < 0.7) continue;

    const gaps = [];
    for (let i = 0; i < boxes.length - 1; i++) {
      const g = boxes[i + 1].top - boxes[i].bottom;
      if (g >= 0 && g <= 120) gaps.push(g);
    }
    if (gaps.length < 3) continue;

    const sorted = gaps.slice().sort((a, b) => a - b);
    const median = sorted[Math.floor(sorted.length / 2)];
    const min = sorted[0], max = sorted[sorted.length - 1];
    if ((max - min) < 10) continue; // already consistent

    const tw = closestTwSpace(median);
    issues.push({
      parent: elId(p),
      gapMedianPx: Math.round(median),
      gapRangePx: [Math.round(min), Math.round(max)],
      tailwindSuggestion: `space-y-${tw.t}`,
    });
    if (issues.length >= limit) break;
  }
  return { stacksChecked: parents.length, inconsistentStacks: issues };
}

function findGaplessFlexOrGrid(limit = 10) {
  const containers = Array.from(document.querySelectorAll('*'))
    .filter(el => {
      if (!isVisible(el)) return false;
      const cs = getComputedStyle(el);
      if (cs.display !== 'flex' && cs.display !== 'grid') return false;
      const kids = Array.from(el.children).filter(isVisible);
      if (kids.length < 3) return false;
      const gap = (parseFloat(cs.columnGap) || 0) + (parseFloat(cs.rowGap) || 0);
      return gap < 2;
    })
    .slice(0, 350);

  const out = [];
  for (const c of containers) {
    const cs = getComputedStyle(c);
    const kids = Array.from(c.children).filter(isVisible).slice(0, 8);
    const boxes = kids.map(k => rect(k));
    let sep = null;
    if (cs.display === 'flex') {
      const flexDir = cs.flexDirection || 'row';
      if (flexDir.includes('row')) {
        boxes.sort((a, b) => a.left - b.left);
        if (boxes.length >= 2) sep = boxes[1].left - boxes[0].right;
      } else {
        boxes.sort((a, b) => a.top - b.top);
        if (boxes.length >= 2) sep = boxes[1].top - boxes[0].bottom;
      }
    } else {
      boxes.sort((a, b) => a.top - b.top);
      if (boxes.length >= 2) sep = boxes[1].top - boxes[0].bottom;
    }
    const suggested = closestTwSpace((sep != null && sep > 2) ? sep : 16);
    out.push({
      container: elId(c),
      display: cs.display,
      approxSeparationPx: (sep == null ? null : Math.round(sep)),
      tailwindSuggestion: `gap-${suggested.t}`,
    });
    if (out.length >= limit) break;
  }
  return { containersChecked: containers.length, gapless: out };
}

// --- Container width heuristics ---

function findTooWideTextBlocks(limit = 10) {
  const vw = document.documentElement.clientWidth || window.innerWidth;
  const nodes = Array.from(document.querySelectorAll('p, li, blockquote, article, section, div'))
    .filter(el => {
      if (!isVisible(el)) return false;
      const txt = (el.textContent || '').trim();
      if (txt.length < 180) return false;
      const r = el.getBoundingClientRect();
      return r.width > Math.min(920, vw * 0.9) && r.width > 520;
    })
    .slice(0, 250);

  const out = [];
  for (const el of nodes) {
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    const fs = parseFloat(cs.fontSize) || 16;
    const ems = r.width / fs;
    if (ems < 40) continue;
    out.push({
      el: elId(el),
      widthPx: Math.round(r.width),
      approxEms: Math.round(ems),
      tailwindSuggestion: 'max-w-prose mx-auto px-4',
    });
    if (out.length >= limit) break;
  }
  return { candidatesChecked: nodes.length, tooWide: out };
}

// --- CTA / tap target signals (with scoring) ---

function parseRGB(str) {
  const m = String(str || '').match(/rgba?\(([^)]+)\)/);
  if (!m) return null;
  const parts = m[1].split(',').map(s => parseFloat(s.trim()));
  return { r: parts[0], g: parts[1], b: parts[2], a: (parts.length >= 4 ? parts[3] : 1) };
}

function relLuminance(rgb) {
  const srgb = [rgb.r, rgb.g, rgb.b].map(v => (v / 255));
  const lin = srgb.map(c => (c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4)));
  return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2];
}

function contrastRatio(fg, bg) {
  const L1 = relLuminance(fg);
  const L2 = relLuminance(bg);
  const hi = Math.max(L1, L2), lo = Math.min(L1, L2);
  return (hi + 0.05) / (lo + 0.05);
}

// Score how "CTA-like" an element appears
function ctaScore(el) {
  const t = (el.innerText || el.getAttribute("aria-label") || "").toLowerCase();
  let s = 0;
  if (/(get started|sign up|start|try|book|request|contact|buy|purchase|subscribe|join|add to cart|checkout)/i.test(t)) s += 4;
  if (/(cta|primary|button|btn)/i.test(el.className || "")) s += 2;
  const cs = getComputedStyle(el);
  if (parseInt(cs.fontWeight) >= 600) s += 1;
  if (cs.textTransform === "uppercase") s += 1;
  return s;
}

function findWeakCTAs(limit = 8) {
  const cands = Array.from(document.querySelectorAll('a, button, [role="button"], input[type="button"], input[type="submit"]'))
    .filter(el => {
      if (!isVisible(el)) return false;
      const r = el.getBoundingClientRect();
      // Ignore tiny or offscreen
      if (r.width < 44 || r.height < 28) return false;
      if (r.bottom < 0 || r.top > innerHeight) return false;
      return true;
    })
    .slice(0, 250);

  const out = [];
  for (const el of cands) {
    const cs = getComputedStyle(el);
    const fg = parseRGB(cs.color);
    const bg = parseRGB(cs.backgroundColor);
    if (!fg || !bg) continue;
    const ratio = contrastRatio(fg, bg);
    const r = el.getBoundingClientRect();
    const score = ctaScore(el);
    
    // Flag if low contrast OR small tap target
    if (ratio < 2.5 || r.height < 34) {
      out.push({
        el: elId(el),
        score,
        contrast: Number(ratio.toFixed(2)),
        heightPx: Math.round(r.height),
        issue: ratio < 2.5 ? 'low-contrast' : 'small-tap-target'
      });
    }
    if (out.length >= limit) break;
  }
  // Sort by CTA score descending (most important CTAs first)
  out.sort((a, b) => b.score - a.score);
  return { scanned: cands.length, weakSignals: out };
}

// --- Container spacing rhythm (manual selector version) ---

function containerSpacingRhythm(selector) {
  const root = document.querySelector(selector);
  if (!root) return { error: `No element for selector: ${selector}` };
  const kids = Array.from(root.children).filter(isVisible);
  const gaps = [];
  for (let i = 0; i < kids.length - 1; i++) {
    const a = kids[i].getBoundingClientRect();
    const b = kids[i + 1].getBoundingClientRect();
    gaps.push(Math.round(b.top - a.bottom));
  }
  const tw = gaps.length > 0 ? closestTwSpace(gaps.reduce((a, b) => a + b, 0) / gaps.length) : null;
  return { 
    selector, 
    childCount: kids.length, 
    gaps,
    tailwindSuggestion: tw ? `space-y-${tw.t}` : null
  };
}

// --- One-call summary for sweep mode triage ---

function auditSummary() {
  const tw = detectTailwindLikely();
  const overflow = detectHorizontalOverflow();
  const selfOverflow = (overflow.overflowPx > 0) ? findSelfOverflowingElements(8) : [];
  const culprits = (overflow.overflowPx > 0) ? findOverflowCulprits(8) : { vw: overflow.clientWidth, offenders: [] };
  const overlaps = findOverlaps(55, 10);
  const stacks = analyzeVerticalStacks(6);
  const gapless = findGaplessFlexOrGrid(6);
  const wideText = findTooWideTextBlocks(6);
  const ctas = findWeakCTAs(6);

  return {
    tailwind: tw,
    overflow: {
      ...overflow,
      selfOverflowing: selfOverflow,
      culprits: culprits.offenders,
    },
    overlaps,
    spacing: {
      inconsistentStacks: stacks.inconsistentStacks,
      gaplessContainers: gapless.gapless,
      tooWideText: wideText.tooWide,
    },
    ctaSignals: ctas.weakSignals,
  };
}
