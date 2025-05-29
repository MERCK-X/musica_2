import pretty_midi
import numpy as np
from music21 import converter, instrument, note, chord
import os

def midi_to_notes(midi_path, seq_length=100):
    """Convierte un archivo MIDI a secuencias de notas para el modelo"""
    pm = pretty_midi.PrettyMIDI(midi_path)
    instrument = pm.instruments[0]
    notes = []
    
    for note in instrument.notes:
        notes.append({
            'pitch': note.pitch,
            'start': note.start,
            'end': note.end,
            'velocity': note.velocity
        })
    
    # Crear secuencias para entrenamiento
    sequences = []
    for i in range(len(notes) - seq_length):
        seq = notes[i:i + seq_length]
        sequences.append(seq)
    
    return sequences

def preprocess_dataset(data_dir, output_dir, seq_length=100):
    """Preprocesa todos los archivos MIDI en un directorio"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    all_sequences = []
    for file in os.listdir(data_dir):
        if file.endswith('.mid') or file.endswith('.midi'):
            try:
                sequences = midi_to_notes(os.path.join(data_dir, file), seq_length)
                all_sequences.extend(sequences)
            except Exception as e:
                print(f"Error procesando {file}: {e}")
    
    # Guardar secuencias preprocesadas
    np.save(os.path.join(output_dir, 'sequences.npy'), np.array(all_sequences))