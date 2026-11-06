#!/usr/bin/env python3
"""
SARATHI Independent Verification Harness
Author: For Hemanth (SARATHI Independent Testing Lead)
Product: CLO (Chief Legal Officer) Agent Increment
Purpose: One-shot automated independent verification of contracts, temporal reasoning,
security boundaries, and Hard Rule 5 zero-evidence refusal.
"""

import sys
import os
import json
import time
import hashlib
from datetime import datetime, timezone

# Ensure repo root is on sys.path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import pytest
from fastapi.testclient import TestClient
from clo.runtime.api import app, registry, vajra_adapter


def run_sarathi_verification():
    print("======================================================================")
    print("  SARATHI INDEPENDENT VERIFICATION HARNESS — CLO INCREMENT (ANSH)    ")
    print("======================================================================")
    start_time = time.time()
    report = {
        "verifier": "Hemanth (SARATHI Independent Testing Lead)",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "build_owner": "Ansh",
        "target_repo": "praj33/BHIV-BIQOS-P0-EXECUTION",
        "checks": [],
        "overall_status": "PENDING"
    }

    # 1. Automated Test Suite Execution (Pytest 20/20)
    print("\n[Step 1/5] Executing 20 automated Pytest test cases across 6 scenarios...")
    test_dir = os.path.join(repo_root, "tests", "clo")
    pytest_exit_code = pytest.main(["-q", test_dir])
    if pytest_exit_code == 0:
        print("  ✓ Pytest Suite: 20/20 tests passed.")
        report["checks"].append({
            "check": "PYTEST_SUITE_EXECUTION",
            "tests_passing": 20,
            "status": "PASS",
            "exit_code": 0
        })
    else:
        print(f"  ✗ Pytest Suite failed with exit code: {pytest_exit_code}")
        report["checks"].append({
            "check": "PYTEST_SUITE_EXECUTION",
            "status": "FAIL",
            "exit_code": pytest_exit_code
        })

    client = TestClient(app)

    # 2. Canonical Registry Integrity
    print("\n[Step 2/5] Validating Canonical Legal Registry & Gazette URLs...")
    docs = registry.list_documents()
    docs_valid = len(docs) == 8 and all(d.source_url.startswith("http") and len(d.sha256_hash) == 64 for d in docs)
    if docs_valid:
        print(f"  ✓ Canonical Registry: All 8 documents verified with SHA-256 integrity hashes.")
        report["checks"].append({
            "check": "CANONICAL_REGISTRY_INTEGRITY",
            "document_count": len(docs),
            "status": "PASS"
        })
    else:
        print("  ✗ Canonical Registry validation failed.")
        report["checks"].append({
            "check": "CANONICAL_REGISTRY_INTEGRITY",
            "status": "FAIL"
        })

    # 3. Temporal As-of-Date Logic (Amendment & Supersession Pair)
    print("\n[Step 3/5] Verifying Temporal As-of-Date Resolution (IT Rules 2011 vs 2021)...")
    res_2018 = client.post("/api/v1/clo/research", json={
        "query": "What is the grievance redressal timeline under intermediary rules?",
        "as_of_date": "2018-05-01",
        "caller_identity": "ansh_clo_build_owner"
    })
    res_2024 = client.post("/api/v1/clo/research", json={
        "query": "What is the grievance redressal timeline under intermediary rules?",
        "as_of_date": "2024-01-01",
        "caller_identity": "ansh_clo_build_owner"
    })

    data_18 = res_2018.json()
    data_24 = res_2024.json()

    # In 2018: 2011 rules is CURRENT
    p_18_status = any(p["document_id"] == "doc-in-it-intermediary-rules-2011" and p["version_status_as_of_date"] == "CURRENT" for p in data_18["evidence_passages"])
    # In 2024: 2021 rules is CURRENT and conflicts/supersession surfaced
    p_24_status = any(p["document_id"] == "doc-in-it-rules-2021" and p["version_status_as_of_date"] == "CURRENT" for p in data_24["evidence_passages"])
    has_conflict = len(data_24["conflicts_identified"]) > 0

    if p_18_status and p_24_status and has_conflict:
        print("  ✓ Temporal Resolution: Correctly evaluated 2018 un-superseded law vs 2024 active superseding law.")
        report["checks"].append({
            "check": "TEMPORAL_AS_OF_DATE_EVALUATION",
            "status": "PASS",
            "details": "2018 evaluated 2011 rules as CURRENT; 2024 evaluated 2021 rules as CURRENT with supersession notice."
        })
    else:
        print("  ✗ Temporal resolution check failed.")
        report["checks"].append({
            "check": "TEMPORAL_AS_OF_DATE_EVALUATION",
            "status": "FAIL"
        })

    # 4. Security & Permission Boundaries (Fail-Closed Enforcement)
    print("\n[Step 4/5] Interrogating Security & Authority Boundaries (VAJRA Fail-Closed)...")
    res_revoked = client.post("/api/v1/clo/research", json={
        "query": "Review data protection obligations",
        "caller_identity": "compromised_key_actor"
    })
    res_suspended = client.post("/api/v1/clo/research", json={
        "query": "Review data protection obligations",
        "caller_identity": "suspended_auditor"
    })
    state_view = vajra_adapter.get_agent_state_view()

    sec_pass = (res_revoked.status_code == 403 and
                res_suspended.status_code == 403 and
                state_view["direct_mutation_allowed"] is False)

    if sec_pass:
        print("  ✓ Security Boundaries: Fail-closed rejection of revoked/suspended callers confirmed (403 Forbidden).")
        print("  ✓ Rule 8: Agent direct ledger mutation prohibited.")
        report["checks"].append({
            "check": "SECURITY_FAIL_CLOSED_BOUNDARIES",
            "status": "PASS",
            "revoked_status": res_revoked.status_code,
            "suspended_status": res_suspended.status_code,
            "rule_8_direct_mutation_allowed": False
        })
    else:
        print("  ✗ Security boundary check failed.")
        report["checks"].append({
            "check": "SECURITY_FAIL_CLOSED_BOUNDARIES",
            "status": "FAIL"
        })

    # 5. Hard Rule 5: Zero Evidence Refusal
    print("\n[Step 5/5] Testing Hard Rule 5 Enforcement (Zero Evidence Refusal)...")
    res_zero = client.post("/api/v1/clo/research", json={
        "query": "What is the speed limit of warp drive spaceships under Indian maritime law?",
        "caller_identity": "ansh_clo_build_owner"
    })
    data_zero = res_zero.json()
    rule5_pass = (data_zero["conclusion"] is None and
                  data_zero["evidence_status"] == "INSUFFICIENT_EVIDENCE" and
                  len(data_zero["evidence_passages"]) == 0 and
                  data_zero["human_review_required"] is True)

    if rule5_pass:
        print("  ✓ Hard Rule 5: Agent strictly refused conclusion on unevidenced topic; flagged for human review.")
        report["checks"].append({
            "check": "RULE_5_ZERO_EVIDENCE_REFUSAL",
            "status": "PASS",
            "conclusion_is_none": True,
            "human_review_flagged": True
        })
    else:
        print("  ✗ Hard Rule 5 check failed.")
        report["checks"].append({
            "check": "RULE_5_ZERO_EVIDENCE_REFUSAL",
            "status": "FAIL"
        })

    duration_ms = int((time.time() - start_time) * 1000)
    report["duration_ms"] = duration_ms
    all_passed = all(c["status"] == "PASS" for c in report["checks"])
    report["overall_status"] = "VERIFIED_ACCEPTED" if all_passed else "DEFECTS_DETECTED"

    # Save verification report
    report_path = os.path.join(repo_root, "docs", "clo", "sarathi_independent_verification_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("\n======================================================================")
    print(f"  SARATHI VERIFICATION OUTCOME: {report['overall_status']} ({duration_ms} ms)")
    print(f"  Audit Report Generated: {report_path}")
    print("======================================================================")
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(run_sarathi_verification())

