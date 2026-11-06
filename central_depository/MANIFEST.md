# BHIV Central Depository — CLO Agent Package Manifest

**Version:** 1.0.0-p0  
**Capability ID:** `cap-clo-legal-intelligence-v1`  
**Domain:** `dom-legal-regulatory-in` (Legal Regulatory Intelligence Substrate)  
**Classification:** C-Suite Executive Intelligence & Legal Reasoning Foundation  
**Accountable Build Owner:** Ansh (CLO Build Owner)  
**Supervisor / Authority:** Nupur (MDU & Programme Authority)  
**Depository Handover Specialist:** Ranjit  
**Audit Standard:** Code-Verified Invariants (Rules 0.1 – 0.9)  
**Date:** 2026-11-06  

---

## 1. Package Manifest & Ownership Registry

| Field | Canonical Value | Verification Status |
| :--- | :--- | :---: |
| **Package Name** | `bhiv-clo-agent` | `VERIFIED` |
| **Semantic Version** | `1.0.0-p0` | `VERIFIED` |
| **Canonical Repository** | `https://github.com/praj33/BHIV-BIQOS-P0-EXECUTION` | `VERIFIED` |
| **Feature Branch** | `feat/clo-agent-increment` | `VERIFIED` |
| **Pull Request** | `https://github.com/praj33/BHIV-BIQOS-P0-EXECUTION/pull/1` | `ACTIVE` |
| **Commit SHA** | `c2651168cd642c1157cf34622d0b8fa51783f245` | `VERIFIED` |
| **Execution Environment** | Python 3.12 / FastAPI / Uvicorn | `VERIFIED LOCAL` |
| **Automated Tests** | 20 / 20 Passing (Pytest 8.3.4 · 0.23s) | `PASSING` |
| **Production Readiness** | Stage B Capability Increment (Deployment/Security proven locally) | `STAGE B VERIFIED` |

---

## 2. Canonical Source Inventory

The canonical source code lives in the repository root under `clo/`. This depository package indexes and references those files without parallel code duplication:

| Subsystem Component | File Path | Functional Role | Line Count |
| :--- | :--- | :--- | :---: |
| **CLO Package Root** | `clo/__init__.py` | Package exports and version tag | 10 |
| **Domain Schemas** | `clo/schemas/models.py` | Pydantic v2 typed models, MDU event schemas | ~140 |
| **Canonical Corpus** | `clo/registry/corpus.py` | 8 official public statutes with verbatim passages | ~370 |
| **Legal Registry Engine** | `clo/registry/registry.py` | Ingestion, temporal as-of-date status evaluator | ~140 |
| **Reasoning Foundation** | `clo/reasoning/engine.py` | Evidence extraction, Rule 5 refusal, conflict surfacing | ~150 |
| **Runtime Service** | `clo/runtime/api.py` | FastAPI application (`/health`, `/research`, `/analyse`) | ~170 |
| **MDU Lineage Adapter** | `clo/adapters/mdu_adapter.py` | Chronological append-only provenance event mapper | ~95 |
| **TANTRA Execution Adapter** | `clo/adapters/tantra_adapter.py` | Workload participant complying with EXECUTION_CONTRACT.md | ~110 |
| **VAJRA Trust Adapter** | `clo/adapters/vajra_adapter.py` | 8-state authority lifecycle & Rule 8 Bounded Agent guard | ~165 |
| **InsightFlow Telemetry** | `clo/adapters/insightflow_adapter.py` | Passive-only telemetry emitter (passive: true) | ~75 |

---

## 3. Documentation & Verification Index

| Document Title | Path | Primary Purpose |
| :--- | :--- | :--- |
| **Baseline Review Packet** | `docs/clo/CLO_BASELINE_REVIEW_PACKET.md` | Phase 1 baseline assessment, component classification, scope freeze. |
| **Legal Corpus Manifest** | `docs/clo/LEGAL_CORPUS_MANIFEST.md` | Authoritative manifest of 8 ingested public legal documents and gazette URLs. |
| **API & Schema Notes** | `docs/clo/API_AND_SCHEMA_NOTES.md` | OpenAPI routes, typed payload schemas, error semantics, trace IDs. |
| **Proposal to MDU** | `docs/clo/PROPOSAL_TO_MDU_LEGAL_SCHEMA.md` | Formal written proposal to Nupur/MDU for canonical legal schema registration. |
| **ECC Integration Spec** | `docs/clo/EXECUTIVE_CONTROL_CENTER_INTEGRATION.md` | Integration contract for Rahil (Executive Control Center C-suite dashboard). |
| **Test Evidence Register** | `docs/clo/TEST_EVIDENCE.md` | Complete terminal outputs for all 20 executed automated test cases. |
| **Integration Status Matrix** | `docs/clo/INTEGRATION_STATUS_TABLE.md` | Verified / Mocked / Blocked status table across all adjacent platforms. |
| **Rollback Instructions** | `docs/clo/ROLLBACK_INSTRUCTIONS.md` | Disaster recovery and emergency state isolation procedures. |
| **Local Run Guide** | `docs/clo/LOCAL_RUN_INSTRUCTIONS.md` | Reproducible local execution instructions, Swagger docs, cURL queries. |
| **Limitations & Deployment** | `docs/clo/LIMITATIONS_AND_DEPLOYMENT.md` | Declared gaps, blockers, and next three accountable task assignments. |
| **Sample Query Output** | `docs/clo/SAMPLE_EVIDENCE_QUERY.json` | Real live JSON payload preserving evidence, citations, and review flags. |

---

## 4. Central Depository Handover Certification

This increment is delivered under strict compliance with the BHIV Anti-Parallel Mandate:
1. **Zero Duplicate Storage or Identity**: No parallel registries, no shadow blockchains, no synthetic authentication mechanisms.
2. **Deterministic Evidence Only**: Zero claims of completion without passing test executions or verbatim Gazette citations.
3. **Fail-Closed Security**: Unauthenticated callers, revoked actors (`REVOKE`), and unauthorized scopes are strictly rejected with `HTTP 403 Forbidden`.
4. **Governed Traceability**: All legal reasoning operations are tied to an immutable `trace_id` and registered with MDU append-only event lineage.

**Certified by Build Owner:** Ansh (CLO Build Owner)  
**Accepted for Depository by:** Ranjit (Central Depository Handover)  

