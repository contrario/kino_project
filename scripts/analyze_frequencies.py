import pandas as pd
import os

# 📍 Βρες τον φάκελο στον οποίο βρίσκεται αυτό το script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 🔁 Κατασκεύασε σωστά το path προς το αρχείο δεδομένων
input_file = os.path.join(BASE_DIR, "..", "data", "kino_draws.csv")

# 🛡️ Έλεγχος αν υπάρχει το αρχείο
if not os.path.exists(input_file):
    print(f"❌ Δεν βρέθηκε το αρχείο: {input_file}")
    exit()

# 📥 Φόρτωσε το αρχείο
df = pd.read_csv(input_file)

# ✔️ Έλεγχος για τη στήλη 'numbers'
if 'numbers' not in df.columns:
    print("❌ Δεν βρέθηκε η στήλη 'numbers'")
    exit()

# 🔢 Ανάλυση αριθμών
all_numbers = []
for row in df['numbers']:
    nums = row.split(';')
    all_numbers.extend(nums)

# 🔢 Μετατροπή σε integers
all_numbers = [int(n) for n in all_numbers]

# 📊 Υπολογισμός συχνοτήτων
freq_series = pd.Series(all_numbers).value_counts().sort_index()
df_freq = freq_series.reset_index()
df_freq.columns = ['Number', 'Frequency']

# 💾 Αποθήκευση στο σωστό path
output_file = os.path.join(BASE_DIR, "..", "data", "number_frequencies.csv")
df_freq.to_csv(output_file, index=False)

print("✅ Υπολογίστηκαν οι συχνότητες!")
print(df_freq.head())

