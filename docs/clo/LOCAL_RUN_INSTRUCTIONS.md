# CLO Agent Increment — Local Run & Verification Instructions

**Product:** CLO (Chief Legal Officer) Agent Increment  
**Build Owner:** Ansh  
**Target Repository:** `praj33/BHIV-BIQOS-P0-EXECUTION`  
**Feature Branch:** `feat/clo-agent-increment`  

---

## 1. Prerequisites

- Python 3.10+ (tested on Python 3.12.3)
- Installed dependencies:
  ```bash
  pip install fastapi uvicorn pydantic httpx pytest pytest-asyncio
  ```

---

## 2. Running Automated Tests

From the `BHIV-BIQOS-P0-EXECUTION` directory:

```bash
# Run full CLO test suite with verbose output
python3 -m pytest tests/clo -v

# Run only temporal supersession tests
python3 -m pytest tests/clo/test_temporal_as_of_date.py -v

# Run only security and permission boundary tests
python3 -m pytest tests/clo/test_security_and_vajra_boundaries.py -v
```

---

## 3. Starting the Local CLO Runtime API

Run the FastAPI application via Uvicorn:

```bash
# In BHIV-BIQOS-P0-EXECUTION:
uvicorn clo.runtime.api:app --host 127.0.0.1 --port 8085 --reload
```

Interactive Swagger documentation will be available at:
`http://127.0.0.1:8085/docs`

---

## 4. Sample Demonstration Queries (cURL)

### 4.1 System Health & Registry Probe
```bash
curl -X GET http://127.0.0.1:8085/health
```

### 4.2 Legal Research Query (Evidence-First with As-of-Date)
```bash
curl -X POST http://127.0.0.1:8085/api/v1/clo/research \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are reasonable security safeguards to prevent personal data breach?",
    "as_of_date": "2024-01-15",
    "caller_identity": "ansh_clo_build_owner",
    "auth_token": "ANSH_CLO_GOVERNED_SESSION"
  }'
```

### 4.3 Historical As-of-Date Query (Evaluating Superseded Law in 2018)
```bash
curl -X POST http://127.0.0.1:8085/api/v1/clo/research \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the timeline for the Grievance Officer to redress complaints under intermediary rules?",
    "as_of_date": "2018-01-01",
    "caller_identity": "ansh_clo_build_owner",
    "auth_token": "ANSH_CLO_GOVERNED_SESSION"
  }'
```

### 4.4 Negative Test (Hard Rule 5: Zero Evidence Refusal)
```bash
curl -X POST http://127.0.0.1:8085/api/v1/clo/research \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the speed limit of warp drive spaceships under maritime law?",
    "caller_identity": "ansh_clo_build_owner",
    "auth_token": "ANSH_CLO_GOVERNED_SESSION"
  }'
```

### 4.5 Negative Test (Security Boundary: Revoked Caller Denied)
```bash
curl -X POST http://127.0.0.1:8085/api/v1/clo/research \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are director duties under Companies Act?",
    "caller_identity": "compromised_key_actor"
  }'
# Returns 403 Forbidden fail-closed
```

