# BIQOS P0 — Master Execution Register

**Custodian:** Raj, Accountable Technical Lead  
**Scope:** Multi-Workstream Task Tracking & Evidence Gates  
**Status Policy:** No task is marked ACCEPTED without concrete evidence and owner approval.  

---

## Allowed Status Definitions
- `NOT STARTED`: Defined task with acceptance criteria; awaiting initiation.
- `IN PROGRESS`: Work actively underway by assigned owner.
- `INTEGRATED`: Code or documentation merged; awaiting test execution.
- `TESTED`: Automated unit, contract, or mock tests passing locally.
- `EVIDENCE READY`: Live logs, API responses, or test run outputs captured in `docs/evidence/`.
- `ACCEPTED`: Formally reviewed and signed off by the responsible system owner.
- `BLOCKED`: Progress halted due to external dependency, missing credentials, or contract mismatch.
- `SIMULATED`: Validated using mock data or stubs; awaiting live backing.

---

## Central Workstream Register

| Task ID | Workstream | Description | Status | Evidence | Dependencies | Proposed Owner | Required Tests | Acceptance Criteria | Blockers | Next Action |
| :---: | :--- | :--- | :---: | :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **TSK-A01** | A. Capability & Repo Mapping | Reconcile 20 Slice 1 repositories against 82 Census items. | `EVIDENCE READY` | `reconciliation.test.ts` (13 tests passing) | Local source files | Raj `[UNCONFIRMED]` | 13 Vitest tests | 100% census data integrity; 15 exact, 1 case-insensitive, 4 candidates identified. | None | Preserve census datasets verbatim. |
| **TSK-A02** | A. Capability & Repo Mapping | Author canonical capability manifest for 20 Slice 1 repositories. | `NOT STARTED` | None | TSK-A01 | Harsha `[UNCONFIRMED]` | Schema validation | Valid JSON manifest conforming to MASTERDB `RegistryObject` schema. | BLK-01 (Catalog unseeded) | Draft offline manifest payload for review. |
| **TSK-B01** | B. TANTRA Discovery | Implement safe, read-only discovery client for public packages. | `EVIDENCE READY` | `masterdb.test.ts` (8 tests passing), live curl | Live MASTERDB endpoint | Raj `[UNCONFIRMED]` | Vitest API client tests | Parses `GET /discovery/packages` and `/runtime` without auth headers or mutations. | None | Integration complete; maintain test coverage. |
| **TSK-B02** | B. TANTRA Discovery | Harden TANTRA test suite for edge cases (404/500, URI encoding). | `IN PROGRESS` | Unit test additions in `masterdb.test.ts` | TSK-B01 | Raj `[UNCONFIRMED]` | Vitest edge-case tests | Direct assertions on HTTP 404/500 status codes, malformed JSON, and query sanitation. | None | Add 3 targeted unit test cases to masterdb.test.ts. |
| **TSK-C01** | C. MASTERDB Capability Access | Secure unauthenticated read-only access to capability catalog. | `BLOCKED` | Live curl returning 401 Bearer required | Platform infra | Rayyan `[UNCONFIRMED]` | HTTP curl probe | `GET /capabilities/public` returns 200 OK with capability objects. | BLK-03 (Bearer auth required) | Configure public read-only route on MASTERDB. |
| **TSK-C02** | C. MASTERDB Capability Access | Validate BCAES architectural graph and SHA-256 replay hash. | `TESTED` | Review packet captures, live `/bcaes/validate/*` | MASTERDB service | Raj `[UNCONFIRMED]` | Deterministic replay test | 6 checks pass; identical SHA-256 hash across consecutive queries. | None (Registry currently 0 items) | Document BCAES query patterns. |
| **TSK-D01** | D. MDU Connectivity | Resolve read timeout on MDU canonical dataset endpoint. | `BLOCKED` | Live envelope error log in `pkg-4d44c0a2dbc0` | MDU service runtime | Harsha `[UNCONFIRMED]` | HTTP status probe | `/api/v1/datasets/canonical/ds-*` responds in < 3000ms. | BLK-02 (MDU timeout) | Coordinate with Nupur on MDU service uptime. |
| **TSK-D02** | D. MDU Connectivity | Align MDU append-only event stream to MASTERDB lineage model. | `BLOCKED` | Known gaps in live runtime envelope | MDU schema contract | Harsha `[UNCONFIRMED]` | Contract schema test | Documented mapping from MDU event IDs to MASTERDB lineage reference. | BLK-06 (Model mismatch) | Technical interview with Nupur & MASTERDB architect. |
| **TSK-E01** | E. NIYANTRAN Workflow Contract | Audit NIYANTRAN Workflow Executor OpenAPI specification. | `NOT STARTED` | None | `bhiv-Shakti-GC-Infra` access | Karana `[UNCONFIRMED]` | OpenAPI linter / Redocly | Verified OpenAPI schema defining task dispatch, execution states, and payloads. | BLK-04 (External repo) | Request read-only access to `bhiv-Shakti-GC-Infra`. |
| **TSK-E02** | E. NIYANTRAN Workflow Contract | Implement safe, read-only health and task probe client. | `NOT STARTED` | None | TSK-E01 | Karana `[UNCONFIRMED]` | Unit test probe | Non-mutating health check verifies executor availability and worker count. | BLK-04 | Specify input/output contracts for trial task. |
| **TSK-F01** | F. Authorization & Governance | Formulate read-only token specification for BIQOS adapter. | `NOT STARTED` | Token draft doc | Platform security | Rayyan `[UNCONFIRMED]` | Token validation test | Scoped, non-expiring (or auto-refreshed) read-only viewer token specification. | BLK-05 (No unified IAM) | Submit IAM specification to platform lead. |
| **TSK-G01** | G. Failure Handling & Retry | Define safe retry policy and idempotency key specification. | `NOT STARTED` | Architecture spec | TSK-E01 | Raj / Karana `[UNCONFIRMED]` | Retry simulation test | Exponential backoff algorithm, max 3 retries, duplicate event rejection via idempotency keys. | None | Author safe execution retry specification. |
| **TSK-G02** | G. Failure Handling & Retry | Define final-state immutable attestation schema. | `NOT STARTED` | TypeScript type defs | BIQOS data model | Raj `[UNCONFIRMED]` | Schema validator | RecordAttestation payload expanded with execution run ID, exit code, and hash. | None | Extend `types/masterdb.ts` with final-state model. |
| **TSK-H01** | H. Observability & Telemetry | Capture request duration and cold-start metrics in API client. | `EVIDENCE READY` | `apiClient.ts:L119-L131` | Local client | Raj `[UNCONFIRMED]` | Unit test timing assertions | Precise durationMs recorded; timeouts flagged with `isColdStart: true`. | None | Verified in Phase 1 review. |
| **TSK-H02** | H. Observability & Telemetry | Integrate PRAVAH systems observability monitoring endpoint. | `NOT STARTED` | None | PRAVAH service | Rayyan `[UNCONFIRMED]` | HTTP telemetry probe | BIQOS client emits health heartbeats to PRAVAH without blocking UI. | None | Establish PRAVAH ingest endpoint contract. |
| **TSK-I01** | I. Cross-Team Coordination | Obtain formal decision on Slice 1 capability manifest seeding. | `BLOCKED` | P0 Decision Log #1 | System Steering | Raj `[UNCONFIRMED]` | Governance sign-off | Formal approval to seed 20 Slice 1 capabilities into MASTERDB. | BLK-01 | Submit approval request to Sir. |
| **TSK-I02** | I. Cross-Team Coordination | Obtain formal decision on constitutional Workflow Executor. | `BLOCKED` | P0 Decision Log #2 | System Steering | Raj `[UNCONFIRMED]` | Governance sign-off | Formal confirmation that NIYANTRAN is the authoritative execution platform. | BLK-04 | Submit architecture decision request to Sir. |
