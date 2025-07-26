# scripts/animate_number_frequencies.py

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
from collections import Counter

# ⚙️ Ρυθμίσεις
CSV_PATH = os.path.join('data', 'kino_data.csv')
OUTPUT_PATH = os.path.join('charts', 'frequency_evolution.gif')  # ➤ άλλαξε σε .gif
FPS = 30
MAX_FRAMES = 500

ALL_NUMBERS = list(range(1, 81))

df = pd.read_csv(CSV_PATH)
if 'winningNumbers' not in df.columns:
    raise ValueError("❌ Το αρχείο δεν περιέχει τη στήλη 'winningNumbers'.")

draws = df['winningNumbers'].apply(eval).tolist()
cumulative_counts = []

counter = Counter()
for draw in draws:
    counter.update(draw)
    cumulative_counts.append(counter.copy())

def update(frame):
    plt.cla()
    freq = cumulative_counts[frame]
    numbers = ALL_NUMBERS
    values = [freq.get(num, 0) for num in numbers]

    plt.bar(numbers, values, color='skyblue')
    plt.title(f"Συσσωρευτική Συχνότητα Αριθμών - Κλήρωση #{frame + 1}")
    plt.xlabel("Αριθμοί")
    plt.ylabel("Συχνότητα")
    plt.xticks(range(0, 81, 5))
    plt.ylim(0, max(values) + 5)

fig = plt.figure(figsize=(12, 6))
ani = animation.FuncAnimation(
    fig, update, frames=min(MAX_FRAMES, len(cumulative_counts)), repeat=False
)

os.makedirs('charts', exist_ok=True)
ani.save(OUTPUT_PATH, writer='pillow', fps=FPS)  # ➤ χρήση pillow writer

print("✅ Ολοκληρώθηκε η δημιουργία animated γραφήματος!")
print(f"📽️ Αρχείο: {OUTPUT_PATH}")
