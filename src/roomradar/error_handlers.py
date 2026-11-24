"""Translate application exceptions into safe API responses."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from roomradar.errors import (
    InvalidObservationError,
    RoomNotFoundError,
    StorageUnavailableError,
)


def error_response(status: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content={"error": {"code": code, "message": message}},
    )


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(RoomNotFoundError)
    async def room_not_found(
        request: Request, exc: RoomNotFoundError
    ) -> JSONResponse:
        return error_response(
            404, "ROOM_NOT_FOUND", "The selected room does not exist."
        )

    @app.exception_handler(InvalidObservationError)
    async def invalid_observation(
        request: Request, exc: InvalidObservationError
    ) -> JSONResponse:
        return error_response(
            422, "VALIDATION_ERROR", "Observation must be Empty or Occupied."
        )

    @app.exception_handler(RequestValidationError)
    async def invalid_request(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        # Do not echo submitted values or the request body.
        return error_response(
            422, "VALIDATION_ERROR", "The request contains invalid fields or values."
        )

    @app.exception_handler(StorageUnavailableError)
    async def storage_unavailable(
        request: Request, exc: StorageUnavailableError
    ) -> JSONResponse:
        return error_response(
            503, "STORAGE_UNAVAILABLE", "Storage is temporarily unavailable."
        )

    @app.exception_handler(Exception)
    async def internal_error(
        request: Request, exc: Exception
    ) -> JSONResponse:
        return error_response(
            500, "INTERNAL_ERROR", "An unexpected server error occurred."
        )