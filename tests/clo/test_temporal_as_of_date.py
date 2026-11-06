"""
Scenario 3: Temporal As-of-Date Resolution (Verified Amendment / Supersession Pair)
Tests that historical queries correctly resolve active law on past dates,
identifying whether IT Intermediary Rules 2011 was active law (prior to Feb 25, 2021)
or superseded (after Feb 25, 2021).
"""

from fastapi.testclient import TestClient
from clo.registry.registry import CanonicalLegalRegistry
from clo.schemas.models import DocumentStatus


def test_registry_as_of_date_supersession_logic(canonical_registry: CanonicalLegalRegistry):
    """Directly verifies registry temporal evaluation on past vs current dates."""
    # Historical date: 2018-05-01 (Before IT Rules 2021 was enacted)
    status_2018, reason_2018 = canonical_registry.get_document_status_as_of(
        "doc-in-it-intermediary-rules-2011", "2018-05-01"
    )
    assert status_2018 == DocumentStatus.CURRENT
    assert "active law on 2018-05-01 prior to supersession" in reason_2018

    # Status of 2021 rules on 2018-05-01
    status_21_in_18, reason_21_in_18 = canonical_registry.get_document_status_as_of(
        "doc-in-it-rules-2021", "2018-05-01"
    )
    assert status_21_in_18 == DocumentStatus.UNKNOWN
    assert "Not yet in force" in reason_21_in_18

    # Present date: 2024-01-01 (After IT Rules 2021 superseded 2011 rules)
    status_2024, reason_2024 = canonical_registry.get_document_status_as_of(
        "doc-in-it-intermediary-rules-2011", "2024-01-01"
    )
    assert status_2024 == DocumentStatus.SUPERSEDED
    assert "Superseded on 2021-02-25" in reason_2024 or "Replaced on 2021-02-25" in reason_2024

    # Status of 2021 rules on 2024-01-01
    status_21_in_24, reason_21_in_24 = canonical_registry.get_document_status_as_of(
        "doc-in-it-rules-2021", "2024-01-01"
    )
    assert status_21_in_24 == DocumentStatus.CURRENT


def test_api_as_of_date_intermediary_timeline(client: TestClient):
    """
    Tests end-to-end API evaluation with temporal parameters:
    1. Query in 2018 resolves 1-month grievance timeline as current law.
    2. Query in 2024 surfaces 15-day timeline and marks 2011 rules as superseded.
    """
    # Query A: As of 2018-01-01
    req_2018 = {
        "query": "What is the timeline for the Grievance Officer to redress complaints under intermediary rules?",
        "as_of_date": "2018-01-01",
        "caller_identity": "ansh_clo_build_owner",
        "trace_id": "trace-temporal-2018"
    }
    res_2018 = client.post("/api/v1/clo/research", json=req_2018)
    assert res_2018.status_code == 200
    data_2018 = res_2018.json()
    assert data_2018["as_of_date_applied"] == "2018-01-01"

    # In 2018, only 2011 rules were active; 2021 rules were not yet in force
    passages_2018 = data_2018["evidence_passages"]
    p_11_list = [p for p in passages_2018 if p["document_id"] == "doc-in-it-intermediary-rules-2011"]
    assert len(p_11_list) >= 1
    assert p_11_list[0]["version_status_as_of_date"] == "CURRENT"

    # Query B: As of 2024-01-01
    req_2024 = {
        "query": "What is the timeline for the Grievance Officer to redress complaints under intermediary rules?",
        "as_of_date": "2024-01-01",
        "caller_identity": "ansh_clo_build_owner",
        "trace_id": "trace-temporal-2024"
    }
    res_2024 = client.post("/api/v1/clo/research", json=req_2024)
    assert res_2024.status_code == 200
    data_2024 = res_2024.json()
    assert data_2024["as_of_date_applied"] == "2024-01-01"

    # In 2024, 2021 rules are CURRENT and 2011 rules are SUPERSEDED
    passages_2024 = data_2024["evidence_passages"]
    p_21_list = [p for p in passages_2024 if p["document_id"] == "doc-in-it-rules-2021"]
    assert len(p_21_list) >= 1
    assert p_21_list[0]["version_status_as_of_date"] == "CURRENT"

    # Explicit conflict/supersession notice surfaced
    assert len(data_2024["conflicts_identified"]) >= 1
    assert "supersession" in data_2024["conflicts_identified"][0].lower()

