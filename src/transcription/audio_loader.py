"""Validation utilities for audio input files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.config import (
    MAX_AUDIO_FILE_SIZE_MB,
    SUPPORTED_AUDIO_EXTENSIONS,
)


class AudioValidationError(ValueError):
    """Raised when an audio input does not satisfy SuMeet requirements."""


@dataclass(frozen=True, slots=True)
class AudioFile:
    """Validated metadata for an audio file."""

    path: Path
    extension: str
    size_bytes: int

    @property
    def size_mb(self) -> float:
        """Return the file size in megabytes."""

        return self.size_bytes / (1024 * 1024)


def validate_audio_file(
    file_path: str | Path,
    max_size_mb: int = MAX_AUDIO_FILE_SIZE_MB,
) -> AudioFile:
    """Validate an audio path and return immutable metadata.

    Validation currently checks:

    - path existence,
    - regular-file status,
    - supported extension,
    - non-empty content,
    - configured maximum file size.

    The file is not decoded at this stage.
    """

    path = Path(file_path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {path}")

    if not path.is_file():
        raise AudioValidationError(
            f"Audio path is not a regular file: {path}"
        )

    extension = path.suffix.lower()

    if extension not in SUPPORTED_AUDIO_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_AUDIO_EXTENSIONS))
        raise AudioValidationError(
            f"Unsupported audio extension '{extension or '<none>'}'. "
            f"Supported extensions: {supported}"
        )

    size_bytes = path.stat().st_size

    if size_bytes == 0:
        raise AudioValidationError(f"Audio file is empty: {path}")

    maximum_bytes = max_size_mb * 1024 * 1024

    if size_bytes > maximum_bytes:
        raise AudioValidationError(
            f"Audio file is {size_bytes / (1024 * 1024):.2f} MB, "
            f"which exceeds the {max_size_mb} MB limit"
        )

    return AudioFile(
        path=path,
        extension=extension,
        size_bytes=size_bytes,
    )
