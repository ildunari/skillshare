# CodePen Demo Code — Liquid Glass

## Table of contents

- [Demo 1: Apple Liquid Glass Dock + Music Player](#demo-1-apple-liquid-glass-dock--music-player)
- [Demo 2: Apple Liquid Glass UI 2025](#demo-2-apple-liquid-glass-ui-2025-inline-player-variant)
- [Demo 3: Animated Liquid Glass](#demo-3-animated-liquid-glass-seed-animation)
- [Demo 4: Parallax Glass Cards](#demo-4-parallax-glass-cards)

---

## Demo 1: Apple Liquid Glass Dock + Music Player
- Author: wprod
- URL: https://codepen.io/wprod/pen/raVpwJL
- Description: macOS Dock-style glass nav, music player, icon row. Uses alpha-based lens filter.

### HTML
```html
<!-- Music Player Card -->
<div class="container container--mobile">
  <div class="glass-container glass-container--rounded glass-container--large">
    <div class="glass-filter"></div>
    <div class="glass-overlay"></div>
    <div class="glass-specular"></div>
    <div class="glass-content">
      <div class="player">
        <div class="player__thumb">
          <img class="player__img"
            src="https://images.unsplash.com/photo-1619983081593-e2ba5b543168?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wzMjM4NDZ8MHwxfHJhbmRvbXx8fHx8fHx8fDE3NDk1NzAwNDV8&ixlib=rb-4.1.0&q=80&w=400" alt="">
          <div class="player__legend">
            <h3 class="player__legend__title">All Of Me</h3>
            <span class="player__legend__sub-title">Nao</span>
          </div>
        </div>
        <div class="player__controls">
          <svg viewBox="0 0 448 512" width="24">
            <path fill="black" d="M424.4 214.7L72.4 6.6C43.8-10.3 0 6.1 0 47.9V464c0 37.5 40.7 60.1 72.4 41.3l352-208c31.4-18.5 31.5-64.1 0-82.6z"/>
          </svg>
          <svg viewBox="0 0 448 512" width="24">
            <path fill="black" d="M424.4 214.7L72.4 6.6C43.8-10.3 0 6.1 0 47.9V464c0 37.5 40.7 60.1 72.4 41.3l352-208c31.4-18.5 31.5-64.1 0-82.6z"/>
          </svg>
          <svg viewBox="0 0 448 512" width="24">
            <path fill="black" d="M424.4 214.7L72.4 6.6C43.8-10.3 0 6.1 0 47.9V464c0 37.5 40.7 60.1 72.4 41.3l352-208c31.4-18.5 31.5-64.1 0-82.6z"/>
          </svg>
        </div>
      </div>
    </div>
  </div>

  <!-- Bottom Nav Bar -->
  <div class="container container--mobile container--inline">
    <div class="glass-container glass-container--rounded glass-container--medium">
      <div class="glass-filter"></div>
      <div class="glass-overlay"></div>
      <div class="glass-specular"></div>
      <div class="glass-content">
        <div class="glass-item glass-item--active">
          <svg viewBox="0 0 576 512" width="40" title="home">
            <path d="M280.37 148.26L96 300.11V464a16 16 0 0 0 16 16l112.06-.29a16 16 0 0 0 15.92-16V368a16 16 0 0 1 16-16h64a16 16 0 0 1 16 16v95.64a16 16 0 0 0 16 16.05L464 480a16 16 0 0 0 16-16V300L295.67 148.26a12.19 12.19 0 0 0-15.3 0zM571.6 251.47L488 182.56V44.05a12 12 0 0 0-12-12h-56a12 12 0 0 0-12 12v72.61L318.47 43a48 48 0 0 0-61 0L4.34 251.47a12 12 0 0 0-1.6 16.9l25.5 31A12 12 0 0 0 45.15 301l235.22-193.74a12.19 12.19 0 0 1 15.3 0L530.9 301a12 12 0 0 0 16.9-1.6l25.5-31a12 12 0 0 0-1.7-16.93z"/>
          </svg>
          Home
        </div>
        <div class="glass-item">
          <!-- ... more nav items ... -->
        </div>
      </div>
    </div>
    <!-- Search button pill -->
    <div class="glass-container glass-container--rounded glass-container--small">
      <div class="glass-filter"></div>
      <div class="glass-overlay"></div>
      <div class="glass-specular"></div>
      <div class="glass-content glass-content--alone">
        <div class="glass-item">
          <svg viewBox="0 0 512 512" width="40" title="search">
            <path d="M505 442.7L405.3 343c-4.5-4.5-10.6-7-17-7H372c27.6-35.3 44-79.7 44-128C416 93.1 322.9 0 208 0S0 93.1 0 208s93.1 208 208 208c48.3 0 92.7-16.4 128-44v16.3c0 6.4 2.5 12.5 7 17l99.7 99.7c9.4 9.4 24.6 9.4 33.9 0l28.3-28.3c9.4-9.4 9.4-24.6.1-34zM208 336c-70.7 0-128-57.2-128-128 0-70.7 57.2-128 128-128 70.7 0 128 57.2 128 128 0 70.7-57.2 128-128 128z"/>
          </svg>
          Search
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Icon Dock Row -->
<div class="container">
  <div class="glass-container">
    <div class="glass-filter"></div>
    <div class="glass-overlay"></div>
    <div class="glass-specular"></div>
    <div class="glass-content">
      <a class="glass-content__link" href="#">
        <img src="https://assets.codepen.io/923404/finder.png" alt="Finder"/>
      </a>
      <a class="glass-content__link" href="#">
        <img src="https://assets.codepen.io/923404/map.png" alt="Maps"/>
      </a>
      <a class="glass-content__link" href="#">
        <img src="https://assets.codepen.io/923404/messages.png" alt="Messages"/>
      </a>
      <a class="glass-content__link" href="#">
        <img src="https://assets.codepen.io/923404/safari.png" alt="Safari"/>
      </a>
      <a class="glass-content__link" href="#">
        <img src="https://assets.codepen.io/923404/books.png" alt="Books"/>
      </a>
    </div>
    <!-- SVG lens filter -->
    <svg xmlns="http://www.w3.org/2000/svg" style="display:none">
      <filter id="lensFilter" x="0%" y="0%" width="100%" height="100%"
              filterUnits="objectBoundingBox">
        <feComponentTransfer in="SourceAlpha" result="alpha">
          <feFuncA type="identity"/>
        </feComponentTransfer>
        <feGaussianBlur in="alpha" stdDeviation="50" result="blur"/>
        <feDisplacementMap in="SourceGraphic" in2="blur"
          scale="50" xChannelSelector="A" yChannelSelector="A"/>
      </filter>
    </svg>
  </div>
</div>
```

### CSS
```css
:root {
  --lg-bg-color:  rgba(255,255,255,0.25);
  --lg-highlight: rgba(255,255,255,0.75);
  --lg-text:      #ffffff;
  --lg-red:       #fb4268;
  --lg-grey:      #444739;
}

body {
  margin: 0;
  padding: 2rem 0;
  min-height: calc(100vh - 4rem);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-family: sans-serif;
  background: url("https://images.unsplash.com/photo-1588943211346-0908a1fb0b01?crop=entropy&cs=srgb&fm=jpg&ixid=M3wzMjM4NDZ8MHwxfHJhbmRvbXx8fHx8fHx8fDE3NDk1MzU4MDV8&ixlib=rb-4.1.0&q=85") center/cover;
  animation: bg-move 5s ease-in-out infinite alternate;
}

@keyframes bg-move {
  from { background-position: center center; }
  to   { background-position: center top; }
}

.container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}
.container--mobile  { min-width: 32rem; }
.container--small   { max-width: 10rem; margin: 5rem 1rem 1rem; }
.container--small svg { fill: white; }
.container--inline  { display: flex; flex-direction: row; }

.glass-container {
  position: relative;
  display: flex;
  align-items: center;
  background: transparent;
  border-radius: 2rem;
  overflow: hidden;
  flex: 1 1 auto;
  box-shadow: 0 6px 6px rgba(0,0,0,0.2), 0 0 20px rgba(0,0,0,0.1);
  color: var(--lg-text);
  transition: all 0.4s cubic-bezier(0.175,0.885,0.32,2.2);
}
.glass-container--rounded { border-radius: 3rem; }
.glass-container--large   { flex: 1 1 auto; }
.glass-container--medium  { flex: 1 1 auto; }
.glass-container--small   { flex: 0 1 auto; }

.glass-filter,
.glass-overlay,
.glass-specular {
  position: absolute;
  inset: 0;
  border-radius: inherit;
}

.glass-filter {
  z-index: 0;
  backdrop-filter: blur(4px);
  filter: url(#lensFilter) saturate(120%) brightness(1.15);
}

.glass-overlay {
  z-index: 1;
  background: var(--lg-bg-color);
}

.glass-specular {
  z-index: 2;
  box-shadow:
    inset 1px 1px 0 var(--lg-highlight),
    inset 0 0 5px var(--lg-highlight);
}

.glass-content {
  position: relative;
  z-index: 3;
  display: flex;
  flex: 1 1 auto;
  align-items: center;
  justify-content: space-around;
  padding: 12px 28px;
  gap: 1rem;
  flex-wrap: wrap;
}

.glass-content__link {
  margin-bottom: -1px;
  margin-top: 6px;
  transition: transform 0.2s ease-out;
}
.glass-content__link img { width: 78px; }
.glass-content__link:hover  { transform: scale(1.1); }
.glass-content__link:active { transform: scale(0.95); }

.glass-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  color: var(--lg-grey);
  transition: color 0.3s ease;
  cursor: pointer;
}
.glass-item svg {
  fill: var(--lg-grey);
  height: 50px;
  margin-bottom: 0.25rem;
  filter: drop-shadow(0 0 3px rgba(255,255,255,0.25));
  transition: transform 0.25s ease-out;
}
.glass-item svg:hover  { transform: scale(1.1); }
.glass-item svg:active { transform: scale(0.95); }

.glass-item--active {
  background: rgba(0,0,0,0.25);
  color: var(--lg-red);
  margin: -8px -40px;
  padding: 0.5rem 2.5rem;
  border-radius: 3rem;
}
.glass-item--active svg { fill: var(--lg-red); }
```

---

## Demo 2: Apple Liquid Glass UI 2025 (inline player variant)
- Author: samarkandiy (fork of wprod)
- URL: https://codepen.io/samarkandiy/pen/MYwQwZZ
- Description: Inline music player with fractal-noise distortion filter variant.

**Key difference from Demo 1:** Uses `#lg-dist` (fractal noise turbulence) instead of alpha lens filter.

### SVG Filter (Fractal Noise Variant)
```html
<svg style="display:none">
  <filter id="lg-dist" x="0%" y="0%" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.008 0.008"
      numOctaves="2" seed="92" result="noise"/>
    <feGaussianBlur in="noise" stdDeviation="2" result="blurred"/>
    <feDisplacementMap in="SourceGraphic" in2="blurred"
      scale="70" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
</svg>
```

### CSS Delta from Demo 1
```css
/* Override filter reference */
.glass-filter {
  backdrop-filter: blur(0px); /* Intentional: no additional blur, SVG handles it */
  filter: url(#lg-dist);
  isolation: isolate;
}

/* Inline player layout */
.container--inline { flex-direction: row; }
.glass-content--inline {
  padding: 0.25rem 2rem 0.25rem 0.75rem;
  flex: 1 1 auto;
  justify-content: space-between;
}
```

---

## Demo 3: Animated Liquid Glass (seed animation)
**Technique:** Animated `seed` attribute on `feTurbulence` for organic fluid motion.

```html
<svg style="display:none">
  <filter id="lg-animated" x="0%" y="0%" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.01 0.01"
      numOctaves="1" seed="5" result="turbulence">
      <!-- Animate seed 1→200 over 8s for continuous fluid movement -->
      <animate attributeName="seed" from="1" to="200"
               dur="8s" repeatCount="indefinite"/>
    </feTurbulence>
    <feGaussianBlur in="turbulence" stdDeviation="3" result="softMap"/>
    <feDisplacementMap in="SourceGraphic" in2="softMap"
      scale="150" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
</svg>
```

---

## Demo 4: Parallax Glass Cards
Source: https://forum.blocsapp.com/t/playing-with-codepen-liquid-glass/26202

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Fixed Glass Cards with Parallax</title>
  <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    html { scroll-behavior:smooth; }
    body {
      min-height: 200vh;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #000;
      overflow-x: hidden;
      position: relative;
    }
    .parallax-bg {
      position: absolute;
      top: 0; left: 0;
      width: 100%; height: 200%;
      z-index: -2;
      background-image: url('https://images.unsplash.com/photo-1539635278303-d4002c07eae3?crop=entropy&cs=srgb&fm=jpg&q=85');
      background-size: cover;
      background-position: center top;
      transform: translateY(0);
      transition: transform 0.1s linear;
    }
    .fixed-cards {
      position: sticky;
      top: 10%;
      z-index: 2;
      display: flex;
      justify-content: center;
      align-items: flex-start;
      padding: 2rem 1rem;
    }
    .container {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(17rem, 1fr));
      gap: 1.5rem;
      max-width: 1200px;
      width: 100%;
    }
    .glass {
      background: rgba(255,255,255,0.15);
      backdrop-filter: blur(10px) saturate(180%);
      border: 1px solid rgba(255,255,255,0.3);
      border-radius: 2rem;
      padding: 1.5rem;
      box-shadow: 0 8px 32px rgba(31,38,135,0.2);
      height: 350px;
      transition: all 0.4s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .glass:hover {
      transform: scale(1.05);
      box-shadow: 0 12px 36px rgba(31,38,135,0.3);
    }
    .btn-glass {
      padding: 0.75rem 1.5rem;
      border-radius: 0.75rem;
      background: rgba(255,255,255,0.15);
      color: white;
      border: 1px solid rgba(255,255,255,0.3);
      backdrop-filter: blur(10px);
      cursor: pointer;
      transition: all 0.3s ease;
      font-weight: 500;
    }
    .btn-glass:hover { transform: scale(1.05); background: rgba(255,255,255,0.25); }
    .card-title    { font-size:1.4rem; font-weight:600; color:white; }
    .card-subtitle { font-size:1rem; color:rgba(255,255,255,0.8); }
    .card-content  { color:white; font-size:0.95rem; line-height:1.5; }
  </style>
</head>
<body>
  <div class="parallax-bg" id="parallax-bg"></div>
  <div class="fixed-cards">
    <div class="container">
      <div class="glass">
        <div>
          <h3 class="card-title">Today's Hits</h3>
          <p class="card-subtitle">Apple Music</p>
        </div>
        <div class="card-content">
          <p>Fresh songs, updated daily.</p>
          <button class="btn-glass">Play Now</button>
        </div>
      </div>
      <!-- Add more cards as needed -->
    </div>
  </div>
  <script>
    window.addEventListener("scroll", () => {
      const scrollY = window.scrollY
      document.getElementById("parallax-bg").style.transform =
        `translateY(${scrollY * 0.3}px)`
    })
  </script>
</body>
</html>
```
