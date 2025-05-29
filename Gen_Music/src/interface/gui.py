import PySimpleGUI as sg
import numpy as np
from ..models.cnn_model import build_cnn_model
from ..models.transformer_model import build_transformer_model
from ..utils.audio_utils import generate_audio_from_predictions

def create_ai_gui(models):
    sg.theme('DarkAmber')
    
    layout = [
        [sg.Text("Generador de Melodías con IA", font=("Helvetica", 16))],
        [sg.Text("Modelo:"), 
         sg.Combo(['CNN', 'Transformer'], default_value='CNN', key='-MODEL-')],
        [sg.Text("Semilla musical (notas iniciales separadas por comas):")],
        [sg.Multiline(size=(50, 5), key='-SEED-')],
        [sg.Text("Longitud de la melodía:"), 
         sg.Slider(range=(4, 64), default_value=16, orientation='h', key='-LENGTH-')],
        [sg.Button("Generar"), sg.Button("Salir")],
        [sg.Text("", size=(50, 1), key='-STATUS-')],
        [sg.ProgressBar(100, orientation='h', size=(50, 20), key='-PROGRESS-')]
    ]
    
    return sg.Window('Generador de Melodías con IA', layout)

def generate_melody(model, seed_notes, length):
    """Genera una melodía usando el modelo seleccionado"""
    # Preprocesar las notas semilla
    seed_sequence = process_seed_notes(seed_notes)
    
    # Generar predicciones
    predictions = []
    current_sequence = seed_sequence.copy()
    
    for i in range(length):
        # Predecir la siguiente nota
        prediction = model.predict(np.array([current_sequence]))[0]
        predicted_note = np.argmax(prediction)
        
        predictions.append(predicted_note)
        current_sequence = np.append(current_sequence[1:], predicted_note)
    
    return predictions