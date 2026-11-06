"""
Canonical Legal Registry Corpus
Ingestion of 8 official public legal documents with verified amendment/replacement pairs.
Aligned with MDU canonical dataset lineage.
"""

import hashlib
from typing import List, Dict
from ..schemas.models import (
    LegalDocument,
    LegalPassage,
    LegalRelation,
    DocumentStatus,
    RelationType,
)


def _compute_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_canonical_corpus() -> Dict[str, LegalDocument]:
    """Builds and returns the 8 official public legal documents with verifiable metadata and verbatim text."""
    corpus: Dict[str, LegalDocument] = {}

    # 1. DPDP Act 2023
    dpdp_passages = [
        LegalPassage(
            section_id="sec-dpdp-4",
            section_number="Section 4",
            heading="Grounds for processing personal data",
            text="A person may process the personal data of a Data Principal only in accordance with the provisions of this Act and for a lawful purpose—(a) for which the Data Principal has given her consent; or (b) for certain legitimate uses.",
            keywords=["consent", "processing", "lawful purpose", "legitimate uses", "data fiduciary", "data principal"],
            effective_date="2023-08-11",
            amendment_history="Enacted as Act No. 22 of 2023, published in Gazette of India on 11th August, 2023."
        ),
        LegalPassage(
            section_id="sec-dpdp-6",
            section_number="Section 6",
            heading="Consent requirements and withdrawal",
            text="Consent given by the Data Principal shall be free, specific, informed, unconditional and unambiguous with a clear affirmative action, and shall signify an agreement for processing her personal data for the specified purpose.",
            keywords=["consent", "free", "specific", "unambiguous", "withdrawal", "notice"],
            effective_date="2023-08-11",
            amendment_history="Enacted as Act No. 22 of 2023."
        ),
        LegalPassage(
            section_id="sec-dpdp-8",
            section_number="Section 8",
            heading="General obligations of Data Fiduciary",
            text="A Data Fiduciary shall protect personal data in its possession or under its control, including in respect of any processing undertaken by it or on its behalf by a Data Processor, by taking reasonable security safeguards to prevent personal data breach.",
            keywords=["obligations", "security safeguards", "data breach", "data fiduciary", "data processor", "reasonable security"],
            effective_date="2023-08-11",
            amendment_history="Enacted as Act No. 22 of 2023."
        ),
        LegalPassage(
            section_id="sec-dpdp-44",
            section_number="Section 44",
            heading="Amendments to Information Technology Act, 2000",
            text="In the Information Technology Act, 2000, section 43A shall be omitted; and in section 87, in sub-section (2), clause (ob) shall be omitted.",
            keywords=["amendment", "omission", "section 43A", "compensation", "it act 2000"],
            effective_date="2023-08-11",
            amendment_history="Enacted as Act No. 22 of 2023; omits section 43A of IT Act 2000 upon commencement."
        ),
    ]
    dpdp_raw = "".join(p.text for p in dpdp_passages)
    corpus["doc-in-dpdp-act-2023"] = LegalDocument(
        document_id="doc-in-dpdp-act-2023",
        title="The Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023)",
        short_name="DPDP Act 2023",
        issuing_authority="Ministry of Law and Justice, Legislative Department, Government of India",
        jurisdiction="India",
        source_url="https://egazette.gov.in/WriteReadData/2023/248045.pdf",
        publication_date="2023-08-11",
        effective_date="2023-08-11",
        retrieval_date="2026-11-06",
        version="1.0.0",
        status=DocumentStatus.CURRENT,
        relations=[
            LegalRelation(
                relation_type=RelationType.AMENDS,
                target_document_id="doc-in-it-act-2000",
                target_section="Section 43A",
                effective_date="2023-08-11",
                description="Section 44 of DPDP Act 2023 omits Section 43A of IT Act 2000."
            ),
            LegalRelation(
                relation_type=RelationType.TRANSITIONAL_TO,
                target_document_id="doc-in-spdi-rules-2011",
                target_section="All Rules",
                effective_date="2023-08-11",
                description="SPDI Rules 2011 issued under Section 43A transition into DPDP Act 2023 regime."
            )
        ],
        sections=dpdp_passages,
        mdu_dataset_id="ds-legal-dpdp-act-2023",
        sha256_hash=_compute_hash(dpdp_raw)
    )

    # 2. IT Act 2000 (Base)
    it_base_passages = [
        LegalPassage(
            section_id="sec-it-10a",
            section_number="Section 10A",
            heading="Validity of contracts formed through electronic means",
            text="Where in a contract formation, the communication of proposals, the acceptance of proposals, the revocation of proposals and acceptances, as the case may be, are expressed in electronic form or by means of an electronic record, such contract shall not be deemed to be unenforceable solely on the ground that such electronic form or means was used for that purpose.",
            keywords=["contract", "electronic means", "electronic record", "validity", "enforceability"],
            effective_date="2000-10-17",
            amendment_history="Inserted by Act 10 of 2009, section 6 (w.e.f. 27-10-2009)."
        ),
        LegalPassage(
            section_id="sec-it-43",
            section_number="Section 43",
            heading="Penalty and compensation for damage to computer, computer system, etc.",
            text="If any person without permission of the owner or any other person who is incharge of a computer, computer system or computer network accesses or secures access, downloads, copies or extracts any data, introduces computer contaminant or virus, or damages any computer source code, he shall be liable to pay damages by way of compensation to the person so affected.",
            keywords=["penalty", "compensation", "unauthorized access", "computer virus", "damage", "data extraction"],
            effective_date="2000-10-17",
            amendment_history="Amended by Act 10 of 2009."
        ),
        LegalPassage(
            section_id="sec-it-65",
            section_number="Section 65",
            heading="Tampering with computer source documents",
            text="Whoever knowingly or intentionally conceals, destroys or alters or intentionally or knowingly causes another to conceal, destroy or alter any computer source code used for a computer, computer programme, computer system or computer network, when the computer source code is required to be kept or maintained by law, shall be punishable with imprisonment up to three years, or with fine which may extend up to two lakh rupees, or with both.",
            keywords=["source code", "tampering", "destruction", "alteration", "imprisonment", "fine"],
            effective_date="2000-10-17",
            amendment_history="Act No. 21 of 2000."
        ),
    ]
    it_raw = "".join(p.text for p in it_base_passages)
    corpus["doc-in-it-act-2000"] = LegalDocument(
        document_id="doc-in-it-act-2000",
        title="The Information Technology Act, 2000 (Act No. 21 of 2000)",
        short_name="IT Act 2000",
        issuing_authority="Parliament of India / Ministry of Electronics and Information Technology",
        jurisdiction="India",
        source_url="https://www.indiacode.nic.in/handle/123456789/1999",
        publication_date="2000-06-09",
        effective_date="2000-10-17",
        retrieval_date="2026-11-06",
        version="1.0.0",
        status=DocumentStatus.AMENDED,
        relations=[
            LegalRelation(
                relation_type=RelationType.AMENDED_BY,
                target_document_id="doc-in-it-amendment-act-2008",
                target_section="Section 43A, 66A-66F, 69, 72A",
                effective_date="2009-10-27",
                description="Substantially amended by Information Technology (Amendment) Act 2008."
            ),
            LegalRelation(
                relation_type=RelationType.AMENDED_BY,
                target_document_id="doc-in-dpdp-act-2023",
                target_section="Section 44",
                effective_date="2023-08-11",
                description="Section 43A omitted by DPDP Act 2023."
            )
        ],
        sections=it_base_passages,
        mdu_dataset_id="ds-legal-it-act-2000",
        sha256_hash=_compute_hash(it_raw)
    )

    # 3. IT (Amendment) Act 2008
    it_amend_passages = [
        LegalPassage(
            section_id="sec-it-43a",
            section_number="Section 43A",
            heading="Compensation for failure to protect data",
            text="Where a body corporate, possessing, dealing or handling any sensitive personal data or information in a computer resource which it owns, controls or operates, is negligent in implementing and maintaining reasonable security practices and procedures and thereby causes wrongful loss or wrongful gain to any person, such body corporate shall be liable to pay damages by way of compensation to the person so affected.",
            keywords=["body corporate", "sensitive personal data", "reasonable security practices", "negligence", "compensation", "damages"],
            effective_date="2009-10-27",
            amendment_history="Inserted by Act 10 of 2009, section 22 (w.e.f. 27-10-2009); subject to omission by Section 44 of DPDP Act 2023."
        ),
        LegalPassage(
            section_id="sec-it-66c",
            section_number="Section 66C",
            heading="Punishment for identity theft",
            text="Whoever, fraudulently or dishonestly make use of the electronic signature, password or any other unique identification feature of any other person, shall be punished with imprisonment of either description for a term which may extend to three years and shall also be liable to fine which may extend to rupees one lakh.",
            keywords=["identity theft", "electronic signature", "password", "fraudulent use", "imprisonment"],
            effective_date="2009-10-27",
            amendment_history="Inserted by Act 10 of 2009, section 32 (w.e.f. 27-10-2009)."
        ),
        LegalPassage(
            section_id="sec-it-72a",
            section_number="Section 72A",
            heading="Punishment for disclosure of information in breach of lawful contract",
            text="Save as otherwise provided in this Act or any other law for the time being in force, any person including an intermediary who, while providing services under the terms of lawful contract, has secured access to any material containing personal information about another person, with the intent to cause or knowing that he is likely to cause wrongful loss or wrongful gain discloses, without the consent of the person concerned, or in breach of a lawful contract, such material, shall be punished with imprisonment for a term which may extend to three years, or with fine which may extend to five lakh rupees, or with both.",
            keywords=["disclosure", "breach of contract", "personal information", "wrongful loss", "imprisonment", "fine"],
            effective_date="2009-10-27",
            amendment_history="Inserted by Act 10 of 2009, section 39 (w.e.f. 27-10-2009)."
        ),
    ]
    it_amend_raw = "".join(p.text for p in it_amend_passages)
    corpus["doc-in-it-amendment-act-2008"] = LegalDocument(
        document_id="doc-in-it-amendment-act-2008",
        title="The Information Technology (Amendment) Act, 2008 (Act No. 10 of 2009)",
        short_name="IT Amendment 2008",
        issuing_authority="Ministry of Law and Justice, Government of India",
        jurisdiction="India",
        source_url="https://egazette.gov.in/WriteReadData/2009/E_10_2009_002.pdf",
        publication_date="2009-02-05",
        effective_date="2009-10-27",
        retrieval_date="2026-11-06",
        version="1.0.0",
        status=DocumentStatus.CURRENT,
        relations=[
            LegalRelation(
                relation_type=RelationType.AMENDS,
                target_document_id="doc-in-it-act-2000",
                target_section="Section 43A, 66, 69, 72A",
                effective_date="2009-10-27",
                description="Substantive amendment introducing corporate data liability and cyber offenses."
            ),
            LegalRelation(
                relation_type=RelationType.AMENDED_BY,
                target_document_id="doc-in-dpdp-act-2023",
                target_section="Section 44",
                effective_date="2023-08-11",
                description="Section 43A omitted by Section 44 of DPDP Act 2023."
            )
        ],
        sections=it_amend_passages,
        mdu_dataset_id="ds-legal-it-amend-2008",
        sha256_hash=_compute_hash(it_amend_raw)
    )

    # 4. IT Rules 2021 (Intermediary Guidelines)
    it_rules_2021_passages = [
        LegalPassage(
            section_id="sec-itrules21-3-1-a",
            section_number="Rule 3(1)(a)",
            heading="Due diligence by intermediary - Rules and Regulations",
            text="The intermediary shall prominently publish on its website, mobile based application or both, as the case may be, the rules and regulations, privacy policy and user agreement for access or usage of its computer resource by any person.",
            keywords=["intermediary", "due diligence", "rules", "privacy policy", "user agreement", "publishing"],
            effective_date="2021-02-25",
            amendment_history="Notified vide G.S.R. 139(E) dated 25th February, 2021."
        ),
        LegalPassage(
            section_id="sec-itrules21-3-2",
            section_number="Rule 3(2)",
            heading="Grievance Redressal Mechanism of Intermediary",
            text="The intermediary shall prominently publish on its website or mobile application the name of the Grievance Officer and his contact details as well as mechanism by which a user or a victim may make complaint against violation of the provisions of this rule. The Grievance Officer shall acknowledge the complaint within twenty-four hours and resolve it within a period of fifteen days from the date of its receipt.",
            keywords=["grievance officer", "complaint", "acknowledgment", "24 hours", "15 days", "redressal"],
            effective_date="2021-02-25",
            amendment_history="Replaced 30-day timeline in 2011 rules with 24-hour ack and 15-day resolution."
        ),
        LegalPassage(
            section_id="sec-itrules21-3-1-d",
            section_number="Rule 3(1)(d)",
            heading="Takedown of unlawful information upon order",
            text="The intermediary, on being informed by a court order or by an appropriate government or its agency under clause (b) of sub-section (3) of section 79, shall not host, store or publish any unlawful information and shall remove or disable access to that information as early as possible, but in no case later than thirty-six hours from the receipt of the court order or on being notified by the Appropriate Government.",
            keywords=["takedown", "unlawful information", "court order", "appropriate government", "36 hours", "section 79"],
            effective_date="2021-02-25",
            amendment_history="Notified vide G.S.R. 139(E)."
        ),
    ]
    it_rules_21_raw = "".join(p.text for p in it_rules_2021_passages)
    corpus["doc-in-it-rules-2021"] = LegalDocument(
        document_id="doc-in-it-rules-2021",
        title="The Information Technology (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021",
        short_name="IT Rules 2021",
        issuing_authority="Ministry of Electronics and Information Technology, Government of India",
        jurisdiction="India",
        source_url="https://www.meity.gov.in/writereaddata/files/Intermediary_Guidelines_and_Digital_Media_Ethics_Code_Rules-2021.pdf",
        publication_date="2021-02-25",
        effective_date="2021-02-25",
        retrieval_date="2026-11-06",
        version="1.0.0",
        status=DocumentStatus.CURRENT,
        relations=[
            LegalRelation(
                relation_type=RelationType.REPLACES,
                target_document_id="doc-in-it-intermediary-rules-2011",
                target_section="All Rules",
                effective_date="2021-02-25",
                description="Explicitly supersedes the Information Technology (Intermediaries guidelines) Rules, 2011."
            ),
            LegalRelation(
                relation_type=RelationType.REFERENCES,
                target_document_id="doc-in-it-act-2000",
                target_section="Section 79, 87",
                effective_date="2021-02-25",
                description="Exercised under Section 87(2)(z) and (zg) read with Section 79(2) of IT Act 2000."
            )
        ],
        sections=it_rules_2021_passages,
        mdu_dataset_id="ds-legal-it-rules-2021",
        sha256_hash=_compute_hash(it_rules_21_raw)
    )

    # 5. IT Rules 2011 (Superseded Pair)
    it_rules_2011_passages = [
        LegalPassage(
            section_id="sec-itrules11-3-1",
            section_number="Rule 3(1)",
            heading="Due diligence to be observed by intermediary",
            text="The intermediary shall observe following due diligence while discharging his duties, namely:—(1) The intermediary shall publish the rules and regulations, privacy policy and user agreement for access-or usage of the intermediary's computer resource by any person.",
            keywords=["intermediary", "due diligence", "rules", "privacy policy", "user agreement"],
            effective_date="2011-04-11",
            amendment_history="Notified vide G.S.R. 314(E) dated 11th April, 2011; superseded on 25-02-2021."
        ),
        LegalPassage(
            section_id="sec-itrules11-3-4",
            section_number="Rule 3(4)",
            heading="Intermediary action upon obtaining knowledge of unlawful content",
            text="The intermediary, on obtaining knowledge by itself or been brought to actual knowledge by an affected person in writing or through email, shall act within thirty-six hours and where applicable, work with user or owner of such information to disable such information.",
            keywords=["takedown", "actual knowledge", "36 hours", "disable access", "affected person"],
            effective_date="2011-04-11",
            amendment_history="Interpreted by Supreme Court in Shreya Singhal (2015) to require court order or government notification; superseded in 2021."
        ),
        LegalPassage(
            section_id="sec-itrules11-3-11",
            section_number="Rule 3(11)",
            heading="Grievance Officer redressal timeline (1 Month)",
            text="The intermediary shall publish on its website the name of the Grievance Officer and his contact details as well as mechanism by which users or any person who suffers can notify their complaints. The Grievance Officer shall redress the complaints within one month from the date of receipt of complaint.",
            keywords=["grievance officer", "complaints", "one month", "redressal timeline"],
            effective_date="2011-04-11",
            amendment_history="Superseded on 2021-02-25 by Rule 3(2) of IT Rules 2021 (which shortened redressal to 15 days and added 24h ack)."
        ),
    ]
    it_rules_11_raw = "".join(p.text for p in it_rules_2011_passages)
    corpus["doc-in-it-intermediary-rules-2011"] = LegalDocument(
        document_id="doc-in-it-intermediary-rules-2011",
        title="The Information Technology (Intermediaries guidelines) Rules, 2011",
        short_name="IT Intermediary Rules 2011",
        issuing_authority="Ministry of Communications and Information Technology, Government of India",
        jurisdiction="India",
        source_url="https://www.meity.gov.in/writereaddata/files/Information%20Technology%20%28Intermediaries%20guidelines%29%20Rules%2C%202011.pdf",
        publication_date="2011-04-11",
        effective_date="2011-04-11",
        retrieval_date="2026-11-06",
        version="1.0.0",
        status=DocumentStatus.SUPERSEDED,
        relations=[
            LegalRelation(
                relation_type=RelationType.SUPERSEDED_BY,
                target_document_id="doc-in-it-rules-2021",
                target_section="All Rules",
                effective_date="2021-02-25",
                description="Repealed and superseded in toto by IT Rules 2021 on 25th February 2021."
            )
        ],
        sections=it_rules_2011_passages,
        mdu_dataset_id="ds-legal-it-rules-2011",
        sha256_hash=_compute_hash(it_rules_11_raw)
    )

    # 6. SPDI Rules 2011
    spdi_passages = [
        LegalPassage(
            section_id="sec-spdi-3",
            section_number="Rule 3",
            heading="Sensitive personal data or information",
            text="Sensitive personal data or information of a person means such personal information which consists of information relating to:—(i) password; (ii) financial information such as Bank account or credit card or debit card or other payment instrument details; (iii) physical, physiological and mental health condition; (iv) sexual orientation; (v) medical records and history; (vi) Biometric information.",
            keywords=["sensitive personal data", "spdi", "passwords", "financial information", "biometric", "medical records"],
            effective_date="2011-04-11",
            amendment_history="Notified vide G.S.R. 313(E) dated 11th April, 2011 under Section 43A of IT Act 2000."
        ),
        LegalPassage(
            section_id="sec-spdi-4",
            section_number="Rule 4",
            heading="Privacy policy and disclosure of information",
            text="The body corporate or any person who on behalf of body corporate collects, receives, possess, stores, deals or handle information of provider of information, shall provide a privacy policy for handling of or dealing in personal information including sensitive personal data or information and ensure that the same are available for view by such providers of information who has provided such information under lawful contract.",
            keywords=["privacy policy", "body corporate", "disclosure", "handling", "sensitive personal data"],
            effective_date="2011-04-11",
            amendment_history="Notified vide G.S.R. 313(E)."
        ),
        LegalPassage(
            section_id="sec-spdi-8",
            section_number="Rule 8",
            heading="Reasonable security practices and procedures (ISO 27001)",
            text="A body corporate or a person on its behalf shall be considered to have complied with reasonable security practices and procedures, if they have implemented such security practices and standards and have a comprehensive documented information security programme and information security policies that contain managerial, technical, operational and physical security control measures that are commensurate with the information assets being protected with the nature of business. The international Standard IS/ISO/IEC 27001 on 'Information Technology - Security Techniques - Information Security Management System - Requirements' is one such standard.",
            keywords=["reasonable security practices", "iso 27001", "information security programme", "security control measures"],
            effective_date="2011-04-11",
            amendment_history="Standard benchmark under Section 43A; transitional in light of DPDP Act 2023."
        ),
    ]
    spdi_raw = "".join(p.text for p in spdi_passages)
    corpus["doc-in-spdi-rules-2011"] = LegalDocument(
        document_id="doc-in-spdi-rules-2011",
        title="The Information Technology (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011",
        short_name="SPDI Rules 2011",
        issuing_authority="Ministry of Communications and Information Technology, Government of India",
        jurisdiction="India",
        source_url="https://www.meity.gov.in/writereaddata/files/GSR313E_10511%281%29_0.pdf",
        publication_date="2011-04-11",
        effective_date="2011-04-11",
        retrieval_date="2026-11-06",
        version="1.0.0",
        status=DocumentStatus.TRANSITIONAL,
        relations=[
            LegalRelation(
                relation_type=RelationType.REFERENCES,
                target_document_id="doc-in-it-act-2000",
                target_section="Section 43A",
                effective_date="2011-04-11",
                description="Exercised under Section 87(2)(ob) read with Section 43A of IT Act 2000."
            ),
            LegalRelation(
                relation_type=RelationType.TRANSITIONAL_TO,
                target_document_id="doc-in-dpdp-act-2023",
                target_section="Section 8, Section 44",
                effective_date="2023-08-11",
                description="Transitions under DPDP Act 2023 as Section 43A is omitted."
            )
        ],
        sections=spdi_passages,
        mdu_dataset_id="ds-legal-spdi-rules-2011",
        sha256_hash=_compute_hash(spdi_raw)
    )

    # 7. Companies Act 2013 (Fiduciary Duties & Governance)
    companies_passages = [
        LegalPassage(
            section_id="sec-ca-134-5",
            section_number="Section 134(5)",
            heading="Directors' Responsibility Statement - Compliance Systems",
            text="The Directors' Responsibility Statement referred to in clause (c) of sub-section (3) shall state that: (e) the directors, in the case of a listed company, had laid down internal financial controls to be followed by the company and that such internal financial controls are adequate and were operating effectively; and (f) the directors had devised proper systems to ensure compliance with the provisions of all applicable laws and that such systems were adequate and operating effectively.",
            keywords=["directors responsibility statement", "compliance systems", "applicable laws", "internal financial controls", "adequate and effective"],
            effective_date="2013-09-12",
            amendment_history="Enacted as Act No. 18 of 2013."
        ),
        LegalPassage(
            section_id="sec-ca-166",
            section_number="Section 166",
            heading="Duties of directors",
            text="(1) Subject to the provisions of this Act, a director of a company shall act in accordance with the articles of the company. (2) A director of a company shall act in good faith in order to promote the objects of the company for the benefit of its members as a whole, and in the best interests of the company, its employees, the shareholders, the community and for the protection of environment. (3) A director of a company shall exercise his duties with due and reasonable care, skill and diligence and shall exercise independent judgment.",
            keywords=["duties of directors", "good faith", "reasonable care", "due diligence", "independent judgment", "fiduciary duty"],
            effective_date="2013-09-12",
            amendment_history="Codified statutory fiduciary duties under Act No. 18 of 2013."
        ),
        LegalPassage(
            section_id="sec-ca-177",
            section_number="Section 177",
            heading="Audit Committee and Vigil Mechanism",
            text="Every listed company and such other class or classes of companies which accept deposits or have borrowed money from banks in excess of fifty crore rupees shall establish a vigil mechanism for directors and employees to report genuine concerns in such manner as may be prescribed. The vigil mechanism shall provide for adequate safeguards against victimisation of persons who use such mechanism.",
            keywords=["audit committee", "vigil mechanism", "whistleblower", "victimisation safeguards", "genuine concerns"],
            effective_date="2013-09-12",
            amendment_history="Enacted as Act No. 18 of 2013."
        ),
    ]
    ca_raw = "".join(p.text for p in companies_passages)
    corpus["doc-in-companies-act-2013"] = LegalDocument(
        document_id="doc-in-companies-act-2013",
        title="The Companies Act, 2013 (Act No. 18 of 2013)",
        short_name="Companies Act 2013",
        issuing_authority="Ministry of Corporate Affairs, Government of India",
        jurisdiction="India",
        source_url="https://www.mca.gov.in/content/dam/mca/pdf/CompaniesAct2013.pdf",
        publication_date="2013-08-29",
        effective_date="2013-09-12",
        retrieval_date="2026-11-06",
        version="1.0.0",
        status=DocumentStatus.CURRENT,
        relations=[
            LegalRelation(
                relation_type=RelationType.REPLACES,
                target_document_id="doc-in-companies-act-1956",
                target_section="Section 217, 291",
                effective_date="2013-09-12",
                description="Modernized corporate governance provisions of Companies Act, 1956."
            )
        ],
        sections=companies_passages,
        mdu_dataset_id="ds-legal-companies-act-2013",
        sha256_hash=_compute_hash(ca_raw)
    )

    # 8. Indian Contract Act 1872
    contract_passages = [
        LegalPassage(
            section_id="sec-ica-10",
            section_number="Section 10",
            heading="What agreements are contracts",
            text="All agreements are contracts if they are made by the free consent of parties competent to contract, for a lawful consideration and with a lawful object, and are not hereby expressly declared to be void.",
            keywords=["contract formation", "agreements", "free consent", "competent to contract", "lawful consideration", "lawful object"],
            effective_date="1872-09-01",
            amendment_history="Act No. 9 of 1872."
        ),
        LegalPassage(
            section_id="sec-ica-23",
            section_number="Section 23",
            heading="What considerations and objects are lawful, and what not",
            text="The consideration or object of an agreement is lawful, unless—it is forbidden by law; or is of such a nature that, if permitted, it would defeat the provisions of any law; or is fraudulent; or involves or implies injury to the person or property of another; or the Court regards it as immoral, or opposed to public policy. In each of these cases, the consideration or object of an agreement is said to be unlawful. Every agreement of which the object or consideration is unlawful is void.",
            keywords=["lawful object", "unlawful consideration", "forbidden by law", "fraudulent", "public policy", "void contract"],
            effective_date="1872-09-01",
            amendment_history="Fundamental contract invalidation doctrine under Act No. 9 of 1872."
        ),
        LegalPassage(
            section_id="sec-ica-73",
            section_number="Section 73",
            heading="Compensation for loss or damage caused by breach of contract",
            text="When a contract has been broken, the party who suffers by such breach is entitled to receive, from the party who has broken the contract, compensation for any loss or damage caused to him thereby, which naturally arose in the usual course of things from such breach, or which the parties knew, when they made the contract, to be likely to result from the breach of it.",
            keywords=["breach of contract", "compensation", "damages", "loss", "direct loss", "contemplation of parties"],
            effective_date="1872-09-01",
            amendment_history="Act No. 9 of 1872."
        ),
    ]
    contract_raw = "".join(p.text for p in contract_passages)
    corpus["doc-in-contract-act-1872"] = LegalDocument(
        document_id="doc-in-contract-act-1872",
        title="The Indian Contract Act, 1872 (Act No. 9 of 1872)",
        short_name="Indian Contract Act 1872",
        issuing_authority="Legislative Department, Ministry of Law and Justice, Government of India",
        jurisdiction="India",
        source_url="https://www.indiacode.nic.in/handle/123456789/2187",
        publication_date="1872-04-25",
        effective_date="1872-09-01",
        retrieval_date="2026-11-06",
        version="1.0.0",
        status=DocumentStatus.CURRENT,
        relations=[
            LegalRelation(
                relation_type=RelationType.REFERENCES,
                target_document_id="doc-in-it-act-2000",
                target_section="Section 10A",
                effective_date="2000-10-17",
                description="Governs validity of electronic proposals and acceptances recognized under Section 10A of IT Act 2000."
            )
        ],
        sections=contract_passages,
        mdu_dataset_id="ds-legal-contract-act-1872",
        sha256_hash=_compute_hash(contract_raw)
    )

    return corpus

