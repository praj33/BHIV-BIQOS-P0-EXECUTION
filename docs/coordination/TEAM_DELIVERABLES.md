# BIQOS P0 — Cross-Team Coordination Matrix

**Author:** Raj, Accountable Technical Lead  
**Scope:** Lead Deliverable Assignments & Confirmation Status  
**Operating Policy:** All assignments are provisional and marked UNCONFIRMED until formally acknowledged.  

---

## 1. Primary Workstream Ownership Table

| Accountable Owner | Primary Functional Role | Assigned Workstream | Required Milestone Deliverable | Upstream Dependencies | Acceptance Criteria & Evidence | Confirmation Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **Raj** | Technical Lead / Frontend Integration | **BIQOS Slice 1 Integration Boundary** | 1. Preserve locked UI layout and census data integrity.<br>2. Harden TANTRA client test suite (404/500, URI encoding).<br>3. Maintain central P0 Execution Register. | None (Workspace self-contained) | - 44/44 unit tests passing.<br>- CSS bundle size unchanged (18.57 kB).<br>- Zero write operations dispatched. | `CONFIRMED (Lead)` |
| **Karana** | Workflow Execution & Orchestration Lead | **NIYANTRAN Execution Platform** | 1. Provide read-only OpenAPI contract for `bhiv-Shakti-GC-Infra`.<br>2. Document task dispatch schema and execution states.<br>3. Expose unauthenticated health/status endpoint. | Access to `bhiv-Shakti-GC-Infra` repository | - Valid OpenAPI 3.0 document.<br>- Zero breaking changes to existing tasks.<br>- Sample trial task execution recipe. | `UNCONFIRMED` |
| **Harsha** | Data Engineering & MDU Integration Lead | **MDU Contracts & Capability Seeding** | 1. Resolve MDU canonical endpoint read timeout.<br>2. Align MDU append-only event stream to MASTERDB lineage model.<br>3. Draft canonical Capability Manifest for 20 Slice 1 repos. | MDU service runtime (Nupur) | - MDU responds in < 3000ms.<br>- Valid JSON manifest for 20 repos.<br>- Lineage test passing in runtime envelope. | `UNCONFIRMED` |
| **Rayyan** | Platform Infrastructure & Security Lead | **Access Control, Network & Observability** | 1. Configure unauthenticated `GET /capabilities/public` route (or provide scoped read-only Bearer token).<br>2. Document PRAVAH systems observability ingest contract.<br>3. Maintain MASTERDB deployment stability. | MASTERDB cluster admin permissions | - Public capability query returns 200 OK.<br>- PRAVAH telemetry ingest spec approved.<br>- Zero credential leaks in client bundles. | `UNCONFIRMED` |

---

## 2. Cross-Team Communication Protocol
1. **Asynchronous Audit Tracking**: All updates must be recorded in `docs/planning/P0_EXECUTION_REGISTER.md` with direct citations to test reports or live evidence files.
2. **Weekly Architecture Alignment**: Review blocked tasks (`BLK-01` through `BLK-06`) with the steering committee and Sir.
3. **Strict Non-Interference**: No owner may push code changes into another team's repository without mutual review and verification.
