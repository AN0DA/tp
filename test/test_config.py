import pytest
import os
from tp.config import (
    get_printer_ip,
    set_printer_ip,
    get_chars_per_line,
    set_chars_per_line,
    get_enable_special_letters,
    set_enable_special_letters,
    CONFIG_FILE,
)

def setup_module(module):
    # Backup the original config file if it exists
    if os.path.exists(CONFIG_FILE):
        os.rename(CONFIG_FILE, CONFIG_FILE + ".bak")

def teardown_module(module):
    # Remove the config file after tests
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
    # Restore the original config file
    if os.path.exists(CONFIG_FILE + ".bak"):
        os.rename(CONFIG_FILE + ".bak", CONFIG_FILE)

def test_set_and_get_printer_ip():
    set_printer_ip("192.168.1.100")
    assert get_printer_ip() == "192.168.1.100"

def test_set_and_get_chars_per_line():
    set_chars_per_line(42)
    assert get_chars_per_line() == 42

def test_set_and_get_enable_special_letters():
    set_enable_special_letters(False)
    assert get_enable_special_letters() is False
    set_enable_special_letters(True)
    assert get_enable_special_letters() is True

def test_default_values():
    # Remove settings to test defaults
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
    assert get_chars_per_line() == 32  # Default chars per line
    assert get_enable_special_letters() is True  # Default special letters enabled
