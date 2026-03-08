from pathlib import Path

from fastapi import APIRouter, HTTPException, status

from backend.services.audio_analysis import analyze_audio_file
from backend.services.drum_generator import generate_basic_rock_drums
from backend.services.bass_generator import generate_basic_bassline
from backend.services.rhythm_generator import generate_basic_rhythm_guitar
from backend.services.audio_renderer import (
    load_source_audio,
    render_drum_stem,
    render_bass_stem,
    render_rhythm_stem,
    mix_stems,
    save_wav,
)

router = APIRouter()

UPLOAD_DIR = Path("backend/uploads")
OUTPUT_DIR = Path("backend/generated")


@router.post("/render/{file_id}")
async def render_band_audio(file_id: str):
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
        duration_seconds = analysis["duration_seconds"]

        drums = generate_basic_rock_drums(beat_timestamps)
        bass = generate_basic_bassline(beat_timestamps)
        rhythm = generate_basic_rhythm_guitar(beat_timestamps)

        source_audio = load_source_audio(str(file_path))
        drum_stem = render_drum_stem(drums, duration_seconds)
        bass_stem = render_bass_stem(bass, duration_seconds)
        rhythm_stem = render_rhythm_stem(rhythm, duration_seconds)

        final_mix = mix_stems([source_audio, drum_stem, bass_stem, rhythm_stem])

        output_filename = f"{Path(file_id).stem}_myband_v1.wav"
        output_path = OUTPUT_DIR / output_filename
        save_wav(final_mix, str(output_path))

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "render_failed",
                "message": str(exc),
            },
        ) from exc

    return {
        "message": "Render successful",
        "source_file": file_id,
        "output_file": output_filename,
        "output_path": str(output_path),
    }