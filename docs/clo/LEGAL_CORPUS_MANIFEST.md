# Canonical Legal Corpus Manifest & Provenance Register

**Product:** CLO (Chief Legal Officer) Agent  
**Build Owner:** Ansh  
**Corpus Status:** Ingested & Verified  
**Canonical Domain:** `dom-legal-regulatory-in`  
**Retrieval Audit Date:** 2026-11-06  

---

## 1. Corpus Summary

The CLO canonical registry contains **8 official public legal documents**, capturing statutory obligations, electronic contracting, corporate fiduciary duties, and intermediary rules in India. It includes verified amendment and replacement pairs enabling temporal as-of-date legal reasoning.

| Canonical Document ID | Short Name | Issuing Authority | Effective Date | Status | Relations Summary | MDU Dataset ID |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| `doc-in-dpdp-act-2023` | DPDP Act 2023 | Ministry of Law & Justice | 2023-08-11 | `CURRENT` | Amends `doc-in-it-act-2000` (Sec 44 omits Sec 43A); transitions `doc-in-spdi-rules-2011`. | `ds-legal-dpdp-act-2023` |
| `doc-in-it-act-2000` | IT Act 2000 | Parliament of India / MeitY | 2000-10-17 | `AMENDED` | Amended by `doc-in-it-amendment-act-2008` & `doc-in-dpdp-act-2023`. | `ds-legal-it-act-2000` |
| `doc-in-it-amendment-act-2008` | IT Amendment 2008 | Ministry of Law & Justice | 2009-10-27 | `CURRENT` | Amends `doc-in-it-act-2000` (inserts Sec 43A, 66C, 72A); Sec 43A omitted by DPDP Act 2023. | `ds-legal-it-amend-2008` |
| `doc-in-it-rules-2021` | IT Rules 2021 | MeitY | 2021-02-25 | `CURRENT` | **Replaces/Supersedes** `doc-in-it-intermediary-rules-2011`. References Sec 79 of IT Act. | `ds-legal-it-rules-2021` |
| `doc-in-it-intermediary-rules-2011` | IT Rules 2011 (Superseded) | Dept. of Information Technology | 2011-04-11 | `SUPERSEDED` | **Superseded by** `doc-in-it-rules-2021` (w.e.f. 2021-02-25). | `ds-legal-it-rules-2011` |
| `doc-in-spdi-rules-2011` | SPDI Rules 2011 | Ministry of Communications & IT | 2011-04-11 | `TRANSITIONAL` | Issued under Sec 43A of IT Act; transitions into DPDP Act 2023 regime. | `ds-legal-spdi-rules-2011` |
| `doc-in-companies-act-2013` | Companies Act 2013 | Ministry of Corporate Affairs | 2013-09-12 | `CURRENT` | Replaces corporate governance provisions of Companies Act, 1956. | `ds-legal-companies-act-2013` |
| `doc-in-contract-act-1872` | Contract Act 1872 | Legislative Dept, Law Ministry | 1872-09-01 | `CURRENT` | References Sec 10A of IT Act 2000 for electronic contracts. | `ds-legal-contract-act-1872` |

---

## 2. Verified Amendment & Replacement Pairs

### Pair A: IT Intermediary Rules 2011 $\rightarrow$ IT Intermediary Rules 2021 (Full Supersession)
- **Prior Active Law (2011-04-11 to 2021-02-24)**:
  - Document: `doc-in-it-intermediary-rules-2011` (G.S.R. 314(E))
  - Rule 3(11): Grievance Officer shall redress complaints within **one month** from receipt.
- **Superseding Law (2021-02-25 to Present)**:
  - Document: `doc-in-it-rules-2021` (G.S.R. 139(E))
  - Rule 3(2): Grievance Officer shall acknowledge complaint within **twenty-four hours** and resolve within **fifteen days**.
- **Temporal Enforcement Logic**:
  - When query is evaluated with `as_of_date < 2021-02-25`: Status of 2011 Rules is `CURRENT` (1-month timeline).
  - When query is evaluated with `as_of_date >= 2021-02-25`: Status of 2011 Rules is `SUPERSEDED`; 2021 Rules is `CURRENT` (15-day timeline).

