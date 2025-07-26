import os
import pandas as pd

# Διαβάζουμε τις κληρώσεις
df = pd.read_csv("kino_data.csv")

# Πόσες κληρώσεις έχουμε;
total_draws = len(df)

# Αν έχουμε λιγότερες από 10 κληρώσεις, σταματάμε
if total_draws < 10:
    raise ValueError("Δεν υπάρχουν αρκετές κληρώσεις για το backtest.")

# Διαβάζουμε το αρχείο με το προτεινόμενο δελτίο (π.χ. από συχνότητες)
with open("suggested_ticket.txt", "r", encoding="utf-8") as f:
    suggested_numbers = list(map(int, f.read().strip().split(",")))

# Πόσες τελευταίες κληρώσεις να συγκρίνουμε
draws_to_check = min(50, total_draws)  # π.χ. 50 ή όσες έχει διαθέσιμες

# Κρατάμε τις πιο πρόσφατες
last_draws = df.tail(draws_to_check)

# Αποθήκευση αποτελεσμάτων
results = []

for index, row in last_draws.iterrows():
    # Μετατρέπουμε τους αριθμούς της κλήρωσης σε λίστα
    numbers = list(map(int, row["winning_numbers"].strip("[]").split(",")))

    # Υπολογίζουμε πόσοι αριθμοί από το δελτίο πέσανε
    hits = len(set(numbers) & set(suggested_numbers))

    results.append({
        "draw_id": row["draw_id"],
        "date": row["draw_time"],
        "hits": hits,
        "numbers": numbers
    })

# Δημιουργούμε DataFrame με τα αποτελέσματα
results_df = pd.DataFrame(results)

# Αποθήκευση σε CSV
results_df.to_csv("backtest_results.csv", index=False, encoding="utf-8")

# Εμφάνιση στατιστικών
avg_hits = results_df["hits"].mean()

print("📊 Αποτελέσματα Backtest")
print(f"➤ Συνολικές κληρώσεις: {draws_to_check}")
print(f"➤ Μέσος όρος επιτυχιών (σε 12 αριθμούς): {avg_hits:.2f}")
print(f"➤ Αποτελέσματα αποθηκεύτηκαν στο 'backtest_results.csv'")
