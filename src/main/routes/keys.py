from fastapi import APIRouter, HTTPException
import logging
import json

import httpx

from ..constants import MESSAGING_SERVICE_URL

router = APIRouter()
logger = logging.getLogger("uvicorn.error")


@router.get("/key/public")
async def get_public_key():
    """Return the current messaging service ephemeral public key."""
    url = f"{MESSAGING_SERVICE_URL.rstrip('/')}/key/public"
    try:
        try:
            resp = httpx.get(url, timeout=5.0)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            from urllib import request

            with request.urlopen(url, timeout=5) as r:
                return json.loads(r.read())
    except Exception as e:
        logger.error("Failed to fetch messaging public key via HTTP: %s", e)
        raise HTTPException(status_code=502, detail="Failed to contact messaging service")
