import pandas as pd
import numpy as np
import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report, average_precision_score, roc_auc_score, precision_recall_curve
from imblearn.over_sampling import SMOTE
import warnings
warnings.filterwarnings('ignore')

MAX_DEPTH = 6             
MIN_SAMPLES_LEAF = 5      
MIN_SAMPLES_SPLIT = 20     
SMOTE_STRATEGY = 0.5       
THRESHOLD_MULTIPLIER = 0.5

INPUT_TRAIN = 'training_dataset.xlsx'
MODEL_FILE = 'decision_tree_model.pkl'

df = pd.read_excel(INPUT_TRAIN)

feature_cols = [c for c in df.columns if c not in ['user', 'label']]
X = df[feature_cols].values
y = df['label'].values
users = df['user'].values

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
fold_results = []
all_val_probs = []
all_val_labels = []

for fold, (train_idx, val_idx) in enumerate(skf.split(X, y), 1):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]

    smote = SMOTE(sampling_strategy=SMOTE_STRATEGY, random_state=42)
    X_train_bal, y_train_bal = smote.fit_resample(X_train, y_train)

    model = DecisionTreeClassifier(
        max_depth=MAX_DEPTH,
        min_samples_leaf=MIN_SAMPLES_LEAF,
        min_samples_split=MIN_SAMPLES_SPLIT,
        class_weight='balanced',
        random_state=42
    )

    model.fit(X_train_bal, y_train_bal)
    val_probs = model.predict_proba(X_val)[:, 1]

    all_val_probs.extend(val_probs)
    all_val_labels.extend(y_val)

    pr_auc = average_precision_score(y_val, val_probs)
    roc_auc = roc_auc_score(y_val, val_probs)

    fold_results.append({
        'fold': fold,
        'pr_auc': pr_auc,
        'roc_auc': roc_auc
    })

all_val_probs = np.array(all_val_probs)
all_val_labels = np.array(all_val_labels)

precisions, recalls, thresholds = precision_recall_curve(all_val_labels, all_val_probs)
f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-10)
best_idx = np.argmax(f1_scores)
best_thr = thresholds[best_idx] if best_idx < len(thresholds) else 0.5
best_thr = best_thr * THRESHOLD_MULTIPLIER

smote = SMOTE(sampling_strategy=SMOTE_STRATEGY, random_state=42)
X_full_bal, y_full_bal = smote.fit_resample(X, y)

final_model = DecisionTreeClassifier(
    max_depth=MAX_DEPTH,
    min_samples_leaf=MIN_SAMPLES_LEAF,
    min_samples_split=MIN_SAMPLES_SPLIT,
    class_weight='balanced',
    random_state=42
)

final_model.fit(X_full_bal, y_full_bal)

joblib.dump({
    'model': final_model,
    'feature_names': feature_cols,
    'threshold': best_thr,
    'cv_results': fold_results,
    'train_users': users
}, MODEL_FILE)

print(f"  CV PR-AUC: {np.mean([r['pr_auc'] for r in fold_results]):.3f}")
