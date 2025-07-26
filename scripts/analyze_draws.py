import csv
from collections import Counter
import os

# Υπολογισμός διαδρομής αρχείου ανεξάρτητα από το πού εκτελείται το script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRAW_FILE = os.path.join(BASE_DIR, "data", "kino_draws.csv")

# Αρχικοποίηση Counter για καταμέτρηση συχνοτήτων αριθμών
number_counter = Counter()

# Διαβάζουμε το CSV και μετράμε τις εμφανίσεις κάθε αριθμού
try:
    with open(DRAW_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            raw_numbers = row.get("numbers", "")
            delimiter = ';' if ';' in raw_numbers else ','

            try:
                numbers = [int(n.strip()) for n in raw_numbers.split(delimiter) if n.strip().isdigit()]
                number_counter.update(numbers)
            except ValueError:
                print(f"❌ Σφάλμα στη μετατροπή: {raw_numbers}")
except FileNotFoundError:
    print(f"❌ Το αρχείο δεν βρέθηκε: {DRAW_FILE}")
    exit(1)

# Εμφάνιση συχνοτήτων με ταξινόμηση κατά φθίνουσα σειρά
print("\n📊 Συχνότητα εμφάνισης αριθμών στο ΚΙΝΟ:\n")
for number, freq in number_counter.most_common():
    print(f"Αριθμός {number:>2} εμφανίστηκε {freq} φορές")