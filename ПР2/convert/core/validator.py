# Функция проверки является ли числом
def validate_numeric_input(value_str):
    try:
        return float(value_str)
    except ValueError:
        raise ValueError("Ошибка: введите корректное число")

# Функция проверки что число положительное
def validate_positive_number(value):
    if value < 0:
        raise ValueError("Ошибка: значение должно быть положительным")
    return value

# Функция проверки допустимости температуры
def validate_temperature_range(value, scale):
    ranges = {
        'c': (-273.15, 10000),
        'f': (-459.67, 18032),
        'k': (0, 10273.15)
    }
    min_temp, max_temp = ranges.get(scale, (-float('inf'), float('inf')))
    if not min_temp <= value <= max_temp:
        raise ValueError(f"Температура должна быть в диапазоне {min_temp} - {max_temp}")
    return value

# Функция проверки существования единицы измерения
def validate_unit_exists(category, unit):
    from core.convert_script import UNITS
    if category not in UNITS:
        raise ValueError(f"Категория '{category}' не найдена")
    if unit not in UNITS[category]:
        raise ValueError(f"Единица '{unit}' не найдена в категории '{category}'")
    return True

# Функция проверки существования категории
def validate_category(category):
    from core.convert_script import UNITS
    if category not in UNITS:
        raise ValueError(f"Категория '{category}' не найдена")
    return True