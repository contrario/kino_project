import os
import pandas as pd
from collections import Counter
import ast

# 📁 Αυτόματη αναγνώριση διαδρομής script
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "backtest_results.csv")

# 📂 Έλεγχος αν υπάρχει το αρχείο
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Δεν βρέθηκε το αρχείο: {file_path}")

df = pd.read_csv(file_path)

# 🧠 Ανάγνωση αριθμών από τη στήλη 'hits'
all_hits = []
for row in df["hits"]:
    try:
        if isinstance(row, str):
            # Αν είναι string τύπου '3,12,25'
            numbers = [int(num) for num in row.split(",") if num.strip().isdigit()]
        elif isinstance(row, int):
            # Αν είναι απλός αριθμός
            numbers = [row]
        elif isinstance(row, list):
            numbers = row
        else:
            # Αν είναι string λίστας: '[3, 12, 25]'
            numbers = ast.literal_eval(str(row))
        all_hits.extend(numbers)
    except Exception as e:
        print(f"❌ Παράλειψη προβληματικής γραμμής: {row} ({e})")

# 📊 Ανάλυση συχνότητας αριθμών
number_counts = Counter(all_hits)

# 🧮 Επιλογή 12 πιο συχνών αριθμών
optimized_ticket = [num for num, count in number_counts.most_common(12)]

# 💾 Αποθήκευση σε αρχείο
output_path = os.path.join(current_dir, "optimized_ticket.txt")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(",".join(str(num) for num in optimized_ticket))

# ✅ Τύπωμα αποτελέσματος
print("🎯 Νέο Βελτιστοποιημένο Δελτίο (Top 12 αριθμοί):")
print("➤", optimized_ticket)
print(f"📁 Αποθηκεύτηκε σε: {output_path}")