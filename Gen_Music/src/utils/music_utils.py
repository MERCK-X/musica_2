import re
from typing import Union, List, Optional, Tuple
import numpy as np

# Definiciones musicales
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
SCALE_TYPES = {
    'major': [0, 2, 4, 5, 7, 9, 11],
    'minor': [0, 2, 3, 5, 7, 8, 10],
    'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],
    'melodic_minor': [0, 2, 3, 5, 7, 9, 11],
    'pentatonic': [0, 2, 4, 7, 9],
    'blues': [0, 3, 5, 6, 7, 10]
}
CHORD_TYPES = {
    'major': [0, 4, 7],
    'minor': [0, 3, 7],
    'diminished': [0, 3, 6],
    'augmented': [0, 4, 8],
    '7th': [0, 4, 7, 10],
    'maj7': [0, 4, 7, 11],
    'min7': [0, 3, 7, 10]
}

def note_to_midi(note: str) -> Optional[int]:
    """
    Convierte un nombre de nota (ej. 'C4') a valor MIDI (0-127)
    
    Args:
        note: Nombre de la nota (ej. 'C#5', 'Ab3')
        
    Returns:
        Valor MIDI o None si no es válido
    """
    match = re.match(r'^([A-Ga-g]#?|b?)(-?\d+)$', note.strip())
    if not match:
        return None
    
    note_name, octave = match.groups()
    note_name = note_name.upper()
    
    if note_name not in NOTE_NAMES:
        # Manejar bemoles (ej. 'Bb' -> 'A#')
        if 'B' in note_name and len(note_name) > 1:
            note_name = NOTE_NAMES[(NOTE_NAMES.index('A') + 1) % 12] + '#'
        elif 'E' in note_name and len(note_name) > 1:
            note_name = NOTE_NAMES[(NOTE_NAMES.index('D') + 1) % 12] + '#'
        else:
            return None
    
    try:
        octave = int(octave)
        if not (-1 <= octave <= 9):
            return None
    except ValueError:
        return None
    
    note_index = NOTE_NAMES.index(note_name)
    return 12 + octave * 12 + note_index

def midi_to_note(midi: int) -> str:
    """
    Convierte un valor MIDI (0-127) a nombre de nota (ej. 'C4')
    
    Args:
        midi: Valor MIDI (0-127)
        
    Returns:
        Nombre de la nota o None si no es válido
    """
    if not 0 <= midi <= 127:
        return None
    
    octave = (midi // 12) - 1
    note_name = NOTE_NAMES[midi % 12]
    return f"{note_name}{octave}"

def note_to_frequency(note: Union[str, int]) -> float:
    """
    Convierte una nota musical a frecuencia en Hz
    
    Args:
        note: Nombre de nota (ej. 'A4') o valor MIDI
        
    Returns:
        Frecuencia en Hz o None si no es válido
    """
    if isinstance(note, str):
        midi = note_to_midi(note)
        if midi is None:
            return None
    elif isinstance(note, int):
        midi = note
    else:
        return None
    
    # Fórmula: f = 440 * 2^((n-69)/12)
    return 440.0 * (2.0 ** ((midi - 69) / 12.0))

def scale_to_midi_notes(root: str, scale_type: str, octaves: int = 2) -> List[int]:
    """
    Genera notas MIDI para una escala
    
    Args:
        root: Nota raíz (ej. 'C', 'F#')
        scale_type: Tipo de escala (ej. 'major', 'minor')
        octaves: Número de octavas a generar
        
    Returns:
        Lista de valores MIDI para la escala
    """
    if scale_type not in SCALE_TYPES:
        return []
    
    root_midi = note_to_midi(root + '4')  # Octava central
    if root_midi is None:
        return []
    
    scale_intervals = SCALE_TYPES[scale_type]
    notes = []
    
    for octave in range(octaves):
        for interval in scale_intervals:
            note = root_midi + interval + octave * 12
            if 0 <= note <= 127:
                notes.append(note)
    
    return notes

def chord_to_midi_notes(root: str, chord_type: str) -> List[int]:
    """
    Genera notas MIDI para un acorde
    
    Args:
        root: Nota raíz (ej. 'C', 'F#')
        chord_type: Tipo de acorde (ej. 'major', 'minor7')
        
    Returns:
        Lista de valores MIDI para el acorde
    """
    if chord_type not in CHORD_TYPES:
        return []
    
    root_midi = note_to_midi(root + '4')  # Octava central
    if root_midi is None:
        return []
    
    chord_intervals = CHORD_TYPES[chord_type]
    return [root_midi + interval for interval in chord_intervals if root_midi + interval <= 127]

def is_valid_note(note: str) -> bool:
    """Verifica si una cadena es una nota musical válida"""
    return note_to_midi(note) is not None

def is_valid_scale(scale: str) -> bool:
    """Verifica si una cadena representa una escala válida (ej. 'C major')"""
    parts = scale.split()
    return len(parts) == 2 and parts[0].upper() in NOTE_NAMES and parts[1] in SCALE_TYPES

def is_valid_chord(chord: str) -> bool:
    """Verifica si una cadena representa un acorde válido (ej. 'Cmaj7')"""
    # Patrones para acordes (ej. C, Cm, Cdim, C7, Cmaj7)
    pattern = r'^([A-Ga-g]#?|b?)(maj|min|m|dim|aug)?(7|maj7|min7)?$'
    match = re.match(pattern, chord.strip(), re.IGNORECASE)
    return bool(match)

def parse_music_input(input_str: str) -> List[int]:
    """
    Parsea una cadena de entrada con notas, acordes o escalas y devuelve valores MIDI
    
    Args:
        input_str: Cadena con notas, acordes o escalas separados por comas
        
    Returns:
        Lista de valores MIDI
    """
    elements = [elem.strip() for elem in input_str.split(',')]
    midi_notes = []
    
    for elem in elements:
        if is_valid_note(elem):
            midi_notes.append(note_to_midi(elem))
        elif is_valid_chord(elem):
            # Extraer root y tipo de acorde
            root = re.match(r'^([A-Ga-g]#?|b?)', elem).group(1)
            chord_type = elem[len(root):].lower()
            if not chord_type:
                chord_type = 'major'
            elif chord_type == 'm':
                chord_type = 'minor'
            midi_notes.extend(chord_to_midi_notes(root, chord_type))
        elif is_valid_scale(elem):
            root, scale_type = elem.split()
            midi_notes.extend(scale_to_midi_notes(root, scale_type))
    
    return [note for note in midi_notes if note is not None]