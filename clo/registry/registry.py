"""
Canonical Legal Registry
Manages ingestion, retrieval, integrity hashing, and temporal status evaluation
for canonical legal documents. Aligned with MDU dataset provenance.
"""

from datetime import datetime, timezone
import re
from typing import Dict, List, Optional, Tuple
from ..schemas.models import (
    LegalDocument,
    LegalPassage,
    LegalRelation,
    DocumentStatus,
    RelationType,
)
from .corpus import build_canonical_corpus

STOP_WORDS = {
    "what", "which", "when", "where", "who", "whom", "this", "that", "these", "those",
    "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "having", "do", "does", "did", "doing", "would", "should", "could", "ought", "the",
    "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by",
    "for", "with", "about", "against", "between", "into", "through", "during", "before",
    "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off",
    "over", "under", "again", "further", "then", "once", "here", "there", "all", "any",
    "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not",
    "only", "own", "same", "so", "than", "too", "very", "can", "will", "just", "don",
    "now", "law", "laws", "rule", "rules", "act", "acts", "section", "sections"
}


class CanonicalLegalRegistry:
    """Canonical Legal Registry holding authoritative statutory documents and relations."""

    def __init__(self):
        self._corpus: Dict[str, LegalDocument] = build_canonical_corpus()

    def get_document(self, document_id: str) -> Optional[LegalDocument]:
        return self._corpus.get(document_id)

    def list_documents(self) -> List[LegalDocument]:
        return list(self._corpus.values())

    def get_document_status_as_of(
        self, document_id: str, as_of_date_str: str
    ) -> Tuple[DocumentStatus, str]:
        """
        Determines the legal status of a document on an explicit as-of date (YYYY-MM-DD).
        Evaluates enactment dates, amendment dates, and supersession/repeal dates.
        """
        doc = self._corpus.get(document_id)
        if not doc:
            return DocumentStatus.UNKNOWN, f"Document '{document_id}' not found in canonical registry."

        try:
            as_of_date = datetime.strptime(as_of_date_str, "%Y-%m-%d").date()
            eff_date = datetime.strptime(doc.effective_date, "%Y-%m-%d").date()
        except ValueError:
            return DocumentStatus.UNKNOWN, f"Invalid date format: {as_of_date_str}. Must be YYYY-MM-DD."

        if as_of_date < eff_date:
            return DocumentStatus.UNKNOWN, f"Not yet in force as of {as_of_date_str} (effective: {doc.effective_date})."

        # Check for supersession or replacement relations
        for rel in doc.relations:
            rel_eff = datetime.strptime(rel.effective_date, "%Y-%m-%d").date()
            if rel.relation_type in (RelationType.SUPERSEDED_BY, RelationType.REPEALED_BY):
                if as_of_date >= rel_eff:
                    return DocumentStatus.SUPERSEDED, f"Superseded on {rel.effective_date} by {rel.target_document_id}."
            elif rel.relation_type == RelationType.AMENDED_BY:
                if as_of_date >= rel_eff:
                    return DocumentStatus.AMENDED, f"Amended on {rel.effective_date} by {rel.target_document_id}."

        # If it reached here, check if another document in corpus replaced it
        for other_doc in self._corpus.values():
            for rel in other_doc.relations:
                if rel.target_document_id == document_id and rel.relation_type == RelationType.REPLACES:
                    rel_eff = datetime.strptime(rel.effective_date, "%Y-%m-%d").date()
                    if as_of_date >= rel_eff:
                        return DocumentStatus.SUPERSEDED, f"Replaced on {rel.effective_date} by {other_doc.document_id}."

        if doc.status == DocumentStatus.SUPERSEDED:
            # Check if as_of_date is prior to the supersession event
            for rel in doc.relations:
                if rel.relation_type == RelationType.SUPERSEDED_BY:
                    rel_eff = datetime.strptime(rel.effective_date, "%Y-%m-%d").date()
                    if as_of_date < rel_eff:
                        return DocumentStatus.CURRENT, f"Was active law on {as_of_date_str} prior to supersession on {rel.effective_date}."

        return doc.status, f"Valid status on {as_of_date_str}."

    def search_passages(
        self,
        query: str,
        as_of_date_str: Optional[str] = None,
        jurisdiction: Optional[str] = "India",
    ) -> List[Tuple[LegalDocument, LegalPassage, DocumentStatus, str]]:
        """
        Searches canonical passages matching query tokens.
        Filters stop words and requires substantive domain token hits.
        Preserves source provenance, verbatim passages, and evaluated temporal status.
        """
        results: List[Tuple[LegalDocument, LegalPassage, DocumentStatus, str]] = []
        raw_words = re.findall(r"[a-zA-Z0-9]+", query.lower())
        substantive_tokens = [w for w in raw_words if len(w) >= 3 and w not in STOP_WORDS]

        if not substantive_tokens:
            return results

        if not as_of_date_str:
            as_of_date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        scored_results: List[Tuple[int, LegalDocument, LegalPassage, DocumentStatus, str]] = []

        for doc in self._corpus.values():
            if jurisdiction and doc.jurisdiction.lower() != jurisdiction.lower():
                continue

            status, status_reason = self.get_document_status_as_of(doc.document_id, as_of_date_str)

            for passage in doc.sections:
                p_text_lower = passage.text.lower()
                p_heading_lower = passage.heading.lower()
                keywords = [k.lower() for k in passage.keywords]

                # Match scoring
                score = 0
                for token in substantive_tokens:
                    # Exact keyword match gives high weight
                    if any(token == kw or token in kw for kw in keywords):
                        score += 3
                    if token in p_heading_lower:
                        score += 2
                    if token in p_text_lower:
                        score += 1

                # Require a minimum score threshold of 2 to avoid spurious single-word hits
                if score >= 2:
                    scored_results.append((score, doc, passage, status, status_reason))

        # Sort descending by score
        scored_results.sort(key=lambda x: x[0], reverse=True)
        return [(doc, passage, status, reason) for _, doc, passage, status, reason in scored_results]

    def get_relations_for_document(self, document_id: str) -> List[LegalRelation]:
        doc = self._corpus.get(document_id)
        if not doc:
            return []
        return doc.relations
