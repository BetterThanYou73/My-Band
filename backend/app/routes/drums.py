from pathlib import Path
from fastapi import APIRouter, HTTPException, status

from backend.services.audio_analysis import analyze_audio_file
from backend.services.drum_generator import generate_basic_rock_drums

router = APIRouter()

UPLOAD_DIR = Path("backend/uploads")

@router.get("/drums/{file_id}")
async def generate_drums_for_audio(file_id: str):
    file_path = UPLOAD_DIR / file_id

    if not file_path.exists():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = {
                "error": "file_not_found",
                "message": f"No uploaded file found for id '{file_id}'."
            }
        )
    
    try:
        analysis = analyze_audio_file(str(file_path))
        beat_timestamps = analysis["beat_timestamps"]
        drum_plan = generate_basic_rock_drums(beat_timestamps)
    
    except Exception as exc:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "error": "drum_generation_failed",
                "message": str(exc),
            }
        ) from exc
    
    return {
        "message": "Drum generation successful",
        "source_file": file_id,
        "tempo_bpm": analysis["tempo_bpm"],
        "beat_count": analysis["beat_count"],
        "drums": drum_plan,
    }
        