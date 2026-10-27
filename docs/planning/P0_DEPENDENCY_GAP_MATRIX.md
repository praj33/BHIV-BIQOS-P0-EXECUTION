# BIQOS P0 — Dependency Gap Matrix

**Author:** Raj, Accountable Technical Lead  
**Scope:** TANTRA Discovery Packages vs. Slice 1 Repositories & Upstream System Blockers  
**Status:** Ground-Truth Verified against Live Cluster (`http://163.128.209.18:30308`)  

---

## 1. Discovered TANTRA Packages vs. Slice 1 Repositories

| # | Discovered TANTRA Package | Target Capability ID | Domain Board | Declared Owner | Status in MASTERDB | Corresponds to Slice 1 Repository? | Reason for Non-Mapping |
| :-: | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **1** | `pkg-4d44c0a2dbc0` | `cap-marine-intel-ports` | Maritime | `masterdb-governance` | `REGISTERED` | **NO** | Domain dataset; not a Slice 1 code repository. |
| **2** | `pkg-5b5054524525` | `cap-gev-wildfire-perimeter-monitoring` | Geospatial | `masterdb-governance` | `REGISTERED` | **NO** | Domain dataset; not a Slice 1 code repository. |
| **3** | `pkg-7aea803f1d1f` | `cap-maritime-cargo` | Maritime | `masterdb-governance` | `REGISTERED` | **NO** | Domain dataset; not a Slice 1 code repository. |
| **4** | `pkg-818ddeb15e98` | `cap-fin-market-analytics` | Finance | `masterdb-governance` | `REGISTERED` | **NO** | Domain dataset; not a Slice 1 code repository. |
| **5** | `pkg-82569894af98` | `cap-gev-satellite-pass-prediction` | Geospatial | `masterdb-governance` | `REGISTERED` | **NO** | Domain dataset; not a Slice 1 code repository. |
| **6** | `pkg-a5cc8fc1bfc6` | `cap-mangrove-monitoring` | Geospatial | `masterdb-governance` | `REGISTERED` | **NO** | Domain dataset; not a Slice 1 code repository. |
| **7** | `pkg-ae7d8c2a73ff` | `cap-gev-earthquake-monitoring` | Geospatial | `masterdb-governance` | `REGISTERED` | **NO** | Domain dataset; not a Slice 1 code repository. |
| **8** | `pkg-b8d6f4428e5a` | `cap-bharat-mala-highways` | Infrastructure | `masterdb-governance` | `REGISTERED` | **NO** | Domain dataset; not a Slice 1 code repository. |
| **9** | `pkg-d77f8fa6db3d` | `cap-gev-weather-forecast-tracking` | Geospatial | `masterdb-governance` | `REGISTERED` | **NO** | Domain dataset; not a Slice 1 code repository. |

> [!CRITICAL]
> **Zero Inferred Mappings Invariant**  
> Even where superficial name similarities exist (e.g., `ds-fin-001` vs. `bhiv-Trade_Bot_`, or `ds-maritime-001` vs. `bhi-Namami-Gange-Demo`), there is **zero authoritative evidence** linking them.  
> All 20 Slice 1 repositories remain strictly `UNREGISTERED_IN_MASTERDB` until an approved capability manifest is formally ingested into MASTERDB.

---

## 2. Upstream Architecture & Infrastructure Dependency Gaps

| Dependency ID | Dependent Component | Upstream System | Nature of Gap | Ground-Truth Finding & Evidence | Severity | Suggested Owner |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: |
| **GAP-01** | Package Readiness | **MDU** | Service Timeout | `GET /api/v1/datasets/canonical/ds-*` times out during runtime envelope generation. | **CRITICAL** | Harsha |
| **GAP-02** | Package Lineage | **MDU** | Contract Incompatibility | MDU implements an append-only event stream; MASTERDB expects `knowledge_object_id` and `lineage_reference` pointer fields. | **HIGH** | Harsha |
| **GAP-03** | Capability Catalog | **MASTERDB** | Authentication Wall | `GET /capabilities` returns HTTP 401 Bearer Token Required, blocking unauthenticated catalog discovery. | **HIGH** | Rayyan |
| **GAP-04** | Capability Seeding | **MASTERDB** | Data Seeding Gap | 0 Slice 1 capabilities are seeded in MASTERDB. The public `/bcaes` registry currently returns 0 objects. | **CRITICAL** | Harsha |
| **GAP-05** | Workflow Execution | **NIYANTRAN** | Unprobed System | `bhiv-Shakti-GC-Infra` resides in an external repository with uninspected input/output contracts and execution endpoints. | **CRITICAL** | Karana |
| **GAP-06** | Identity & Access | **Platform Security** | Missing SSO/IAM | No ecosystem-wide IAM exists; service calls rely on static tokens without human identity verification. | **MEDIUM** | Rayyan |
| **GAP-07** | Schema Versioning | **MASTERDB** | Version Incoherence | Packages declare `schema_version` values of `v1.0`, `v1.1`, `v1.2`, and `v2.0` without a backward-compatibility matrix. | **MEDIUM** | Harsha |
