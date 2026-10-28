# BIQOS P0 — Cross-Team Coordination Matrix

**Author:** Raj, Accountable Technical Lead  
**Scope:** Lead Deliverable Assignments & Confirmation Status  
**Operating Policy:** All assignments are provisional and marked UNCONFIRMED until formally acknowledged.  

---

## 1. Primary Workstream Ownership Table

| Accountable Owner | Primary Functional Role | Assigned Workstream | Required Milestone Deliverable | Upstream Dependencies | Acceptance Criteria & Evidence | Confirmation Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **Raj** | Technical Lead / Frontend Integration | **BIQOS Slice 1 Integration Boundary** | 1. Preserve locked UI layout and census data integrity.<br>2. Implement resilient unit test suite in `masterdb.test.ts` covering stale IDs (404), dynamic reseed counts, and MDU timeout envelopes.<br>3. Maintain central P0 Execution Register. | None (Workspace self-contained) | - Test suite expands with 404, reseed, and degraded envelope assertions.<br>- CSS bundle size unchanged (18.57 kB).<br>- Zero write operations dispatched. | `CONFIRMED (Lead)` |
| **Karana** | Workflow Execution & Orchestration Lead | **NIYANTRAN Execution Platform** | 1. Provide read-only OpenAPI contract for `bhiv-Shakti-GC-Infra` (`TSK-E01`).<br>2. Document task dispatch schema and execution states (`PENDING`, `RUNNING`, `COMPLETED`, `FAILED`).<br>3. Expose unauthenticated health/status endpoint (`TSK-E02`). | Access to `bhiv-Shakti-GC-Infra` repository; `DEC-01` approval | - Valid OpenAPI 3.0 document.<br>- Zero breaking changes to existing tasks.<br>- Sample trial task execution recipe. | `UNCONFIRMED` |
| **Harsha** | Data Engineering & MDU Integration Lead | **MDU Contracts & Capability Seeding** | 1. Investigate and resolve MDU canonical endpoint read timeout on `ds-*` (`TSK-D01`).<br>2. Align MDU append-only event stream to MASTERDB lineage model (`TSK-D02`).<br>3. Draft canonical Capability Manifest for 20 Slice 1 repos (`TSK-A02`). | MDU service runtime (Nupur); `DEC-03` & `DEC-04` approvals | - MDU responds in < 3000ms.<br>- Documented lineage event mapping.<br>- Valid JSON manifest for 20 repos. | `UNCONFIRMED` |
| **Rayyan** | Platform Infrastructure & Security Lead | **Access Control, Network & Identification** | 1. Propose an unauthenticated `GET /capabilities/public` route or evaluate read-only access options under pending decision DEC-02 (`TSK-C01`).<br>2. Formulate package ID stabilization policy or evaluate public canonical dataset lookup route options under pending decision DEC-07 (`TSK-B03`).<br>3. Document PRAVAH systems observability ingest contract (`TSK-H02`). | MASTERDB cluster admin permissions; `DEC-02` & `DEC-07` approvals | - Public capability query returns 200 OK.<br>- Stable package ID generation or canonical route active.<br>- Zero credential leaks in client bundles. | `UNCONFIRMED` |

---

## 2. Cross-Team Communication Protocol
1. **Asynchronous Audit Tracking**: All updates must be recorded in `docs/planning/P0_EXECUTION_REGISTER.md` with direct citations to test reports or live evidence files.
2. **Weekly Architecture Alignment**: Review blocked tasks (`BLK-01` through `BLK-07`) with the steering committee and Sir.
3. **Strict Non-Interference**: No owner may push code changes into another team's repository without mutual review and verification.