### Pair B: IT Act 2000 $\rightarrow$ IT Amendment Act 2008 $\rightarrow$ DPDP Act 2023 (Corporate Data Liability)
- **Base Law (2000)**: IT Act 2000 contained no explicit corporate data protection provision.
- **Amended Law (2009-10-27)**: IT Amendment Act 2008 inserted Section 43A making bodies corporate liable to pay compensation for negligence in implementing reasonable security practices.
- **Omission by DPDP Act 2023 (2023-08-11)**: Section 44 of DPDP Act 2023 expressly omits Section 43A of the IT Act 2000 upon commencement, shifting corporate security obligations to Section 8 of the DPDP Act 2023.

---

## 3. Official Source Provenance Details

### 1. Digital Personal Data Protection Act, 2023
- **Source URL**: `https://egazette.gov.in/WriteReadData/2023/248045.pdf`
- **Gazette Ref**: The Gazette of India, Extraordinary, Part II—Section 1, No. 22 of 2023
- **Publication Date**: August 11, 2023
- **Effective Date**: August 11, 2023
- **Sections Ingested**: Section 4 (Grounds for processing), Section 6 (Consent), Section 8 (General obligations of Data Fiduciary), Section 44 (Amendments to IT Act 2000).

### 2. Information Technology Act, 2000
- **Source URL**: `https://www.indiacode.nic.in/handle/123456789/1999`
- **Gazette Ref**: Act No. 21 of 2000
- **Publication Date**: June 9, 2000
- **Effective Date**: October 17, 2000
- **Sections Ingested**: Section 10A (Electronic contracts), Section 43 (Damage compensation), Section 65 (Source code tampering).

### 3. Information Technology (Amendment) Act, 2008
- **Source URL**: `https://egazette.gov.in/WriteReadData/2009/E_10_2009_002.pdf`
- **Gazette Ref**: The Gazette of India, Extraordinary, Part II—Section 1, Act No. 10 of 2009
- **Publication Date**: February 5, 2009
- **Effective Date**: October 27, 2009
- **Sections Ingested**: Section 43A (Data protection compensation), Section 66C (Identity theft), Section 72A (Breach of lawful contract).

### 4. IT (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021
- **Source URL**: `https://www.meity.gov.in/writereaddata/files/Intermediary_Guidelines_and_Digital_Media_Ethics_Code_Rules-2021.pdf`
- **Gazette Ref**: G.S.R. 139(E), Ministry of Electronics and Information Technology
- **Publication Date**: February 25, 2021
- **Effective Date**: February 25, 2021
- **Sections Ingested**: Rule 3(1)(a) (Publish rules and privacy policy), Rule 3(2) (Grievance mechanism 24h/15d), Rule 3(1)(d) (36h takedown upon court order).

### 5. IT (Intermediaries guidelines) Rules, 2011
- **Source URL**: `https://www.meity.gov.in/writereaddata/files/Information%20Technology%20%28Intermediaries%20guidelines%29%20Rules%2C%202011.pdf`
- **Gazette Ref**: G.S.R. 314(E), Department of Information Technology
- **Publication Date**: April 11, 2011
- **Effective Date**: April 11, 2011
- **Sections Ingested**: Rule 3(1) (Due diligence), Rule 3(4) (36h action upon actual knowledge), Rule 3(11) (1-month grievance redressal).

### 6. IT (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011
- **Source URL**: `https://www.meity.gov.in/writereaddata/files/GSR313E_10511%281%29_0.pdf`
- **Gazette Ref**: G.S.R. 313(E), Department of Information Technology
- **Publication Date**: April 11, 2011
- **Effective Date**: April 11, 2011
- **Sections Ingested**: Rule 3 (SPDI definitions), Rule 4 (Privacy policy), Rule 8 (ISO 27001 standard).

### 7. Companies Act, 2013
- **Source URL**: `https://www.mca.gov.in/content/dam/mca/pdf/CompaniesAct2013.pdf`
- **Gazette Ref**: Act No. 18 of 2013, Ministry of Corporate Affairs
- **Publication Date**: August 29, 2013
- **Effective Date**: September 12, 2013
- **Sections Ingested**: Section 134(5) (Directors' responsibility for compliance systems), Section 166 (Duties of directors), Section 177 (Audit Committee and vigil mechanism).

### 8. Indian Contract Act, 1872
- **Source URL**: `https://www.indiacode.nic.in/handle/123456789/2187`
- **Gazette Ref**: Act No. 9 of 1872, Legislative Department
- **Publication Date**: April 25, 1872
- **Effective Date**: September 1, 1872
- **Sections Ingested**: Section 10 (What agreements are contracts), Section 23 (Lawful consideration and object), Section 73 (Breach of contract damages).

