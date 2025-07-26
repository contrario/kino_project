import os
import csv
from collections import Counter

# 📥 Διαβάζουμε το αρχείο
with open('kino_data.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Παράλειψη επικεφαλίδας
    all_numbers = []

    for row in reader:
        if row:  # Αν η γραμμή δεν είναι κενή
            numbers_str = row[1].split(',')  # Υποθέτουμε ότι οι αριθμοί είναι στη στήλη 1 (δεύτερη)
            numbers = [int(n.strip()) for n in numbers_str if n.strip().isdigit()]
            all_numbers.extend(numbers)

# 📊 Υπολογισμός συχνοτήτων
counter = Counter(all_numbers)

# 💾 Αποθήκευση σε νέο αρχείο
with open('frequencies.csv', 'w', newline='', encoding='utf-8') as f_out:
    writer = csv.writer(f_out)
    writer.writerow(['Αριθμός', 'Συχνότητα'])
    for number, freq in sorted(counter.items(), key=lambda x: -x[1]):
        writer.writerow([number, freq])

# ✅ Μήνυμα επιτυχίας
print("✅ Οι συχνότητες αποθηκεύτηκαν στο αρχείο 'frequencies.csv'")
