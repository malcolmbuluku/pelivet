"""Small shared helpers."""
from datetime import datetime, timezone


def utcnow() -> datetime:
    """Current UTC time as a naive datetime (replaces deprecated datetime.utcnow()).

    Kept naive to match how SQLite stores DateTime columns, so all comparisons stay consistent.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)
