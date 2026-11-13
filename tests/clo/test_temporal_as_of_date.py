"""
Scenario 3: Temporal As-of-Date Resolution (Verified Amendment / Supersession Pair)
Tests that historical queries correctly resolve active law on past dates,
identifying whether IT Intermediary Rules 2011 was active law (prior to Feb 25, 2021)
or superseded (after Feb 25, 2021).
"""

from fastapi.testclient import TestClient
from clo.registry.registry import CanonicalLegalRegistry
from clo.schemas.models import DocumentStatus


def test_registry_as_of_date_supersession_logic(canonical_registry: CanonicalLegalRegistry):
    """Directly verifies registry temporal evaluation on past vs current dates."""
    # Historical date: 2018-05-01 (Before IT Rules 2021 was enacted)
    status_2018, reason_2018 = canonical_registry.get_document_status_as_of(
        "doc-in-it-intermediary-rules-2011", "2018-05-01"
    )
    assert status_2018 == DocumentStatus.CURRENT
    assert "active law on 2018-05-01 prior to supersession" in reason_2018

    # Status of 2021 rules on 2018-05-01
    status_21_in_18, reason_21_in_18 = canonical_registry.get_document_status_as_of(
        "doc-in-it-rules-2021", "2018-05-01"
    )
    assert status_21_in_18 == DocumentStatus.UNKNOWN
    assert "Not yet in force" in reason_21_in_18

    # Present date: 2024-01-01 (After IT Rules 2021 superseded 2011 rules)
    status_2024, reason_2024 = canonical_registry.get_document_status_as_of(
        "doc-in-it-intermediary-rules-2011", "2024-01-01"
    )
    assert status_2024 == DocumentStatus.SUPERSEDED
    assert "Superseded on 2021-02-25" in reason_2024 or "Replaced on 2021-02-25" in reason_2024

    # Status of 2021 rules on 2024-01-01
    status_21_in_24, reason_21_in_24 = canonical_registry.get_document_status_as_of(
        "doc-in-it-rules-2021", "2024-01-01"
    )
    assert status_21_in_24 == DocumentStatus.CURRENT


def test_api_as_of_date_intermediary_timeline(client: TestClient):
    """
    Tests end-to-end API evaluation with temporal parameters:
    1. Query in 2018 resolves 1-month grievance timeline as current law.
    2. Query in 2024 surfaces 15-day timeline and marks 2011 rules as superseded.
    """
    # Query A: As of 2018-01-01
    req_2018 = {
        "query": "What is the timeline for the Grievance Officer to redress complaints under intermediary rules?",
        "as_of_date": "2018-01-01",
        "caller_identity": "ansh_clo_build_owner",
        "trace_id": "trace-temporal-2018"
    }
    res_2018 = client.post("/api/v1/clo/research", json=req_2018)
    assert res_2018.status_code == 200
    data_2018 = res_2018.json()
    assert data_2018["as_of_date_applied"] == "2018-01-01"

    # In 2018, only 2011 rules were active; 2021 rules were not yet in force
    passages_2018 = data_2018["evidence_passages"]
    p_11_list = [p for p in passages_2018 if p["document_id"] == "doc-in-it-intermediary-rules-2011"]
    assert len(p_11_list) >= 1
    assert p_11_list[0]["version_status_as_of_date"] == "CURRENT"

    # Query B: As of 2024-01-01
    req_2024 = {
        "query": "What is the timeline for the Grievance Officer to redress complaints under intermediary rules?",
        "as_of_date": "2024-01-01",
        "caller_identity": "ansh_clo_build_owner",
        "trace_id": "trace-temporal-2024"
    }
    res_2024 = client.post("/api/v1/clo/research", json=req_2024)
    assert res_2024.status_code == 200
    data_2024 = res_2024.json()
    assert data_2024["as_of_date_applied"] == "2024-01-01"

    # In 2024, 2021 rules are CURRENT and 2011 rules are SUPERSEDED
    passages_2024 = data_2024["evidence_passages"]
    p_21_list = [p for p in passages_2024 if p["document_id"] == "doc-in-it-rules-2021"]
    assert len(p_21_list) >= 1
    assert p_21_list[0]["version_status_as_of_date"] == "CURRENT"

    # Explicit conflict/supersession notice surfaced
    assert len(data_2024["conflicts_identified"]) >= 1
    assert "supersession" in data_2024["conflicts_identified"][0].lower()


