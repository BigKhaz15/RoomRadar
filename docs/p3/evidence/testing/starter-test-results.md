# Starter Test Results

## Environment

- Tester: Malak Zaarour
- Date: November 25, 2026
- Operating system: Windows
- Python version: 3.12.10
- Branch: p3/malak
- Commit tested: 8572f7ec8c63a7b52a78e16e3718ce90b8a4f14b
- Working tree: Clean

## Test Command

```powershell
$env:PYTHONPATH = "src"
& ".\.venv\Scripts\python.exe" -m unittest discover -s tests -p "test_error_handlers.py" -v
```

## Actual Results

| Measurement | Result |
|---|---|
| Tests executed | 4 |
| Tests passed | 4 |
| Tests failed | 0 |
| Tests skipped | 0 |
| Execution time | 0.083 seconds |

## Test Outcomes

| Test function | Result |
|---|---|
| test_application_errors_use_safe_contract | PASS |
| test_extra_identity_field_is_rejected_without_echo | PASS |
| test_invalid_observation_is_rejected | PASS |
| test_valid_observation_is_accepted | PASS |

## Warnings

A StarletteDeprecationWarning concerning httpx and TestClient was observed. The warning did not cause any test failures. Dependency changes will be coordinated with Adam.

## Limitations

These tests verify the existing error-handling and validation functionality through test-only routes. They do not verify PostgreSQL storage, actual reporting endpoints, catalog filtering, report expiration, or browser behavior. Coverage has not yet been measured.

This run establishes the initial testing baseline for P3 integration testing.