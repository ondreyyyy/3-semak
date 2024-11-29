## Запуск эмулятора

cd 'путь до shell_emulator'

python emulator.py config.json

![image](https://github.com/user-attachments/assets/c8a36004-d49f-4209-9b79-8dff9644e933)

![image](https://github.com/user-attachments/assets/2f9a3ae7-37ef-42b5-abac-38521ea00f3b)

## Запуск всех тестов

cd 'путь до shell_emulator'

python -m unittest discover -s tests

![image](https://github.com/user-attachments/assets/109522c9-88b8-479c-84fc-529620fe1273)

## Запуск отдельных команд

На примере комманды ls

cd 'путь до shell_emulator'

python -m unittest tests.test_ls

![image](https://github.com/user-attachments/assets/0dcc7b06-ba85-4672-829c-02d98f0e552a)
