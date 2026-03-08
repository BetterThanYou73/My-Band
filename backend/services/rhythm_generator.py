from backend.services.music_theory import get_root_midi, get_fifth_midi


def generate_basic_rhythm_guitar(beat_timestamps: list[float], key: str = "E") -> dict:
    strums = []

    if not beat_timestamps:
        return {
            "pattern": "rhythm_basic",
            "strums": []
        }

    root_midi = get_root_midi(key)
    fifth_midi = get_fifth_midi(key)

    for i, beat_time in enumerate(beat_timestamps):
        beat_in_bar = i % 4

        if beat_in_bar == 0:
            strums.append({
                "time": round(float(beat_time), 3),
                "chord_role": "power_chord_root",
                "root_midi": root_midi,
                "fifth_midi": fifth_midi,
                "duration": 0.6,
                "style": "downstroke"
            })
        elif beat_in_bar == 2:
            strums.append({
                "time": round(float(beat_time), 3),
                "chord_role": "power_chord_root",
                "root_midi": root_midi,
                "fifth_midi": fifth_midi,
                "duration": 0.45,
                "style": "downstroke"
            })

    return {
        "pattern": "rhythm_basic",
        "key_center": key,
        "strums": strums
    }