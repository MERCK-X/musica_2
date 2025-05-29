from src.data_processing.midi_processor import preprocess_dataset
from src.models.model_trainer import train_models

def main():
    # Preprocesar datos MIDI
    print("Preprocesando datos MIDI...")
    preprocess_dataset("data/midi", "data/processed")
    
    # Entrenar modelos
    print("Entrenando modelos...")
    train_models("data/processed/sequences.npy", "models")

if __name__ == "__main__":
    main()