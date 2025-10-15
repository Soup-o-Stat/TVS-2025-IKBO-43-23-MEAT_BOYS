import pytest
from convert.core import convert_script as conv

class TestConvertScript:
    
    def test_c_to_f_basic(self):
        assert conv.c_to_f(0) == 32.0
        assert conv.c_to_f(100) == 212.0
    
    def test_f_to_c_basic(self):
        assert conv.f_to_c(32) == 0.0
        assert conv.f_to_c(212) == 100.0
    
    def test_c_to_k_basic(self):
        assert conv.c_to_k(0) == 273.15
        assert conv.c_to_k(-273.15) == 0.0
    
    def test_k_to_c_basic(self):
        assert conv.k_to_c(273.15) == 0.0
        assert conv.k_to_c(0) == -273.15
    
    def test_convert_length_meter_to_km(self):
        result = conv.convert_linear("длина", 1000, "метр", "километр")
        assert result == 1.0
    
    def test_convert_mass_gram_to_kg(self):
        result = conv.convert_linear("масса", 1000, "грамм", "килограмм")
        assert result == 1.0
    
    def test_convert_unknown_category(self):
        with pytest.raises(ValueError):
            conv.convert_linear("объем", 100, "литр", "галлон")
    
    def test_convert_unknown_unit(self):
        with pytest.raises(ValueError):
            conv.convert_linear("длина", 100, "фут", "метр")
    
    def test_temperature_round_trip(self):
        original = 25.5
        converted = conv.f_to_c(conv.c_to_f(original))
        assert converted == pytest.approx(original, abs=1e-10)
    
    def test_linear_round_trip(self):
        original = 150
        converted = conv.convert_linear("длина", 
            conv.convert_linear("длина", original, "сантиметр", "метр"),
            "метр", "сантиметр")
        assert converted == pytest.approx(original, abs=1e-10)

if __name__ == "__main__":
    print(conv.c_to_f(0) == 32.0)