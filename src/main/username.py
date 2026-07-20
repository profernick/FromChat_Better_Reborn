"""Username lookup and uniqueness helpers."""

from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

from .models import User


def username_taken(db: Session, username: str, *, exclude_user_id: int | None = None) -> bool:
    """Return True if another account already uses this username (case-insensitive)."""
    query = db.query(User.id).filter(func.lower(User.username) == username.lower())
    if exclude_user_id is not None:
        query = query.filter(User.id != exclude_user_id)
    return query.first() is not None
