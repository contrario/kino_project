import os
import pandas as pd
import joblib
import numpy as np
from pathlib import Path

# Ρυθμίσεις
DATA_PATH = Path("data/kino_dataset_cleaned.csv")
MODEL_PATH = Path("models/best_model.pkl")
TOP_K = 12          # Πλήθος αριθμών στο "έξυπνο δελτίο"
N_RECENT_DRAWS = 5  # Πόσες πρόσφατες κληρώσεις να λάβουμε υπόψη

# Βήμα 1: Φόρτωση μοντέλου
model = joblib.load(MODEL_PATH)
print("✅ Φορτώθηκε το μοντέλο")

# Βήμα 2: Φόρτωση dataset
df = pd.read_csv(DATA_PATH)
print(f"✅ Φορτώθηκε το dataset ({len(df)} εγγραφές)")

# Βήμα 3: Λήψη των N πιο πρόσφατων εγγραφών
recent_draws = df.sort_values("draw_time", ascending=False).head(N_RECENT_DRAWS)
recent_features = recent_draws.drop(columns=["draw_id", "draw_time", "numbers"])

# Βήμα 4: Δημιουργία μέσου όρου χαρακτηριστικών
avg_features = recent_features.mean().values.reshape(1, -1)

# Βήμα 5: Πρόβλεψη πιθανοτήτων για κάθε αριθμό
predicted_probs = model.predict_proba(avg_features)[0]  # μέγεθος (80,)
number_prob_pairs = list(zip(range(1, 81), predicted_probs))

# Ταξινόμηση με βάση τις πιθανότητες
sorted_pairs = sorted(number_prob_pairs, key=lambda x: x[1], reverse=True)
smart_ticket = [num for num, prob in sorted_pairs[:TOP_K]]

# Βήμα 6: Εκτύπωση αποτελέσματος
print("\n🎯 Προτεινόμενο 'έξυπνο' δελτίο ΚΙΝΟ:")
print("🎟️", sorted(smart_ticket))




