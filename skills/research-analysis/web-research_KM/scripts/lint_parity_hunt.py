#!/usr/bin/env python3
"""
Parity-Hunt Gate Checker

This script verifies that all stop gates for product-parity-hunt mode are satisfied.
Run before writing the final report to ensure the research is complete.

Usage:
    python lint_parity_hunt.py [research_dir]

    research_dir: Path to research folder (default: current directory)

Exit codes:
    0 - All gates passed
    1 - Missing required artifacts
    2 - Parity matrix incomplete
    3 - Query coverage insufficient
    4 - Candidate inventory insufficient
    5 - Evidence ledger incomplete
"""

import sys
import re
from pathlib import Path
from typing import Tuple, List

def check_artifacts_exist(root: Path) -> Tuple[bool, List[str]]:
    """Check that all required artifacts exist."""
    required = [
        "parity-matrix.md",
        "candidate-inventory.md",
        "query-families.md",
        "open-questions.md",
        "evidence-ledger.md",
        "action-log.md",
        "plan.md"
    ]
    missing = [f for f in required if not (root / f).exists()]
    return len(missing) == 0, missing

def check_parity_matrix(root: Path) -> Tuple[bool, str]:
    """Check that parity matrix has scores for all rows."""
    parity_file = root / "parity-matrix.md"
    if not parity_file.exists():
        return False, "parity-matrix.md not found"

    content = parity_file.read_text(errors="ignore")

    # Look for table rows with capability names
    capability_rows = [
        "Scheduling", "Durable Execution", "Persistence",
        "Notifications", "UI", "Integrations",
        "Human Oversight", "Security"
    ]

    # Check if rows have scores (look for | number | pattern or empty score)
    unscored = []
    for cap in capability_rows:
        # Find the row for this capability
        pattern = rf"\|\s*\*?\*?{cap}\*?\*?\s*\|.*\|.*\|.*\|\s*(\d*)\s*\|"
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            score = match.group(1).strip()
            if not score or score == "":
                unscored.append(cap)
        else:
            # Row might not exist or have different format
            if cap.lower() not in content.lower():
                unscored.append(f"{cap} (row not found)")

    if unscored:
        return False, f"Unscored capabilities: {', '.join(unscored)}"

    return True, "All capabilities scored"

