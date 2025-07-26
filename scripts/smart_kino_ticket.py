# 📍 scripts/smart_kino_ticket.py

import pandas as pd
from collections import Counter
from datetime import datetime
import os

# ===== ΡΥΘΜΙΣΕΙΣ =====
INPUT_CSV = '../data/kino_data_prepared.csv'
OUTPUT_DIR = '../outputs'
ANALYSIS_DRAWS = 200            # Πόσες κληρώσεις να αναλυθούν
PLAY_NUMBERS = 5                # Πόσους αριθμούς να προτείνει
DRAWS_TO_PLAY = 10              # Για πόσες κληρώσεις ισχύει το δελτίο
BET_PER_DRAW = 0.50             # Ποντάρισμα ανά κλήρωση
MIN_HOUR = 9                    # Ανάλυση μετά τις 9:00 το πρωί (π.χ. αποφυγή νύχτας)
SAVE_RESULTS = True             # Να αποθηκεύεται το δελτίο σε αρχείο;

# ======== ΑΝΑΓΝΩΣΗ ΔΕΔΟΜΕΝΩΝ =========
df = pd.read_csv(INPUT_CSV)
required_cols = ['draw_id', 'draw_time', 'hour'] + [f'number_{i}' for i in range(1, 21)]

if any(col not in df.columns for col in required_cols):
    raise ValueError("❌ Το αρχείο δεν έχει την κατάλληλη μορφή. Τρέξε πρώτα το prepare_data.")

# ========= ΦΙΛΤΡΑΡΙΣΜΑ ==========
df['draw_time'] = pd.to_datetime(df['draw_time'])
df = df[df['hour'] >= MIN_HOUR]
df = df.sort_values(by='draw_id', ascending=False).head(ANALYSIS_DRAWS)

# ========= ΑΝΑΛΥΣΗ ΣΥΧΝΟΤΗΤΑΣ ==========
numbers = []
for col in [f'number_{i}' for i in range(1, 21)]:
    numbers += df[col].tolist()

counter = Counter(numbers)
most_common = counter.most_common(PLAY_NUMBERS)
proposed_numbers = sorted([num for num, _ in most_common])

# ========= BACKTEST ==========
recent_df = df.copy()
recent_df['success'] = recent_df[[f'number_{i}' for i in range(1, 21)]].apply(
    lambda row: len(set(proposed_numbers).intersection(set(row))), axis=1)

backtest_successes = recent_df['success'].sum()
avg_match_per_draw = recent_df['success'].mean()

# ========= ΟΝΟΜΑ ΑΡΧΕΙΟΥ =========
now = datetime.now()
filename = f"ticket_{now.strftime('%Y-%m-%d_%H-%M')}.txt"
filepath = os.path.join(OUTPUT_DIR, filename)

# ========= ΕΜΦΑΝΙΣΗ =========
print("\n🎯 Προτεινόμενο Δελτίο:")
print(f"Αριθμοί: {proposed_numbers}")
print(f"📅 Από κλήρωση {df['draw_id'].max() + 1} έως {df['draw_id'].max() + DRAWS_TO_PLAY}")
print(f"💰 Κόστος: {BET_PER_DRAW * DRAWS_TO_PLAY:.2f} €")

print("\n📊 Backtest (σε προηγούμενες 200 κληρώσεις):")
print(f" - Μέσος όρος επιτυχιών ανά κλήρωση: {avg_match_per_draw:.2f}")
print(f" - Σύνολο επιτυχιών: {backtest_successes}")

# ========= ΑΠΟΘΗΚΕΥΣΗ =========
if SAVE_RESULTS:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"🎯 Προτεινόμενο Δελτίο ({now.strftime('%Y-%m-%d %H:%M')}):\n")
        f.write(f"Αριθμοί: {proposed_numbers}\n")
        f.write(f"Ανάλυση από {ANALYSIS_DRAWS} κληρώσεις μετά τις {MIN_HOUR}:00\n")
        f.write(f"Μέσος όρος επιτυχιών: {avg_match_per_draw:.2f}\n")
        f.write(f"Κόστος: {BET_PER_DRAW * DRAWS_TO_PLAY:.2f} €\n")
        f.write(f"Κλήρωση από: {df['draw_id'].max() + 1} έως {df['draw_id'].max() + DRAWS_TO_PLAY}\n")

    print(f"\n✅ Αποθηκεύτηκε στο αρχείο: {filepath}")