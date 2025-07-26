import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 📍 Διαδρομή αρχείου CSV
csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'kino_data.csv')

# 📥 Φόρτωση δεδομένων
df = pd.read_csv(csv_path)

# 📊 Δημιουργία πίνακα counts: [θέση] x [αριθμός]
heatmap_data = pd.DataFrame(0, index=range(1, 21), columns=range(1, 81))

for i in range(1, 21):
    counts = df[f'num_{i}'].value_counts()
    for number, count in counts.items():
        heatmap_data.at[i, number] = count

# 🎨 Εμφάνιση heatmap
plt.figure(figsize=(16, 8))
sns.heatmap(heatmap_data, cmap='viridis', linewidths=0.5, linecolor='gray')

# 🏷️ Ετικέτες
plt.title('Θερμικός χάρτης αριθμών ανά θέση στο KINO', fontsize=14)
plt.xlabel('Αριθμός')
plt.ylabel('Θέση (num_1 έως num_20)')
plt.yticks(rotation=0)
plt.tight_layout()

# 📈 Εμφάνιση
plt.show()







