import os
import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

SCRIPT_DIR = 'Path'
PARENT_DIR = 'Path'

TEST_FEATURES = 'Path'
INSIDERS_FILE = 'Path'

MODEL_FILE = 'Path'
SCALER_FILE = 'Path'

OUTPUT_FILE = 'Path'

HIGH_PERCENTILE = 99.9
LOW_PERCENTILE = 95.0
USER_PERCENTILE = 97.0
USB_ZSCORE_THR = 3.0

model = load_model(MODEL_FILE, compile=False)
scaler = joblib.load(SCALER_FILE)

df = pd.read_excel(TEST_FEATURES).fillna(0)

if "user" not in df.columns:
    raise ValueError("test_features.xlsx must contain a 'user' column")

users = df["user"].astype(str)
feature_cols = [c for c in df.columns if c != "user"]

expected = int(getattr(scaler, "n_features_in_", len(feature_cols)))
if len(feature_cols) != expected:
    print(f"[WARN] Scaler expects {expected} features, data has {len(feature_cols)}.")
    feature_cols = feature_cols[:expected]

X = scaler.transform(df[feature_cols].values)

pred = model.predict(X, verbose=0)
errors = np.mean(np.power(X - pred, 2), axis=1)

error_df = pd.DataFrame({
    "user": users.values,
    "error": errors
})

print(f"Rows evaluated: {len(error_df)}")
print(f"Unique users:   {error_df['user'].nunique()}")

high_thr = float(np.quantile(errors, HIGH_PERCENTILE / 100.0))
low_thr = float(np.quantile(errors, LOW_PERCENTILE / 100.0))

error_df["usb_zscore"] = df["usb_zscore"].values

error_df["user_p97"] = error_df.groupby("user")["error"].transform(lambda x: np.quantile(x, USER_PERCENTILE/100.0))

error_df["day_flagged"] = (
    (error_df["error"] >= high_thr) |
    ((error_df["error"] >= low_thr) & (error_df["error"] < high_thr) &
     (error_df["error"] >= error_df["user_p97"]) & (error_df["usb_zscore"] > USB_ZSCORE_THR))
)

print(f"High threshold (P{HIGH_PERCENTILE}): {high_thr:.6f}")
print(f"Low threshold (P{LOW_PERCENTILE}): {low_thr:.6f}")
print(f"Days flagged: {error_df['day_flagged'].sum()}")

flagged_users = set(error_df.loc[error_df["day_flagged"], "user"].unique())
print(f"Users flagged: {len(flagged_users)}")

insiders = set(pd.read_csv(INSIDERS_FILE)["user"].astype(str).unique())

actual_insiders = insiders & set(users.unique())

tp = len(flagged_users & actual_insiders)
fp = len(flagged_users - actual_insiders)
fn = len(actual_insiders - flagged_users)

total_flagged = len(flagged_users)
total_insiders = len(actual_insiders)

precision = 100 * tp / total_flagged if total_flagged else 0.0
recall = 100 * tp / total_insiders if total_insiders else 0.0
fp_rate = 100 * fp / total_flagged if total_flagged else 0.0

print("\n" + "=" * 60)
print("RESULTS (Two-tier threshold)")
print("=" * 60)
print(f"High: P{HIGH_PERCENTILE} | Low: P{LOW_PERCENTILE} + user P{USER_PERCENTILE} + USB>{USB_ZSCORE_THR}")
print("-" * 60)
print(f"Insiders caught: {tp} / {total_insiders} ({recall:.1f}%)")
print(f"False positives: {fp} / {total_flagged} ({fp_rate:.1f}%)")
print(f"Precision: {precision:.1f}%")
print(f"Insiders missed: {fn}")
print(f"Missed insiders: {actual_insiders - flagged_users}")
print("=" * 60)

error_df["is_insider"] = error_df["user"].isin(insiders)

out_cols = ["user", "error", "usb_zscore", "day_flagged", "is_insider"]
out = error_df[out_cols].sort_values("error", ascending=False)

out.to_excel(OUTPUT_FILE, index=False)
print(f"\nSaved results to: {OUTPUT_FILE}")
