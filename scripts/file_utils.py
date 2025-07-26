import os
# scripts/file_utils.py

import pandas as pd

def save_to_csv(df, filename):
    try:
        df.to_csv(filename, index=False)
        print(f"💾 Saved to {filename}")
    except Exception as e:
        print(f"❌ Failed to save file: {e}")