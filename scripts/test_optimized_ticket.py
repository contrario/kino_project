import os
import pandas as pd
from pathlib import Path

# ➤ Project root
project_root = Path(__file__).resolve().parent.parent

# ➤ Paths
data_path = project_root / "data" / "kino_data.csv"
ticket_path = project_root / "scripts" / "optimized_ticket.txt"

# ➤ Έλεγχος ύπαρξης αρχείων
if not data_path.exists():
    raise FileNotFoundError(f"Δεν βρέθηκε το αρχείο: {data_path}")
if not ticket_path.exists():
    raise FileNotFoundError(f"Δεν βρέθηκε το αρχείο: {ticket_path}")

# ➤ Φόρτωση δεδομένων
df = pd.read_csv(data_path)

# ➤ Εμφάνιση στηλών
print("\n📄 Διαθέσιμες στήλες:")
print(df.columns.tolist())

# ➤ Στήλες με αριθμούς
number_columns = [f"num_{i}" for i in range(1, 21)]
if not all(col in df.columns for col in number_columns):
    raise ValueError("Δεν βρέθηκαν όλες οι στήλες num_1 έως num_20 στο αρχείο.")

# ➤ Φόρτωση βελτιστοποιημένου δελτίου
with open(ticket_path, encoding="utf-8", "r") as f:
    ticket = eval(f.read())  # Π.χ. [3, 12, 19, 25, 37, 41, 60]

# ➤ Υπολογισμός επιτυχιών
hits = []
for _, row in df.iterrows():
    draw_numbers = [int(row[f"num_{i}"]) for i in range(1, 21)]
    hit_count = len(set(ticket) & set(draw_numbers))
    hits.append(hit_count)

# ➤ Αποτελέσματα
total_draws = len(hits)
average_hits = sum(hits) / total_draws if total_draws > 0 else 0

print("\n🔎 Backtest Optimized Ticket")
print(f"🎟 Δελτίο: {ticket}")
print(f"📅 Κληρώσεις: {total_draws}")
print(f"🎯 Μέσος όρος επιτυχιών: {average_hits:.2f}")
