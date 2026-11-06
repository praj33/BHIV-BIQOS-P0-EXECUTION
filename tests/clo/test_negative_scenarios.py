"""
Scenario 6: Negative Scenarios & Rule 5 Enforcement
Validates strict refusal to conclude when evidence is absent (Rule 5),
conflict surfacing without silent resolution, and malformed input handling.
"""

from fastapi.testclient import TestClient
from clo.reasoning.engine import LegalReasoningEngine
from clo.schemas.models import LegalQueryRequest


def test_hard_rule_5_zero_evidence_refusal(client: TestClient):
    """
    Hard Rule 5: Zero evidence means zero legal conclusion.
    Query on an entirely unevidenced matter must refuse to conclude, return conclusion=None,
    mark evidence_status='INSUFFICIENT_EVIDENCE', and flag human_review_required=True.
    """
    payload = {
        "query": "What is the maximum allowed warp speed of interstellar spacecraft under Indian maritime law?",
        "as_of_date": "2024-01-01",
        "caller_identity": "ansh_clo_build_owner",
        "trace_id": "trace-neg-zero-evidence"
    }

    response = client.post("/api/v1/clo/research", json=payload)
    assert response.status_code == 200
    data = response.json()

    # Strict Rule 5 assertions
    assert data["conclusion"] is None, "Rule 5 Violation: Agent produced conclusion without evidence!"
    assert data["evidence_status"] == "INSUFFICIENT_EVIDENCE"
    assert len(data["evidence_passages"]) == 0
    assert data["human_review_required"] is True
    assert any("INSUFFICIENT_CANONICAL_EVIDENCE" in r for r in data["review_reasons"])
    assert any("Rule 5" in lim for lim in data["limitations"])


def test_conflicting_sources_explicitly_surfaced(engine: LegalReasoningEngine):
    """
    Verifies that when a query matches overlapping or amended statutory provisions
    (e.g., Section 43A corporate liability vs DPDP Act Section 44 omission),
    the conflict is surfaced explicitly and NOT resolved silently.
    """
    req = LegalQueryRequest(
        query="What is corporate liability for compensation under section 43A and DPDP Act?",
        as_of_date="2024-01-01",
    )
    res = engine.reason_over_query(req)

    assert res.evidence_status in ("CONFLICT_DETECTED", "EVIDENCE_VERIFIED")
    assert len(res.conflicts_identified) >= 1
    assert any("Section 43A" in msg for msg in res.conflicts_identified)
    assert res.human_review_required is True


def test_invalid_date_format_handled_gracefully(engine: LegalReasoningEngine):
    """
    Verifies that an invalid date string does not crash the service with 500 error,
    falling back safely to temporal unknown.
    """
    req = LegalQueryRequest(
        query="What are director duties under Companies Act?",
        as_of_date="invalid-date-format-99999",
    )
    res = engine.reason_over_query(req)
    assert res.trace_id is not None
    # Response must be generated without unhandled exception
    assert res.as_of_date_applied == "invalid-date-format-99999"
