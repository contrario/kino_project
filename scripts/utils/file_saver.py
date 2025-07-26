import os
import csv
from datetime import datetime
from scripts.utils.logger import log_info

def save_draws_to_csv(draws, filepath):
    if not draws:
        log_info("⚠️ Δεν υπάρχουν δεδομένα για αποθήκευση.")
        return

    fieldnames = ['drawId', 'drawTime', 'winningNumbers']
    with open(filepath, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for draw in draws:
            writer.writerow({
                'drawId': draw.get('drawId'),
                'drawTime': datetime.fromtimestamp(draw.get('drawTime') / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                'winningNumbers': ','.join(map(str, draw.get('winningNumbers', {}).get('list', [])))
            })

    log_info(f"📁 Δεδομένα αποθηκεύτηκαν στο αρχείο: {filepath}")