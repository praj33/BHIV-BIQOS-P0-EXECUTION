# BIQOS P0 — Interface Contract Status Inventory

**Author:** Raj, Accountable Technical Lead  
**Scope:** Inspected Architectural Schemas, API Contracts & Compatibility Status  
**Operating Policy:** Inventory only contracts actually inspected in source code or live cluster.  

---

## 1. Inspected Schemas & Interface Inventory

| Contract Identifier | Originating System | Source File / Document Location | Declared Version | Verification Status | Known Compatibility Issues | Missing Documentation | Required Owner Confirmation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`MasterDbCapability`** | MASTERDB Core | `app/src/types/masterdb.ts:L3-L20` | `v1.3.0` | `VERIFIED IN SOURCE` | Live `/capabilities` requires Bearer auth; unauthenticated fallback queries `/bcaes`. | Schema for nested `contract.schema_ref`. | Rayyan / Platform Lead |
| **`BcaesRegistryObject`** | MASTERDB BCAES Module | `bcaes_registry/models.py`, `# BCAES Canonical Registry Architecture.txt` | `v1.0.0` | `VERIFIED IN SOURCE` & `VERIFIED LIVE` | Registry currently returns empty array `[]` (0 seeded objects). | Formal data-entry guide for 11 object registries. | Kavy (BCAES Owner) |
| **`TantraPackage`** | TANTRA / MASTERDB Discovery | `app/src/types/masterdb.ts:L48-L62` | `v1.0` to `v2.0` | `VERIFIED IN SOURCE` & `VERIFIED LIVE` | Unpinned schema versions across packages (`v1.0`, `v1.1`, `v1.2`, `v2.0`). | Schema registry migration rules between minor versions. | TANTRA Team Lead |
| **`TantraRuntimeEnvelope`** | TANTRA Runtime Engine | `app/src/types/masterdb.ts:L104-L115` | `v1.0.0` | `VERIFIED IN SOURCE` & `VERIFIED LIVE` | MDU provenance fetch times out; lineage gaps documented in payload. | Corrective action promotion API documentation. | TANTRA / MDU Leads |
| **`CanonicalBiqosRecord`** | BIQOS Convergence Model | `app/src/types/biqos.ts:L98-L122` | `v2.2.0` | `VERIFIED IN SOURCE` & `VERIFIED BY TEST` | None within BIQOS. Fully normalized across 6 dimensions. | Upstream dependency graph schema. | Raj (Technical Lead) |
| **`RawCensusRecord`** | Capability Census | `01-source-data/Capability_Census.json` | Baseline | `VERIFIED IN SOURCE` | Null `deployment_system` for deployed records (e.g. record #60). | Census maintenance and update protocol. | Data Steward |
| **`RawInventoryRepository`** | Slice 1 Inventory | `01-source-data/Slice_1_Repository_Inventory.json` | Baseline | `VERIFIED IN SOURCE` | Port-only declarations without host URL (repos #6, #18, #19, #20). | Production host domain naming standards. | Data Steward |
| **`MduProvenanceEvent`** | MDU Provenance Engine | Live Envelope (`known_gaps`) | `api/v1` | `BLOCKED` (Live Timeout) | Append-only event list vs. MASTERDB single-pointer expectation. | MDU OpenAPI specification for canonical dataset endpoints. | Nupur (MDU Owner) |
| **`NiyantranTaskExecution`** | NIYANTRAN Workflow Platform | `bhiv-Shakti-GC-Infra` (External) | Uninspected | `UNKNOWN / NOT INSPECTED` | Complete external repository; API contracts not yet verified in workspace. | OpenAPI 3.0 specification for task dispatch and state polling. | Karana / Pratik |
