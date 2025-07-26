import os
# scripts/plot_kino_data.py

import matplotlib.pyplot as plt
from collections import Counter

def plot_frequency_bar_chart(draws_df):
    try:
        all_numbers = [num for sublist in draws_df['winning_numbers'] for num in sublist]
        freq = Counter(all_numbers)

        numbers = list(freq.keys())
        frequencies = list(freq.values())

        plt.figure(figsize=(14, 6))
        plt.bar(numbers, frequencies, color='skyblue')
        plt.xlabel("Numbers")
        plt.ylabel("Frequency")
        plt.title("KINO Number Frequencies")
        plt.xticks(range(1, 81), rotation=90)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig("kino_frequency_chart.png")
        print("🖼️ Saved chart as kino_frequency_chart.png")
        plt.close()
    except Exception as e:
        print(f"❌ Error plotting frequency chart: {e}")