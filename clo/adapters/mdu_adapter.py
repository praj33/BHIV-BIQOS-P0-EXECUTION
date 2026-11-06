"""
MDU (Metadata & Data Understanding) Lineage Adapter
Implements alignment with MDU's canonical append-only event stream model
(ORIGIN, INGESTION, VALIDATION, RETRIEVAL) to close lineage gaps without silent canon creation.
"""

from datetime import datetime, timezone
import hashlib
import json
import uuid
from typing import List, Dict, Any, Optional
from ..schemas.models import MduProvenanceEvent, LegalDocument


class MduLineageAdapter:
    """Manages append-only provenance event logs conforming to MDU architecture."""

    def __init__(self):
        self._events: List[MduProvenanceEvent] = []

    def record_event(
        self,
        dataset_id: str,
        event_type: str,
        actor: str,
        details: Dict[str, Any],
        payload_bytes: Optional[bytes] = None,
    ) -> MduProvenanceEvent:
        """Records an append-only provenance event with deterministic SHA-256 evidence hashing."""
        event_id = f"mdu-ev-{uuid.uuid4().hex[:12]}"
        timestamp = datetime.now(timezone.utc).isoformat()

        if payload_bytes:
            ev_hash = hashlib.sha256(payload_bytes).hexdigest()
        else:
            raw_data = json.dumps(details, sort_keys=True).encode("utf-8")
            ev_hash = hashlib.sha256(raw_data).hexdigest()

        event = MduProvenanceEvent(
            event_id=event_id,
            dataset_id=dataset_id,
            event_type=event_type,
            timestamp=timestamp,
            actor=actor,
            evidence_hash=ev_hash,
            details=details,
        )
        self._events.append(event)
        return event

    def register_document_origin(self, doc: LegalDocument, actor: str = "CLO_BUILD_OWNER_ANSH") -> MduProvenanceEvent:
        """Records the canonical ORIGIN event for a legal document."""
        return self.record_event(
            dataset_id=doc.mdu_dataset_id,
            event_type="ORIGIN",
            actor=actor,
            details={
                "document_id": doc.document_id,
                "title": doc.title,
                "source_url": doc.source_url,
                "issuing_authority": doc.issuing_authority,
                "publication_date": doc.publication_date,
                "effective_date": doc.effective_date,
                "version": doc.version,
                "status": doc.status.value,
            },
            payload_bytes=doc.sha256_hash.encode("utf-8"),
        )

    def record_retrieval_lineage(
        self,
        dataset_id: str,
        trace_id: str,
        query: str,
        matched_sections: List[str],
        actor: str = "CLO_RUNTIME_SERVICE",
    ) -> MduProvenanceEvent:
        """Records governed retrieval provenance into MDU event stream."""
        return self.record_event(
            dataset_id=dataset_id,
            event_type="RETRIEVAL",
            actor=actor,
            details={
                "trace_id": trace_id,
                "query": query,
                "matched_sections": matched_sections,
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
            },
        )

    def get_event_stream(self, dataset_id: Optional[str] = None) -> List[MduProvenanceEvent]:
        """Returns the full chronological event stream or filtered by dataset."""
        if not dataset_id:
            return list(self._events)
        return [e for e in self._events if e.dataset_id == dataset_id]
