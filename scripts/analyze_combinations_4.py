# analyze_combinations_4.py

import os
import pandas as pd
from itertools import combinations
from collections import Counter

# 🔧 Υπολογισμός δυναμικής διαδρομής (path) ανεξάρτητα από το πού τρέχει το script
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
input_path = os.path.join(base_dir, "data", "kino_draws.csv")
output_path = os.path.join(base_dir, "data", "top_4_combinations.csv")

# ✅ Έλεγχος αν υπάρχει το αρχείο
if not os.path.exists(input_path):
    print(f"❌ Το αρχείο δεν βρέθηκε: {input_path}")
else:
    # 📥 Φόρτωσε το αρχείο
    df = pd.read_csv(input_path)

    if 'numbers' not in df.columns:
        print("❌ Δεν βρέθηκε η στήλη 'numbers'")
    else:
        # 🔢 Ανάλυση: μετατροπή κάθε σειράς σε λίστα αριθμών (integers)
        all_combinations = []
        for row in df['numbers']:
            numbers = list(map(int, str(row).split(';')))
            combos = combinations(numbers, 4)
            all_combinations.extend(combos)

        # 🧮 Υπολογισμός συχνοτήτων
        combination_counts = Counter(all_combinations)
        most_common = combination_counts.most_common(100)

        # 📄 Αποθήκευση σε DataFrame και CSV
        result_df = pd.DataFrame(most_common, columns=['Combination', 'Frequency'])
        result_df.to_csv(output_path, index=False, encoding='utf-8-sig')

        print("✅ Οι πιο συχνές 4άδες υπολογίστηκαν και αποθηκεύτηκαν!")
        print(result_df.head())

