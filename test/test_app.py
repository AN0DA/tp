import os
import sys
from collections.abc import Generator
from test.test_config import CONFIG_FILE
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from tp.app import app

runner = CliRunner()


@pytest.fixture
def mock_printer() -> Generator[MagicMock, None, None]:
    with patch("tp.app.ThermalPrinter") as mock_printer_class:
        yield mock_printer_class


@pytest.fixture
def mock_get_printer_ip() -> Generator:
    with patch("tp.app.get_printer_ip", return_value="192.168.1.100"):
        yield


def test_task_command(mock_printer: MagicMock, mock_get_printer_ip: MagicMock) -> None:
    result = runner.invoke(app, ["print", "task"], input="Test Title\nTest Text")
    assert result.exit_code == 0
    assert "Printed task." in result.output
    mock_printer.return_value.task.assert_called_with("Test Title", "Test Text")


def test_task_command_no_ip() -> None:
    with patch("tp.app.get_printer_ip", side_effect=ValueError("Printer IP address not set")):
        result = runner.invoke(app, ["print", "task"], input="Test Title\nTest Text")
        assert result.exit_code != 0
        assert "Printer IP address not set" in result.output


def test_small_note_command(mock_printer: MagicMock, mock_get_printer_ip: MagicMock) -> None:
    result = runner.invoke(app, ["print", "small-note"], input="y")
    assert result.exit_code == 0
    assert "Printed small note." in result.output
    assert mock_printer.return_value.small_note.called


def test_small_note_command_cancel() -> None:
    result = runner.invoke(app, ["print", "small-note"], input="n")
    assert result.exit_code == 0
    assert "Cancelled printing small note." in result.output


def test_ticket_command(mock_printer: MagicMock, mock_get_printer_ip: MagicMock) -> None:
    inputs = "Test Title\n123\nTest Text"
    result = runner.invoke(app, ["print", "ticket"], input=inputs)
    assert result.exit_code == 0
    assert "Printed ticket." in result.output
    mock_printer.return_value.ticket.assert_called_with("Test Title", "123", "Test Text")


def test_settings_show_command() -> None:
    with patch("tp.app.get_printer_ip", return_value="192.168.1.100"), patch(
        "tp.app.get_chars_per_line", return_value=32
    ), patch("tp.app.get_enable_special_letters", return_value=True):
        result = runner.invoke(app, ["settings", "show"])
        assert result.exit_code == 0
        assert "Printer IP Address: 192.168.1.100" in result.output
        assert "Characters Per Line: 32" in result.output
        assert "Enable Special Letters: True" in result.output


def test_config_edit_command(mocker: Any) -> None:
    config_file_path = os.path.abspath(CONFIG_FILE)
    # Mock typer.echo
    mock_echo = mocker.patch("tp.app.typer.echo")
    # Mock sys.exit
    mocker.patch("tp.app.sys.exit")

    if sys.platform == "win32":
        # Mock os.startfile on Windows
        mock_startfile = mocker.patch("tp.app.os.startfile")
    elif sys.platform == "darwin":
        # Mock subprocess.call for macOS
        mock_subprocess_call = mocker.patch("tp.app.subprocess.call")
    else:
        # Mock subprocess.call for Linux and other platforms
        mock_subprocess_call = mocker.patch("tp.app.subprocess.call")

    result = runner.invoke(app, ["config", "edit"])
    assert result.exit_code == 0
    mock_echo.assert_any_call(f"Opening configuration file: {config_file_path}")

    if sys.platform == "win32":
        assert mock_startfile.called
    else:
        assert mock_subprocess_call.called
