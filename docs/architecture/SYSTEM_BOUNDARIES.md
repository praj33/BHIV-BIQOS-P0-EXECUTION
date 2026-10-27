# BHIV Ecosystem — System Responsibility & Boundary Matrix

**Author:** Raj, Accountable Technical Lead  
**Scope:** BIQOS P0 Architecture  
**Status:** Baseline Established · Derived from Stage A Ground-Truth Audit  

---

## 1. Architectural Philosophy: The Anti-Parallel Mandate

The primary architectural mandate of the **BIQOS P0 Mission** is:
> **Reuse existing systems. Do not design parallel runtimes, shadow registries, or duplicate governance mechanisms.**

To operationalize this, every responsibility in the ecosystem must have **exactly one primary constitutional owner**. Where boundaries interact, deterministic interface contracts must govern the exchange.

---

## 2. Core System Responsibility Matrix

| System | Constitutional Role | Declared Primary Owner | Primary Boundaries & Authorities | Existing Implementation / Endpoint | Boundary Verification Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **BIQOS** | Capability Inventory & Convergence UI | **Raj** | User-facing capability inventory, local census reconciliation, read-only status and attestation visibility. | `BHIV-BIQOS-SLICE-1` (`http://localhost:5173/`) | `VERIFIED IN SOURCE` & `VERIFIED LIVE` |
| **MASTERDB** | Canonical Knowledge & Lifecycle Runtime | **Central Platform** | Dataset validation rule engine (`config/validation_rules.json`), Package Lifecycle State Graph, BCAES Architectural Catalog (`/bcaes/*`), SQL artifact storage. | `http://163.128.209.18:30308` (`GET /health`, `GET /docs`) | `VERIFIED LIVE` |
| **TANTRA** | Governed Discovery & Reasoning | **TANTRA Team** | Knowledge discovery package provider, retrieval-readiness rule evaluation (`PACKAGE_CERTIFIED`, `LINEAGE_REGISTERED`), runtime envelope generation. | `GET /discovery/packages`<br>`GET /tantra/packages/{id}/runtime` | `VERIFIED LIVE` |
| **MDU** | Schema, Ontology & Provenance Authority | **Nupur / Harsha** | Authoritative canonical schemas, ontology definitions, append-only provenance event logs (`ORIGIN`, `INGESTION`, `VALIDATION`). | Upstream API: `/api/v1/datasets/canonical/*` | `BLOCKED` (Timeout & Schema Mismatch) |
| **Bucket** | Evidence & Provenance Storage | **Bucket Team** | Immutable persistence of raw datasets, execution evidence, audit logs, and provenance payloads. | S3 / MinIO Object Store (`bhiv-bucket-backend`) | `UNKNOWN / NOT INSPECTED` |
| **PRAVAH** | Systems Observability Layer | **Shivam / Rayyan** | Operational systems health monitoring, uptime tracking, latency telemetry, readiness endpoints. | `bhiv-pravah` (`https://pravah.blackholeinfiverse.com`) | `UNKNOWN / NOT INSPECTED` |
| **NIYANTRAN / SHAKTI** | Workflow Execution & Orchestration | **Pratik / Karana** | Proposed workflow execution platform, state machine transitions, task scheduling, asynchronous job dispatch. | `bhiv-Shakti-GC-Infra` (`https://niyantrankendra.blackholeinfiverse.com`) | `UNKNOWN / NOT INSPECTED` (Pending Contract Audit) |
| **Security / IAM** | Authorization & Identity | **Rayyan / Platform** | Token issuance, request signing, role-based access control, cryptographic verification. | `auth/` module in MASTERDB (Bearer tokens; no human SSO) | `VERIFIED IN SOURCE` & `VERIFIED LIVE` |

---

## 3. Detailed Boundary Definitions

### 3.1 BIQOS (`BHIV-BIQOS-SLICE-1`)
- **Owns**:
  - Ingestion and validation of the 20 Slice 1 Repository declarations and 82 Capability Census records.
  - Deterministic string matching and audit categorization (`EXACT`, `CASE_INSENSITIVE`, `UNRESOLVED_ALIAS_CANDIDATE`, `UNMATCHED`).
  - Read-only polling of MASTERDB health and BCAES capability registries.
  - User-facing presentation across desktop and mobile drawers.
- **Deliberately Does NOT Own**:
  - Capability registration or mutation (strictly read-only).
  - Workflow dispatch or execution scheduling.
  - Independent schema or ontology definitions.

### 3.2 MASTERDB Runtime
- **Owns**:
  - The deterministic rule validation engine (`config/validation_rules.json`).
  - The directed state graph of knowledge package lifecycles.
  - The BCAES Canonical Registry (11 object classes: `dom-`, `cap-`, `psv-`, `prd-`, `prg-`, `frw-`, `eng-`, `run-`, `itg-`, `kas-`, `ifc-`).
  - Data observability metrics (`/metrics`).
- **Deliberately Does NOT Own**:
  - Authoring canonical schemas or ontology (owned by MDU).
  - Runtime workflow orchestration (owned by NIYANTRAN/SHAKTI).
  - Systems/infrastructure health monitoring (owned by PRAVAH).

### 3.3 MDU (Metadata & Data Understanding)
- **Owns**:
  - The definition and semantic validation of all ecosystem datasets.
  - The chronological provenance stream of data transformation events.
- **Contract Boundary with MASTERDB**:
  - MASTERDB consumes MDU data via `MDUContractAdapter`.
  - *Current Conflict*: MASTERDB expects a singular `knowledge_object_id` and `lineage_reference`; MDU implements an append-only event array with `event_id` + `dataset_id`.

### 3.4 NIYANTRAN / SHAKTI (Proposed Execution Engine)
- **Proposed Role**:
  - Scheduled task runner, dependency resolver, and distributed execution worker.
- **Current Audit Boundary**:
  - Resides in an external repository (`bhiv-Shakti-GC-Infra`).
  - Before BIQOS or MASTERDB integrates with NIYANTRAN, its OpenAPI contract, execution state schema, and failure handling must be audited and verified under Stage B.

---

## 4. Established vs Pending Architectural Boundaries

```
+---------------------------------------------------------------------------------+
| ESTABLISHED & VERIFIED BOUNDARIES                                               |
| - BIQOS read-only boundary (apiClient.ts, zero credentials, 8s timeout)         |
| - MASTERDB read-only discovery boundary (GET /discovery/packages)               |
| - MASTERDB BCAES query boundary (GET /bcaes/registries/capability/objects)      |
| - Local census reconciliation invariants (41 passing Vitest tests)              |
+---------------------------------------------------------------------------------+
                                       |
                                       v
+---------------------------------------------------------------------------------+
| PENDING & BLOCKED BOUNDARIES (REQUIRING FORMAL CONFIRMATION)                    |
| - NIYANTRAN Workflow Executor contract: Unprobed; input/output schema pending   |
| - MDU Provenance Event Stream: Blocked by live read timeout; model mismatch     |
| - MASTERDB Capability Catalog: Blocked by 401 Bearer token requirement          |
| - Slice 1 Capability Seeding: 0 Slice 1 repos registered in live catalog        |
| - Ecosystem IAM / SSO: No centralized identity provider currently deployed     |
+---------------------------------------------------------------------------------+
```
