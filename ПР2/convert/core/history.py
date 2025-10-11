import json
import datetime
from pathlib import Path

FILENAME = Path("conversion_history.json")

def load_history():
    #Загрузить историю из файла
    if FILENAME.exists():
        with open(FILENAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history):
    #Сохранить историю в файл
    with open(FILENAME, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def add_conversion(category, value, from_unit, to_unit, result):
    #Добавить запись о конвертации
    history = load_history()
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "category": category,
        "value": value,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "result": result
    }
    history.append(entry)
    save_history(history)

def get_recent_conversions(count=5):
    #Получить последние сколько-то конвертаций
    history = load_history()
    return history[-count:]

def clear_history():
    #Очистить всю историю
    save_history([])

def get_conversions_by_category(category):
    #Получить все конвертации по категории
    history = load_history()
    return [entry for entry in history if entry["category"] == category]

def get_statistics():
    #Получить статистику по истории
    history = load_history()
    if not history:
        return {"total": 0}

    categories = {}
    for entry in history:
        cat = entry["category"]
        categories[cat] = categories.get(cat, 0) + 1

    return {
        "total": len(history),
        "by_category": categories,
        "first_conversion": history[0]["timestamp"],
        "last_conversion": history[-1]["timestamp"]
    }