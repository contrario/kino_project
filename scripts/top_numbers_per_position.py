import os
import requests
import pandas as pd
import time
from datetime import datetime, timedelta

def get_draws_for_date(date_str):
    url = "https://api.opap.gr/draws/v3.0/1100/draw-date/" + (date_str or '') + "/" + date_str
    try:
        response = requests.get(url)
        response.raise_for_status()
        draws = response.json()['content']
        return draws
    except Exception as e:
        print(f"[{date_str}] Σφάλμα API: {e}")
        return []

def process_draw(draw):
    numbers = draw.get('winningNumbers', {}).get('list', [])
    if len(numbers) != 20:
        return None
    numbers.sort()
    return {
        'draw_id': draw['drawId'],
        'draw_time': datetime.fromtimestamp(draw['drawTime'] / 1000),
        **{f'num_{i+1}': num for i, num in enumerate(numbers)}
    }

def collect_kino_data(start_date, end_date, output_file='kino_data.csv'):
    current_date = start_date
    all_results = []

    print(f"Ξεκινάμε συλλογή δεδομένων από {start_date.date()} έως {end_date.date()}...\n")
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        print(f"📅 {date_str}", end=': ')
        draws = get_draws_for_date(date_str)

        daily_results = []
        for draw in draws:
            processed = process_draw(draw)
            if processed:
                daily_results.append(processed)

        print(f"{len(daily_results)} κληρώσεις")
        all_results.extend(daily_results)

        current_date += timedelta(days=1)
        time.sleep(0.5)  # Μικρό delay για να μην μπλοκάρει το API

    df = pd.DataFrame(all_results)
    df.sort_values(by='draw_time', inplace=True)
    df.to_csv(output_file, index=False)
    print(f"\n✅ Τελείωσε! Αποθηκεύτηκαν {len(df)} κληρώσεις στο αρχείο: {output_file}")

# ---------------------------------------
# ✅ Επεξεργάσου αυτές τις 2 ημερομηνίες:
# ---------------------------------------
start = datetime.strptime("2024-01-01", "%Y-%m-%d")
end = datetime.strptime("2024-06-30", "%Y-%m-%d")

collect_kino_data(start, end)
