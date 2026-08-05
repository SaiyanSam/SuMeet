"""Tests for audio transcription without loading Whisper."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest

from src.transcription.transcriber import (
    TranscriptionError,
    transcribe_audio,
)
from src.transcription.whisper_client import (
    WhisperConfig,
    resolve_compute_type,
)


@dataclass
class FakeSegment:
    start: float
    end: float
    text: str


@dataclass
class FakeInfo:
    language: str
    duration: float


class FakeWhisperModel:
    def __init__(
        self,
        segments: list[FakeSegment],
        info: FakeInfo,
    ) -> None:
        self.segments = segments
        self.info = info
        self.received_audio: str | None = None
        self.received_kwargs: dict | None = None

    def transcribe(self, audio: str, **kwargs):
        self.received_audio = audio
        self.received_kwargs = kwargs
        return iter(self.segments), self.info


class FailingWhisperModel:
    def transcribe(self, audio: str, **kwargs):
        raise RuntimeError("decoder failure")


def create_mock_audio(tmp_path: Path) -> Path:
    audio_path = tmp_path / "meeting.wav"
    audio_path.write_bytes(b"mock audio content")
    return audio_path


def test_resolve_compute_type_for_cpu() -> None:
    config = WhisperConfig(device="cpu")

    assert resolve_compute_type(config) == "int8"


def test_resolve_compute_type_for_cuda() -> None:
    config = WhisperConfig(device="cuda")

    assert resolve_compute_type(config) == "float16"


def test_explicit_compute_type_is_preserved() -> None:
    config = WhisperConfig(
        device="cpu",
        compute_type="float32",
    )

    assert resolve_compute_type(config) == "float32"


def test_transcribe_audio_returns_valid_transcript(
    tmp_path: Path,
) -> None:
    audio_path = create_mock_audio(tmp_path)

    fake_model = FakeWhisperModel(
        segments=[
            FakeSegment(
                start=0.0,
                end=4.5,
                text=" Welcome everyone. ",
            ),
            FakeSegment(
                start=4.5,
                end=10.0,
                text="I will complete testing.",
            ),
        ],
        info=FakeInfo(
            language="en",
            duration=10.0,
        ),
    )

    transcript = transcribe_audio(
        audio_path=audio_path,
        meeting_id="meeting_001",
        title="Weekly Review",
        config=WhisperConfig(
            model_size="base.en",
            device="cpu",
            language="en",
        ),
        model=fake_model,
    )

    assert transcript.meeting_id == "meeting_001"
    assert transcript.title == "Weekly Review"
    assert transcript.language == "en"
    assert transcript.duration_seconds == 10.0
    assert len(transcript.segments) == 2

    assert transcript.segments[0].segment_id == "seg_0001"
    assert transcript.segments[0].start == 0.0
    assert transcript.segments[0].end == 4.5
    assert transcript.segments[0].text == "Welcome everyone."
    assert transcript.segments[0].speaker is None

    assert fake_model.received_audio == str(audio_path.resolve())
    assert fake_model.received_kwargs == {
        "language": "en",
        "beam_size": 5,
        "vad_filter": True,
    }


def test_empty_whisper_segments_are_skipped(
    tmp_path: Path,
) -> None:
    audio_path = create_mock_audio(tmp_path)

    fake_model = FakeWhisperModel(
        segments=[
            FakeSegment(start=0.0, end=1.0, text="   "),
            FakeSegment(start=1.0, end=3.0, text="Valid speech."),
        ],
        info=FakeInfo(
            language="en",
            duration=3.0,
        ),
    )

    transcript = transcribe_audio(
        audio_path=audio_path,
        meeting_id="meeting_001",
        title="Weekly Review",
        model=fake_model,
    )

    assert len(transcript.segments) == 1
    assert transcript.segments[0].segment_id == "seg_0001"
    assert transcript.segments[0].text == "Valid speech."


def test_no_valid_segments_raises_error(
    tmp_path: Path,
) -> None:
    audio_path = create_mock_audio(tmp_path)

    fake_model = FakeWhisperModel(
        segments=[
            FakeSegment(start=0.0, end=1.0, text=" "),
        ],
        info=FakeInfo(
            language="en",
            duration=1.0,
        ),
    )

    with pytest.raises(
        TranscriptionError,
        match="no non-empty transcript segments",
    ):
        transcribe_audio(
            audio_path=audio_path,
            meeting_id="meeting_001",
            title="Weekly Review",
            model=fake_model,
        )


def test_model_failure_is_wrapped(
    tmp_path: Path,
) -> None:
    audio_path = create_mock_audio(tmp_path)

    with pytest.raises(
        TranscriptionError,
        match="Failed to transcribe audio file",
    ):
        transcribe_audio(
            audio_path=audio_path,
            meeting_id="meeting_001",
            title="Weekly Review",
            model=FailingWhisperModel(),
        )
