# P3 Development Agreement

## One application

Everyone works from a complete clone of RoomRadar.
Do not create separate applications or blank section documents.

The P2 baseline remains available under the p2 tag.
Do not move or replace that tag.

## Planned implementation layout

src/roomradar/
  main.py                 FastAPI application and API routes
  schemas.py              Shared request and response definitions
  catalog.py              Room lookup and filtering
  reporting.py            Report validation and acceptance coordination
  status.py               Occupancy labels and expiration rules
  repository.py           Database reads, writes and transaction handling
  database.py             Database connection and initialization
  static/
    index.html            Browser interface
    styles.css            Interface styling
    app.js                Browser interactions and API calls

tests/
  conftest.py             Shared test fixtures
  test_catalog.py         Catalog and filter tests
  test_reporting.py       Reporting and failure-path tests
  test_status.py          Status and expiration tests
  test_repository.py      Storage and transaction tests
  test_api.py             API integration tests

These are planned paths, not claims of completed implementation.
Additional files may be added when needed.

## Shared interfaces

Before feature implementation begins, the team must agree on:
- API endpoint names and request/response fields
- Room and report data structures
- Service function signatures
- Database schema
- Error responses and timestamp format

Record these agreements in docs/p3/api-contract.md.
Changes affecting another member's work must be discussed in the relevant
issue or pull request before integration.

## Prerequisites

Each member needs:
- Their own GitHub account with repository access
- Git
- Python
- An IDE or editor, such as VS Code
- A modern browser

The initial application setup will specify the Python version, dependencies,
PostgreSQL setup and exact run commands. Use those shared instructions.

## Branch and review workflow

1. Start your P3 branch from the shared main baseline.
2. Commit and push your own meaningful changes.
3. Open a pull request linked to your assigned issue.
4. The assigned reviewer checks the work and records actual findings.
5. Resolve findings with additional commits.
6. Adam integrates using a merge commit to preserve original commits.

Keep your branch updated with main before integration.
Do not resolve unfamiliar conflicts by blindly accepting either version.

## Documentation

Write the report in the complete shared Google Doc.
Follow docs/p3/evidence/README.md for authorship evidence.

Each member writes their own contribution statement and AI-use entry.
Only claim work and verification actually performed.
