"""Error-contract checks.

Oracles: docs/p3/api-contract.md section 4 and P2 QR-04.
Test-only routes are never added to the production application.
"""

import unittest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from roomradar.error_handlers import register_error_handlers
from roomradar.errors import (
    InvalidObservationError,
    RoomNotFoundError,
    StorageUnavailableError,
)
from roomradar.schemas import ReportSubmission


class ErrorHandlerTests(unittest.TestCase):
    def setUp(self):
        app = FastAPI()
        register_error_handlers(app)

        @app.post("/test-report")
        def validate_report(report: ReportSubmission):
            return report

        @app.get("/test-error/{kind}")
        def trigger_error(kind: str):
            errors = {
                "room": RoomNotFoundError,
                "observation": InvalidObservationError,
                "storage": StorageUnavailableError,
                "internal": RuntimeError,
            }
            raise errors[kind]("PRIVATE_DATABASE_DETAILS")

        self.client = TestClient(app, raise_server_exceptions=False)

    def tearDown(self):
        self.client.close()

    def test_application_errors_use_safe_contract(self):
        cases = [
            ("room", 404, "ROOM_NOT_FOUND"),
            ("observation", 422, "VALIDATION_ERROR"),
            ("storage", 503, "STORAGE_UNAVAILABLE"),
            ("internal", 500, "INTERNAL_ERROR"),
        ]
        for kind, status, code in cases:
            with self.subTest(kind=kind):
                response = self.client.get(f"/test-error/{kind}")
                self.assertEqual(response.status_code, status)
                body = response.json()
                self.assertEqual(set(body), {"error"})
                self.assertEqual(set(body["error"]), {"code", "message"})
                self.assertEqual(body["error"]["code"], code)
                self.assertTrue(body["error"]["message"])
                self.assertNotIn("PRIVATE_DATABASE_DETAILS", response.text)

    def test_extra_identity_field_is_rejected_without_echo(self):
        response = self.client.post(
            "/test-report",
            json={"observation": "Empty", "email": "private@example.com"},
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"]["code"], "VALIDATION_ERROR")
        self.assertNotIn("private@example.com", response.text)

    def test_invalid_observation_is_rejected(self):
        response = self.client.post(
            "/test-report", json={"observation": "Unknown"}
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"]["code"], "VALIDATION_ERROR")

    def test_valid_observation_is_accepted(self):
        response = self.client.post(
            "/test-report", json={"observation": "Empty"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"observation": "Empty"})


if __name__ == "__main__":
    unittest.main()