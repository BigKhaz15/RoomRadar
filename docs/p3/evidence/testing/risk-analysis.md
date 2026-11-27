# RoomRadar P3 – Testing Priorities and Risk Analysis

**Author:** Malak Zaarour  
**Date:** November 25, 2026  
**Status:** Initial test planning

## Testing Objective

The primary objective of integration testing is to verify that RoomRadar's API, catalog service, reporting service, status resolver, and database repository interact correctly. Testing prioritizes failures that could provide misleading occupancy information, compromise report integrity, or violate anonymous reporting requirements.

## Risk-Based Testing Priorities

| Risk ID | Potential failure | Impact | Priority | Planned verification | Oracle source |
|---|---|---|---|---|---|
| RISK-01 | Incorrect latest report selection | Students receive inaccurate room availability information. | High | Verify that the latest accepted report determines occupancy. Coordinate transaction checks with Roshan. | FR-12, ADR-02, API contract §7 |
| RISK-02 | Incorrect report expiration | Outdated occupancy information is presented as current. | High | Verify missing reports and report ages of 3599, 3600, and 3601 seconds. | FR-01, FR-13, FR-14, ADR-03, API contract §7 |
| RISK-03 | Storage failure acknowledged as success | Students believe their reports were saved when they were not. | High | Simulate a known storage failure and verify a 503 response and preservation of the previous accepted report. | FR-11, FR-15, API contract §§3–4 |
| RISK-04 | Invalid room identifiers or observations accepted | Invalid reports compromise stored data and occupancy accuracy. | High | Submit invalid identifiers and observations; verify rejection without storage. | API contract §§3–4 |
| RISK-05 | Identifying information accepted or required | Anonymous reporting requirements are violated. | High | Verify anonymous submissions and rejection of additional identifying fields. | FR-02, API contract §§1, 3 |
| RISK-06 | Incorrect catalog results or filtering | Students cannot locate appropriate study rooms. | High | Verify unfiltered room lists, building filters, implemented combined filters, and empty results. | FR-04, FR-06–FR-10, API contract §3 |
| RISK-07 | Incorrect occupancy timestamps or response fields | Students cannot accurately determine the freshness of a report. | High | Verify status labels, UTC timestamps, expiration times, and remaining seconds. | FR-05, FR-13, API contract §§1–2, 7 |
| RISK-08 | Test fixtures modify development or demonstration data | Normal application data may be lost or corrupted. | High | Verify isolated test database configuration and safe fixture cleanup before running database integration tests. | Issue #27 testing requirements |

## Testing Scope and Dependencies

API integration tests will use controlled test data and explicit expected results derived from the approved P2 requirements and the proposed P3 API contract.

Actual PostgreSQL transaction behavior will be verified in coordination with Roshan. Browser expiration and user-interface behavior will be verified in coordination with Tien and Jeimy.

Optional capacity and amenity filtering will be tested according to the final implemented scope. Deferred filters must not be silently ignored by the API.

Mocked dependencies will be explicitly documented, including the real behaviors they cannot verify.

## Current Limitations

The initial application foundation has been successfully executed, and all four existing error-handler tests passed on commit 8572f7ec8c63a7b52a78e16e3718ce90b8a4f14b.

These results do not establish successful database integration or complete application functionality. The risks and verification activities listed above represent planned testing, not completed integration tests.

The API contract remains proposed for team review. Expected results will be updated if agreed contract changes occur.