#!/usr/bin/env python3
"""
Generate visual reports from skill audit data.
Produces PNG charts for runtime distribution, entity types, health heatmap,
drift status, and bloat analysis.

Usage:
    python visualize_audit.py --discovery DISCOVERY --inventory INVENTORY \\
        --freshness FRESHNESS --xdiff XDIFF --output-dir /tmp/audit-viz/

Requires: matplotlib (usually pre-installed with Python on macOS).
Falls back to text-based summaries if matplotlib unavailable.
"""

import argparse
import json
import os
import sys
from collections import defaultdict

try:
    import matplotlib
    matplotlib.use("Agg")  # Non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("WARNING: matplotlib not available. Install with: pip3 install matplotlib", file=sys.stderr)
    print("Falling back to text-only output.", file=sys.stderr)


# ── Color palette ────────────────────────────────────────────────────────────
COLORS = {
    "claude-code": "#D97706",
    "factory": "#059669",
    "global-pool": "#2563EB",
    "kiro": "#7C3AED",
    "codex-cli": "#DC2626",
    "cursor": "#0891B2",
    "gemini-cli": "#4285F4",
    "antigravity": "#34A853",
    "osaurus": "#6366F1",
    "project-local": "#9CA3AF",
}

SCOPE_COLORS = {
    "global": "#3B82F6",
    "project-local": "#F59E0B",
}

STATUS_COLORS = {
    "identical": "#10B981",
    "symlinked": "#6366F1",
    "drifted": "#EF4444",
    "singleton": "#F59E0B",
}

ENTITY_COLORS = {
    "skill": "#3B82F6",
    "agent": "#8B5CF6",
    "command": "#F59E0B",
    "rule": "#EF4444",
    "plugin": "#10B981",
    "context": "#6B7280",
    "profile": "#EC4899",
}


def get_runtime_color(runtime: str) -> str:
    """Get color for a runtime, with fallback for workspace-qualified names."""
    if runtime in COLORS:
        return COLORS[runtime]
    for prefix, color in COLORS.items():
        if runtime.startswith(prefix):
            return color
    return "#9CA3AF"


