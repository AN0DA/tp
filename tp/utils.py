import textwrap
from typing import Dict, List, Any
from tp.config import get_chars_per_line, get_enable_special_letters
import logging
import re

logger = logging.getLogger(__name__)

POLISH_CHARACTERS = {
    "ą": "a",
    "ć": "c",
    "ę": "e",
    "ł": "l",
    "ń": "n",
    "ó": "o",
    "ś": "s",
    "ź": "z",
    "ż": "z",
    "Ą": "A",
    "Ć": "C",
    "Ę": "E",
    "Ł": "L",
    "Ń": "N",
    "Ó": "O",
    "Ś": "S",
    "Ź": "Z",
    "Ż": "Z",
}


def remove_polish_special_characters(text: str) -> str:
    """
    Replace Polish special letters with their ASCII equivalents.
    """
    for polish_char, ascii_char in POLISH_CHARACTERS.items():
        text = text.replace(polish_char, ascii_char)
    return text


class TemplateRenderer:
    """
    Renders templates with context, handling markdown formatting,
    text wrapping, and special character processing.
    """

    def __init__(self) -> None:
        self.reload_settings()
        logging.debug("Initialized TemplateRenderer.")

    def reload_settings(self) -> None:
        """
        Reload settings from the configuration.
        """
        self.chars_per_line = get_chars_per_line()
        self.enable_special_letters = get_enable_special_letters()
        logging.debug("TemplateRenderer settings reloaded.")

    def render(self, template: str, context: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Render the template with context, handling special characters,
        markdown formatting, and wrapping.
        """
        try:
            logger.debug("Rendering template with context: %s", context)
            text = template.format(**context)
            logger.debug("Formatted text: %s", text)
        except KeyError as e:
            logger.error(f"Missing placeholder in context: {e}")
            raise

        if not self.enable_special_letters:
            logger.debug("Removing special letters from text")
            text = remove_polish_special_characters(text)

        segments = self.parse_markdown(text)
        logger.debug("Parsed segments: %s", segments)
        return segments

    def parse_markdown(self, text: str) -> List[Dict[str, Any]]:
        """
        Parses markdown text and returns a list of segments with text and formatting.
        """
        logger = logging.getLogger(__name__)
        logger.debug("Parsing markdown text")
        # Define patterns for markdown elements
        patterns = [
            (r"\*\*(.*?)\*\*", {"bold": True}),
            (r"__(.*?)__", {"bold": True}),
            (r"\*(.*?)\*", {"italic": True}),
            (r"_(.*?)_", {"italic": True}),
            (r"~~(.*?)~~", {"underline": True}),
            (r"`(.*?)`", {"font": "B"}),
        ]

        combined_pattern = "|".join(f"({p})" for p, _ in patterns)
        regex = re.compile(combined_pattern)

        segments = []
        pos = 0
        while pos < len(text):
            match = regex.search(text, pos)
            if match:
                start, end = match.span()
                # Add any text before the match as a plain segment
                if start > pos:
                    plain_text = text[pos:start]
                    wrapped_text = textwrap.fill(plain_text, width=self.chars_per_line)
                    segments.append({"text": wrapped_text, "styles": {}})
                # Determine which group matched
                for i, (_, style) in enumerate(patterns):
                    if match.group(i + 1):
                        content = match.group(i + 1)
                        wrapped_text = textwrap.fill(content, width=self.chars_per_line)
                        segments.append({"text": wrapped_text, "styles": style})
                        break
                pos = end
            else:
                # No more matches; add the rest of the text as a plain segment
                plain_text = text[pos:]
                wrapped_text = textwrap.fill(plain_text, width=self.chars_per_line)
                segments.append({"text": wrapped_text, "styles": {}})
                break
        logger.debug("Parsed segments: %s", segments)
        return segments
