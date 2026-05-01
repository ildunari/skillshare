# User question templates

Use questions for low-confidence or high-impact decisions. Batch related questions by slide, table, or document section so the user makes one coherent decision instead of answering many isolated prompts.

## General pattern

```text
I found [issue] at [location]. It matters because [plain accessibility impact]. My recommended fix is [specific change]. Approve? [Y/n/describe]
```

Include the default if silence matters:

```text
If you want me to decide, I will [default policy].
```

## Decorative vs informative image

```text
This image at [location] appears decorative because [reason: repeats adjacent text, divider, background texture, logo already named nearby]. Mark it decorative? [Y/n/describe]
If you want me to decide, I will keep short alt text unless the image clearly adds no meaning.
```

```text
This image seems informative because it conveys [data/action/identity/process]. I recommend alt text: “[alt]”. Use this? [Y/n/edit]
```

## Reading order

```text
On slide [n], the visual order appears to be [title → chart → note → callout], but the current object order is [title → callout → chart → note]. I recommend reordering to [order]. Apply this reading order? [Y/n/describe]
```

## Heading structure

```text
Paragraph [location] looks like a section heading for “[text]” and sits between Heading [n] and lower-level content. I recommend setting it to Heading [level] so screen reader navigation matches the visible outline. Apply? [Y/n]
```

Ask when the text might be a visual label rather than a heading:

```text
“[text]” is styled like a heading, but it may be a card label rather than a document section. Should it become a navigable heading or stay normal text? [heading/normal]
```

## Contrast

```text
The [text/object] at [location] has contrast [ratio]:1 against [background], below the [threshold]:1 target. The least disruptive fix is [change], which keeps [brand/theme constraint]. Apply? [Y/n/describe]
```

## Complex or layout table

```text
Table [location] appears to be used for layout rather than data because [evidence: no headers, borderless two-column prose, images beside text]. Flattening it into normal reading flow would improve accessibility but changes structure. Flatten, keep as table, or defer? [flatten/keep/defer]
```

```text
Table [location] is a data table with a clear header row: [headers]. I recommend marking row 1 as the header and preserving the table. Apply? [Y/n]
```

## Merged cells

```text
Merged cells at [location] may confuse header associations. They seem to mean [grouping/total/category]. Split them, keep them, or defer? [split/keep/defer]
```

## Floating object / wrap

```text
The floating object at [location] is read far from the paragraph it illustrates. I recommend setting it inline after “[nearby text]”. Apply? [Y/n]
```

```text
This floating object appears intentional as a side callout/watermark. I recommend preserving the float and only adjusting reading order. Apply? [Y/n]
```

## Link text

```text
The link text “[current]” is ambiguous. The destination/context indicates “[purpose]”. I recommend replacing it with “[new text]”. Apply? [Y/n/edit]
```

## Slide title

```text
Slide [n] needs a unique title for navigation. Based on the visible content, I recommend “[title]”. Use this title? [Y/n/edit]
```
