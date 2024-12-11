import unittest
from unittest.mock import patch, MagicMock
import os
import subprocess
from visualizer import visualize_graph, visualize_graph_on_screen
from graph_builder import get_commits, get_commit_files, build_dependency_graph, save_graph_to_dot


class TestVisualizer(unittest.TestCase):

    @patch('visualizer.visualize_graph_on_screen')
    @patch('subprocess.run')
    def test_visualize_graph_failure(self, mock_run, mock_screen):
        # Моделируем ошибку вызова команды
        mock_run.side_effect = subprocess.CalledProcessError(1, ['dot'])

        # Проверяем, что исключение вызывается
        try:
            visualize_graph("test.dot", "dot")
        except subprocess.CalledProcessError as e:
            # Проверяем, что subprocess.CalledProcessError поднят
            self.assertEqual(e.returncode, 1)
            self.assertEqual(e.cmd, ['dot'])

        # Проверяем вызов subprocess.run
        mock_run.assert_called_once_with(
            ["dot", "-Tpng", "test.dot", "-o", "dependencies.png"],
            check=True,
            capture_output=True,
            text=True
        )
        # Убедимся, что visualize_graph_on_screen не был вызван
        mock_screen.assert_not_called()

    @patch('subprocess.run')
    def test_visualize_graph_file_not_found(self, mock_run):
        # Симулируем ошибку, если программа не найдена
        mock_run.side_effect = FileNotFoundError
        with patch('visualizer.visualize_graph_on_screen') as mock_screen:
            visualize_graph('test.dot', 'dot')
            mock_run.assert_called_once_with(
                ['dot', '-Tpng', 'test.dot', '-o', 'dependencies.png'],
                check=True,
                capture_output=True,
                text=True
            )

    @patch('subprocess.run')
    def test_visualize_graph_success(self, mock_run):
        # Подготовим моки
        mock_run.return_value = MagicMock(returncode=0)
        with patch('visualizer.visualize_graph_on_screen') as mock_screen:
            visualize_graph('test.dot', 'dot')
            mock_run.assert_called_once_with(
                ['dot', '-Tpng', 'test.dot', '-o', 'dependencies.png'],
                check=True,
                capture_output=True,
                text=True
            )
            mock_screen.assert_called_once_with('dependencies.png')

    @patch('subprocess.run')
    def test_visualize_graph_on_screen_linux(self, mock_run):
        # Тест для Linux
        with patch('os.name', 'posix'):
            with patch('subprocess.run') as mock_subprocess:
                visualize_graph_on_screen('dependencies.png')
                mock_subprocess.assert_called_once_with(['xdg-open', 'dependencies.png'])

    @patch('subprocess.run')
    def test_visualize_graph_on_screen_windows(self, mock_run):
        # Тест для Windows
        with patch('os.name', 'nt'):
            with patch('subprocess.run') as mock_subprocess:
                visualize_graph_on_screen('dependencies.png')
                mock_subprocess.assert_called_once_with(['mspaint', 'dependencies.png'])

    @patch('subprocess.run')
    def test_visualize_graph_on_screen_mac(self, mock_run):
        # Тест для macOS
        with patch('os.name', 'darwin'):
            with patch('subprocess.run') as mock_subprocess:
                visualize_graph_on_screen('dependencies.png')
                mock_subprocess.assert_called_once_with(['open', 'dependencies.png'])

    @patch('subprocess.run')
    def test_get_commits_success(self, mock_run):
        # Мокируем успешный вызов git log
        mock_run.return_value = MagicMock(returncode=0, stdout='commit1\ncommit2\n')
        commits = get_commits('test_repo')
        self.assertEqual(commits, ['commit1', 'commit2'])
        mock_run.assert_called_once_with(['git', '-C', 'test_repo', 'log', '--pretty=format:%H'], capture_output=True,
                                         text=True, check=True)

    @patch('subprocess.run')
    def test_get_commits_failure(self, mock_run):
        # Мокируем ошибку при вызове git log
        mock_run.side_effect = subprocess.CalledProcessError(1, 'git')
        with self.assertRaises(subprocess.CalledProcessError):
            get_commits('test_repo')

    @patch('subprocess.run')
    def test_get_commit_files(self, mock_run):
        # Мокируем успешный вызов git show
        mock_run.return_value = MagicMock(returncode=0, stdout='file1\nfile2\n')
        files = get_commit_files('test_repo', 'commit1')
        self.assertEqual(files, ['file1', 'file2'])
        mock_run.assert_called_once_with(['git', '-C', 'test_repo', 'show', '--pretty=', '--name-only', 'commit1'],
                                         capture_output=True, text=True, check=True)

    @patch('subprocess.run')
    def test_build_dependency_graph(self, mock_run):
        # Мокируем вызовы get_commits и get_commit_files
        with patch('graph_builder.get_commits') as mock_get_commits:
            with patch('graph_builder.get_commit_files') as mock_get_files:
                mock_get_commits.return_value = ['commit1', 'commit2']
                mock_get_files.side_effect = [['file1', 'file2'], ['file3', 'file4']]

                graph = build_dependency_graph('test_repo')
                self.assertIsNotNone(graph)
                graph_nodes = {os.path.basename(node) for node in graph['nodes']}
                self.assertIn('commit1', graph_nodes)
                self.assertIn('file1', graph_nodes)
                self.assertIn(('commit1', os.path.abspath('file1')), graph['edges'])

    def test_save_graph_to_dot(self):
        # Тестируем успешное сохранение DOT файла
        graph = {
            "nodes": {'commit1', 'file1'},
            "edges": {('commit1', 'file1')},
            "file_to_commits": {'file1': {'commit1'}}
        }
        with patch('builtins.open', unittest.mock.mock_open()) as mock_open:
            save_graph_to_dot(graph, 'test.dot')
            mock_open.assert_called_once_with('test.dot', 'w')
            handle = mock_open()
            handle.write.assert_any_call('  "commit1" [label="commit1"];\n')
            handle.write.assert_any_call('  "file1" [label="file1"];\n')


if __name__ == '__main__':
    unittest.main()
