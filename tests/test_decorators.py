import pytest
import os
import tempfile
from src.decorators import log


class TestLogDecorator:
    """Тесты для декоратора log."""

    def test_log_to_console_success(self, capsys):
        """Тестируем логирование успешной операции в консоль."""

        @log()
        def add(a, b):
            return a + b

        result = add(2, 3)

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "add ok" in captured.out
        assert result == 5

    def test_log_to_console_error(self, capsys):
        """Тестируем логирование ошибки в консоль."""

        @log()
        def divide(a, b):
            return a / b

        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "divide error: ZeroDivisionError" in captured.out
        assert "Inputs: (10, 0), {}" in captured.out

    def test_log_to_file_success(self):
        """Тестируем логирование успешной операции в файл."""
        # Создаем временный файл
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            temp_filename = f.name

        try:
            @log(filename=temp_filename)
            def multiply(x, y):
                return x * y

            result = multiply(4, 5)

            # Проверяем запись в файл
            with open(temp_filename, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "multiply ok" in content
                assert result == 20
        finally:
            # Удаляем временный файл
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

    def test_log_to_file_error(self):
        """Тестируем логирование ошибки в файл."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            temp_filename = f.name

        try:
            @log(filename=temp_filename)
            def failing_function():
                raise ValueError("Test error")

            with pytest.raises(ValueError):
                failing_function()

            # Проверяем запись в файл
            with open(temp_filename, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "failing_function error: ValueError" in content
                assert "Inputs: (), {}" in content
        finally:
            # Удаляем временный файл
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

    def test_function_arguments_preserved(self):
        """Тестируем что декоратор сохраняет аргументы и возвращаемое значение."""

        @log()
        def greet(name, greeting="Hello"):
            return f"{greeting}, {name}!"

        result = greet("Alice", greeting="Hi")

        assert result == "Hi, Alice!"

    def test_function_name_preserved(self):
        """Тестируем что декоратор сохраняет имя функции."""

        @log()
        def test_function():
            pass

        assert test_function.__name__ == "test_function"
