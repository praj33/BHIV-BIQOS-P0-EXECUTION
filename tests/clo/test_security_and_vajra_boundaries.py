"""
Scenario 4: Permissions & Security Boundary (Fail-Closed Enforcement)
Validates VAJRA 8-state deterministic authority lifecycle, Rule 8 Bounded Agent guard,
and fail-closed rejection of revoked, suspended, or unauthenticated callers.
"""

import pytest
from fastapi.testclient import TestClient
from clo.adapters.vajra_adapter import VajraTrustAdapter


def test_vajra_valid_caller_granted(client: TestClient):
    """Verifies that an authorized subject in USE state is granted access."""
    payload = {
        "query": "What are reasonable security practices for protecting sensitive personal data?",
        "caller_identity": "ansh_clo_build_owner",
        "auth_token": "ANSH_CLO_GOVERNED_SESSION",
        "trace_id": "trace-sec-valid-001"
    }
    response = client.post("/api/v1/clo/research", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "VERIFIED: USE" in data["vajra_trust_status"]


def test_vajra_revoked_caller_blocked_fail_closed(client: TestClient):
    """
    Verifies that a compromised caller in REVOKE state is rejected fail-closed with 403 Forbidden.
    Illegal re-entry is blocked.
    """
    payload = {
        "query": "What are reasonable security practices?",
        "caller_identity": "compromised_key_actor",
        "trace_id": "trace-sec-revoked-002"
    }
    response = client.post("/api/v1/clo/research", json=payload)
    assert response.status_code == 403
    err = response.json()["detail"]
    assert err["error"] == "VAJRA_AUTHORITY_DENIED"
    assert err["current_state"] == "REVOKE"
    assert "blocked state" in err["reason"].lower()


def test_vajra_suspended_caller_blocked(client: TestClient):
    """Verifies that an actor in SUSPEND state is denied access."""
    payload = {
        "query": "Review director liability under Companies Act.",
        "caller_identity": "suspended_auditor",
        "trace_id": "trace-sec-suspended-003"
    }
    response = client.post("/api/v1/clo/research", json=payload)
    assert response.status_code == 403
    err = response.json()["detail"]
    assert err["current_state"] == "SUSPEND"


def test_vajra_unregistered_subject_blocked(client: TestClient):
    """Verifies that an unknown subject is rejected fail-closed."""
    payload = {
        "query": "General contracting principles.",
        "caller_identity": "unknown_intruder_subject",
        "trace_id": "trace-sec-unknown-004"
    }
    response = client.post("/api/v1/clo/research", json=payload)
    assert response.status_code == 403
    err = response.json()["detail"]
    assert err["current_state"] == "UNKNOWN_SUBJECT"


def test_rule_8_bounded_agent_model(vajra: VajraTrustAdapter):
    """
    Verifies Rule 8 compliance:
    CLO Agent operates with read-only state reflection; direct ledger mutations are strictly forbidden.
    """
    state_view = vajra.get_agent_state_view()
    assert state_view["substrate"] == "VAJRA_TRUST_LAYER"
    assert state_view["rule_8_bounded_guard"] == "ENFORCED"
    assert state_view["direct_mutation_allowed"] is False
    assert state_view["governed_proposal_pathway"] == "TANTRA_GOVERNANCE_GATE"


def test_truthstore_evidence_recording_auth(vajra: VajraTrustAdapter):
    """
    Verifies TruthStore recording enforces secret token verification.
    """
    valid_record = vajra.record_truthstore_evidence(
        trace_id="trace-sec-ts-001",
        payload={"query": "test", "result": "verified"},
        token="CANONICAL_VAJRA_TANTRA_SECRET",
    )
    assert valid_record["verified"] is True
    assert valid_record["evidence_hash"].startswith("sha256:")

    # Attempt recording without valid secret -> must fail with PermissionError
    with pytest.raises(PermissionError, match="HTTP 401 Unauthorized"):
        vajra.record_truthstore_evidence(
            trace_id="trace-sec-ts-002",
            payload={"query": "unauthorized"},
            token="INVALID_TOKEN",
        )

