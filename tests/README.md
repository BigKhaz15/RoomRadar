# RoomRadar Tests

This folder contains tests for the P3 application.

Feature owners write tests for their own behavior. The testing lead
coordinates integration tests, shared fixtures and quality measurements.

Each test must have:
- A clear purpose
- An expected result derived from a requirement, design decision or use-case step
- Assertions that check the expected behavior

Priority risks include:
- Missing reports and the 60-minute expiration boundary
- Latest-report selection and acceptance ordering
- Storage failures and rollback
- Invalid room identifiers and occupancy observations
- Combined filters and no matching rooms

Record actual results, including failures and known gaps.
Do not report the P2 spike results as proof that the P3 application passes.


## Pytest and Coverage

The initial pytest setup preserves the existing unittest error-handler tests and supports the new API tests through shared fixtures.

### Testing Dependencies

The following versions have been verified locally with Python 3.12.10:

- pytest 9.2.0
- pytest-cov 7.1.0
- coverage 7.17.5

Until the shared development dependencies are updated in coordination with Adam, install the testing tools locally:

```powershell
python -m pip install pytest==9.2.0 pytest-cov==7.1.0 coverage==7.17.5
```

### Run All Tests

From the repository root, using the project's virtual environment:

```powershell
$env:PYTHONPATH = "src"
python -m pytest tests/ -v
```

### Run API Tests Only

```powershell
python -m pytest tests/test_api.py -v
```

### Measure Statement and Branch Coverage

```powershell
python -m pytest tests/ -v --cov=roomradar --cov-branch --cov-report=term-missing
```

Coverage is measured for the Python package under src/roomradar/. Browser JavaScript is not included.

### List Collected Tests

```powershell
python -m pytest tests/ --collect-only -q
```

### Shared Fixtures

The client fixture in tests/conftest.py provides a FastAPI TestClient for the actual RoomRadar application and closes the client after each test.

### Database Safety

The current foundation tests do not require a database. Before database-backed integration tests are introduced, an isolated PostgreSQL test database must be configured in coordination with Roshan.

Tests must never initialize, modify, or clear normal development or demonstration data.

### Testing Evidence

Test inventories, risk analysis, coverage measurements, and execution results are maintained under:

`docs/p3/evidence/testing/`

Preliminary foundation test results must not be interpreted as verification of the complete application.