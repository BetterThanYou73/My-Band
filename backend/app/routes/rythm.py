from pathlib import Path

from fastapi import APIRouter, HTTPException, status

from backend.services.audio_analysis import analyze_audio_file
from backend.services.rhythm_generator import generate_basic_rhythm_guitar

router = APIRouter()

UPLOAD_DIR = Path("backend/uploads")


@router.get("/generate/rhythm/{file_id}")
async def generate_rhythm(file_id: str):
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
        rhythm_plan = generate_basic_rhythm_guitar(beat_timestamps)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "rhythm_generation_failed",
                "message": str(exc),
            },
        ) from exc

    return {
        "message": "Rhythm guitar generation successful",
        "source_file": file_id,
        "tempo_bpm": analysis["tempo_bpm"],
        "beat_count": analysis["beat_count"],
        "rhythm_guitar": rhythm_plan,
    }