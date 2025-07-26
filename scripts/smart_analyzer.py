import pandas as pd
import numpy as np
from collections import Counter
import os

# 📌 Ρύθμιση διαδρομής αρχείου CSV
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'kino_data.csv')

def load_kino_data(filepath: str) -> pd.DataFrame:
    """Φόρτωση και προεπεξεργασία δεδομένων ΚΙΝΟ"""
    df = pd.read_csv(filepath)
    if 'draw_id' not in df.columns:
        raise ValueError("Το αρχείο δεν περιέχει σωστά δεδομένα.")
    return df

def flatten_draws(df: pd.DataFrame) -> list:
    """Εξαγωγή όλων των αριθμών από τις κληρώσεις"""
    number_cols = [col for col in df.columns if col.startswith('num_')]
    flat_numbers = df[number_cols].values.flatten().tolist()
    return [int(num) for num in flat_numbers if not pd.isna(num)]

def get_most_common(numbers: list, top_n: int = 10) -> pd.Series:
    """Οι πιο συχνοί αριθμοί"""
    counter = Counter(numbers)
    return pd.Series(dict(counter.most_common(top_n)))

def get_least_common(numbers: list, bottom_n: int = 10) -> pd.Series:
    """Οι λιγότερο συχνοί αριθμοί"""
    counter = Counter(numbers)
    least_common = counter.most_common()[:-bottom_n-1:-1]
    return pd.Series(dict(least_common))

def generate_ticket(freq_counter: Counter, ticket_size: int = 12) -> list:
    """Πρόταση δελτίου βάσει συχνότητας"""
    return [int(num) for num, _ in freq_counter.most_common(ticket_size)]

# 🚀 Κύρια λειτουργία
def main():
    print("\n📂 Ανάλυση δεδομένων ΚΙΝΟ...\n")

    try:
        df = load_kino_data(data_path)
        print(f"✅ Φορτώθηκαν {len(df)} κληρώσεις.\n")
    except Exception as e:
        print(f"❌ Σφάλμα κατά τη φόρτωση: {e}")
        return

    numbers = flatten_draws(df)

    most_common = get_most_common(numbers, top_n=10)
    least_common = get_least_common(numbers, bottom_n=10)
    freq_counter = Counter(numbers)
    ticket = generate_ticket(freq_counter, ticket_size=12)

    print("📊 Πιο συχνοί αριθμοί:")
    print(most_common)
    print("\n📉 Λιγότερο συχνοί αριθμοί:")
    print(least_common)
    print(f"\n🎯 Προτεινόμενο δελτίο (βάσει συχνότητας): {ticket}\n")

if __name__ == "__main__":
    main()