import pytest
import sys
import os
import core.validator as val

def test_validate_numeric_input_valid():
    assert val.validate_numeric_input("42") == 42.0
    assert val.validate_numeric_input("3.14") == 3.14
    assert val.validate_numeric_input("-10") == -10.0
    
def test_validate_numeric_input_invalid():
    with pytest.raises(ValueError, match="Ошибка: введите корректное число"):
        val.validate_numeric_input("abc")
    
def test_validate_positive_number_valid():
    assert val.validate_positive_number(5) == 5
    assert val.validate_positive_number(0) == 0
    assert val.validate_positive_number(0.001) == 0.001
    
def test_validate_positive_number_invalid():
    with pytest.raises(ValueError, match="Ошибка: значение должно быть положительным"):
        val.validate_positive_number(-5)
    
def test_validate_temperature_range_valid():
    assert val.validate_temperature_range(0, 'c') == 0
    assert val.validate_temperature_range(-273.15, 'c') == -273.15
    assert val.validate_temperature_range(32, 'f') == 32
    assert val.validate_temperature_range(273.15, 'k') == 273.15
    
def test_validate_temperature_range_invalid():
    with pytest.raises(ValueError):
        val.validate_temperature_range(-274, 'c')
    with pytest.raises(ValueError):
        val.validate_temperature_range(-1, 'k')
    
def test_validate_unit_exists_valid():
    assert val.validate_unit_exists("длина", "метр") == True
    assert val.validate_unit_exists("масса", "грамм") == True
    
def test_validate_unit_exists_invalid():
    with pytest.raises(ValueError):
        val.validate_unit_exists("длина", "фут")
    with pytest.raises(ValueError):
        val.validate_unit_exists("объем", "литр")
    
def test_validate_category_valid():
    assert val.validate_category("длина") == True
    assert val.validate_category("масса") == True
    
def test_validate_category_invalid():
    with pytest.raises(ValueError):
        val.validate_category("объем")