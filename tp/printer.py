from typing import Any

from escpos.printer import Network


class ThermalPrinter:
    def __init__(self, ip_address: str) -> None:
        self.printer = Network(ip_address)

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.printer.close()

    def small_note(self) -> None:
        self.printer.ln(7)
        self.printer.cut()

    def task(self, title: str, text: str) -> None:
        self.printer.ln()
        if title:
            self.printer.set(align="center", font="a", bold=True, double_width=True, double_height=True)
            self.printer.textln(title)
            self.printer.textln("-----------------------\n")
        self.printer.set(align="left", font="a", bold=False)
        self.printer.textln(text)
        self.printer.cut()

    def ticket(self, title: str, ticket_number: str, text: str) -> None:
        self.printer.ln()
        if title:
            self.printer.set(align="center", font="a", bold=True, double_width=True, double_height=True)
            self.printer.textln(title)
        if ticket_number:
            self.printer.set(
                align="center", font="b", bold=False, underline=True, double_width=True, double_height=True
            )
            self.printer.textln(ticket_number)
        if not title and not ticket_number:
            self.printer.ln(2)
        self.printer.set(align="center", font="a", bold=True, double_width=True, double_height=True)
        self.printer.textln("-----------------------\n")
        self.printer.set(align="left", font="a", bold=False)
        self.printer.textln(text)
        self.printer.cut()
