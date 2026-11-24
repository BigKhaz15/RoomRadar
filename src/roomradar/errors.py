"""Shared application errors.

API routes translate these exceptions into safe HTTP responses.
"""


class RoomNotFoundError(Exception):
    """The requested room does not exist in the catalog."""


class InvalidObservationError(Exception):
    """The observation is not Empty or Occupied."""


class StorageUnavailableError(Exception):
    """A database operation could not be completed."""