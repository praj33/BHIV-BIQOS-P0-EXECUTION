"""
CLO Legal Reasoning Foundation & Temporal Engine
Implements evidence-first query resolution, as-of-date legal temporal status,
supersession/amendment tracking, conflict surfacing, and zero-evidence refusal per Rule 5.
"""

from datetime import datetime, timezone
import uuid
from typing import List, Dict, Optional, Tuple
from ..schemas.models import (
    LegalQueryRequest,
    LegalReasoningResponse,
    EvidencePassage,
    DocumentStatus,
    RelationType,
)
from ..registry.registry import CanonicalLegalRegistry


class LegalReasoningEngine:
    """Core legal intelligence and temporal reasoning engine for CLO Agent."""

    def __init__(self, registry: Optional[CanonicalLegalRegistry] = None):
        self.registry = registry or CanonicalLegalRegistry()

    def reason_over_query(self, request: LegalQueryRequest) -> LegalReasoningResponse:
        """
        Executes evidence-first legal reasoning over the canonical corpus.
        Preserves statutory provenance, evaluates as-of-date status, surfaces conflicts,
        and refuses conclusions when evidence is absent (Rule 5).
        """
        trace_id = request.trace_id or f"trace-clo-{uuid.uuid4().hex[:12]}"
        as_of_date = request.as_of_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # 1. Search canonical passages
        raw_results = self.registry.search_passages(
            query=request.query,
            as_of_date_str=as_of_date,
            jurisdiction=request.jurisdiction,
        )

        # 2. Hard Rule 5: Zero evidence -> Refuse legal conclusion
        if not raw_results:
            return LegalReasoningResponse(
                trace_id=trace_id,
                query=request.query,
                as_of_date_applied=as_of_date,
                conclusion=None,
                evidence_status="INSUFFICIENT_EVIDENCE",
                evidence_passages=[],
                source_version_status={},
                conflicts_identified=[],
                limitations=[
                    "No verified statutory provisions found in canonical corpus matching query terms.",
                    "Per BHIV Constitutional Rule 5: Zero evidence means zero legal conclusion. Agent refuses to speculate."
                ],
                human_review_required=True,
                review_reasons=[
                    "INSUFFICIENT_CANONICAL_EVIDENCE: Query cannot be grounded in official gazette sources. Mandatory human legal review required."
                ],
                mdu_provenance_event_ids=[]
            )

        # 3. Build Evidence Passages preserving source provenance & verbatim text
        evidence_passages: List[EvidencePassage] = []
        source_version_status: Dict[str, str] = {}
        conflicts: List[str] = []
        review_reasons: List[str] = []
        has_superseded_evidence = False
        has_transitional_evidence = False
        has_penal_provision = False

        for doc, passage, status, status_reason in raw_results:
            status_str = status.value
            source_version_status[doc.document_id] = f"{status_str}: {status_reason}"

            if status == DocumentStatus.SUPERSEDED:
                has_superseded_evidence = True
            elif status == DocumentStatus.TRANSITIONAL:
                has_transitional_evidence = True

            if any(term in passage.text.lower() for term in ["punish", "imprisonment", "fine", "penalty", "liable"]):
                has_penal_provision = True

            evidence_passages.append(
                EvidencePassage(
                    document_id=doc.document_id,
                    document_title=doc.title,
                    section_number=passage.section_number,
                    heading=passage.heading,
                    verbatim_passage=passage.text,
                    version=doc.version,
                    version_status_as_of_date=status_str,
                    source_url=doc.source_url,
                    effective_date=passage.effective_date,
                )
            )

        # 4. Conflict & Supersession Detection Logic
        # Check if query touches both IT Rules 2011 and IT Rules 2021
        doc_ids = {p.document_id for p in evidence_passages}
        if "doc-in-it-intermediary-rules-2011" in doc_ids and "doc-in-it-rules-2021" in doc_ids:
            conflicts.append(
                f"Temporal Supersession Conflict: Query retrieves both IT Rules 2011 (superseded) and IT Rules 2021 (active). "
                f"Under as-of-date {as_of_date}, the 2021 rules prevail with a 15-day grievance resolution and 24-hour ack mandate, "
                f"whereas 2011 rules allowed 1-month turnaround."
            )

        # Check if query touches Section 43A of IT Act and DPDP Act 2023 Section 44
        if "doc-in-it-amendment-act-2008" in doc_ids and "doc-in-dpdp-act-2023" in doc_ids:
            conflicts.append(
                f"Statutory Transition Notice: Section 43A of IT Act 2000 (reasonable security practices and compensation) "
                f"is omitted by Section 44 of DPDP Act 2023. As-of-date {as_of_date} governs whether Section 43A or DPDP Section 8 applies."
            )

        # 5. Formulate Evidence-Backed Conclusion
        evidence_status = "CONFLICT_DETECTED" if conflicts else "EVIDENCE_VERIFIED"
        
        # Synthesize grounded summary citing explicit sections
        citations = [f"{p.document_title} ({p.section_number} - {p.heading})" for p in evidence_passages[:3]]
        conclusion = (
            f"Ground-truth statutory analysis as of {as_of_date}: "
            f"Grounded directly in {len(evidence_passages)} verifiable statutory provision(s) across {len(doc_ids)} document(s): "
            + "; ".join(citations) + ". "
            + ("Direct conflicts/supersessions surfaced between retrieved versions." if conflicts else "Provisions are authoritative and active.")
        )

        # 6. Establish Limitations
        limitations = [
            f"Statutory analysis strictly evaluated as of temporal date: {as_of_date}.",
            "Source passages quoted verbatim from official Gazette notifications and IndiaCode canonical repositories.",
            "This automated synthesis constitutes legal information and reasoning support under BIQOS; it does not replace formal counsel sign-off.",
            "Judicial interpretations and High Court / Supreme Court stays are subject to external case-law verification."
        ]

        # 7. Human Review Triggers
        human_review_required = False
        if conflicts:
            human_review_required = True
            review_reasons.append("STATUTORY_CONFLICT_DETECTED: Overlapping or superseded legal instruments identified.")
        if has_superseded_evidence:
            human_review_required = True
            review_reasons.append("SUPERSEDED_LAW_REFERENCED: Query involves statutory provisions that have undergone legislative repeal or replacement.")
        if has_transitional_evidence:
            human_review_required = True
            review_reasons.append("TRANSITIONAL_REGIME: Legal provisions are currently transitioning between legacy and new statutory frameworks.")
        if has_penal_provision:
            human_review_required = True
            review_reasons.append("PENAL_OR_LIABILITY_RISK: Retrieved provisions contain statutory penalties, corporate liability, or criminal offenses.")

        # If zero triggers hit, standard review flag for CLO governance
        if not review_reasons:
            review_reasons.append("ROUTINE_AUDIT: Standard CLO governance review for executive consumption.")

        return LegalReasoningResponse(
            trace_id=trace_id,
            query=request.query,
            as_of_date_applied=as_of_date,
            conclusion=conclusion,
            evidence_status=evidence_status,
            evidence_passages=evidence_passages,
            source_version_status=source_version_status,
            conflicts_identified=conflicts,
            limitations=limitations,
            human_review_required=human_review_required,
            review_reasons=review_reasons,
            mdu_provenance_event_ids=[]
        )
