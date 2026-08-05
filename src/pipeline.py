"""Entry point for the Day 1 transcript-ingestion pipeline."""

from __future__ import annotations

from pathlib import Path

import orjson

from src.ingestion.transcript_parser import parse_transcript_file


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "samples" / "sample_meeting.txt"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "outputs" / "sample_meeting.json"


def save_transcript_json(output_path: Path, transcript_data: dict) -> None:
    """Save structured transcript data as readable JSON."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_bytes(
        orjson.dumps(
            transcript_data,
            option=orjson.OPT_INDENT_2,
        )
    )


def run_pipeline(
    input_path: Path = DEFAULT_INPUT,
    output_path: Path = DEFAULT_OUTPUT,
) -> Path:
    """Parse one transcript file and save the validated result."""

    transcript = parse_transcript_file(
        file_path=input_path,
        meeting_id="meeting_001",
        title="Weekly Project Review",
        language="en",
    )

    save_transcript_json(
        output_path=output_path,
        transcript_data=transcript.model_dump(),
    )

    print(f"Parsed {len(transcript.segments)} transcript segments.")
    print(f"Participants: {', '.join(transcript.participants) or 'Not available'}")
    print(f"Saved output to: {output_path}")

    return output_path


if __name__ == "__main__":
    run_pipeline()
