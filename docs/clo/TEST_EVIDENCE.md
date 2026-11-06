# CLO Agent Increment — Test Execution & Evidence Register

**Product:** CLO (Chief Legal Officer) Agent Increment  
**Build Owner:** Ansh  
**Test Runner:** `pytest 8.3.4` (Python 3.12.3)  
**Execution Timestamp:** 2026-11-06T10:20:39Z  
**Target Repository:** `praj33/BHIV-BIQOS-P0-EXECUTION`  
**Feature Branch:** `feat/clo-agent-increment`  
**Status:** 20/20 PASSING (100% Pass Rate · 0.23s duration)  

---

## 1. Test Execution Command & Terminal Output

### Command Executed:
```bash
python3 -m pytest tests/clo -v
```

### Actual Terminal Output:
```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-8.3.4, pluggy-1.6.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /media/ubuntu/New Volume/project/blackhole-infiverse-products/CLO/BHIV-BIQOS-P0-EXECUTION
plugins: asyncio-0.24.0, anyio-4.14.2, colcon-core-0.19.0, cov-4.1.0
asyncio: mode=Mode.STRICT, default_loop_scope=None
collecting ... collected 20 items

tests/clo/test_clo_contracts.py::test_health_check_contract PASSED       [  5%]
tests/clo/test_clo_contracts.py::test_list_canonical_documents PASSED    [ 10%]
tests/clo/test_clo_contracts.py::test_get_individual_canonical_document PASSED [ 15%]
tests/clo/test_legal_retrieval_and_reasoning.py::test_evidence_preserved_in_data_protection_query PASSED [ 20%]
tests/clo/test_legal_retrieval_and_reasoning.py::test_fiduciary_duties_governance_query PASSED [ 25%]
tests/clo/test_negative_scenarios.py::test_hard_rule_5_zero_evidence_refusal PASSED [ 30%]
tests/clo/test_negative_scenarios.py::test_conflicting_sources_explicitly_surfaced PASSED [ 35%]
tests/clo/test_negative_scenarios.py::test_invalid_date_format_handled_gracefully PASSED [ 40%]
tests/clo/test_security_and_vajra_boundaries.py::test_vajra_valid_caller_granted PASSED [ 45%]
tests/clo/test_security_and_vajra_boundaries.py::test_vajra_revoked_caller_blocked_fail_closed PASSED [ 50%]
tests/clo/test_security_and_vajra_boundaries.py::test_vajra_suspended_caller_blocked PASSED [ 55%]
tests/clo/test_security_and_vajra_boundaries.py::test_vajra_unregistered_subject_blocked PASSED [ 60%]
tests/clo/test_security_and_vajra_boundaries.py::test_rule_8_bounded_agent_model PASSED [ 65%]
tests/clo/test_security_and_vajra_boundaries.py::test_truthstore_evidence_recording_auth PASSED [ 70%]
tests/clo/test_tantra_and_insightflow_integration.py::test_tantra_workload_execution_success PASSED [ 75%]
tests/clo/test_tantra_and_insightflow_integration.py::test_tantra_workload_unauthorized_signature_rejected PASSED [ 80%]
tests/clo/test_tantra_and_insightflow_integration.py::test_tantra_failure_isolation_offline_service PASSED [ 85%]
tests/clo/test_tantra_and_insightflow_integration.py::test_insightflow_passive_telemetry_emission PASSED [ 90%]
tests/clo/test_temporal_as_of_date.py::test_registry_as_of_date_supersession_logic PASSED [ 95%]
tests/clo/test_temporal_as_of_date.py::test_api_as_of_date_intermediary_timeline PASSED [100%]

============================== 20 passed in 0.23s ==============================
```

---

## 2. Test Scenario Verification Coverage

| Scenario ID | Test Function | Technical Invariant Verified | Outcome |
| :--- | :--- | :--- | :---: |
| **SCN-01** | `test_health_check_contract` | Verifies typed OpenAPI contract, 8 statutes in registry, active adapters. | `PASS` |
| **SCN-02** | `test_list_canonical_documents` | Validates all 8 canonical documents with official gazette URLs and SHA-256 hashes. | `PASS` |
| **SCN-03** | `test_get_individual_canonical_document` | Validates individual statutory sections, relations, and 404 error semantics. | `PASS` |
| **SCN-04** | `test_evidence_preserved_in_data_protection_query` | Verifies verbatim statutory passage survival, section citations, and MDU provenance links. | `PASS` |
| **SCN-05** | `test_fiduciary_duties_governance_query` | Verifies Companies Act 2013 directors' duties (Section 166) verbatim evidence. | `PASS` |
| **SCN-06** | `test_hard_rule_5_zero_evidence_refusal` | **Negative**: Unevidenced query returns `conclusion: null`, `INSUFFICIENT_EVIDENCE`, and review flag. | `PASS` |
| **SCN-07** | `test_conflicting_sources_explicitly_surfaced` | **Negative**: Conflicting provisions (Sec 43A vs DPDP omission) surfaced without silent resolution. | `PASS` |
| **SCN-08** | `test_invalid_date_format_handled_gracefully` | **Negative**: Invalid date format handled without 500 crash. | `PASS` |
| **SCN-09** | `test_vajra_valid_caller_granted` | Valid caller in `USE` state with valid token granted 200 OK. | `PASS` |
| **SCN-10** | `test_vajra_revoked_caller_blocked_fail_closed` | **Negative**: Revoked caller (`REVOKE` state) blocked fail-closed with 403 Forbidden. | `PASS` |
| **SCN-11** | `test_vajra_suspended_caller_blocked` | **Negative**: Suspended caller (`SUSPEND` state) blocked fail-closed with 403 Forbidden. | `PASS` |
| **SCN-12** | `test_vajra_unregistered_subject_blocked` | **Negative**: Unregistered caller rejected with 403 Forbidden. | `PASS` |
| **SCN-13** | `test_rule_8_bounded_agent_model` | Verifies Rule 8: read-only state view, direct ledger mutations strictly blocked. | `PASS` |
| **SCN-14** | `test_truthstore_evidence_recording_auth` | Verifies TruthStore recording enforces secret token verification (401 on unauthorized). | `PASS` |
| **SCN-15** | `test_tantra_workload_execution_success` | Validates TANTRA workload participant contract, deterministic SHA-256 execution hash. | `PASS` |
| **SCN-16** | `test_tantra_workload_unauthorized_signature_rejected` | **Negative**: Missing/forged bridge signature rejected fail-closed with 401 Unauthorized. | `PASS` |
| **SCN-17** | `test_tantra_failure_isolation_offline_service` | Verifies failure isolation: offline remote TANTRA handled gracefully without crash. | `PASS` |
| **SCN-18** | `test_insightflow_passive_telemetry_emission` | Verifies passive telemetry emission conforming to InsightFlow schema (`passive: true`). | `PASS` |
| **SCN-19** | `test_registry_as_of_date_supersession_logic` | Verifies temporal logic on past dates (2018 active vs 2024 superseded). | `PASS` |
| **SCN-20** | `test_api_as_of_date_intermediary_timeline` | Verifies end-to-end API temporal query: 1-month timeline in 2018 vs 15-day timeline in 2024. | `PASS` |

