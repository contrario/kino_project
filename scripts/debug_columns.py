import os
import pandas as pd

input_file = r'C:\Users\Hlias\Documents\kino_project\data\kino_draws.csv'

df = pd.read_csv(input_file)

print("📋 Στήλες του αρχείου:")
print(df.columns.tolist())

print("\n🔍 Προεπισκόπηση πρώτων γραμμών:")
print(df.head())