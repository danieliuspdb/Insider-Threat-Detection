import os
import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import warnings
warnings.filterwarnings('ignore')

SCRIPT_DIR = 'Path'
BASE_DIR = 'Path'

TEST_FEATURES = 'Path'
INSIDERS_FILE = 'Path'

MODEL_FILE = 'Path'
SCALER_FILE = 'Path'

OUTPUT_FILE = 'Path'

SEQUENCE_LENGTH = 30

HIGH_PERCENTILE = 99.9
LOW_PERCENTILE = 95.0
USER_PERCENTILE = 97.0
USB_ZSCORE_THR = 3.0

def create_sequences_with_metadata(df, user, sequence_length):
    user_data = df[df['user'] == user].sort_values('date')

    if len(user_data) < sequence_length:
        return None

    feature_cols = [col for col in user_data.columns if col not in ['user', 'date']]
    features = user_data[feature_cols].values
    dates = user_data['date'].values

    X_sequences = []
    y_targets = []
    y_dates = []

    for i in range(len(features) - sequence_length + 1):
        X_sequences.append(features[i:i+sequence_length-1])
        y_targets.append(features[i+sequence_length-1])
        y_dates.append(dates[i+sequence_length-1])

    return {
        'X': np.array(X_sequences),
        'y': np.array(y_targets),
        'dates': y_dates,
        'user': user
    }

def main():
    print("=" * 70)
    print("REAL LSTM - Evaluation")
    print("Next-day prediction error for anomaly detection")
    print("=" * 70)

    model = load_model(MODEL_FILE, compile=False)
    scaler = joblib.load(SCALER_FILE)

    df = pd.read_excel(TEST_FEATURES).fillna(0)

    if 'user' not in df.columns or 'date' not in df.columns:
        raise ValueError("Test data must contain 'user' and 'date' columns")

    print(f"Total activity days: {len(df)}")
    print(f"Unique users: {df['user'].nunique()}")

    feature_cols = [col for col in df.columns if col not in ['user', 'date']]
    num_features = len(feature_cols)
    print(f"Features per timestep: {num_features}")

    df_with_user_date = df.copy()

    print(f"\nCreating sequences (length={SEQUENCE_LENGTH})...")
    all_results = []

    users = df['user'].unique()
    valid_users = 0
    skipped_users = 0

    for user in users:
        seq_data = create_sequences_with_metadata(df, user, SEQUENCE_LENGTH)

        if seq_data is None:
            skipped_users += 1
            continue

        valid_users += 1
        X_seqs = seq_data['X']
        y_targets = seq_data['y']
        y_dates = seq_data['dates']

        X_reshaped = X_seqs.reshape(-1, num_features)
        X_scaled = scaler.transform(X_reshaped)
        X_scaled = X_scaled.reshape(-1, SEQUENCE_LENGTH-1, num_features)

        y_scaled = scaler.transform(y_targets)

        y_pred = model.predict(X_scaled, verbose=0)

        prediction_errors = np.mean(np.power(y_scaled - y_pred, 2), axis=1)

        for seq_idx, (date, error) in enumerate(zip(y_dates, prediction_errors)):
            all_results.append({
                'user': user,
                'date': date,
                'error': error,
                'sequence_idx': seq_idx
            })

    print(f"Valid users: {valid_users}")
    print(f"Skipped users (<{SEQUENCE_LENGTH} days): {skipped_users}")

    error_df = pd.DataFrame(all_results)

    print(f"\nPredictions made: {len(error_df)}")
    print(f"Unique users: {error_df['user'].nunique()}")

    df_usb = df_with_user_date[['user', 'date', 'usb_zscore']].copy()
    error_df = error_df.merge(df_usb, on=['user', 'date'], how='left')
    error_df['usb_zscore'] = error_df['usb_zscore'].fillna(0)

    errors = error_df['error'].values
    high_thr = float(np.quantile(errors, HIGH_PERCENTILE / 100.0))
    low_thr = float(np.quantile(errors, LOW_PERCENTILE / 100.0))

    error_df['user_p_thr'] = error_df.groupby('user')['error'].transform(
        lambda x: np.quantile(x, USER_PERCENTILE / 100.0)
    )

    error_df['day_flagged'] = (
        (error_df['error'] >= high_thr) |
        ((error_df['error'] >= low_thr) & (error_df['error'] < high_thr) &
         (error_df['error'] >= error_df['user_p_thr']) & (error_df['usb_zscore'] > USB_ZSCORE_THR))
    )

    print(f"\nHigh threshold (P{HIGH_PERCENTILE}): {high_thr:.6f}")
    print(f"Low threshold (P{LOW_PERCENTILE}): {low_thr:.6f}")
    print(f"Days flagged: {error_df['day_flagged'].sum()}")

    flagged_users = set(error_df.loc[error_df['day_flagged'], 'user'].unique())
    print(f"Users flagged: {len(flagged_users)}")

    insiders = set(pd.read_csv(INSIDERS_FILE)['user'].astype(str).unique())
    actual_insiders = insiders & set(error_df['user'].unique())

    tp = len(flagged_users & actual_insiders)
    fp = len(flagged_users - actual_insiders)
    fn = len(actual_insiders - flagged_users)

    total_flagged = len(flagged_users)
    total_insiders = len(actual_insiders)

    precision = 100 * tp / total_flagged if total_flagged else 0.0
    recall = 100 * tp / total_insiders if total_insiders else 0.0
    fp_rate = 100 * fp / total_flagged if total_flagged else 0.0

    print("\n" + "=" * 70)
    print("=" * 70)
    print(f"High: P{HIGH_PERCENTILE} | Low: P{LOW_PERCENTILE} + user P{USER_PERCENTILE} + USB>{USB_ZSCORE_THR}")
    print("-" * 70)
    print(f"Insiders caught: {tp} / {total_insiders} ({recall:.1f}%)")
    print(f"False positives: {fp} / {total_flagged} ({fp_rate:.1f}%)")
    print(f"Precision: {precision:.1f}%")
    print(f"Insiders missed: {fn}")
    print(f"Missed insiders: {actual_insiders - flagged_users}")
    print("=" * 70)

    error_df['is_insider'] = error_df['user'].isin(insiders)
    out_cols = ['user', 'date', 'error', 'usb_zscore', 'day_flagged', 'is_insider']
    out = error_df[out_cols].sort_values('error', ascending=False)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    out.to_excel(OUTPUT_FILE, index=False)
    print(f"\nSaved results to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
