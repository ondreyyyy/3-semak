import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from commands.exit_shell import execute as exit_shell_execute


class TestExitShell(unittest.TestCase):
    def test_exit(self):
        with self.assertRaises(SystemExit):
            exit_shell_execute()


if __name__ == "__main__":
    unittest.main()
