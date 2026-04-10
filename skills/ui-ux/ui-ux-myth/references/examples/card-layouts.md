# Card layouts (how to avoid “three generic cards”)

Cards aren’t evil — but “card grid everywhere” is a template smell.

## 1) Use asymmetric grids by default

```html
<section class="Section">
  <div class="Container Grid Grid--split">
    <header class="Stack">
      <p class="MetaLabel">What you get</p>
      <h2 class="SectionTitle">A UI system that scales without feeling generic.</h2>
      <p class="SectionSubtitle">Primitives, patterns, and tokens that make shipping fast and coherent.</p>
    </header>

    <div class="Stack">
      <article class="Card">
        <h3>Tokens-first</h3>
        <p>Colors, spacing, and typography are roles — not random hex codes.</p>
      </article>
      <article class="Card">
        <h3>Accessible by default</h3>
        <p>Focus, labels, keyboard navigation, reduced motion.</p>
      </article>
    </div>
  </div>
</section>
```

```css
.Grid { display: grid; gap: 1.5rem; }
@media (min-width: 900px) { .Grid--split { grid-template-columns: 1.6fr 1fr; } }
```

This reads more “designed” than 3 equal columns.

## 2) Replace “feature cards” with a ranked list

Lists are often more scannable and honest.

```html
<ol class="FeatureList">
  <li>
    <h3>Fast onboarding</h3>
    <p>Get to first value in minutes, not days.</p>
  </li>
  <li>
    <h3>Clear states</h3>
    <p>Loading, empty, error, and success are designed — not afterthoughts.</p>
  </li>
  <li>
    <h3>Mobile ergonomics</h3>
    <p>Primary actions stay in reach; touch targets are sized.</p>
  </li>
</ol>
```

## 3) Use “callout panels” instead of cards

A single strong panel can outperform 6 weak cards.

```html
<aside class="Callout">
  <p class="MetaLabel">Proof</p>
  <p class="Callout__quote">“We shipped the redesign in 3 days and support tickets dropped.”</p>
  <p class="Callout__meta">— Support lead</p>
</aside>
```

## 4) Card styling rules (if you use them)

- Use one dominant surface + one accent. Don’t rainbow.
- Increase padding before adding shadows.
- Use borders + subtle depth before giant shadows.
- Use real hierarchy inside the card (title, supporting text, actions).
