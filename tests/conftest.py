"""Shared fixtures for RoomRadar integration testing."""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Provide a test client for the actual RoomRadar application."""
    from roomradar.main import app

    with TestClient(app) as test_client:
        yield test_client
