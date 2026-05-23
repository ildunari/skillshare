---
name: bria-rmbg-background-removal_briaai
description: Load when the user asks to remove, cut out, isolate, mask, or make transparent the background of an image using BRIA RMBG-2.0, especially when they want a high-quality alpha PNG or foreground matte rather than a generative edit.
metadata:
  model: briaai/RMBG-2.0
  local_command: bria-rmbg
---
# BRIA RMBG-2.0 Background Removal

Use this skill when Kosta wants image background removal, foreground cutouts, transparent PNGs, alpha mattes, or batch product/person/object isolation. Prefer this over generative image editing when the goal is a faithful cutout of the original pixels.

## Local command

On the Mac Studio, BRIA RMBG-2.0 is installed as:

```bash
bria-rmbg INPUT_IMAGE -o OUTPUT.png --mask MASK.png --json
```

The implementation lives at `~/.local/share/bria-rmbg2/` with the launcher at `~/.local/bin/bria-rmbg`. It uses `briaai/RMBG-2.0` through Hugging Face Transformers with `trust_remote_code=True`, and auto-selects CUDA, then MPS, then CPU unless `--device` is set.

## Standard workflow

1. Save or locate the input image locally. If the user sent a Telegram image, use the local attachment path from the session/cache.
2. Run:
   ```bash
   bria-rmbg /path/to/input.jpg -o /path/to/input.rmbg.png --mask /path/to/input.mask.png --json
   ```
3. Verify the output exists and has an alpha channel:
   ```bash
   python3 - <<'PY'
   from PIL import Image
   im = Image.open('/path/to/input.rmbg.png')
   print(im.mode, im.size)
   assert im.mode == 'RGBA'
   PY
   ```
4. If replying through Telegram/Hermes, deliver the PNG with `MEDIA:/absolute/path/to/input.rmbg.png`.

## Quality notes

- Output is an RGBA PNG. The optional mask is a grayscale alpha matte.
- For fine hair, glass, or semi-transparent edges, inspect the result visually before claiming success.
- For very large images, keep the original-size output but let the model infer at the default 1024 square input; only change `--size` if quality/performance clearly needs it.
- Use `--device cpu` only if MPS/CUDA fails.

## Access and license constraint

BRIA RMBG-2.0 Hugging Face weights are gated and licensed CC BY-NC 4.0 for non-commercial use unless Kosta has a commercial BRIA agreement. If `bria-rmbg` returns a gated-repo/403 error, the install is present but the active Hugging Face account has not been granted access to `briaai/RMBG-2.0`; send Kosta the access URL rather than debugging the script endlessly: https://huggingface.co/briaai/RMBG-2.0

For commercial/production use, use BRIA's licensed API or confirm a self-hosted commercial license first.
