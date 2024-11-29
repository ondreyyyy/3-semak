import os

def execute(vfs, current_dir, path):
    # Если путь пустой, выводим текущую директорию
    if not path.strip():
        return current_dir

    # Если путь абсолютный ("/"), переходим в корень
    if path.strip() == "/":
        return "/"

    # Приводим путь к единому формату
    if current_dir == "/":
        current_dir = ""  # Для корректного объединения

    # Новый путь
    if path.startswith("/"):
        new_path = os.path.normpath(path.strip("/")) + "/"
    else:
        new_path = os.path.normpath(os.path.join(current_dir.strip("/"), path.strip("/"))) + "/"

    # Проверяем, существует ли директория в VFS
    normalized_vfs_namelist = [os.path.normpath(file) for file in vfs.namelist()]
    if any(file.startswith(new_path.rstrip("/")) or new_path.rstrip("/") in file for file in normalized_vfs_namelist):
        return new_path

    # Если директория не найдена
    raise FileNotFoundError(f"Directory '{path}' not found.")
