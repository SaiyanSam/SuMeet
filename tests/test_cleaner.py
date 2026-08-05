"""Tests for transcript cleaning utilities."""

from src.ingestion.transcript_cleaner import clean_speaker, clean_text


def test_clean_text_normalizes_whitespace() -> None:
    assert clean_text("  Hello    everyone.  ") == "Hello everyone."


def test_clean_text_removes_space_before_punctuation() -> None:
    assert clean_text("Testing is complete  .") == "Testing is complete."


def test_clean_speaker_normalizes_whitespace() -> None:
    assert clean_speaker("  Alice   Smith  ") == "Alice Smith"


def test_clean_speaker_handles_missing_value() -> None:
    assert clean_speaker(None) is None


def test_clean_speaker_handles_empty_value() -> None:
    assert clean_speaker("   ") is None
