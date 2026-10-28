# BIQOS P0 — Testing Strategy & Verification Protocol

**Author:** Raj, Accountable Technical Lead  
**Scope:** Multi-Tiered Verification Framework for BIQOS P0 Mission  
**Policy:** Never claim that an unimplemented or unexecuted test has passed.  

---

## 1. Testing Tier Architecture

The BIQOS P0 verification framework is divided into five distinct tiers:

```
[ Tier 1: Unit & Source Reconciliation ]  -> Local census integrity & string matching
                   │
                   ▼
[ Tier 2: Contract & Schema Validation ]   -> JSON schema conformity & OpenAPI linting
                   │
                   ▼
[ Tier 3: Network Resilience & Failures ]  -> Abort timeouts, cold starts, 401/404 handling
                   │
                   ▼
[ Tier 4: Safe Retries & Deduplication ]   -> Idempotency keys, duplicate event rejection
                   │
                   ▼
[ Tier 5: Governed End-to-End Execution ] -> Full Objective -> Execution -> Verification
```

---

## 2. Implementation Status by Tier

| Testing Tier | Scope & Focus | Existing Implementation | Test Runner | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Tier 1: Unit & Reconciliation** | Validates 20 inventory repos against 82 census records. | `app/src/tests/reconciliation.test.ts` | Vitest | `PASSING (13/13)` |
| **Tier 2: Contract & Schema** | Validates MASTERDB and TANTRA response structures. | `app/src/tests/masterdb.test.ts` | Vitest | `PASSING (16/16)` |
| **Tier 3: Network & Failure** | Validates timeouts (8s), 404 fallback, 401 Bearer fallback. | `app/src/tests/masterdb.test.ts` | Vitest | `PASSING (12/12)` |
| **Tier 4: Safe Retries & Dedup** | Validates concurrent request deduplication via promises. | `app/src/services/masterdb.ts` | Vitest | `SIMULATED / PARTIAL` |
| **Tier 5: End-to-End Governed** | Multi-system workflow dispatch, execution, and attestation. | None (Planned for Stage B) | N/A | `PLANNED / NOT IMPLEMENTED` |

---

## 3. How to Execute Existing Application Tests

From the application workspace (`BHIV-BIQOS-SLICE-1/app`):

```bash
# Run all automated tests
npm test

# Run tests in watch mode
npm run test:watch

# Execute static linter across all 17 files
npm run lint

# Compile production build bundle to verify types
npm run build
```

---

## 4. Evidence Generation Guidelines
- Every test run used for compliance must record:
  - Exact command line executed.
  - Number of passing, failing, and skipped tests.
  - Duration of test execution.
  - Git commit hash of the tested tree.
- Store summarized outputs in `docs/evidence/EVIDENCE_INDEX.md`.

---

## 5. Proposed Safe Test Suite: Reseeding, Stale IDs & MDU Resilience (P0 Hardening)

Based on the October 28, 2026 ground-truth audit, the following safe, read-only test cases are recommended for implementation in `app/src/tests/masterdb.test.ts`:

### 5.1 Test: Previously Observed Package ID Returning 404 Not Found
- **Scenario**: A client queries a package ID that existed prior to a database reseed (e.g. `pkg-4d44c0a2dbc0`), and the live service returns HTTP 404.
- **Verification Criteria**:
  - `apiClient.getTantraPackageRuntime('pkg-4d44c0a2dbc0')` resolves with `ok: false`, `status: 404`, and structured error message.
  - `masterDbService.getTantraPackageRuntime('pkg-4d44c0a2dbc0')` resolves to `null` without throwing an unhandled exception.
  - The 404 response is **not** cached in `tantraRuntimeCache`, allowing recovery if the ID is re-registered later.

### 5.2 Test: Dynamic Discovery Results Changing After Reseed
- **Scenario**: The package count from `GET /discovery/packages` changes between probe cycles (e.g., from 9 to 12 packages).
- **Verification Criteria**:
  - Adapter updates `tantraPackagesCache` with the fresh list.
  - `getConnectionStatus().tantraPackagesCount` reflects the updated count (`12`).
  - Existing local census records remain uncorrupted and maintain deterministic fallback.

### 5.3 Test: Canonical Dataset Identifier Lookup Contract (Contract Dependency)
- **Scenario**: Client attempts resolution by canonical dataset ID (`ds-marine-intel-ports`).
- **Verification Criteria**:
  - Since no direct endpoint exists today (`GAP-08`), client searches local discovery cache for matching `dataset_id`.
  - If match found, retrieves runtime envelope via current active package ID (`pkg-cd95bf999daa`).
  - If no match found or endpoint unsupported, client marks lookup as a contract dependency without crashing or calling undocumented URLs.

### 5.4 Test: Upstream MDU Timeout Handling
- **Scenario**: Upstream MDU service times out during envelope generation, causing backend to return `mdu_provenance.source == "unavailable"`.
- **Verification Criteria**:
  - Runtime envelope parsing succeeds without JSON validation error.
  - `retrieval_readiness.rules` correctly reflects `LINEAGE_REGISTERED: false`.
  - Overall status evaluates cleanly to `NOT_RETRIEVABLE`.

### 5.5 Test: Missing Lineage Fields Graceful Degradation
- **Scenario**: Envelope payload omits legacy fields (`knowledge_object_id`, `lineage_reference`, `derivation_path`) and contains `known_gaps`.
- **Verification Criteria**:
  - Lineage parser accurately populates `known_gaps` array.
  - Zero synthetic identifiers are invented or injected into the record.

### 5.6 Test: Deterministic Readiness Verdict When Evidence Is Absent
- **Scenario**: A package in state `REGISTERED` is evaluated for readiness while lacking certification and lineage proofs.
- **Verification Criteria**:
  - `PACKAGE_CERTIFIED` rule evaluates strictly to `false`.
  - `retrieval_readiness.status` evaluates strictly to `NOT_RETRIEVABLE`.
  - Zero false certifications or readiness passes are synthesized.
