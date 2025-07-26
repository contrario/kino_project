import os
# scripts/hot_cold_numbers.py

from collections import Counter

def identify_hot_cold_numbers(draws_df, top_n=10):
    try:
        all_numbers = [num for sublist in draws_df['winning_numbers'] for num in sublist]
        freq = Counter(all_numbers)

        sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        hot = [num for num, _ in sorted_freq[:top_n]]
        cold = [num for num, _ in sorted_freq[-top_n:]]

        return hot, cold
    except Exception as e:
        print(f"❌ Error in identify_hot_cold_numbers: {e}")
        return [], []