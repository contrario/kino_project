# 📁 scripts/analyze_overlap.py

import pandas as pd
import itertools
import time
import os

start = time.time()
print("🔎 Ανάλυση επικάλυψης 4άδων & 5άδων σε εξέλιξη...")

# Δημιουργία φακέλου αποτελεσμάτων
os.makedirs("results", exist_ok=True)

# Διαβάζουμε τα δεδομένα
df = pd.read_csv("kino_data.csv")

# Έλεγχος σωστής στήλης
if 'winning_numbers' not in df.columns:
    print("❌ Σφάλμα: Δεν βρέθηκε η στήλη 'winning_numbers' στο αρχείο kino_data.csv.")
    print(f"📋 Βρέθηκαν οι στήλες: {list(df.columns)}")
    exit(1)

# Μετατροπή σε λίστα αριθμών
df['winning_numbers'] = df['winning_numbers'].apply(eval)

# Φιλτράρουμε κληρώσεις με τουλάχιστον 15 αριθμούς
df = df[df['winning_numbers'].apply(len) >= 15]

# Μετρητές συχνοτήτων
combinations_4 = {}
combinations_5 = {}

# Εξαγωγή συνδυασμών
for numbers in df['winning_numbers']:
    for comb in itertools.combinations(numbers, 4):
        comb = tuple(sorted(comb))
        combinations_4[comb] = combinations_4.get(comb, 0) + 1
    for comb in itertools.combinations(numbers, 5):
        comb = tuple(sorted(comb))
        combinations_5[comb] = combinations_5.get(comb, 0) + 1

# Αποτελέσματα
df_4 = pd.DataFrame(combinations_4.items(), columns=['Combination', 'Frequency']).sort_values(by='Frequency', ascending=False)
df_5 = pd.DataFrame(combinations_5.items(), columns=['Combination', 'Frequency']).sort_values(by='Frequency', ascending=False)

# Αποθήκευση
df_4.head(50).to_csv("results/most_common_4_in_15plus.csv", index=False)
df_5.head(50).to_csv("results/most_common_5_in_15plus.csv", index=False)

end = time.time()
print("✅ Οι συχνότερες επαναλαμβανόμενες 4άδες και 5άδες αποθηκεύτηκαν!")
print(f"⏱️ Χρόνος εκτέλεσης: {round(end - start, 2)} δευτερόλεπτα")

