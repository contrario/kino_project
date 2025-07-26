import pandas as pd
import os
import itertools
from collections import Counter
import time

start_time = time.time()

# 📁 Βεβαιωνόμαστε ότι υπάρχει ο φάκελος εξόδου
os.makedirs("output", exist_ok=True)

# 📂 Διαδρομή αρχείου
input_path = "data/kino_draws.csv"
output_path = "output/top_13_combinations.csv"

# ✅ Ανάγνωση αρχείου
try:
    df = pd.read_csv(input_path)

    # 🧠 Παίρνουμε μόνο τις τελευταίες 500 κληρώσεις
    recent_df = df.tail(500)

    # 🔢 Εξαγωγή μόνο των αριθμών από κάθε σειρά
    number_columns = [col for col in df.columns if col.startswith("num_")]
    recent_draws = recent_df[number_columns].values.tolist()

    # 🔁 Εξαγωγή όλων των 13άδων
    all_combinations = []
    for draw in recent_draws:
        draw = sorted(set(draw))
        if len(draw) >= 13:
            combs = itertools.combinations(draw, 13)
            all_combinations.extend(combs)

    # 📊 Καταμέτρηση συχνοτήτων
    counter = Counter(all_combinations)
    most_common = counter.most_common(10)

    # 📄 Αποθήκευση σε CSV
    result_df = pd.DataFrame(most_common, columns=["Combination", "Frequency"])
    result_df.to_csv(output_path, index=False)

    elapsed = time.time() - start_time
    print("✅ Οι πιο συχνές 13άδες υπολογίστηκαν και αποθηκεύτηκαν!")
    print(result_df)
    print(f"⏱️ Χρόνος εκτέλεσης: {elapsed:.2f} δευτερόλεπτα")

except FileNotFoundError:
    print(f"❌ Το αρχείο δεν βρέθηκε: {input_path}")
except Exception as e:
    print(f"❌ Σφάλμα: {e}")