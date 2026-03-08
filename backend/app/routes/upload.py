from pathlib import Path
import shutil
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a", ".flac"}


@router.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code = 400,
            detail = f"Unsupported file type: {suffix}. Allowed types: {sorted(ALLOWED_EXTENSIONS)}"
        )
    
    file_id = f"{uuid4()}{suffix}"

    destination = UPLOAD_DIR / file_id


    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


    return {
        "message" : "File uploaded successfully",
        "file_id" : file_id,
        "orignal_filename" : file.filename,
    }