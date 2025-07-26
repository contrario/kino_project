# analyze_combinations_7.py

import pandas as pd
from itertools import combinations
from collections import Counter
import os

# 🔧 Διαδρομή αρχείου δεδομένων
DATA_PATH = os.path.join("data", "kino_draws.csv")

# ✅ Έλεγχος αν υπάρχει το αρχείο
if not os.path.exists(DATA_PATH):
    print(f"❌ Το αρχείο δεν βρέθηκε: {DATA_PATH}")
else:
    try:
        df = pd.read_csv(DATA_PATH)

        # ✅ Λίστα με τα 20 νικητήρια νούμερα ανά κλήρωση
        winning_numbers_cols = [f"num_{i}" for i in range(1, 21)]
        all_combinations = []

        for _, row in df.iterrows():
            numbers = row[winning_numbers_cols].dropna().astype(int).tolist()
            comb = combinations(sorted(numbers), 7)
            all_combinations.extend(comb)

        # 📊 Καταμέτρηση συχνότητας
        counter = Counter(all_combinations)
        most_common = counter.most_common(10)

        # 📄 Δημιουργία DataFrame για τα αποτελέσματα
        result_df = pd.DataFrame(most_common, columns=["Combination", "Frequency"])

        # 💾 Αποθήκευση αρχείου
        output_file = os.path.join("output", "most_common_7_combinations.csv")
        os.makedirs("output", exist_ok=True)
        result_df.to_csv(output_file, index=False)

        print("✅ Οι πιο συχνές 7άδες υπολογίστηκαν και αποθηκεύτηκαν!")
        print(result_df)

    except Exception as e:
        print(f"❌ Σφάλμα κατά την ανάλυση των δεδομένων: {e}")