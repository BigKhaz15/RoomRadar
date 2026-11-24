"""Shared data models for RoomRadar services and API responses."""

from datetime import datetime, timezone
from typing import Annotated, Literal

from pydantic import (
    AfterValidator,
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
)


def normalize_utc(value: datetime) -> datetime:
    return value.astimezone(timezone.utc)


UtcTimestamp = Annotated[AwareDatetime, AfterValidator(normalize_utc)]
Observation = Literal["Empty", "Occupied"]
OccupancyLabel = Literal["Reported Empty", "Reported Occupied", "Unknown"]


class SharedModel(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class ReportSubmission(SharedModel):
    """The only permitted report input is its observation."""

    observation: Observation


class RoomRecord(SharedModel):
    room_identifier: str = Field(min_length=1)
    building: str = Field(min_length=1)
    capacity: int = Field(gt=0, strict=True)
    amenities: list[str]


class ReportRecord(SharedModel):
    room_identifier: str = Field(min_length=1)
    observation: Observation
    submission_time: UtcTimestamp
    acceptance_order: int = Field(gt=0, strict=True)


class OccupancyState(SharedModel):
    label: OccupancyLabel
    latest_report_time: UtcTimestamp | None
    expires_at: UtcTimestamp | None
    remaining_seconds: float = Field(ge=0)


class RoomView(RoomRecord):
    occupancy: OccupancyState


class RoomListResponse(SharedModel):
    rooms: list[RoomView]
    server_time: UtcTimestamp


class RoomDetailResponse(SharedModel):
    room: RoomView
    server_time: UtcTimestamp


class OccupancyResponse(SharedModel):
    room_identifier: str
    occupancy: OccupancyState
    server_time: UtcTimestamp


class AcceptedReport(SharedModel):
    observation: Observation
    submission_time: UtcTimestamp
    acceptance_order: int = Field(gt=0, strict=True)


class ReportAcceptedResponse(SharedModel):
    message: Literal["Report accepted"] = "Report accepted"
    room_identifier: str
    accepted_report: AcceptedReport
    occupancy: OccupancyState
    server_time: UtcTimestamp


class ErrorDetail(SharedModel):
    code: Literal[
        "ROOM_NOT_FOUND",
        "VALIDATION_ERROR",
        "STORAGE_UNAVAILABLE",
        "INTERNAL_ERROR",
    ]
    message: str


class ErrorResponse(SharedModel):
    error: ErrorDetail