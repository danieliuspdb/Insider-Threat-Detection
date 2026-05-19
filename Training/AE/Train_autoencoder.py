import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.callbacks import EarlyStopping
import joblib
import json

SCRIPT_DIR = 'Path'
INPUT_FILE = 'Path'
MODEL_FILE = 'Path'
SCALER_FILE = 'Path'

df = pd.read_excel(INPUT_FILE)

df = df.fillna(0)

print(f"Data shape: {df.shape}")
print(f"Features: {list(df.columns)}")

X = df.values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_val = train_test_split(X_scaled, test_size=0.2, random_state=42)

print(f"Training samples: {len(X_train)}")
print(f"Validation samples: {len(X_val)}")

input_dim = X_train.shape[1]

input_layer = Input(shape=(input_dim,))
encoded = Dense(64, activation='relu')(input_layer)
encoded = Dense(32, activation='relu')(encoded)
encoded = Dense(16, activation='relu')(encoded) 

decoded = Dense(32, activation='relu')(encoded)
decoded = Dense(64, activation='relu')(decoded)
output_layer = Dense(input_dim, activation='linear')(decoded)

autoencoder = Model(input_layer, output_layer)

autoencoder.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse')

autoencoder.summary()

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)

history = autoencoder.fit(
    X_train, X_train,
    epochs=100,
    batch_size=32,
    validation_data=(X_val, X_val),
    callbacks=[early_stop],
    verbose=1
)

log_dir = os.path.join(SCRIPT_DIR, "..", "graphs", "autoencoder")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "training_history.json")
with open(log_file, 'w') as f:
    json.dump(history.history, f, indent=2)

val_pred = autoencoder.predict(X_val)
val_mse = np.mean(np.power(X_val - val_pred, 2), axis=1)

print(f"Validation - Mean: {val_mse.mean():.6f}, Std: {val_mse.std():.6f}")
print(f"Threshold (mean + 2*std): {val_mse.mean() + 2*val_mse.std():.6f}")

autoencoder.save(MODEL_FILE)
joblib.dump(scaler, SCALER_FILE)

threshold = val_mse.mean() + 2 * val_mse.std()
np.save(os.path.join(SCRIPT_DIR, "..", "ML Model", "threshold.npy"), threshold)

print(f"\nModel saved to: {MODEL_FILE}")
print(f"Scaler saved to: {SCALER_FILE}")
print(f"Threshold: {threshold:.6f}")
