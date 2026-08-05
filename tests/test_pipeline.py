"""Tests for the transcript-ingestion pipeline."""

from pathlib import Path

import orjson

from src.pipeline import run_pipeline


def test_pipeline_creates_json_output(tmp_path: Path) -> None:
    input_path = tmp_path / "meeting.txt"
    output_path = tmp_path / "meeting.json"

    input_path.write_text(
        (
            "[00:00] Alice: Welcome everyone.\n"
            "[00:05] Bob: I will finish testing."
        ),
        encoding="utf-8",
    )

    result_path = run_pipeline(
        input_path=input_path,
        output_path=output_path,
    )

    assert result_path == output_path
    assert output_path.exists()

    data = orjson.loads(output_path.read_bytes())

    assert data["meeting_id"] == "meeting_001"
    assert len(data["segments"]) == 2
    assert data["segments"][0]["speaker"] == "Alice"
    assert data["segments"][1]["speaker"] == "Bob"
