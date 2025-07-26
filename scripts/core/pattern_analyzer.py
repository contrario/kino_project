import os
import sys
from collections import Counter

# ✅ Προσθέτει το path του φακέλου scripts στο sys.path για να βρίσκει το utils
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.abspath(os.path.join(current_dir, '..'))
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from utils.logger import log_info  # Βεβαιώσου ότι υπάρχει

def analyze_draws(draws):
    log_info("Ξεκίνησε η ανάλυση μοτίβων...")

    all_numbers = []
    for draw in draws:
        numbers = draw.get('winningNumbers', {}).get('list', [])
        all_numbers.extend(numbers)

    counter = Counter(all_numbers)
    most_common = counter.most_common(10)

    log_info("Ανάλυση μοτίβων ολοκληρώθηκε.")
    return {
        'most_common_numbers': most_common
    }
