import os

def execute(vfs, current_dir, path):
    if not path:
        return "Usage: tac <file_path>"

    # Убираем начальные и конечные слэши у текущей директории и пути
    normalized_dir = current_dir.strip("/")
    normalized_path = path.strip("/")

    # Формируем полный путь относительно текущей директории
    if normalized_dir:
        full_path = f"{normalized_dir}/{normalized_path}"
    else:
        full_path = normalized_path

    # Нормализуем путь для проверки внутри архива
    full_path = os.path.normpath(full_path).replace("\\", "/")

    # Проверяем наличие файла в архиве
    if full_path not in vfs.namelist():
        return f"File '{path}' not found in '{current_dir}'."

    # Читаем содержимое файла и переворачиваем строки
    try:
        content = vfs.read(full_path).decode('utf-8')
        return "\n".join(reversed(content.splitlines()))
    except Exception as e:
        return f"Error reading file '{path}': {e}"
