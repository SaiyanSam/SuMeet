"""Cached faster-whisper model loading."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from faster_whisper import WhisperModel
from pydantic import BaseModel, ConfigDict, Field


DeviceType = Literal["auto", "cpu", "cuda"]


class WhisperConfig(BaseModel):
    """Configuration for loading and running faster-whisper."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
    )

    model_size: str = Field(default="base.en", min_length=1)
    device: DeviceType = "auto"
    compute_type: str | None = None
    language: str | None = "en"
    beam_size: int = Field(default=5, ge=1, le=20)
    vad_filter: bool = True


def resolve_compute_type(config: WhisperConfig) -> str:
    """Choose a reasonable compute type when none is supplied."""

    if config.compute_type:
        return config.compute_type

    if config.device == "cuda":
        return "float16"

    return "int8"


@lru_cache(maxsize=4)
def load_whisper_model(
    model_size: str,
    device: DeviceType,
    compute_type: str,
) -> WhisperModel:
    """Load and cache a faster-whisper model."""

    return WhisperModel(
        model_size,
        device=device,
        compute_type=compute_type,
    )


class WhisperClient:
    """Small wrapper around a cached faster-whisper model."""

    def __init__(self, config: WhisperConfig) -> None:
        self.config = config

    def get_model(self) -> WhisperModel:
        """Return the cached model instance."""

        return load_whisper_model(
            model_size=self.config.model_size,
            device=self.config.device,
            compute_type=resolve_compute_type(self.config),
        )