def test_dpdp_section_8_and_it_section_43a_as_of_2024_01_15(client: TestClient, canonical_registry: CanonicalLegalRegistry):
    """
    Regression Test 1 (G.S.R. 843(E) dated 13 Nov 2025):
    As of 2024-01-15:
    - DPDP Act Section 8 is NOT yet in force (PENDING_COMMENCEMENT until 2027-05-13).
    - Section 43A of IT Act 2000 remains in force and applicable (CURRENT).
    - tantra_execution_id is populated in the API response.
    """
    dpdp_doc = canonical_registry.get_document("doc-in-dpdp-act-2023")
    sec_8 = next(s for s in dpdp_doc.sections if s.section_number == "Section 8")
    status_sec8, reason_sec8 = canonical_registry.get_passage_status_as_of(dpdp_doc, sec_8, "2024-01-15")
    assert status_sec8 == DocumentStatus.PENDING_COMMENCEMENT
    assert "not in force as of 2024-01-15" in reason_sec8
    assert "2027-05-13" in reason_sec8

    it_doc = canonical_registry.get_document("doc-in-it-amendment-act-2008")
    sec_43a = next(s for s in it_doc.sections if s.section_number == "Section 43A")
    status_43a, reason_43a = canonical_registry.get_passage_status_as_of(it_doc, sec_43a, "2024-01-15")
    assert status_43a == DocumentStatus.CURRENT
    assert "In force and applicable" in reason_43a

    # Test via API
    req = {
        "query": "What are reasonable security safeguards to prevent personal data breach and compensation for failure to protect data?",
        "as_of_date": "2024-01-15",
        "caller_identity": "ansh_clo_build_owner",
        "trace_id": "trace-temporal-dpdp-2024"
    }
    res = client.post("/api/v1/clo/research", json=req)
    assert res.status_code == 200
    data = res.json()
    assert data["as_of_date_applied"] == "2024-01-15"
    assert data["tantra_execution_id"] is not None and len(data["tantra_execution_id"]) > 0

    p_dpdp = [p for p in data["evidence_passages"] if p["document_id"] == "doc-in-dpdp-act-2023" and p["section_number"] == "Section 8"]
    assert len(p_dpdp) >= 1
    assert p_dpdp[0]["version_status_as_of_date"] == "PENDING_COMMENCEMENT"

    p_43a = [p for p in data["evidence_passages"] if p["document_id"] == "doc-in-it-amendment-act-2008" and p["section_number"] == "Section 43A"]
    assert len(p_43a) >= 1
    assert p_43a[0]["version_status_as_of_date"] == "CURRENT"

    # Verify transition conflict message confirms Section 43A is active governing law
    assert any("Section 43A of IT Act 2000 remains active" in c for c in data["conflicts_identified"])


def test_dpdp_section_8_and_it_section_43a_as_of_2026_11_07(client: TestClient, canonical_registry: CanonicalLegalRegistry):
    """
    Regression Test 2 (G.S.R. 843(E) dated 13 Nov 2025):
    As of 2026-11-07:
    - Same commencement position: DPDP Section 8 remains PENDING_COMMENCEMENT.
    - Section 43A of IT Act 2000 remains CURRENT and applicable.
    """
    dpdp_doc = canonical_registry.get_document("doc-in-dpdp-act-2023")
    sec_8 = next(s for s in dpdp_doc.sections if s.section_number == "Section 8")
    status_sec8, reason_sec8 = canonical_registry.get_passage_status_as_of(dpdp_doc, sec_8, "2026-11-07")
    assert status_sec8 == DocumentStatus.PENDING_COMMENCEMENT
    assert "2027-05-13" in reason_sec8

    it_doc = canonical_registry.get_document("doc-in-it-amendment-act-2008")
    sec_43a = next(s for s in it_doc.sections if s.section_number == "Section 43A")
    status_43a, reason_43a = canonical_registry.get_passage_status_as_of(it_doc, sec_43a, "2026-11-07")
    assert status_43a == DocumentStatus.CURRENT

    req = {
        "query": "What are reasonable security safeguards to prevent personal data breach and compensation for failure to protect data?",
        "as_of_date": "2026-11-07",
        "caller_identity": "ansh_clo_build_owner",
        "trace_id": "trace-temporal-dpdp-2026"
    }
    res = client.post("/api/v1/clo/research", json=req)
    assert res.status_code == 200
    data = res.json()
    assert data["as_of_date_applied"] == "2026-11-07"
    assert data["tantra_execution_id"] is not None and len(data["tantra_execution_id"]) > 0

    p_dpdp = [p for p in data["evidence_passages"] if p["document_id"] == "doc-in-dpdp-act-2023" and p["section_number"] == "Section 8"]
    assert len(p_dpdp) >= 1
    assert p_dpdp[0]["version_status_as_of_date"] == "PENDING_COMMENCEMENT"

    p_43a = [p for p in data["evidence_passages"] if p["document_id"] == "doc-in-it-amendment-act-2008" and p["section_number"] == "Section 43A"]
    assert len(p_43a) >= 1
    assert p_43a[0]["version_status_as_of_date"] == "CURRENT"


