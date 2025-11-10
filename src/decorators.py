"""
Модуль для работы с декораторами.
"""
import functools


def log(filename=None):
    """
    Декоратор для логирования работы функций.

    Args:
        filename: Имя файла для записи логов. Если None, логи выводятся в консоль.

    Returns:
        Декорированную функцию
    """
    def decorator(func):
        @functools.wraps(func)  # Здесь используется functools!
        def wrapper(*args, **kwargs):
            # Формируем сообщение о вызове функции
            func_name = func.__name__

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Формируем сообщение об успехе
                log_message = f"{func_name} ok\n"

                # Записываем в файл или выводим в консоль
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_message)
                else:
                    print(log_message, end='')

                return result

            except Exception as e:
                # Формируем сообщение об ошибке
                error_message = f"{func_name} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"

                # Записываем в файл или выводим в консоль
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(error_message)
                else:
                    print(error_message, end='')

                # Пробрасываем исключение дальше
                raise

        return wrapper
    return decorator
