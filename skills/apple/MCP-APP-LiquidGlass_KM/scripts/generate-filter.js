#!/usr/bin/env node
/**
 * generate-filter.js
 * Generate parametric SVG filter strings for Liquid Glass effects.
 * Usage: node generate-filter.js [--type fractal|lens|animated|specular] [--scale 70] [--freq 0.008]
 *
 * Outputs a ready-to-paste SVG <filter> string.
 */

const args = process.argv.slice(2)
const get = (flag, def) => {
  const i = args.indexOf(flag)
  return i !== -1 ? args[i + 1] : def
}

const type   = get('--type',  'fractal')
const id     = get('--id',    'lg-dist')
const scale  = get('--scale', '70')
const freq   = get('--freq',  '0.008')
const seed   = get('--seed',  '92')
const blur   = get('--blur',  '2')
const octaves = get('--octaves', '2')
const dur    = get('--dur',   '8s')

function fractalFilter() {
  return `<filter id="${id}" x="0%" y="0%" width="100%" height="100%">
  <feTurbulence
    type="fractalNoise"
    baseFrequency="${freq} ${freq}"
    numOctaves="${octaves}"
    seed="${seed}"
    result="noise"
  />
  <feGaussianBlur in="noise" stdDeviation="${blur}" result="blurred"/>
  <feDisplacementMap
    in="SourceGraphic"
    in2="blurred"
    scale="${scale}"
    xChannelSelector="R"
    yChannelSelector="G"
  />
</filter>`
}

function lensFilter() {
  return `<filter id="${id}" x="0%" y="0%" width="100%" height="100%"
        filterUnits="objectBoundingBox">
  <feComponentTransfer in="SourceAlpha" result="alpha">
    <feFuncA type="identity"/>
  </feComponentTransfer>
  <feGaussianBlur in="alpha" stdDeviation="${blur * 25}" result="blur"/>
  <feDisplacementMap
    in="SourceGraphic"
    in2="blur"
    scale="${scale}"
    xChannelSelector="A"
    yChannelSelector="A"
  />
</filter>`
}

function animatedFilter() {
  return `<filter id="${id}" x="0%" y="0%" width="100%" height="100%">
  <feTurbulence
    type="fractalNoise"
    baseFrequency="${freq} ${freq}"
    numOctaves="${octaves}"
    seed="5"
    result="turbulence">
    <animate attributeName="seed" from="1" to="200"
             dur="${dur}" repeatCount="indefinite"/>
  </feTurbulence>
  <feGaussianBlur in="turbulence" stdDeviation="${blur}" result="softMap"/>
  <feDisplacementMap
    in="SourceGraphic"
    in2="softMap"
    scale="${scale}"
    xChannelSelector="R"
    yChannelSelector="G"
  />
</filter>`
}

function specularFilter() {
  return `<filter id="${id}" x="0%" y="0%" width="100%" height="100%"
        filterUnits="objectBoundingBox">
  <feTurbulence
    type="fractalNoise"
    baseFrequency="${freq} ${freq}"
    numOctaves="1"
    seed="5"
    result="turbulence">
    <animate attributeName="seed" from="1" to="200"
             dur="${dur}" repeatCount="indefinite"/>
  </feTurbulence>
  <feComponentTransfer in="turbulence" result="mapped">
    <feFuncR type="gamma" amplitude="1" exponent="10" offset="0.5"/>
    <feFuncG type="gamma" amplitude="0" exponent="1"  offset="0"/>
    <feFuncB type="gamma" amplitude="0" exponent="1"  offset="0.5"/>
  </feComponentTransfer>
  <feGaussianBlur in="turbulence" stdDeviation="${blur}" result="softMap"/>
  <feSpecularLighting
    in="softMap"
    surfaceScale="5"
    specularConstant="1"
    specularExponent="100"
    lighting-color="white"
    result="specLight">
    <fePointLight x="-200" y="-200" z="300"/>
  </feSpecularLighting>
  <feComposite
    in="specLight"
    operator="arithmetic"
    k1="0" k2="1" k3="1" k4="0"
    result="litImage"/>
  <feDisplacementMap
    in="SourceGraphic"
    in2="softMap"
    scale="${scale}"
    xChannelSelector="R"
    yChannelSelector="G"
  />
</filter>`
}

const generators = {
  fractal:  fractalFilter,
  lens:     lensFilter,
  animated: animatedFilter,
  specular: specularFilter,
}

if (!generators[type]) {
  console.error(`Unknown type: ${type}. Choose from: fractal, lens, animated, specular`)
  process.exit(1)
}

const filterXML = generators[type]()
const output = `<!-- Liquid Glass SVG Filter (type=${type}, scale=${scale}, freq=${freq}) -->
<svg style="display:none">
  <defs>
    ${filterXML}
  </defs>
</svg>`

console.log(output)

// Also log the CSS to use it:
console.log(`\n/* CSS to apply this filter: */
.glass-filter {
  backdrop-filter: blur(4px);
  filter: url(#${id}) saturate(120%) brightness(1.15);
  isolation: isolate;
}`)

// ─── Module export for programmatic use ──────────────────────────────────────
if (typeof module !== 'undefined') {
  module.exports = { fractalFilter, lensFilter, animatedFilter, specularFilter }
}
