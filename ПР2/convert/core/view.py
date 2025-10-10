import time
import core.convert_script as conversions

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
        value = float(input("\nВведите значение: "))
        from_unit = input("Из (например, метр): ").strip().lower()
        to_unit = input("В (например, километр): ").strip().lower()

        result = conversions.convert_linear(category, value, from_unit, to_unit)
        print(f"\n{value} {from_unit} = {result} {to_unit}\n")
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
    choice = input(">> ")
    if choice == "0":
        return

    try:
        value = float(input("Введите значение: "))

        if choice == "1":
            print(value, "°C =", conversions.c_to_f(value), "°F")
        elif choice == "2":
            print(value, "°F =", conversions.f_to_c(value), "°C")
        elif choice == "3":
            print(value, "°C =", conversions.c_to_k(value), "K")
        elif choice == "4":
            print(value, "K =", conversions.k_to_c(value), "°C")
        elif choice == "5":
            print(value, "°F =", conversions.f_to_k(value), "K")
        elif choice == "6":
            print(value, "K =", conversions.k_to_f(value), "°F")
        else:
            print("Неверный выбор!")
    except ValueError:
        print("Ошибка: введите число!")
