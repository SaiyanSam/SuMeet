"""Validated models for agent tool selection and execution."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


ToolName = Literal[
    "transcribe_audio",
    "summarize_meeting",
    "extract_action_items",
    "extract_decisions",
    "extract_blockers",
    "search_transcript",
    "create_action_dataframe",
    "plot_meeting_data",
]


class ToolCall(BaseModel):
    """A tool request selected by the meeting agent."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    name: ToolName
    arguments: dict[str, Any] = Field(default_factory=dict)


class MeetingToolInput(BaseModel):
    """Common input for tools operating on one meeting."""

    model_config = ConfigDict(extra="forbid")

    meeting_id: str = Field(min_length=1)


class SummarizeMeetingInput(MeetingToolInput):
    """Input for the meeting summarization tool."""

    summary_type: Literal["one_line", "executive", "detailed"] = "executive"
    include_topics: bool = True
    include_decisions: bool = True


class ExtractActionItemsInput(MeetingToolInput):
    """Input for action-item extraction."""

    include_unassigned: bool = True


class SearchTranscriptInput(MeetingToolInput):
    """Input for semantic transcript search."""

    query: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)
