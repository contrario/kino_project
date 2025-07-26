import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import random

# ➤ Ρυθμίσεις paths
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, "kino_data.csv")
ticket_path = os.path.join(base_dir, "optimized_ticket.txt")
report_path = os.path.join(base_dir, "multi_ticket_analysis.txt")
graph_path = os.path.join(base_dir, "multi_ticket_hits_distribution.png")

# ➤ Φόρτωσε δεδομένα
df = pd.read_csv(data_path)

# ➤ Δες τις πρώτες 5 γραμμές για επιβεβαίωση
if df.empty or "winning_numbers" not in df.columns:
    raise ValueError("Δεν βρέθηκε η στήλη 'winning_numbers' στο αρχείο.")

# ➤ Μετατροπή της στήλης winning_numbers σε λίστες ακεραίων
df["numbers"] = df["winning_numbers"].apply(lambda x: [int(n) for n in str(x).split(",")])

# ➤ Φόρτωσε το αρχικό βελτιστοποιημένο δελτίο
with open(ticket_path, encoding="utf-8", "r") as f:
    line = f.readline()
    ticket = tuple(int(x) for x in line.strip("[]()").split(",") if x.strip().isdigit())

# ➤ Δημιουργία 10 τυχαίων δελτίων από τη βάση δεδομένων
num_tickets = 10  # 10 διαφορετικά δελτία
generated_tickets = []

for _ in range(num_tickets):
    random_ticket = random.sample(range(1, 81), 7)  # Εδώ επιλέγουμε 7 αριθμούς τυχαία από το 1 έως το 80
    generated_tickets.append(random_ticket)

# ➤ Υπολογισμός επιτυχιών για όλα τα δελτία
ticket_performance = {}

for ticket in generated_tickets:
    hits_per_ticket = []
    for draw in df["numbers"]:
        hit_count = len(set(ticket) & set(draw))
        hits_per_ticket.append(hit_count)

    # Υπολογισμός μέσου όρου επιτυχιών για το δελτίο
    ticket_performance[tuple(ticket)] = sum(hits_per_ticket) / len(hits_per_ticket)

# ➤ Βρες το καλύτερο δελτίο
best_ticket = max(ticket_performance, key=ticket_performance.get)
best_ticket_hits = ticket_performance[best_ticket]

# ➤ Αποθήκευση αποτελεσμάτων
with open(report_path, "w", encoding="utf-8") as f:
    f.write(f"📅 Πληροφορίες Ανάλυσης για {num_tickets} Δελτία\n")
    for ticket, performance in ticket_performance.items():
        f.write(f"\n🎟 Δελτίο: {ticket}\n")
        f.write(f"🎯 Μέσος όρος επιτυχιών: {performance:.2f}\n")

    f.write(f"\n\n📈 Καλύτερο Δελτίο: {best_ticket}\n")
    f.write(f"🎯 Μέσος όρος επιτυχιών: {best_ticket_hits:.2f}\n")

print(f"\n📁 Αναφορά αποθηκεύτηκε: {report_path}")
print(f"\n🎯 Καλύτερο Δελτίο: {best_ticket} με μέσο όρο επιτυχιών: {best_ticket_hits:.2f}")

# ➤ Γράφημα κατανομής επιτυχιών
hit_counts = Counter(ticket_performance.values())

plt.figure(figsize=(10, 5))
plt.bar(hit_counts.keys(), hit_counts.values(), color='skyblue')
plt.xlabel("Αριθμός επιτυχιών")
plt.ylabel("Συχνότητα")
plt.title("📊 Κατανομή Επιτυχιών Πολλαπλών Δελητίων")
plt.tight_layout()
plt.savefig(graph_path)
print(f"🖼️ Γράφημα αποθηκεύτηκε: {graph_path}")

