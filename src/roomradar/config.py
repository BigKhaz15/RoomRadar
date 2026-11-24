import os


def get_database_url() -> str:
    """Read database configuration when a database operation needs it."""
    value = os.environ.get("DATABASE_URL", "").strip()

    if not value:
        raise RuntimeError(
            "DATABASE_URL is not configured. See docs/p3/setup.md."
        )

    return value