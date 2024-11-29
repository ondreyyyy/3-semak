import unittest
import zipfile
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from commands.cd import execute as cd_execute

class TestCDCommand(unittest.TestCase):
    def setUp(self):
        # Создание временного архива
        self.test_vfs = "test_vfs.zip"
        with zipfile.ZipFile(self.test_vfs, "w") as zf:
            zf.writestr("file1.txt", "Content of file1")
            zf.writestr("dir1/file2.txt", "Content of file2")
            zf.writestr("dir1/dir2/file3.txt", "Content of file3")
            zf.writestr("dir2/file4.txt", "Content of file4")
            zf.writestr("dir1/", "")
            zf.writestr("dir1/dir2/", "")
            zf.writestr("dir2/", "")

        # Открытие архива для тестов
        self.vfs = zipfile.ZipFile(self.test_vfs, "a")

    def tearDown(self):
        # Закрытие и удаление тестового архива
        self.vfs.close()
        if os.path.exists(self.test_vfs):
            os.remove(self.test_vfs)

    def test_cd_current_directory(self):
        result = cd_execute(self.vfs, "/", "")
        self.assertEqual(result, "/")

    def test_cd_root(self):
        result = cd_execute(self.vfs, "dir1/", "/")
        self.assertEqual(result, "/")

    def test_cd_valid_directory(self):
        result = cd_execute(self.vfs, "/", "dir1")
        self.assertEqual(result, "dir1/")

    def test_cd_nested_directory(self):
        result = cd_execute(self.vfs, "dir1/", "dir2")
        expected_result = os.path.normpath("dir1/dir2/") + "/"
        self.assertEqual(result, expected_result)

    def test_cd_invalid_directory(self):
        with self.assertRaises(FileNotFoundError):
            cd_execute(self.vfs, "/", "nonexistent")

    def test_cd_parent_directory(self):
        result = cd_execute(self.vfs, "dir1/dir2/", "..")
        self.assertEqual(result, "dir1/")

    def test_cd_absolute_path(self):
        result = cd_execute(self.vfs, "dir1/", "/dir2")
        expected_result = os.path.normpath("dir2/") + "/"
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
