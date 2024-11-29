import unittest
import time
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from commands.uptime import execute as uptime_execute


class TestUptime(unittest.TestCase):
    def test_uptime(self):
        time.sleep(1)  # Подождём немного, чтобы проверить отсчёт времени
        result = uptime_execute()
        self.assertIn("Uptime:", result)
        self.assertIn("h", result)
        self.assertIn("m", result)
        self.assertIn("s", result)


if __name__ == "__main__":
    unittest.main()
