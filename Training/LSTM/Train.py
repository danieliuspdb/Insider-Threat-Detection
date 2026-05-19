import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import joblib
import warnings
import json
warnings.filterwarnings('ignore')

np.random.seed(42)
tf.random.set_seed(42)

SCRIPT_DIR = 'Path'
INPUT_FILE = 'Path'
MODEL_DIR = 'Path'
MODEL_FILE = 'Path'
SCALER_FILE = 'Path'

SEQUENCE_LENGTH = 30
LSTM_UNITS = 64
LATENT_DIM = 32
EPOCHS = 50
BATCH_SIZE = 32
VALIDATION_SPLIT = 0.2

def create_sequences(df, user, sequence_length):
    user_data = df[df['user'] == user].sort_values('date')

    feature_cols = [col for col in user_data.columns if col not in ['user', 'date']]
    features = user_data[feature_cols].values

    if len(features) < sequence_length:
        return np.array([]), np.array([])

    X_sequences = []
    y_targets = []

    for i in range(len(features) - sequence_length + 1):
        X_sequences.append(features[i:i+sequence_length-1])
        y_targets.append(features[i+sequence_length-1])

    return np.array(X_sequences), np.array(y_targets)

def main():

    df = pd.read_excel(INPUT_FILE)

    if 'user' not in df.columns or 'date' not in df.columns:
        raise ValueError("Data must contain 'user' and 'date' columns")

    print(f"Total activity days: {len(df)}")
    print(f"Users: {df['user'].nunique()}")

    feature_cols = [col for col in df.columns if col not in ['user', 'date']]
    num_features = len(feature_cols)
    print(f"Features ({num_features}): {feature_cols[:5]}... (and {num_features-5} more)")

    print(f"\nCreating sequences ({SEQUENCE_LENGTH-1} days → predict day {SEQUENCE_LENGTH})...")
    all_X = []
    all_y = []

    users = df['user'].unique()
    valid_users = 0
    skipped_users = 0

    for user in users:
        X_seqs, y_targets = create_sequences(df, user, SEQUENCE_LENGTH)
        if len(X_seqs) > 0:
            all_X.append(X_seqs)
            all_y.append(y_targets)
            valid_users += 1
        else:
            skipped_users += 1

    print(f"Valid users: {valid_users}")
    print(f"Skipped users (<{SEQUENCE_LENGTH} days): {skipped_users}")

    X = np.concatenate(all_X, axis=0)
    y = np.concatenate(all_y, axis=0)

    print(f"\nTotal sequences: {len(X)}")
    print(f"X shape (input): {X.shape} - {SEQUENCE_LENGTH-1} days")
    print(f"y shape (target): {y.shape} - next day to predict")

    scaler = StandardScaler()

    all_data = np.concatenate([X.reshape(-1, num_features), y.reshape(-1, num_features)], axis=0)
    scaler.fit(all_data)

    X_reshaped = X.reshape(-1, num_features)
    X_scaled = scaler.transform(X_reshaped)
    X_scaled = X_scaled.reshape(-1, SEQUENCE_LENGTH-1, num_features)

    y_scaled = scaler.transform(y)

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(scaler, SCALER_FILE)

    print(f"  Input: {SEQUENCE_LENGTH-1} days")
    print(f"  Output: next day ({num_features} features)")

    inputs = layers.Input(shape=(SEQUENCE_LENGTH-1, num_features))
    lstm1 = layers.LSTM(LSTM_UNITS, activation='tanh', return_sequences=True)(inputs)
    dropout1 = layers.Dropout(0.2)(lstm1)
    lstm2 = layers.LSTM(LATENT_DIM, activation='tanh', return_sequences=False)(dropout1)
    dropout2 = layers.Dropout(0.2)(lstm2)
    outputs = layers.Dense(num_features)(dropout2)

    model = keras.Model(inputs, outputs)

    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']
    )

    print(model.summary())

    print(f"Task: Predict day {SEQUENCE_LENGTH} from days 1-{SEQUENCE_LENGTH-1}")
    history = model.fit(
        X_scaled, y_scaled,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_split=VALIDATION_SPLIT,
        verbose=1,
        shuffle=True,
        callbacks=[
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-6
            )
        ]
    )

    log_dir = os.path.join(SCRIPT_DIR, "..", "..", "graphs", "lstm")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "training_history.json")
    with open(log_file, 'w') as f:
        json.dump(history.history, f, indent=2)

    model.save(MODEL_FILE)
    print(f"\nModel saved to {MODEL_FILE}")

    train_loss = history.history['loss'][-1]
    val_loss = history.history['val_loss'][-1]
    print(f"\nFinal Training Loss (prediction error): {train_loss:.6f}")
    print(f"Final Validation Loss: {val_loss:.6f}")

if __name__ == "__main__":
    main()
