from fastapi import FastAPI

app = FastAPI(title="RoomRadar")


@app.get("/health")
def health_check() -> dict[str, str]:
    """Confirm that the API is running, not database readiness."""
    return {"status": "ok"}