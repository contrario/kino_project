import unittest
import os
import pandas as pd

from scripts.utils import logger, file_manager
from scripts.analysis import pattern_analyzer

class TestLogger(unittest.TestCase):
    def test_log_info(self):
        # Απλά τσεκάρει ότι το log_info δεν πετάει exception
        try:
            logger.log_info("Testing log_info message.")
        except Exception as e:
            self.fail(f"log_info raised an exception: {e}")

class TestFileManager(unittest.TestCase):
    def setUp(self):
        # Χρησιμοποιούμε έγκυρα δεδομένα με σωστό drawTime σε milliseconds
        self.test_data = [
            {"drawId": 1, "drawTime": 1753012800000, "winningNumbers": {"list": [1, 2, 3, 4, 5]}},
            {"drawId": 2, "drawTime": 1753013100000, "winningNumbers": {"list": [6, 7, 8, 9, 10]}}
        ]
        self.test_path = "tests/test_kino_data.csv"

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_save_and_read_csv(self):
        file_manager.save_data_to_csv(self.test_data, self.test_path)
        df = pd.read_csv(self.test_path)
        self.assertEqual(len(df), 2)
        self.assertIn("draw_id", df.columns)
        self.assertIn("numbers", df.columns)
        self.assertEqual(df.iloc[0]["draw_id"], 1)

class TestPatternAnalyzer(unittest.TestCase):
    def setUp(self):
        # Δημιουργούμε ένα προσωρινό αρχείο CSV με αριθμούς
        self.temp_path = "tests/test_pattern_input.csv"
        with open(self.temp_path, "w", encoding="utf-8") as f:
            f.write("draw_id,draw_time,numbers\n")
            f.write("1,2025-07-20 12:00:00,\"2,4,6,8,10\"\n")
            f.write("2,2025-07-20 12:05:00,\"2,4,6,11,12\"\n")  # 2 εμφανίζεται 2 φορές

    def tearDown(self):
        if os.path.exists(self.temp_path):
            os.remove(self.temp_path)

    def test_analyze_patterns(self):
        freq = pattern_analyzer.analyze_patterns(self.temp_path)
        self.assertIsInstance(freq, dict)
        self.assertGreaterEqual(freq.get(2, 0), 2)  # Ο αριθμός 2 εμφανίζεται τουλάχιστον 2 φορές

if __name__ == '__main__':
    unittest.main()