import pytest
import json
import tempfile
import os
import core.history as hm
from pathlib import Path
from unittest.mock import patch
import sys

@pytest.fixture(autouse=True)
def setup(self):
    self.original_filename = hm.FILENAME
    self.temp_file = tempfile.NamedTemporaryFile(delete=False)
    self.temp_file.close()
    hm.FILENAME = Path(self.temp_file.name)
    yield
    hm.FILENAME = self.original_filename
    if os.path.exists(self.temp_file.name):
        os.unlink(self.temp_file.name)
    
def test_load_history_empty(self):
    assert hm.load_history() == []
    
def test_save_and_load_history(self):
    test_data = [{"test": "data"}]
    hm.save_history(test_data)
    loaded_data = hm.load_history()
    assert loaded_data == test_data
    
def test_add_conversion(self):
    hm.add_conversion("длина", 100, "см", "м", 1.0)
    history = hm.load_history()
    assert len(history) == 1
    assert history[0]["category"] == "длина"
    assert history[0]["value"] == 100
    
def test_get_recent_conversions(self):
    for i in range(3):
        hm.add_conversion("длина", i, "м", "см", i*100)
    recent = hm.get_recent_conversions(2)
    assert len(recent) == 2
    assert recent[0]["value"] == 1
    assert recent[1]["value"] == 2
    
def test_clear_history(self):
    hm.add_conversion("масса", 1000, "г", "кг", 1.0)
    hm.clear_history()
    assert hm.load_history() == []
    
def test_get_conversions_by_category(self):
    hm.add_conversion("длина", 100, "см", "м", 1.0)
    hm.add_conversion("масса", 1000, "г", "кг", 1.0)
    hm.add_conversion("длина", 2, "м", "км", 0.002)
    length_conv = hm.get_conversions_by_category("длина")
    assert len(length_conv) == 2
    for conv in length_conv:
        assert conv["category"] == "длина"
    
def test_get_statistics_empty(self):
    stats = hm.get_statistics()
    assert stats == {"total": 0}
    
def test_get_statistics_with_data(self):
    hm.add_conversion("длина", 100, "см", "м", 1.0)
    hm.add_conversion("масса", 1000, "г", "кг", 1.0)
    hm.add_conversion("длина", 2, "м", "км", 0.002)
    stats = hm.get_statistics()
    assert stats["total"] == 3
    assert stats["by_category"]["длина"] == 2
    assert stats["by_category"]["масса"] == 1
    
def test_timestamp_format(self):
    hm.add_conversion("длина", 100, "см", "м", 1.0)
    history = hm.load_history()
    timestamp = history[0]["timestamp"]
    assert "T" in timestamp
    assert ":" in timestamp
    
def test_file_persistence(self):
    hm.add_conversion("длина", 150, "см", "м", 1.5)
    assert hm.FILENAME.exists()
    with open(hm.FILENAME, 'r') as f:
        data = json.load(f)
    assert len(data) == 1
    assert data[0]["value"] == 150