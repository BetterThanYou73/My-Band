from backend.services.music_theory import get_root_midi, get_fifth_midi


def generate_basic_bassline(
    beat_timestamps: list[float],
    key: str = "E",
    progression_roots: list[str] | None = None,
) -> dict:
    notes = []

    if not beat_timestamps:
        return {
            "pattern": "bass_basic",
            "notes": []
        }

    for i, beat_time in enumerate(beat_timestamps):
        beat_in_bar = i % 4
        bar_index = i // 4

        current_root = key
        if progression_roots:
            current_root = progression_roots[bar_index % len(progression_roots)]

        root_midi = get_root_midi(current_root)
        fifth_midi = get_fifth_midi(current_root)

        if beat_in_bar == 0:
            notes.append({
                "time": round(float(beat_time), 3),
                "note_role": "root",
                "chord_root": current_root,
                "midi_note": root_midi,
                "duration": 0.4
            })
        elif beat_in_bar == 2:
            notes.append({
                "time": round(float(beat_time), 3),
                "note_role": "fifth",
                "chord_root": current_root,
                "midi_note": fifth_midi,
                "duration": 0.35
            })

    return {
        "pattern": "bass_basic",
        "key_center": key,
        "progression_roots": progression_roots or [],
        "notes": notes
    }