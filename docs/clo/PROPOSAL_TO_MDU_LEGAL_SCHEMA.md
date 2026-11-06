# Formal Proposal to MDU Authority — Legal Domain Canonical Schema & Provenance Architecture (Revision 2)

**TO:** Nupur Gavane (MDU Authority & Programme Supervisor)  
**FROM:** Ansh (CLO Build Owner)  
**DATE:** 2026-11-06  
**STATUS:** REVISED SUBMISSION — Addressing MDU Review Feedback of 2026-11-06  
**SUBJECT:** Canonical Schema Proposal for Legal Domain Knowledge Objects & MDU Event Integration  

---

## 1. Governance Context & Purpose

Under **Constitutional Authority Boundaries (Rule 3)**:
> *"MDU = schema, memory, ontology, lineage, provenance authority. CLO (Ansh) = legal-domain capability only. No silent canon creation. No silent schema or semantic changes. Any proposed change to a canonical schema goes to Nupur/MDU as a written proposal, not a commit."*

This revised document addresses each item raised in the MDU Review ([`docs/clo/MDU_REVIEW_OF_CLO_LEGAL_SCHEMA_PROPOSAL.md`](https://github.com/praj33/BHIV-BIQOS-P0-EXECUTION/blob/main/docs/clo/MDU_REVIEW_OF_CLO_LEGAL_SCHEMA_PROPOSAL.md)). It establishes the canonical structure for the Legal Domain within MDU, conforms strictly to MDU's existing write validator, and adopts the official `BHIV-DS-{DOMAIN}-{NAME}-{NUMBER}` identifier convention.

---

## 2. Alignment with MDU Architecture & Feedback Resolution

In response to MDU review findings, the CLO Agent implementation adheres to the following MDU ground-truths:

1. **Dataset Identifier Format**: Replaced legacy lowercase `ds-legal-*` with MDU canonical format: `BHIV-DS-LEGAL-{NAME}-{NUMBER}` (uppercase).
2. **Event Types**: Restated event stream to MDU's accepted write-validator event types:
   - Accepted: `ORIGIN`, `INGESTION`, `TRANSFORMATION`, `VALIDATION`, `TRUST_CHANGE`, `SCHEMA_CHANGE`.
   - **`RETRIEVAL` dropped from MDU stream**: Query-time reads are not provenance events in MDU. CLO retains query execution traces internally and within InsightFlow telemetry, not as MDU dataset events.
3. **Event Fields & Evidence Hashes**:
   - `id` and `recorded_at` are server-assigned by MDU.
   - Client actor maps to `recorded_by`.
   - MDU currently does not have a native `evidence_hash` field. Cryptographic SHA-256 payload hashes are transported inside the `transformation_reference` JSON object.
4. **Relationship Types**: MDU relationships (`relationship_type`) are stored as strings up to 50 characters, with standard values `DERIVED_FROM` and `DEPENDS_ON`. Novel legal relationships (`AMENDS`, `REPLACES`, `SUPERSEDED_BY`, etc.) are retained inside the CLO document payload (`relations` array) and are **not** written to top-level MDU relationships pending supervisor decision on vocabulary extension.
5. **Domain Category**: Dataset metadata sets `domain_primary: "LEGAL"`. We formally submit a request to the supervisor to recognize "Legal" as a canonical category with Ansh designated as Domain Owner.
6. **Hash Ownership**: Acknowledged that MDU does not assign schema hashes; MASTERDB manages `knowledge_hash`.

---

## 3. Proposed Canonical Schemas

### 3.1 Domain Identifier & Metadata
- **Domain Primary**: `LEGAL`
- **Domain Sub-classification**: Regulatory & Statutory Corpus
- **Jurisdiction**: India (Commercial, Intermediary & Data Protection)
- **Domain Owner**: Ansh (CLO Build Owner)

### 3.2 Canonical Document Schema (`LegalDocument`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "LegalDocument",
  "type": "object",
  "required": [
    "mdu_dataset_id",
    "document_id",
    "title",
    "short_name",
    "issuing_authority",
    "jurisdiction",
    "source_url",
    "publication_date",
    "effective_date",
    "retrieval_date",
    "version",
    "status",
    "sha256_hash",
    "sections"
  ],
  "properties": {
    "mdu_dataset_id": {
      "type": "string",
      "pattern": "^BHIV-DS-LEGAL-[A-Z0-9-]+-[0-9]{3}$",
      "description": "MDU canonical dataset identifier (e.g., BHIV-DS-LEGAL-DPDP-ACT-2023-001)"
    },
    "document_id": {
      "type": "string",
      "pattern": "^doc-in-[a-z0-9-]+$",
      "description": "CLO internal reference handle (e.g. doc-in-dpdp-act-2023)"
    },
    "title": { "type": "string" },
    "short_name": { "type": "string" },
    "issuing_authority": { "type": "string" },
    "jurisdiction": { "type": "string" },
    "source_url": { "type": "string", "format": "uri" },
    "publication_date": { "type": "string", "format": "date" },
    "effective_date": { "type": "string", "format": "date" },
    "retrieval_date": { "type": "string", "format": "date" },
    "version": { "type": "string" },
    "status": {
      "type": "string",
      "enum": ["CURRENT", "AMENDED", "SUPERSEDED", "REPEALED", "TRANSITIONAL", "UNKNOWN"]
    },
    "sha256_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
    "relations": {
      "type": "array",
      "items": { "$ref": "#/$defs/LegalRelation" },
      "description": "Domain-internal statutory relationships (kept in payload, not top-level MDU relationships)"
    },
    "sections": {
      "type": "array",
      "items": { "$ref": "#/$defs/LegalPassage" }
    }
  },
  "$defs": {
    "LegalRelation": {
      "type": "object",
      "required": ["relation_type", "target_dataset_id", "effective_date", "description"],
      "properties": {
        "relation_type": {
          "type": "string",
          "enum": ["AMENDS", "AMENDED_BY", "REPLACES", "SUPERSEDED_BY", "REFERENCES", "REPEALED_BY", "TRANSITIONAL_TO"]
        },
        "target_dataset_id": { "type": "string" },
        "target_section": { "type": "string" },
        "effective_date": { "type": "string", "format": "date" },
        "description": { "type": "string" }
      }
    },
    "LegalPassage": {
      "type": "object",
      "required": ["section_id", "section_number", "heading", "text", "effective_date"],
      "properties": {
        "section_id": { "type": "string" },
        "section_number": { "type": "string" },
        "heading": { "type": "string" },
        "text": { "type": "string" },
        "keywords": { "type": "array", "items": { "type": "string" } },
        "effective_date": { "type": "string", "format": "date" },
        "amendment_history": { "type": "string" }
      }
    }
  }
}
```

### 3.3 MDU Provenance Event Format
Aligned directly with MDU's live event model:
```json
{
  "dataset_id": "BHIV-DS-LEGAL-DPDP-ACT-2023-001",
  "event_type": "ORIGIN",
  "recorded_by": "CLO_BUILD_OWNER_ANSH",
  "transformation_reference": {
    "evidence_hash": "sha256:442d1a1bd144c84a55bbdffc1f94790bc994b9da3051b498eedacd0fda154599",
    "document_id": "doc-in-dpdp-act-2023",
    "source_url": "https://egazette.gov.in/WriteReadData/2023/248045.pdf",
    "publication_date": "2023-08-11",
    "effective_date": "2023-08-11",
    "version": "1.0.0"
  }
}
```
*(Server assigns `id` and `recorded_at` upon write).*

---

## 4. Canonical Dataset Manifest for Registration

Upon formal supervisor approval, the following 8 canonical datasets will be registered under the official MDU naming scheme:

| # | Canonical MDU Dataset ID | Document Title & Reference | Status | Primary Authority |
| :---: | :--- | :--- | :---: | :--- |
| 1 | `BHIV-DS-LEGAL-DPDP-ACT-2023-001` | Digital Personal Data Protection Act, 2023 (Act 22 of 2023) | `CURRENT` | Ministry of Law and Justice / MeitY |
| 2 | `BHIV-DS-LEGAL-IT-ACT-2000-001` | Information Technology Act, 2000 (Act 21 of 2000) | `AMENDED` | Ministry of Law and Justice / MeitY |
| 3 | `BHIV-DS-LEGAL-IT-AMENDMENT-ACT-2008-001` | Information Technology (Amendment) Act, 2008 (Act 10 of 2009) | `CURRENT` | Ministry of Law and Justice |
| 4 | `BHIV-DS-LEGAL-IT-RULES-2021-001` | IT (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021 | `CURRENT` | Ministry of Electronics and IT (MeitY) |
| 5 | `BHIV-DS-LEGAL-IT-INTERMEDIARY-RULES-2011-001` | IT (Intermediaries guidelines) Rules, 2011 | `SUPERSEDED` | Ministry of Communications and IT |
| 6 | `BHIV-DS-LEGAL-SPDI-RULES-2011-001` | IT (Reasonable Security Practices and SPDI) Rules, 2011 | `CURRENT` | Ministry of Communications and IT |
| 7 | `BHIV-DS-LEGAL-COMPANIES-ACT-2013-001` | Companies Act, 2013 (Act 18 of 2013 — Sec 134, 166, 177) | `CURRENT` | Ministry of Corporate Affairs (MCA) |
| 8 | `BHIV-DS-LEGAL-CONTRACT-ACT-1872-001` | Indian Contract Act, 1872 (Act 9 of 1872 — Sec 10, 23, 73) | `CURRENT` | Legislative Department, Ministry of Law |

---

## 5. Supervisor Decisions Requested

We request Nupur's guidance and formal decisions on:
1. **Approval of MDU Dataset Naming**: Formal acceptance of `BHIV-DS-LEGAL-{NAME}-{NUMBER}` for the 8 statutory datasets.
2. **Domain Category Registration**: Formal inclusion of `LEGAL` in the MDU domain registry with Ansh designated as domain owner.
3. **Relationship Vocabulary Extension**: Supervisor determination whether MDU will formally adopt legal relationship vocabulary (`AMENDS`, `REPLACES`, `SUPERSEDED_BY`) in MDU v2, or permanently maintain them encapsulated in payload attributes.
4. **Controlled First Registration**: Written authorization to register a single pilot dataset (`BHIV-DS-LEGAL-DPDP-ACT-2023-001`) on the live MDU VM (`https://parakosha.blackholeinfiverse.com`).

Zero commits or live writes have been made or will be made to MDU master datasets without this written authorization.
