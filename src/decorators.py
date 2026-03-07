"""
Модуль для работы с декораторами.
"""
import functools
from typing import Callable, Any, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования работы функций.

    Args:
        filename: Имя файла для записи логов. Если None, логи выводятся в консоль.

    Returns:
        Декорированную функцию
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            func_name = func.__name__

            try:
                result = func(*args, **kwargs)
                log_message = f"{func_name} ok\n"

                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_message)
                else:
                    print(log_message, end='')

                return result

            except Exception as e:
                log_message = f"{func_name} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"

                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_message)
                else:
                    print(log_message, end='')

                raise

        return wrapper
    return decorator
