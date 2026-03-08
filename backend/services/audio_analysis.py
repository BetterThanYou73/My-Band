from pathlib import Path

import librosa
import numpy as np


PITCH_CLASSES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


def detect_key(y_mono: np.ndarray, sr: int) -> dict:
    chroma = librosa.feature.chroma_stft(y=y_mono, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)

    major_scores = []
    minor_scores = []

    for i in range(12):
        rotated_major = np.roll(MAJOR_PROFILE, i)
        rotated_minor = np.roll(MINOR_PROFILE, i)

        major_score = np.corrcoef(chroma_mean, rotated_major)[0, 1]
        minor_score = np.corrcoef(chroma_mean, rotated_minor)[0, 1]

        major_scores.append(major_score)
        minor_scores.append(minor_score)

    best_major_idx = int(np.argmax(major_scores))
    best_minor_idx = int(np.argmax(minor_scores))

    best_major_score = float(major_scores[best_major_idx])
    best_minor_score = float(minor_scores[best_minor_idx])

    if best_major_score >= best_minor_score:
        return {
            "key": PITCH_CLASSES[best_major_idx],
            "mode": "major",
            "confidence": round(best_major_score, 3),
        }

    return {
        "key": PITCH_CLASSES[best_minor_idx],
        "mode": "minor",
        "confidence": round(best_minor_score, 3),
    }


def analyze_audio_file(file_path: str) -> dict:
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
    key_info = detect_key(y_mono, sr)

    return {
        "filename": path.name,
        "sample_rate": int(sr),
        "channels": int(channels),
        "duration_seconds": round(float(duration_seconds), 3),
        "total_samples": int(total_samples),
        "tempo_bpm": round(tempo_value, 2),
        "beat_count": int(len(beat_timestamps)),
        "beat_timestamps": [round(float(t), 3) for t in beat_timestamps],
        "beat_timestamps_preview": [round(float(t), 3) for t in beat_timestamps[:10]],
        "detected_key": key_info["key"],
        "detected_mode": key_info["mode"],
        "key_confidence": key_info["confidence"],
    }