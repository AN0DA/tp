from typing import Dict, List
from escpos.printer import Network
import logging

logger = logging.getLogger(__name__)


class ThermalPrinter:
    """
    A class to interface with a thermal printer over the network.
    """

    def __init__(self, ip_address: str):
        """
        Initialize the ThermalPrinter with the given IP address.
        """
        self.printer = Network(ip_address, timeout=10)
        logging.debug(f"Initialized ThermalPrinter with IP {ip_address}")

    def print_segments(self, segments: List[Dict[str, Dict]]) -> None:
        """
        Given a list of segments, each a dict with 'text' and 'styles', print them accordingly.
        """
        try:
            for segment in segments:
                text = segment["text"]
                styles = segment.get("styles", {})
                logger.debug("Printing segment: %s with styles: %s", text, styles)
                self.printer.set(
                    align=styles.get("align", "left"),
                    font=styles.get("font", "a"),
                    bold=styles.get("bold", False),
                    underline=1 if styles.get("underline", False) else 0,
                    double_width=styles.get("double_width", False),
                    double_height=styles.get("double_height", False),
                )
                self.printer.text(text)
            # Reset styles
            self.printer.set(
                align="left",
                font="a",
                bold=False,
                underline=0,
                double_width=False,
                double_height=False,
            )
            logger.info("Printed segments successfully.")
        except Exception as e:
            logger.error(f"Error printing segments: {e}", exc_info=True)
            raise

    def task(self, title: str, text: str) -> None:
        """
        Print a task template with the specified styling.
        """
        segments = []
        segments.append({'text': '\n', 'styles': {}})
        if title:
            segments.append({
                'text': f"{title}\n",
                'styles': {
                    'align': 'center',
                    'font': 'a',
                    'bold': True,
                    'double_width': True,
                    'double_height': True
                }
            })
            segments.append({
                'text': "-----------------------\n",
                'styles': {
                    'align': 'center',
                    'font': 'a',
                    'bold': True,
                    'double_width': True,
                    'double_height': True
                }
            })
        segments.append({
            'text': f"{text}\n",
            'styles': {
                'align': 'left',
                'font': 'a',
                'bold': False
            }
        })
        self.print_segments(segments)
        self.printer.cut()

    def small_note(self) -> None:
        """
        Print a small note template.
        """
        segments = [{'text': '\n' * 7, 'styles': {}}]
        self.print_segments(segments)
        self.printer.cut()

    def ticket(self, title: str, ticket_number: str, text: str) -> None:
        """
        Print a ticket template with the specified styling.
        """
        segments = []
        segments.append({'text': '\n', 'styles': {}})
        if title:
            segments.append({
                'text': f"{title}\n",
                'styles': {
                    'align': 'center',
                    'font': 'a',
                    'bold': True,
                    'double_width': True,
                    'double_height': True
                }
            })
        if ticket_number:
            segments.append({
                'text': f"{ticket_number}\n",
                'styles': {
                    'align': 'center',
                    'font': 'b',
                    'underline': True,
                    'double_width': True,
                    'double_height': True
                }
            })
        if not title and not ticket_number:
            segments.append({'text': '\n' * 2, 'styles': {}})
        segments.append({
            'text': "-----------------------\n",
            'styles': {
                'align': 'center',
                'font': 'a',
                'bold': True,
                'double_width': True,
                'double_height': True
            }
        })
        segments.append({
            'text': f"{text}\n",
            'styles': {
                'align': 'left',
                'font': 'a',
                'bold': False
            }
        })
        self.print_segments(segments)
        self.printer.cut()
