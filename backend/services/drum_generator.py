def generate_basic_rock_drums(beat_timestamps: list[float]) -> dict:

    kick_times = []
    snare_times = []
    hihat_times = []
    fill_sections = []

    if not beat_timestamps:
        return {
            "pattern": "rock",
            "kick_times": kick_times,
            "snare_times": snare_times,
            "hihat_time": hihat_times,
            "fill_sections": fill_sections,
        }
    
    for i, beat_time in enumerate(beat_timestamps):

        beats_in_bar = i % 4

        hihat_times.append(round(float(beat_time), 3))

        if beats_in_bar in (0, 2):
            kick_times.append(round(float(beat_time), 3))

        if beats_in_bar in (1, 3):
            snare_times.append(round(float(beat_time), 3))

        if beats_in_bar == 3 and i >= 15:
            fill_sections.append(round(float(beat_time), 3))

    
    return {
        "pattern": "rock",
        "kick_times": kick_times,
        "snare_times": snare_times,
        "hihat_time": hihat_times,
        "fill_sections": fill_sections,
    }