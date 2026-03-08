from backend.services.music_theory import get_root_midi, get_fifth_midi


def generate_basic_bassline(beat_timestamps: list[float], key: str = "E") -> dict:
    notes = []

    if not beat_timestamps:
        return {
            "pattern": "bass_basic",
            "notes": []
        }

    root_midi = get_root_midi(key)
    fifth_midi = get_fifth_midi(key)

    for i, beat_time in enumerate(beat_timestamps):
        beat_in_bar = i % 4

        if beat_in_bar == 0:
            notes.append({
                "time": round(float(beat_time), 3),
                "note_role": "root",
                "midi_note": root_midi,
                "duration": 0.4
            })
        elif beat_in_bar == 2:
            notes.append({
                "time": round(float(beat_time), 3),
                "note_role": "fifth",
                "midi_note": fifth_midi,
                "duration": 0.35
            })

    return {
        "pattern": "bass_basic",
        "key_center": key,
        "notes": notes
    }