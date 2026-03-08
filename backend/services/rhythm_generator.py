def generate_basic_rhythm_guitar(beat_timestamps: list[float]) -> dict:
    strums = []

    if not beat_timestamps:
        return {
            "pattern": "rhythm_basic",
            "strums": []
        }

    for i, beat_time in enumerate(beat_timestamps):
        beat_in_bar = i % 4

        if beat_in_bar == 0:
            strums.append({
                "time": round(float(beat_time), 3),
                "chord_role": "power_chord_root",
                "duration": 0.6,
                "style": "downstroke"
            })
        elif beat_in_bar == 2:
            strums.append({
                "time": round(float(beat_time), 3),
                "chord_role": "power_chord_root",
                "duration": 0.45,
                "style": "downstroke"
            })

    return {
        "pattern": "rhythm_basic",
        "strums": strums
    }