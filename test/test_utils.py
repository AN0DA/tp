# tests/test_utils.py

from typing import Any

import pytest

from tp.utils import TemplateRenderer, remove_polish_special_characters


def test_remove_polish_special_characters() -> None:
    text = "Zażółć gęślą jaźń"
    expected = "Zazolc gesla jazn"
    assert remove_polish_special_characters(text) == expected


def test_template_renderer_missing_placeholder() -> None:
    renderer = TemplateRenderer()
    template = "Hello, {name}!"
    context: dict[str, str] = {}
    with pytest.raises(KeyError):
        renderer.render(template, context)


def test_template_renderer_special_letters_disabled(mocker: Any) -> None:
    # Mock get_enable_special_letters to return False
    mocker.patch("tp.utils.get_enable_special_letters", return_value=False)
    renderer = TemplateRenderer()
    template = "Zażółć gęślą jaźń"
    context: dict[str, str] = {}
    segments = renderer.render(template, context)
    expected_text = "Zazolc gesla jazn"
    combined_text = "".join(segment["text"] for segment in segments)
    assert combined_text == expected_text
