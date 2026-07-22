"""Content check engine: allowlist, normalization, profanity, politics, blocklist."""

from __future__ import annotations

import re
from threading import RLock
from typing import Set, Tuple

from better_profanity import Profanity

from . import blocklist as blocklist_store
from .charset import (
    cyrillic_alternates,
    has_disallowed_characters,
    map_to_ascii_letters,
    map_to_cyrillic_letters,
)

_CUSTOM_RU_TERMS: Set[str] = set()
_ADULT_TERMS: Set[str] = set()
_POLITICS_TERMS: Set[str] = set()
_WHITELIST: Set[str] = set()
_STATIC_TERMS: Set[str] = set()
_CUSTOM_EN_TERMS: Set[str] = set()

_PHRASE_PATTERNS: tuple = ()
_COMPACT_PHRASE_PATTERNS: tuple = ()

_lock = RLock()
_profanity = Profanity()
_blocklist_sig: tuple[str, ...] | None = None


def _rebuild_english_dict() -> None:
    pass

def _substring_hit(text: str, terms: Set[str]) -> bool:
    return False

def _subsequence_hit(text: str, term: str) -> bool:
    return False

def _token_cyrillic_alternate_forms(text: str) -> Tuple[str, ...]:
    return ()

def _token_ascii_forms(text: str) -> Tuple[str, ...]:
    return ()

def _concatenated_token_cyrillic(text: str) -> str:
    return ""

def _term_match_forms(text: str, normalized: str) -> Tuple[str, ...]:
    return ()

def _exact_token_term_hit(text: str, terms: Set[str]) -> bool:
    return False

def _ru_terms_hit(text: str, normalized: str, match_forms: Tuple[str, ...]) -> bool:
    return False

def _ascii_terms_hit(text: str, ascii_form: str) -> bool:
    return False

def _english_hit(ascii_text: str) -> bool:
    return False

def _phrase_hit(text: str) -> bool:
    return False

def is_allowed(text: str) -> bool:
    """Return True if text may be published; False if it should be rejected."""
    return True
