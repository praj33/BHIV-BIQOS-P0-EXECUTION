"""
CLO Domain Data Models & Integration Schemas
Aligned with MDU Provenance Model, TANTRA Execution Contract, and VAJRA Authority Substrate.
"""

from __future__ import annotations
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class DocumentStatus(str, Enum):
    CURRENT = "CURRENT"
    AMENDED = "AMENDED"
    SUPERSEDED = "SUPERSEDED"
    REPEALED = "REPEALED"
    TRANSITIONAL = "TRANSITIONAL"
    UNKNOWN = "UNKNOWN"


class RelationType(str, Enum):
    AMENDS = "AMENDS"
    AMENDED_BY = "AMENDED_BY"
    REPLACES = "REPLACES"
    SUPERSEDED_BY = "SUPERSEDED_BY"
    REFERENCES = "REFERENCES"
    REPEALED_BY = "REPEALED_BY"
    TRANSITIONAL_TO = "TRANSITIONAL_TO"


class LegalRelation(BaseModel):
    """Explicit legal relationship between two documents or sections."""
    model_config = ConfigDict(frozen=True)

    relation_type: RelationType = Field(..., description="Nature of legal relationship")
    target_document_id: str = Field(..., description="Canonical ID of related document")
    target_section: Optional[str] = Field(None, description="Section or clause identifier")
    effective_date: str = Field(..., description="Date the relation came into legal effect (YYYY-MM-DD)")
    description: str = Field(..., description="Legal rationale or citation")


class LegalPassage(BaseModel):
    """Verbatim legal statutory passage extracted from official source."""
    model_config = ConfigDict(frozen=True)

    section_id: str = Field(..., description="Unique section identifier")
    section_number: str = Field(..., description="Official section or rule designation")
    heading: str = Field(..., description="Statutory heading or title")
    text: str = Field(..., description="Verbatim statutory text as published in official gazette")
    keywords: List[str] = Field(default_factory=list, description="Keywords for retrieval indexing")
    effective_date: str = Field(..., description="Effective date of this passage version (YYYY-MM-DD)")
    amendment_history: Optional[str] = Field(None, description="Legislative amendment notes")


class LegalDocument(BaseModel):
    """Canonical legal document specification aligned with MDU dataset requirements."""
    document_id: str = Field(..., description="Canonical unique identifier (e.g., doc-in-dpdp-act-2023)")
    title: str = Field(..., description="Full official statutory title")
    short_name: str = Field(..., description="Recognized short form or acronym")
    issuing_authority: str = Field(..., description="Official legislative or executive issuing authority")
    jurisdiction: str = Field(..., description="Jurisdiction (e.g., India)")
    source_url: str = Field(..., description="Verifiable official public URL (e.g. egazette.gov.in)")
    publication_date: str = Field(..., description="Gazette notification date (YYYY-MM-DD)")
    effective_date: str = Field(..., description="Enforcement date (YYYY-MM-DD)")
    retrieval_date: str = Field(..., description="Date captured from public registry (YYYY-MM-DD)")
    version: str = Field(..., description="Version identifier")
    status: DocumentStatus = Field(..., description="Current statutory status")
    relations: List[LegalRelation] = Field(default_factory=list, description="Legal relations to other acts/rules")
    sections: List[LegalPassage] = Field(default_factory=list, description="Verbatim statutory passages")
    mdu_dataset_id: str = Field(..., description="Linked MDU canonical dataset identifier")
    sha256_hash: str = Field(..., description="Deterministic SHA-256 integrity hash of document text")


class MduProvenanceEvent(BaseModel):
    """MDU-compliant append-only provenance event record."""
    event_id: str = Field(..., description="Unique UUID for this provenance entry")
    dataset_id: str = Field(..., description="Canonical dataset identifier (e.g., ds-legal-it-act-2000)")
    event_type: str = Field(..., description="Lifecycle event type: ORIGIN, INGESTION, VALIDATION, RETRIEVAL")
    timestamp: str = Field(..., description="ISO 8601 UTC timestamp")
    actor: str = Field(..., description="Actor identity performing operation (e.g. CLO_BUILD_OWNER_ANSH)")
    evidence_hash: str = Field(..., description="SHA-256 hash of payload/evidence at this step")
    details: Dict[str, Any] = Field(default_factory=dict, description="Metadata and audit disclosures")


