"""Tests for audio input validation."""

from pathlib import Path

import pytest

from src.transcription.audio_loader import (
    AudioValidationError,
    validate_audio_file,
)


@pytest.mark.parametrize(
    "extension",
    [".wav", ".mp3", ".m4a", ".WAV", ".MP3"],
)
def test_supported_audio_extensions(
    tmp_path: Path,
    extension: str,
) -> None:
    audio_path = tmp_path / f"meeting{extension}"
    audio_path.write_bytes(b"mock audio bytes")

    audio = validate_audio_file(audio_path)

    assert audio.path == audio_path.resolve()
    assert audio.extension == extension.lower()
    assert audio.size_bytes == len(b"mock audio bytes")
    assert audio.size_mb > 0


def test_missing_audio_file_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        validate_audio_file(tmp_path / "missing.wav")


def test_directory_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(AudioValidationError):
        validate_audio_file(tmp_path)


def test_unsupported_extension_is_rejected(tmp_path: Path) -> None:
    audio_path = tmp_path / "meeting.flac"
    audio_path.write_bytes(b"mock audio bytes")

    with pytest.raises(
        AudioValidationError,
        match="Unsupported audio extension",
    ):
        validate_audio_file(audio_path)


def test_empty_audio_file_is_rejected(tmp_path: Path) -> None:
    audio_path = tmp_path / "empty.wav"
    audio_path.touch()

    with pytest.raises(
        AudioValidationError,
        match="Audio file is empty",
    ):
        validate_audio_file(audio_path)


def test_oversized_audio_file_is_rejected(tmp_path: Path) -> None:
    audio_path = tmp_path / "large.wav"
    audio_path.write_bytes(b"1234567890")

    with pytest.raises(
        AudioValidationError,
        match="exceeds the 0 MB limit",
    ):
        validate_audio_file(
            audio_path,
            max_size_mb=0,
        )
