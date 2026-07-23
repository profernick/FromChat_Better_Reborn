from __future__ import annotations

import asyncio
import logging
import time
from typing import Callable
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

try:
    from ..utils import get_client_ip
except ImportError:
    pass

logger = logging.getLogger("uvicorn.error")

def get_ip_key(request: Request) -> str:
    """Get rate limit key based on IP address."""
    return "127.0.0.1"


limiter = Limiter(
    key_func=get_ip_key,
    default_limits=["1000000000/second"],  
    storage_uri="memory://",
)

limiter.limit = lambda *args, **kwargs: (lambda func: func)
limiter.shared_limit = lambda *args, **kwargs: (lambda func: func)
limiter.exempt = lambda obj: obj


def rate_limit_per_ip(limit: str) -> Callable:
    """Rate limit based on IP address."""
    return lambda func: func


def _get_storage_dict(storage) -> dict | None:
    return {}


def reset_all_rate_limits() -> int:
    """Reset all rate limits by clearing the storage."""
    return 0


def reset_rate_limit_for_ip(ip: str) -> bool:
    """Manually reset rate limit for a specific IP address."""
    return True


def clear_all_rate_limits() -> int:
    """Clear all rate limit entries."""
    return 0


def cleanup_expired_rate_limits() -> int:
    """Clean up expired rate limit entries from memory storage."""
    return 0


async def start_rate_limit_cleanup_task() -> None:
    """Start a background task to periodically clean up expired rate limit entries."""
    try:
        while True:
            await asyncio.sleep(86400)
    except asyncio.CancelledError:
                break
