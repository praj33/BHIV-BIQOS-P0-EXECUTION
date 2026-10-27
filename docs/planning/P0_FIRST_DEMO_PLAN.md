# BIQOS P0 — First Read-Only Demonstration Plan
## Phase 1 Milestone: Public TANTRA Discovery & Retrieval-Readiness Audit

**Author:** Raj, Accountable Technical Lead  
**Scope:** Thin-Thread Read-Only Proof of Concept  
**Execution Environment:** Local BIQOS Vite Service (`http://localhost:5173/`) against Live MASTERDB (`http://163.128.209.18:30308`)  
**Safety Mandate:** Zero Write Operations · Zero Mutation Endpoints · Zero Credentials  

---

## 1. User Objective
A stakeholder or operator wishes to interrogate the live ecosystem for a specific registered Knowledge Package (e.g., Maritime Port Intelligence: `pkg-4d44c0a2dbc0`), verify its constitutional lifecycle state, audit its retrieval readiness rules, inspect documented MDU lineage gaps, and produce a deterministic, immutable attestation report without modifying backend state.

---

## 2. Package Discovery
1. Client issues a safe HTTP GET request to `http://163.128.209.18:30308/discovery/packages`.
2. Response validates:
   - Status code is `200 OK`.
   - Payload is valid JSON containing an array of packages.
   - Target package `pkg-4d44c0a2dbc0` is present with `status: "REGISTERED"`, `board: "maritime"`, and `owner: "masterdb-governance"`.
3. Discovered packages are stored in the client-side read-only in-memory cache (`tantraPackagesCache`).

---

## 3. Retrieval-Readiness Inspection
1. Client issues a safe HTTP GET request to `http://163.128.209.18:30308/tantra/packages/pkg-4d44c0a2dbc0/runtime`.
2. Client validates input ID using `encodeURIComponent(packageId.trim())`.
3. Response is parsed into a typed `TantraRuntimeEnvelope` containing:
   - Package metadata and transition history.
   - Lineage registration status.
   - Retrieval readiness rule evaluation.

---

## 4. Certification and Lineage Checks
The client evaluates the 4 constitutional retrieval readiness rules returned by the live service:
1. **Rule 1: `PACKAGE_CERTIFIED`**:
   - Status: `passed == false`
   - Reason: `Package status is REGISTERED; CERTIFIED or RETRIEVAL_READY is required.`
2. **Rule 2: `NOT_DEPRECATED_OR_ARCHIVED`**:
   - Status: `passed == true`
   - Reason: `Package is active.`
3. **Rule 3: `METADATA_COMPLETE`**:
   - Status: `passed == true`
   - Reason: `All required package metadata fields are present.`
4. **Rule 4: `LINEAGE_REGISTERED`**:
   - Status: `passed == false`
   - Reason: `No knowledge object with a source_reference is registered for this package.`
   - Gaps confirmed: Documents 3 MDU model gaps (`knowledge_object_id`, `lineage_reference`, `derivation_path`).

---

## 5. Deterministic Assessment Output
The client generates an immutable verification summary:
```json
{
  "audit_target": "pkg-4d44c0a2dbc0",
  "dataset_id": "ds-marine-intel-ports",
  "lifecycle_state": "REGISTERED",
  "overall_readiness": "NOT_RETRIEVABLE",
  "rules_passed": 2,
  "rules_failed": 2,
  "lineage_complete": false,
  "mdu_status": "TIMEOUT_OR_UNAVAILABLE",
  "attestation_verdict": "GOVERNANCE_INSPECTION_CONFIRMED",
  "generated_at": "2026-10-27T14:30:00Z"
}
```

---

## 6. Evidence Retention
- The complete HTTP request/response payloads are captured and saved in `docs/evidence/`.
- The duration (latency in milliseconds) is recorded.
- The SHA-256 hash of the response payload is computed to guarantee replayability.

---

## 7. Expected Result
- The live cluster proves that public discovery and retrieval-readiness evaluation are operational.
- The system honestly reports `NOT_RETRIEVABLE` rather than synthesizing a false pass.
- No write calls are dispatched, and the BIQOS dashboard layout remains completely undisturbed.

---

## 8. Failure Cases & Resilience
1. **Network Timeout (> 8000ms)**: Client gracefully aborts via `AbortController` and reports `COLD_START_OR_TIMEOUT`.
2. **Endpoint 404 Not Found**: Client handles non-existent IDs cleanly, returning HTTP 404 without crashing.
3. **MDU Timeout**: Handled gracefully by MASTERDB runtime envelope, returning structured lineage gaps.

---

## 9. Tests and Acceptance Criteria
- Vitest suite executes with 100% pass rate.
- Linter reports 0 warnings and 0 errors across all files.
- Zero mutations or auth headers sent over the wire.

---

## 10. Remaining Gaps to Full Execution Demonstration
- This initial milestone demonstrates **read-only readiness assessment**.
- The subsequent **Objective → Execution → Verification** milestone requires:
  1. Authoritative OpenAPI contracts for NIYANTRAN (`bhiv-Shakti-GC-Infra`).
  2. A designated test capability with valid input/output schemas.
  3. Resolution of the MDU canonical endpoint timeout.
