import pandas as pd
from collections import Counter
from itertools import combinations
import os

# 🔹 Απόλυτο path στο αρχείο kino_draws.csv (μέσα στον φάκελο data)
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "kino_draws.csv"))

# 🔍 Έλεγχος αν υπάρχει το αρχείο
if not os.path.exists(file_path):
    print(f"❌ Το αρχείο δεν βρέθηκε: {file_path}")
    exit()

# ✅ Φόρτωση δεδομένων
df = pd.read_csv(file_path)

if 'numbers' not in df.columns:
    print("❌ Η στήλη 'numbers' δεν υπάρχει στο αρχείο.")
    exit()

# 🔄 Μετατροπή των αριθμών σε λίστες ακεραίων
df['numbers'] = df['numbers'].apply(lambda x: [int(num) for num in str(x).split(';')])

# 🔢 Υπολογισμός συχνότερων 3άδων
combo_counter = Counter()
for draw in df['numbers']:
    draw_combinations = combinations(sorted(draw), 3)
    combo_counter.update(draw_combinations)

# 📊 Πίνακας με τις 20 πιο συχνές 3άδες
most_common_combos = combo_counter.most_common(20)
combo_df = pd.DataFrame(most_common_combos, columns=["Combination", "Frequency"])

# 💾 Αποθήκευση στο data/most_common_combinations.csv
output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "most_common_combinations.csv"))
combo_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print("✅ Οι πιο συχνές 3άδες υπολογίστηκαν και αποθηκεύτηκαν!")
print(combo_df.head())
