import pandas as pd
from itertools import combinations
from collections import Counter
import os

# Ορισμός διαδρομής αρχείου
input_path = os.path.join("data", "kino_draws.csv")
output_path = os.path.join("data", "most_common_6.csv")

# Έλεγχος αν το αρχείο υπάρχει
if not os.path.exists(input_path):
    print(f"❌ Το αρχείο δεν βρέθηκε: {input_path}")
else:
    # Ανάγνωση του dataset
    df = pd.read_csv(input_path)

    # Έλεγχος ότι οι απαραίτητες στήλες υπάρχουν
    number_columns = [f'num_{i}' for i in range(1, 21)]
    if not all(col in df.columns for col in number_columns):
        print("❌ Οι αναμενόμενες στήλες 'num_1' έως 'num_20' δεν βρέθηκαν.")
        print(f"📌 Οι στήλες που βρέθηκαν είναι: {list(df.columns)}")
    else:
        # Δημιουργία λίστας με όλους τους αριθμούς κάθε κλήρωσης
        all_combinations = []
        for _, row in df.iterrows():
            numbers = [row[f'num_{i}'] for i in range(1, 21)]
            combos = combinations(sorted(numbers), 6)
            all_combinations.extend(combos)

        # Υπολογισμός συχνότητας εμφάνισης κάθε 6άδας
        combo_counts = Counter(all_combinations)
        most_common = combo_counts.most_common(10)

        # Μετατροπή σε DataFrame και αποθήκευση
        result_df = pd.DataFrame(most_common, columns=["Combination", "Frequency"])
        result_df.to_csv(output_path, index=False)

        print("✅ Οι πιο συχνές 6άδες υπολογίστηκαν και αποθηκεύτηκαν!")
        print(result_df)
