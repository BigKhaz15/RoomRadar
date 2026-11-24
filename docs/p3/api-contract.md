# RoomRadar P3 API and Service Contract

Status: Proposed for team review.
Owner: Adam Khazem.

This contract defines implementation interfaces for the approved P2 behavior.
It does not claim that these endpoints are already implemented.

## 1. Common conventions

- API prefix: /api
- Requests and responses use JSON.
- No accounts, authentication or identifying report fields.
- Timestamps are timezone-aware UTC ISO 8601 strings ending in Z.
- A room identifier is globally unique across the catalog.
- Report observations are exactly "Empty" or "Occupied".
- Display labels are exactly "Reported Empty", "Reported Occupied" or "Unknown".
- Room lists are ordered by room_identifier for predictable results.
- An empty result is a successful response with an empty rooms array.

The browser connects to the same server that serves its page.

## 2. Room representation

```json
{
  "room_identifier": "DEMO-A-101",
  "building": "Demo Building A",
  "capacity": 4,
  "amenities": ["Whiteboard"],
  "occupancy": {
    "label": "Reported Empty",
    "latest_report_time": "2026-11-23T18:00:00Z",
    "expires_at": "2026-11-23T19:00:00Z",
    "remaining_seconds": 1200
  }
}
```

- capacity is a positive integer.
- amenities is an array of strings.
- latest_report_time is null when no report exists.
- expires_at is null when no report exists.
- remaining_seconds is a nonnegative number, not rounded upward.
- Missing reports have Unknown status, null timestamps and zero remaining seconds.
- Expired reports have Unknown status, retained timestamps and zero remaining seconds.

The example is synthetic demonstration data.

## 3. Endpoints

### GET /health

Confirms that the API process responds; it does not verify database readiness.

200:
```json
{"status": "ok"}
```

### GET /api/rooms

Optional query parameters:
- building: exact catalog building name.
- minimum_capacity: positive integer.
- amenity: exact catalog amenity name.

All supplied filters combine using AND.
No filters returns all catalog rooms, including Unknown rooms.
Unknown building or amenity values produce no matches, not an error.
The browser omits unused filters.

200:
```json
{
  "rooms": [],
  "server_time": "2026-11-23T18:40:00Z"
}
```

Each rooms entry uses the room representation above.

Building filtering is MUST.
Minimum-capacity filtering is SHOULD; amenity filtering is COULD.
If either optional filter is deferred, document that decision and remove its
control from the UI. An unsupported supplied filter returns 422; it must
not be silently ignored.

### GET /api/rooms/{room_identifier}

Returns the selected room, including occupancy and timing.

200:
```json
{
  "room": {},
  "server_time": "2026-11-23T18:40:00Z"
}
```

The room object uses the complete room representation above.
An identifier absent from the catalog returns 404.

### GET /api/rooms/{room_identifier}/occupancy

200:
```json
{
  "room_identifier": "DEMO-A-101",
  "occupancy": {
    "label": "Unknown",
    "latest_report_time": null,
    "expires_at": null,
    "remaining_seconds": 0
  },
  "server_time": "2026-11-23T18:40:00Z"
}
```

An identifier absent from the catalog returns 404.

### POST /api/rooms/{room_identifier}/reports

Request:
```json
{"observation": "Empty"}
```

Only observation is permitted in the request body.
Missing, invalid or additional fields return 422.
The server assigns submission time and acceptance order.

201, only after the report transaction commits:
```json
{
  "message": "Report accepted",
  "room_identifier": "DEMO-A-101",
  "accepted_report": {
    "observation": "Empty",
    "submission_time": "2026-11-23T18:40:00Z",
    "acceptance_order": 12
  },
  "occupancy": {
    "label": "Reported Empty",
    "latest_report_time": "2026-11-23T18:40:00Z",
    "expires_at": "2026-11-23T19:40:00Z",
    "remaining_seconds": 3600
  },
  "server_time": "2026-11-23T18:40:00Z"
}
```

remaining_seconds reflects actual response-time age and may be less than 3600.
accepted_report identifies the report accepted by this request.
occupancy reflects the latest accepted report retrieved for the response;
another concurrent submission may already be newer.

