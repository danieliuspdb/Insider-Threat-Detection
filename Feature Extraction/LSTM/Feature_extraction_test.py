import pandas as pd
import numpy as np
from collections import defaultdict
import os
import warnings
warnings.filterwarnings('ignore')

SCRIPT_DIR = 'Path'
BASE_PATH = 'Path'
OUTPUT_FILE = 'Path'

MAX_ROWS = 300000
OFF_HOURS_START = 20
OFF_HOURS_END = 6
SENSITIVE = ['confidential', 'secret', 'private', 'classified', 'password', 'financial']

def is_off_hours(hour):
    return hour >= OFF_HOURS_START or hour < OFF_HOURS_END

def main():
    user_day_data = defaultdict(lambda: {
        'usb_count': 0,
        'files_count': 0,
        'sensitive_count': 0,
        'emails_sent_count': 0,
        'external_email_count': 0,
        'attachment_count': 0,
        'http_count': 0,
        'off_hours_flag': 0,
    })

    logon_df = pd.read_csv(os.path.join(BASE_PATH, "logon.csv"), nrows=MAX_ROWS)
    logon_df['datetime'] = pd.to_datetime(logon_df['date'], format='%m/%d/%Y %H:%M:%S', errors='coerce')
    logon_df['date_only'] = logon_df['datetime'].dt.date

    for _, row in logon_df.iterrows():
        if pd.isna(row['date_only']): continue
        key = (row['user'], row['date_only'])
        if row['activity'] == 'Logon' and pd.notna(row['datetime']) and is_off_hours(row['datetime'].hour):
            user_day_data[key]['off_hours_flag'] = 1
    del logon_df

    email_df = pd.read_csv(os.path.join(BASE_PATH, "email.csv"), nrows=MAX_ROWS)
    email_df['datetime'] = pd.to_datetime(email_df['date'], format='%m/%d/%Y %H:%M:%S', errors='coerce')
    email_df['date_only'] = email_df['datetime'].dt.date

    for _, row in email_df.iterrows():
        if pd.isna(row['date_only']): continue
        key = (row['user'], row['date_only'])

        user_day_data[key]['emails_sent_count'] += 1

        if pd.notna(row.get('attachments')) and str(row['attachments']).strip():
            attach_count = len(str(row['attachments']).split(';'))
            user_day_data[key]['attachment_count'] += attach_count

        is_external = False
        for field in ['to', 'cc', 'bcc']:
            if pd.notna(row.get(field)) and '@dtaa.com' not in str(row[field]).lower():
                is_external = True
                break
        if is_external:
            user_day_data[key]['external_email_count'] += 1
    del email_df

    http_df = pd.read_csv(os.path.join(BASE_PATH, "http.csv"), nrows=MAX_ROWS)
    http_df['datetime'] = pd.to_datetime(http_df['date'], format='%m/%d/%Y %H:%M:%S', errors='coerce')
    http_df['date_only'] = http_df['datetime'].dt.date

    for _, row in http_df.iterrows():
        if pd.isna(row['date_only']): continue
        key = (row['user'], row['date_only'])
        user_day_data[key]['http_count'] += 1
    del http_df

    file_df = pd.read_csv(os.path.join(BASE_PATH, "file.csv"), nrows=MAX_ROWS)
    file_df['datetime'] = pd.to_datetime(file_df['date'], format='%m/%d/%Y %H:%M:%S', errors='coerce')
    file_df['date_only'] = file_df['datetime'].dt.date

    for _, row in file_df.iterrows():
        if pd.isna(row['date_only']): continue
        key = (row['user'], row['date_only'])
        user_day_data[key]['files_count'] += 1
        filename = str(row.get('filename', '')).lower()
        if any(k in filename for k in SENSITIVE):
            user_day_data[key]['sensitive_count'] += 1
    del file_df

    device_df = pd.read_csv(os.path.join(BASE_PATH, "device.csv"), nrows=MAX_ROWS)
    device_df['datetime'] = pd.to_datetime(device_df['date'], format='%m/%d/%Y %H:%M:%S', errors='coerce')
    device_df['date_only'] = device_df['datetime'].dt.date

    for _, row in device_df.iterrows():
        if pd.isna(row['date_only']): continue
        key = (row['user'], row['date_only'])
        if row['activity'] == 'Connect':
            user_day_data[key]['usb_count'] += 1
    del device_df

    results = []
    for (user, date), data in user_day_data.items():
        results.append({
            'user': user,
            'date': date,  # Keep date for LSTM sequencing
            'usb_insert_count': data['usb_count'],
            'files_accessed_count': data['files_count'],
            'sensitive_file_count': data['sensitive_count'],
            'emails_sent_count': data['emails_sent_count'],
            'external_email_count': data['external_email_count'],
            'attachment_count': data['attachment_count'],
            'http_count': data['http_count'],
            'after_hours_flag': data['off_hours_flag'],
        })

    df = pd.DataFrame(results)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(['user', 'date']).reset_index(drop=True)

    # Initialize statistical features
    df['avg_30d_files_accessed'] = 0.0
    df['avg_30d_usb_insertions'] = 0.0
    df['usb_zscore'] = 0.0
    df['files_zscore'] = 0.0
    df['sensitive_zscore'] = 0.0
    df['consecutive_anomaly_usb'] = 0
    df['usb_first_seen_30d'] = 0
    df['sensitive_ratio'] = 0.0
    df['spike_7d_usb'] = 0.0

    for user in df['user'].unique():
        mask = df['user'] == user
        ud = df.loc[mask].copy()
        indices = ud.index

        # 30-day rolling averages
        df.loc[indices, 'avg_30d_files_accessed'] = ud['files_accessed_count'].rolling(window=30, min_periods=1).mean().values
        df.loc[indices, 'avg_30d_usb_insertions'] = ud['usb_insert_count'].rolling(window=30, min_periods=1).mean().values

        # Z-scores (per-user standardization)
        for src, dst in [('usb_insert_count', 'usb_zscore'),
                         ('files_accessed_count', 'files_zscore'),
                         ('sensitive_file_count', 'sensitive_zscore')]:
            if ud[src].std() > 0:
                df.loc[indices, dst] = ((ud[src] - ud[src].mean()) / ud[src].std()).round(2)

        # Consecutive USB anomalies
        usb_zscores = df.loc[indices, 'usb_zscore'].values
        consecutive = 0
        consec_values = []
        for z in usb_zscores:
            if z > 2:
                consecutive += 1
            else:
                consecutive = 0
            consec_values.append(consecutive)
        df.loc[indices, 'consecutive_anomaly_usb'] = consec_values

        # USB first seen in 30 days
        usb_counts = ud['usb_insert_count'].values
        usb_first_seen = []
        for i in range(len(usb_counts)):
            if usb_counts[i] > 0:
                start = max(0, i - 30)
                prev_usb = usb_counts[start:i].sum() if i > 0 else 0
                usb_first_seen.append(1 if prev_usb == 0 else 0)
            else:
                usb_first_seen.append(0)
        df.loc[indices, 'usb_first_seen_30d'] = usb_first_seen

        # 7-day USB spike detection
        epsilon = 0.001
        usb_series = ud['usb_insert_count']
        avg_7d = usb_series.rolling(window=7, min_periods=1).mean().shift(1).fillna(0)
        std_7d = usb_series.rolling(window=7, min_periods=1).std().shift(1).fillna(0)
        spike_7d = (usb_series.values - avg_7d.values) / (std_7d.values + epsilon)
        df.loc[indices, 'spike_7d_usb'] = np.round(spike_7d, 2)

    # Ratios and weighted features
    df['sensitive_ratio'] = (df['sensitive_file_count'] / (df['files_accessed_count'] + 1)).round(4)
    df['after_hours_weighted'] = df['after_hours_flag'] * 2.0
    df['consecutive_anomaly_weighted'] = df['consecutive_anomaly_usb'] * 2.0

    # Final column selection (keep user and date for LSTM)
    feature_columns = [
        'user',
        'date',
        'usb_insert_count',
        'files_accessed_count',
        'sensitive_file_count',
        'emails_sent_count',
        'external_email_count',
        'attachment_count',
        'http_count',
        'after_hours_flag',
        'avg_30d_files_accessed',
        'avg_30d_usb_insertions',
        'usb_zscore',
        'files_zscore',
        'sensitive_zscore',
        'consecutive_anomaly_usb',
        'usb_first_seen_30d',
        'sensitive_ratio',
        'spike_7d_usb',
        'after_hours_weighted',
        'consecutive_anomaly_weighted',
    ]

    df = df[feature_columns]
    df = df.fillna(0)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    print(f"\nSaving to {OUTPUT_FILE}...")
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"DONE Rows: {len(df)}, Users: {df['user'].nunique()}, Features: {len(df.columns)-2} (+ user + date)")

    return df

if __name__ == "__main__":
    main()
