# scripts/visualize_hot_cold.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time

# Έναρξη χρονισμού
start_time = time.time()

# Δημιουργία φακέλου charts αν δεν υπάρχει
os.makedirs("charts", exist_ok=True)

# Φόρτωση δεδομένων
df = pd.read_csv("results/number_frequency.csv")
df_hot = pd.read_csv("results/hot_numbers.csv")
df_cold = pd.read_csv("results/cold_numbers.csv")

# Γραφικό στυλ
sns.set_style("whitegrid")

# 1. Όλες οι συχνότητες
plt.figure(figsize=(16, 6))
sns.barplot(data=df, x='Number', y='Frequency', palette='viridis', hue='Number', legend=False)
plt.title("Συχνότητα Εμφάνισης Όλων των Αριθμών")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("charts/all_frequencies.png")
plt.close()

# 2. Hot Numbers
plt.figure(figsize=(10, 6))
sns.barplot(data=df_hot, x='Number', y='Frequency', palette='Reds', hue='Number', legend=False)
plt.title("Top-10 Hot Numbers")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/hot_numbers.png")
plt.close()

# 3. Cold Numbers
plt.figure(figsize=(10, 6))
sns.barplot(data=df_cold, x='Number', y='Frequency', palette='Blues', hue='Number', legend=False)
plt.title("Top-10 Cold Numbers")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/cold_numbers.png")
plt.close()

# Χρονισμός και έξοδος
elapsed = round(time.time() - start_time, 2)
print(f"✅ Ολοκληρώθηκε η δημιουργία καθαρών γραφημάτων χωρίς warnings!")
print("📂 Τα γραφήματα αποθηκεύτηκαν στον φάκελο 'charts/'")
print(f"⏱️ Χρόνος εκτέλεσης: {elapsed} sec")



