"""
CLO Agent Runtime API
FastAPI service exposing typed, documented, evidence-first endpoints for legal research,
compliance analysis, temporal status evaluation, and TANTRA execution participation.
"""

from datetime import datetime, timezone
import uuid
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Header, Depends, status
from fastapi.responses import JSONResponse

from ..schemas.models import (
    LegalQueryRequest,
    LegalReasoningResponse,
    LegalDocument,
    MduProvenanceEvent,
    TantraWorkloadRequest,
    TantraWorkloadResponse,
)
from ..registry.registry import CanonicalLegalRegistry
from ..reasoning.engine import LegalReasoningEngine
from ..adapters.mdu_adapter import MduLineageAdapter
from ..adapters.tantra_adapter import TantraExecutionAdapter
from ..adapters.vajra_adapter import VajraTrustAdapter
from ..adapters.insightflow_adapter import InsightFlowTelemetryAdapter

app = FastAPI(
    title="BHIV CLO Agent Runtime API",
    description="Chief Legal Officer Agent increment for the BHIV / BIQOS Ecosystem. "
                "Evidence-first legal reasoning, temporal as-of-date evaluation, "
                "and constitutional integration with TANTRA and VAJRA.",
    version="1.0.0-p0",
)

# Initialize core singletons
registry = CanonicalLegalRegistry()
reasoning_engine = LegalReasoningEngine(registry=registry)
mdu_adapter = MduLineageAdapter()
vajra_adapter = VajraTrustAdapter()
tantra_adapter = TantraExecutionAdapter(engine=reasoning_engine)
insightflow_adapter = InsightFlowTelemetryAdapter()

# Seed MDU origin events for all 8 canonical documents on startup
for doc in registry.list_documents():
    mdu_adapter.register_document_origin(doc, actor="CLO_BUILD_OWNER_ANSH")


@app.get("/health", tags=["System"])
def health_check() -> Dict[str, Any]:
    """Returns service health, canonical corpus inventory, and subsystem integration status."""
    return {
        "service": "bhiv-clo-agent-runtime",
        "version": "1.0.0-p0",
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "canonical_registry": {
            "document_count": len(registry.list_documents()),
            "jurisdiction": "India",
            "statutes": [doc.document_id for doc in registry.list_documents()],
        },
        "adapters": {
            "mdu_lineage": "ACTIVE_APPEND_ONLY",
            "tantra_execution": "READY_PARTICIPANT",
            "vajra_trust": "ENFORCING_8_STATE_LIFECYCLE",
            "insightflow": "PASSIVE_EMITTER_ACTIVE",
        },
        "governance": {
            "rule_5_evidence_guard": "ENFORCED",
            "rule_8_bounded_agent": "ENFORCED",
            "silent_canon_creation": "FORBIDDEN",
        }
    }


@app.post(
    "/api/v1/clo/research",
    response_model=LegalReasoningResponse,
    tags=["Legal Reasoning"],
    status_code=status.HTTP_200_OK,
)
def research_legal_query(
    request: LegalQueryRequest,
    authorization: Optional[str] = Header(None),
) -> LegalReasoningResponse:
    """
    Executes an evidence-first legal research query over canonical public legal sources.
    Evaluates temporal as-of-date validity, surfaces conflicts, enforces zero-evidence refusal,
    and records MDU provenance and InsightFlow telemetry.
    """
    trace_id = request.trace_id or f"trace-clo-{uuid.uuid4().hex[:12]}"
    caller = request.caller_identity or "ansh_clo_build_owner"
    token = request.auth_token or authorization

    # 1. VAJRA Authority Verification (Fail-closed)
    auth_result = vajra_adapter.verify_authority(
        subject=caller,
        action="legal:research",
        trace_id=trace_id,
        token=token,
    )
    if not auth_result.allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "VAJRA_AUTHORITY_DENIED",
                "reason": auth_result.reason,
                "current_state": auth_result.current_state,
                "subject": caller,
            }
        )

    # 2. Execute Reasoning over Corpus
    response = reasoning_engine.reason_over_query(request)
    response.trace_id = trace_id
    response.vajra_trust_status = f"VERIFIED: {auth_result.current_state}"

    # 3. Record MDU Provenance Event
    matched_sections = [f"{p.document_id}#{p.section_number}" for p in response.evidence_passages]
    ev = mdu_adapter.record_retrieval_lineage(
        dataset_id="ds-legal-aggregate-query",
        trace_id=trace_id,
        query=request.query,
        matched_sections=matched_sections,
        actor=caller,
    )
    response.mdu_provenance_event_ids.append(ev.event_id)

    # 4. Emit Passive InsightFlow Telemetry
    insightflow_adapter.emit_telemetry_event(
        trace_id=trace_id,
        execution_id=f"exec-clo-{uuid.uuid4().hex[:8]}",
        event_type="legal_reasoning_query",
        status=response.evidence_status,
        payload={
            "query": request.query,
            "as_of_date": response.as_of_date_applied,
            "evidence_count": len(response.evidence_passages),
            "human_review_required": response.human_review_required,
        }
    )

    return response


@app.post(
    "/api/v1/clo/analyse",
    response_model=LegalReasoningResponse,
    tags=["Legal Reasoning"],
)
def analyse_compliance(
    request: LegalQueryRequest,
    authorization: Optional[str] = Header(None),
) -> LegalReasoningResponse:
    """Performs structured legal compliance and liability analysis with review triggers."""
    return research_legal_query(request, authorization=authorization)


@app.get("/api/v1/clo/documents", response_model=List[LegalDocument], tags=["Registry"])
def list_canonical_documents() -> List[LegalDocument]:
    """Returns the manifest of all 8 canonical public legal documents in the registry."""
    return registry.list_documents()


@app.get("/api/v1/clo/documents/{document_id}", response_model=LegalDocument, tags=["Registry"])
def get_canonical_document(document_id: str) -> LegalDocument:
    """Returns details, statutory passages, and amendment relations for a single document."""
    doc = registry.get_document(document_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document '{document_id}' not found in canonical legal registry."
        )
    return doc


@app.get("/api/v1/clo/mdu-lineage", response_model=List[MduProvenanceEvent], tags=["Provenance"])
def get_mdu_lineage_stream(dataset_id: Optional[str] = None) -> List[MduProvenanceEvent]:
    """Returns the chronological MDU append-only provenance event stream."""
    return mdu_adapter.get_event_stream(dataset_id=dataset_id)


@app.post("/api/v1/clo/tantra/workload", response_model=TantraWorkloadResponse, tags=["TANTRA Participant"])
def execute_tantra_workload(request: TantraWorkloadRequest) -> TantraWorkloadResponse:
    """
    Executes workload according to TANTRA Execution Service Contract (`services/execution/EXECUTION_CONTRACT.md`).
    Enforces bridge signature verification and returns deterministic execution hash.
    """
    try:
        return tantra_adapter.execute_participant_workload(request)
    except PermissionError as pe:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(pe)
        )
