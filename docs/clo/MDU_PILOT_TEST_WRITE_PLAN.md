# Pilot Plan: Isolated Namespaced Test Write to MDU (Parakosha)

**Document Reference:** `docs/clo/MDU_PILOT_TEST_WRITE_PLAN.md`  
**To:** Nupur Gavane (MDU Authority & Programme Supervisor)  
**From:** Ansh (CLO Build Owner)  
**Date:** 2026-11-09  
**Status:** DRAFT SUBMISSION FOR SUPERVISOR REVIEW & KEY PROVISIONING  
**Authority Reference:** Sir’s Revised Assignment (Approving `LEGAL` category through MDU governance, maintaining `AMENDS`/`REPLACES` in payload, authorizing isolated namespaced test writes only)  

---

## 1. Executive Summary & Governance Guardrails

In accordance with Sir’s revised assignment and MDU supervisory governance:
1. **Zero Production Writes:** No production datasets (such as `BHIV-DS-LEGAL-DPDP-ACT-2023-001`) will be registered or written to during this pilot.
2. **Isolated Namespacing:** All pilot operations are strictly restricted to the designated test identifier: `BHIV-DS-LEGAL-TEST-PILOT-001`.
3. **Vocabulary & Relation Conformance:** The `LEGAL` category is used for `domain_primary`. Domain-specific relationship types (`AMENDS`, `REPLACES`, `SUPERSEDED_BY`) remain strictly inside the document payload (`relations` array) and are **not** written to top-level MDU relationships.
4. **MDU Endpoint:** All operations target the official MDU VM instance at `https://parakosha.blackholeinfiverse.com`.
5. **No Execution Without Prior Approval:** Zero writes will be dispatched until Nupur provides the authorized `X-API-Key` and records formal supervisory approval.

---

## 2. Schema Compatibility Specification

The pilot write strictly conforms to MDU's live write validator rules:

