# TANTRA Retrieval-Readiness Assessment: `pkg-4d44c0a2dbc0`

**Assessment Role:** Raj, Accountable Technical Lead  
**Evaluation Mode:** Strict Read-Only Probe · Zero Mutation Calls · Zero Credentials · Public GET Only  
**Target Package ID:** `pkg-4d44c0a2dbc0`  
**Target Live Cluster Base URL:** `http://163.128.209.18:30308`  
**Assessment Execution Timestamp:** `2026-10-28T14:02:34+05:30` (`2026-10-28T08:32:34Z`)  

---

## 1. Pre-Execution Client & Endpoint Verification

Prior to dispatching any network call, client methods and endpoint routing were inspected in the existing codebase:

| Endpoint Path | HTTP Method | Implementation Location | Authentication Required? | Public Read-Only Confirmed? |
| :--- | :---: | :--- | :---: | :---: |
| `/discovery/packages` | **GET** | `app/src/services/apiClient.ts:L150-L152` | **NO** (Public) | **YES** |
| `/tantra/packages/{package_id}/runtime` | **GET** | `app/src/services/apiClient.ts:L158-L173` | **NO** (Public) | **YES** |

### Safety Invariants Enforced
- **Zero Credentials / Tokens**: Requests used standard `fetch` with `Accept: application/json`. No `Authorization` headers, cookies, or Bearer tokens were transmitted.
- **Zero Mutation**: No `POST`, `PUT`, `PATCH`, or `DELETE` calls were made.
- **Zero State Modification**: No packages were registered, certified, promoted, or altered.
- **Input Sanitization**: `packageId` passed through `encodeURIComponent(packageId.trim())`.

---

## 2. Live Probe Observations & Protocol Logs

### Probe 1: Public Discovery Listing
- **Request**: `GET http://163.128.209.18:30308/discovery/packages`
- **Timestamp**: `2026-10-28T14:02:34.112Z`
- **HTTP Status**: `200 OK`
- **Round-Trip Duration**: `98 ms`
- **Key Response Observations**:
  - `count`: **12** (Expanded from 9 observed in Stage A audit).
  - `packages`: 12 packages listed, all in status `REGISTERED`, created on `2026-10-28T07:38:09Z`.
  - **Target ID Check**: `pkg-4d44c0a2dbc0` is **NOT PRESENT** in the active package listing.

### Probe 2: Runtime-Readiness Envelope for `pkg-4d44c0a2dbc0`
- **Request**: `GET http://163.128.209.18:30308/tantra/packages/pkg-4d44c0a2dbc0/runtime`
- **Timestamp**: `2026-10-28T14:02:34.215Z`
- **HTTP Status**: `404 Not Found`
- **Round-Trip Duration**: `58 ms`
- **Response Payload (Complete)**:
  ```json
  {
    "error": {
      "type": "http_error",
      "message": "'No package found for package_id=pkg-4d44c0a2dbc0'",
      "path": "/tantra/packages/pkg-4d44c0a2dbc0/runtime"
    }
  }
  ```

---

## 3. Fresh Observations vs. Earlier Stage A Audit Findings

| Audit Dimension | Stage A Audit (Captured 2026-10-26) | Fresh Assessment (Captured 2026-10-28) | Architectural Analysis & Drift |
| :--- | :--- | :--- | :--- |
| **Catalog Size** | 9 packages discovered | **12 packages discovered** | Catalog expanded: 3 new VANA / FSI spatial packages seeded. |
| **Cluster Seeding Timestamp** | `2026-10-22T03:59:26Z` | `2026-10-28T07:38:09Z` | Backend was restarted/reseeded today (~1 hour prior to audit). |
| **Target Package ID** | `pkg-4d44c0a2dbc0` present | `pkg-4d44c0a2dbc0` **absent (404 Not Found)** | **CRITICAL DISCOVERY**: Package IDs are ephemerally generated on re-seeding. |
| **Active Dataset ID for Maritime Ports** | `ds-marine-intel-ports` (`pkg-4d44c0a2dbc0`) | `ds-marine-intel-ports` (`pkg-cd95bf999daa`) | Same underlying dataset; active ID is now `pkg-cd95bf999daa`. |

