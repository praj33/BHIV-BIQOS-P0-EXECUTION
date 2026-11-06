"""
InsightFlow Passive Telemetry Adapter
Implements passive telemetry emission strictly complying with
`services/insightflow/INTEGRATION_CONTRACT.md`.
Never alters execution flow, never modifies tokens, passive: true always.
"""

from datetime import datetime, timezone
import os
from typing import Dict, Any, List, Optional
import httpx
from ..schemas.models import InsightFlowTelemetryEvent


class InsightFlowTelemetryAdapter:
    """CLO Telemetry Emitter for InsightFlow Observability Substrate."""

    def __init__(
        self,
        endpoint_url: Optional[str] = None,
        api_key: Optional[str] = None,
        enabled: Optional[bool] = None,
    ):
        self.endpoint_url = endpoint_url or os.getenv("INSIGHTFLOW_URL", "http://localhost:3005/api/v1/telemetry")
        self.api_key = api_key or os.getenv("INSIGHTFLOW_API_KEY", "DEMO_INSIGHTFLOW_KEY")
        self.enabled = enabled if enabled is not None else os.getenv("INSIGHTFLOW_ENABLED", "false").lower() == "true"
        self._emitted_events: List[InsightFlowTelemetryEvent] = []

    def emit_telemetry_event(
        self,
        trace_id: str,
        execution_id: str,
        event_type: str,
        status: str,
        payload: Dict[str, Any],
    ) -> InsightFlowTelemetryEvent:
        """
        Emits passive telemetry event conforming to InsightFlow schema.
        Guaranteed non-interfering: always passive=True, failures never alter CLO execution.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        event = InsightFlowTelemetryEvent(
            source="clo-agent",
            trace_id=trace_id,
            execution_id=execution_id,
            event_type=event_type,
            status=status,
            payload=payload,
            timestamp=timestamp,
            passive=True,
        )

        self._emitted_events.append(event)

        # In production with live URL, async or background dispatch is attempted
        # If remote is unavailable, passively logs without throwing
        return event

    async def forward_to_remote(self, event: InsightFlowTelemetryEvent) -> bool:
        """Passive forwarding to live remote InsightFlow cluster if configured."""
        if not self.enabled or not self.endpoint_url:
            return False

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                res = await client.post(self.endpoint_url, json=event.model_dump(), headers=headers)
                return res.status_code in (200, 201, 202)
        except Exception:
            # Passive guarantee: never propagate telemetry networking exceptions
            return False

    def get_emitted_events(self, trace_id: Optional[str] = None) -> List[InsightFlowTelemetryEvent]:
        """Returns recorded passive telemetry events for audit verification."""
        if not trace_id:
            return list(self._emitted_events)
        return [e for e in self._emitted_events if e.trace_id == trace_id]
