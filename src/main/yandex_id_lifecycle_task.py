"""Periodic release of Yandex IDs held on soft-deleted accounts."""

from __future__ import annotations

import asyncio
import logging

from .db import SessionLocal
from .yandex_id_lifecycle import release_expired_yandex_ids

logger = logging.getLogger("uvicorn.error")

# Check often enough that a 3-day hold is accurate within ~15 minutes.
YANDEX_ID_RELEASE_POLL_SECONDS = 15 * 60


async def start_yandex_id_release_task(interval_seconds: int = YANDEX_ID_RELEASE_POLL_SECONDS) -> None:
    while True:
        try:
            with SessionLocal() as db:
                release_expired_yandex_ids(db)
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error("Error in yandex id release task: %s", e)
            try:
                await asyncio.sleep(60)
            except asyncio.CancelledError:
                break
            continue
        try:
            await asyncio.sleep(interval_seconds)
        except asyncio.CancelledError:
            break
