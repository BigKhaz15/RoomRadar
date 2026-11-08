#!/usr/bin/env python3
"""
S-01: Reporting Service Concurrency and Latency Spike
Addresses QAS-01: At least 95 of 100 student submissions visibly confirmed
within 3 seconds.

Fires 100 concurrent valid POST /api/reports requests and measures the
round-trip time from dispatch to acknowledgment for each.
"""

import asyncio
import time
import statistics
from dataclasses import dataclass, field

import aiohttp

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE_URL = "http://localhost:8000"
ENDPOINT = f"{BASE_URL}/api/reports"
CONCURRENCY = 100
THRESHOLD_SECONDS = 3.0
THRESHOLD_MS = THRESHOLD_SECONDS * 1000


# ---------------------------------------------------------------------------
# Result container
# ---------------------------------------------------------------------------
@dataclass
class RequestResult:
    index: int
    ok: bool
    status: int | None
    latency_ms: float
    error: str | None = None


@dataclass
class SpikeSummary:
    results: list[RequestResult] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def successes(self) -> int:
        return sum(1 for r in self.results if r.ok)

    @property
    def within_threshold(self) -> int:
        return sum(1 for r in self.results if r.ok and r.latency_ms <= THRESHOLD_MS)

    @property
    def failures(self) -> int:
        return sum(1 for r in self.results if not r.ok)

    @property
    def avg_latency_ms(self) -> float:
        latencies = [r.latency_ms for r in self.results if r.ok]
        return statistics.mean(latencies) if latencies else 0.0

    @property
    def p95_latency_ms(self) -> float:
        latencies = sorted(r.latency_ms for r in self.results if r.ok)
        if not latencies:
            return 0.0
        idx = int(round(0.95 * (len(latencies) - 1)))
        return latencies[idx]


# ---------------------------------------------------------------------------
# Payload builder — a valid report submission
# ---------------------------------------------------------------------------
def build_payload(index: int) -> dict:
    return {
        "student_id": f"student-{index:03d}",
        "assignment_id": "assignment-42",
        "report_content": f"Report submission #{index} — spike load test payload.",
        "submitted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


# ---------------------------------------------------------------------------
# Single request worker
# ---------------------------------------------------------------------------
async def submit_report(session: aiohttp.ClientSession, index: int) -> RequestResult:
    payload = build_payload(index)
    start = time.perf_counter()
    try:
        async with session.post(ENDPOINT, json=payload, timeout=THRESHOLD_SECONDS * 2) as resp:
            body = await resp.text()
            elapsed_ms = (time.perf_counter() - start) * 1000
            ok = resp.status in (200, 201) and bool(body)
            return RequestResult(
                index=index,
                ok=ok,
                status=resp.status,
                latency_ms=elapsed_ms,
                error=None if ok else f"status={resp.status}",
            )
    except Exception as exc:  # noqa: BLE001 — spike wants any failure recorded
        elapsed_ms = (time.perf_counter() - start) * 1000
        return RequestResult(
            index=index,
            ok=False,
            status=None,
            latency_ms=elapsed_ms,
            error=f"{type(exc).__name__}: {exc}",
        )


# ---------------------------------------------------------------------------
# Driver — fire all 100 concurrently, then summarize
# ---------------------------------------------------------------------------
async def run_spike() -> SpikeSummary:
    summary = SpikeSummary()
    connector = aiohttp.TCPConnector(limit=CONCURRENCY)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [submit_report(session, i) for i in range(1, CONCURRENCY + 1)]
        # asyncio.gather launches them all at once -> concurrent fire
        summary.results = await asyncio.gather(*tasks)
    return summary


def print_report(summary: SpikeSummary) -> None:
    pct_within = (summary.within_threshold / summary.total * 100) if summary.total else 0.0
    pct_failed = (summary.failures / summary.total * 100) if summary.total else 0.0

    print("=" * 60)
    print("S-01: Reporting Service Concurrency & Latency Spike")
    print("=" * 60)
    print(f"Total concurrent submissions:            {summary.total}")
    print(f"Submissions confirmed within 3 seconds:  {summary.within_threshold} "
          f"out of {summary.total} ({pct_within:.0f}%)")
    print(f"Average round-trip response time:        {summary.avg_latency_ms:.0f} ms")
    print(f"P95 round-trip response time:            {summary.p95_latency_ms:.0f} ms")
    print(f"Failed or timed-out submissions:         {pct_failed:.0f}%")
    print("-" * 60)
    passed = pct_within >= 95.0
    print(f"QAS-01 (95% within 3s): {'PASS' if passed else 'FAIL'}")
    print("=" * 60)

    if summary.failures:
        print("\nFailure detail:")
        for r in summary.results:
            if not r.ok:
                print(f"  #{r.index}: {r.error}")


if __name__ == "__main__":
    summary = asyncio.run(run_spike())
    print_report(summary)