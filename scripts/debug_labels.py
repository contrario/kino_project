import os
import pandas as pd

df = pd.read_csv("data/kino_dataset_cleaned.csv")

print("🔍 Προεπισκόπηση label τιμών:")
print(df['label'].head(10))

print("\n📊 Τύποι:")
print(df['label'].apply(type).value_counts())