class LegalQueryRequest(BaseModel):
    """Input contract for CLO research and reasoning endpoints."""
    query: str = Field(..., description="Legal question or compliance query")
    as_of_date: Optional[str] = Field(None, description="Historical or current evaluation date (YYYY-MM-DD)")
    jurisdiction: Optional[str] = Field("India", description="Target jurisdiction filter")
    trace_id: Optional[str] = Field(None, description="Distributed execution trace ID")
    caller_identity: Optional[str] = Field(None, description="Identity of caller for VAJRA authority verification")
    auth_token: Optional[str] = Field(None, description="Bearer token for authority gate")


class EvidencePassage(BaseModel):
    """Evidence passage surviving in the output with full provenance."""
    document_id: str
    document_title: str
    section_number: str
    heading: str
    verbatim_passage: str
    version: str
    version_status_as_of_date: str
    source_url: str
    effective_date: str


class LegalReasoningResponse(BaseModel):
    """Evidence-first output contract for CLO Agent responses."""
    trace_id: str = Field(..., description="Trace identifier matching caller or generated by Core")
    query: str = Field(..., description="Original input query")
    as_of_date_applied: str = Field(..., description="Resolved evaluation date (YYYY-MM-DD)")
    conclusion: Optional[str] = Field(None, description="Legal reasoning conclusion (None if zero evidence)")
    evidence_status: str = Field(..., description="EVIDENCE_VERIFIED | INSUFFICIENT_EVIDENCE | CONFLICT_DETECTED")
    evidence_passages: List[EvidencePassage] = Field(default_factory=list, description="Verbatim statutory evidence")
    source_version_status: Dict[str, str] = Field(default_factory=dict, description="Status of each referenced doc")
    conflicts_identified: List[str] = Field(default_factory=list, description="Explicit legal conflicts detected")
    limitations: List[str] = Field(default_factory=list, description="Boundaries and limitations of legal output")
    human_review_required: bool = Field(..., description="Strict human-in-the-loop review flag")
    review_reasons: List[str] = Field(default_factory=list, description="Specific triggers requiring human review")
    mdu_provenance_event_ids: List[str] = Field(default_factory=list, description="MDU audit event IDs")
    tantra_execution_id: Optional[str] = Field(None, description="TANTRA execution identifier")
    vajra_trust_status: Optional[str] = Field(None, description="VAJRA verification verdict")


class TantraWorkloadRequest(BaseModel):
    """Complies with TANTRA services/execution/EXECUTION_CONTRACT.md POST /run."""
    workload: str
    trace_id: str
    execution_id: str
    bridge_signature: str


class TantraWorkloadResponse(BaseModel):
    """Complies with TANTRA services/execution/EXECUTION_CONTRACT.md response."""
    trace_id: str
    execution_id: str
    status: str
    result: Dict[str, Any]
    artifact_location: str
    duration_ms: int


class VajraVerifyRequest(BaseModel):
    """Complies with VAJRA POST /api/vajra/authority/verify."""
    subject: str
    action: str
    trace_id: str
    token: Optional[str] = None


class VajraVerifyResponse(BaseModel):
    """Complies with VAJRA authority verification response."""
    allowed: bool
    subject: str
    current_state: str
    action: str
    reason: Optional[str] = None


class InsightFlowTelemetryEvent(BaseModel):
    """Complies with services/insightflow/INTEGRATION_CONTRACT.md."""
    source: str = "tantra-bridge"
    trace_id: str
    execution_id: str
    event_type: str
    status: str
    payload: Dict[str, Any]
    timestamp: str
    passive: bool = True

