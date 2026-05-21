#!/usr/bin/env python3
"""
track_element.py — Element tracking across video frames

Tracks an element (by initial bbox or feature points) across a video segment.
Outputs per-frame position, scale, and opacity proxy measurements.

Methods:
1. Template matching (robust for UI elements with stable appearance)
2. Feature point tracking (Lucas-Kanade optical flow)
3. Bbox re-detection via contour matching (fallback)
"""

import json
import sys
from pathlib import Path
from typing import Optional

import cv2
import numpy as np


def track_template(
    video_path: str,
    bbox: tuple[int, int, int, int],  # x, y, w, h in first frame
    start_sec: float,
    end_sec: float,
    fps: Optional[float] = None,
) -> list[dict]:
    """
    Track element via template matching.

    Good for: UI elements that translate without changing appearance much.
    Returns per-frame {frame, timeSec, x, y, w, h, confidence, centerX, centerY}.
    """
    cap = cv2.VideoCapture(video_path)
    if fps is None:
        fps = cap.get(cv2.CAP_PROP_FPS) or 60.0

    start_frame = int(start_sec * fps)
    end_frame = int(end_sec * fps)

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # Read first frame and extract template
    ret, first_frame = cap.read()
    if not ret:
        raise RuntimeError("Cannot read first frame")

    x, y, w, h = bbox
    template = first_frame[y:y+h, x:x+w].copy()
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    results = [{
        "frame": 0,
        "timeSec": 0.0,
        "timeMs": 0.0,
        "x": x, "y": y, "w": w, "h": h,
        "centerX": x + w // 2,
        "centerY": y + h // 2,
        "confidence": 1.0,
    }]

    # Search window: expand around last known position
    search_margin = max(w, h)

    frame_idx = 1
    last_x, last_y = x, y

    for i in range(1, end_frame - start_frame):
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Define search region
        sx = max(0, last_x - search_margin)
        sy = max(0, last_y - search_margin)
        ex = min(gray.shape[1], last_x + w + search_margin)
        ey = min(gray.shape[0], last_y + h + search_margin)

        search_region = gray[sy:ey, sx:ex]

        if search_region.shape[0] < template_gray.shape[0] or search_region.shape[1] < template_gray.shape[1]:
            # Search region too small, use full frame
            search_region = gray
            sx, sy = 0, 0

        match = cv2.matchTemplate(search_region, template_gray, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(match)

        found_x = sx + max_loc[0]
        found_y = sy + max_loc[1]

        t_sec = round(frame_idx / fps, 4)

        results.append({
            "frame": frame_idx,
            "timeSec": t_sec,
            "timeMs": round(t_sec * 1000, 1),
            "x": found_x, "y": found_y, "w": w, "h": h,
            "centerX": found_x + w // 2,
            "centerY": found_y + h // 2,
            "confidence": round(float(max_val), 4),
        })

        last_x, last_y = found_x, found_y
        frame_idx += 1

    cap.release()
    return results


def track_features(
    video_path: str,
    bbox: tuple[int, int, int, int],
    start_sec: float,
    end_sec: float,
    fps: Optional[float] = None,
    max_points: int = 50,
) -> list[dict]:
    """
    Track element via Lucas-Kanade optical flow on feature points.

    Good for: elements that change appearance (scale, color) during animation.
    Returns per-frame {frame, timeSec, centerX, centerY, spreadX, spreadY, pointCount}.
    """
    cap = cv2.VideoCapture(video_path)
    if fps is None:
        fps = cap.get(cv2.CAP_PROP_FPS) or 60.0

    start_frame = int(start_sec * fps)
    end_frame = int(end_sec * fps)

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    ret, first_frame = cap.read()
    if not ret:
        raise RuntimeError("Cannot read first frame")

    x, y, w, h = bbox
    gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

    # Find good features within bbox
    mask = np.zeros_like(gray)
    mask[y:y+h, x:x+w] = 255

    points = cv2.goodFeaturesToTrack(
        gray, maxCorners=max_points, qualityLevel=0.01,
        minDistance=5, mask=mask
    )

    if points is None or len(points) == 0:
        return []

    lk_params = dict(
        winSize=(21, 21),
        maxLevel=3,
        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01),
    )

    results = []
    prev_gray = gray

    for i in range(end_frame - start_frame):
        center = np.mean(points, axis=0)[0]
        spread = np.std(points, axis=0)[0]

        t_sec = round(i / fps, 4)
        results.append({
            "frame": i,
            "timeSec": t_sec,
            "timeMs": round(t_sec * 1000, 1),
            "centerX": round(float(center[0]), 1),
            "centerY": round(float(center[1]), 1),
            "spreadX": round(float(spread[0]), 1),
            "spreadY": round(float(spread[1]), 1),
            "pointCount": len(points),
        })

        ret, frame = cap.read()
        if not ret:
            break

        curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        new_points, status, _ = cv2.calcOpticalFlowPyrLK(
            prev_gray, curr_gray, points, None, **lk_params
        )

        if new_points is not None:
            good = status.flatten() == 1
            points = new_points[good].reshape(-1, 1, 2)

        if len(points) < 3:
            break

        prev_gray = curr_gray

    cap.release()
    return results


