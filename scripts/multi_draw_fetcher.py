import requests
import csv
import os
from datetime import datetime
import time

# --- ΡΥΘΜΙΣΕΙΣ ---
# Αριθμός κληρώσεων που θέλετε να κατεβάσετε προς τα πίσω από την τελευταία.
# Βάλτε έναν μεγάλο αριθμό (π.χ. 5000 ή 10000) για να πάρετε πολλά δεδομένα.
NUM_DRAWS_TO_FETCH = 5000

# Όνομα αρχείου αποθήκευσης (πρέπει να είναι το ίδιο με αυτό που διαβάζει το kino_predictor.py)
OUTPUT_FILENAME = "kino_data.csv"

# --- ΣΥΝΑΡΤΗΣΕΙΣ ---

def get_latest_draw_id():
    """Ανακτά το τελευταίο διαθέσιμο draw_id από το API του ΟΠΑΠ."""
    # Διορθωμένο URL σύμφωνα με την τεκμηρίωση του ΟΠΑΠ
    url = "https://api.opap.gr/draws/v3.0/1100/last-result-and-active"
    try:
        response = requests.get(url)
        response.raise_for_status() # Ελέγχει για HTTP λάθη (π.χ. 404, 500)
        data = response.json()

        # Η δομή της απάντησης για το "last-result-and-active" είναι διαφορετική.
        # Το drawId βρίσκεται μέσα στο 'last' αντικείμενο.
        last_result = data.get("last")
        if last_result:
            return last_result.get("drawId")
        else:
            print("Δεν βρέθηκε 'last' αντικείμενο στην απάντηση του API.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"ΣΦΑΛΜΑ κατά την ανάκτηση του τελευταίου draw ID: {e}")
        return None

def fetch_and_save_kino_data():
    """Ανακτά δεδομένα ΚΙΝΟ και τα αποθηκεύει σε αρχείο CSV."""
    latest_draw_id = get_latest_draw_id()
    if latest_draw_id is None:
        print("Δεν μπόρεσα να ανακτήσω το τελευταίο draw ID. Διακοπή.")
        return

    print(f"Το τελευταίο διαθέσιμο draw ID είναι: {latest_draw_id}")
    print(f"Θα επιχειρήσω να κατεβάσω {NUM_DRAWS_TO_FETCH} κληρώσεις προς τα πίσω από το ID {latest_draw_id}...")

    # Φορτώνουμε τα ήδη υπάρχοντα draw_id στο Set για γρήγορο έλεγχο
    existing_draw_ids = set()
    if os.path.exists(OUTPUT_FILENAME):
        with open(OUTPUT_FILENAME, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            # Ελέγχουμε αν υπάρχει η στήλη 'draw_id'
            if 'draw_id' in reader.fieldnames:
                for row in reader:
                    existing_draw_ids.add(row["draw_id"])
            else:
                print(f"ΠΡΟΕΙΔΟΠΟΙΗΣΗ: Το αρχείο '{OUTPUT_FILENAME}' δεν περιέχει στήλη 'draw_id'. Θα το ξαναγράψω.")
                # Αν δεν υπάρχει η στήλη, θεωρούμε ότι το αρχείο είναι προβληματικό και θα το ξαναγράψουμε
                existing_draw_ids.clear() # Καθαρίζουμε το set για να ξαναγραφτεί το αρχείο

    # Ανοίγουμε το αρχείο σε 'a' (append) mode. Αν δεν υπάρχει, θα δημιουργηθεί.
    # Το newline='' είναι σημαντικό για τα CSV files
    with open(OUTPUT_FILENAME, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)

        # Γράφουμε την κεφαλίδα μόνο αν το αρχείο είναι άδειο (νέο ή ξαναγράφτηκε)
        if os.path.getsize(OUTPUT_FILENAME) == 0 or not existing_draw_ids:
            writer.writerow(["draw_id", "draw_time", "winning_numbers"])
            print(f"Δημιουργήθηκε νέο αρχείο '{OUTPUT_FILENAME}' με κεφαλίδα.")

        # Ξεκινάμε από το τελευταίο ID και πάμε προς τα πίσω
        for i, draw_id in enumerate(range(latest_draw_id, latest_draw_id - NUM_DRAWS_TO_FETCH, -1)):
            if str(draw_id) in existing_draw_ids:
                if i % 100 == 0:
                    print(f"[{draw_id}] ⚠️ Ήδη υπάρχει (προσπερνώ {i+1}/{NUM_DRAWS_TO_FETCH}).")
                continue

            url = f"https://api.opap.gr/draws/v3.0/1100/{draw_id}"
            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"[{draw_id}] ❌ ΣΦΑΛΜΑ κατά την ανάκτηση: {e}. Συνέχεια στην επόμενη κλήρωση.")
                time.sleep(1)
                continue

            data = response.json()
            numbers = data.get("winningNumbers", {}).get("list", [])
            draw_time_ms = data.get("drawTime")

            if not numbers or draw_time_ms is None:
                print(f"[{draw_id}] ❌ Δεν βρέθηκαν πλήρη δεδομένα για την κλήρωση. Προσπερνώ.")
                continue

            draw_datetime = datetime.fromtimestamp(draw_time_ms / 1000).strftime("%Y-%m-%d %H:%M:%S")

            writer.writerow([draw_id, draw_datetime, ",".join(map(str, numbers))])
            existing_draw_ids.add(str(draw_id))
            if i % 10 == 0:
                print(f"[{draw_id}] ✅ Αποθηκεύτηκε ({i+1}/{NUM_DRAWS_TO_FETCH}).")

            time.sleep(0.1)

    print(f"\nΟλοκληρώθηκε η άντληση δεδομένων. Συνολικά {len(existing_draw_ids)} μοναδικές κληρώσεις στο '{OUTPUT_FILENAME}'.")
    print("Θυμηθείτε να επανεκτελέσετε το 'kino_predictor.py' για να χρησιμοποιήσει τα νέα δεδομένα.")


# --- ΚΥΡΙΟ ΠΡΟΓΡΑΜΜΑ ---
if __name__ == "__main__":
    fetch_and_save_kino_data()