"""Release Yandex IDs from soft-deleted accounts after a hold period."""

from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from .models import User
from .security.audit import log_security

logger = logging.getLogger("uvicorn.error")


def yandex_id_hold_days() -> int:
    raw = (os.getenv("YANDEX_ID_HOLD_DAYS") or "3").strip()
    try:
        days = int(raw)
    except ValueError as exc:
        raise SystemExit(f"Invalid YANDEX_ID_HOLD_DAYS={os.getenv('YANDEX_ID_HOLD_DAYS')!r}") from exc
    if days < 0:
        raise SystemExit(f"YANDEX_ID_HOLD_DAYS must be >= 0, got {days}")
    return days


def release_expired_yandex_ids(db: Session) -> int:
    """
    Clear yandex_id on deleted users whose deleted_at is older than the hold.
    Legacy rows with deleted=True and deleted_at NULL are released immediately.
    Returns the number of rows updated.
    """
    hold = yandex_id_hold_days()
    cutoff = datetime.now(timezone.utc) - timedelta(days=hold)
    rows = (
        db.query(User)
        .filter(
            User.deleted.is_(True),
            User.yandex_id.isnot(None),
        )
        .filter(
            (User.deleted_at.is_(None)) | (User.deleted_at < cutoff),
        )
        .all()
    )
    if not rows:
        return 0
    for user in rows:
        previous = user.yandex_id
        user.yandex_id = None
        log_security(
            "yandex_id_released",
            severity="info",
            user_id=user.id,
            username=user.username,
            previous_yandex_id=previous,
            hold_days=hold,
        )
    db.commit()
    logger.info("Released yandex_id for %s deleted user(s) (hold_days=%s)", len(rows), hold)
    return len(rows)
