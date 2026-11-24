from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from roomradar.error_handlers import register_error_handlers

STATIC_DIR = Path(__file__).resolve().parent / "static"

app = FastAPI(title="RoomRadar")
register_error_handlers(app)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=FileResponse, include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health_check() -> dict[str, str]:
    """Confirm that the API is running, not database readiness."""
    return {"status": "ok"}