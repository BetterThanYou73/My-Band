def generate_basic_bassline(beat_timestamps: list[float]) -> dict:

    notes = []

    if not beat_timestamps:
        return {
            "pattern": "basic_bass",
            "notes": notes,
        }
    
    for i, beat_time in enumerate(beat_timestamps):
        beats_in_bar = i % 4

        if beats_in_bar == 0:
            notes.append({
                "time": round(float(beat_time), 3),
                "note_role": "root",
                "duration": 0.4,
            })

        elif beats_in_bar == 2:
            notes.append({
                "time": round(float(beat_time), 3),
                "note_role": "fifth",
                "duration": 0.35,
            })


    return {
        "pattern": "bass_basic",
        "notes": notes,
    }

