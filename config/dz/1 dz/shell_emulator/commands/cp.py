import os
import zipfile

def execute(vfs, current_dir, src, dst):
    # Нормализация текущей директории и путей
    if current_dir == "/":
        src_path = src.strip("/")
        dst_path = dst.strip("/")
    else:
        src_path = os.path.normpath(os.path.join(current_dir.strip("/"), src.strip("/")))
        dst_path = os.path.normpath(os.path.join(current_dir.strip("/"), dst.strip("/")))

    src_path = src_path.replace("\\", "/")
    dst_path = dst_path.replace("\\", "/")

    # Если путь для dst начинается с "/", то это абсолютный путь
    if dst.startswith("/"):
        dst_path = dst.strip("/")

    # Проверка существования исходного файла
    if src_path not in vfs.namelist():
        return f"Source file '{src}' not found. path = '{src_path}'"

    # Читаем содержимое исходного файла
    try:
        content = vfs.read(src_path)
    except KeyError:
        return f"Source file '{src}' not found."

    # Запись содержимого в архив
    try:
        with zipfile.ZipFile(vfs.filename, "a") as archive:
            archive.writestr(dst_path, content)
    except Exception as e:
        return f"Error copying file: {e}"

    return f"Copied '{src}' to '{dst}'."
