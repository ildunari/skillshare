#!/usr/bin/env python3
from __future__ import annotations

import argparse
from _shared import load_json, write_json


def main():
    parser = argparse.ArgumentParser(description="Compare canonical source skills against downstream installs.")
    parser.add_argument("topology")
    parser.add_argument("--output", "-o", required=True)
    args = parser.parse_args()

    topo = load_json(args.topology)
    mode = topo.get("summary", {}).get("mode", "canonical-source")
    if mode != "canonical-source":
        payload = {
            "summary": {
                "mode": mode,
                "row_count": 0,
                "in_sync": 0,
                "out_of_sync": 0,
                "install_only": 0,
                "undistributed_source": 0,
                "not_applicable": True,
                "reason": "Canonical-vs-install drift only applies in canonical-source mode.",
            },
            "rows": [],
        }
        write_json(args.output, payload)
        print(args.output)
        return

    rows = []
    for skill in topo.get("skills", []):
        source_hash = skill.get("source_hash")
        for target in skill.get("targets", []):
            status = target["status"]
            if not skill.get("source_present") and status == "present":
                drift = "install-only"
            elif skill.get("source_present") and status == "missing":
                drift = "undistributed-source"
            elif skill.get("source_present") and status == "present":
                hashes = set(target.get("hashes") or [])
                drift = "in-sync" if source_hash in hashes and len(hashes) == 1 else "out-of-sync"
            else:
                drift = "absent"
            rows.append({
                "skill_slug": skill["skill_slug"],
                "target": target["target"],
                "source_present": skill.get("source_present"),
                "source_hash": source_hash,
                "target_status": status,
                "target_hashes": target.get("hashes") or [],
                "drift_status": drift,
                "target_copies": target.get("copies") or [],
            })
    payload = {
        "summary": {
            "mode": mode,
            "row_count": len(rows),
            "in_sync": sum(1 for r in rows if r["drift_status"] == "in-sync"),
            "out_of_sync": sum(1 for r in rows if r["drift_status"] == "out-of-sync"),
            "install_only": sum(1 for r in rows if r["drift_status"] == "install-only"),
            "undistributed_source": sum(1 for r in rows if r["drift_status"] == "undistributed-source"),
        },
        "rows": rows,
    }
    write_json(args.output, payload)
    print(args.output)


if __name__ == "__main__":
    main()
