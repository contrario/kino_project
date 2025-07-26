# scripts/smart_fetcher.py

import requests
import pandas as pd
import time
from datetime import datetime, timedelta
import os

def fetch_kino_data(start_date, end_date, output_file='data/kino_data.csv'):
    base_url = "https://api.opap.gr/draws/v3.0/1100/draw-date/"
    current_date = start_date
    all_results = []

    print(f"🟡 Συλλογή από {start_date.date()} έως {end_date.date()}...\n")

    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        print(f"📅 {date_str}", end=': ')

        try:
            url = f"{base_url}{date_str}/{date_str}"
            response = requests.get(url)
            response.raise_for_status()
            draws = response.json()['content']
        except Exception as e:
            print(f"❌ API Σφάλμα: {e}")
            current_date += timedelta(days=1)
            continue

        daily_results = []
        for draw in draws:
            numbers = draw.get('winningNumbers', {}).get('list', [])
            if len(numbers) != 20:
                continue
            numbers.sort()
            row = {
                'draw_id': draw['drawId'],
                'draw_time': datetime.fromtimestamp(draw['drawTime'] / 1000)
            }
            for i, num in enumerate(numbers):
                row[f'num_{i+1}'] = num
            daily_results.append(row)

        print(f"{len(daily_results)} κληρώσεις")
        all_results.extend(daily_results)
        current_date += timedelta(days=1)
        time.sleep(0.3)

    df = pd.DataFrame(all_results)
    df.sort_values(by='draw_time', inplace=True)

    os.makedirs('data', exist_ok=True)
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"\n✅ Αποθηκεύτηκαν {len(df)} κληρώσεις στο αρχείο: {output_file}")