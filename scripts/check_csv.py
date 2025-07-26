import pandas as pd
import os

# Δημιουργία διαδρομής προς το CSV αρχείο
csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'kino_data.csv')

# Ανάγνωση του αρχείου
df = pd.read_csv(csv_path)

# Εκτύπωση όλων των στηλών
print("🔎 Στήλες στο αρχείο:")
print(df.columns.tolist())