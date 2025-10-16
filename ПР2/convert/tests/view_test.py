import pytest
import sys
import os
import core.view as view
from unittest.mock import patch, MagicMock

@patch('builtins.input')
@patch('builtins.print')
def test_menu_navigation(self, mock_print, mock_input):
    mock_input.return_value = '1'
    with patch('core.view.convert_menu') as mock_convert:
        view.menu()
        mock_convert.assert_called_once()
    
@patch('builtins.input')
@patch('builtins.print')
def test_menu_invalid_input(self, mock_print, mock_input):
    mock_input.return_value = 'abc'
    view.menu()
    mock_print.assert_any_call("Введите число!")
    
@patch('builtins.input')
@patch('builtins.print')
def test_convert_menu_linear(self, mock_print, mock_input):
    mock_input.return_value = '1'
    with patch('core.view.convert_linear_menu') as mock_linear:
        view.convert_menu()
        mock_linear.assert_called_with('длина')
    
@patch('builtins.input')
@patch('builtins.print')
def test_convert_linear_menu_success(self, mock_print, mock_input):
    mock_input.side_effect = ['100', 'сантиметр', 'метр']
        
    with patch('core.validator.validate_numeric_input') as mock_val_num, \
        patch('core.validator.validate_positive_number') as mock_val_pos, \
        patch('core.validator.validate_unit_exists') as mock_val_unit, \
        patch('core.conversions.convert_linear') as mock_convert, \
        patch('core.unit_formater.format_conversion_result') as mock_format, \
        patch('core.history.add_conversion') as mock_history:
            
        mock_val_num.return_value = 100.0
        mock_val_pos.return_value = 100.0
        mock_convert.return_value = 1.0
        mock_format.return_value = "100 см = 1 м"
            
        view.convert_linear_menu('длина')
            
        mock_convert.assert_called_once()
        mock_history.assert_called_once()
        mock_print.assert_any_call("\n100 см = 1 м\n")
    
@patch('builtins.input')
@patch('builtins.print')
def test_convert_temperature_menu_success(self, mock_print, mock_input):
    mock_input.side_effect = ['1', '0']
        
    with patch('core.validator.validate_numeric_input') as mock_val_num, \
        patch('core.conversions.c_to_f') as mock_convert, \
        patch('core.unit_formater.format_conversion_result') as mock_format, \
        patch('core.history.add_conversion') as mock_history:
            
        mock_val_num.side_effect = [1.0, 0.0]
        mock_convert.return_value = 32.0
        mock_format.return_value = "0°C = 32°F"
            
        view.convert_temperature_menu()
            
        mock_convert.assert_called_once_with(0.0)
        mock_history.assert_called_once()
    
@patch('core.history.get_recent_conversions')
@patch('builtins.print')
def test_show_recent_history(self, mock_print, mock_get_recent):
    mock_get_recent.return_value = [{
        'timestamp': '2024-01-15T10:00:00',
        'category': 'длина',
        'value': 100.0,
        'from_unit': 'см',
        'to_unit': 'м',
        'result': 1.0
    }]
        
    view.show_recent_history()
    mock_print.assert_any_call("\nПоследние 5 конвертаций:")
    
@patch('core.history.get_statistics')
@patch('builtins.print')
def test_show_statistics(self, mock_print, mock_get_stats):
    mock_get_stats.return_value = {
        'total': 5,
        'by_category': {'длина': 3, 'масса': 2},
        'first_conversion': '2024-01-15T10:00:00',
        'last_conversion': '2024-01-15T11:00:00'
    }
        
    view.show_statistics()
    mock_print.assert_any_call("Всего конвертаций: 5")
    
@patch('builtins.input')
@patch('builtins.print')
def test_history_menu_clear(self, mock_print, mock_input):
    mock_input.side_effect = ['4', '0']
        
    with patch('core.history.clear_history') as mock_clear:
        view.history_menu()
        mock_clear.assert_called_once()
        mock_print.assert_any_call("История очищена.")
    
@patch('builtins.input')
@patch('builtins.print')
def test_convert_linear_menu_validation_error(self, mock_print, mock_input):
    mock_input.side_effect = ['invalid', 'см', 'м']
        
    with patch('core.validator.validate_numeric_input') as mock_val_num:
        mock_val_num.side_effect = ValueError("Ошибка числа")
            
        view.convert_linear_menu('длина')
        mock_print.assert_any_call("Ошибка:", "Ошибка числа")
    
@patch('builtins.input')
@patch('builtins.print')
def test_convert_temperature_invalid_choice(self, mock_print, mock_input):
    mock_input.side_effect = ['7', '0']
        
    with patch('core.validator.validate_numeric_input') as mock_val_num:
        mock_val_num.return_value = 7.0
            
        view.convert_temperature_menu()
        mock_print.assert_any_call("Неверный выбор!")