def chart_runtime_distribution(discovery: dict, output_dir: str) -> str:
    """Bar chart: items per agent runtime."""
    by_runtime = discovery.get("summary", {}).get("by_runtime", {})
    if not by_runtime:
        return ""

    runtimes = sorted(by_runtime.keys(), key=lambda k: -by_runtime[k])
    counts = [by_runtime[r] for r in runtimes]
    colors = [get_runtime_color(r) for r in runtimes]

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(range(len(runtimes)), counts, color=colors, edgecolor="white", linewidth=0.5)
    ax.set_yticks(range(len(runtimes)))
    ax.set_yticklabels(runtimes, fontsize=10)
    ax.set_xlabel("Item Count", fontsize=11)
    ax.set_title("Items by Agent Runtime", fontsize=14, fontweight="bold")
    ax.invert_yaxis()

    # Value labels
    for bar, count in zip(bars, counts):
        ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height() / 2,
                str(count), va="center", fontsize=10, fontweight="bold")

    plt.tight_layout()
    path = os.path.join(output_dir, "runtime_distribution.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def chart_entity_types(discovery: dict, output_dir: str) -> str:
    """Pie chart: entity type breakdown."""
    by_type = discovery.get("summary", {}).get("by_entity_type", {})
    if not by_type:
        return ""

    labels = sorted(by_type.keys(), key=lambda k: -by_type[k])
    sizes = [by_type[l] for l in labels]
    colors = [ENTITY_COLORS.get(l, "#9CA3AF") for l in labels]

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, autopct="%1.0f%%",
        startangle=140, textprops={"fontsize": 11}
    )
    for t in autotexts:
        t.set_fontweight("bold")
    ax.set_title("Entity Type Distribution", fontsize=14, fontweight="bold")

    plt.tight_layout()
    path = os.path.join(output_dir, "entity_types.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def chart_scope_split(discovery: dict, output_dir: str) -> str:
    """Stacked bar: global vs project-local per runtime."""
    items = discovery.get("skills", [])
    runtime_scope = defaultdict(lambda: {"global": 0, "project-local": 0})
    for item in items:
        rt = item.get("agent_runtime", "unknown")
        scope = item.get("scope", "global")
        runtime_scope[rt][scope] += 1

    runtimes = sorted(runtime_scope.keys(), key=lambda k: -(runtime_scope[k]["global"] + runtime_scope[k]["project-local"]))
    globals_ = [runtime_scope[r]["global"] for r in runtimes]
    locals_ = [runtime_scope[r]["project-local"] for r in runtimes]

    fig, ax = plt.subplots(figsize=(12, 6))
    y = range(len(runtimes))
    ax.barh(y, globals_, color=SCOPE_COLORS["global"], label="Global", edgecolor="white", linewidth=0.5)
    ax.barh(y, locals_, left=globals_, color=SCOPE_COLORS["project-local"], label="Project-Local", edgecolor="white", linewidth=0.5)
    ax.set_yticks(y)
    ax.set_yticklabels(runtimes, fontsize=10)
    ax.set_xlabel("Count", fontsize=11)
    ax.set_title("Global vs Project-Local by Runtime", fontsize=14, fontweight="bold")
    ax.legend(loc="lower right")
    ax.invert_yaxis()

    plt.tight_layout()
    path = os.path.join(output_dir, "scope_split.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def chart_drift_status(xdiff: dict, output_dir: str) -> str:
    """Donut chart: drift status distribution."""
    summary = xdiff.get("summary", {})
    if not summary:
        return ""

    statuses = ["identical", "symlinked", "drifted", "singleton"]
    sizes = [summary.get(s, 0) for s in statuses]
    colors = [STATUS_COLORS[s] for s in statuses]

    # Filter out zeros
    filtered = [(s, sz, c) for s, sz, c in zip(statuses, sizes, colors) if sz > 0]
    if not filtered:
        return ""
    statuses, sizes, colors = zip(*filtered)

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=statuses, colors=colors, autopct="%1.0f%%",
        startangle=90, pctdistance=0.8, textprops={"fontsize": 11}
    )
    # Draw donut hole
    centre_circle = plt.Circle((0, 0), 0.55, fc="white")
    ax.add_artist(centre_circle)
    ax.text(0, 0, f"{sum(sizes)}\nunique", ha="center", va="center",
            fontsize=16, fontweight="bold")

    for t in autotexts:
        t.set_fontweight("bold")
    ax.set_title("Cross-Location Drift Status", fontsize=14, fontweight="bold")

    plt.tight_layout()
    path = os.path.join(output_dir, "drift_status.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def chart_health_heatmap(freshness: dict, output_dir: str) -> str:
    """Heatmap: health flags by runtime."""
    items = freshness.get("skills", [])
    if not items:
        return ""

    # Collect flag types per runtime
    runtimes = set()
    flag_types = {"stale", "no FEEDBACK.md", "stale models"}
    runtime_flags = defaultdict(lambda: defaultdict(int))

    for item in items:
        rt = item.get("agent_runtime", "unknown")
        runtimes.add(rt)
        for flag in item.get("flags", []):
            if "stale (" in flag:
                runtime_flags[rt]["stale"] += 1
            elif "no FEEDBACK" in flag:
                runtime_flags[rt]["no FEEDBACK.md"] += 1
            elif "stale model" in flag:
                runtime_flags[rt]["stale models"] += 1

    runtimes = sorted(runtimes, key=lambda r: -sum(runtime_flags[r].values()))
    flag_list = sorted(flag_types)

    if not runtimes or not flag_list:
        return ""

    # Build matrix
    matrix = []
    for rt in runtimes:
        row = [runtime_flags[rt].get(f, 0) for f in flag_list]
        matrix.append(row)

    fig, ax = plt.subplots(figsize=(10, max(6, len(runtimes) * 0.5)))
    im = ax.imshow(matrix, cmap="YlOrRd", aspect="auto")

    ax.set_xticks(range(len(flag_list)))
    ax.set_xticklabels(flag_list, fontsize=11, rotation=30, ha="right")
    ax.set_yticks(range(len(runtimes)))
    ax.set_yticklabels(runtimes, fontsize=10)

    # Annotate cells
    for i in range(len(runtimes)):
        for j in range(len(flag_list)):
            val = matrix[i][j]
            if val > 0:
                ax.text(j, i, str(val), ha="center", va="center",
                        fontsize=11, fontweight="bold",
                        color="white" if val > 5 else "black")

    ax.set_title("Health Flags by Runtime", fontsize=14, fontweight="bold")
    fig.colorbar(im, ax=ax, shrink=0.6, label="Count")

    plt.tight_layout()
    path = os.path.join(output_dir, "health_heatmap.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def chart_bloat_analysis(inventory: dict, output_dir: str) -> str:
    """Scatter plot: line count vs reference count, sized by script count."""
    items = [i for i in inventory.get("skills", [])
             if i.get("entity_type", "skill") == "skill" and i.get("line_count", 0) > 0]
    if not items:
        return ""

    # Top 40 by line count for readability
    items = sorted(items, key=lambda i: -i.get("line_count", 0))[:40]

    names = [i.get("name", "?")[:25] for i in items]
    lines = [i.get("line_count", 0) for i in items]
    refs = [i.get("ref_count", 0) for i in items]
    scripts = [max(i.get("script_count", 0) * 30 + 20, 20) for i in items]
    runtimes = [i.get("agent_runtime", "unknown") for i in items]
    colors = [get_runtime_color(r) for r in runtimes]

    fig, ax = plt.subplots(figsize=(14, 8))
    scatter = ax.scatter(lines, refs, s=scripts, c=colors, alpha=0.7, edgecolors="white", linewidth=0.5)

    # Label top 15 biggest
    for i in range(min(15, len(items))):
        ax.annotate(names[i], (lines[i], refs[i]),
                    fontsize=8, alpha=0.8, ha="left",
                    xytext=(5, 5), textcoords="offset points")

    # Bloat threshold line
    ax.axvline(x=500, color="#EF4444", linestyle="--", alpha=0.5, label="Bloat threshold (500L)")

    ax.set_xlabel("Line Count", fontsize=11)
    ax.set_ylabel("Reference File Count", fontsize=11)
    ax.set_title("Skill Complexity: Lines vs References (bubble = scripts)", fontsize=14, fontweight="bold")
    ax.legend(loc="upper right")

    plt.tight_layout()
    path = os.path.join(output_dir, "bloat_analysis.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def text_summary(discovery: dict, inventory: dict, freshness: dict, xdiff: dict) -> str:
    """Generate text-only summary when matplotlib unavailable."""
    lines = ["=" * 60, "SKILL LIBRARY AUDIT — VISUAL SUMMARY (TEXT)", "=" * 60, ""]

    # Runtime distribution
    by_runtime = discovery.get("summary", {}).get("by_runtime", {})
    lines.append("ITEMS BY RUNTIME:")
    for rt, count in sorted(by_runtime.items(), key=lambda x: -x[1]):
        bar = "█" * (count // 5) + "▌" * (1 if count % 5 >= 3 else 0)
        lines.append(f"  {rt:30s} {bar} {count}")
    lines.append("")

    # Entity types
    by_type = discovery.get("summary", {}).get("by_entity_type", {})
    lines.append("ENTITY TYPES:")
    for et, count in sorted(by_type.items(), key=lambda x: -x[1]):
        lines.append(f"  {et:15s} {count}")
    lines.append("")

    # Drift
    summary = xdiff.get("summary", {})
    lines.append("DRIFT STATUS:")
    for status in ["identical", "symlinked", "drifted", "singleton"]:
        lines.append(f"  {status:15s} {summary.get(status, 0)}")
    lines.append("")

    # Health
    lines.append("HEALTH FLAGS:")
    lines.append(f"  Stale:           {freshness.get('stale_count', 0)}")
    lines.append(f"  No FEEDBACK.md:  {freshness.get('no_feedback_count', 0)}")
    lines.append(f"  Stale models:    {freshness.get('stale_models_count', 0)}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate visual audit reports")
    parser.add_argument("--discovery", required=True, help="Discovery JSON")
    parser.add_argument("--inventory", required=True, help="Inventory JSON")
    parser.add_argument("--freshness", required=True, help="Freshness JSON")
    parser.add_argument("--xdiff", required=True, help="Cross-location diff JSON")
    parser.add_argument("--output-dir", "-o", default="/tmp/audit-viz",
                        help="Output directory for PNG files")
    args = parser.parse_args()

    # Load all data
    with open(args.discovery) as f:
        discovery = json.load(f)
    with open(args.inventory) as f:
        inventory = json.load(f)
    with open(args.freshness) as f:
        freshness = json.load(f)
    with open(args.xdiff) as f:
        xdiff = json.load(f)

    os.makedirs(args.output_dir, exist_ok=True)

    if not HAS_MPL:
        summary = text_summary(discovery, inventory, freshness, xdiff)
        print(summary)
        txt_path = os.path.join(args.output_dir, "summary.txt")
        with open(txt_path, "w") as f:
            f.write(summary)
        print(f"\nText summary written to {txt_path}", file=sys.stderr)
        return

    charts = []
    print("Generating charts...", file=sys.stderr)

    c = chart_runtime_distribution(discovery, args.output_dir)
    if c:
        charts.append(c)
        print(f"  ✓ {os.path.basename(c)}", file=sys.stderr)

    c = chart_entity_types(discovery, args.output_dir)
    if c:
        charts.append(c)
        print(f"  ✓ {os.path.basename(c)}", file=sys.stderr)

    c = chart_scope_split(discovery, args.output_dir)
    if c:
        charts.append(c)
        print(f"  ✓ {os.path.basename(c)}", file=sys.stderr)

    c = chart_drift_status(xdiff, args.output_dir)
    if c:
        charts.append(c)
        print(f"  ✓ {os.path.basename(c)}", file=sys.stderr)

    c = chart_health_heatmap(freshness, args.output_dir)
    if c:
        charts.append(c)
        print(f"  ✓ {os.path.basename(c)}", file=sys.stderr)

    c = chart_bloat_analysis(inventory, args.output_dir)
    if c:
        charts.append(c)
        print(f"  ✓ {os.path.basename(c)}", file=sys.stderr)

    print(f"\n{len(charts)} charts written to {args.output_dir}/", file=sys.stderr)

    # Write manifest
    manifest = {
        "generated_at": discovery.get("discovered_at", ""),
        "charts": [{"path": c, "name": os.path.splitext(os.path.basename(c))[0]} for c in charts],
        "total_items": discovery.get("total_items", 0),
    }
    manifest_path = os.path.join(args.output_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Manifest: {manifest_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
