from pathlib import Path

from fastapi import APIRouter, HTTPException, status

from backend.services.audio_analysis import analyze_audio_file
from backend.services.drum_generator import generate_basic_rock_drums
from backend.services.bass_generator import generate_basic_bassline
from backend.services.rhythm_generator import generate_basic_rhythm_guitar

router = APIRouter()

UPLOAD_DIR = Path("backend/uploads")


@router.get("/generate/band/{file_id}")
async def generate_band(file_id: str):
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

        drums = generate_basic_rock_drums(beat_timestamps)
        bass = generate_basic_bassline(beat_timestamps)
        rhythm_guitar = generate_basic_rhythm_guitar(beat_timestamps)

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
        },
        "arrangement": {
            "drums": drums,
            "bass": bass,
            "rhythm_guitar": rhythm_guitar,
        },
    }