# CLO Agent Increment — API & Schema Documentation

**Product:** CLO (Chief Legal Officer) Agent  
**Build Owner:** Ansh  
**Runtime:** FastAPI (`app`) / Uvicorn  
**Default Port:** 8085 (configurable)  
**Version:** 1.0.0-p0  

---

## 1. Architectural Design

The CLO Agent exposes an evidence-first REST API designed for executive governance and distributed reasoning workflows.
All endpoints preserve:
- Verbatim statutory source passages (from official Gazettes).
- Distributed `trace_id` continuity across services.
- Temporal `as_of_date` legal validity evaluations.
- VAJRA 8-state deterministic authority lifecycle checks.
- Append-only MDU provenance event logging.

---

## 2. API Endpoints

### 2.1 `GET /health`
System diagnostic and subsystem integration status probe.

**Response (200 OK):**
```json
{
  "service": "bhiv-clo-agent-runtime",
  "version": "1.0.0-p0",
  "status": "healthy",
  "timestamp": "2026-11-06T10:20:00Z",
  "canonical_registry": {
    "document_count": 8,
    "jurisdiction": "India",
    "statutes": [
      "doc-in-dpdp-act-2023",
      "doc-in-it-act-2000",
      "doc-in-it-amendment-act-2008",
      "doc-in-it-rules-2021",
      "doc-in-it-intermediary-rules-2011",
      "doc-in-spdi-rules-2011",
      "doc-in-companies-act-2013",
      "doc-in-contract-act-1872"
    ]
  },
  "adapters": {
    "mdu_lineage": "ACTIVE_APPEND_ONLY",
    "tantra_execution": "READY_PARTICIPANT",
    "vajra_trust": "ENFORCING_8_STATE_LIFECYCLE",
    "insightflow": "PASSIVE_EMITTER_ACTIVE"
  },
  "governance": {
    "rule_5_evidence_guard": "ENFORCED",
    "rule_8_bounded_agent": "ENFORCED",
    "silent_canon_creation": "FORBIDDEN"
  }
}
```

---

### 2.2 `POST /api/v1/clo/research`
Core legal research endpoint performing evidence-first retrieval over canonical statutes.

**Request Body (`LegalQueryRequest`):**
```json
{
  "query": "What are reasonable security safeguards to prevent personal data breach?",
  "as_of_date": "2024-01-15",
  "jurisdiction": "India",
  "caller_identity": "ansh_clo_build_owner",
  "auth_token": "ANSH_CLO_GOVERNED_SESSION",
  "trace_id": "trace-uuid-1234"
}
```

**Response (200 OK — `LegalReasoningResponse`):**
```json
{
  "trace_id": "trace-uuid-1234",
  "query": "What are reasonable security safeguards to prevent personal data breach?",
  "as_of_date_applied": "2024-01-15",
  "conclusion": "Ground-truth statutory analysis as of 2024-01-15: Grounded directly in...",
  "evidence_status": "EVIDENCE_VERIFIED",
  "evidence_passages": [
    {
      "document_id": "doc-in-dpdp-act-2023",
      "document_title": "The Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023)",
      "section_number": "Section 8",
      "heading": "General obligations of Data Fiduciary",
      "verbatim_passage": "A Data Fiduciary shall protect personal data in its possession...",
      "version": "1.0.0",
      "version_status_as_of_date": "CURRENT",
      "source_url": "https://egazette.gov.in/WriteReadData/2023/248045.pdf",
      "effective_date": "2023-08-11"
    }
  ],
  "source_version_status": {
    "doc-in-dpdp-act-2023": "CURRENT: Valid status on 2024-01-15."
  },
  "conflicts_identified": [],
  "limitations": [
    "Statutory analysis strictly evaluated as of temporal date: 2024-01-15.",
    "Source passages quoted verbatim from official Gazette notifications and IndiaCode canonical repositories.",
    "This automated synthesis constitutes legal information and reasoning support under BIQOS; it does not replace formal counsel sign-off.",
    "Judicial interpretations and High Court / Supreme Court stays are subject to external case-law verification."
  ],
  "human_review_required": true,
  "review_reasons": ["ROUTINE_AUDIT: Standard CLO governance review for executive consumption."],
  "mdu_provenance_event_ids": ["mdu-ev-8f9a12c3"],
  "tantra_execution_id": null,
  "vajra_trust_status": "VERIFIED: USE"
}
```

**Error Responses:**
- `403 Forbidden`: If caller is not registered in VAJRA authority catalog, or in `REVOKE` / `SUSPEND` state.
- `401 Unauthorized`: If invalid token provided.

---

### 2.3 `POST /api/v1/clo/analyse`
Performs comprehensive compliance analysis with corporate liability and governance review triggers.

---

### 2.4 `GET /api/v1/clo/documents` & `GET /api/v1/clo/documents/{document_id}`
Retrieves manifest of canonical documents and individual statutory sections.

---

### 2.5 `GET /api/v1/clo/mdu-lineage`
Retrieves chronological append-only MDU provenance event stream (`ORIGIN`, `INGESTION`, `VALIDATION`, `RETRIEVAL`).

---

### 2.6 `POST /api/v1/clo/tantra/workload`
Execution participant interface complying with `services/execution/EXECUTION_CONTRACT.md`.

**Request:**
```json
{
  "workload": "{\"query\": \"...\"}",
  "trace_id": "uuid",
  "execution_id": "uuid",
  "bridge_signature": "Bearer VERIFIED_TANTRA_BRIDGE_TOKEN"
}
```

**Response (200 OK):**
```json
{
  "trace_id": "uuid",
  "execution_id": "uuid",
  "status": "completed",
  "result": {
    "execution_hash": "<sha256>",
    "legal_reasoning": { ... }
  },
  "artifact_location": "artifacts/<trace_id>/<execution_id>",
  "duration_ms": 12
}
```

