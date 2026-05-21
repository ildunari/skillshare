#!/usr/bin/env python3
"""
flow_analysis.py — Optical flow utilities for motion classification

Provides:
1. Dense optical flow (Farnebäck) for global motion fields
2. Scroll detection (coherent vertical/horizontal motion)
3. Motion region clustering (find distinct moving elements)
4. Motion energy time series (for segment detection support)
"""

import json
import sys
from typing import Optional

import cv2
import numpy as np


def compute_dense_flow(
    frame_prev: np.ndarray,
    frame_curr: np.ndarray,
) -> np.ndarray:
    """
    Compute dense optical flow between two frames (Farnebäck).

    Returns flow array of shape (H, W, 2) where [:,:,0] = dx, [:,:,1] = dy.
    """
    gray_prev = cv2.cvtColor(frame_prev, cv2.COLOR_BGR2GRAY) if len(frame_prev.shape) == 3 else frame_prev
    gray_curr = cv2.cvtColor(frame_curr, cv2.COLOR_BGR2GRAY) if len(frame_curr.shape) == 3 else frame_curr

    flow = cv2.calcOpticalFlowFarneback(
        gray_prev, gray_curr,
        None,
        pyr_scale=0.5,
        levels=3,
        winsize=15,
        iterations=3,
        poly_n=5,
        poly_sigma=1.2,
        flags=0,
    )
    return flow


def classify_motion(flow: np.ndarray, coherence_threshold: float = 0.7) -> dict:
    """
    Classify the dominant motion in a flow field.

    Returns:
    - type: "scroll_vertical" | "scroll_horizontal" | "mixed" | "static"
    - coherence: how much of the frame moves in the same direction (0..1)
    - dominantDirection: [dx, dy] average motion vector
    - magnitude: average motion magnitude
    """
    mag, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])

    avg_mag = float(np.mean(mag))

    if avg_mag < 0.5:  # effectively static
        return {
            "type": "static",
            "coherence": 0.0,
            "dominantDirection": [0.0, 0.0],
            "magnitude": round(avg_mag, 3),
        }

    # Check coherence: what fraction of pixels move in similar direction?
    dx_mean = float(np.mean(flow[..., 0]))
    dy_mean = float(np.mean(flow[..., 1]))

    # Compute dot product of each pixel's flow with mean direction
    mean_mag = np.sqrt(dx_mean**2 + dy_mean**2)
    if mean_mag < 0.1:
        coherence = 0.0
    else:
        dot = (flow[..., 0] * dx_mean + flow[..., 1] * dy_mean) / (mag * mean_mag + 1e-6)
        coherence = float(np.mean(np.clip(dot, 0, 1)))

    # Classify
    if coherence > coherence_threshold:
        if abs(dy_mean) > abs(dx_mean) * 2:
            motion_type = "scroll_vertical"
        elif abs(dx_mean) > abs(dy_mean) * 2:
            motion_type = "scroll_horizontal"
        else:
            motion_type = "scroll_diagonal"
    else:
        motion_type = "mixed"  # multiple things moving differently

    return {
        "type": motion_type,
        "coherence": round(coherence, 3),
        "dominantDirection": [round(dx_mean, 2), round(dy_mean, 2)],
        "magnitude": round(avg_mag, 3),
    }


