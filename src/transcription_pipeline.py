"""Command-line pipeline for audio transcription."""

from __future__ import annotations

import argparse
from pathlib import Path

import orjson

from src.config import OUTPUTS_DIR
from src.transcription.transcriber import transcribe_audio
from src.transcription.whisper_client import WhisperConfig


def save_transcript(
    transcript_data: dict,
    output_path: Path,
) -> Path:
    """Save a transcript as readable JSON."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_bytes(
        orjson.dumps(
            transcript_data,
            option=orjson.OPT_INDENT_2,
        )
    )

    return output_path


def run_audio_pipeline(
    audio_path: str | Path,
    meeting_id: str,
    title: str,
    output_path: str | Path | None = None,
    model_size: str = "base.en",
    device: str = "cpu",
    compute_type: str | None = None,
    language: str | None = "en",
) -> Path:
    """Transcribe one audio file and save the result."""

    audio_path = Path(audio_path)

    if output_path is None:
        output_path = OUTPUTS_DIR / f"{audio_path.stem}_transcript.json"
    else:
        output_path = Path(output_path)

    config = WhisperConfig(
        model_size=model_size,
        device=device,
        compute_type=compute_type,
        language=language,
    )

    transcript = transcribe_audio(
        audio_path=audio_path,
        meeting_id=meeting_id,
        title=title,
        config=config,
    )

    saved_path = save_transcript(
        transcript_data=transcript.model_dump(),
        output_path=output_path,
    )

    print(f"Meeting ID: {transcript.meeting_id}")
    print(f"Language: {transcript.language or 'Unknown'}")
    print(f"Duration: {transcript.duration_seconds:.2f} seconds")
    print(f"Segments: {len(transcript.segments)}")
    print(f"Saved transcript to: {saved_path}")

    return saved_path


def build_parser() -> argparse.ArgumentParser:
    """Create command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Transcribe meeting audio using faster-whisper."
    )

    parser.add_argument("audio_path", type=Path)
    parser.add_argument(
        "--meeting-id",
        default="meeting_001",
    )
    parser.add_argument(
        "--title",
        default="Untitled Meeting",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
    )
    parser.add_argument(
        "--model-size",
        default="base.en",
    )
    parser.add_argument(
        "--device",
        choices=["auto", "cpu", "cuda"],
        default="cpu",
    )
    parser.add_argument(
        "--compute-type",
        default=None,
    )
    parser.add_argument(
        "--language",
        default="en",
    )

    return parser


def main() -> None:
    args = build_parser().parse_args()

    run_audio_pipeline(
        audio_path=args.audio_path,
        meeting_id=args.meeting_id,
        title=args.title,
        output_path=args.output,
        model_size=args.model_size,
        device=args.device,
        compute_type=args.compute_type,
        language=args.language,
    )


if __name__ == "__main__":
    main()
