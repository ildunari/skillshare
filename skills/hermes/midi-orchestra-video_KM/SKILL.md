---
name: midi-orchestra-video
description: Compose original orchestral music in code and render it as a Synthesia-style falling-notes video with per-instrument visual layers. Proven pipeline on the Mac Studio (fluidsynth + FluidR3 GM + PIL + ffmpeg).
---

# MIDI → orchestra audio → visualizer video

Proven 2026-06-11 (Kosta rated the first output "actually beautiful"). Reference scripts: `~/.hermes/assets/melody-pipeline/` (compose3.py = 3-min 11-instrument piece, visualize3.py = full layer set, fable-prompt.md = reusable prompt).

## Pipeline

1. **Compose as data**: explicit `(beat, pitch, dur, velocity)` lists per part. Use midiutil (in a venv; `PIP_USER=0 pip install midiutil pillow`). Sustain pedal CC64≈90 on piano tracks. Design a real arc — sections with distinct texture (solo intro → engine → lift → climax → quiet bridge → rebuild → bigger climax → major-key resolution → fade) beats random notes by miles.
2. **Render audio**: `fluidsynth -ni -g 0.55 -r 44100 -F out.wav ~/.hermes/assets/soundfonts/FluidR3_GM.sf2 song.mid` (brew fluidsynth; soundfont 148MB, RIFF-verified). Then `loudnorm=I=-16:TP=-1.5`.
3. **Visualize**: PIL frames 1280×720 @30fps from the same note data; ffmpeg mux `-c:v libx264 -pix_fmt yuv420p -crf 18-19 -c:a aac`.

## GM programs that sound good in FluidR3

piano 0, strings 48, cello 42, French horn 60, flute 73, harp 46, celesta 8 (music-box feel), pizzicato 45, choir aahs 52, timpani 47. Avoid MIDI channel 9 (GM drums).

## Visual language (per instrument, all driven by actual note activity)

Piano = falling gold (RH) / teal (LH) bars onto an 88-key keyboard + key lights + spark particles on landing. Strings = violet aurora ribbons. Cello = crimson glow above the keys. Horn = amber halo. Flute = cyan comets. Harp = falling pale-gold shimmer streaks. Celesta = twinkling 4-point stars. Pizzicato = expanding green rings (x mapped from pitch). Choir = pearly wash over the upper sky. Timpani = white flash + decaying camera shake (vel ≥80 only).

## Hard-won gotchas

- **Mix levels**: GM channel volume CC7 — orchestra needs 95–105 vs piano's default 127-ish, or it's inaudible behind the piano (Kosta heard "only two instruments" at CC7 76–88). Velocity caps per part too.
- **Ending**: never leave a dead tail. Compose a real cadence (full-orchestra swell + timpani roll), then fade audio and video TOGETHER: `VIDEO_T = frames/30`; audio fade `st = VIDEO_T - lead_in - fade_dur` so silence lands exactly at the video's fade-to-black; mux with `adelay=<lead_in_ms>` + `-shortest`. Verify: last 0.5s max_volume < -50dB, final frame brightness ≈ 0.
- **Lead-in**: give the first note ~2s of empty fall (shift visualizer events +2s, adelay=2000 the audio).
- **Verification that matters**: per-section RMS profile (does the energy arc match the design?), spot-read 2-3 frames at structurally different moments, ffprobe duration, non-silent audio.
- **Fast renderer** (`render_fast.py` in the pipeline dir): precompute ALL particle systems as deterministic spawn lists (seeded `random.Random(base+index)` per event — sparks/comets/rain/twinkles/rings become pure functions of t; the shake decay and comet spawn cadence are precomputed timelines), then `multiprocessing.Pool.imap` frames across cores and pipe raw RGB into ffmpeg stdin. Benchmark on the M2 Max (12 cores): 5,496 frames in **15s (~355 fps)** vs 12 min single-threaded+PNGs — ~46×. Keep `libx264 -crf 19` (3-min ≈ 25MB); `h264_videotoolbox` at 7000k is faster (430fps) but bloats to 127MB — over Telegram's 50MB cap. Workers rebuild static layers + spawn lists at import (deterministic seeds → identical state under macOS spawn).
- **Revision loop**: spawn a review-lane Agent on the composition source with the listener's complaints + a do-not-touch list; ask for a concrete plan (exact notes/beats/patterns, no code). Proven fixes: arpeggio pattern VARIANTS per section instead of one looping figure; climax-II as development (diminution + passing tones early, longer peaks late, written-out exhale); transition bars that thin to near-silence before big arrivals; staggered/re-attacked string pads; keep flute ≤G6 and answering in gaps, never doubling the melody 8va.
- 3-min 720p30 mp4 ≈ 25MB — under Telegram's 50MB cap.
