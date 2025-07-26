import os
from pathlib import Path

file_path = Path("C:/Users/Hlias/Documents/kino_project/data/kino_draws.csv")

if file_path.exists():
    print("✅ Βρέθηκε το αρχείο!")
else:
    print("❌ Δεν υπάρχει αρχείο με αυτό το όνομα σε αυτό το path.")