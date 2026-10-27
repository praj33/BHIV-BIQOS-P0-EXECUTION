# BIQOS P0 — Evidence & Artifact Index

**Custodian:** Raj, Accountable Technical Lead  
**Scope:** Immutable Index of Test Runs, Audits, Live API Responses & Build Hashes  
**Policy:** No synthetic evidence. Non-existing items are strictly labeled PENDING.  

---

## 1. Automated Test Execution Evidence

| Evidence ID | Test Scope | Runner & Environment | Results & Metrics | Verification Date | Primary Log / Report Location |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **EVD-TST-01** | Census Data Reconciliation | Vitest v3.0.7 / Node.js 20 / Windows | **13 / 13 passing (100%)** in 10ms | 2026-10-26 | `app/src/tests/reconciliation.test.ts` |
| **EVD-TST-02** | MASTERDB & TANTRA Adapter | Vitest v3.0.7 / Node.js 20 / Windows | **28 / 28 passing (100%)** in 91ms | 2026-10-26 | `app/src/tests/masterdb.test.ts` |
| **EVD-TST-03** | Total Integrated Unit Suite | Vitest v3.0.7 / Node.js 20 / Windows | **41 / 41 passing (100%)** in 772ms | 2026-10-26 | Reproduced in Stage A Audit |
| **EVD-LNT-01** | Code Quality & Linter | Oxlint / 17 codebase files | **0 errors, 0 warnings** in 5ms | 2026-10-26 | `.oxlintrc.json` execution log |
| **EVD-BLD-01** | Production Build Bundle | TypeScript 5.7 / Vite v6.4.1 | Bundle size: **18.57 kB CSS (gzip 4.33 kB)** | 2026-10-26 | `dist/assets/index-DR7pYILA.css` |

---

## 2. Live Network Interrogation Evidence

| Evidence ID | Target Endpoint | HTTP Method | Response Status | Key Response Findings | Capture Timestamp |
| :--- | :--- | :---: | :---: | :--- | :---: |
| **EVD-NET-01** | `http://163.128.209.18:30308/health` | GET | `200 OK` | Returns `status: "healthy"`, `version: "1.3.0"`. | 2026-10-26T14:17:15Z |
| **EVD-NET-02** | `http://163.128.209.18:30308/capabilities` | GET | `401 Unauthorized` | Returns `Missing bearer token`. Proves auth boundary. | 2026-10-26T14:17:18Z |
| **EVD-NET-03** | `http://163.128.209.18:30308/bcaes/registries/capability/objects` | GET | `200 OK` | Returns `{ "registry_type": "capability", "objects": [] }`. | 2026-10-26T14:17:22Z |
| **EVD-NET-04** | `http://163.128.209.18:30308/discovery/packages` | GET | `200 OK` | Returns `count: 9` packages, all in state `REGISTERED`. | 2026-10-26T14:17:39Z |
| **EVD-NET-05** | `http://163.128.209.18:30308/tantra/packages/pkg-4d44c0a2dbc0/runtime` | GET | `200 OK` | Returns `retrieval_readiness.status == "NOT_RETRIEVABLE"`, documents 3 MDU gaps. | 2026-10-26T14:18:02Z |

---

## 3. UI Baseline & Audit Evidence

| Evidence ID | Scope | Visual Reference Artifact | Comparison Result | Date |
| :--- | :--- | :--- | :--- | :---: |
| **EVD-UI-01** | Desktop Dashboard Baseline | `desktop_view_1791804781824.png` (1920×945) | Exact match: 44px banner, 7 KPI cards, 20-row table. | 2026-10-23 |
| **EVD-UI-02** | Desktop Record Drawer | `desktop_row1_drawer_1791876447257.png` | Exact 3-section match: 6 Dimensions, Audit, Reconciliation. | 2026-10-23 |
| **EVD-UI-03** | Mobile Drawer Layout | `mobile_row1_drawer_1791876459067.png` (500×717) | Exact match: single-column vertical card stacking, zero overflow. | 2026-10-23 |
| **EVD-UI-04** | Banner Wording Verification | `SystemBanner.tsx` line audit | Status: `Local Reconciliation Active · Verified Read-Only Connectivity`. | 2026-10-23 |

---

## 4. Pending Future Demonstration Evidence

| Evidence ID | Demonstration Description | Target Deliverable | Current Status |
| :--- | :--- | :--- | :---: |
| **EVD-DEM-01** | Read-Only TANTRA Discovery & Readiness Run Log | JSON summary output of thin-thread audit | `PENDING` |
| **EVD-DEM-02** | NIYANTRAN Trial Task Execution Output | Signed execution receipt with exit code 0 | `PENDING` |
| **EVD-DEM-03** | MDU Provenance Event Stream Capture | JSON event list for canonical dataset | `PENDING` |
