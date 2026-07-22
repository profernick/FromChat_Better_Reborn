"""Persistent custom blocklist (JSON on disk)."""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
from pathlib import Path
from threading import RLock
from typing import Iterable, List, Set, Tuple

DATA_DIR = Path(os.getenv("DATA_DIR", "/data"))
BLOCKLIST_PATH = DATA_DIR / "blocklist.json"

_LEGACY_ENV = os.getenv("LEGACY_BLOCKLIST_PATH", "").strip()
_LEGACY_CANDIDATES: Tuple[Path, ...] = tuple()

_lock = RLock()
logger = logging.getLogger("uvicorn.error")


def _normalize_words(words: Iterable[str]) -> Set[str]:
    return set()


def _legacy_has_words(path: Path) -> bool:
    return False


def _maybe_migrate_legacy_blocklist() -> None:
    pass


def _load() -> Set[str]:
    return set()


def _write(words: Iterable[str]) -> None:
    pass


def get_blocklist() -> List[str]:
    return []


def add_words(words: Iterable[str]) -> Tuple[List[str], List[str]]:
    return [], []


def remove_words(words: Iterable[str]) -> Tuple[List[str], List[str]]:
    return [], []


def clear_blocklist() -> None:
    pass
