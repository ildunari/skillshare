# Product, ecommerce, and editing workflows

## Contents

- [Editing rule](#editing-rule)
- [Product extraction](#product-extraction)
- [Background replacement](#background-replacement)
- [Product ad from reference](#product-ad-from-reference)
- [Virtual clothing try-on](#virtual-clothing-try-on)
- [Interior design swap](#interior-design-swap)
- [Object removal](#object-removal)
- [Sketch to render](#sketch-to-render)
- [Style transfer](#style-transfer)
- [Lighting or weather transform](#lighting-or-weather-transform)
- [Person into scene](#person-into-scene)
- [Before-and-after comparison](#before-and-after-comparison)

## Editing rule

Every edit prompt should say what to preserve, what to change, and how to integrate the change. Most bad edits happen because the prompt focuses only on the new object and forgets to lock identity, geometry, lighting, labels, or camera angle.

## Product extraction

Template:

```text
Extract the product from the input image and place it on a plain opaque white background.
Preserve product geometry, proportions, label text, and packaging details exactly.
Output: centered product, crisp silhouette, no halos or fringing, subtle realistic contact shadow only.
Do not restyle, redesign, relabel, or add new elements.
```

## Background replacement

Template:

```text
Replace only the background with [new background].
Preserve the subject/product exactly: shape, labels, colors, lighting direction, camera angle, and proportions.
Integrate with realistic contact shadows, reflections, and color temperature.
Do not alter the subject, add logos, add text, or change framing.
```

## Product ad from reference

Template:

```text
Use the provided product image as the exact product reference.
Create a photorealistic ad scene for [use case/audience].
Preserve product geometry and label legibility exactly.
Scene: [scene].
Exact ad copy: "[copy]".
Typography: [style], clean and readable.
Constraints: no extra logos, no product redesign, no watermark, no additional claims.
```

## Virtual clothing try-on

Template:

```text
Dress the person in the provided clothing reference.
Preserve the person's face, identity, skin tone, body shape, pose, expression, hairstyle, camera angle, and background.
Change only the clothing. Fit the garment naturally to the body and pose with realistic folds, occlusion, shadows, and color temperature.
Do not add accessories, text, logos, or change the person's body.
```

## Interior design swap

Template:

```text
In this room photo, replace only [object] with [new object/style].
Preserve camera angle, room geometry, windows, walls, floor, lighting, shadows, and all surrounding objects.
Make the new object photorealistic with correct scale, contact shadows, and material texture.
Do not redesign the room or add extra decor.
```

## Object removal

Template:

```text
Remove [object/person] from the image.
Fill the area naturally using the surrounding background, lighting, texture, and perspective.
Preserve all other objects, people, camera angle, colors, and image quality.
Do not add new elements or change the scene.
```

## Sketch to render

Template:

```text
Turn this sketch into a photorealistic [object/scene] render.
Preserve the exact layout, proportions, perspective, and main design intent of the sketch.
Choose realistic materials, lighting, and environment consistent with the sketch.
Do not add new elements, text, logos, or change the design silhouette.
```

## Style transfer

Template:

```text
Use the reference image only for visual style: palette, texture, brushwork, line quality, lighting mood, and composition rhythm.
Generate a new original image of [new subject].
Preserve no characters, logos, text, or protected distinctive elements from the reference.
Constraints: [background/framing/no extra elements].
```

## Lighting or weather transform

Template:

```text
Transform the scene to [time/weather/season].
Change only environmental conditions: lighting direction, shadows, atmosphere, precipitation, sky, and ground wetness/snow.
Preserve identity, geometry, camera angle, object placement, and composition.
Make it look like the same photo taken under new conditions.
```

## Person into scene

Template:

```text
Place the person from the reference image into [new scene].
Preserve the person's facial identity, body proportions, hairstyle, and key features.
Adapt wardrobe/pose only as requested: [change].
Scene integration: realistic scale, lighting, shadows, color temperature, and camera perspective.
Avoid movie-poster exaggeration unless requested. Do not add text or change identity.
```

## Before-and-after comparison

Template:

```text
Create a split-screen before-and-after comparison for [edit/concept].
Left side: original-style state [description].
Right side: transformed state [description].
Use matching camera angle, scale, and lighting so the change is easy to compare.
Add only these labels: "Before" and "After".
Constraints: no extra text, no misleading changes outside the intended difference.
```
