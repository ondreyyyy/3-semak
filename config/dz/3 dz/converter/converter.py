import json
import re
import sys
import io

# Переопределим стандартный ввод и вывод для использования UTF-8
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Функция для преобразования JSON в ваш конфигурационный язык
def parse_json_to_custom_language(data):
    result = []

    def process_value(value):
        if isinstance(value, int) or isinstance(value, float):
            return value
        elif isinstance(value, str):
            return value
        elif isinstance(value, list):
            return "{ " + ", ".join(map(str, (process_value(v) for v in value))) + " }"
        elif isinstance(value, dict):
            if "expr" in value:
                return process_expression(value["expr"])  # Обрабатываем выражение в словаре
            else:
                raise ValueError(f"Неподдерживаемый тип значения: {type(value)}")
        else:
            raise ValueError(f"Неподдерживаемый тип значения: {type(value)}")

    def process_expression(expr):
        """Обрабатывает константные выражения в префиксной форме."""
        if not expr or not isinstance(expr, list) or len(expr) < 2:
            raise ValueError(f"Некорректное константное выражение: {expr}")

        operator = expr[0]
        args = [process_value(arg) for arg in expr[1:]]

        if operator == "+":
            if not all(isinstance(arg, (int, float)) for arg in args):
                raise ValueError("Сложение требует числовые аргументы.")
            return sum(args)
        elif operator == "-":
            if len(args) != 2 or not all(isinstance(arg, (int, float)) for arg in args):
                raise ValueError("Вычитание требует ровно два числовых аргумента.")
            return args[0] - args[1]
        elif operator == "concat":
            if not all(isinstance(arg, str) for arg in args):
                raise ValueError("Конкатенация требует строковые аргументы.")
            return "".join(args)
        else:
            raise ValueError(f"Неподдерживаемая операция: {operator}")

    for key, value in data.items():
        if key.startswith("//"):
            # Однострочный комментарий
            result.append(f"// {value}")
        elif key == "/*":
            # Многострочный комментарий
            if not isinstance(value, list):
                raise ValueError("Многострочный комментарий должен быть списком строк.")
            result.append("(*")
            result.extend(value)
            result.append("*)")
        elif re.match(r"^[a-z][a-z0-9_]*$", key):
            # Имена и константы
            if isinstance(value, (int, float, list)):
                result.append(f"{key} is {process_value(value)}")
            elif isinstance(value, dict) and "expr" in value:
                # Константное выражение
                result.append(f"{key} is {process_expression(value['expr'])}")
            elif isinstance(value, str):
                # Строка, которая не является выражением
                result.append(f"{key} is {process_value(value)}")
            else:
                raise ValueError(f"Некорректное значение для ключа {key}.")
        else:
            raise ValueError(f"Некорректное имя ключа: {key}")

    return "\n".join(result)

# Основная функция для запуска
def main():
    try:
        # Считываем JSON с stdin
        input_data = sys.stdin.read()
        json_data = json.loads(input_data)

        # Преобразуем в конфигурационный язык
        output = parse_json_to_custom_language(json_data)

        # Выводим результат
        print(output)
    except json.JSONDecodeError as e:
        print(f"Ошибка: Некорректный ввод JSON - {e}", file=sys.stderr)
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
