NOTE_TO_MIDI = {
    "C": 36,
    "C#": 37,
    "D": 38,
    "D#": 39,
    "E": 40,
    "F": 41,
    "F#": 42,
    "G": 43,
    "G#": 44,
    "A": 45,
    "A#": 46,
    "B": 47,
}

ENHARMONIC_EQUIVALENTS = {
    "E#": "F",
    "B#": "C",
    "Cb": "B",
    "Fb": "E",
}


def normalize_note_name(note: str) -> str:
    note = note.strip()
    return ENHARMONIC_EQUIVALENTS.get(note, note)


def get_root_midi(note: str) -> int:
    normalized = normalize_note_name(note)
    if normalized not in NOTE_TO_MIDI:
        raise ValueError(f"Unsupported note name: {note}")
    return NOTE_TO_MIDI[normalized]


def get_fifth_midi(note: str) -> int:
    root = get_root_midi(note)
    return root + 7