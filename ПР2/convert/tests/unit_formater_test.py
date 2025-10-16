import pytest
from datetime import datetime
import core.unit_formater as uf

def test_format_number_basic():
    assert uf.format_number(0) == "0"
    assert uf.format_number(3.14) == "3.14"
    assert uf.format_number(5.0) == "5"

def test_format_number_scientific():
    result = uf.format_number(1234567)
    assert "e" in result or result.isdigit()

def test_format_unit_name_plural():
    assert uf.format_unit_name("метр", 1) == "метр"
    assert uf.format_unit_name("метр", 2) == "метры"
    assert uf.format_unit_name("грамм", 5) == "граммы"

def test_format_temperature_symbols():
    from_sym, to_sym = uf.format_temperature(0, 'c', 'f')
    assert from_sym == '°C'
    assert to_sym == '°F'

def test_format_conversion_result_length():
    result = uf.format_conversion_result(100, "сантиметр", 1, "метр")
    assert "100 сантиметры = 1 метр" in result

def test_format_conversion_result_temperature():
    result = uf.format_conversion_result(0, "c", 32, "f")
    assert "0°C = 32°F" in result

def test_format_history_entry():
    entry = {
        'timestamp': '2024-01-15T14:30:00',
        'value': 100.0,
        'from_unit': 'сантиметр',
        'to_unit': 'метр',
        'result': 1.0
    }
    result = uf.format_history_entry(entry)
    assert "[15.01.2024 14:30]" in result
    assert "100 сантиметры = 1 метр" in result

def test_format_number_precision():
    assert uf.format_number(3.141592, precision=3) == "3.142"
    assert uf.format_number(3.141592, precision=5) == "3.14159"

def test_format_unit_name_unknown():
    assert uf.format_unit_name("литр", 2) == "литр"

def test_format_temperature_unknown():
    from_sym, to_sym = uf.format_temperature(100, 'rankine', 'unknown')
    assert from_sym == 'rankine'
    assert to_sym == 'unknown'
