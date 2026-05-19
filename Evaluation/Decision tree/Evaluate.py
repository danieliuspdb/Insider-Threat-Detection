import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import classification_report, confusion_matrix, average_precision_score, roc_auc_score
import os

INPUT_TEST = 'Path'
MODEL_FILE = 'Path'
OUTPUT = 'Path'

BASE = '..'
INSIDERS_FILE = 'Path'

model_data = joblib.load(MODEL_FILE)
model = model_data['model']
feature_names = model_data['feature_names']
threshold = model_data['threshold']
cv_results = model_data['cv_results']
train_users = set(model_data['train_users'])

test_df = pd.read_excel(INPUT_TEST)
test_users = set(test_df['user'])

X_test = test_df[feature_names].values
y_test = test_df['label'].values

probs = model.predict_proba(X_test)[:, 1]
preds = (probs >= threshold).astype(int)

test_df['prob'] = probs
test_df['pred'] = preds

test_pr_auc = average_precision_score(y_test, probs)
test_roc_auc = roc_auc_score(y_test, probs)

flagged_users = set(test_df[preds == 1]['user'])
insiders = set(pd.read_csv(INSIDERS_FILE)['user'].astype(str).unique())
test_insiders = insiders & test_users

tp = len(flagged_users & test_insiders)
fp = len(flagged_users - test_insiders)
fn = len(test_insiders - flagged_users)
tn = len(test_users) - tp - fp - fn

precision = 100 * tp / len(flagged_users) if flagged_users else 0
recall = 100 * tp / len(test_insiders) if test_insiders else 0
f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0
fp_rate = 100 * fp / (fp + tn) if (fp + tn) > 0 else 0

test_df.to_excel(OUTPUT, index=False)

summary = pd.DataFrame([{
    'split': 'test',
    'total_users': len(test_users),
    'insiders': len(test_insiders),
    'users_flagged': len(flagged_users),
    'true_positives': tp,
    'false_positives': fp,
    'true_negatives': tn,
    'false_negatives': fn,
    'precision': precision,
    'recall': recall,
    'f1_score': f1,
    'fp_rate': fp_rate,
    'pr_auc': test_pr_auc,
    'roc_auc': test_roc_auc,
    'cv_mean_pr_auc': np.mean([r['pr_auc'] for r in cv_results]),
    'cv_mean_roc_auc': np.mean([r['roc_auc'] for r in cv_results])
}])

summary.to_excel('evaluation_summary.xlsx', index=False)

print(f"\n{'='*70}")
print(f"{'='*70}")
print(f"Insiders Caught: {recall:.1f}% ({tp}/{len(test_insiders)})")
print(f"False Positive Rate: {fp_rate:.1f}% ({fp}/{fp+tn})")
print(f"Precision: {precision:.1f}% ({tp}/{len(flagged_users)})")
print(f"F1 Score: {f1:.1f}%")
print(f"PR-AUC: {test_pr_auc:.3f}")
print(f"{'='*70}")
