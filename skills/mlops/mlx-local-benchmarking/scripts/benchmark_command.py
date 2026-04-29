#!/usr/bin/env python3
"""Time a command over warm-up and measured runs.

This measures wall-clock time for subprocess commands. It cannot see MLX
in-process peak memory; use MLX memory APIs inside Python when possible.
"""

from __future__ import annotations

import argparse
import statistics
import subprocess
import sys
import time
from typing import List


def run_command(cmd: List[str]) -> float:
    start = time.perf_counter()
    subprocess.run(cmd, check=True)
    return time.perf_counter() - start


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark a shell command.")
    parser.add_argument("--runs", type=int, default=5, help="Measured runs")
    parser.add_argument("--warmup", type=int, default=1, help="Warm-up runs")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Command after --")
    args = parser.parse_args()

    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        parser.error("Provide a command after --")
    if args.runs < 1 or args.warmup < 0:
        parser.error("--runs must be positive and --warmup non-negative")

    for idx in range(args.warmup):
        duration = run_command(command)
        print(f"warmup_{idx + 1}_seconds={duration:.6f}")

    durations = []
    for idx in range(args.runs):
        duration = run_command(command)
        durations.append(duration)
        print(f"run_{idx + 1}_seconds={duration:.6f}")

    print(f"median_seconds={statistics.median(durations):.6f}")
    print(f"mean_seconds={statistics.mean(durations):.6f}")
    print(f"min_seconds={min(durations):.6f}")
    print(f"max_seconds={max(durations):.6f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
