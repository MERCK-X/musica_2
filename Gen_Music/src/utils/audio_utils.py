import os
import numpy as np
from pydub import AudioSegment, effects
from pydub.generators import Sine, Sawtooth, Square, Pulse
import pretty_midi
from datetime import datetime
from typing import Union, List, Optional
import tempfile
import soundfile as sf

def generate_audio_from_predictions(
    predictions: Union[List[int], np.ndarray],
    output_dir: str = "audio_output",
    instrument_type: str = "piano",
    tempo: int = 120,
    note_duration: float = 0.5,
    velocity: int = 100,
    format: str = "mp3"
) -> str:
    """
    Genera un archivo de audio a partir de predicciones de notas MIDI
    
    Args:
        predictions: Lista de valores MIDI (0-127)
        output_dir: Directorio de salida
        instrument_type: Tipo de instrumento (piano, synth, etc.)
        tempo: Tempo en BPM
        note_duration: Duración de cada nota en segundos
        velocity: Velocidad de las notas (0-127)
        format: Formato de salida (mp3, wav)
        
    Returns:
        Ruta al archivo generado
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Crear objeto PrettyMIDI
    pm = pretty_midi.PrettyMIDI()
    
    # Seleccionar instrumento según tipo
    program = {
        "piano": 0,
        "synth": 80,
        "guitar": 24,
        "strings": 48,
        "bass": 32
    }.get(instrument_type.lower(), 0)
    
    instrument = pretty_midi.Instrument(program=program)
    
    # Calcular tiempo por beat según tempo
    beat_duration = 60.0 / tempo
    
    # Añadir notas al instrumento
    current_time = 0.0
    for pitch in predictions:
        if 0 <= pitch <= 127:  # Rango válido MIDI
            note = pretty_midi.Note(
                velocity=velocity,
                pitch=int(pitch),
                start=current_time,
                end=current_time + note_duration * beat_duration
            )
            instrument.notes.append(note)
        current_time += note_duration * beat_duration
    
    pm.instruments.append(instrument)
    
    # Guardar archivo MIDI temporal
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    midi_path = os.path.join(tempfile.gettempdir(), f"temp_{timestamp}.mid")
    pm.write(midi_path)
    
    # Convertir a formato de audio deseado
    output_path = os.path.join(output_dir, f"melody_{timestamp}.{format}")
    midi_to_mp3(midi_path, output_path)
    
    # Limpiar archivo temporal
    os.remove(midi_path)
    
    return output_path

def midi_to_mp3(midi_path: str, output_path: str) -> None:
    """
    Convierte un archivo MIDI a MP3 usando soundfont
    
    Args:
        midi_path: Ruta al archivo MIDI
        output_path: Ruta de salida para el MP3
    """
    try:
        # Usar soundfont para mejor calidad
        soundfont = "/usr/share/sounds/sf2/FluidR3_GM.sf2"  # Ajustar según sistema
        
        if os.path.exists(soundfont):
            # Convertir usando fluidsynth si está disponible
            os.system(f"fluidsynth -ni {soundfont} {midi_path} -F {output_path} -r 44100")
            
            # Normalizar volumen
            normalize_audio(output_path)
        else:
            # Conversión básica si no hay soundfont
            midi_audio = AudioSegment.from_file(midi_path, format="mid")
            midi_audio.export(output_path, format="mp3", bitrate="192k")
    except Exception as e:
        print(f"Error convirtiendo MIDI a MP3: {str(e)}")
        raise

def normalize_audio(file_path: str, target_dBFS: float = -20.0) -> None:
    """
    Normaliza el volumen de un archivo de audio
    
    Args:
        file_path: Ruta al archivo de audio
        target_dBFS: Nivel de volumen objetivo
    """
    try:
        audio = AudioSegment.from_file(file_path)
        change_in_dBFS = target_dBFS - audio.dBFS
        normalized = audio.apply_gain(change_in_dBFS)
        normalized.export(file_path, format=file_path.split('.')[-1])
    except Exception as e:
        print(f"Error normalizando audio: {str(e)}")

def concatenate_audio_files(file_paths: List[str], output_path: str) -> None:
    """
    Concatena múltiples archivos de audio en uno solo
    
    Args:
        file_paths: Lista de rutas a archivos de audio
        output_path: Ruta de salida para el archivo concatenado
    """
    if not file_paths:
        return
        
    combined = AudioSegment.empty()
    for file_path in file_paths:
        sound = AudioSegment.from_file(file_path)
        combined += sound
    
    combined.export(output_path, format=output_path.split('.')[-1])

def generate_waveform(
    frequency: float,
    duration: float,
    sample_rate: int = 44100,
    wave_type: str = "sine",
    volume: float = 0.8
) -> np.ndarray:
    """
    Genera una forma de onda de audio
    
    Args:
        frequency: Frecuencia en Hz
        duration: Duración en segundos
        sample_rate: Tasa de muestreo
        wave_type: Tipo de onda (sine, square, sawtooth, pulse)
        volume: Volumen (0.0 a 1.0)
        
    Returns:
        Array numpy con la forma de onda
    """
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    if wave_type == "sine":
        wave = np.sin(2 * np.pi * frequency * t)
    elif wave_type == "square":
        wave = np.sign(np.sin(2 * np.pi * frequency * t))
    elif wave_type == "sawtooth":
        wave = 2 * (t * frequency - np.floor(0.5 + t * frequency))
    elif wave_type == "pulse":
        wave = np.where(np.sin(2 * np.pi * frequency * t) > 0, 1, -1)
    else:
        raise ValueError("Tipo de onda no soportado")
    
    return wave * volume