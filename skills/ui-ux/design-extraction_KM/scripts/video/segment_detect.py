#!/usr/bin/env python3
"""
segment_detect.py — Motion segment detection

Detects time windows where UI motion occurs using:
1. Frame differencing (pixel change energy)
2. Motion energy thresholds
3. Scene cut detection (for route transitions)

Output: List of segments with start/end times and motion energy profile.
"""

import json
import sys
from pathlib import Path
from typing import Optional

import cv2
import numpy as np


def compute_frame_diff_energy(
    video_path: str,
    fps: Optional[float] = None,
    roi: Optional[tuple[int, int, int, int]] = None,  # x, y, w, h
) -> list[dict]:
    """
    Compute per-frame difference energy (mean absolute pixel change).

    Returns list of {frame, timeSec, energy, isSceneCut}.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")

    if fps is None:
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    prev_gray = None
    frame_idx = 0
    results = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Apply ROI if specified
        if roi:
            x, y, w, h = roi
            frame = frame[y:y+h, x:x+w]

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)  # reduce noise

        if prev_gray is not None:
            diff = cv2.absdiff(gray, prev_gray)
            energy = float(np.mean(diff))

            # Scene cut heuristic: very high energy spike
            is_scene_cut = energy > 40.0  # threshold tunable

            results.append({
                "frame": frame_idx,
                "timeSec": round(frame_idx / fps, 4),
                "energy": round(energy, 3),
                "isSceneCut": is_scene_cut,
            })

        prev_gray = gray
        frame_idx += 1

    cap.release()
    return results


def find_motion_segments(
    energy_profile: list[dict],
    motion_threshold: float = 2.0,
    min_segment_frames: int = 3,
    merge_gap_frames: int = 5,
    fps: float = 60.0,
) -> list[dict]:
    """
    Find contiguous segments where motion energy exceeds threshold.

    Returns list of {startFrame, endFrame, startSec, endSec, peakEnergy, meanEnergy, isSceneCut}.
    """
    segments = []
    in_segment = False
    seg_start = 0
    seg_peak = 0
    seg_energies = []
    has_scene_cut = False

    for entry in energy_profile:
        above = entry["energy"] > motion_threshold

        if above and not in_segment:
            in_segment = True
            seg_start = entry["frame"]
            seg_peak = entry["energy"]
            seg_energies = [entry["energy"]]
            has_scene_cut = entry["isSceneCut"]
        elif above and in_segment:
            seg_peak = max(seg_peak, entry["energy"])
            seg_energies.append(entry["energy"])
            if entry["isSceneCut"]:
                has_scene_cut = True
        elif not above and in_segment:
            # Check if this is just a brief dip (merge gap)
            # Look ahead
            lookahead = [
                e for e in energy_profile
                if entry["frame"] < e["frame"] <= entry["frame"] + merge_gap_frames
                and e["energy"] > motion_threshold
            ]
            if lookahead:
                seg_energies.append(entry["energy"])
                continue

            # End segment
            seg_end = entry["frame"]
            if (seg_end - seg_start) >= min_segment_frames:
                segments.append({
                    "startFrame": seg_start,
                    "endFrame": seg_end,
                    "startSec": round(seg_start / fps, 3),
                    "endSec": round(seg_end / fps, 3),
                    "durationMs": round((seg_end - seg_start) / fps * 1000, 1),
                    "peakEnergy": round(seg_peak, 3),
                    "meanEnergy": round(float(np.mean(seg_energies)), 3),
                    "containsSceneCut": has_scene_cut,
                })
            in_segment = False

    # Handle segment at end of video
    if in_segment:
        last = energy_profile[-1]
        seg_end = last["frame"]
        if (seg_end - seg_start) >= min_segment_frames:
            segments.append({
                "startFrame": seg_start,
                "endFrame": seg_end,
                "startSec": round(seg_start / fps, 3),
                "endSec": round(seg_end / fps, 3),
                "durationMs": round((seg_end - seg_start) / fps * 1000, 1),
                "peakEnergy": round(seg_peak, 3),
                "meanEnergy": round(float(np.mean(seg_energies)), 3),
                "containsSceneCut": has_scene_cut,
            })

    return segments


def detect_motion_regions(
    video_path: str,
    start_sec: float,
    end_sec: float,
    min_area: int = 100,
) -> list[dict]:
    """
    Within a segment, find distinct moving regions (candidate animated elements).

    Returns list of {bbox: [x,y,w,h], centroid: [cx,cy], area, frameCount}.
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 60.0

    start_frame = int(start_sec * fps)
    end_frame = int(end_sec * fps)

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # Accumulate motion across segment
    prev_gray = None
    motion_accum = None

    for i in range(end_frame - start_frame):
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        if prev_gray is not None:
            diff = cv2.absdiff(gray, prev_gray)
            if motion_accum is None:
                motion_accum = diff.astype(np.float32)
            else:
                motion_accum += diff.astype(np.float32)

        prev_gray = gray

    cap.release()

    if motion_accum is None:
        return []

    # Threshold accumulated motion
    motion_norm = cv2.normalize(motion_accum, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    _, thresh = cv2.threshold(motion_norm, 30, 255, cv2.THRESH_BINARY)

    # Morphological cleanup
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))

    # Find contours → moving regions
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    regions = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < min_area:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cx, cy = x + w // 2, y + h // 2
        regions.append({
            "bbox": [x, y, w, h],
            "centroid": [cx, cy],
            "area": int(area),
        })

    # Sort by area descending
    regions.sort(key=lambda r: r["area"], reverse=True)
    return regions


def detect_segments(video_path: str, motion_threshold: float = 2.0) -> dict:
    """
    Full segment detection pipeline.

    Returns {metadata, energyProfile, segments, summary}.
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 60.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    energy = compute_frame_diff_energy(video_path, fps=fps)
    segments = find_motion_segments(energy, motion_threshold=motion_threshold, fps=fps)

    return {
        "videoPath": video_path,
        "fps": fps,
        "totalFrames": total_frames,
        "durationSec": round(total_frames / fps, 3),
        "motionThreshold": motion_threshold,
        "segmentCount": len(segments),
        "segments": segments,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python segment_detect.py <video_path> [threshold]")
        sys.exit(1)

    video = sys.argv[1]
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0

    result = detect_segments(video, motion_threshold=threshold)
    print(json.dumps(result, indent=2))
