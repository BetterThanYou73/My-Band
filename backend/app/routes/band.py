from pathlib import Path

from fastapi import APIRouter, HTTPException, Query, status

from backend.services.audio_analysis import analyze_audio_file
from backend.services.drum_generator import generate_basic_rock_drums
from backend.services.bass_generator import generate_basic_bassline
from backend.services.rhythm_generator import generate_basic_rhythm_guitar
from backend.services.progression import parse_progression

router = APIRouter()

UPLOAD_DIR = Path("backend/uploads")


@router.get("/generate/band/{file_id}")
async def generate_band(
    file_id: str,
    key: str | None = Query(default=None),
    progression: str | None = Query(default=None),
):
    file_path = UPLOAD_DIR / file_id

    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "file_not_found",
                "message": f"No uploaded file found for id '{file_id}'.",
            },
        )

    try:
        analysis = analyze_audio_file(str(file_path))
        beat_timestamps = analysis["beat_timestamps"]

        selected_key = key if key else analysis["detected_key"]
        progression_roots = parse_progression(progression) if progression else None

        drums = generate_basic_rock_drums(beat_timestamps)
        bass = generate_basic_bassline(
            beat_timestamps,
            key=selected_key,
            progression_roots=progression_roots,
        )
        rhythm_guitar = generate_basic_rhythm_guitar(
            beat_timestamps,
            key=selected_key,
            progression_roots=progression_roots,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "band_generation_failed",
                "message": str(exc),
            },
        ) from exc

    return {
        "message": "Band generation successful",
        "source_file": file_id,
        "analysis": {
            "tempo_bpm": analysis["tempo_bpm"],
            "beat_count": analysis["beat_count"],
            "duration_seconds": analysis["duration_seconds"],
            "sample_rate": analysis["sample_rate"],
            "channels": analysis["channels"],
            "detected_key": analysis.get("detected_key"),
            "detected_mode": analysis.get("detected_mode"),
        },
        "generation_settings": {
            "selected_key": selected_key,
            "progression_roots": progression_roots or [],
        },
        "arrangement": {
            "drums": drums,
            "bass": bass,
            "rhythm_guitar": rhythm_guitar,
        },
    }