| MDU Validator Rule | CLO Implementation in Pilot |
| :--- | :--- |
| **Endpoint** | `https://parakosha.blackholeinfiverse.com` |
| **Authentication** | `X-API-Key: <MDU_API_KEY_PROVIDED_BY_NUPUR>` |
| **Accepted Event Types** | Uses `ORIGIN` for initial dataset provenance creation. (No `RETRIEVAL` events sent to MDU). |
| **Server-Assigned Fields** | `id` (event UUID) and `recorded_at` (ISO-8601 UTC timestamp) are server-assigned upon ingestion. |
| **Actor Mapping** | Mapped to `recorded_by: "CLO_BUILD_OWNER_ANSH"`. |
| **Evidence / Integrity Hash** | Cryptographic SHA-256 hash transported inside `transformation_reference.evidence_hash`. |
| **Relationship Encapsulation** | `AMENDS` and `REPLACES` encapsulated inside `transformation_reference.payload.relations`, leaving MDU top-level relationships untouched. |
| **Domain Category** | `domain_primary: "LEGAL"` (approved under Sir's revised assignment). |

---

## 3. Test Dataset Identifier

- **Canonical Test Dataset ID:** `BHIV-DS-LEGAL-TEST-PILOT-001`
- **Pattern Match:** `^BHIV-DS-LEGAL-TEST-PILOT-[0-9]{3}$` (Conforms to `BHIV-DS-{DOMAIN}-{NAME}-{NUMBER}`)
- **Domain Sub-classification:** `Regulatory & Statutory Corpus (Test Isolation)`
- **Lifecycle Status:** `TEST_ISOLATED`
- **Is Test Flag:** `true`

---

## 4. The Write Operation (Exact Payload)

### 4.1 Provenance Event: `ORIGIN`
- **Target Route:** `POST https://parakosha.blackholeinfiverse.com/api/v1/events` (or `/api/v1/provenance`)
- **Headers:**
  ```http
  Content-Type: application/json
  X-API-Key: <PROVIDED_BY_NUPUR>
  X-Trace-ID: trace-clo-pilot-write-001
  ```

### 4.2 Request Body:
```json
{
  "dataset_id": "BHIV-DS-LEGAL-TEST-PILOT-001",
  "event_type": "ORIGIN",
  "recorded_by": "CLO_BUILD_OWNER_ANSH",
  "transformation_reference": {
    "evidence_hash": "sha256:442d1a1bd144c84a55bbdffc1f94790bc994b9da3051b498eedacd0fda154599",
    "document_id": "doc-in-dpdp-act-2023-test-pilot",
    "title": "The Digital Personal Data Protection Act, 2023 (Pilot Test Extract)",
    "short_name": "DPDP Act 2023 (Test)",
    "issuing_authority": "Ministry of Law and Justice / MeitY",
    "jurisdiction": "India",
    "source_url": "https://egazette.gov.in/WriteReadData/2023/248045.pdf",
    "publication_date": "2023-08-11",
    "enactment_date": "2023-08-11",
    "effective_date": "2027-05-13",
    "version": "1.0.0-pilot",
    "status": "PENDING_COMMENCEMENT",
    "gazette_notification_ref": "G.S.R. 843(E) dated 13 November 2025",
    "relations": [
      {
        "relation_type": "AMENDS",
        "target_dataset_id": "BHIV-DS-LEGAL-IT-ACT-2000-001",
        "target_section": "Section 43A",
        "effective_date": "2027-05-13",
        "description": "Omits Section 43A of the Information Technology Act, 2000 per DPDP Section 44(2) upon scheduled commencement."
      }
    ],
    "sample_passage": {
      "section_number": "8",
      "heading": "General obligations of Data Fiduciary",
      "text": "A Data Fiduciary shall protect personal data in its possession or under its control, including in respect of any processing undertaken by it or on its behalf by a Data Processor, by taking reasonable security safeguards to prevent personal data breach."
    }
  }
}
```

---

## 5. Audit Procedure

Immediately upon dispatch of the write:
1. **HTTP Status Code Verification:** Confirm server returns `201 Created` (or `200 OK`).
2. **Capture Server Attributes:** Extract and record:
   - Server-assigned `id` (e.g. `mdu-ev-...` or server UUID)
   - Server-assigned `recorded_at` timestamp
3. **Payload Hash Integrity Check:** 
   - Recompute SHA-256 over raw canonical payload bytes.
   - Assert equality: `sha256(payload_bytes) == transformation_reference.evidence_hash`.
4. **Audit Trail Logging:** Record full request, response, and latency in:
   - `docs/clo/MDU_PILOT_AUDIT_REPORT.json`
   - Local InsightFlow telemetry trace.

---

## 6. Validation Procedure (Read-Back & Lineage Query)

To prove that the write succeeded without data corruption or schema mismatch:
1. **Read-Back Query:**
   ```http
   GET https://parakosha.blackholeinfiverse.com/api/v1/datasets/BHIV-DS-LEGAL-TEST-PILOT-001/provenance
   X-API-Key: <PROVIDED_BY_NUPUR>
   ```
2. **Validation Invariants:**
   - Response contains the recorded event.
   - `dataset_id` matches `BHIV-DS-LEGAL-TEST-PILOT-001`.
   - `event_type` is `ORIGIN`.
   - `recorded_by` is `CLO_BUILD_OWNER_ANSH`.
   - `transformation_reference.evidence_hash` matches client-side SHA-256.
   - `transformation_reference.relations[0].relation_type` is intact as `AMENDS`.
   - Server response schema complies with MDU OpenAPI specifications.

---

## 7. Cleanup & Rollback Procedure

To ensure the test dataset leaves zero operational footprint or schema pollution:
1. **Tombstoning via Append-Only Event:**
   In compliance with MDU’s append-only design, append a concluding `VALIDATION` event retiring the test dataset:
   ```json
   {
     "dataset_id": "BHIV-DS-LEGAL-TEST-PILOT-001",
     "event_type": "VALIDATION",
     "recorded_by": "CLO_BUILD_OWNER_ANSH",
     "transformation_reference": {
       "action": "TOMBSTONE_TEST_DATASET",
       "status": "TEST_RETIRED",
       "retired_at": "2026-11-09T...",
       "reason": "Pilot write validation complete. Isolated test dataset retired.",
       "is_test": true,
       "active": false
     }
   }
   ```
2. **Isolation Guarantee:** Production dataset catalog queries filter by `status != "TEST_RETIRED"` or ignore the `TEST-PILOT` namespace.
3. **Emergency Rollback:** If the write fails validation or exhibits unexpected behavior, the test dataset is immediately retired via tombstone event, and the incident is documented in `docs/clo/MDU_PILOT_AUDIT_REPORT.json` without modifying any production dataset.

---

## 8. Verification Checklist Before Execution

- [x] Schema compatibility confirmed against MDU write validator.
- [x] `LEGAL` category assigned to `domain_primary`.
- [x] `AMENDS`/`REPLACES` retained inside payload, not top-level relations.
- [x] Test dataset namespaced as `BHIV-DS-LEGAL-TEST-PILOT-001`.
- [x] Provision-level commencement date (`2027-05-13` per G.S.R. 843(E)) reflected in payload.
- [x] Audit and read-back validation steps scripted.
- [x] Append-only tombstone cleanup procedure defined.
- [ ] MDU API key received from Nupur.
- [ ] Formal supervisory approval recorded by Nupur.