def check_query_coverage(root: Path) -> Tuple[bool, str]:
    """Check query families and execution count."""
    qf_file = root / "query-families.md"
    if not qf_file.exists():
        return False, "query-families.md not found"

    content = qf_file.read_text(errors="ignore")

    # Count query families (rows in the main table)
    # Look for table rows that aren't headers
    family_rows = re.findall(r"^\|\s*[A-Za-z].*\|.*\|.*\d+.*\|", content, re.MULTILINE)
    num_families = len(family_rows)

    # Count executed queries in the execution log
    # Look for numbered rows in the execution log table
    query_log_rows = re.findall(r"^\|\s*\d+\s*\|[^|]+\|[^|]+\|[^|]+\|", content, re.MULTILINE)
    num_queries = len(query_log_rows)

    # Also try counting by looking for query text patterns
    if num_queries < 10:
        # Alternative: count lines that look like queries
        http_count = len(re.findall(r"https?://", content))
        search_terms = len(re.findall(r'"[^"]{10,}"', content))
        num_queries = max(num_queries, http_count + search_terms // 2)

    issues = []
    if num_families < 8:
        issues.append(f"Only {num_families} query families (need ≥8)")
    if num_queries < 30:
        issues.append(f"Only ~{num_queries} queries executed (need ≥30)")

    if issues:
        return False, "; ".join(issues)

    return True, f"{num_families} families, ~{num_queries} queries"

def check_candidate_inventory(root: Path) -> Tuple[bool, str]:
    """Check candidate inventory has sufficient candidates per class."""
    ci_file = root / "candidate-inventory.md"
    if not ci_file.exists():
        return False, "candidate-inventory.md not found"

    content = ci_file.read_text(errors="ignore")

    # Count candidates by solution class
    classes = {
        "workflow-automation": 0,
        "durable-execution": 0,
        "event-driven-runtime": 0,
        "data-orchestrator": 0
    }

    for line in content.split("\n"):
        if "|" in line:
            line_lower = line.lower()
            for cls in classes:
                if cls in line_lower:
                    # Check if the row has actual content (not just template)
                    cols = line.split("|")
                    if len(cols) >= 3 and cols[1].strip() and cols[2].strip():
                        classes[cls] += 1

    # Check quotas
    issues = []
    for cls, count in classes.items():
        if count < 3:
            issues.append(f"{cls}: {count}/3")

    if issues:
        return False, f"Insufficient candidates: {', '.join(issues)}"

    total = sum(classes.values())
    return True, f"{total} total candidates across classes"

def check_evidence_ledger(root: Path) -> Tuple[bool, str]:
    """Check evidence ledger has URLs for claims."""
    ledger_file = root / "evidence-ledger.md"
    if not ledger_file.exists():
        return False, "evidence-ledger.md not found"

    content = ledger_file.read_text(errors="ignore")

    # Count claims (rows with claim IDs like q1-c1)
    claims = re.findall(r"\|\s*q\d+-c\d+\s*\|", content, re.IGNORECASE)
    num_claims = len(claims)

    # Count URLs
    urls = re.findall(r"https?://[^\s\|]+", content)
    num_urls = len(urls)

    if num_claims == 0:
        return False, "No claims in evidence ledger"

    if num_urls < num_claims * 0.5:
        return False, f"Insufficient evidence: {num_claims} claims but only {num_urls} URLs"

    return True, f"{num_claims} claims with {num_urls} evidence URLs"

def main():
    # Get research directory
    if len(sys.argv) > 1:
        root = Path(sys.argv[1])
    else:
        root = Path(".")

    if not root.exists():
        print(f"ERROR: Directory not found: {root}")
        sys.exit(1)

    print(f"🔍 Checking parity-hunt gates in: {root.absolute()}\n")

    all_passed = True
    exit_code = 0

    # Gate 1: Required artifacts exist
    passed, details = check_artifacts_exist(root)
    if passed:
        print("✅ Gate 1: Required artifacts exist")
    else:
        print(f"❌ Gate 1: Missing artifacts: {', '.join(details)}")
        all_passed = False
        exit_code = 1

    # Gate 2: Parity matrix complete
    passed, details = check_parity_matrix(root)
    if passed:
        print(f"✅ Gate 2: Parity matrix complete — {details}")
    else:
        print(f"❌ Gate 2: Parity matrix incomplete — {details}")
        all_passed = False
        if exit_code == 0:
            exit_code = 2

    # Gate 3: Query coverage
    passed, details = check_query_coverage(root)
    if passed:
        print(f"✅ Gate 3: Query coverage sufficient — {details}")
    else:
        print(f"❌ Gate 3: Query coverage insufficient — {details}")
        all_passed = False
        if exit_code == 0:
            exit_code = 3

    # Gate 4: Candidate inventory
    passed, details = check_candidate_inventory(root)
    if passed:
        print(f"✅ Gate 4: Candidate inventory sufficient — {details}")
    else:
        print(f"❌ Gate 4: Candidate inventory insufficient — {details}")
        all_passed = False
        if exit_code == 0:
            exit_code = 4

    # Gate 5: Evidence ledger
    passed, details = check_evidence_ledger(root)
    if passed:
        print(f"✅ Gate 5: Evidence ledger complete — {details}")
    else:
        print(f"❌ Gate 5: Evidence ledger incomplete — {details}")
        all_passed = False
        if exit_code == 0:
            exit_code = 5

    print()
    if all_passed:
        print("🎉 All gates passed! Ready to write final report.")
        sys.exit(0)
    else:
        print("⚠️  Some gates failed. Continue research or write stop-report.md with failures.")
        sys.exit(exit_code)

if __name__ == "__main__":
    main()
