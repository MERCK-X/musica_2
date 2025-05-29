"""
Módulo para procesamiento de datos musicales

Contiene:
- midi_processor: Conversión de archivos MIDI a formatos procesables
- data_augmentation: Técnicas para aumentar el dataset
"""
from .midi_processor import midi_to_notes, preprocess_dataset
from .data_augmentation import augment_sequence, transpose_sequence

__all__ = ['midi_to_notes', 'preprocess_dataset', 'augment_sequence', 'transpose_sequence']