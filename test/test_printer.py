# tests/test_printer.py

from collections.abc import Generator
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from tp.printer import ThermalPrinter


@pytest.fixture
def mock_network_printer() -> Generator[MagicMock, None, None]:
    with patch("tp.printer.Network") as mock_network:
        yield mock_network


def test_printer_initialization(mock_network_printer: MagicMock) -> None:
    ThermalPrinter("192.168.1.100")
    mock_network_printer.assert_called_with("192.168.1.100", timeout=10)


def test_print_segments(mock_network_printer: MagicMock) -> None:
    printer = ThermalPrinter("192.168.1.100")
    segment: dict[str, Any] = {"text": "Test", "styles": {"bold": False}}
    printer.print_segments([segment])
    # Verify that set and text methods are called with correct arguments
    mock_network_printer.return_value.set.assert_called_with(
        align="left", font="a", bold=False, underline=0, double_width=False, double_height=False
    )
    mock_network_printer.return_value.text.assert_called_with("Test")


def test_task_method(mock_network_printer: MagicMock) -> None:
    printer = ThermalPrinter("192.168.1.100")
    printer.task("Title", "Content")
    # Ensure print_segments and cut are called
    assert mock_network_printer.return_value.cut.called


def test_small_note_method(mock_network_printer: MagicMock) -> None:
    printer = ThermalPrinter("192.168.1.100")
    printer.small_note()
    # Ensure print_segments and cut are called
    assert mock_network_printer.return_value.cut.called


def test_ticket_method(mock_network_printer: MagicMock) -> None:
    printer = ThermalPrinter("192.168.1.100")
    printer.ticket("Title", "123", "Content")
    # Ensure print_segments and cut are called
    assert mock_network_printer.return_value.cut.called


def test_print_segments_exception(mock_network_printer: MagicMock) -> None:
    # Simulate an exception during printing
    mock_network_printer.return_value.text.side_effect = Exception("Printer error")
    printer = ThermalPrinter("192.168.1.100")
    segment: dict[str, Any] = {"text": "Test", "styles": {}}
    with pytest.raises(Exception, match="Printer error"):
        printer.print_segments([segment])
