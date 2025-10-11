import time
import core.convert_script as conversions
import core.validator as validator
import core.unit_formater as unit_formater
import core.history as history

# Функция запуска
def startup():
    print("""
$$$$$$\   $$$$$$\  $$\   $$\ $$\    $$\ $$$$$$$$\ $$$$$$$\ $$$$$$$$\ $$$$$$$$\ $$$$$$$\  
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

# Функция вывода меню
def menu():
    print()
    print("Что вы хотите сделать?")
    print("1. Конвертировать")
    print("0. Выйти")
    try:
        choice = int(input(">> "))
        if choice == 1:
            convert_menu()
        elif choice == 0:
            exit()
        else:
            print("Неверный ввод!")
    except ValueError:
        print("Введите число!")

# Функция вывода меню конвертаций
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

# Функция вывода линейных конвертаций
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

    except Exception as e:
        print("Ошибка:", e)

# Функция вывода меню конвертаций температур
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

        if choice == 1:
            from_unit = "c"
            value = validator.validate_temperature_range(value, from_unit)
            to_unit = "f"
            result = conversions.c_to_f(value)
            formated_result = unit_formater.format_conversion_result(value, from_unit, result, to_unit)
            print(f"\n{formated_result}\n")
        elif choice == 2:
            from_unit = "f"
            value = validator.validate_temperature_range(value, from_unit)
            to_unit = "c"
            result = conversions.f_to_c(value)
            formated_result = unit_formater.format_conversion_result(value, from_unit, result, to_unit)
            print(f"\n{formated_result}\n")
        elif choice == 3:
            from_unit = "c"
            value = validator.validate_temperature_range(value, from_unit)
            to_unit = "k"
            result = conversions.c_to_k(value)
            formated_result = unit_formater.format_conversion_result(value, from_unit, result, to_unit)
            print(f"\n{formated_result}\n")
        elif choice == 4:
            from_unit = "k"
            value = validator.validate_temperature_range(value, from_unit)
            to_unit = "c"
            result = conversions.k_to_c(value)
            formated_result = unit_formater.format_conversion_result(value, from_unit, result, to_unit)
            print(f"\n{formated_result}\n")
        elif choice == 5:
            from_unit = "f"
            value = validator.validate_temperature_range(value, from_unit)
            to_unit = "k"
            result = conversions.f_to_k(value)
            formated_result = unit_formater.format_conversion_result(value, from_unit, result, to_unit)
            print(f"\n{formated_result}\n")
        elif choice == 6:
            from_unit = "k"
            value = validator.validate_temperature_range(value, from_unit)
            to_unit = "f"
            result = conversions.k_to_f(value)
            formated_result = unit_formater.format_conversion_result(value, from_unit, result, to_unit)
            print(f"\n{formated_result}\n")
        else:
            print("Неверный выбор!")
    except ValueError:
        print("Ошибка: введите число!")
