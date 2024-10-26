import pytest
from unittest.mock import patch, MagicMock
from tp.app import ThermalPrinterApp

@pytest.fixture
def app():
    app = ThermalPrinterApp()
    app.get_printer_ip = MagicMock(return_value="192.168.1.100")
    app.show_message = MagicMock()
    app.show_error = MagicMock()
    return app

@pytest.mark.asyncio
async def test_print_task(app):
    with patch('tp.app.ThermalPrinter') as MockPrinter:
        mock_printer_instance = MockPrinter.return_value
        await app.print_task("Test Task", "This is a test.")
        mock_printer_instance.task.assert_called_with("Test Task", "This is a test.")
        app.show_message.assert_called_with("Printed task.")

@pytest.mark.asyncio
async def test_print_task_no_ip():
    app = ThermalPrinterApp()
    app.get_printer_ip = MagicMock(return_value=None)
    app.show_error = MagicMock()
    await app.print_task("Test Task", "This is a test.")
    app.show_error.assert_called_with("Printer IP address not set. Please set it in the settings.")

@pytest.mark.asyncio
async def test_print_ticket(app):
    with patch('tp.app.ThermalPrinter') as MockPrinter:
        mock_printer_instance = MockPrinter.return_value
        await app.print_ticket("Test Ticket", "12345", "This is a test ticket.")
        mock_printer_instance.ticket.assert_called_with("Test Ticket", "12345", "This is a test ticket.")
        app.show_message.assert_called_with("Printed ticket.")

@pytest.mark.asyncio
async def test_print_small_note(app):
    with patch('tp.app.ThermalPrinter') as MockPrinter:
        mock_printer_instance = MockPrinter.return_value
        await app.print_small_note()
        mock_printer_instance.small_note.assert_called_once()
        app.show_message.assert_called_with("Printed small note.")
