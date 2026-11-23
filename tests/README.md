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
