from pathlib import Path
import shutil
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile, status

router = APIRouter()

UPLOAD_DIR = Path("backend/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a", ".flac"}
MAX_FILE_SIZE_MB = 25

@router.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided."
        )


    suffix = Path(file.filename).suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "unsupported_file_type",
                "message": f"Unsupported file type '{suffix}'.",
                "allowed_types": sorted(ALLOWED_EXTENSIONS),
            },
        )
    
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "file_too_large",
                "message": f"File exceeds {MAX_FILE_SIZE_MB} MB limit.",
            },
        )

    
    generated_name = f"{uuid4()}{suffix}"

    destination = UPLOAD_DIR / generated_name


    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "upload_failed",
                "message": "Failed to save uploaded file.",
            },
        ) from exc
    finally:
        file.file.close()


    return {
        "message": "Upload successful.",
        "file": {
            "id": generated_name,
            "original_name": file.filename,
            "extension": suffix,
            "size_bytes": file_size,
            "stored_path": str(destination),
        },
    }