import pandas as pd
import os

# Βρες το path
base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, "kino_data.csv")

# Φόρτωσε το CSV
df = pd.read_csv(data_path)

# Δείξε όλες τις στήλες
print("📄 Όλες οι στήλες:")
print(list(df.columns))

# Δείξε τις πρώτες 5 γραμμές
print("\n🔍 Πρώτες 5 γραμμές:")
print(df.head())