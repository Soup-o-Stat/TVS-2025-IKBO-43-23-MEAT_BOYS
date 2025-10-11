import time
import core.convert_script as conversions
import core.validator as validator
import core.unit_formater as unit_formater
import core.history as history

def startup():
    print(r"""
/$$$$$\   $$$$$$\  $$\   $$\ $$\    $$\ $$$$$$$$\ $$$$$$$\ $$$$$$$$\ $$$$$$$$\ $$$$$$$\  
$$  __$$\ $$  __$$\ $$$\  $$ |$$ |   $$ |$$  _____|$$  __$$\\__$$  __|$$  _____|$$  __$$\ 
$$ /  \__|$$ /  $$ |$$$$\ $$ |$$ |   $$ |$$ |      $$ |  $$ |  $$ |   $$ |      $$ |  $$ |
$$ |      $$ |  $$ |$$ $$\$$ |\$$\  $$  |$$$$$\    $$$$$$$  |  $$ |   $$$$$\    $$$$$$$  |
$$ |      $$ |  $$ |$$ \$$$$ | \$$\$$  / $$  __|   $$  __$$<   $$ |   $$  __|   $$  __$$< 
$$ |  $$\ $$ |  $$ |$$ |\$$$ |  \$$$  /  $$ |      $$ |  $$ |  $$ |   $$ |      $$ |  $$ |
\$$$$$$  | $$$$$$  |$$ | \$$ |   \$  /   $$$$$$$$\ $$ |  $$ |  $$ |   $$$$$$$$\ $$ |  $$ |
 \______/  \______/ \__|  \__|    \_/    \________|\__|  \__|  \__|   \________|\__|  \__|
    """)
    time.sleep(1)
    while True:
        menu()

#Главное меню
def menu():
    print()
    print("Что вы хотите сделать?")
    print("1. Конвертировать")
    print("2. Посмотреть историю")
    print("0. Выйти")

    try:
        choice = int(input(">> "))
        if choice == 1:
            convert_menu()
        elif choice == 2:
            history_menu()
        elif choice == 0:
            exit()
        else:
            print("Неверный ввод!")
    except ValueError:
        print("Введите число!")

#Меню истории
def history_menu():
    while True:
        print("\nИстория конвертаций:")
        print("1. Последние 5 конвертаций")
        print("2. Вся история")
        print("3. Статистика")
        print("4. Очистить историю")
        print("0. Назад")
        choice = input(">> ")
        if choice == "1":
            show_recent_history()
        elif choice == "2":
            show_full_history()
        elif choice == "3":
            show_statistics()
        elif choice == "4":
            history.clear_history()
            print("История очищена.")
        elif choice == "0":
            return
        else:
            print("Неверный ввод!")

def show_recent_history():
    data = history.get_recent_conversions(5)
    if not data:
        print("История пуста.")
        return
    print("\nПоследние 5 конвертаций:")
    for entry in data:
        print(
            f"[{entry['timestamp']}] {entry['category']}: {entry['value']} {entry['from_unit']} → {entry['result']} {entry['to_unit']}")

def show_full_history():
    data = history.load_history()
    if not data:
        print("История пуста.")
        return
    print("\nВся история:")
    for entry in data:
        print(
            f"[{entry['timestamp']}] {entry['category']}: {entry['value']} {entry['from_unit']} → {entry['result']} {entry['to_unit']}")

def show_statistics():
    stats = history.get_statistics()
    if stats["total"] == 0:
        print("История пуста.")
        return
    print("\nСтатистика:")
    print(f"Всего конвертаций: {stats['total']}")
    print("По категориям:")
    for cat, count in stats["by_category"].items():
        print(f" - {cat}: {count}")
    print(f"Первая: {stats['first_conversion']}")
    print(f"Последняя: {stats['last_conversion']}")

#Меню выбора типа конвертации
def convert_menu():
    print()
    print("Что вы хотите конвертировать?")
    print("1. Длина")
    print("2. Температура")
    print("3. Масса")
    print("0. Назад")

    choice = input(">> ")
    if choice == "1":
        convert_linear_menu("длина")
    elif choice == "2":
        convert_temperature_menu()
    elif choice == "3":
        convert_linear_menu("масса")
    elif choice == "0":
        return
    else:
        print("Неверный ввод!")

#Конвертации длины/массы
def convert_linear_menu(category):
    print("\nДоступные единицы:")
    for unit in conversions.UNITS[category]:
        print(" -", unit)

    try:
        value_str = input("\nВведите значение: ")
        value = validator.validate_numeric_input(value_str)
        value = validator.validate_positive_number(value)

        from_unit = input("Из (например, метр): ").strip().lower()
        to_unit = input("В (например, километр): ").strip().lower()

        validator.validate_unit_exists(category, from_unit)
        validator.validate_unit_exists(category, to_unit)

        result = conversions.convert_linear(category, value, from_unit, to_unit)
        formated_result = unit_formater.format_conversion_result(value, from_unit, result, to_unit)
        print(f"\n{formated_result}\n")

        history.add_conversion(category, value, from_unit, to_unit, result)

    except Exception as e:
        print("Ошибка:", e)

#Конвертации температур
def convert_temperature_menu():
    print("""
1. Цельсий --> Фаренгейт
2. Фаренгейт --> Цельсий
3. Цельсий --> Кельвин
4. Кельвин --> Цельсий
5. Фаренгейт --> Кельвин
6. Кельвин --> Фаренгейт
0. Назад
""")
    try:
        str_choice = input(">> ")
        choice = validator.validate_numeric_input(str_choice)

        if choice == 0:
            return

        str_value = input("Введите значение: ")
        value = validator.validate_numeric_input(str_value)

        conversions_map = {
            1: ("цельсий", "фаренгейт", conversions.c_to_f),
            2: ("фаренгейт", "цельсий", conversions.f_to_c),
            3: ("цельсий", "кельвин", conversions.c_to_k),
            4: ("кельвин", "цельсий", conversions.k_to_c),
            5: ("фаренгейт", "кельвин", conversions.f_to_k),
            6: ("кельвин", "фаренгейт", conversions.k_to_f)
        }

        if choice not in conversions_map:
            print("Неверный выбор!")
            return

        from_unit, to_unit, func = conversions_map[choice]
        value = validator.validate_temperature_range(value, from_unit[0])
        result = func(value)

        formated_result = unit_formater.format_conversion_result(value, from_unit, result, to_unit)
        print(f"\n{formated_result}\n")

        history.add_conversion("температура", value, from_unit, to_unit, result)

    except ValueError:
        print("Ошибка: введите число!")

if __name__ == "__main__":
    startup()
