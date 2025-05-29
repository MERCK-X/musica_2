import numpy as np
from tensorflow.keras.utils import to_categorical
from .cnn_model import build_cnn_model
from .transformer_model import build_transformer_model

def prepare_data(sequences):
    """Prepara los datos para el entrenamiento"""
    X = []
    y = []
    
    for seq in sequences:
        pitches = [note['pitch'] for note in seq]
        X.append(pitches[:-1])
        y.append(pitches[-1])
    
    X = np.array(X)
    y = to_categorical(np.array(y), num_classes=128)
    
    return X, y

def train_models(data_path, model_save_path):
    """Entrena ambos modelos y los guarda"""
    sequences = np.load(data_path, allow_pickle=True)
    X, y = prepare_data(sequences)
    
    # Entrenar CNN
    cnn_model = build_cnn_model((X.shape[1], 1))
    cnn_model.fit(X, y, epochs=50, batch_size=64, validation_split=0.2)
    cnn_model.save(f"{model_save_path}/cnn_model.h5")
    
    # Entrenar Transformer
    transformer_model = build_transformer_model((X.shape[1],))
    transformer_model.compile(optimizer='adam', loss='categorical_crossentropy')
    transformer_model.fit(X, y, epochs=50, batch_size=64, validation_split=0.2)
    transformer_model.save(f"{model_save_path}/transformer_model.h5")