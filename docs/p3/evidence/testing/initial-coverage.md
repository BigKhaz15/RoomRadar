# RoomRadar P3 – Initial Pytest and Coverage Baseline

**Author:** Malak Zaarour  
**Date:** November 26, 2026  
**Branch:** p3/malak  
**Commit tested:** e6964da  
**Application foundation:** 8572f7e

## 1. Environment

- Operating system: Windows
- Python: 3.12.10
- pytest: 9.2.0
- pytest-cov: 7.1.0
- coverage: 7.17.5

Testing tools were installed locally in the virtual environment. Shared dependency files have not been modified.

## 2. Commands

```powershell
$env:PYTHONPATH = "src"
python -m pytest tests/test_error_handlers.py -v
python -m pytest tests/test_error_handlers.py -v --cov=roomradar --cov-branch --cov-report=term-missing
```

## 3. Actual Test Results

| Measurement | Result |
|---|---|
| Tests collected | 4 |
| Tests passed | 4 |
| Tests failed | 0 |
| Tests skipped | 0 |
| Subtests passed | 4 |
| Warnings | 1 |
| Execution time without coverage | 0.73 seconds |
| Execution time with coverage | 0.95 seconds |

## 4. Coverage Results

Measured scope: src/roomradar/

| File | Statements | Missed | Branches | Partial branches | Reported coverage |
|---|---:|---:|---:|---:|---:|
| __init__.py | 0 | 0 | 0 | 0 | 100% |
| config.py | 6 | 6 | 2 | 0 | 0% |
| error_handlers.py | 22 | 0 | 0 | 0 | 100% |
| errors.py | 3 | 0 | 0 | 0 | 100% |
| main.py | 15 | 15 | 0 | 0 | 0% |
| schemas.py | 54 | 1 | 0 | 0 | 98% |
| Total | 100 | 22 | 2 | 0 | 76% |

- Statement coverage: 78%
- Branch coverage: 0%
- Combined statement and branch coverage: 76% (rounded)

## 5. Uncovered Code

- config.py: lines 1–13
- main.py: lines 1–24
- schemas.py: line 16

## 6. Warnings

One StarletteDeprecationWarning concerning httpx and TestClient was observed. No tests failed because of this warning.

## 7. Interpretation and Limitations

The existing unittest tests execute successfully under pytest without modification. The coverage plugin also successfully measures Python statement and branch coverage.

The measured coverage applies only to the current Python application foundation. Existing tests exercise error handling and schema validation through test-only routes.

These measurements do not establish the correctness of PostgreSQL transactions, catalog filtering, actual reporting endpoints, occupancy expiration, or browser behavior.

Browser JavaScript is not included in the coverage measurement.

Assertion strength and mutation testing have not yet been evaluated.

These preliminary measurements will be replaced by integrated application measurements once the required components become available.