from pathlib import Path
from fastapi import APIRouter, HTTPException, status
from backend.services.audio_analysis import analyze_audio_file

router = APIRouter()

UPLOAD_DIR = Path("backend/uploads")

@router.get("/analyze/{file_id}")
async def analyze_uploaded_audio(file_id: str):

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
    except ValueError as exc:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "error": "analysis_failed",
                "message": str(exc)
            }
        ) from exc
    
    return {
        "message": "Analysis successful",
        "analysis": analysis,
    }