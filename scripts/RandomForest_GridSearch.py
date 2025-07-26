import os
# scripts/RandomForest_GridSearch.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from imblearn.over_sampling import SMOTE

# 📌 Top-10 features που ήδη είδαμε
top10_features = ['num_8', 'num_4', 'num_14', 'gap_1', 'gap_17', 'gap_43', 'num_12', 'num_5', 'freq_8', 'freq_4']

# 🔹 Φόρτωση δεδομένων
df = pd.read_csv('data/kino_features.csv')

# 🔍 Target & Features
X = df[top10_features]
y = df['is_7_hit']

# 🔁 SMOTE για εξισορρόπηση
X_res, y_res = SMOTE(random_state=42).fit_resample(X, y)

# ✂️ Διαχωρισμός σε train/test
X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.3, random_state=42)

# 🔍 Ορισμός Grid
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 5, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2']
}

# 🔍 GridSearchCV
grid_search = GridSearchCV(
    estimator=RandomForestClassifier(random_state=42),
    param_grid=param_grid,
    cv=5,
    scoring='f1',
    n_jobs=-1,
    verbose=2
)

grid_search.fit(X_train, y_train)

# ✅ Καλύτερες παράμετροι
print("🏆 Best Parameters:")
print(grid_search.best_params_)

# 🔍 Αξιολόγηση στο test set
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

print(f"\n🎯 Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(f"📌 Precision: {precision_score(y_test, y_pred):.2f}")
print(f"📈 Recall: {recall_score(y_test, y_pred):.2f}")
print(f"🧪 F1-Score: {f1_score(y_test, y_pred):.2f}")