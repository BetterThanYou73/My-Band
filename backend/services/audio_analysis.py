from pathlib import Path

import librosa

def analyze_audio_file(file_path: Path) -> dict:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:

        y, sr = librosa.load(path, sr=None, mono=False)
        
    except Exception as exc:
        raise ValueError(f"Failed to analyze audio file: {path.name}") from exc
        

    if hasattr(y, "ndim") and y.ndim > 1:
        channels = y.shape[0]
        total_samples = y.shape[1]
        
    else:
        channels = 1
        total_samples = len(y)

    duration_seconds = total_samples / sr if sr else 0

    return {
        "filename": path.name,
        "sample_rate": sr,
        "channels": channels,
        "duration_seconds": round(duration_seconds, 3),
        "total_samples": int(total_samples),
    }