import os
import unittest
from scripts.fetchers.smart_fetch_kino_data import fetch_recent_draws

class TestFetchKinoData(unittest.TestCase):
    def test_fetch_recent_draws(self):
        """Test if recent draws are fetched and have expected structure"""
        draws = fetch_recent_draws()
        self.assertIsInstance(draws, list)
        if draws:
            self.assertGreaterEqual(len(draws), 1)
            for draw in draws:
                self.assertIn("drawId", draw)
                self.assertIn("drawTime", draw)
                self.assertIn("winningNumbers", draw)
                self.assertIn("list", draw["winningNumbers"])
                self.assertEqual(len(draw["winningNumbers"]["list"]), 20)
        else:
            print("⚠️ Προσοχή: Δεν επιστράφηκαν κληρώσεις. Έλεγξε το εύρος ημερομηνιών.")

if __name__ == "__main__":
    unittest.main()


