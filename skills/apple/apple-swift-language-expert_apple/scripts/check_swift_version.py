#!/usr/bin/env python3
"""Check the installed Swift toolchain version.

This script compares the installed Swift version against the baseline documented
in the `apple-swift-language-expert` skill.  It prints a warning if the
installed version is older than the baseline and reminds you to consult the
skill's version matrix.  The script handles missing toolchains gracefully.

Usage::

    python3 check_swift_version.py

The script attempts to run `swift --version` and parse the output.  If Swift
is not found, it advises installing a toolchain.  You can override the
baseline by setting the environment variables `BASELINE_MAJOR` and
`BASELINE_MINOR` (integers).

"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from typing import Optional, Tuple


def get_swift_version() -> Optional[Tuple[int, int, str]]:
    """Return the installed Swift version as (major, minor, full_output).

    Returns None if the `swift` executable is not found or its version cannot
    be parsed.
    """
    try:
        # Capture both stdout and stderr to handle cases where swift writes to stderr.
        output = subprocess.check_output(["swift", "--version"], stderr=subprocess.STDOUT, text=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    match = re.search(r"Swift version\s+([0-9]+)\.([0-9]+)", output)
    if match:
        major = int(match.group(1))
        minor = int(match.group(2))
        return (major, minor, output.strip())
    return None


def main() -> int:
    # Baseline version reflects the last verified Swift in SKILL.md.  Update when
    # the skill is revised.
    baseline_major = int(os.environ.get("BASELINE_MAJOR", "6"))
    baseline_minor = int(os.environ.get("BASELINE_MINOR", "2"))
    version_info = get_swift_version()
    print("⚙️  Swift toolchain version checker")
    if version_info is None:
        print("❌ Swift is not installed or `swift --version` could not be run.\n"
              "Please ensure you have a Swift toolchain installed and in your PATH.")
        return 1
    major, minor, full_output = version_info
    print(f"Detected Swift version: {major}.{minor}")
    if (major, minor) < (baseline_major, baseline_minor):
        print(f"⚠️  Your Swift version {major}.{minor} is older than the baseline "
              f"{baseline_major}.{baseline_minor}. Some features described in the skill may be unavailable.")
        print("Consider upgrading your toolchain or adjusting your code accordingly.")
    else:
        print(f"✅ Your Swift version {major}.{minor} meets or exceeds the baseline {baseline_major}.{baseline_minor}.")
    # Show the full version output for transparency
    print("\nFull `swift --version` output:\n" + full_output)
    print("\nRemember to consult the skill's feature matrix and run `evolution_tracker.py` for the latest proposals.")
    return 0


if __name__ == "__main__":
    sys.exit(main())