import datetime

# Функция форматирования числа с заданной точностью
def format_number(value, precision=6):
    if value == 0:
        return "0"
    
    if abs(value) >= 1e6 or (abs(value) <= 1e-4 and value != 0):
        return f"{value:.{precision-1}e}"
    
    formatted = f"{value:.{precision}f}"
    if '.' in formatted:
        formatted = formatted.rstrip('0').rstrip('.')
    
    return formatted

# Функция форматирования названия единиц измерения
def format_unit_name(unit, value):
    if value == 1:
        return unit
    
    plural_rules = {
        'метр': 'метры',
        'километр': 'километры',
        'сантиметр': 'сантиметры',
        'грамм': 'граммы',
        'килограмм': 'килограммы',
        'тонна': 'тонны'
    }
    
    return plural_rules.get(unit, unit)

# Функция специального форматирования для температур
def format_temperature(value, from_unit, to_unit):
    symbols = {
        'c': '°C',
        'f': '°F', 
        'k': 'K',
        'цельсий': '°C',
        'фаренгейт': '°F',
        'кельвин': 'K'
    }
    
    from_symbol = symbols.get(from_unit.lower(), from_unit)
    to_symbol = symbols.get(to_unit.lower(), to_unit)
    
    return from_symbol, to_symbol

# Функция форматирования полного результата конвертации
def format_conversion_result(value, from_unit, result, to_unit):
    formatted_value = format_number(value)
    formatted_result = format_number(result)
    
    if any(unit in ['c', 'f', 'k', 'цельсий', 'фаренгейт', 'кельвин'] 
           for unit in [from_unit, to_unit]):
        from_sym, to_sym = format_temperature(value, from_unit, to_unit)
        return f"{formatted_value}{from_sym} = {formatted_result}{to_sym}"
    
    from_name = format_unit_name(from_unit, value)
    to_name = format_unit_name(to_unit, result)
    
    return f"{formatted_value} {from_name} = {formatted_result} {to_name}"

# Функция форматирования записи истории для красивого вывода
def format_history_entry(entry):
    timestamp = datetime.datetime.fromisoformat(entry['timestamp'])
    date_str = timestamp.strftime("%d.%m.%Y %H:%M")
    result_str = format_conversion_result(
        entry['value'],
        entry['from_unit'],
        entry['result'],
        entry['to_unit']
    )
    return f"[{date_str}] {result_str}"