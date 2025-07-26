# analyze_combinations_11.py

import pandas as pd
from itertools import combinations
from collections import Counter
import os

# 📌 Ορισμός διαδρομής αρχείου
csv_path = os.path.join("data", "kino_draws.csv")

# ✅ Έλεγχος αν υπάρχει το αρχείο
if not os.path.exists(csv_path):
    print(f"❌ Το αρχείο δεν βρέθηκε: {csv_path}")
    exit()

# 📥 Φόρτωση του dataset
df = pd.read_csv(csv_path)

# ✅ Έλεγχος στηλών
expected_columns = [f'num_{i}' for i in range(1, 21)]
if not all(col in df.columns for col in expected_columns):
    print(f"❌ Οι απαραίτητες στήλες δεν βρέθηκαν.")
    print(f"📌 Οι στήλες που βρέθηκαν είναι: {list(df.columns)}")
    exit()

# 🔄 Δημιουργία λίστας με όλους τους αριθμούς της κάθε κλήρωσης
draws = df[expected_columns].values.tolist()

# 🎯 Υπολογισμός όλων των δυνατών 11άδων
all_combinations = []
for draw in draws:
    draw_combinations = combinations(sorted(draw), 11)
    all_combinations.extend(draw_combinations)

# 📊 Μέτρηση συχνότητας εμφάνισης κάθε 11άδας
comb_counter = Counter(all_combinations)

# 🔝 Επιλογή των 10 πιο συχνών
most_common = comb_counter.most_common(10)

# 📄 Μετατροπή σε DataFrame για αποθήκευση
result_df = pd.DataFrame(most_common, columns=["Combination", "Frequency"])

# 📁 Αποθήκευση αποτελεσμάτων
output_path = os.path.join("output", "top_11_combinations.csv")
os.makedirs("output", exist_ok=True)
result_df.to_csv(output_path, index=False)

print("✅ Οι πιο συχνές 11άδες υπολογίστηκαν και αποθηκεύτηκαν!")
print(result_df)