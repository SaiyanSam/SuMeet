"""Parse plain-text meeting transcripts into validated models."""

from __future__ import annotations

import re
from pathlib import Path

from src.ingestion.transcript_cleaner import clean_speaker, clean_text
from src.models.transcript import Transcript, TranscriptSegment


TIMESTAMP_PATTERN = re.compile(
    r"^\[(?P<timestamp>\d{1,2}:\d{2}(?::\d{2})?)\]\s*"
)

SPEAKER_PATTERN = re.compile(
    r"^(?P<speaker>[^:]{1,100}):\s*(?P<text>.+)$"
)


def timestamp_to_seconds(timestamp: str) -> float:
    """Convert MM:SS or HH:MM:SS into seconds."""

    parts = [int(part) for part in timestamp.split(":")]

    if len(parts) == 2:
        minutes, seconds = parts
        return float(minutes * 60 + seconds)

    if len(parts) == 3:
        hours, minutes, seconds = parts
        return float(hours * 3600 + minutes * 60 + seconds)

    raise ValueError(f"Unsupported timestamp format: {timestamp}")


def parse_transcript_line(
    line: str,
) -> tuple[float | None, str | None, str] | None:
    """Parse one transcript line."""

    line = line.strip()

    if not line:
        return None

    start: float | None = None

    timestamp_match = TIMESTAMP_PATTERN.match(line)
    if timestamp_match:
        start = timestamp_to_seconds(timestamp_match.group("timestamp"))
        line = line[timestamp_match.end():].strip()

    speaker: str | None = None
    text = line

    speaker_match = SPEAKER_PATTERN.match(line)
    if speaker_match:
        speaker = clean_speaker(speaker_match.group("speaker"))
        text = speaker_match.group("text")

    text = clean_text(text)

    if not text:
        return None

    return start, speaker, text


def parse_transcript_text(
    raw_text: str,
    meeting_id: str,
    title: str,
    language: str | None = None,
) -> Transcript:
    """Parse transcript text into a validated Transcript."""

    parsed_rows: list[tuple[float | None, str | None, str]] = []

    for line in raw_text.splitlines():
        parsed = parse_transcript_line(line)

        if parsed is not None:
            parsed_rows.append(parsed)

    if not parsed_rows:
        raise ValueError("Transcript did not contain any valid segments")

    segments: list[TranscriptSegment] = []

    for index, (start, speaker, text) in enumerate(parsed_rows):
        next_start = (
            parsed_rows[index + 1][0]
            if index + 1 < len(parsed_rows)
            else None
        )

        end: float | None = None

        if start is not None and next_start is not None:
            if next_start < start:
                raise ValueError(
                    "Transcript timestamps must be in non-decreasing order"
                )
            end = next_start
        elif start is not None:
            end = start

        segments.append(
            TranscriptSegment(
                segment_id=f"seg_{index + 1:04d}",
                start=start,
                end=end,
                speaker=speaker,
                text=text,
            )
        )

    duration_seconds = max(
        (
            segment.end
            for segment in segments
            if segment.end is not None
        ),
        default=None,
    )

    return Transcript(
        meeting_id=meeting_id,
        title=title,
        language=language,
        duration_seconds=duration_seconds,
        segments=segments,
    )


def parse_transcript_file(
    file_path: str | Path,
    meeting_id: str,
    title: str,
    language: str | None = None,
) -> Transcript:
    """Load and parse a UTF-8 text transcript."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Transcript file not found: {path}")

    if not path.is_file():
        raise ValueError(f"Transcript path is not a file: {path}")

    raw_text = path.read_text(encoding="utf-8")

    return parse_transcript_text(
        raw_text=raw_text,
        meeting_id=meeting_id,
        title=title,
        language=language,
    )