A missing catalog room returns 404.
A known storage failure returns 503 without a success acknowledgment.
A failed transaction does not replace a previously accepted report.

## 4. Error format

Application errors use:

```json
{
  "error": {
    "code": "ROOM_NOT_FOUND",
    "message": "The selected room does not exist."
  }
}
```

Codes:
- 404 ROOM_NOT_FOUND
- 422 VALIDATION_ERROR
- 503 STORAGE_UNAVAILABLE
- 500 INTERNAL_ERROR

Adam normalizes framework validation errors to this format.
Do not expose database details, credentials or stack traces.

If the browser loses the response, it must not claim that storage failed:
the report may already have committed. Show that the outcome could not
be confirmed and allow the user to check the room status.
Do not automatically retry a report submission.

## 5. Shared internal data structures

Define shared models in schemas.py:

RoomRecord:
- room_identifier: str
- building: str
- capacity: int
- amenities: list[str]

ReportRecord:
- room_identifier: str
- observation: Literal["Empty", "Occupied"]
- submission_time: timezone-aware datetime
- acceptance_order: int

OccupancyState:
- label: one of the three permitted display labels
- latest_report_time: timezone-aware datetime or None
- expires_at: timezone-aware datetime or None
- remaining_seconds: float

RoomView combines RoomRecord fields with occupancy: OccupancyState.

Internal timestamps remain datetime values.
API serialization converts them to UTC strings.

## 6. Component interfaces and ownership

Use synchronous service and repository functions for this initial implementation.
Database connections are scoped to operations or requests, never a shared
mutable global connection.

Roshan — repository.py:
- list_rooms() -> list[RoomRecord]
- get_room(room_identifier: str) -> RoomRecord | None
- get_latest_report(room_identifier: str) -> ReportRecord | None
- append_report(room_identifier: str, observation: str) -> ReportRecord

Raghameena — catalog.py:
- find_rooms(building: str | None = None,
             minimum_capacity: int | None = None,
             amenity: str | None = None) -> list[RoomRecord]
- find_room(room_identifier: str) -> RoomRecord | None

Catalog functions use the repository and return room records.
Adam combines records with occupancy for API responses.

Raghameena — status.py:
- derive_status(report: ReportRecord | None,
                now: datetime) -> OccupancyState

Status derivation is a pure calculation with no database calls.
An explicit now value makes boundary tests deterministic.

Adam — reporting.py:
- submit_report(room_identifier: str, observation: str) -> ReportRecord

Reporting coordinates validation and repository acceptance.
Adam owns API routes, shared schemas, response assembly and error mapping.

Tien owns browser rendering and API calls.
Malak owns shared test fixtures and API integration tests.

Shared exceptions belong in errors.py:
- RoomNotFoundError
- InvalidObservationError
- StorageUnavailableError

Coordinate interface changes in the relevant issue or PR before integration.

## 7. Acceptance and expiration rules

Latest means most recently accepted, not greatest client-supplied time.
No client-supplied timestamp or acceptance order is accepted.

Serialize acceptance for a room within the database transaction.
Assign submission time and order after acquiring the room’s serialization lock.
Return success only after commit.

An increasing acceptance_order determines latest-report precedence.
Gaps are acceptable; duplicate order values are not.
A database sequence alone does not establish commit order without serialization.

expires_at = submission_time + 60 minutes.
At now >= expires_at, the status is Unknown.
Missing reports also produce Unknown.
Expiration never deletes the report timestamp.

For each response, use one current-time value for server_time and all
status calculations in that response.

## 8. Browser expiration

Use server-supplied remaining_seconds, accounting for elapsed request and
view time, rather than trusting the browser's wall-clock date.

When remaining time reaches zero, display Unknown and retain the timestamp.
Recheck expiration when the page becomes visible again.
Clear obsolete timers when changing or closing a room view.

The baseline does not require push updates for other users’ submissions.

## 9. Review before integration

- Roshan checks storage models, acceptance ordering and repository signatures.
- Raghameena checks filtering and status interfaces.
- Tien checks whether responses support the required browser workflows.
- Malak checks that behavior and errors can be tested.

Record agreement or requested changes in the foundation PR.
This document remains proposed until that review occurs.