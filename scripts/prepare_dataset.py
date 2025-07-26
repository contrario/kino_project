import os
import pandas as pd
from pathlib import Path

# Απόλυτο path προς το αρχείο
input_file = Path(__file__).resolve().parent.parent / 'data' / 'kino_draws.csv'

# Έλεγχος ύπαρξης αρχείου
if not input_file.exists():
    print(f"❌ Το αρχείο δεν βρέθηκε: {input_file}")
else:
    print("✅ Το αρχείο φορτώθηκε")
    df = pd.read_csv(input_file)

    if 'numbers' not in df.columns:
        print("❌ Δεν βρέθηκε η στήλη 'numbers'")
        print(f"📋 Διαθέσιμες στήλες: {df.columns.tolist()}")
    else:
        print("✅ Η στήλη 'numbers' βρέθηκε")
        print(df.head())

















