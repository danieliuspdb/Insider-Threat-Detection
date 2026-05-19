import os
import pandas as pd
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(SCRIPT_DIR, "..", "..")

AUTOENCODER_RESULTS = 'Path'
LSTM_RESULTS = 'Path'
INSIDERS_FILE = 'Path'

OUTPUT_FILE = 'Path'

autoencoder_df = pd.read_excel(AUTOENCODER_RESULTS)

lstm_df = pd.read_excel(LSTM_RESULTS)

has_date = 'date' in autoencoder_df.columns and 'date' in lstm_df.columns

if has_date:
    merge_cols = ['user', 'date']
else:
    merge_cols = ['user']

merged = autoencoder_df.merge(
    lstm_df[merge_cols + ['error', 'day_flagged']],
    on=merge_cols,
    how='outer',
    suffixes=('_autoencoder', '_lstm')
)

merged['error_autoencoder'] = merged['error_autoencoder'].fillna(0)
merged['error_lstm'] = merged['error_lstm'].fillna(0)
merged['day_flagged_autoencoder'] = merged['day_flagged_autoencoder'].fillna(False)
merged['day_flagged_lstm'] = merged['day_flagged_lstm'].fillna(False)

merged['ensemble_OR'] = merged['day_flagged_autoencoder'] | merged['day_flagged_lstm']

merged['ensemble_AND'] = merged['day_flagged_autoencoder'] & merged['day_flagged_lstm']

merged['ensemble_weighted_error'] = 0.5 * merged['error_autoencoder'] + 0.5 * merged['error_lstm']

merged['ensemble_max_error'] = merged[['error_autoencoder', 'error_lstm']].max(axis=1)

error_threshold = np.percentile(merged['ensemble_weighted_error'], 99.0)
merged['ensemble_weighted_flag'] = merged['ensemble_weighted_error'] >= error_threshold

insiders = set(pd.read_csv(INSIDERS_FILE)['user'].astype(str).unique())
merged['is_insider'] = merged['user'].isin(insiders)

print("\n" + "=" * 70)
print("ENSEMBLE EVALUATION RESULTS")
print("=" * 70)

methods = [
    ('Autoencoder Only', 'day_flagged_autoencoder'),
    ('LSTM Only', 'day_flagged_lstm'),
    ('Ensemble OR (either flags)', 'ensemble_OR'),
    ('Ensemble AND (both flag)', 'ensemble_AND'),
    ('Ensemble Weighted Error', 'ensemble_weighted_flag')
]

for method_name, flag_col in methods:
    flagged_users = set(merged.loc[merged[flag_col], 'user'].unique())
    actual_insiders = insiders & set(merged['user'].unique())

    tp = len(flagged_users & actual_insiders)
    fp = len(flagged_users - actual_insiders)
    fn = len(actual_insiders - flagged_users)

    total_flagged = len(flagged_users)
    total_insiders = len(actual_insiders)

    precision = 100 * tp / total_flagged if total_flagged else 0.0
    recall = 100 * tp / total_insiders if total_insiders else 0.0

    print(f"\n{method_name}:")
    print(f"  Users flagged: {total_flagged}")
    print(f"  Insiders caught: {tp}/{total_insiders} ({recall:.1f}%)")
    print(f"  False positives: {fp} ({100*fp/total_flagged if total_flagged else 0:.1f}%)")
    print(f"  Precision: {precision:.1f}%")
    print(f"  Missed: {actual_insiders - flagged_users}")

print("=" * 70)

output_cols = [
    'user', 'error_autoencoder', 'error_lstm',
    'day_flagged_autoencoder', 'day_flagged_lstm',
    'ensemble_OR', 'ensemble_AND', 'ensemble_weighted_error',
    'ensemble_weighted_flag', 'is_insider'
]
if has_date:
    output_cols.insert(1, 'date')

user_agg = merged.groupby('user').agg({
    'error_autoencoder': 'max',
    'error_lstm': 'max',
    'day_flagged_autoencoder': 'max',
    'day_flagged_lstm': 'max',
    'ensemble_OR': 'max',
    'ensemble_AND': 'max',
    'ensemble_weighted_error': 'max',
    'ensemble_weighted_flag': 'max',
    'is_insider': 'first'
}).reset_index()

user_agg.sort_values('ensemble_weighted_error', ascending=False).to_excel(OUTPUT_FILE, index=False)
print(f"\nResults saved to: {OUTPUT_FILE}")
