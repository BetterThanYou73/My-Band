from pathlib import Path
import wave
import librosa

import numpy as np

DEFAULT_SAMPLE_RATE = 44100


def _time_to_sample(time_seconds: float, sr:int) -> int:
    return int(round(time_seconds * sr))

def _add_sine_tone(buffer: np.ndarray, start_time: float, duration: float, freq: float, amplitude: float, sr: int) -> None:
    start = _time_to_sample(start_time, sr)
    length = int(duration * sr)

    if start >= len(buffer):
        return
    
    end = min(start + length, len(buffer))
    actual_length = end - start

    t = np.arange(actual_length) / sr
    envelope = np.linspace(1.0, 0.0, actual_length)
    tone = amplitude * np.sin(2 * np.pi * freq * t) * envelope

    buffer[start:end] += tone


def _add_noise_hit(buffer: np.ndarray, start_time: float, duration: float, amplitude: float, sr: int) -> None:
    start = _time_to_sample(start_time, sr)
    length = int(duration * sr)

    if start >= len(buffer):
        return

    end = min(start + length, len(buffer))
    actual_length = end - start

    envelope = np.linspace(1.0, 0.0, actual_length)
    noise = amplitude * np.random.randn(actual_length) * envelope

    buffer[start:end] += noise


def render_drum_stem(drum_plan: dict, duration_seconds: float, sr: int=DEFAULT_SAMPLE_RATE) -> np.ndarray:
    total_samples = int(duration_seconds * sr) + sr
    buffer = np.zeros(total_samples, dtype=np.float32)

    for t in drum_plan.get("kick_times", []):
        _add_sine_tone(buffer, t, 0.12, 80.0, 0.8, sr)

    for t in drum_plan.get("snare_times", []):
        _add_noise_hit(buffer, t, 0.10, 0.5, sr)

    for t in drum_plan.get("hihat_times", []):
        _add_noise_hit(buffer, t, 0.03, 0.2, sr)

    return buffer


def render_bass_stem(bass_plan: dict, duration_seconds: float, sr: int=DEFAULT_SAMPLE_RATE) -> np.ndarray:
    total_samples = int(duration_seconds * sr) + sr
    buffer = np.zeros(total_samples, dtype=np.float32)


    role_to_freq = {
        "root": 55.0,
        "fifth": 82.41,
    }

    for note in bass_plan.get("notes", []):
        freq = role_to_freq.get(note["note_role"], 55.0)
        _add_sine_tone(
            buffer,
            note["time"],
            note["duration"],
            freq,
            0.55,
            sr,
        )

    return buffer

def render_rhythm_stem(rhythm_plan: dict, duration_seconds: float, sr: int=DEFAULT_SAMPLE_RATE) -> np.ndarray:
    total_samples = int(duration_seconds * sr) + sr
    buffer = np.zeros(total_samples, dtype=np.float32)

    for strum in rhythm_plan.get("strums", []):
        start_time = strum["time"]
        duration = strum["duration"]

        _add_sine_tone(buffer, start_time, duration, 110.0, 0.22, sr)
        _add_sine_tone(buffer, start_time, duration, 138.59, 0.18, sr)
        _add_sine_tone(buffer, start_time, duration, 164.81, 0.15, sr)

    return buffer



def mix_stems(stems: list[np.ndarray]) -> np.ndarray:
    if not stems:
        return np.array([], dtype=np.float32)

    max_len = max(len(stem) for stem in stems)
    mix = np.zeros(max_len, dtype=np.float32)

    for stem in stems:
        mix[:len(stem)] += stem

    peak = np.max(np.abs(mix))
    if peak > 0:
        mix = mix / peak * 0.9

    return mix.astype(np.float32)


def save_wav(audio: np.ndarray, output_path: str, sr: int = DEFAULT_SAMPLE_RATE):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    audio_int16 = (audio * 32767).astype(np.int16)

    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(audio_int16.tobytes())


def load_source_audio(file_path: str, sr: int = DEFAULT_SAMPLE_RATE) -> np.ndarray:
    y, _ = librosa.load(file_path, sr=sr, mono=True)

    peak = np.max(np.abs(y))
    if peak > 0:
        y = y / peak * 0.7

    return y.astype(np.float32)