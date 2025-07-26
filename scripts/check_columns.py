import os
import pandas as pd

# Διαδρομή προς το αρχείο CSV
csv_path = "../data/kino_data.csv"

# Φόρτωση δεδομένων
df = pd.read_csv(csv_path)

# Καθαρισμός πιθανών κενών στους τίτλους στηλών
df.columns = df.columns.str.strip()

# Εκτύπωση όλων των στηλών
print("📋 Στήλες του αρχείου:")
for col in df.columns:
    print(f"- {col}")

