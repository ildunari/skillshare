# Seedance image-to-video hero backgrounds — 2026-05-07

Session pattern: Kosta supplied a still image and asked to turn it into a website hero/poster video using Seedance. The useful class-level lesson is prompt shape plus credit-cost reporting for fal Seedance calls.

## Local run pattern

Use image-to-video when the user provides an image. Upload the local image to fal storage, then call:

```python
import fal_client

image_url = fal_client.upload_file('/abs/path/to/image.jpg')
result = fal_client.subscribe(
    'bytedance/seedance-2.0/image-to-video',
    arguments={
        'prompt': prompt,
        'image_url': image_url,
        'resolution': '720p',
        'duration': '5',
        'aspect_ratio': '16:9',
        'generate_audio': False,
    },
    with_logs=True,
)
video_url = result['video']['url']
seed = result.get('seed')
```

If the current shell lacks `FAL_KEY`, load Hermes env files explicitly before importing/calling fal:

```python
from dotenv import load_dotenv
load_dotenv('/Users/Kosta/.hermes/profiles/gpt/.env', override=False)
load_dotenv('/Users/Kosta/.hermes/.env', override=False)
```

Download the returned MP4 and deliver local files as `MEDIA:/abs/path/file.mp4` on Telegram.

## Hero-background prompt recipe

For website backgrounds, do not prompt like a normal action scene. Prompt it as a restrained “living poster.” Preserve the core composition and leave negative space for headline text.

Effective ingredients:

- “cinematic website hero background video from the provided image”
- “very slow, elegant, loopable motion”
- “hand/object remains anatomically stable and almost still” when the source contains hands/faces/bodies
- subtle motion only in mist, particles, light bloom, parallax, or clouds
- “slow cinematic push-in with tiny parallax, no cuts”
- “keep composition hero-friendly with empty space for typography”
- explicit avoid list: warped fingers, extra fingers, changing pose, flicker, jitter, text, logos, watermarks, UI, busy clutter

Example prompt core from the session:

```text
Create a cinematic website hero background video from the provided image. Preserve the luminous hand emerging from pastel mist. The hand should remain anatomically stable and almost still, with only subtle natural floating/parallax drift. Soft mist and silk-like light trails gently flow across the palm. A warm glow blooms quietly in the palm, then settles. Fine particles shimmer faintly in the light. Background clouds breathe slowly. Slow cinematic push-in, no cuts, no fast movement, no zoom jump. Keep composition hero-friendly with empty space for typography. Output should feel like a calm, luminous, seamless living poster.

Avoid warped fingers, extra fingers, changing hand pose, deformed anatomy, flicker, jitter, abrupt brightness changes, text, logos, watermarks, UI, extra hands, over-saturated neon, and busy clutter.
```

## Cost reporting

When Kosta asks what a Seedance render cost, answer directly from duration × current fal price rather than hand-waving. For the 2026-05-07 render, fal public/model-provider snippets showed Seedance 2.0 image-to-video at about `$0.3024/sec`; a 5-second 720p image-to-video render cost about `$1.512` (`5 * 0.3024`), i.e. roughly `$1.51`.

Always label pricing as current/checked-at-time; fal model pricing may change. Prefer checking fal/model docs or provider listing again before quoting future costs.
