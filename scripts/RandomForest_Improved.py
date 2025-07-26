import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from imblearn.over_sampling import SMOTE
from collections import Counter

# 📥 Φόρτωση εμπλουτισμένων δεδομένων
df = pd.read_csv("data/kino_features_enriched.csv")

# 🎯 Στόχος
y = df['is_7_hit']

# 📊 Χαρακτηριστικά προς εκπαίδευση (εξαιρούμε τις στήλες draw_id, draw_time και num_1 έως num_20)
exclude_cols = ['draw_id', 'draw_time'] + [f'num_{i}' for i in range(1, 21)] + ['is_7_hit']
X = df.drop(columns=exclude_cols)

print("🔍 Κατανομή 'is_7_hit':")
print(y.value_counts())

# ⚖️ Ισορροπία δεδομένων με SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

print("\n🔁 Νέα κατανομή μετά το SMOTE:")
print(Counter(y_resampled))

# 🔀 Διαχωρισμός
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# 🌳 Μοντέλο
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 📈 Προβλέψεις
y_pred = model.predict(X_test)

# 🎯 Αξιολόγηση
print(f"\n🎯 Ακρίβεια: {accuracy_score(y_test, y_pred):.2f}")
print(f"📌 Precision: {precision_score(y_test, y_pred):.2f}")
print(f"📈 Recall: {recall_score(y_test, y_pred):.2f}")
print(f"🧪 F1-Score: {f1_score(y_test, y_pred):.2f}")

# 🧪 Cross-Validation
scores = cross_val_score(model, X_resampled, y_resampled, cv=5)
print(f"\n✅ Αξιολογήσεις με Cross-Validation: {scores}")
print(f"📊 Μέση ακρίβεια: {scores.mean():.4f}")











