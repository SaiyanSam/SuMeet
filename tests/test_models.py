"""Tests for SuMeet transcript models."""

import pytest
from pydantic import ValidationError

from src.models.transcript import Transcript, TranscriptSegment


def test_valid_transcript_segment() -> None:
    segment = TranscriptSegment(
        segment_id="seg_0001",
        start=0.0,
        end=5.0,
        speaker="Alice",
        text="Welcome everyone.",
    )

    assert segment.segment_id == "seg_0001"
    assert segment.start == 0.0
    assert segment.end == 5.0
    assert segment.speaker == "Alice"
    assert segment.text == "Welcome everyone."


def test_segment_without_timestamps_is_valid() -> None:
    segment = TranscriptSegment(
        segment_id="seg_0001",
        speaker="Alice",
        text="Welcome everyone.",
    )

    assert segment.start is None
    assert segment.end is None


def test_segment_rejects_incomplete_timestamp_pair() -> None:
    with pytest.raises(ValidationError):
        TranscriptSegment(
            segment_id="seg_0001",
            start=0.0,
            speaker="Alice",
            text="Welcome everyone.",
        )


def test_segment_rejects_reversed_timestamps() -> None:
    with pytest.raises(ValidationError):
        TranscriptSegment(
            segment_id="seg_0001",
            start=8.0,
            end=5.0,
            speaker="Alice",
            text="Welcome everyone.",
        )


def test_segment_rejects_empty_text() -> None:
    with pytest.raises(ValidationError):
        TranscriptSegment(
            segment_id="seg_0001",
            text="",
        )


def test_transcript_extracts_participants() -> None:
    transcript = Transcript(
        meeting_id="meeting_001",
        title="Weekly Review",
        duration_seconds=12.0,
        segments=[
            TranscriptSegment(
                segment_id="seg_0001",
                start=0.0,
                end=5.0,
                speaker="Alice",
                text="Welcome everyone.",
            ),
            TranscriptSegment(
                segment_id="seg_0002",
                start=5.0,
                end=12.0,
                speaker="Bob",
                text="I will complete testing.",
            ),
            TranscriptSegment(
                segment_id="seg_0003",
                speaker="Alice",
                text="Thanks.",
            ),
        ],
    )

    assert transcript.participants == ["Alice", "Bob"]


def test_transcript_rejects_duplicate_segment_ids() -> None:
    with pytest.raises(ValidationError):
        Transcript(
            meeting_id="meeting_001",
            title="Weekly Review",
            segments=[
                TranscriptSegment(
                    segment_id="seg_0001",
                    text="First statement.",
                ),
                TranscriptSegment(
                    segment_id="seg_0001",
                    text="Second statement.",
                ),
            ],
        )
        
        
from src.models.meeting import (
    ActionItem,
    Decision,
    MeetingRecord,
    Topic,
)
from src.models.tool_calls import SearchTranscriptInput, ToolCall


def test_valid_action_item() -> None:
    action = ActionItem(
        action_id="action_001",
        task="Complete backend testing",
        owner="Bob",
        deadline_original="Thursday",
        timestamp=5.0,
        evidence="I will complete backend testing by Thursday.",
        evidence_segment_id="seg_0002",
        confidence=0.9,
    )

    assert action.owner == "Bob"
    assert action.deadline_original == "Thursday"


def test_action_item_rejects_invalid_confidence() -> None:
    with pytest.raises(ValidationError):
        ActionItem(
            action_id="action_001",
            task="Complete backend testing",
            timestamp=5.0,
            evidence="I will complete backend testing.",
            evidence_segment_id="seg_0002",
            confidence=1.5,
        )


def test_topic_rejects_reversed_timestamps() -> None:
    with pytest.raises(ValidationError):
        Topic(
            topic_id="topic_001",
            title="Deployment",
            summary="The team discussed deployment.",
            start_time=20.0,
            end_time=10.0,
        )


def test_valid_meeting_record() -> None:
    record = MeetingRecord(
        meeting_id="meeting_001",
        title="Weekly Review",
        participants=["Alice", "Bob"],
        one_line_summary="The team reviewed release progress.",
        action_items=[
            ActionItem(
                action_id="action_001",
                task="Complete backend testing",
                owner="Bob",
                timestamp=5.0,
                evidence="I will complete backend testing by Thursday.",
                evidence_segment_id="seg_0002",
            )
        ],
        decisions=[
            Decision(
                decision_id="decision_001",
                decision="Move the release to Friday.",
                timestamp=12.0,
                evidence="Let's move the release to Friday.",
                evidence_segment_id="seg_0003",
            )
        ],
    )

    assert len(record.action_items) == 1
    assert len(record.decisions) == 1


def test_meeting_record_rejects_duplicate_action_ids() -> None:
    repeated_action = ActionItem(
        action_id="action_001",
        task="Complete backend testing",
        timestamp=5.0,
        evidence="I will complete backend testing.",
        evidence_segment_id="seg_0002",
    )

    with pytest.raises(ValidationError):
        MeetingRecord(
            meeting_id="meeting_001",
            title="Weekly Review",
            action_items=[repeated_action, repeated_action],
        )


def test_valid_tool_call() -> None:
    call = ToolCall(
        name="search_transcript",
        arguments={
            "meeting_id": "meeting_001",
            "query": "deployment",
            "top_k": 5,
        },
    )

    assert call.name == "search_transcript"


def test_tool_call_rejects_unknown_tool() -> None:
    with pytest.raises(ValidationError):
        ToolCall(
            name="delete_everything",
            arguments={},
        )


def test_search_input_restricts_top_k() -> None:
    with pytest.raises(ValidationError):
        SearchTranscriptInput(
            meeting_id="meeting_001",
            query="deployment",
            top_k=100,
        )
