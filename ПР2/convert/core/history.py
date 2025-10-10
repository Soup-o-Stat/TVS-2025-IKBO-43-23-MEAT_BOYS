import json
import datetime
from pathlib import Path

class ConversionHistory:
    # Конструктор класса
    def __init__(self, filename="conversion_history.json"):
        self.filename = Path(filename)
        self.history = self._load_history()
    
    # Метод зарузки истории из файла
    def _load_history(self):
        if self.filename.exists():
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    # Метод загрузки истории в файл
    def _save_history(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    # Метод добавления конвертации в историю
    def add_conversion(self, category, value, from_unit, to_unit, result):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "category": category,
            "value": value,
            "from_unit": from_unit,
            "to_unit": to_unit,
            "result": result
        }
        self.history.append(entry)
        self._save_history()
    
    # Метод получения списка последних конвертаций
    def get_recent_conversions(self, count=5):
        return self.history[-count:]
    
    # Метод очистки истории
    def clear_history(self):
        self.history = []
        self._save_history()
    
    # Метод получение списка конвертаций по категоории
    def get_conversions_by_category(self, category):
        return [entry for entry in self.history if entry["category"] == category]
    
    # Метод получения статистики конвертаций по категориям
    def get_statistics(self):
        if not self.history:
            return {"total": 0}
        
        categories = {}
        for entry in self.history:
            cat = entry["category"]
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "total": len(self.history),
            "by_category": categories,
            "first_conversion": self.history[0]["timestamp"],
            "last_conversion": self.history[-1]["timestamp"]
        }