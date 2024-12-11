import os
import subprocess

def get_commits(repository_path):
    if not os.path.isdir(repository_path):
        print(f"Error: Repository at '{repository_path}' does not exist.")
        return []

    try:
        cmd = ["git", "-C", repository_path, "log", "--pretty=format:%H"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error while fetching commits: {e.stderr}")
        raise
    except FileNotFoundError:
        print("Error: Git is not installed or not found in PATH.")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

def save_graph_to_dot(graph, file_path):
    if not graph:
        print("Error: Graph is empty. Nothing to save.")
        return

    try:
        with open(file_path, "w") as f:
            f.write("digraph G {\n")
            for node in graph["nodes"]:
                label = os.path.basename(node)
                f.write(f'  "{node}" [label="{label}"];\n')
            for edge in graph["edges"]:
                f.write(f'  "{edge[0]}" -> "{edge[1]}";\n')
            f.write("}\n")
        print(f"Graph saved to '{file_path}'")
    except Exception as e:
        print(f"Error saving graph to DOT file: {e}")


def get_commit_files(repository_path, commit_hash):
    try:
        cmd = ["git", "-C", repository_path, "show", "--pretty=", "--name-only", commit_hash]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error while fetching files for commit {commit_hash}: {e.stderr}")
        raise

def get_directories_from_files(files):
    directories = set()
    for file in files:
        directory = os.path.dirname(file)
        if directory:
            directories.add(directory)
    return directories

def build_dependency_graph(repository_path):
    try:
        commits = get_commits(repository_path)
    except Exception as e:
        print(f"Failed to build dependency graph: {e}")
        return None

    graph = {"nodes": set(), "edges": set(), "file_to_commits": {}}

    for commit in commits:
        try:
            files = get_commit_files(repository_path, commit)
        except Exception as e:
            print(f"Skipping commit {commit} due to error: {e}")
            continue

        directories = get_directories_from_files(files)

        # Добавление коммита как узла
        graph["nodes"].add(commit)
        for file in files:
            full_path = os.path.abspath(file)
            # Добавление файла как узла и связи с коммитом
            graph["nodes"].add(full_path)
            graph["edges"].add((commit, full_path))

            # Связываем файлы, изменённые в одном коммите
            if full_path not in graph["file_to_commits"]:
                graph["file_to_commits"][full_path] = set()
            graph["file_to_commits"][full_path].add(commit)

        for directory in directories:
            full_path = os.path.abspath(directory)
            # Добавление папки как узла и связи с файлами
            graph["nodes"].add(full_path)
            for file in files:
                if os.path.dirname(file) == directory:
                    graph["edges"].add((full_path, os.path.abspath(file)))

    # Создание транзитивных зависимостей
    for file_commits in graph["file_to_commits"].values():
        commits_list = list(file_commits)
        for i in range(len(commits_list)):
            for j in range(i + 1, len(commits_list)):
                graph["edges"].add((commits_list[i], commits_list[j]))

    return graph
