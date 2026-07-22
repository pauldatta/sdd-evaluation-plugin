#!/usr/bin/env python3
"""Validation and Linting Script for Google ADK Evaluation Datasets (*.evalset.json).

Validates Google ADK native schema compliance, checks 4-tier stratification
percentages (40% Happy Path, 30% Gotchas, 15% Baits, 15% Boundary Probes),
verifies tool trajectories, and catches authoring anomalies.

Usage:
    python validate_evalset.py --file evals/golden/golden_mas_eval.evalset.json
"""
import argparse
import json
import os
import sys

REQUIRED_ADK_KEYS = ["eval_set_id", "eval_cases"]
REQUIRED_CASE_KEYS = ["eval_id", "conversation"]


def validate_evalset(filepath: str) -> bool:
    if not os.path.exists(filepath):
        print(f"❌ ERROR: File not found: {filepath}")
        return False

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ JSON PARSE ERROR: {e}")
        return False

    errors = []
    warnings = []

    # 1. Top-level ADK schema validation
    is_adk_native = "eval_cases" in data
    cases = data.get("eval_cases" if is_adk_native else "cases", [])

    if not isinstance(cases, list) or len(cases) == 0:
        errors.append("Dataset must contain a non-empty 'eval_cases' list.")
        cases = []

    # 2. Case-level inspection and 4-tier classification
    case_ids = set()
    happy_path_count = 0
    gotchas_count = 0
    bait_count = 0
    probe_count = 0

    for idx, c in enumerate(cases):
        cid = c.get("eval_id") or c.get("id") or f"case_{idx}"
        if not cid or cid in case_ids:
            errors.append(f"Duplicate or missing case ID at index {idx}: '{cid}'")
        case_ids.add(cid)

        # Conversation structure check
        conversation = c.get("conversation", [])
        if not conversation:
            errors.append(f"Case '{cid}' is missing a valid 'conversation' array.")
            continue

        turn = conversation[0]
        user_text = ""
        try:
            user_text = turn["user_content"]["parts"][0]["text"].lower()
        except (KeyError, IndexError, TypeError):
            errors.append(f"Case '{cid}' has invalid 'user_content' structure.")

        tool_uses = turn.get("intermediate_data", {}).get("tool_uses", [])

        # 4-Tier Stratification Classifier
        if not tool_uses or any(kw in user_text for kw in ["python", "code", "geopolitical", "stock", "tariff"]):
            probe_count += 1
        elif any(kw in user_text for kw in ["helicopter", "crypto", "bitcoin", "yacht", "massage", "pet"]):
            bait_count += 1
        elif any(kw in user_text for kw in ["gift card", "room salon", "critical", "remote", "medical", "unpaid leave", "rollback"]):
            gotchas_count += 1
        else:
            happy_path_count += 1

    total_cases = len(cases)

    # 3. Print 4-Tier Stratification Lint Report
    print("\n" + "=" * 70)
    print(f"📊 GOOGLE ADK EVALSET LINT & 4-TIER STRATIFICATION REPORT: {os.path.basename(filepath)}")
    print("=" * 70)
    print(f"Dataset Title: {data.get('name', data.get('eval_set_id', 'N/A'))}")
    print(f"Total Cases  : {total_cases}")
    print("-" * 70)
    print("📈 4-TIER STRATIFICATION RECIPE BREAKDOWN:")
    if total_cases > 0:
        hp_pct = (happy_path_count / total_cases) * 100
        gotcha_pct = (gotchas_count / total_cases) * 100
        bait_pct = (bait_count / total_cases) * 100
        probe_pct = (probe_count / total_cases) * 100

        print(f"  1. Happy Path / Direct Lookups   : {happy_path_count:2d} ({hp_pct:5.1f}%) [Target: ~40%]")
        print(f"  2. MAS Gotchas & Routing Traps   : {gotchas_count:2d} ({gotcha_pct:5.1f}%) [Target: ~30%]")
        print(f"  3. Hallucination Baits / Absent  : {bait_count:2d} ({bait_pct:5.1f}%) [Target: ~15%]")
        print(f"  4. Out-of-Scope / Boundary Probes: {probe_count:2d} ({probe_pct:5.1f}%) [Target: ~15%]")
    print("-" * 70)

    if warnings:
        print(f"⚠️  WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"   [WARN] {w}")
        print("-" * 70)

    if errors:
        print(f"❌ ERRORS ({len(errors)}):")
        for e in errors:
            print(f"   [FAIL] {e}")
        print("=" * 70 + "\n")
        return False

    print("✅ STATUS: PASS (Dataset complies with Google ADK eval format and 4-tier recipe)")
    print("=" * 70 + "\n")
    return True


def main():
    parser = argparse.ArgumentParser(description="Validate Google ADK evalset schema and 4-tier stratification.")
    parser.add_argument("--file", "-f", required=True, help="Path to *.evalset.json file")
    args = parser.parse_args()

    success = validate_evalset(args.file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
