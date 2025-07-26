import sys
import os
import unittest

# ✅ Προσθήκη του φακέλου scripts στο path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from core.pattern_analyzer import analyze_draws

class TestPatternAnalyzer(unittest.TestCase):
    def test_analyze_draws_basic(self):
        sample_draws = [
            {'drawId': 1, 'winningNumbers': {'list': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}},
            {'drawId': 2, 'winningNumbers': {'list': [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]}},
            {'drawId': 3, 'winningNumbers': {'list': [5, 10, 15, 20, 25, 30, 35, 40, 45, 49]}}
        ]

        result = analyze_draws(sample_draws)

        self.assertIsInstance(result, dict)
        self.assertIn('most_common_numbers', result)
        self.assertGreater(len(result['most_common_numbers']), 0)

if __name__ == '__main__':
    unittest.main()


