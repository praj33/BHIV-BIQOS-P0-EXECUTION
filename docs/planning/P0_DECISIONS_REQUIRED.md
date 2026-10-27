# BIQOS P0 — Architectural & Governance Decision Log

**Author:** Raj, Accountable Technical Lead  
**Scope:** Pending Decisions Requiring System Owner & Steering Committee Sign-Off  
**Status Policy:** Every item remains labeled PENDING until signed off with recorded evidence.  

---

## 1. Decision Register

| ID | Architectural / Governance Decision Topic | Affected Systems | Primary Options Considered | Recommended Option | Impact If Unresolved | Status | Required Sign-Off |
| :-: | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **DEC-01** | **Designation of Constitutional Workflow Executor** | NIYANTRAN, MASTERDB, BIQOS | **Option A**: NIYANTRAN (`bhiv-Shakti-GC-Infra`) as ecosystem task executor.<br>**Option B**: MASTERDB internal transition state graph.<br>**Option C**: Lightweight custom runner. | **Option A**: Preserves existing platform assignment to Karana/Pratik. | Cannot implement or test Stage B workflow execution. | `PENDING` | Technical Steering Committee / Sir |
| **DEC-02** | **Public Read-Only Capability Catalog Exposure** | MASTERDB, BIQOS | **Option A**: Expose unauthenticated `GET /capabilities/public` route.<br>**Option B**: Issue client-side read-only Bearer token to BIQOS.<br>**Option C**: Restrict catalog inspection solely to `/bcaes/*`. | **Option A**: Aligns with existing unauthenticated `/bcaes/*` and `/discovery/*` patterns. | BIQOS UI remains restricted to empty registry fallback. | `PENDING` | Platform Security (Rayyan) / Sir |
| **DEC-03** | **MDU Lineage Model Reconciliation** | MDU, MASTERDB, TANTRA | **Option A**: Retain legacy expectation of `knowledge_object_id` pointer.<br>**Option B**: Update MASTERDB to consume MDU's append-only event stream (`dataset_id` + timestamp). | **Option B**: Conforms to MDU's actual production reality and live contract. | 100% of packages remain permanently stuck at `NOT_RETRIEVABLE`. | `PENDING` | MDU Owner (Nupur) & MASTERDB Architect |
| **DEC-04** | **Slice 1 Capability Manifest Seeding Authority** | BIQOS, MASTERDB, Census | **Option A**: Data Steward centrally authors and seeds 20 Slice 1 capabilities into MASTERDB.<br>**Option B**: Individual repo owners self-register.<br>**Option C**: BIQOS automatically seeds on startup. | **Option A**: Prevents uncoordinated drift and enforces schema compliance. | Slice 1 records remain indefinitely unseeded (`UNREGISTERED_IN_MASTERDB`). | `PENDING` | Data Steward / Project Lead |
| **DEC-05** | **Authoritative Policy for Candidate Aliases** | BIQOS, Census, Inventory | **Option A**: Formally approve 4 candidate aliases (`bhiv-UCCIS-Final`, etc.).<br>**Option B**: Require repo owners to update repository names.<br>**Option C**: Keep permanently as unverified warnings. | **Option A**: Resolves 4 candidate warnings with documented audit trail. | 4 repositories remain flagged with governance warnings. | `PENDING` | Repository Owners & Data Steward |
| **DEC-06** | **UI Baseline Preservation Invariant** | BIQOS Slice 1 UI | **Option A**: Lock Phase 2.1/2.2 layout permanently; integrate data into existing cards.<br>**Option B**: Redesign banner and drawer to show workflow execution traces. | **Option A**: Prevents visual bloat, keeps bundle size frozen (18.57 kB). | Uncontrolled UI churn and visual regression during Phase 4/5. | `CONFIRMED IN REPAIR` | Raj (Lead) & Sir |
