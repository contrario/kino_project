import os
import requests
import pandas as pd
import time
from datetime import datetime, timedelta
from tqdm import tqdm

def fetch_kino_data(start_date: str, end_date: str, output_file: str = "kino_data.csv"):
    """
    Κατεβάζει αποτελέσματα ΚΙΝΟ από το API του ΟΠΑΠ για εύρος ημερομηνιών.
    Αποθηκεύει τα αποτελέσματα σε CSV αρχείο.
    """
    base_url = "https://api.opap.gr/draws/v3.0/1100/draw-date/"

    # Μετατροπή string -> datetime
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    # Συγκέντρωση όλων των αποτελεσμάτων εδώ
    all_results = []

    print(f"📅 Λήψη αποτελεσμάτων από {start_date} έως {end_date}...")

    for day in tqdm(range((end - start).days + 1)):
        current_day = start + timedelta(days=day)
        date_str = current_day.strftime("%Y-%m-%d")

        url = f"{base_url}{date_str}/{date_str}"
        try:
            response = requests.get(url)
            data = response.json()

            for draw in data['content']:
                draw_id = draw['drawId']
                draw_time = draw['drawTime']
                winning_numbers = draw['winningNumbers']['list']
                all_results.append({
                    "draw_id": draw_id,
                    "draw_time": draw_time,
                    "numbers": winning_numbers
                })

            # Μικρή καθυστέρηση για ευγένεια προς το API
            time.sleep(0.3)

        except Exception as e:
            print(f"⚠️ Σφάλμα για {date_str}: {e}")
            continue

    # Δημιουργία DataFrame
    df = pd.DataFrame(all_results)

    # Ανάλυση ώρας για heatmaps
    df['draw_time'] = pd.to_datetime(df['draw_time'])
    df['hour'] = df['draw_time'].dt.hour

    # Επέκταση αριθμών σε ξεχωριστές στήλες (number_1 ... number_20)
    numbers_df = pd.DataFrame(df['numbers'].to_list(), columns=[f"number_{i}" for i in range(1, 21)])
    final_df = pd.concat([df.drop(columns=['numbers']), numbers_df], axis=1)

    final_df.to_csv(output_file, index=False)
    print(f"✅ Αποθήκευση στο αρχείο: {output_file}")

if __name__ == "__main__":
    # 👉 Εδώ ορίζεις το εύρος
    fetch_kino_data(start_date="2024-06-01", end_date="2024-07-20")







