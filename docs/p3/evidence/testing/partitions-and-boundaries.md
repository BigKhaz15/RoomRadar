# RoomRadar P3 – Test Partitions and Boundaries

**Author:** Malak Zaarour  
**Date:** November 25, 2026  
**Status:** Initial test planning

## 1. Objective

Equivalence partitioning and boundary value analysis are used to identify representative test inputs and important edge cases. Expected results are derived from the P2 requirements and the proposed P3 API contract rather than from observed application output.

## 2. Equivalence Partitions

| Input | Partition | Representative input | Expected result | Oracle source | Test coverage |
|---|---|---|---|---|---|
| Room identifier | Existing room | DEMO-A-101 | Room retrieved or report accepted for a valid request | Contract §3 | NONE |
| Room identifier | Nonexistent room | INVALID-ROOM | 404 ROOM_NOT_FOUND; no report stored | Contract §§3–4 | NONE |
| Observation | Valid Empty | Empty | 201; report stored | FR-02, FR-11; Contract §3 | NONE |
| Observation | Valid Occupied | Occupied | 201; report stored | FR-02, FR-11; Contract §3 | NONE |
| Observation | Invalid value | Available | 422 VALIDATION_ERROR; no report stored | Contract §§3–4 | NONE |
| Observation | Empty string | "" | 422 VALIDATION_ERROR | Contract §§3–4 | NONE |
| Observation | Missing field | {} | 422 VALIDATION_ERROR | Contract §§3–4 | NONE |
| Report payload | Anonymous | Observation only | Accepted without identification | FR-02; Contract §§1, 3 | NONE |
| Report payload | Additional identifying field | Observation and username | 422 VALIDATION_ERROR | FR-02; Contract §3 | NONE |
| Report state | Missing report | No stored report | Unknown; null timestamps; zero remaining seconds | FR-01; Contract §2 | NONE |
| Report state | Current report | Report aged 1200 seconds | Corresponding Reported Empty or Reported Occupied label | FR-01, FR-05; Contract §7 | NONE |
| Report state | Expired report | Report aged 4000 seconds | Unknown; retained timestamps; zero remaining seconds | FR-01, FR-13; Contract §§2, 7 | NONE |
| Building filter | No filter | Parameter omitted | All catalog rooms returned | FR-06; Contract §3 | NONE |
| Building filter | Matching building | Demo Building A | Only rooms in the selected building | FR-04; Contract §3 | NONE |
| Building filter | No matching building | Nonexistent Building | 200 with an empty rooms array | FR-10; Contract §3 | NONE |
| Combined filters | Matching criteria | Building A, minimum capacity 4 | Rooms satisfying all active filters | FR-09; Contract §3 | NONE |
| Combined filters | No matching criteria | Building A, minimum capacity 100 | 200 with an empty rooms array | FR-09, FR-10; Contract §3 | NONE |
| Amenity filter | Matching amenity | Whiteboard | Only rooms containing the selected amenity | FR-08; Contract §3 | NONE |
| Amenity filter | Unknown amenity | Nonexistent Amenity | 200 with an empty rooms array | Contract §3 | NONE |
| Optional filter | Deferred functionality | Supplied unsupported filter | 422; filter is not silently ignored | Contract §3 | NONE |
| Storage outcome | Successful commit | Valid report | 201 only after commit | FR-11, FR-15; Contract §3 | NONE |
| Storage outcome | Known storage failure | Injected write failure | 503; no success acknowledgment; previous report preserved | FR-15; Contract §§3–4 | NONE |

## 3. Boundary Value Analysis

### 3.1 Report Expiration

The expiration threshold is 3600 seconds after report submission. Controlled UTC timestamps will be used instead of waiting for reports to expire in real time.

The following cases assume an accepted Empty report.

| Report age | Boundary position | Expected label | Remaining seconds | Timestamp | Test coverage |
|---|---|---|---|---|---|
| 0 seconds | Initial report age | Reported Empty | 3600 | Retained | NONE |
| 3599 seconds | Immediately below expiration | Reported Empty | 1 | Retained | NONE |
| 3600 seconds | Exact expiration boundary | Unknown | 0 | Retained | NONE |
| 3601 seconds | Immediately above expiration | Unknown | 0 | Retained | NONE |

Oracle: FR-01, FR-13, FR-14, ADR-03 and API contract §§2, 7.

### 3.2 Minimum Capacity

These cases apply if minimum-capacity filtering is implemented. The proposed controlled fixture contains rooms with capacities of 2, 4, and 6.

| Minimum capacity | Boundary condition | Expected result | Test coverage |
|---|---|---|---|
| 0 | Invalid lower boundary | 422 VALIDATION_ERROR | NONE |
| 1 | Minimum valid input | All three fixture rooms returned | NONE |
| 3 | Below a room capacity of 4 | Rooms with capacities 4 and 6 | NONE |
| 4 | Equal to a room capacity of 4 | Rooms with capacities 4 and 6 | NONE |
| 5 | Above a room capacity of 4 | Only the room with capacity 6 | NONE |
| 7 | Above maximum fixture capacity | 200 with an empty rooms array | NONE |

Oracle: FR-07 and API contract §3.

## 4. Acceptance Ordering

| Condition | Expected result | Test coverage |
|---|---|---|
| One accepted report | Occupancy reflects the accepted report | NONE |
| Two accepted reports | Report with the greater acceptance order determines occupancy | NONE |
| Two reports with identical submission timestamps | Acceptance order determines precedence | NONE |
| Failed subsequent transaction | Previously accepted report remains unchanged | NONE |

Oracle: FR-12, ADR-02 and API contract §7.

PostgreSQL transaction and concurrency verification will be coordinated with Roshan.

## 5. Coverage Status and Limitations

NONE indicates that no P3 integration test has yet been established for the corresponding partition or boundary.

The existing starter tests provide preliminary validation and error-handling evidence through test-only routes but do not establish coverage of the integrated API and database behavior.

Test coverage entries will be updated with stable test IDs as tests are implemented. Optional filtering partitions depend on the final delivered scope. Browser expiration verification will be coordinated with Tien and Jeimy.

All representative room records and input values in this document are proposed synthetic test data.