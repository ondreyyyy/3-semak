import unittest
import zipfile
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from commands.ls import execute as ls_execute


class TestLS(unittest.TestCase):
    def setUp(self):
        # Создание временного архива
        self.test_vfs = "test_vfs.zip"
        with zipfile.ZipFile(self.test_vfs, "w") as zf:
            zf.writestr("file1.txt", "Content of file1")
            zf.writestr("dir1/file2.txt", "Content of file2")
            zf.writestr("dir1/file3.txt", "Content of file3")
            zf.writestr("dir2/file4.txt", "Content of file4")

    def tearDown(self):
        # Удаление временного архива
        os.remove(self.test_vfs)

    def test_ls_root(self):
        with zipfile.ZipFile(self.test_vfs, "r") as vfs:
            result = ls_execute(vfs, "/", "")
            self.assertIn("file1.txt", result)
            self.assertIn("dir1/", result)
            self.assertIn("dir2/", result)

    def test_ls_root_with_path(self):
        with zipfile.ZipFile(self.test_vfs, "r") as vfs:
            result = ls_execute(vfs, "/", "/")
            self.assertIn("file1.txt", result)
            self.assertIn("dir1/", result)
            self.assertIn("dir2/", result)

    def test_ls_subdir_dir1(self):
        with zipfile.ZipFile(self.test_vfs, "r") as vfs:
            result = ls_execute(vfs, "/", "dir1")
            self.assertIn("file2.txt", result)
            self.assertIn("file3.txt", result)
            self.assertNotIn("file1.txt", result)  # Проверка, что файл из корня не включён

    def test_ls_subdir_dir2(self):
        with zipfile.ZipFile(self.test_vfs, "r") as vfs:
            result = ls_execute(vfs, "/", "dir2")
            self.assertIn("file4.txt", result)
            self.assertNotIn("file1.txt", result)

    def test_ls_nonexistent_dir(self):
        with zipfile.ZipFile(self.test_vfs, "r") as vfs:
            result = ls_execute(vfs, "/", "nonexistent_dir")
            self.assertEqual(result, "Directory not found or Directory is empty.")

    def test_ls_empty_dir(self):
        with zipfile.ZipFile(self.test_vfs, "a") as zf:
            zf.writestr("empty_dir/", "")

        with zipfile.ZipFile(self.test_vfs, "r") as vfs:
            result = ls_execute(vfs, "/", "empty_dir")
            self.assertEqual(result, "Directory not found or Directory is empty.")


if __name__ == "__main__":
    unittest.main()