def measure_opacity_proxy(
    video_path: str,
    bbox: tuple[int, int, int, int],
    start_sec: float,
    end_sec: float,
    fps: Optional[float] = None,
) -> list[dict]:
    """
    Measure mean luminance in a region as opacity proxy.

    For fade-in/out, luminance change correlates with opacity change
    when the element is brighter/darker than background.

    Returns per-frame {frame, timeSec, meanLuma, normalizedProgress}.
    """
    cap = cv2.VideoCapture(video_path)
    if fps is None:
        fps = cap.get(cv2.CAP_PROP_FPS) or 60.0

    start_frame = int(start_sec * fps)
    end_frame = int(end_sec * fps)

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    x, y, w, h = bbox
    measurements = []

    frame_idx = 0
    while frame_idx < (end_frame - start_frame):
        ret, frame = cap.read()
        if not ret:
            break

        region = frame[y:y+h, x:x+w]
        gray_region = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        mean_luma = float(np.mean(gray_region))

        t_sec = round(frame_idx / fps, 4)
        measurements.append({
            "frame": frame_idx,
            "timeSec": t_sec,
            "timeMs": round(t_sec * 1000, 1),
            "meanLuma": round(mean_luma, 2),
        })

        frame_idx += 1

    cap.release()

    # Normalize to 0-1 progress
    if measurements:
        lumas = [m["meanLuma"] for m in measurements]
        min_l, max_l = min(lumas), max(lumas)
        range_l = max_l - min_l if max_l > min_l else 1.0
        for m in measurements:
            m["normalizedProgress"] = round((m["meanLuma"] - min_l) / range_l, 4)

    return measurements


def extract_property_timeseries(
    tracking_data: list[dict],
    property_name: str = "centerX",
) -> tuple[np.ndarray, np.ndarray]:
    """
    Extract normalized (t, progress) arrays from tracking data.

    Returns (t_norm[0..1], progress_norm[0..1]).
    """
    values = [d[property_name] for d in tracking_data]
    times = [d["timeSec"] for d in tracking_data]

    t = np.array(times)
    v = np.array(values, dtype=float)

    # Normalize time to [0, 1]
    t_range = t[-1] - t[0]
    t_norm = (t - t[0]) / t_range if t_range > 0 else t * 0

    # Normalize value to [0, 1]
    v_range = v[-1] - v[0]
    if abs(v_range) < 1e-6:
        progress = np.zeros_like(v)
    else:
        progress = (v - v[0]) / v_range

    return t_norm, progress


if __name__ == "__main__":
    print("Usage: import and call track_template() or track_features()")
    print("  track_template(video, bbox=(x,y,w,h), start_sec, end_sec)")
    print("  track_features(video, bbox=(x,y,w,h), start_sec, end_sec)")
