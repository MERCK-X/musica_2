from interface.gui import create_ai_gui
from models.cnn_model import build_cnn_model
from models.transformer_model import build_transformer_model
from utils.audio_utils import generate_audio_from_predictions
import tensorflow as tf
import numpy as np

def load_models():
    """Carga los modelos preentrenados"""
    try:
        cnn_model = tf.keras.models.load_model("models/cnn_model.h5")
        transformer_model = tf.keras.models.load_model("models/transformer_model.h5")
        return {
            'CNN': cnn_model,
            'Transformer': transformer_model
        }
    except Exception as e:
        print(f"Error cargando modelos: {e}")
        return None

def main():
    # Cargar modelos
    models = load_models()
    if not models:
        print("No se pudieron cargar los modelos. Ejecuta train.py primero.")
        return
    
    # Crear interfaz
    window = create_ai_gui(models)
    
    while True:
        event, values = window.read()
        
        if event == "Generar" and values['-SEED-']:
            try:
                window['-STATUS-'].update("Generando melodía...")
                window['-PROGRESS-'].update(0)
                
                # Seleccionar modelo
                model_type = values['-MODEL-']
                model = models[model_type]
                
                # Generar melodía
                length = int(values['-LENGTH-'])
                predictions = generate_melody(model, values['-SEED-'], length)
                window['-PROGRESS-'].update(50)
                
                # Generar audio
                output_path = generate_audio_from_predictions(predictions)
                window['-PROGRESS-'].update(100)
                window['-STATUS-'].update(f"Audio generado: {output_path}")
                
            except Exception as e:
                window['-STATUS-'].update(f"Error: {str(e)}")
                
        elif event == "Salir" or event == None:
            break
            
    window.close()

if __name__ == "__main__":
    main()