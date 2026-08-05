"""Utilities for lightweight transcript cleaning."""

from __future__ import annotations

import re


def clean_text(text: str) -> str:
    """Normalize transcript text without changing its meaning."""

    cleaned = text.strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"\s+([,.;!?])", r"\1", cleaned)

    return cleaned


def clean_speaker(speaker: str | None) -> str | None:
    """Normalize an optional speaker label."""

    if speaker is None:
        return None

    cleaned = re.sub(r"\s+", " ", speaker.strip())

    return cleaned or None
