"""Convert audio files into validated SuMeet transcripts."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Any, Protocol

from src.models.transcript import Transcript, TranscriptSegment
from src.transcription.audio_loader import validate_audio_file
from src.transcription.whisper_client import WhisperClient, WhisperConfig


class WhisperSegmentLike(Protocol):
    """Minimal segment interface returned by faster-whisper."""

    start: float
    end: float
    text: str


class WhisperInfoLike(Protocol):
    """Minimal metadata interface returned by faster-whisper."""

    language: str
    duration: float


class WhisperModelLike(Protocol):
    """Protocol allowing Whisper to be replaced by a test double."""

    def transcribe(
        self,
        audio: str,
        **kwargs: Any,
    ) -> tuple[Iterable[WhisperSegmentLike], WhisperInfoLike]:
        ...


class TranscriptionError(RuntimeError):
    """Raised when audio transcription cannot produce valid output."""


def transcribe_audio(
    audio_path: str | Path,
    meeting_id: str,
    title: str,
    config: WhisperConfig | None = None,
    model: WhisperModelLike | None = None,
) -> Transcript:
    """Transcribe audio into the shared Transcript schema.

    A model can be injected during tests to avoid loading or downloading
    an actual Whisper model.
    """

    validated_audio = validate_audio_file(audio_path)
    whisper_config = config or WhisperConfig()

    active_model = model
    if active_model is None:
        active_model = WhisperClient(whisper_config).get_model()

    try:
        raw_segments, info = active_model.transcribe(
            str(validated_audio.path),
            language=whisper_config.language,
            beam_size=whisper_config.beam_size,
            vad_filter=whisper_config.vad_filter,
        )
    except Exception as exc:
        raise TranscriptionError(
            f"Failed to transcribe audio file: {validated_audio.path}"
        ) from exc

    transcript_segments: list[TranscriptSegment] = []

    for raw_segment in raw_segments:
        text = raw_segment.text.strip()

        if not text:
            continue
    
        segment_number = len(transcript_segments) + 1
    
        transcript_segments.append(
            TranscriptSegment(
                segment_id=f"seg_{segment_number:04d}",
                start=float(raw_segment.start),
                end=float(raw_segment.end),
                speaker=None,
                text=text,
            )
        )

    if not transcript_segments:
        raise TranscriptionError(
            "Whisper returned no non-empty transcript segments"
        )

    language = getattr(info, "language", None)
    duration = getattr(info, "duration", None)

    if duration is None:
        duration = max(
            segment.end
            for segment in transcript_segments
            if segment.end is not None
        )

    return Transcript(
        meeting_id=meeting_id,
        title=title,
        language=language,
        duration_seconds=float(duration),
        segments=transcript_segments,
    )
