import pytest
from unittest.mock import MagicMock, patch
from tp.printer import ThermalPrinter

def test_printer_initialization():
    ip_address = "192.168.1.100"
    with patch('tp.printer.Network') as MockNetwork:
        printer = ThermalPrinter(ip_address)
        MockNetwork.assert_called_with(ip_address, timeout=5)  # Adjust timeout value if necessary

def test_print_template():
    ip_address = "192.168.1.100"
    with patch('tp.printer.Network') as MockNetwork:
        mock_printer = MockNetwork.return_value
        printer = ThermalPrinter(ip_address)
        template = "Hello, {name}!"
        context = {"name": "World"}
        printer.print_template(template, context)
        assert mock_printer.text.call_count == 1
        mock_printer.text.assert_called_with("Hello, World!\n")

def test_task():
    ip_address = "192.168.1.100"
    with patch('tp.printer.Network') as MockNetwork:
        mock_printer = MockNetwork.return_value
        printer = ThermalPrinter(ip_address)
        printer.task("Test Task", "This is a test.")
        expected_calls = [
            # Assuming your code prints these lines
            patch.call("Test Task\n"),
            patch.call("This is a test.\n"),
        ]
        assert mock_printer.text.call_count == len(expected_calls)
        mock_printer.text.assert_has_calls(expected_calls)

def test_ticket():
    ip_address = "192.168.1.100"
    with patch('tp.printer.Network') as MockNetwork:
        mock_printer = MockNetwork.return_value
        printer = ThermalPrinter(ip_address)
        printer.ticket("Test Ticket", "12345", "This is a test ticket.")
        expected_calls = [
            patch.call("Test Ticket\n"),
            patch.call("12345\n"),
            patch.call("This is a test ticket.\n"),
        ]
        assert mock_printer.text.call_count == len(expected_calls)
        mock_printer.text.assert_has_calls(expected_calls)
