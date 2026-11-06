# MDU Review of the CLO Legal Schema Proposal

Reviewer: Nupur Gavane (MDU)
Date: 2026-11-06
Document reviewed: docs/clo/PROPOSAL_TO_MDU_LEGAL_SCHEMA.md (submitted by Ansh, 2026-11-06), with docs/clo/DAY_BY_DAY_EXECUTION_REPORT.md
Status of this review: DRAFT recommendation. Nothing is approved. Nothing is registered in MDU. Any canonical change needs the supervisor's approval.

## 1. Summary

The proposal follows the governance rule (a written proposal, no silent canon). Its direction is sound: it reuses MDU's append-only provenance model instead of building a parallel store. Several parts do not match what MDU actually accepts today, and one part (the relationship vocabulary) is a canonical decision that is not MDU's to make alone. The recommendation is CONDITIONAL: revise and resubmit the items in Section 3, and do not register any dataset until the supervisor approves.

## 2. What matches MDU

| Proposal item | MDU position |
|---|---|
| Append-only event stream per dataset | Matches. MDU provenance records are written once; no update or delete is declared for provenance. |
| First event is ORIGIN | Matches the documented rule that the first provenance event is ORIGIN. |
| Source URL, dates, version carried with the dataset | Can be carried. Fields exist for source and version; the exact placement still has to be confirmed against the live contract. |
| No commit to canonical repositories without sign-off | Matches. |

## 3. What does not match, or needs a decision

1. Dataset identifier format. The proposal uses ds-legal-dpdp-act-2023 and a pattern ^ds-legal-[a-z0-9-]+$. MDU's canonical identifier is BHIV-DS-{DOMAIN}-{NAME}-{NUMBER}, for example BHIV-DS-MARITIME-AIS-LIVE-001, and the API stores it upper-cased. A lowercase ds- identifier would be rejected or would create a second identifier format. The supervisor's direction of 2026-11-05 says not to introduce new identifier formats silently. Required: use the MDU form, for example BHIV-DS-LEGAL-DPDP-ACT-2023-001, and keep any other identifier as a separate reference field.
2. Event types. The proposal lists ORIGIN, INGESTION, VALIDATION and RETRIEVAL. The MDU write validator accepts ORIGIN, INGESTION, TRANSFORMATION, VALIDATION, TRUST_CHANGE and SCHEMA_CHANGE. RETRIEVAL is not accepted. Reads are also not provenance events in MDU. Required: either drop RETRIEVAL, or propose it as a vocabulary change for the supervisor to decide (Finding 1 in the MDU schema drift report is an open supervisor decision).
3. Event fields. The proposal's MduProvenanceEvent has event_id, timestamp, actor and evidence_hash. In MDU the id and recorded_at are set by the server, so a client-supplied event_id or timestamp cannot be stored as written. The actor maps to recorded_by. MDU has no evidence-hash field; the hash can travel inside transformation_reference (a JSON object whose structure MDU does not define). Required: restate the event in MDU's real fields, and say where the SHA-256 hash is carried.
4. The statement in Section 2 of the proposal that MDU "implements ... evidence hashes" is not accurate. MDU has no integrity-hash field today. Required: correct the statement. Whether MDU should gain one is a separate proposal.
5. Relationship types. The proposal defines AMENDS, AMENDED_BY, REPLACES, SUPERSEDED_BY, REFERENCES, REPEALED_BY and TRANSITIONAL_TO. In MDU, relationship_type is a free string up to 50 characters, not a database enumeration. The values offered are DERIVED_FROM, DEPENDS_ON, MERGED_FROM and FILTERED_FROM; only DERIVED_FROM and DEPENDS_ON are in use. So the new values would be technically storable, but they would add new canonical vocabulary. That decision belongs to the supervisor (open Finding 2). Required: submit the vocabulary as an explicit proposal for approval. Until then keep these relations inside the CLO document payload and do not write them as MDU relationships.
6. Domain registration. The proposal registers a domain dom-legal-regulatory-in. MDU's dataset has a domain_primary field and no separate domain registry. The MDU 14-category coverage matrix defines no legal category. Required: say whether this is a value for domain_primary or a request for a new MDU category. If a category, it goes to the supervisor with the domain owner (Ansh) named.
7. Hash assignment. Section 5 says Harsha/MDU will assign canonical schema registry hashes in MASTERDB/MDU. MDU does not assign schema hashes, and the MASTERDB hash (knowledge_hash) belongs to MASTERDB. Required: remove or name the actual owner.
8. Legal content. This review does not check legal accuracy, effective dates, amendment relationships or the gazette URLs. Some Acts commence in stages, so effective_date may differ by provision. The domain owner must verify the content.

## 4. Report consistency questions for Ansh

- Test counts and commits differ between his messages and the report: 22 of 22 tests and merge commit a5b648a (message), 20 of 20 tests and head commit 1df15a9 (report), and 0451ee7 on feat/clo-agent-increment (earlier message). One commit and one count must be named in the evidence.
- The report links point to local file paths on a laptop. The evidence must use repository URLs.
- The report lists a live MDU timeout (BLK-02). MDU moved to the VM on 2026-10-31; the Render address no longer works. Which URL was used? The current address is https://parakosha.blackholeinfiverse.com.
- The independent SARATHI validation is reported as VERIFIED_ACCEPTED by a script in Ansh's own repository. Confirm that Hemanth ran it himself.

## 5. Recommendation and next steps

1. Return the proposal to Ansh with Section 3 items 1 to 7 as required revisions.
2. Do not register any of the 8 datasets in MDU today. A live write needs the supervisor's explicit approval and the write-permission workflow does not exist yet. If the supervisor approves, start with one dataset under a test identifier.
3. Raise two decisions with the supervisor: the event and relationship vocabularies, and whether a legal domain category is created.
4. Record the amendment/replacement pair in the CLO payload for today, and describe the MDU mapping as proposed, not live.
