import pandas as pd
import json
import os

# 📥 Διαβάζουμε τα δεδομένα
df = pd.read_csv("../data/kino_full_data.csv", encoding="utf-8")

# 🔍 Ανάλυση: μέτρηση συχνοτήτων
all_numbers = []
for row in df["numbers"]:
    if isinstance(row, str):
        nums = [int(n) for n in row.strip("[]").replace(" ", "").split(",")]
        all_numbers.extend(nums)

number_counts = pd.Series(all_numbers).value_counts().sort_values(ascending=False)

# 💡 Επιλογή top αριθμών
TOP_N = 20
top_numbers = number_counts.head(TOP_N).index.tolist()

# 💾 Αποθήκευση top αριθμών
os.makedirs("../data", exist_ok=True)
with open("../data/rolling_window_top_numbers.json", "w", encoding="utf-8") as f:
    json.dump(top_numbers, f, indent=2)

print(f"✅ Οι {TOP_N} πιο συχνοί αριθμοί αποθηκεύτηκαν σε: ../data/rolling_window_top_numbers.json")

# 🎟️ Δημιουργία προτεινόμενου δελτίου
TICKET_SIZE = 12
ticket = sorted(top_numbers[:TICKET_SIZE])

# 📝 Αποθήκευση δελτίου
with open("../output/smart_ticket.txt", "w", encoding="utf-8") as f:
    f.write("🎯 Προτεινόμενο Δελτίο:\n")
    f.write(", ".join(str(n) for n in ticket) + "\n")
    if 'drawId' in df.columns:
        f.write(f"📅 Από κλήρωση {df['drawId'].iloc[0]} έως {df['drawId'].iloc[-1]}\n")

print(f"🎟️ Προτεινόμενο δελτίο: {ticket}")
print("📁 Αποθηκεύτηκε σε: ../output/smart_ticket.txt")