from backend.services.music_theory import normalize_note_name


def extract_root_from_chord(chord: str) -> str:
    chord = chord.strip()
    if not chord:
        raise ValueError("Empty chord provided")

    if len(chord) >= 2 and chord[1] in {"#", "b"}:
        root = chord[:2]
    else:
        root = chord[:1]

    return normalize_note_name(root)


def parse_progression(progression: str) -> list[str]:
    chords = [c.strip() for c in progression.split(",") if c.strip()]
    if not chords:
        raise ValueError("Progression is empty")
    return [extract_root_from_chord(chord) for chord in chords]