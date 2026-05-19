
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split

BASE = '..'
AE_RESULTS = 'Path'
LSTM_RESULTS = 'Path'
INSIDERS_FILE = 'Path'
OUTPUT_TRAIN = 'Path'
OUTPUT_TEST = 'Path'

ae_df = pd.read_excel(AE_RESULTS)
lstm_df = pd.read_excel(LSTM_RESULTS)

ae_per_user = ae_df.groupby('user').agg({
    'error': ['max', 'mean', 'std']
}).fillna(0)
ae_per_user.columns = ['error_ae_max', 'error_ae_mean', 'error_ae_std']
ae_per_user = ae_per_user.reset_index()

lstm_per_user = lstm_df.groupby('user').agg({
    'error': ['max', 'mean', 'std'],
    'usb_zscore': ['max', 'mean', 'std']
}).fillna(0)
lstm_per_user.columns = ['error_lstm_max', 'error_lstm_mean', 'error_lstm_std',
                          'usb_zscore_max', 'usb_zscore_mean', 'usb_zscore_std']
lstm_per_user = lstm_per_user.reset_index()

user_features = lstm_per_user.merge(ae_per_user, on='user', how='inner')

insiders = set(pd.read_csv(INSIDERS_FILE)['user'].astype(str).unique())
user_features['label'] = user_features['user'].isin(insiders).astype(int)

train_df, test_df = train_test_split(
    user_features,
    test_size=0.3,
    random_state=42,
    stratify=user_features['label']
)

train_df.to_excel(OUTPUT_TRAIN, index=False)
test_df.to_excel(OUTPUT_TEST, index=False)