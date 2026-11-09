# S-01: Reporting Service Concurrency and Latency Spike

**Risk or decision addressed:** Addresses QAS-01 (At least 95 of 100 student
submissions visibly confirmed within 3 seconds) and the architectural choice
of a single deployable backend handling asynchronous report storage.

**Question (answerable yes/no):** Can the reporting service endpoint
successfully store and acknowledge 100 concurrent valid report submissions
within the 3-second window with a 95%+ success rate?

**Set-up:** Isolated benchmark script (`spike_qas01.py`) that simultaneously
fires 100 HTTP POST requests containing valid report payloads against the
local `/api/reports` endpoint.

**How measured:** Round-trip response time per request from client dispatch
to acknowledgment; counted successes within the 3-second threshold.

**Result:**
| Metric | Value |
|---|---|
| Total concurrent submissions | 100 |
| Confirmed within 3 seconds | 98 / 100 (98%) |
| Average round-trip | 420 ms |
| Failed or timed-out | 0% |

**What it changed/confirmed:** Confirmed the current backend repository
boundary and DB write configuration meet QAS-01 without a separate message
queue or microservice layer.

**Where to see it:** `spike_qas01.py` and `execution_output.log` in this folder.

## How to reproduce
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# start backend on localhost:8000, then:
python spike_qas01.py | tee execution_output.log
