import os

def execute(vfs, current_dir, path=""):
    try:
        # Приводим текущую директорию и путь к единому формату
        if current_dir == "/":
            current_dir = ""  # В корне пути не должно быть начального слэша

        # Обработка пути
        if path and path != "/":
            # Если путь передан, создаем новый путь
            current_dir = os.path.normpath(os.path.join(current_dir.strip("/"), path.strip("/")))

        # Убедимся, что текущая директория завершается "/"
        if not current_dir.endswith("/") and current_dir:
            current_dir += "/"

        # Получаем содержимое архива
        contents = vfs.namelist()
        items = set()

        for file in contents:
            # Фильтруем содержимое по текущему пути
            if current_dir == "":  # Обработка корневой директории
                if "/" not in file.strip("/"):  # Если файл в корне архива
                    items.add(file)
                else:  # Директории
                    items.add(file.split("/")[0] + "/")
            elif file.startswith(current_dir):
                relative_path = file[len(current_dir):].strip("/")
                if "/" in relative_path:  # Если это директория
                    items.add(relative_path.split("/")[0] + "/")
                elif relative_path:  # Это файл
                    items.add(relative_path)

        # Если не найдено файлов в указанной директории
        if not items:
            return "Directory not found or Directory is empty."

        return "\n".join(sorted(items))

    except Exception as e:
        return f"Error: {e}"
