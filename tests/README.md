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
