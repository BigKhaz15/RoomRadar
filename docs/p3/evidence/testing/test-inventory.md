# RoomRadar P3 – Test Inventory and Oracle Sources

**Author:** Malak Zaarour  
**Date:** November 25, 2026  
**Status:** Initial test planning

## 1. Test Design

Each integration test has a stable identifier, a defined scenario, an explicit expected result, and a specification-based oracle. Expected results are derived from the P2 requirements and proposed P3 API contract, independently of application output.

Controlled synthetic room records and report timestamps will be used to ensure repeatable results.

## 2. Planned API Integration Tests

| Test ID | Test scenario | Expected result | Oracle source | Status |
|---|---|---|---|---|
| INT-01 | Retrieve all catalog rooms | 200; all seeded rooms returned in room_identifier order, including Unknown rooms | FR-06; Contract §§1, 3 | Planned |
| INT-02 | Filter rooms by building | 200; only rooms in the selected building returned | FR-04; Contract §3 | Planned |
| INT-03 | Apply combined implemented filters | 200; every returned room satisfies all supplied filters | FR-09; Contract §3 | Planned |
| INT-04 | Apply filters with no matches | 200; empty rooms array | Contract §3 | Planned |
| INT-05 | Submit valid anonymous Empty and Occupied reports | 201 after successful storage; correct acknowledgment and accepted report fields | FR-02, FR-11, FR-15; Contract §3 | Planned |
| INT-06 | Submit a report for a nonexistent room | 404 ROOM_NOT_FOUND; no report stored | Contract §§3–4 | Planned |
| INT-07 | Submit invalid or missing observations | 422 VALIDATION_ERROR; no report stored | Contract §§3–4 | Planned |
| INT-08 | Simulate known storage failure | 503 STORAGE_UNAVAILABLE; no success acknowledgment; previous accepted report preserved | FR-11, FR-15; Contract §§3–4 | Planned |
| INT-09 | Retrieve occupancy for a current report | 200; correct status label, UTC report timestamp, expiration time and remaining seconds | FR-01, FR-05, FR-13; Contract §§2, 7 | Planned |
| INT-10 | Retrieve occupancy without an existing report | 200; Unknown, null timestamps and zero remaining seconds | FR-01; Contract §2 | Planned |
| INT-11 | Retrieve occupancy at report age 3599 seconds | Reported status; one second remaining with controlled time | FR-01; ADR-03; Contract §7 | Planned |
| INT-12 | Retrieve occupancy at report age 3600 seconds | Unknown; retained timestamps and zero remaining seconds | FR-01, FR-14; ADR-03; Contract §7 | Planned |
| INT-13 | Retrieve occupancy at report age 3601 seconds | Unknown; retained timestamps and zero remaining seconds | FR-01, FR-13; ADR-03; Contract §7 | Planned |
| INT-14 | Verify anonymous reporting and reject extra identity fields | Valid anonymous requests accepted; additional fields rejected with 422; identifying information not echoed | FR-02; Contract §§1, 3–4 | Planned |
| INT-15 | Submit multiple valid reports for the same room | Occupancy reflects the report with the latest acceptance order | FR-12; ADR-02; Contract §7 | Planned |
| INT-16 | Retrieve a specific existing room | 200; correct identifier, building, capacity, amenities and occupancy fields | FR-03; Contract §§2–3 | Planned |
| INT-17 | Retrieve details or occupancy for a nonexistent room | 404 ROOM_NOT_FOUND | Contract §§3–4 | Planned |
| INT-18 | Supply a deferred optional filter, if applicable | 422; unsupported filter is not silently ignored | Contract §3 | Conditional |
| INT-19 | Verify minimum-capacity boundaries, if implemented | Only rooms meeting or exceeding the threshold are returned; invalid thresholds rejected | FR-07; Contract §3 | Conditional |
| INT-20 | Verify amenity filtering, if implemented | Only matching rooms returned; unknown amenities produce an empty result | FR-08; Contract §3 | Conditional |

## 3. Assertion Strategy

Tests will verify more than HTTP response codes. Where applicable, assertions will examine:

- Exact room identifiers and expected catalog records.
- Response body fields and error codes.
- Stored report contents and acceptance ordering.
- Preservation of previously accepted reports after failed submissions.
- Status labels, report timestamps and expiration boundaries.
- Absence of identifying fields in reporting responses.
- Consistency between server time and occupancy calculations.

Expected values will be defined using controlled fixtures and specification requirements, not copied from application responses.

## 4. Coordination with Feature Owners

| Owner | Testing responsibility |
|---|---|
| Adam | Reporting component tests, API implementation and shared error handling |
| Roshan | Actual PostgreSQL transactions, concurrency, rollback and repository tests |
| Raghameena | Catalog filtering and status calculation component tests |
| Tien and Jeimy | Browser behavior, live expiration and end-to-end verification |
| Malak | Shared fixtures, API integration tests, combined suite execution and quality measurements |

Feature owners' test IDs and results will be incorporated into the final combined test inventory once their tests are available.

## 5. Current Status and Limitations

The tests listed in this inventory are planned and have not yet been implemented or executed.

The four existing starter error-handler tests passed on November 25, 2026, as recorded in starter-test-results.md. Those tests provide preliminary evidence only and do not verify the complete application.

Any mocked dependencies will be identified in the corresponding test evidence. Mocked storage behavior will not be presented as proof of actual PostgreSQL transaction correctness.

The proposed API contract and optional filter scope must be confirmed before finalizing test implementation. Untested partitions and boundaries will remain marked NONE until corresponding tests exist.

## 6. Implemented Foundation API Tests

The following tests were implemented on November 26, 2026, using the shared TestClient fixture in tests/conftest.py and the actual RoomRadar FastAPI application.

| Test ID | Test function | Expected result | Oracle source | Status |
|---|---|---|---|---|
| API-001 | test_api_001_health_endpoint | HTTP 200 and exact JSON response containing status: ok | API contract §3 | PASS |
| API-002 | test_api_002_homepage | HTTP 200, HTML content type and RoomRadar text | P3 team guide, page 3 | PASS |
| API-003 | test_api_003_openapi_schema | HTTP 200, RoomRadar application title and registered GET /health endpoint | P3 team guide, page 3; API contract §3 | PASS |

**Implementation files:**

- tests/conftest.py
- tests/test_api.py

**Supporting evidence:**

- docs/p3/evidence/testing/foundation-test-results.md

The three tests passed individually and as part of the combined seven-test suite.

These tests establish basic application availability and route registration. They do not verify database readiness, catalog filtering, report persistence or occupancy expiration.

The planned INT-01 through INT-20 integration tests remain pending until the required application components and isolated database fixtures are available.