import pytest
from tp.utils import TemplateRenderer, remove_polish_special_characters
from tp.config import set_chars_per_line, set_enable_special_letters

def test_remove_polish_special_characters():
    text = "Zażółć gęślą jaźń"
    expected = "Zazolc gesla jazn"
    assert remove_polish_special_characters(text) == expected

def test_template_renderer_with_special_letters_enabled():
    set_chars_per_line(50)
    set_enable_special_letters(True)
    renderer = TemplateRenderer()
    template = "{text}"
    context = {"text": "Zażółć gęślą jaźń"}
    rendered_segments = renderer.render(template, context)
    rendered_text = ''.join(segment['text'] for segment in rendered_segments)
    assert "Zażółć gęślą jaźń" in rendered_text

def test_template_renderer_with_special_letters_disabled():
    set_chars_per_line(50)
    set_enable_special_letters(False)
    renderer = TemplateRenderer()
    template = "{text}"
    context = {"text": "Zażółć gęślą jaźń"}
    rendered_segments = renderer.render(template, context)
    rendered_text = ''.join(segment['text'] for segment in rendered_segments)
    assert "Zazolc gesla jazn" in rendered_text

def test_template_renderer_text_wrapping():
    set_chars_per_line(20)
    set_enable_special_letters(True)
    renderer = TemplateRenderer()
    template = "{text}"
    context = {"text": "This is a very long line that should wrap correctly."}
    rendered_segments = renderer.render(template, context)
    rendered_text = ''.join(segment['text'] for segment in rendered_segments)
    expected_text = "This is a very long\nline that should\nwrap correctly."
    assert rendered_text == expected_text
