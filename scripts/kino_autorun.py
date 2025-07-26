import os
import requests
from datetime import datetime, timedelta
from utils.logger import log_info, log_warning, log_error
from utils.file_manager import save_data_to_csv
from analyzers.pattern_analyzer import analyze_patterns

def fetch_kino_draws(from_date: str, to_date: str):
    url = f"https://api.opap.gr/draws/v3.0/1100/draw-date/{from_date}/{to_date}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("content", [])
    except requests.exceptions.RequestException as e:
        log_error(f"Error fetching data: {e}")
        return []

def run_kino_system():
    log_info("Ξεκίνησε το αυτόματο σύστημα KINO.")

    # ✅ Επιλογή χθεσινής ημερομηνίας
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    from_date = to_date = yesterday.strftime("%Y-%m-%d")

    log_info("➡️ Ανάκτηση νέων κληρώσεων...")

    draws = fetch_kino_draws(from_date, to_date)

    if not draws:
        log_warning("⚠️ Δεν βρέθηκαν νέα δεδομένα.")
        return

    log_info(f"✅ Βρέθηκαν {len(draws)} νέες κληρώσεις.")

    # Αποθήκευση σε CSV
    save_data_to_csv(draws, "data/kino_data.csv")

    # Ανάλυση μοτίβων
    analyze_patterns(draws)

if __name__ == "__main__":
    run_kino_system()

