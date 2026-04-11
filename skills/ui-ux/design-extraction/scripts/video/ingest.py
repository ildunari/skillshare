#!/usr/bin/env python3
"""
ingest.py — Video ingestion & normalization

Accepts a video file, normalizes to constant frame rate (CFR),
extracts metadata, and optionally generates low-res proxies.

Output: JSON metadata + normalized video file.
"""

import json
import subprocess
import sys
import shutil
from pathlib import Path
from typing import Optional


def run_ffprobe(video_path: str) -> dict:
    """Extract video metadata via ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format", "-show_streams",
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr}")
    return json.loads(result.stdout)


def get_video_stream(probe: dict) -> Optional[dict]:
    """Find the first video stream in probe data."""
    for stream in probe.get("streams", []):
        if stream.get("codec_type") == "video":
            return stream
    return None


def parse_fps(stream: dict) -> float:
    """Parse FPS from stream data, handling fractional representations."""
    # Try r_frame_rate first (real/average frame rate)
    r_fps = stream.get("r_frame_rate", "0/1")
    if "/" in r_fps:
        num, den = r_fps.split("/")
        fps = float(num) / float(den) if float(den) > 0 else 0
    else:
        fps = float(r_fps)

    # Fall back to avg_frame_rate
    if fps <= 0:
        avg = stream.get("avg_frame_rate", "0/1")
        if "/" in avg:
            num, den = avg.split("/")
            fps = float(num) / float(den) if float(den) > 0 else 0
        else:
            fps = float(avg)

    return fps


def extract_metadata(video_path: str) -> dict:
    """Extract structured metadata from video."""
    probe = run_ffprobe(video_path)
    vstream = get_video_stream(probe)

    if not vstream:
        raise ValueError("No video stream found")

    fps = parse_fps(vstream)
    duration = float(probe.get("format", {}).get("duration", 0))
    width = int(vstream.get("width", 0))
    height = int(vstream.get("height", 0))
    codec = vstream.get("codec_name", "unknown")

    # Detect if VFR (variable frame rate) — heuristic
    r_fps = parse_fps(vstream)
    avg_str = vstream.get("avg_frame_rate", "0/1")
    if "/" in avg_str:
        n, d = avg_str.split("/")
        avg_fps = float(n) / float(d) if float(d) > 0 else 0
    else:
        avg_fps = float(avg_str)

    is_vfr = abs(r_fps - avg_fps) > 1.0 if avg_fps > 0 else False

    return {
        "path": str(video_path),
        "durationSec": round(duration, 3),
        "fps": round(fps, 2),
        "avgFps": round(avg_fps, 2),
        "isVFR": is_vfr,
        "width": width,
        "height": height,
        "codec": codec,
        "rotation": int(vstream.get("tags", {}).get("rotate", 0)),
    }


def normalize_video(
    input_path: str,
    output_path: str,
    target_fps: int = 60,
    max_height: Optional[int] = None,
    strip_audio: bool = True,
) -> str:
    """
    Normalize video to CFR, optionally resize and strip audio.

    Returns path to normalized file.
    """
    cmd = ["ffmpeg", "-y", "-i", input_path]

    # Video filters
    vfilters = [f"fps={target_fps}"]

    if max_height:
        vfilters.append(f"scale=-2:{max_height}")

    # Auto-rotate
    cmd.extend(["-vf", ",".join(vfilters)])

    # Encoding
    cmd.extend(["-c:v", "libx264", "-preset", "fast", "-crf", "18"])

    if strip_audio:
        cmd.extend(["-an"])

    cmd.append(output_path)

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg normalize failed: {result.stderr[:500]}")

    return output_path


def generate_proxy(input_path: str, output_path: str, max_height: int = 480, fps: int = 15) -> str:
    """Generate low-res proxy for cheap Gemini inventory pass."""
    return normalize_video(input_path, output_path, target_fps=fps, max_height=max_height)


def extract_frames(
    video_path: str,
    output_dir: str,
    fps: Optional[int] = None,
    start_sec: Optional[float] = None,
    end_sec: Optional[float] = None,
    fmt: str = "png",
) -> list[str]:
    """
    Extract frames from video segment.

    If fps is None, extracts at native frame rate.
    Returns list of frame file paths.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    cmd = ["ffmpeg", "-y"]

    if start_sec is not None:
        cmd.extend(["-ss", str(start_sec)])
    if end_sec is not None:
        duration = end_sec - (start_sec or 0)
        cmd.extend(["-t", str(duration)])

    cmd.extend(["-i", video_path])

    if fps:
        cmd.extend(["-vf", f"fps={fps}"])

    cmd.append(f"{output_dir}/frame_%06d.{fmt}")

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Frame extraction failed: {result.stderr[:500]}")

    frames = sorted(Path(output_dir).glob(f"*.{fmt}"))
    return [str(f) for f in frames]


def ingest(video_path: str, work_dir: str, target_fps: int = 60) -> dict:
    """
    Full ingestion pipeline.

    Returns metadata dict with paths to normalized video, proxy, and frame dir.
    """
    work = Path(work_dir)
    work.mkdir(parents=True, exist_ok=True)

    # 1. Extract metadata
    meta = extract_metadata(video_path)

    # 2. Normalize to CFR
    norm_path = str(work / "normalized.mp4")
    normalize_video(video_path, norm_path, target_fps=target_fps)
    meta["normalizedPath"] = norm_path
    meta["normalizedFps"] = target_fps

    # 3. Generate proxy for Gemini inventory pass
    proxy_path = str(work / "proxy.mp4")
    generate_proxy(video_path, proxy_path)
    meta["proxyPath"] = proxy_path

    # 4. Save metadata
    meta_path = str(work / "metadata.json")
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)
    meta["metadataPath"] = meta_path

    return meta


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ingest.py <video_path> [work_dir]")
        sys.exit(1)

    video = sys.argv[1]
    workdir = sys.argv[2] if len(sys.argv) > 2 else "./video_work"

    result = ingest(video, workdir)
    print(json.dumps(result, indent=2))
