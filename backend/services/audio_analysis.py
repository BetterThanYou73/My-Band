from pathlib import Path

import librosa
import numpy as np

def analyze_audio_file(file_path: Path) -> dict:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:

        y, sr = librosa.load(path, sr=None, mono=False)
        
    except Exception as exc:
        raise ValueError(f"Failed to analyze audio file: {path.name}") from exc
        

    if isinstance(y, np.ndarray) and y.ndim > 1:
        channels = y.shape[0]
        total_samples = y.shape[1]
        y_mono = librosa.to_mono(y)
    else:
        channels = 1
        total_samples = len(y)
        y_mono = y

    duration_seconds = total_samples / sr if sr else 0
    tempo, beat_frames = librosa.beat.beat_track(y=y_mono, sr=sr)

    if isinstance(tempo, np.ndarray):
        if tempo.size == 0:
            tempo_value = 0.0
        else:
            tempo_value = float(tempo.flatten()[0])
    else:
        tempo_value = float(tempo)


    beat_timestamps = librosa.frames_to_time(beat_frames, sr=sr)

    return {
        "filename": path.name,
        "sample_rate": sr,
        "channels": channels,
        "duration_seconds": round(duration_seconds, 3),
        "total_samples": int(total_samples),
        "tempo_bpm": round(tempo_value, 2),
        "beat_count": int(len(beat_timestamps)),
        "beat_timestamps_preview": [round(float(t), 3) for t in beat_timestamps[:10]],
    }