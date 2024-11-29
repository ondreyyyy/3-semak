import unittest
import zipfile
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from commands.cp import execute as cp_execute

class TestCPCommand(unittest.TestCase):
    def setUp(self):
        # Создание тестового архива
        self.test_zip = "test_vfs.zip"
        with zipfile.ZipFile(self.test_zip, "w") as archive:
            archive.writestr("file1.txt", "This is file1.")
            archive.writestr("dir1/file2.txt", "This is file2.")
            archive.writestr("dir1/dir2/file3.txt", "This is file3.")

        # Открытие архива для тестов
        self.vfs = zipfile.ZipFile(self.test_zip, "a")

    def tearDown(self):
        # Закрытие и удаление тестового архива
        self.vfs.close()
        if os.path.exists(self.test_zip):
            os.remove(self.test_zip)

    def test_copy_in_same_directory(self):
        """Проверка копирования файла в той же директории."""
        result = cp_execute(self.vfs, "/", "file1.txt", "file1_copy.txt")
        self.assertEqual(result, "Copied 'file1.txt' to 'file1_copy.txt'.")
        with zipfile.ZipFile(self.test_zip, "r") as archive:
            self.assertIn("file1_copy.txt", archive.namelist())

    def test_copy_in_subdirectory(self):
        """Проверка копирования файла внутри поддиректории."""
        result = cp_execute(self.vfs, "dir1", "file2.txt", "file2_copy.txt")
        self.assertEqual(result, "Copied 'file2.txt' to 'file2_copy.txt'.")
        with zipfile.ZipFile(self.test_zip, "r") as archive:
            self.assertIn("dir1/file2_copy.txt", archive.namelist())

    def test_copy_to_root_from_subdirectory(self):
        """Проверка копирования файла из поддиректории в корневую директорию."""
        result = cp_execute(self.vfs, "dir1", "file2.txt", "/file2_copy.txt")
        self.assertEqual(result, "Copied 'file2.txt' to '/file2_copy.txt'.")
        with zipfile.ZipFile(self.test_zip, "r") as archive:
            self.assertIn("file2_copy.txt", archive.namelist())

    def test_copy_nonexistent_file(self):
        """Проверка ошибки при попытке копирования несуществующего файла."""
        result = cp_execute(self.vfs, "/", "nonexistent.txt", "copy.txt")
        self.assertEqual(result, "Source file 'nonexistent.txt' not found. path = 'nonexistent.txt'")

    def test_copy_to_nested_directory(self):
        """Проверка копирования файла в вложенную директорию."""
        result = cp_execute(self.vfs, "/", "file1.txt", "dir1/dir2/file1_copy.txt")
        self.assertEqual(result, "Copied 'file1.txt' to 'dir1/dir2/file1_copy.txt'.")
        with zipfile.ZipFile(self.test_zip, "r") as archive:
            self.assertIn("dir1/dir2/file1_copy.txt", archive.namelist())

    def test_copy_absolute_to_absolute(self):
        """Проверка копирования файла по абсолютным путям."""
        result = cp_execute(self.vfs, "/", "/file1.txt", "/file1_copy.txt")
        self.assertEqual(result, "Copied '/file1.txt' to '/file1_copy.txt'.")
        with zipfile.ZipFile(self.test_zip, "r") as archive:
            self.assertIn("file1_copy.txt", archive.namelist())

    def test_copy_with_relative_path(self):
        """Проверка копирования файла с использованием относительного пути."""
        result = cp_execute(self.vfs, "dir1", "../file1.txt", "file1_copy.txt")
        self.assertEqual(result, "Copied '../file1.txt' to 'file1_copy.txt'.")
        with zipfile.ZipFile(self.test_zip, "r") as archive:
            self.assertIn("dir1/file1_copy.txt", archive.namelist())


if __name__ == "__main__":
    unittest.main()
