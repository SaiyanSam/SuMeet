"""Pydantic models for meeting transcripts."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator


class TranscriptSegment(BaseModel):
    """A timestamped segment of a meeting transcript."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    segment_id: str = Field(
        min_length=1,
        description="Unique identifier for the transcript segment.",
    )
    start: float | None = Field(
        default=None,
        ge=0,
        description="Segment start time in seconds.",
    )
    end: float | None = Field(
        default=None,
        ge=0,
        description="Segment end time in seconds.",
    )
    speaker: str | None = Field(
        default=None,
        description="Speaker label, when available.",
    )
    text: str = Field(
        min_length=1,
        description="Transcript text for this segment.",
    )

    @model_validator(mode="after")
    def validate_timestamp_order(self) -> "TranscriptSegment":
        """Ensure that timestamps are either both present or both absent."""

        if (self.start is None) != (self.end is None):
            raise ValueError(
                "start and end must either both be provided or both be omitted"
            )

        if (
            self.start is not None
            and self.end is not None
            and self.end < self.start
        ):
            raise ValueError("end timestamp cannot be earlier than start")

        return self


class Transcript(BaseModel):
    """A validated transcript belonging to one meeting."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    meeting_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    language: str | None = None
    duration_seconds: float | None = Field(default=None, ge=0)
    segments: list[TranscriptSegment] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_segment_ids(self) -> "Transcript":
        """Reject transcripts containing duplicate segment IDs."""

        segment_ids = [segment.segment_id for segment in self.segments]

        if len(segment_ids) != len(set(segment_ids)):
            raise ValueError("segment IDs must be unique")

        return self

    @property
    def participants(self) -> list[str]:
        """Return unique known speakers in first-appearance order."""

        speakers: list[str] = []

        for segment in self.segments:
            if segment.speaker and segment.speaker not in speakers:
                speakers.append(segment.speaker)

        return speakers
