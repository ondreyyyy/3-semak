import os
import sys
import json
import zipfile
import tkinter as tk
from tkinter import scrolledtext
from commands import ls_execute, cd_execute, exit_shell, uptime_execute, cp_execute, tac_execute


class ShellEmulator:
    def __init__(self, config):
        self.username = config["username"]
        self.vfs_path = config["vfs_path"]
        self.current_dir = "/"
        self.vfs = None

        self.load_vfs()

        self.root = tk.Tk()
        self.root.title("Shell Emulator")
        self.root.geometry("800x600")

        self.output = scrolledtext.ScrolledText(self.root, state='disabled', wrap=tk.WORD)
        self.output.pack(fill=tk.BOTH, expand=True)

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(fill=tk.X)

        self.prompt = tk.Label(self.input_frame, text=f"{self.username}@shell:~$ ")
        self.prompt.pack(side=tk.LEFT)

        self.input_field = tk.Entry(self.input_frame)
        self.input_field.pack(fill=tk.X, side=tk.LEFT, expand=True)
        self.input_field.bind("<Return>", self.handle_input)

        self.show_output("Shell started. Type 'exit' to quit.")

    def load_vfs(self):
        if self.vfs:
            self.vfs.close()
        self.vfs = zipfile.ZipFile(self.vfs_path)

    def handle_input(self, event=None):
        command = self.input_field.get().strip()
        self.input_field.delete(0, tk.END)
        self.show_output(f"{self.username}@shell:~$ {command}")

        try:
            if command == "exit":
                self.exit_shell()
            elif command.startswith("ls"):
                # Обрабатываем команду ls с аргументом или без
                args = command.split(" ", 1)
                if len(args) > 1:
                    # Если аргумент указан, передаем путь в ls_execute
                    self.show_output(ls_execute(self.vfs, self.current_dir, args[1]))
                else:
                    # Если аргумента нет, передаем текущую директорию
                    self.show_output(ls_execute(self.vfs, self.current_dir))
            elif command.startswith("cd"):
                if command.strip() == "cd":
                    self.show_output(self.current_dir)  # Печатаем текущую директорию
                else:
                    path = command.split(" ", 1)[1] if " " in command else "/"
                    self.current_dir = cd_execute(self.vfs, self.current_dir, path)
                    self.show_output(f"Changed directory to: {self.current_dir}")
            elif command == "uptime":
                self.show_output(uptime_execute())
            elif command.startswith("cp"):
                args = command.split(" ", 2)
                if len(args) < 3:
                    self.show_output("Usage: cp <source> <destination>")
                else:
                    # Формируем пути для src и dst
                    src = args[1]
                    dst = args[2]
                    result = cp_execute(self.vfs, self.current_dir, src, dst)
                    self.show_output(result)
                    self.load_vfs()  # Перезагрузка VFS для учёта изменений
            elif command.startswith("tac"):
                path = command.split(" ", 1)[1] if " " in command else ""
                if not path:
                    self.show_output("Usage: tac <file_path>")
                else:
                    self.show_output(tac_execute(self.vfs, self.current_dir, path))
        except Exception as e:
            self.show_output(f"Error: {e}")

    def show_output(self, message):
        self.output.config(state='normal')
        self.output.insert(tk.END, message + "\n")
        self.output.config(state='disabled')

    def exit_shell(self):
        self.vfs.close()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


def main():
    if len(sys.argv) != 2:
        print("Usage: python emulator.py <config.json>")
        sys.exit(1)

    with open(sys.argv[1], "r") as config_file:
        config = json.load(config_file)

    emulator = ShellEmulator(config)
    emulator.run()


if __name__ == "__main__":
    main()
