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
    # Check temporal status on as-of 2024-01-15: DPDP Sec 8 is PENDING_COMMENCEMENT per G.S.R. 843(E)
    assert dpdp_passage.version_status_as_of_date == "PENDING_COMMENCEMENT"
    it_43a_passages = [p for p in legal_output.evidence_passages if p.document_id == "doc-in-it-amendment-act-2008"]
    assert len(it_43a_passages) >= 1
    assert it_43a_passages[0].version_status_as_of_date == "CURRENT"
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


def test_full_7_hop_target_integration_flow_via_rest_api(client, vajra, insightflow):
    """
    Executes and asserts every hop in the canonical target flow via the FastAPI HTTP endpoints:
    Hop 1: CLO Legal Knowledge (GET /api/v1/clo/documents)
    Hop 2: Legal Intelligence (POST /api/v1/clo/research)
    Hop 3: Agent Composition (Evaluated in response envelope)
    Hop 4: TANTRA Contracts & Execution (POST /api/v1/clo/tantra/workload)
    Hop 5: VAJRA Trust & Identity (VAJRA authorization check & Rule 8 Bounded Agent)
    Hop 6: Bucket Evidence / Provenance (TruthStore + GET /api/v1/clo/mdu-lineage)
    Hop 7: InsightFlow Observability (Passive telemetry stream verification)
    """
    trace_id = "trace-flow-7hop-rest-002"
    execution_id = "exec-flow-7hop-rest-002"
    as_of_date = "2024-01-15"
    caller = "ansh_clo_build_owner"
    token = "ANSH_CLO_GOVERNED_SESSION"

    # =========================================================================
    # HOP 1: CLO Legal Knowledge (via REST API)
    # =========================================================================
    doc_res = client.get("/api/v1/clo/documents")
    assert doc_res.status_code == 200, "Hop 1 API Failed: GET /api/v1/clo/documents failed"
    docs = doc_res.json()
    assert len(docs) == 8, "Hop 1 API Failed: Canonical registry must contain 8 official statutes"
    dpdp = next(d for d in docs if d["document_id"] == "doc-in-dpdp-act-2023")
    assert dpdp["source_url"].startswith("https://egazette.gov.in"), "Hop 1 API Failed: Missing Gazette URL"
    assert len(dpdp["sha256_hash"]) == 64, "Hop 1 API Failed: Missing integrity SHA-256"

    # =========================================================================
    # HOP 2, 3, 5, 6, 7: Legal Intelligence & Agent Composition via POST /api/v1/clo/research
    # =========================================================================
    query_payload = {
        "query": "What are reasonable security safeguards to prevent personal data breach?",
        "as_of_date": as_of_date,
        "jurisdiction": "India",
        "trace_id": trace_id,
        "caller_identity": caller,
        "auth_token": token,
    }
    research_res = client.post("/api/v1/clo/research", json=query_payload)
    assert research_res.status_code == 200, f"Hop 2 API Failed: {research_res.text}"
    rdata = research_res.json()

    # HOP 2: Legal Intelligence assertions
    assert rdata["conclusion"] is not None, "Hop 2 API Failed: Missing conclusion"
    assert len(rdata["evidence_passages"]) >= 1, "Hop 2 API Failed: Missing evidence passages"
    dpdp_passages = [p for p in rdata["evidence_passages"] if p["document_id"] == "doc-in-dpdp-act-2023"]
    assert len(dpdp_passages) >= 1
    assert "reasonable security safeguards to prevent personal data breach" in dpdp_passages[0]["verbatim_passage"]
    assert dpdp_passages[0]["version_status_as_of_date"] == "PENDING_COMMENCEMENT"
    it_43a_passages = [p for p in rdata["evidence_passages"] if p["document_id"] == "doc-in-it-amendment-act-2008"]
    assert len(it_43a_passages) >= 1
    assert it_43a_passages[0]["version_status_as_of_date"] == "CURRENT"
    assert rdata["tantra_execution_id"] is not None and len(rdata["tantra_execution_id"]) > 0
    assert len(rdata["conflicts_identified"]) >= 1, "Hop 2 API Failed: Conflict not surfaced"

    # HOP 3: Agent Composition assertions
    assert rdata["human_review_required"] is True, "Hop 3 API Failed: Human review flag not raised"
    assert len(rdata["review_reasons"]) >= 1, "Hop 3 API Failed: Missing review reasons"
    assert len(rdata["limitations"]) >= 3, "Hop 3 API Failed: Missing executive limitations"

    # =========================================================================
    # HOP 4: TANTRA Contracts and Execution (via REST API)
    # =========================================================================
    tantra_payload = {
        "workload": json.dumps({
            "query": query_payload["query"],
            "as_of_date": as_of_date,
            "jurisdiction": "India",
            "composed_by": "BIQOS_AGENT_COMPOSITION_LAYER",
            "executive_review_required": rdata["human_review_required"]
        }),
        "trace_id": trace_id,
        "execution_id": execution_id,
        "bridge_signature": "Bearer VERIFIED_TANTRA_BRIDGE_TOKEN"
    }
    tantra_res = client.post("/api/v1/clo/tantra/workload", json=tantra_payload)
    assert tantra_res.status_code == 200, f"Hop 4 API Failed: {tantra_res.text}"
    tdata = tantra_res.json()
    assert tdata["status"] == "completed", "Hop 4 API Failed: Workload status not completed"
    assert tdata["trace_id"] == trace_id, "Hop 4 API Failed: trace_id broken"
    assert tdata["execution_id"] == execution_id, "Hop 4 API Failed: execution_id broken"
    assert len(tdata["result"]["execution_hash"]) == 64, "Hop 4 API Failed: Missing execution hash"
    assert tdata["artifact_location"] == f"artifacts/{trace_id}/{execution_id}"

    # =========================================================================
    # HOP 5: VAJRA Trust and Identity
    # =========================================================================
    state_view = vajra.get_agent_state_view()
    assert state_view["rule_8_bounded_guard"] == "ENFORCED", "Hop 5 API Failed: Rule 8 not enforced"
    assert state_view["direct_mutation_allowed"] is False, "Hop 5 API Failed: Direct mutation must be False"
    assert rdata["vajra_trust_status"].startswith("VERIFIED"), "Hop 5 API Failed: VAJRA trust status not verified"

    # =========================================================================
    # HOP 6: Bucket Evidence / Provenance
    # =========================================================================
    truth_rec = vajra.record_truthstore_evidence(
        trace_id=trace_id,
        payload=tdata["result"],
        token="CANONICAL_VAJRA_TANTRA_SECRET",
        subject=caller,
    )
    assert truth_rec["verified"] is True, "Hop 6 API Failed: TruthStore record verification failed"
    assert truth_rec["evidence_hash"].startswith("sha256:"), "Hop 6 API Failed: TruthStore hash missing"

    mdu_res = client.get("/api/v1/clo/mdu-lineage")
    assert mdu_res.status_code == 200, "Hop 6 API Failed: GET /api/v1/clo/mdu-lineage failed"
    mdu_events = mdu_res.json()
    assert len(mdu_events) >= 1
    retrieval_events = [ev for ev in mdu_events if ev["event_type"] == "RETRIEVAL" and ev["details"].get("trace_id") == trace_id]
    assert len(retrieval_events) >= 1, "Hop 6 API Failed: Retrieval lineage event not found in MDU stream"
    assert retrieval_events[0]["actor"] == caller

    # =========================================================================
    # HOP 7: InsightFlow Observability
    # =========================================================================
    telemetry_events = insightflow.get_emitted_events(trace_id=trace_id)
    assert len(telemetry_events) >= 1, "Hop 7 API Failed: No telemetry recorded for trace"
    assert telemetry_events[0].passive is True, "Hop 7 API Failed: Passive guarantee violated"
    assert telemetry_events[0].source == "clo-agent", "Hop 7 API Failed: Source must be clo-agent"
    assert telemetry_events[0].trace_id == trace_id, "Hop 7 API Failed: Telemetry trace_id broken"

