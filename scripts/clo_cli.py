#!/usr/bin/env python3
"""
CLO Agent Interactive CLI
Product: Chief Legal Officer (CLO) Agent for BIQOS
Build Owner: Ansh
Allows stakeholders (Nupur, Raj, Rahil, Hemanth) to test legal queries,
as-of-date temporal resolution, and authority boundary checks from the terminal.
"""

import argparse
import json
import os
import sys

# Ensure repo root is on sys.path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from clo.reasoning.engine import LegalReasoningEngine
from clo.schemas.models import LegalQueryRequest
from clo.adapters.vajra_adapter import VajraTrustAdapter
from clo.adapters.mdu_adapter import MduLineageAdapter
from clo.adapters.insightflow_adapter import InsightFlowTelemetryAdapter


def main():
    parser = argparse.ArgumentParser(
        description="BHIV CLO Agent — Interactive Legal Reasoning CLI"
    )
    parser.add_argument(
        "--query", "-q",
        type=str,
        required=True,
        help="Legal or compliance query text"
    )
    parser.add_argument(
        "--as-of-date", "-d",
        type=str,
        default=None,
        help="Evaluation date in YYYY-MM-DD format (enables historical supersession analysis)"
    )
    parser.add_argument(
        "--caller", "-c",
        type=str,
        default="ansh_clo_build_owner",
        help="Caller identity for VAJRA authority verification (e.g. ansh_clo_build_owner, compromised_key_actor)"
    )
    parser.add_argument(
        "--token", "-t",
        type=str,
        default="ANSH_CLO_GOVERNED_SESSION",
        help="Bearer token for VAJRA authority gate"
    )
    parser.add_argument(
        "--json-output",
        action="store_true",
        help="Output raw JSON response rather than human-readable report"
    )

    args = parser.parse_args()

    # Initialize components
    engine = LegalReasoningEngine()
    vajra = VajraTrustAdapter()
    mdu = MduLineageAdapter()
    insightflow = InsightFlowTelemetryAdapter()

    # Step 1: VAJRA Authority Verification
    auth_res = vajra.verify_authority(
        subject=args.caller,
        action="legal:research",
        trace_id="cli-interactive-session",
        token=args.token,
    )

    if not auth_res.allowed:
        print("\n======================================================================")
        print("  [ACCESS DENIED] VAJRA AUTHORITY GATE BLOCKED EXECUTION (FAIL-CLOSED)  ")
        print("======================================================================")
        print(f"  Subject:       {auth_res.subject}")
        print(f"  Current State: {auth_res.current_state}")
        print(f"  Reason:        {auth_res.reason}")
        print("======================================================================\n")
        sys.exit(1)

    # Step 2: Reason over query
    req = LegalQueryRequest(
        query=args.query,
        as_of_date=args.as_of_date,
        caller_identity=args.caller,
        auth_token=args.token,
    )
    response = engine.reason_over_query(req)
    response.vajra_trust_status = f"VERIFIED: {auth_res.current_state}"

    # Step 3: Record MDU Lineage
    matched = [f"{p.document_id}#{p.section_number}" for p in response.evidence_passages]
    ev = mdu.record_retrieval_lineage(
        dataset_id="ds-legal-aggregate-query",
        trace_id=response.trace_id,
        query=args.query,
        matched_sections=matched,
        actor=args.caller,
    )
    response.mdu_provenance_event_ids.append(ev.event_id)

    # Step 4: Emit Passive InsightFlow Telemetry
    insightflow.emit_telemetry_event(
        trace_id=response.trace_id,
        execution_id="exec-cli-001",
        event_type="cli_legal_query",
        status=response.evidence_status,
        payload={"query": args.query, "as_of_date": response.as_of_date_applied}
    )

    if args.json_output:
        print(response.model_dump_json(indent=2))
        return

    # Formatted Terminal Report
    print("\n======================================================================")
    print("  BHIV CLO AGENT — EVIDENCE-BACKED REASONING REPORT                  ")
    print("======================================================================")
    print(f"  Trace ID:          {response.trace_id}")
    print(f"  Evaluation Date:   {response.as_of_date_applied}")
    print(f"  Evidence Status:   {response.evidence_status}")
    print(f"  VAJRA Trust Gate:  {response.vajra_trust_status}")
    print(f"  Human Review Req:  {response.human_review_required}")
    print("----------------------------------------------------------------------")
    print("  QUERY:")
    print(f"  \"{response.query}\"")
    print("----------------------------------------------------------------------")
    print("  CONCLUSION:")
    if response.conclusion:
        print(f"  {response.conclusion}")
    else:
        print("  [REFUSED TO CONCLUDE] Zero evidence in canonical corpus (Rule 5 Enforced).")
    print("----------------------------------------------------------------------")

    if response.conflicts_identified:
        print("  CONFLICTS / SUPERSESSIONS SURFACED:")
        for c in response.conflicts_identified:
            print(f"  ⚠ {c}")
        print("----------------------------------------------------------------------")

    print(f"  VERBATIM STATUTORY EVIDENCE ({len(response.evidence_passages)} passage(s) retrieved):")
    for i, p in enumerate(response.evidence_passages, 1):
        print(f"\n  [{i}] {p.document_title}")
        print(f"      Designation:    {p.section_number} — {p.heading}")
        print(f"      Version Status: {p.version_status_as_of_date} (as of {response.as_of_date_applied})")
        print(f"      Official URL:   {p.source_url}")
        print(f"      Effective Date: {p.effective_date}")
        print(f"      Verbatim Text:  \"{p.verbatim_passage}\"")

    print("\n----------------------------------------------------------------------")
    print("  LIMITATIONS:")
    for lim in response.limitations:
        print(f"  • {lim}")

    if response.human_review_required:
        print("\n  MANDATORY HUMAN REVIEW TRIGGERS:")
        for r in response.review_reasons:
            print(f"  🚩 {r}")

    print("\n  MDU AUDIT EVENT IDS:")
    for ev_id in response.mdu_provenance_event_ids:
        print(f"  ✓ {ev_id}")
    print("======================================================================\n")


if __name__ == "__main__":
    main()
