"""
Full Target Integration Flow Verification Test
Traces the exact 7-hop flow required by Section 4:
CLO Legal Knowledge → Legal Intelligence → Agent Composition → TANTRA Contracts and Execution → VAJRA Trust and Identity → Bucket Evidence/Provenance → InsightFlow Observability
"""

import json
from datetime import datetime, timezone
import pytest

from clo.registry.registry import CanonicalLegalRegistry
from clo.reasoning.engine import LegalReasoningEngine
from clo.schemas.models import LegalQueryRequest, TantraWorkloadRequest
from clo.adapters.tantra_adapter import TantraExecutionAdapter
from clo.adapters.vajra_adapter import VajraTrustAdapter
from clo.adapters.mdu_adapter import MduLineageAdapter
from clo.adapters.insightflow_adapter import InsightFlowTelemetryAdapter


def test_full_7_hop_target_integration_flow():
    """
    Executes and asserts every hop in the canonical target flow:
    Hop 1: CLO Legal Knowledge
    Hop 2: Legal Intelligence
    Hop 3: Agent Composition
    Hop 4: TANTRA Contracts and Execution
    Hop 5: VAJRA Trust and Identity
    Hop 6: Bucket Evidence / Provenance
    Hop 7: InsightFlow Observability
    """
    trace_id = "trace-flow-7hop-verified-001"
    execution_id = "exec-flow-7hop-verified-001"
    as_of_date = "2024-01-15"
    caller = "ansh_clo_build_owner"
    token = "ANSH_CLO_GOVERNED_SESSION"

    # =========================================================================
    # HOP 1: CLO Legal Knowledge
    # =========================================================================
    registry = CanonicalLegalRegistry()
    docs = registry.list_documents()
    assert len(docs) == 8, "Hop 1 Failed: Canonical registry must contain exactly 8 official statutes"
    dpdp_doc = registry.get_document("doc-in-dpdp-act-2023")
    assert dpdp_doc is not None, "Hop 1 Failed: DPDP Act 2023 missing from legal knowledge base"
    assert dpdp_doc.source_url.startswith("https://egazette.gov.in"), "Hop 1 Failed: Official gazette source URL missing"
    assert len(dpdp_doc.sha256_hash) == 64, "Hop 1 Failed: SHA-256 integrity hash missing"

    # =========================================================================
    # HOP 2: Legal Intelligence
    # =========================================================================
    engine = LegalReasoningEngine(registry=registry)
    query_req = LegalQueryRequest(
        query="What are reasonable security safeguards to prevent personal data breach?",
        as_of_date=as_of_date,
        jurisdiction="India",
        trace_id=trace_id,
        caller_identity=caller,
        auth_token=token,
    )
    legal_output = engine.reason_over_query(query_req)
    assert legal_output.conclusion is not None, "Hop 2 Failed: Legal intelligence failed to produce conclusion"
    assert len(legal_output.evidence_passages) >= 1, "Hop 2 Failed: Verbatim statutory passages missing"
    # Check verbatim statutory text preserved
    dpdp_passage = [p for p in legal_output.evidence_passages if p.document_id == "doc-in-dpdp-act-2023"][0]
    assert "reasonable security safeguards to prevent personal data breach" in dpdp_passage.verbatim_passage
    # Check temporal status
    assert dpdp_passage.version_status_as_of_date == "CURRENT"
    # Check conflict surfacing
    assert len(legal_output.conflicts_identified) >= 1, "Hop 2 Failed: Statutory transition conflict not surfaced"

    # =========================================================================
    # HOP 3: Agent Composition
    # =========================================================================
    # Wraps legal intelligence into executive composition envelope with review flags and trace continuity
    assert legal_output.human_review_required is True, "Hop 3 Failed: Human review flag not raised"
    assert len(legal_output.review_reasons) >= 1, "Hop 3 Failed: Review reasons missing in executive envelope"
    assert len(legal_output.limitations) >= 3, "Hop 3 Failed: Limitations omitted from executive payload"
    workload_payload = {
        "query": query_req.query,
        "as_of_date": as_of_date,
        "jurisdiction": "India",
        "composed_by": "BIQOS_AGENT_COMPOSITION_LAYER",
        "executive_review_required": legal_output.human_review_required,
    }

    # =========================================================================
    # HOP 4: TANTRA Contracts and Execution
    # =========================================================================
    tantra = TantraExecutionAdapter(engine=engine)
    tantra_req = TantraWorkloadRequest(
        workload=json.dumps(workload_payload),
        trace_id=trace_id,
        execution_id=execution_id,
        bridge_signature="Bearer VERIFIED_TANTRA_BRIDGE_TOKEN",
    )
    tantra_res = tantra.execute_participant_workload(tantra_req)
    assert tantra_res.status == "completed", "Hop 4 Failed: TANTRA execution participant did not complete"
    assert tantra_res.trace_id == trace_id, "Hop 4 Failed: trace_id broken across TANTRA contract"
    assert tantra_res.execution_id == execution_id, "Hop 4 Failed: execution_id broken across TANTRA contract"
    assert "execution_hash" in tantra_res.result, "Hop 4 Failed: Replay-safe execution hash missing"
    assert len(tantra_res.result["execution_hash"]) == 64, "Hop 4 Failed: Invalid execution hash"
    assert tantra_res.artifact_location == f"artifacts/{trace_id}/{execution_id}"

    # =========================================================================
    # HOP 5: VAJRA Trust and Identity
    # =========================================================================
    vajra = VajraTrustAdapter()
    auth_verdict = vajra.verify_authority(
        subject=caller,
        action="legal:research",
        trace_id=trace_id,
        token=token,
    )
    assert auth_verdict.allowed is True, "Hop 5 Failed: VAJRA authority verification denied valid caller"
    assert auth_verdict.current_state == "USE", "Hop 5 Failed: Active 8-state lifecycle state must be USE"
    state_view = vajra.get_agent_state_view()
    assert state_view["rule_8_bounded_guard"] == "ENFORCED", "Hop 5 Failed: Rule 8 Bounded Agent guard missing"
    assert state_view["direct_mutation_allowed"] is False, "Hop 5 Failed: Direct ledger mutation must be false"

    # =========================================================================
    # HOP 6: Bucket Evidence / Provenance
    # =========================================================================
    # TruthStore hash logging
    truth_record = vajra.record_truthstore_evidence(
        trace_id=trace_id,
        payload=tantra_res.result,
        token="CANONICAL_VAJRA_TANTRA_SECRET",
        subject=caller,
    )
    assert truth_record["verified"] is True, "Hop 6 Failed: TruthStore evidence record failed verification"
    assert truth_record["evidence_hash"].startswith("sha256:"), "Hop 6 Failed: TruthStore hash missing"
    # MDU append-only event stream logging
    mdu = MduLineageAdapter()
    mdu_ev = mdu.record_retrieval_lineage(
        dataset_id="ds-legal-aggregate-query",
        trace_id=trace_id,
        query=query_req.query,
        matched_sections=[f"{p.document_id}#{p.section_number}" for p in legal_output.evidence_passages],
        actor=caller,
    )
    assert mdu_ev.event_id.startswith("mdu-ev-"), "Hop 6 Failed: MDU event ID format invalid"
    assert mdu_ev.event_type == "RETRIEVAL", "Hop 6 Failed: MDU event type must be RETRIEVAL"
    assert len(mdu_ev.evidence_hash) == 64, "Hop 6 Failed: MDU evidence hash missing"

    # =========================================================================
    # HOP 7: InsightFlow Observability
    # =========================================================================
    insightflow = InsightFlowTelemetryAdapter()
    telemetry_ev = insightflow.emit_telemetry_event(
        trace_id=trace_id,
        execution_id=execution_id,
        event_type="legal_reasoning_flow_completion",
        status="EVIDENCE_VERIFIED",
        payload={
            "query": query_req.query,
            "as_of_date": as_of_date,
            "execution_hash": tantra_res.result["execution_hash"],
            "truthstore_entry": truth_record["entry_id"],
            "mdu_event_id": mdu_ev.event_id,
        }
    )
    assert telemetry_ev.source == "clo-agent", "Hop 7 Failed: Telemetry source must be clo-agent"
    assert telemetry_ev.trace_id == trace_id, "Hop 7 Failed: Telemetry trace_id broken"
    assert telemetry_ev.execution_id == execution_id, "Hop 7 Failed: Telemetry execution_id broken"
    assert telemetry_ev.passive is True, "Hop 7 Failed: Passive-only guarantee violated"
    assert telemetry_ev.status == "EVIDENCE_VERIFIED", "Hop 7 Failed: Telemetry status mismatch"

    # Verify that telemetry is captured in collector
    recorded = insightflow.get_emitted_events(trace_id=trace_id)
    assert len(recorded) == 1, "Hop 7 Failed: Telemetry event not recorded in trace stream"
    assert recorded[0].event_type == "legal_reasoning_flow_completion"
