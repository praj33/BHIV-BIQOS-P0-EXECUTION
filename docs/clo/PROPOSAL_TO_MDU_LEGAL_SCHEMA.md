# Formal Proposal to MDU Authority — Legal Domain Canonical Schema & Provenance Architecture

**TO:** Nupur (MDU Authority & Programme Supervisor)  
**FROM:** Ansh (CLO Build Owner)  
**DATE:** 2026-11-06  
**STATUS:** PENDING FORMAL REVIEW (Submitted in compliance with Rule 3 — No Silent Canon Creation)  
**SUBJECT:** Canonical Schema Proposal for Legal Domain Knowledge Objects & MDU Event Integration  

---

## 1. Governance Context & Purpose

Under **Constitutional Authority Boundaries (Rule 3)**:
> *"MDU = schema, memory, ontology, lineage, provenance authority. CLO (Ansh) = legal-domain capability only. No silent canon creation. No silent schema or semantic changes. Any proposed change to a canonical schema goes to Nupur/MDU as a written proposal, not a commit."*

This document serves as the official written proposal to establish the **Legal Domain (`dom-legal`)** canonical data structures and to align the CLO Agent increment with MDU's chronological append-only event stream architecture.

---

## 2. Alignment with MDU Architecture & Resolution of Gap BLK-06

In the Stage A Ground-Truth Audit (`STAGE_A_GROUND_TRUTH_AUDIT.md`), gap **BLK-06** highlighted an architectural divergence:
- Legacy MASTERDB components expect a single `knowledge_object_id` and `lineage_reference` pointer.
- MDU implements a chronological, append-only event array containing `event_id`, `dataset_id`, `event_type` (`ORIGIN`, `INGESTION`, `VALIDATION`, `RETRIEVAL`), and evidence hashes.

**CLO Architectural Stance:**  
The CLO Agent product **explicitly adopts MDU's append-only event stream model**. It rejects synthetic single-pointer workarounds. Every legal document ingestion and reasoning retrieval operation emits an immutable, hash-linked `MduProvenanceEvent`.

---

## 3. Proposed Canonical Schemas

### 3.1 Domain Identifier Registration
- **Domain ID**: `dom-legal-regulatory-in`
- **Class**: Public Regulatory & Statutory Corpus
- **Jurisdiction**: India (Federal & Intermediary Law)

### 3.2 Canonical Document Schema (`LegalDocument`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "LegalDocument",
  "type": "object",
  "required": [
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
    "mdu_dataset_id",
    "sha256_hash",
    "sections"
  ],
  "properties": {
    "document_id": { "type": "string", "pattern": "^doc-[a-z0-9-]+$" },
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
    "mdu_dataset_id": { "type": "string", "pattern": "^ds-legal-[a-z0-9-]+$" },
    "sha256_hash": { "type": "string", "pattern": "^[a-f0-9]{64}$" },
    "relations": {
      "type": "array",
      "items": { "$ref": "#/$defs/LegalRelation" }
    },
    "sections": {
      "type": "array",
      "items": { "$ref": "#/$defs/LegalPassage" }
    }
  },
  "$defs": {
    "LegalRelation": {
      "type": "object",
      "required": ["relation_type", "target_document_id", "effective_date", "description"],
      "properties": {
        "relation_type": {
          "type": "string",
          "enum": ["AMENDS", "AMENDED_BY", "REPLACES", "SUPERSEDED_BY", "REFERENCES", "REPEALED_BY", "TRANSITIONAL_TO"]
        },
        "target_document_id": { "type": "string" },
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

### 3.3 MDU Provenance Event Schema (`MduProvenanceEvent`)
```json
{
  "event_id": "mdu-ev-7f8a9b1c2d3e",
  "dataset_id": "ds-legal-dpdp-act-2023",
  "event_type": "ORIGIN",
  "timestamp": "2026-11-06T10:15:30Z",
  "actor": "CLO_BUILD_OWNER_ANSH",
  "evidence_hash": "sha256:7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
  "details": {
    "document_id": "doc-in-dpdp-act-2023",
    "source_url": "https://egazette.gov.in/WriteReadData/2023/248045.pdf",
    "publication_date": "2023-08-11",
    "version": "1.0.0"
  }
}
```

---

## 4. Initial Ingested Corpus Alignment Request

We request MDU registration for the following 8 canonical datasets:
1. `ds-legal-dpdp-act-2023`: The Digital Personal Data Protection Act, 2023.
2. `ds-legal-it-act-2000`: The Information Technology Act, 2000.
3. `ds-legal-it-amend-2008`: The Information Technology (Amendment) Act, 2008.
4. `ds-legal-it-rules-2021`: IT (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021.
5. `ds-legal-it-rules-2011`: IT (Intermediaries guidelines) Rules, 2011 (Superseded).
6. `ds-legal-spdi-rules-2011`: IT (SPDI) Rules, 2011.
7. `ds-legal-companies-act-2013`: The Companies Act, 2013 (Fiduciary Duties & Governance).
8. `ds-legal-contract-act-1872`: The Indian Contract Act, 1872 (Electronic Formation & Legality).

---

## 5. Next Steps for MDU Review
1. Nupur to review and approve schema syntax and event model alignment.
2. Once approved, Harsha/MDU to assign canonical schema registry hashes in MASTERDB/MDU.
3. Zero commits have been or will be made to canonical MDU master repositories without this formal sign-off.

