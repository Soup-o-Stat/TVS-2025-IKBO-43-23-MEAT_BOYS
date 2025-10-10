UNITS = {
    "длина": {
        "миллиметр": 10 ** -3,   # 0.001 метра
        "сантиметр": 10 ** -2,   # 0.01 метра
        "дециметр": 10 ** -1,    # 0.1 метра
        "метр": 1,               # базовая единица
        "километр": 10 ** 3      # 1000 метров
    },
    "масса": {
        "грамм": 1,              # базовая единица
        "килограмм": 10 ** 3,    # 1000 грамм
        "центнер": 10 ** 5,      # 100 000 грамм
        "тонна": 10 ** 6         # 1 000 000 грамм
    }
}

def c_to_f(c):
    return c * 9.0 / 5.0 + 32.0

def f_to_c(f):
    return (f - 32.0) * 5.0 / 9.0

def c_to_k(c):
    return c + 273.15

def k_to_c(k):
    return k - 273.15

def f_to_k(f):
    return (f - 32.0) * 5.0 / 9.0 + 273.15

def k_to_f(k):
    return (k - 273.15) * 9.0 / 5.0 + 32.0

def convert_linear(category, value, from_unit, to_unit):
    if category not in UNITS:
        raise ValueError("Неизвестная категория конверсии: " + str(category))

    units = UNITS[category]
    if from_unit not in units:
        raise ValueError("Неизвестная единица: " + from_unit)
    if to_unit not in units:
        raise ValueError("Неизвестная единица: " + to_unit)
    base_value = value * units[from_unit]
    result = base_value / units[to_unit]
    return result
