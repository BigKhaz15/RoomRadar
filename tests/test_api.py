"""RoomRadar API integration tests."""


def test_api_001_health_endpoint(client):
    """Oracle: API contract section 3, GET /health."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_api_002_homepage(client):
    """Oracle: P3 setup guide, starter page availability."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "RoomRadar" in response.text


def test_api_003_openapi_schema(client):
    """Oracle: P3 setup guide and API contract section 3."""
    response = client.get("/openapi.json")

    assert response.status_code == 200

    schema = response.json()

    assert schema["info"]["title"] == "RoomRadar"
    assert "/health" in schema["paths"]
    assert "get" in schema["paths"]["/health"]
