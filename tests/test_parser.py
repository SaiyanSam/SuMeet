"""Tests for transcript parsing."""

import pytest

from src.ingestion.transcript_parser import (
    parse_transcript_line,
    parse_transcript_text,
    timestamp_to_seconds,
)


def test_timestamp_to_seconds_mm_ss() -> None:
    assert timestamp_to_seconds("02:15") == 135.0


def test_timestamp_to_seconds_hh_mm_ss() -> None:
    assert timestamp_to_seconds("01:02:03") == 3723.0


def test_parse_timestamped_speaker_line() -> None:
    parsed = parse_transcript_line(
        "[00:05] Bob: I will complete backend testing."
    )

    assert parsed == (
        5.0,
        "Bob",
        "I will complete backend testing.",
    )


def test_parse_speaker_line_without_timestamp() -> None:
    parsed = parse_transcript_line("Alice: Welcome everyone.")

    assert parsed == (
        None,
        "Alice",
        "Welcome everyone.",
    )


def test_parse_plain_line() -> None:
    parsed = parse_transcript_line("General discussion begins.")

    assert parsed == (
        None,
        None,
        "General discussion begins.",
    )


def test_parse_transcript_text() -> None:
    transcript = parse_transcript_text(
        raw_text=(
            "[00:00] Alice: Welcome everyone.\n"
            "[00:05] Bob: I will finish testing.\n"
            "[00:12] Alice: Let us release on Friday."
        ),
        meeting_id="meeting_001",
        title="Weekly Review",
        language="en",
    )

    assert len(transcript.segments) == 3
    assert transcript.segments[0].start == 0.0
    assert transcript.segments[0].end == 5.0
    assert transcript.segments[1].start == 5.0
    assert transcript.segments[1].end == 12.0
    assert transcript.segments[2].start == 12.0
    assert transcript.segments[2].end == 12.0
    assert transcript.participants == ["Alice", "Bob"]
    assert transcript.duration_seconds == 12.0


def test_empty_transcript_is_rejected() -> None:
    with pytest.raises(ValueError):
        parse_transcript_text(
            raw_text="\n\n",
            meeting_id="meeting_001",
            title="Empty Meeting",
        )


def test_decreasing_timestamps_are_rejected() -> None:
    with pytest.raises(ValueError):
        parse_transcript_text(
            raw_text=(
                "[00:10] Alice: First statement.\n"
                "[00:05] Bob: Second statement."
            ),
            meeting_id="meeting_001",
            title="Invalid Meeting",
        )