def test_dpdp_section_8_and_it_section_43a_from_2027_05_13(client: TestClient, canonical_registry: CanonicalLegalRegistry):
    """
    Regression Test 3 (G.S.R. 843(E) dated 13 Nov 2025):
    From 2027-05-13 (scheduled commencement):
    - DPDP Section 8 comes into force and becomes CURRENT.
    - Section 43A of IT Act 2000 becomes SUPERSEDED / OMITTED by Section 44(2) of DPDP Act 2023.
    """
    dpdp_doc = canonical_registry.get_document("doc-in-dpdp-act-2023")
    sec_8 = next(s for s in dpdp_doc.sections if s.section_number == "Section 8")
    status_sec8, reason_sec8 = canonical_registry.get_passage_status_as_of(dpdp_doc, sec_8, "2027-05-13")
    assert status_sec8 == DocumentStatus.CURRENT
    assert "In force and applicable" in reason_sec8

    it_doc = canonical_registry.get_document("doc-in-it-amendment-act-2008")
    sec_43a = next(s for s in it_doc.sections if s.section_number == "Section 43A")
    status_43a, reason_43a = canonical_registry.get_passage_status_as_of(it_doc, sec_43a, "2027-05-13")
    assert status_43a == DocumentStatus.SUPERSEDED
    assert "omitted / amended w.e.f. 2027-05-13" in reason_43a

    # Test via API
    req = {
        "query": "What are reasonable security safeguards to prevent personal data breach and compensation for failure to protect data?",
        "as_of_date": "2027-05-13",
        "caller_identity": "ansh_clo_build_owner",
        "trace_id": "trace-temporal-dpdp-2027"
    }
    res = client.post("/api/v1/clo/research", json=req)
    assert res.status_code == 200
    data = res.json()
    assert data["as_of_date_applied"] == "2027-05-13"
    assert data["tantra_execution_id"] is not None and len(data["tantra_execution_id"]) > 0

    p_dpdp = [p for p in data["evidence_passages"] if p["document_id"] == "doc-in-dpdp-act-2023" and p["section_number"] == "Section 8"]
    assert len(p_dpdp) >= 1
    assert p_dpdp[0]["version_status_as_of_date"] == "CURRENT"

    p_43a = [p for p in data["evidence_passages"] if p["document_id"] == "doc-in-it-amendment-act-2008" and p["section_number"] == "Section 43A"]
    assert len(p_43a) >= 1
    assert p_43a[0]["version_status_as_of_date"] == "SUPERSEDED"

    assert any("DPDP Act Section 8 is the active governing law" in c for c in data["conflicts_identified"])


