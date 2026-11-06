"""
Scenario 1: CLO Typed Input/Output Contracts & Health Check
Validates FastAPI endpoint schemas, canonical registry inventory (8 statutes),
and active subsystem adapters.
"""

from fastapi.testclient import TestClient


def test_health_check_contract(client: TestClient):
    """Verifies that GET /health returns valid JSON conforming to system contract."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()

    assert data["service"] == "bhiv-clo-agent-runtime"
    assert data["version"] == "1.0.0-p0"
    assert data["status"] == "healthy"
    assert data["canonical_registry"]["document_count"] == 8
    assert data["canonical_registry"]["jurisdiction"] == "India"
    assert "doc-in-dpdp-act-2023" in data["canonical_registry"]["statutes"]
    assert "doc-in-it-rules-2021" in data["canonical_registry"]["statutes"]
    assert data["adapters"]["vajra_trust"] == "ENFORCING_8_STATE_LIFECYCLE"
    assert data["governance"]["rule_5_evidence_guard"] == "ENFORCED"
    assert data["governance"]["silent_canon_creation"] == "FORBIDDEN"


def test_list_canonical_documents(client: TestClient):
    """Verifies GET /api/v1/clo/documents returns all 8 ingested official documents."""
    response = client.get("/api/v1/clo/documents")
    assert response.status_code == 200
    docs = response.json()
    assert len(docs) == 8

    doc_ids = {d["document_id"] for d in docs}
    expected_ids = {
        "doc-in-dpdp-act-2023",
        "doc-in-it-act-2000",
        "doc-in-it-amendment-act-2008",
        "doc-in-it-rules-2021",
        "doc-in-it-intermediary-rules-2011",
        "doc-in-spdi-rules-2011",
        "doc-in-companies-act-2013",
        "doc-in-contract-act-1872",
    }
    assert expected_ids.issubset(doc_ids)

    # Validate that every document has an official source URL, date, and sha256 hash
    for doc in docs:
        assert doc["source_url"].startswith("http")
        assert len(doc["sha256_hash"]) == 64
        assert doc["mdu_dataset_id"].startswith("ds-legal-")
        assert len(doc["sections"]) > 0


def test_get_individual_canonical_document(client: TestClient):
    """Verifies GET /api/v1/clo/documents/{id} returns full statutory sections and relations."""
    response = client.get("/api/v1/clo/documents/doc-in-dpdp-act-2023")
    assert response.status_code == 200
    doc = response.json()
    assert doc["document_id"] == "doc-in-dpdp-act-2023"
    assert doc["short_name"] == "DPDP Act 2023"
    assert len(doc["relations"]) >= 1

    # Check relation to IT Act 2000
    rel = doc["relations"][0]
    assert rel["relation_type"] == "AMENDS"
    assert rel["target_document_id"] == "doc-in-it-act-2000"

    # Test 404 for nonexistent document
    notFound = client.get("/api/v1/clo/documents/nonexistent-statute")
    assert notFound.status_code == 404

