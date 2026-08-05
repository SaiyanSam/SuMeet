"""Structured models for extracted meeting intelligence."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.models.transcript import TranscriptSegment


class EvidenceReference(BaseModel):
    """Grounding reference to an original transcript segment."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    segment_id: str = Field(min_length=1)
    timestamp: float | None = Field(default=None, ge=0)
    speaker: str | None = None
    text: str = Field(min_length=1)


class Topic(BaseModel):
    """A major topic discussed during the meeting."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    topic_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    start_time: float | None = Field(default=None, ge=0)
    end_time: float | None = Field(default=None, ge=0)
    evidence_segment_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_time_order(self) -> "Topic":
        if (
            self.start_time is not None
            and self.end_time is not None
            and self.end_time < self.start_time
        ):
            raise ValueError("topic end_time cannot be earlier than start_time")

        return self


class ActionItem(BaseModel):
    """A task assigned or proposed during the meeting."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    action_id: str = Field(min_length=1)
    task: str = Field(min_length=1)
    owner: str | None = None
    deadline_original: str | None = None
    deadline_normalized: str | None = None
    status: str = "Pending"
    timestamp: float | None = Field(default=None, ge=0)
    evidence: str = Field(min_length=1)
    evidence_segment_id: str = Field(min_length=1)
    confidence: float | None = Field(default=None, ge=0, le=1)


class Decision(BaseModel):
    """A decision made during the meeting."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    decision_id: str = Field(min_length=1)
    decision: str = Field(min_length=1)
    timestamp: float | None = Field(default=None, ge=0)
    evidence: str = Field(min_length=1)
    evidence_segment_id: str = Field(min_length=1)


class Blocker(BaseModel):
    """An unresolved issue, dependency, or project risk."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    blocker_id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    owner: str | None = None
    category: str | None = None
    timestamp: float | None = Field(default=None, ge=0)
    evidence: str = Field(min_length=1)
    evidence_segment_id: str = Field(min_length=1)


class MeetingRecord(BaseModel):
    """Complete structured representation of a processed meeting."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    meeting_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    language: str | None = None
    duration_seconds: float | None = Field(default=None, ge=0)
    participants: list[str] = Field(default_factory=list)

    one_line_summary: str | None = None
    executive_summary: str | None = None

    topics: list[Topic] = Field(default_factory=list)
    action_items: list[ActionItem] = Field(default_factory=list)
    decisions: list[Decision] = Field(default_factory=list)
    blockers: list[Blocker] = Field(default_factory=list)
    transcript_segments: list[TranscriptSegment] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_unique_record_ids(self) -> "MeetingRecord":
        collections = {
            "topic": [item.topic_id for item in self.topics],
            "action": [item.action_id for item in self.action_items],
            "decision": [item.decision_id for item in self.decisions],
            "blocker": [item.blocker_id for item in self.blockers],
        }

        for item_type, identifiers in collections.items():
            if len(identifiers) != len(set(identifiers)):
                raise ValueError(f"{item_type} IDs must be unique")

        return self
