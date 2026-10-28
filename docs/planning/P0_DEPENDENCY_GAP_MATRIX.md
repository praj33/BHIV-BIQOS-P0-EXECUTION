# BIQOS P0 — Dependency Gap Matrix

**Author:** Raj, Accountable Technical Lead  
**Scope:** TANTRA Discovery Packages vs. Slice 1 Repositories & Upstream System Blockers  
**Status:** Ground-Truth Verified against Live Cluster (`http://163.128.209.18:30308`) on 2026-10-28

---

## 1. Discovered TANTRA Packages vs. Slice 1 Repositories (Active Reseed: 12 Packages)

On **October 28, 2026 at 07:38:09 UTC**, the live MASTERDB cluster reseeded, expanding the public discovery catalog from 9 to **12 Knowledge Packages**, with package IDs observed to have rotated across cluster snapshots (note: the internal backend ID-generation contract has not been inspected):

| # | Active TANTRA Package ID | Target Dataset ID | Domain Board | Declared Owner | Status in MASTERDB | Corresponds to Slice 1 Repository? | Reason for Non-Mapping | Historical Stage A ID (Pre-Reseed) |
| :-: | :--- | :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **1** | `pkg-cd95bf999daa` | `ds-marine-intel-ports` | Maritime | `masterdb-governance` | `REGISTERED` | **NO** | Domain dataset; not a Slice 1 code repository. | `pkg-4d44c0a2dbc0` (Now 404) |
| **2** | `pkg-8ac4a5f564e8` | `ds-gev-wildfire-perimeters` | Geospatial | `masterdb-governance` | `REGISTERED` | **NO** | Domain dataset; not a Slice 1 code repository. | `pkg-5b5054524525` |
| **3** | `pkg-fdb252a97b55` | `ds-maritime-001` | Maritime | `masterdb-governance` | `REGISTERED` | **NO** | Domain dataset; not a Slice 1 code repository. | `pkg-7aea803f1d1f` |
| **4** | `pkg-c6eb4a8ecdc1` | `ds-fin-001` | Finance | `masterdb-governance` | `REGISTERED` | **NO** | Domain dataset; not a Slice 1 code repository. | `pkg-818ddeb15e98` |
| **5** | `pkg-024a72e872b8` | `ds-gev-satellite-tles` | Geospatial | `masterdb-governance` | `REGISTERED` | **NO** | Domain dataset; not a Slice 1 code repository. | `pkg-82569894af98` |
| **6** | `pkg-bd17d06784ae` | `ds-mangrove-001` | Geospatial | `masterdb-governance` | `REGISTERED` | **NO** | Domain dataset; not a Slice 1 code repository. | `pkg-a5cc8fc1bfc6` |
| **7** | `pkg-e71aa726f3f4` | `ds-gev-seismic-events` | Geospatial | `masterdb-governance` | `REGISTERED` | **NO** | Domain dataset; not a Slice 1 code repository. | `pkg-ae7d8c2a73ff` |
| **8** | `pkg-5f825da9d452` | `ds-bharatmala-001` | Infrastructure | `masterdb-governance` | `REGISTERED` | **NO** | Domain dataset; not a Slice 1 code repository. | `pkg-b8d6f4428e5a` |
| **9** | `pkg-97aad5d44ad8` | `ds-gev-weather-telemetry` | Geospatial | `masterdb-governance` | `REGISTERED` | **NO** | Domain dataset; not a Slice 1 code repository. | `pkg-d77f8fa6db3d` |
| **10** | `pkg-04d17aaca527` | `DS-FSI-ISFR-2023-FOREST-COVER` | Geospatial | `masterdb-governance` | `REGISTERED` | **NO** | Forestry dataset; not a Slice 1 code repository. | *New in Oct 28 reseed* |
| **11** | `pkg-b28e736588f8` | `DS-VANA-SPATIAL-LAYERS` | Geospatial | `masterdb-governance` | `REGISTERED` | **NO** | Spatial layer dataset; not a Slice 1 code repository. | *New in Oct 28 reseed* |
| **12** | `pkg-ba021794347b` | `DS-VANA-THANE-CREEK-BLUE-CARBON` | Geospatial | `masterdb-governance` | `REGISTERED` | **NO** | Blue carbon dataset; not a Slice 1 code repository. | *New in Oct 28 reseed* |

> [!CRITICAL]
> **Zero Inferred Mappings Invariant**  
> Even with the addition of VANA spatial datasets (`DS-VANA-SPATIAL-LAYERS`, `DS-VANA-THANE-CREEK-BLUE-CARBON`), which share nomenclature with Slice 1 repository #19 (`bhiv-Vana_lineage_dashboard`), there is **zero authoritative evidence** mapping them.
> All 20 Slice 1 repositories remain strictly `UNREGISTERED_IN_MASTERDB` until an approved capability manifest is formally ingested into MASTERDB.

---

## 2. Upstream Architecture & Infrastructure Dependency Gaps

| Dependency ID | Dependent Component | Upstream System | Nature of Gap | Ground-Truth Finding & Evidence | Severity | Suggested Owner |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: |
| **GAP-01** | Package Readiness | **MDU** | Service Timeout | `GET /api/v1/datasets/canonical/ds-*` times out during runtime envelope generation (re-verified on `pkg-cd95bf999daa` on 2026-10-28). | **CRITICAL** | Harsha |
| **GAP-02** | Package Lineage | **MDU** | Contract Incompatibility | MDU implements an append-only event stream; MASTERDB expects `knowledge_object_id` and `lineage_reference` pointer fields. | **HIGH** | Harsha |
| **GAP-03** | Capability Catalog | **MASTERDB** | Authentication Wall | `GET /capabilities` returns HTTP 401 Bearer Token Required, blocking unauthenticated catalog discovery. | **HIGH** | Rayyan |
| **GAP-04** | Capability Seeding | **MASTERDB** | Data Seeding Gap | 0 Slice 1 capabilities are seeded in MASTERDB. The public `/bcaes` registry currently returns 0 objects. | **CRITICAL** | Harsha |
| **GAP-05** | Workflow Execution | **NIYANTRAN** | Unprobed System | `bhiv-Shakti-GC-Infra` resides in an external repository with uninspected input/output contracts and execution endpoints. | **CRITICAL** | Karana |
| **GAP-06** | Identity & Access | **Platform Security** | Missing SSO/IAM | No ecosystem-wide IAM exists; service calls rely on static tokens without human identity verification. | **MEDIUM** | Rayyan |
| **GAP-07** | Schema Versioning | **MASTERDB** | Version Incoherence | Packages declare `schema_version` values of `v1.0`, `v1.1`, `v1.2`, and `v2.0` without a backward-compatibility matrix. | **MEDIUM** | Harsha |
| **GAP-08** | Identifier Stability | **MASTERDB** | Package ID Rotation | Package IDs observed to rotate across cluster reseed snapshots (e.g. `pkg-4d44c0a2dbc0` -> `pkg-cd95bf999daa`), breaking static ID references. No public canonical dataset lookup route was identified in the inspected interface. | **HIGH** | Rayyan / Raj |
