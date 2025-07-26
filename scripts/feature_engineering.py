import os
import pandas as pd
import numpy as np
from collections import Counter

# 📥 Διαβάζουμε το αρχείο CSV με τα βασικά δεδομένα
df = pd.read_csv("data/kino_features.csv")

# 🎯 Στόχος: Περιέχει η κλήρωση το 7;
draw_cols = [f'num_{i}' for i in range(1, 21)]
df['is_7_hit'] = df[draw_cols].apply(lambda row: 7 in row.values, axis=1).astype(int)

# ➕ Νέα χαρακτηριστικά
df['odd_count'] = df[draw_cols].apply(lambda row: sum(num % 2 == 1 for num in row), axis=1)
df['even_count'] = 20 - df['odd_count']
df['sum_total'] = df[draw_cols].sum(axis=1)
df['low_numbers_count'] = df[draw_cols].apply(lambda row: sum(num <= 40 for num in row), axis=1)
df['high_numbers_count'] = 20 - df['low_numbers_count']
df['std_deviation'] = df[draw_cols].std(axis=1)

# 🎯 Συχνότερα νούμερα συνολικά
all_numbers = df[draw_cols].values.flatten()
top_10_common = [num for num, _ in Counter(all_numbers).most_common(10)]

def count_common(row):
    return sum(num in top_10_common for num in row)

df['most_common_hits'] = df[draw_cols].apply(count_common, axis=1)

# 🔁 Διαδοχικοί αριθμοί (π.χ. 22-23-24)
def count_consecutive(numbers):
    sorted_nums = sorted(numbers)
    count = 0
    for i in range(1, len(sorted_nums)):
        if sorted_nums[i] == sorted_nums[i - 1] + 1:
            count += 1
    return count

df['consecutive_count'] = df[draw_cols].apply(count_consecutive, axis=1)

# 🔢 Μοναδικά τελευταία ψηφία (modulo 10)
df['unique_modulo_10'] = df[draw_cols].apply(lambda row: len(set(num % 10 for num in row)), axis=1)

# 💾 Αποθήκευση των enriched δεδομένων
df.to_csv("data/kino_features_enriched.csv", index=False)
print("✅ Ολοκληρώθηκε η παραγωγή εμπλουτισμένων χαρακτηριστικών.")



