import numpy as np
from typing import List, Dict, Any
import random

def transpose_sequence(sequence: List[Dict[str, Any]], semitones: int) -> List[Dict[str, Any]]:
    """
    Transpone una secuencia de notas por un número de semitonos
    
    Args:
        sequence: Secuencia de notas a transponer
        semitones: Número de semitonos a transponer (positivo o negativo)
        
    Returns:
        Secuencia transpuesta
    """
    transposed = []
    for note_data in sequence:
        new_note = note_data.copy()
        new_note['pitch'] = max(0, min(127, note_data['pitch'] + semitones))
        transposed.append(new_note)
    return transposed

def augment_sequence(sequence: List[Dict[str, Any]], 
                    augmentation_types: List[str] = None) -> List[List[Dict[str, Any]]]:
    """
    Aplica aumentos de datos a una secuencia musical
    
    Args:
        sequence: Secuencia original de notas
        augmentation_types: Tipos de aumento a aplicar (None para todos)
        
    Returns:
        Lista de secuencias aumentadas (incluyendo la original)
    """
    if augmentation_types is None:
        augmentation_types = ['transpose', 'time_shift', 'velocity_change']
    
    augmented_sequences = [sequence]
    
    # Transposición (variaciones de tono)
    if 'transpose' in augmentation_types:
        for semitones in [-3, -2, 2, 3]:  # Evitamos transposiciones cromáticas
            augmented_sequences.append(transpose_sequence(sequence, semitones))
    
    # Cambios de tiempo (pequeñas variaciones rítmicas)
    if 'time_shift' in augmentation_types:
        time_shift = random.uniform(-0.05, 0.05)
        time_shifted = []
        for note_data in sequence:
            new_note = note_data.copy()
            new_note['start'] += time_shift
            new_note['end'] += time_shift
            time_shifted.append(new_note)
        augmented_sequences.append(time_shifted)
    
    # Cambios de velocidad (dinámica)
    if 'velocity_change' in augmentation_types:
        velocity_factor = random.uniform(0.8, 1.2)
        velocity_changed = []
        for note_data in sequence:
            new_note = note_data.copy()
            new_note['velocity'] = int(max(1, min(127, note_data['velocity'] * velocity_factor)))
            velocity_changed.append(new_note)
        augmented_sequences.append(velocity_changed)
    
    return augmented_sequences