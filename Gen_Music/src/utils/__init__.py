"""
Módulo de utilidades para el generador de melodías

Contiene:
- audio_utils: Funciones para manipulación y generación de audio
- music_utils: Utilidades para teoría musical y conversiones
"""

from .audio_utils import (
    generate_audio_from_predictions,
    midi_to_mp3,
    normalize_audio,
    concatenate_audio_files
)
from .music_utils import (
    note_to_midi,
    midi_to_note,
    note_to_frequency,
    scale_to_midi_notes,
    chord_to_midi_notes,
    is_valid_note,
    is_valid_scale,
    is_valid_chord
)

__all__ = [
    'generate_audio_from_predictions',
    'midi_to_mp3',
    'normalize_audio',
    'concatenate_audio_files',
    'note_to_midi',
    'midi_to_note',
    'note_to_frequency',
    'scale_to_midi_notes',
    'chord_to_midi_notes',
    'is_valid_note',
    'is_valid_scale',
    'is_valid_chord'
]