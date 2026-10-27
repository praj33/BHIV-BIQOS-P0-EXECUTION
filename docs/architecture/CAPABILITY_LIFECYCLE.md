# BHIV Ecosystem — Capability & Package Lifecycle Specification

**Author:** Raj, Accountable Technical Lead  
**Scope:** Constitutional State Machine Transitions & Evidence Gates  
**Status:** Approved Specification · Aligned with MASTERDB & TANTRA Runtimes  

---

## 1. The Canonical 6-Stage State Graph

Every capability, knowledge package, and workflow in the BHIV ecosystem progresses through a strictly directed, non-interchangeable lifecycle graph:

```
   [ DISCOVERED ]
          │
          ▼  (Registration Gate: Manifest Validation & Owner Assignment)
   [ REGISTERED ]
          │
          ▼  (Certification Gate: Rule Engine & Schema Verification)
   [ CERTIFIED ]
          │
          ▼  (Readiness Gate: Retrieval Rules & Lineage Completeness)
   [ AVAILABLE ]
          │
          ▼  (Invocation Gate: Authorized Dispatch & Idempotency Key)
    [ INVOKED ]
       ┌──┴──┐
       ▼     ▼
 [ COMPLETED ] [ FAILED ]  (Final State: Deterministic Evidence & Verification)
```

> [!CAUTION]
> **Non-Interchangeability Rule**  
> Discovery is **not** registration. Registration is **not** certification. Certification is **not** availability. Availability is **not** execution.  
> Skipping states or synthesizing attestations without authoritative evidence is a violation of BIQOS constitutional policy.

---

## 2. Stage-by-Stage Transition Specification

### Stage 1: DISCOVERED
* **Definition**: A candidate capability or repository has been identified in source code, static census files, or public registry announcements.
* **Entry Evidence**: Repository declaration in `01-source-data/Slice_1_Repository_Inventory.json` or package listed in `GET /discovery/packages`.
* **State Invariants**:
  - Attestation in BIQOS: `UNREGISTERED_IN_MASTERDB` or `UNATTESTED_LOCAL_RECONCILED`.
  - Runtime Health: Strictly `UNPROBED`.
  - Dependencies: Strictly `UNMAPPED`.
* **Exit Gate to REGISTERED**: Submission of a valid Capability Manifest signed by the designated repository owner.

---

### Stage 2: REGISTERED
* **Definition**: The capability is recorded in the MASTERDB BCAES catalog (`bcaes_registry/models.py:RegistryObject`) with an authoritative unique identifier.
* **ID Convention**: Prefix `cap-` for capabilities, `pkg-` for knowledge packages.
* **Required Metadata Fields**:
  - `id`: Unique identifier (e.g. `cap-shakti-auth`).
  - `name`: Canonical system name.
  - `version`: Semantic version string (`1.0.0`).
  - `owner`: Accountable team or individual.
  - `classification`: Fixed to registry type (`capability`).
  - `status`: `REGISTERED`.
* **Current Ground-Truth Reality**:
  - Exactly **9 TANTRA knowledge packages** are in state `REGISTERED`.
  - Exactly **0 Slice 1 capabilities** are in state `REGISTERED` in the live service.

---

### Stage 3: CERTIFIED
* **Definition**: The registered package or capability has been evaluated and approved by MASTERDB's deterministic rule validation engine (`config/validation_rules.json`).
* **Validation Invariants**:
  - Contract schema conforms to declared version (`schema_version`).
  - Status is active (not `DEPRECATED` or `ARCHIVED`).
  - All mandatory metadata fields are populated.
* **Transition Evidence**:
  - A transition event recorded in package history:
    `{ "from_status": "REGISTERED", "to_status": "CERTIFIED", "actor": "validation_engine" }`.
  - Cryptographic validation proof or SHA-256 replay hash.
* **Current Ground-Truth Reality**:
  - All 9 discovered packages **fail** certification (Rule `PACKAGE_CERTIFIED: false`, detail: `Package status is REGISTERED; CERTIFIED or RETRIEVAL_READY is required`).

---

### Stage 4: AVAILABLE (RETRIEVAL_READY)
* **Definition**: The capability or package is fully prepared for runtime querying, workflow invocation, or reasoning consumption by downstream services (TANTRA).
* **Constitutional Retrieval Readiness Rules**:
  1. `PACKAGE_CERTIFIED`: Must be `true`.
  2. `NOT_DEPRECATED_OR_ARCHIVED`: Must be `true`.
  3. `METADATA_COMPLETE`: Must be `true`.
  4. `LINEAGE_REGISTERED`: Source reference registered with MDU provenance engine.
* **Transition Evidence**:
  - Response from `GET /tantra/packages/{id}/runtime` returns:
    `retrieval_readiness.status == "RETRIEVAL_READY"`.
* **Current Ground-Truth Reality**:
  - 100% of discovered packages evaluate to `NOT_RETRIEVABLE` due to failing rules 1 and 4.

---

### Stage 5: INVOKED
* **Definition**: An authorized workflow execution platform (NIYANTRAN / SHAKTI) has accepted an execution command targeting an AVAILABLE capability.
* **Invocation Invariants**:
  - Input parameters validated against capability contract schema.
  - Caller identity and authorization verified via signed token.
  - Execution run ID assigned; idempotency key recorded.
  - Start timestamp and initial parameters logged to immutable store.
* **Current Ground-Truth Reality**:
  - No workflow invocation mechanism is implemented or connected in BIQOS Slice 1.

---

### Stage 6: COMPLETED or FAILED
* **Definition**: Execution has terminated, producing an immutable final-state evidence record.
* **COMPLETED Invariants**:
  - Exit code `0`; valid output payload conforming to contract schema.
  - Total duration recorded; telemetry reported to PRAVAH.
* **FAILED Invariants**:
  - Non-zero error code or structured error envelope (`errorType`, `message`, `retryable`).
  - Failure cause categorized: `VALIDATION_ERROR`, `TIMEOUT`, `NETWORK_ERROR`, `UNAUTHORIZED`.
  - Safe retry policy enforced (exponential backoff, max retry counter).
* **Final Attestation Output**:
  - An immutable, replayable verification report retained in the evidence index.