---

## 4. Correlated Comparative Readiness Evaluation on Current Active Maritime Package (`pkg-cd95bf999daa`)

To provide authoritative evaluation of the retrieval readiness rule engine against the current live cluster without violating read-only boundaries, the runtime envelope of the active maritime port intelligence package (`pkg-cd95bf999daa`) was queried via public GET:

- **Request**: `GET http://163.128.209.18:30308/tantra/packages/pkg-cd95bf999daa/runtime`
- **Timestamp**: `2026-10-28T14:03:38Z`
- **HTTP Status**: `200 OK` (Duration: `3100 ms`)

### Constitutional Readiness Rule Evaluation
| Rule Identifier | Evaluated Status | Reason Provided by Live Engine | Verdict |
| :--- | :---: | :--- | :---: |
| `PACKAGE_CERTIFIED` | **FAILED** | `Package status is REGISTERED; CERTIFIED or RETRIEVAL_READY is required.` | **NON-COMPLIANT** |
| `NOT_DEPRECATED_OR_ARCHIVED` | **PASSED** | `Package is active.` | **COMPLIANT** |
| `METADATA_COMPLETE` | **PASSED** | `All required package metadata fields are present.` | **COMPLIANT** |
| `LINEAGE_REGISTERED` | **FAILED** | `No knowledge object with a source_reference is registered for this package.` | **NON-COMPLIANT** |

### Overall Readiness Verdict
- **Overall Status**: `NOT_RETRIEVABLE`
- **Rules Passed**: 2 of 4 (50%)
- **Corrective Actions Required by Engine**:
  1. `Promote the package through VERIFIED -> CERTIFIED before requesting retrieval readiness.`
  2. `Register a Knowledge Object with a source_reference for this package via the Knowledge Object & Provenance Engine.`

### Lineage & Upstream MDU Status
- `knowledge_object_registered`: `false`
- `mdu_provenance.source`: `unavailable`
- `mdu_provenance.reason`: `MDU provenance fetch failed: MDU request failed for /api/v1/datasets/canonical/ds-marine-intel-ports: The read operation timed out`
- `known_gaps`: Re-confirmed 3 model discrepancies (`knowledge_object_id`, `lineage_reference`, `derivation_path`).

---

## 5. Identified Limitations & Blockers

1. **Ephemeral Package ID Generation**:
   - Package IDs (e.g. `pkg-4d44c0a2dbc0`) do not persist across database reseeding cycles. A stateless client cannot rely on hardcoded package IDs over time.
   - **Recommendation**: Package references should be indexed by canonical `dataset_id` + `version` or registered with stable deterministic IDs.
2. **Upstream MDU Read Timeout (`BLK-02`)**:
   - Live query to `/api/v1/datasets/canonical/ds-marine-intel-ports` continues to time out on the backend, preventing lineage registration.
3. **Absence of Package Certification**:
   - Packages remain stuck in `REGISTERED` status; no unauthenticated promotion or certification pathway exists.

---

## 6. Attestation Verdict

```json
{
  "requested_package_id": "pkg-4d44c0a2dbc0",
  "http_status": 404,
  "assessment_timestamp": "2026-10-28T14:02:34+05:30",
  "fresh_observation": "PACKAGE_NOT_FOUND_RESEEDED",
  "active_dataset_equivalent": "ds-marine-intel-ports",
  "current_active_package_id": "pkg-cd95bf999daa",
  "current_readiness_status": "NOT_RETRIEVABLE",
  "rules_passed": 2,
  "rules_failed": 2,
  "upstream_blocker": "MDU_ENDPOINT_TIMEOUT",
  "attestation_verdict": "VERIFIED_UNAVAILABLE_OR_NOT_RETRIEVABLE",
  "mutations_dispatched": 0,
  "credentials_used": false
}
```
