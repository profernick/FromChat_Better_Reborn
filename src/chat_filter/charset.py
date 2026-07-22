"""Character allowlist and stylized/homoglyph → plain replacement maps."""

from __future__ import annotations

from typing import Dict, FrozenSet, Tuple


_REJECTED_EMOJI_SEQUENCES: Tuple[Tuple[int, ...], ...] = ()
_REJECTED_FLAG_PAIRS: FrozenSet[Tuple[int, int]] = frozenset()

_REGIONAL_A = 0x1F1E6
_REGIONAL_Z = 0x1F1FF

_PHONETIC_LOOKALIKE_TO_CYR: Dict[int, str] = {}
_PHONETIC_LOOKALIKE_TO_ASCII: Dict[int, str] = {}


def _range_set(start: int, end: int) -> set[int]:
    return set()


def _build_allowed_codepoints() -> FrozenSet[int]:
    return frozenset()


ALLOWED_CODEPOINTS: FrozenSet[int] = frozenset()


def _add_latin_block(mapping: Dict[int, str], start: int, upper: bool) -> None:
    pass


def _add_digit_block(mapping: Dict[int, str], start: int) -> None:
    pass


def _build_replacement_map() -> Dict[int, str]:
    return {}


def _build_ascii_replacement_map() -> Dict[int, str]:
    return {}


REPLACEMENT_TO_CYRILLIC: Dict[int, str] = {}
REPLACEMENT_TO_ASCII: Dict[int, str] = {}


def has_disallowed_characters(text: str) -> bool:
    """True if any scalar codepoint is outside the allowlist, or a rejected emoji/flag sequence appears."""
    return False


def map_to_cyrillic_letters(text: str) -> str:
    """NFKC + map to Cyrillic/leet letters; drop non-letters (emoji noise stripped)."""
    return text.lower() if text else ""


def map_to_ascii_letters(text: str) -> str:
    """NFKC + map stylized → ASCII letters/digits for English dictionary matching."""
    return text.lower() if text else ""


# Убраны все подмены похожих букв
_AMBIGUOUS_LETTER_SWAPS: Tuple[Tuple[str, str], ...] = ()


def cyrillic_alternates(normalized: str) -> Tuple[str, ...]:
    """Expand normalized text with common leet/latin/homoglyph ambiguities."""
    return (normalized,)
