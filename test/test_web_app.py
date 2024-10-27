# tests/test_web_app.py

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from flask.testing import FlaskClient

from tp import web_app


@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    web_app.app.config["TESTING"] = True
    with web_app.app.test_client() as client:
        yield client


@pytest.fixture
def mock_printer() -> Generator:
    with patch("tp.web_app.ThermalPrinter") as mock_printer_class:
        yield mock_printer_class


@pytest.fixture
def mock_get_printer_ip() -> Generator:
    with patch("tp.web_app.get_printer_ip", return_value="192.168.1.100"):
        yield


def test_index_route(client: FlaskClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert b"Thermal Printer Application" in response.data


def test_task_route_get(client: FlaskClient) -> None:
    response = client.get("/task")
    assert response.status_code == 200
    assert b"Print Task" in response.data


def test_task_route_post(client: FlaskClient, mock_printer: MagicMock, mock_get_printer_ip: MagicMock) -> None:
    response = client.post("/task", data={"title": "Test Title", "text": "Test Text"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Printed task." in response.data
    mock_printer.return_value.task.assert_called_with("Test Title", "Test Text")


def test_task_route_post_no_ip(client: FlaskClient) -> None:
    with patch("tp.web_app.get_printer_ip", side_effect=ValueError("Printer IP address not set")):
        response = client.post("/task", data={"title": "Test Title", "text": "Test Text"}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Printer IP address not set" in response.data


def test_small_note_route_post_yes(
    client: FlaskClient, mock_printer: MagicMock, mock_get_printer_ip: MagicMock
) -> None:
    response = client.post("/small_note", data={"confirm": "yes"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Printed small note." in response.data
    assert mock_printer.return_value.small_note.called


def test_small_note_route_post_no(client: FlaskClient) -> None:
    response = client.post("/small_note", data={"confirm": "no"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Cancelled printing small note." in response.data


def test_ticket_route_post(client: FlaskClient, mock_printer: MagicMock, mock_get_printer_ip: MagicMock) -> None:
    data = {"title": "Test Title", "ticket_number": "123", "text": "Test Text"}
    response = client.post("/ticket", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Printed ticket." in response.data
    mock_printer.return_value.ticket.assert_called_with("Test Title", "123", "Test Text")


def test_settings_route_get(client: FlaskClient) -> None:
    with patch("tp.web_app.get_printer_ip", return_value="192.168.1.100"), patch(
        "tp.web_app.get_chars_per_line", return_value=32
    ), patch("tp.web_app.get_enable_special_letters", return_value=True):
        response = client.get("/settings")
        assert response.status_code == 200
        assert b"192.168.1.100" in response.data
        assert b"32" in response.data
        assert b"True" in response.data


def test_settings_route_post(client: FlaskClient) -> None:
    data = {"ip_address": "192.168.1.101", "chars_per_line": "48", "enable_special_letters": "False"}
    with patch("tp.web_app.set_printer_ip") as mock_set_ip, patch(
        "tp.web_app.set_chars_per_line"
    ) as mock_set_chars, patch("tp.web_app.set_enable_special_letters") as mock_set_enable:
        response = client.post("/settings", data=data, follow_redirects=True)
        assert response.status_code == 200
        assert b"Settings saved." in response.data
        mock_set_ip.assert_called_with("192.168.1.101")
        mock_set_chars.assert_called_with(48)
        mock_set_enable.assert_called_with(False)
