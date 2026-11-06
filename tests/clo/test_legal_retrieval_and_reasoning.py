"""
Scenario 2: Legal Retrieval & Evidence Preservation
Tests that queries preserve verbatim statutory passages, source URLs, section numbers,
version status, limitations, and human review flags through the entire output envelope.
"""

from fastapi.testclient import TestClient


def test_evidence_preserved_in_data_protection_query(client: TestClient):
    """
    Queries DPDP Act 2023 obligations and verifies that evidence passages survive intact
    with verbatim statutory text, official URLs, and human review flags.
    """
    payload = {
        "query": "What are the security safeguards and obligations of a Data Fiduciary regarding personal data breach?",
        "as_of_date": "2024-01-15",
        "caller_identity": "ansh_clo_build_owner",
        "trace_id": "trace-test-evidence-001"
    }

    response = client.post("/api/v1/clo/research", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["trace_id"] == "trace-test-evidence-001"
    assert data["evidence_status"] in ("EVIDENCE_VERIFIED", "CONFLICT_DETECTED")
    assert data["as_of_date_applied"] == "2024-01-15"
    assert data["conclusion"] is not None
    assert len(data["evidence_passages"]) >= 1

    # Inspect the first evidence passage
    passage = data["evidence_passages"][0]
    assert passage["document_id"] in ("doc-in-dpdp-act-2023", "doc-in-it-amendment-act-2008", "doc-in-spdi-rules-2011")
    assert passage["source_url"].startswith("http")
    assert len(passage["verbatim_passage"]) > 20
    assert "personal data" in passage["verbatim_passage"].lower() or "data" in passage["verbatim_passage"].lower()
    assert passage["version_status_as_of_date"] in ("CURRENT", "AMENDED", "TRANSITIONAL")

    # Verify limitations survive
    assert len(data["limitations"]) >= 3
    assert any("2024-01-15" in lim for lim in data["limitations"])

    # Verify human review flag
    assert data["human_review_required"] is True
    assert len(data["review_reasons"]) >= 1

    # Verify MDU provenance event linked
    assert len(data["mdu_provenance_event_ids"]) >= 1
    assert data["mdu_provenance_event_ids"][0].startswith("mdu-ev-")


def test_fiduciary_duties_governance_query(client: TestClient):
    """
    Queries Companies Act 2013 directors' duties and checks verbatim evidence.
    """
    payload = {
        "query": "What are the statutory duties of directors to act in good faith and exercise reasonable care?",
        "as_of_date": "2024-06-01",
        "caller_identity": "ansh_clo_build_owner",
        "trace_id": "trace-test-ca13-002"
    }

    response = client.post("/api/v1/clo/research", json=payload)
    assert response.status_code == 200
    data = response.json()

    ca_passages = [p for p in data["evidence_passages"] if p["document_id"] == "doc-in-companies-act-2013"]
    assert len(ca_passages) >= 1
    section_numbers = [p["section_number"] for p in ca_passages]
    assert "Section 166" in section_numbers
    p166 = [p for p in ca_passages if p["section_number"] == "Section 166"][0]
    assert "good faith" in p166["verbatim_passage"].lower()
    assert "reasonable care" in p166["verbatim_passage"].lower()
