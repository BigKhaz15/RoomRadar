# S-01: Anonymous report acceptance and expiration spike

## Question
Can a disposable local implementation persist 100 anonymous reports using ten concurrent request workers, maintain a unique acceptance order, reject invalid input, roll back a failed acceptance, and apply the 60-minute expiration rule?

## Decision and scope
Supports ADR-02/ADR-03 and FR-11/12/14/15. This is a Python-standard-library HTTP server plus a temporary SQLite repository, not the proposed FastAPI/PostgreSQL application. SQLite BEGIN IMMEDIATE serializes all writes; it is a surrogate for investigating the acceptance boundary. PostgreSQL per-room coordination must still be implemented and tested. Success is acknowledged only after commit.

## Reproduce
Requires Python 3.10 or later; no external dependencies.

From this directory run:

```bash
python spike.py
```

The command starts its own localhost server on a free port, creates a temporary database, sends 100 requests through ten worker threads, checks the persisted rows, runs additional correctness checks, writes results.json and shuts down. It exits nonzero if a correctness check fails. It overwrites results.json on rerun; timings will vary. To capture a new console summary use `python spike.py > execution_output.log`.

## Actual supplied execution
Executed by the AI assistant in its Linux environment at 2026-11-09 00:07 UTC (November 8, 6:07 PM Central). Python 3.12.14; SQLite 3.53.1. Files include original per-request measurements in results.json and the console summary in execution_output.log. These are not claimed as a teammate's independent execution or review.

- 100/100 HTTP submissions acknowledged and verified against committed database rows.
- 100 unique acceptance-order values.
- 100/100 HTTP acknowledgments within 3 seconds; mean 26.150 ms, nearest-rank p95 132.227 ms.
- All eight recorded correctness checks passed: persistence, unique ordering, rollback, invalid-input rejection, equal-timestamp precedence, status at 3599 seconds, status/timestamp at 3600 seconds, and no-report behavior.
- Three invalid submissions (extra student_id field, missing catalog room, invalid observation) were rejected without new rows.

## Interpretation and limitations
The local surrogate demonstrates a viable atomic acceptance boundary and deterministic expiration rules. It does NOT prove QAS-01: HTTP acknowledgment is not visible browser confirmation. There is no browser, public network, FastAPI, PostgreSQL, cloud host or UI timer in this test. The expiration checks supply test times directly, so they do not measure clock synchronization or browser suspension. Acceptance order means serialized commit order, not client response-arrival order.

## Contribution and repository handling
Prepared and executed with AI assistance during Adam's final integration; disclose this assistance in section 10.5. Preserve Roshan's original contribution in Git history and record why it was superseded (incompatible payload, missing reproducible backend, and unsupported UI-performance conclusion). Do not relabel this run as Roshan's execution.

Upload this directory to /spikes/S-01-report-acceptance/ and commit it before citing it as repository evidence. No repository upload or merge has been performed by the assistant.
