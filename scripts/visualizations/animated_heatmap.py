import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.animation as animation
import os
import sys

# --- Ρύθμιση ασφαλών διαδρομών ---
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
csv_path = os.path.join(base_dir, 'data', 'kino_data_prepared.csv')
output_gif_path = os.path.join(base_dir, 'data', 'kino_animated_heatmap.gif')

# --- Έλεγχος ύπαρξης αρχείου ---
if not os.path.exists(csv_path):
    print(f"❌ Δεν βρέθηκε το αρχείο: {csv_path}")
    sys.exit(1)

# --- Φόρτωση δεδομένων ---
try:
    df = pd.read_csv(csv_path, parse_dates=['draw_time'])
except Exception as e:
    print(f"❌ Σφάλμα κατά την ανάγνωση του CSV: {e}")
    sys.exit(1)

# --- Εντοπισμός των αριθμητικών στηλών (num1–num20) ---
number_columns = [col for col in df.columns if col.startswith('num')]
if len(number_columns) < 5:
    print(f"❌ Δεν βρέθηκαν επαρκείς στήλες με αριθμούς (π.χ. num1–num20). Βρέθηκαν: {number_columns}")
    sys.exit(1)

# --- Συνένωση αριθμών σε λίστα ανά κλήρωση ---
df['winning_numbers'] = df[number_columns].values.tolist()

# --- Δημιουργία στήλης εβδομάδας ---
if 'draw_time' not in df.columns:
    print("❌ Η στήλη 'draw_time' λείπει από το CSV.")
    sys.exit(1)
df['week'] = df['draw_time'].dt.strftime('%Y-%W')

# --- Συνάρτηση heatmap ---
def create_heatmap_data(week_data):
    matrix = np.zeros((8, 10))  # 80 αριθμοί
    for numbers in week_data['winning_numbers']:
        for number in numbers:
            if 1 <= number <= 80:
                row = (number - 1) // 10
                col = (number - 1) % 10
                matrix[row, col] += 1
    return matrix

# --- Προετοιμασία εβδομάδων ---
weeks = sorted(df['week'].unique())

# --- Plot setup ---
fig, ax = plt.subplots(figsize=(8, 6))

def update(i):
    ax.clear()
    week = weeks[i]
    week_data = df[df['week'] == week]
    matrix = create_heatmap_data(week_data)
    sns.heatmap(matrix, annot=False, fmt='g', cmap='YlOrRd', cbar=True, ax=ax)
    ax.set_title(f"Εβδομάδα: {week}", fontsize=14)
    ax.set_xticks(np.arange(10) + 0.5)
    ax.set_yticks(np.arange(8) + 0.5)
    ax.set_xticklabels(range(1, 11))
    ax.set_yticklabels([f"{i*10+1}-{i*10+10}" for i in range(8)])

# --- Δημιουργία animation ---
try:
    ani = animation.FuncAnimation(fig, update, frames=len(weeks), repeat=False)
    ani.save(output_gif_path, writer='pillow', fps=1)
    print(f"✅ Το animated GIF αποθηκεύτηκε στο:\n{output_gif_path}")
except Exception as e:
    print(f"❌ Σφάλμα κατά τη δημιουργία του GIF: {e}")
