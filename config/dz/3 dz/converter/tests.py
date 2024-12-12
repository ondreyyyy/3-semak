import json
from converter import parse_json_to_custom_language


# Тест 1: Числовые значения и операции
def test_integer_and_float():
    input_data = """
    {
        "integer_example": 100,
        "float_example": 3.14
    }
    """
    expected_output = """integer_example is 100
float_example is 3.14"""

    json_data = json.loads(input_data)
    output = parse_json_to_custom_language(json_data)
    assert output == expected_output, f"Expected: {expected_output}, got: {output}"


# Тест 2: Строковые выражения и конкатенация
def test_string_concatenation():
    input_data = """
    {
        "string_example": "Hello",
        "concat_example": {
            "expr": ["concat", "Hello", " ", "World"]
        }
    }
    """
    expected_output = """string_example is Hello
concat_example is Hello World"""

    json_data = json.loads(input_data)
    output = parse_json_to_custom_language(json_data)
    assert output == expected_output, f"Expected: {expected_output}, got: {output}"


# Тест 3: Массивы и вложенные операции
def test_array_and_nested_operations():
    input_data = """
    {
        "array_example": [1, 2, 3, 4],
        "sum_array_example": {
            "expr": ["+", 1, {
                "expr": ["+", 2, 3]
            }]
        }
    }
    """
    expected_output = """array_example is { 1, 2, 3, 4 }
sum_array_example is 6"""

    json_data = json.loads(input_data)
    output = parse_json_to_custom_language(json_data)
    assert output == expected_output, f"Expected: {expected_output}, got: {output}"


# Функция для запуска всех тестов
def run_tests():
    test_integer_and_float()
    test_string_concatenation()
    test_array_and_nested_operations()
    print("Все тесты пройдены успешно!")


# Запуск тестов
if __name__ == "__main__":
    run_tests()
