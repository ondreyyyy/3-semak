import unittest
import zipfile
from io import BytesIO
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from commands.tac import execute as tac_execute

class TestTacCommand(unittest.TestCase):
    def setUp(self):
        # Создаем виртуальный архив VFS с тестовыми данными
        self.vfs_data = BytesIO()
        with zipfile.ZipFile(self.vfs_data, "w") as zf:
            zf.writestr("file1.txt", "Line 1\nLine 2\nLine 3")
            zf.writestr("dir1/file2.txt", "Alpha\nBeta\nGamma")
            zf.writestr("dir1/file3.txt", "")
            zf.writestr("dir2/file4.txt", "Only line")
        self.vfs_data.seek(0)
        self.vfs = zipfile.ZipFile(self.vfs_data)

    def tearDown(self):
        self.vfs.close()
        self.vfs_data.close()

    def test_tac_root_file(self):
        result = tac_execute(self.vfs, "/", "file1.txt")
        expected = "Line 3\nLine 2\nLine 1"
        self.assertEqual(result, expected)

    def test_tac_subdir_file_relative(self):
        result = tac_execute(self.vfs, "/dir1", "file2.txt")
        expected = "Gamma\nBeta\nAlpha"
        self.assertEqual(result, expected)

    def test_tac_subdir_file_absolute(self):
        result = tac_execute(self.vfs, "/", "dir1/file2.txt")
        expected = "Gamma\nBeta\nAlpha"
        self.assertEqual(result, expected)

    def test_tac_empty_file(self):
        result = tac_execute(self.vfs, "/dir1", "file3.txt")
        expected = ""
        self.assertEqual(result, expected)

    def test_tac_nonexistent_file(self):
        result = tac_execute(self.vfs, "/", "nonexistent.txt")
        expected = "File 'nonexistent.txt' not found in '/'."
        self.assertEqual(result, expected)

    def test_tac_subdir_nonexistent_file(self):
        result = tac_execute(self.vfs, "/dir1", "missing.txt")
        expected = "File 'missing.txt' not found in '/dir1'."
        self.assertEqual(result, expected)

    def test_tac_nested_subdir_file(self):
        result = tac_execute(self.vfs, "/dir2", "../dir1/file2.txt")
        expected = "Gamma\nBeta\nAlpha"
        self.assertEqual(result, expected)

    def test_tac_invalid_usage(self):
        result = tac_execute(self.vfs, "/", "")
        expected = "Usage: tac <file_path>"
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
