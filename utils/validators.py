# utils/validators.py
from datetime import datetime
import functools


def log_operation(func):
    """Dekorator logujący operacje na wpisach."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Wywołano: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


def validate_date(date_str):
    """Waliduj datę w formacie YYYY-MM-DD."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_time(time_str):
    """Waliduj czas w formacie HH:MM."""
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False
