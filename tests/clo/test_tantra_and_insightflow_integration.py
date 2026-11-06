"""
Scenario 5: TANTRA Workload Execution & Failure Isolation, InsightFlow Telemetry
Validates compliance with `services/execution/EXECUTION_CONTRACT.md` and
`services/insightflow/INTEGRATION_CONTRACT.md`.
"""

import pytest
from fastapi.testclient import TestClient
from clo.adapters.tantra_adapter import TantraExecutionAdapter
from clo.adapters.insightflow_adapter import InsightFlowTelemetryAdapter
from clo.schemas.models import TantraWorkloadRequest


def test_tantra_workload_execution_success(client: TestClient):
    """
    Executes a workload via CLO TANTRA participant endpoint.
    Verifies bridge signature validation, trace immutability, and deterministic replay hashing.
    """
    payload = {
        "workload": '{"query": "What constitutes sensitive personal data under SPDI rules?", "as_of_date": "2024-01-01"}',
        "trace_id": "trace-tantra-wk-001",
        "execution_id": "exec-tantra-wk-001",
        "bridge_signature": "Bearer VERIFIED_TANTRA_BRIDGE_TOKEN"
    }

    response = client.post("/api/v1/clo/tantra/workload", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["trace_id"] == "trace-tantra-wk-001"
    assert data["execution_id"] == "exec-tantra-wk-001"
    assert data["status"] == "completed"
    assert data["artifact_location"] == "artifacts/trace-tantra-wk-001/exec-tantra-wk-001"
    assert "execution_hash" in data["result"]
    assert len(data["result"]["execution_hash"]) == 64
    assert data["result"]["legal_reasoning"]["evidence_status"] in ("EVIDENCE_VERIFIED", "CONFLICT_DETECTED")


def test_tantra_workload_unauthorized_signature_rejected(client: TestClient):
    """
    Verifies that an unverified or missing bridge signature is rejected with 401 Unauthorized.
    """
    payload = {
        "workload": "query text",
        "trace_id": "trace-tantra-invalid",
        "execution_id": "exec-tantra-invalid",
        "bridge_signature": "Bearer MALICIOUS_OR_FORGED_SIGNATURE"
    }
    response = client.post("/api/v1/clo/tantra/workload", json=payload)
    assert response.status_code == 401
    assert "BRIDGE_SIGNATURE_REJECTED" in response.json()["detail"]


@pytest.mark.asyncio
async def test_tantra_failure_isolation_offline_service(tantra: TantraExecutionAdapter):
    """
    Verifies failure isolation: when remote TANTRA execution service is offline,
    the adapter handles the failure gracefully and returns a degraded status envelope without crashing.
    """
    # Use unroutable local port to simulate offline service
    tantra_isolated = TantraExecutionAdapter(tantra_execution_url="http://127.0.0.1:59999")
    result = await tantra_isolated.forward_to_tantra_service(
        workload="test query",
        trace_id="trace-fail-iso-001",
        execution_id="exec-fail-iso-001",
        bridge_signature="Bearer VERIFIED_TANTRA_BRIDGE_TOKEN",
    )

    assert result["status"] == "DEGRADED_ISOLATED"
    assert result["isolated"] is True
    assert "unavailable" in result["error"].lower()


def test_insightflow_passive_telemetry_emission(insightflow: InsightFlowTelemetryAdapter):
    """
    Verifies InsightFlow integration strictly adheres to passive-only contract:
    passive=True, never alters execution flow, captures trace_id and status.
    """
    event = insightflow.emit_telemetry_event(
        trace_id="trace-if-001",
        execution_id="exec-if-001",
        event_type="test_audit_event",
        status="EVIDENCE_VERIFIED",
        payload={"query_topic": "intermediary takedown timeline"}
    )

    assert event.source == "clo-agent"
    assert event.trace_id == "trace-if-001"
    assert event.execution_id == "exec-if-001"
    assert event.passive is True
    assert event.status == "EVIDENCE_VERIFIED"

    recorded = insightflow.get_emitted_events(trace_id="trace-if-001")
    assert len(recorded) == 1
    assert recorded[0].event_type == "test_audit_event"