def detect_scroll_segments(
    video_path: str,
    start_sec: Optional[float] = None,
    end_sec: Optional[float] = None,
    sample_interval: int = 2,  # analyze every Nth frame
) -> list[dict]:
    """
    Detect scroll vs non-scroll segments in a video.

    Returns list of {startSec, endSec, type, avgCoherence, avgMagnitude, scrollDirection}.
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 60.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    start_frame = int((start_sec or 0) * fps)
    end_frame = int((end_sec or total_frames / fps) * fps)
    end_frame = min(end_frame, total_frames)

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    prev_frame = None
    classifications = []
    frame_idx = start_frame

    while frame_idx < end_frame:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % sample_interval == 0 and prev_frame is not None:
            # Downsample for speed
            small_prev = cv2.resize(prev_frame, (320, 180))
            small_curr = cv2.resize(frame, (320, 180))

            flow = compute_dense_flow(small_prev, small_curr)
            cls = classify_motion(flow)
            cls["frameSec"] = round(frame_idx / fps, 3)
            classifications.append(cls)

        prev_frame = frame.copy()
        frame_idx += 1

    cap.release()

    # Group into segments
    segments = []
    if not classifications:
        return segments

    current_type = classifications[0]["type"]
    seg_start = classifications[0]["frameSec"]
    seg_coherences = [classifications[0]["coherence"]]
    seg_magnitudes = [classifications[0]["magnitude"]]

    for cls in classifications[1:]:
        if cls["type"] == current_type:
            seg_coherences.append(cls["coherence"])
            seg_magnitudes.append(cls["magnitude"])
        else:
            segments.append({
                "startSec": round(seg_start, 3),
                "endSec": round(cls["frameSec"], 3),
                "type": current_type,
                "avgCoherence": round(float(np.mean(seg_coherences)), 3),
                "avgMagnitude": round(float(np.mean(seg_magnitudes)), 3),
            })
            current_type = cls["type"]
            seg_start = cls["frameSec"]
            seg_coherences = [cls["coherence"]]
            seg_magnitudes = [cls["magnitude"]]

    # Final segment
    segments.append({
        "startSec": round(seg_start, 3),
        "endSec": round(classifications[-1]["frameSec"], 3),
        "type": current_type,
        "avgCoherence": round(float(np.mean(seg_coherences)), 3),
        "avgMagnitude": round(float(np.mean(seg_magnitudes)), 3),
    })

    return segments


def estimate_parallax_rates(
    video_path: str,
    regions: list[tuple[int, int, int, int]],  # list of (x,y,w,h) bboxes
    start_sec: float,
    end_sec: float,
) -> list[dict]:
    """
    Estimate parallax rates for specific regions during a scroll segment.

    Rate = region_velocity / global_scroll_velocity.
    rate < 1 = background parallax, rate > 1 = foreground parallax, rate ≈ 1 = normal scroll.

    Returns list of {bbox, rate, confidence} per region.
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 60.0
    start_frame = int(start_sec * fps)
    end_frame = int(end_sec * fps)

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    prev_frame = None
    global_velocities = []
    region_velocities = [[] for _ in regions]

    for i in range(end_frame - start_frame):
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_frame is not None:
            # Global flow
            flow = compute_dense_flow(prev_frame, gray)
            global_dy = float(np.median(flow[..., 1]))
            global_velocities.append(global_dy)

            # Per-region flow
            for j, (rx, ry, rw, rh) in enumerate(regions):
                region_flow = flow[ry:ry+rh, rx:rx+rw]
                if region_flow.size > 0:
                    region_dy = float(np.median(region_flow[..., 1]))
                    region_velocities[j].append(region_dy)

        prev_frame = gray

    cap.release()

    # Compute rates
    global_avg = np.mean(global_velocities) if global_velocities else 0
    results = []

    for j, (bbox, rvels) in enumerate(zip(regions, region_velocities)):
        if rvels and abs(global_avg) > 0.1:
            region_avg = np.mean(rvels)
            rate = region_avg / global_avg
            confidence = min(1.0, len(rvels) / 10)  # more frames = more confident
        else:
            rate = 1.0
            confidence = 0.0

        results.append({
            "bbox": list(bbox),
            "rate": round(float(rate), 3),
            "confidence": round(confidence, 2),
        })

    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python flow_analysis.py <video_path> [start_sec] [end_sec]")
        sys.exit(1)

    video = sys.argv[1]
    start = float(sys.argv[2]) if len(sys.argv) > 2 else None
    end = float(sys.argv[3]) if len(sys.argv) > 3 else None

    segments = detect_scroll_segments(video, start_sec=start, end_sec=end)
    print(json.dumps({"scrollSegments": segments}, indent=2))