def test_dpdp_section_6_9_and_section_27_1_d_commencement_boundary_2026_11_13(client: TestClient, canonical_registry: CanonicalLegalRegistry):
    """
    Regression Test 4 (G.S.R. 843(E) dated 13 Nov 2025 - 12-Month Staged Commencement Boundary):
    On the exact 13 November 2026 boundary:
    1. Prior to 13 Nov 2026 (as of 2026-11-07 / 2026-11-12):
       - DPDP Section 6(9) (Consent Manager registration) is PENDING_COMMENCEMENT.
       - DPDP Section 27(1)(d) (Board inquiry into Consent Manager breach) is PENDING_COMMENCEMENT.
       - DPDP Section 8 remains PENDING_COMMENCEMENT (18-month staged commencement).
       - IT Act Section 43A remains CURRENT.
    2. On 13 Nov 2026 (2026-11-13):
       - DPDP Section 6(9) becomes CURRENT (in force).
       - DPDP Section 27(1)(d) becomes CURRENT (in force).
       - DPDP Section 8 remains PENDING_COMMENCEMENT (scheduled for 2027-05-13).
       - IT Act Section 43A remains CURRENT (omission scheduled for 2027-05-13).
    """
    dpdp_doc = canonical_registry.get_document("doc-in-dpdp-act-2023")
    sec_6_9 = next(s for s in dpdp_doc.sections if s.section_number == "Section 6(9)")
    sec_27_1_d = next(s for s in dpdp_doc.sections if s.section_number == "Section 27(1)(d)")
    sec_8 = next(s for s in dpdp_doc.sections if s.section_number == "Section 8")

    it_doc = canonical_registry.get_document("doc-in-it-amendment-act-2008")
    sec_43a = next(s for s in it_doc.sections if s.section_number == "Section 43A")

    # --- Phase A: Prior to 13 November 2026 (e.g. 2026-11-07) ---
    status_69_pre, _ = canonical_registry.get_passage_status_as_of(dpdp_doc, sec_6_9, "2026-11-07")
    status_27d_pre, _ = canonical_registry.get_passage_status_as_of(dpdp_doc, sec_27_1_d, "2026-11-07")
    status_8_pre, _ = canonical_registry.get_passage_status_as_of(dpdp_doc, sec_8, "2026-11-07")
    status_43a_pre, _ = canonical_registry.get_passage_status_as_of(it_doc, sec_43a, "2026-11-07")

    assert status_69_pre == DocumentStatus.PENDING_COMMENCEMENT
    assert status_27d_pre == DocumentStatus.PENDING_COMMENCEMENT
    assert status_8_pre == DocumentStatus.PENDING_COMMENCEMENT
    assert status_43a_pre == DocumentStatus.CURRENT

    # --- Phase B: On exact commencement date 13 November 2026 (2026-11-13) ---
    status_69_on, reason_69 = canonical_registry.get_passage_status_as_of(dpdp_doc, sec_6_9, "2026-11-13")
    status_27d_on, reason_27d = canonical_registry.get_passage_status_as_of(dpdp_doc, sec_27_1_d, "2026-11-13")
    status_8_on, reason_8 = canonical_registry.get_passage_status_as_of(dpdp_doc, sec_8, "2026-11-13")
    status_43a_on, reason_43a = canonical_registry.get_passage_status_as_of(it_doc, sec_43a, "2026-11-13")

    assert status_69_on == DocumentStatus.CURRENT
    assert "In force and applicable" in reason_69
    assert status_27d_on == DocumentStatus.CURRENT
    assert "In force and applicable" in reason_27d

    # Section 8 and Section 43A maintain their staged positions until 2027-05-13
    assert status_8_on == DocumentStatus.PENDING_COMMENCEMENT
    assert "2027-05-13" in reason_8
    assert status_43a_on == DocumentStatus.CURRENT

    # --- Phase C: API Verification for Consent Manager Query on 2026-11-13 ---
    req_cm = {
        "query": "Every Consent Manager shall be registered with the Board and Board inquiry into breach of registration conditions",
        "as_of_date": "2026-11-13",
        "caller_identity": "ansh_clo_build_owner",
        "trace_id": "trace-temporal-cm-2026-11-13"
    }
    res_cm = client.post("/api/v1/clo/research", json=req_cm)
    assert res_cm.status_code == 200
    data_cm = res_cm.json()
    assert data_cm["as_of_date_applied"] == "2026-11-13"
    assert data_cm["tantra_execution_id"] is not None and len(data_cm["tantra_execution_id"]) > 0

    p_69 = [p for p in data_cm["evidence_passages"] if p["document_id"] == "doc-in-dpdp-act-2023" and p["section_number"] == "Section 6(9)"]
    assert len(p_69) >= 1
    assert p_69[0]["version_status_as_of_date"] == "CURRENT"

    p_27d = [p for p in data_cm["evidence_passages"] if p["document_id"] == "doc-in-dpdp-act-2023" and p["section_number"] == "Section 27(1)(d)"]
    assert len(p_27d) >= 1
    assert p_27d[0]["version_status_as_of_date"] == "CURRENT"



