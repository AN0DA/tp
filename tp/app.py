from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static, Input, Label, MarkdownViewer
from textual.containers import Vertical, Horizontal
from textual.screen import Screen
from tp.config import (
    get_printer_ip,
    set_printer_ip,
    get_chars_per_line,
    set_chars_per_line,
    get_enable_special_letters,
    set_enable_special_letters,
)
from tp.printer import ThermalPrinter
from typing import Optional
import logging
import sys

# Initialize the logger
logger = logging.getLogger(__name__)


class MainView(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Vertical(
            Label("Select a Printing Command:", id="main_label"),
            Horizontal(
                Button("Task", id="task_button"),
                Button("Small Note", id="small_note_button"),
                Button("Ticket", id="ticket_button"),
                Button("Settings", id="settings_button"),
            ),
            Static("Preview will appear here.", id="preview"),
            id="main_container",
        )

    async def on_button_pressed(self, event):
        logger = logging.getLogger(__name__)
        button_id = event.button.id
        logger.debug("Button pressed in MainView: %s", button_id)
        if button_id == "task_button":
            await self.app.push_screen(TaskInputView())
        elif button_id == "small_note_button":
            await self.app.push_screen(ConfirmPrintScreen("small_note"))
        elif button_id == "ticket_button":
            await self.app.push_screen(TicketInputView())
        elif button_id == "settings_button":
            await self.app.push_screen(SettingsView())

    async def on_mount(self):
        preview = self.query_one("#preview")
        preview.update("Select a command to see the preview.")


class TaskInputView(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Vertical(
            Label("Enter Task Details:", id="task_label"),
            Label("Title:"),
            Input(placeholder="Title", id="title_input"),
            Label("Text (supports markdown):"),
            Input(placeholder="Text", id="text_input"),
            Horizontal(
                Button("Preview", id="preview_button"),
                Button("Print", id="print_button"),
                Button("Back", id="back_button"),
            ),
            id="task_input_container",
        )
        yield Static(id="preview_area")

    async def on_button_pressed(self, event):
        logger = logging.getLogger(__name__)
        button_id = event.button.id
        logger.debug("Button pressed in TaskInputView: %s", button_id)
        if button_id == "preview_button":
            title = self.query_one("#title_input").value
            text = self.query_one("#text_input").value
            logger.debug("Preview button clicked with title: %s, text: %s", title, text)
            preview_text = f"**Task:** {title}\n{text}"
            self.query_one("#preview_area").update(MarkdownViewer(markdown=preview_text))
        elif button_id == "print_button":
            title = self.query_one("#title_input").value
            text = self.query_one("#text_input").value
            logger.debug("Print button clicked with title: %s, text: %s", title, text)
            await self.app.print_task(title, text)
            self.app.pop_screen()
        elif button_id == "back_button":
            logger.debug("Back button clicked in TaskInputView")
            self.app.pop_screen()


class TicketInputView(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Vertical(
            Label("Enter Ticket Details:", id="ticket_label"),
            Label("Title:"),
            Input(placeholder="Title", id="title_input"),
            Label("Ticket Number:"),
            Input(placeholder="Ticket Number", id="ticket_number_input"),
            Label("Text (supports markdown):"),
            Input(placeholder="Text", id="text_input"),
            Horizontal(
                Button("Preview", id="preview_button"),
                Button("Print", id="print_button"),
                Button("Back", id="back_button"),
            ),
            id="ticket_input_container",
        )
        yield Static(id="preview_area")

    async def on_button_pressed(self, event):
        logger = logging.getLogger(__name__)
        button_id = event.button.id
        logger.debug("Button pressed in TicketInputView: %s", button_id)
        if button_id == "preview_button":
            title = self.query_one("#title_input").value
            ticket_number = self.query_one("#ticket_number_input").value
            text = self.query_one("#text_input").value
            logger.debug(
                "Preview button clicked with title: %s, ticket_number: %s, text: %s", title, ticket_number, text
            )
            preview_text = f"**Ticket:** {title}\n**Number:** {ticket_number}\n{text}"
            self.query_one("#preview_area").update(MarkdownViewer(markdown=preview_text))
        elif button_id == "print_button":
            title = self.query_one("#title_input").value
            ticket_number = self.query_one("#ticket_number_input").value
            text = self.query_one("#text_input").value
            logger.debug("Print button clicked with title: %s, ticket_number: %s, text: %s", title, ticket_number, text)
            await self.app.print_ticket(title, ticket_number, text)
            self.app.pop_screen()
        elif button_id == "back_button":
            logger.debug("Back button clicked in TicketInputView")
            self.app.pop_screen()


class SettingsView(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Vertical(
            Label("Printer Settings", id="settings_label"),
            Label("Printer IP Address:"),
            Input(placeholder="Printer IP Address", id="ip_input"),
            Label("Characters Per Line:"),
            Input(placeholder="Characters Per Line", id="chars_per_line_input"),
            Label("Enable Special Letters (True/False):"),
            Input(placeholder="Enable Special Letters (True/False)", id="enable_special_letters_input"),
            Horizontal(
                Button("Save", id="save_button"),
                Button("Back", id="back_button"),
            ),
            id="settings_container",
        )

    async def on_mount(self):
        logger = logging.getLogger(__name__)
        try:
            ip_address = get_printer_ip()
            logger.debug("Loaded printer IP: %s", ip_address)
        except ValueError:
            ip_address = ""
            logger.debug("No printer IP found in settings.")
        self.query_one("#ip_input").value = ip_address

        chars_per_line = get_chars_per_line()
        logger.debug("Loaded chars_per_line: %d", chars_per_line)
        self.query_one("#chars_per_line_input").value = str(chars_per_line)

        enable_special_letters = get_enable_special_letters()
        logger.debug("Loaded enable_special_letters: %s", enable_special_letters)
        self.query_one("#enable_special_letters_input").value = str(enable_special_letters)

    async def on_button_pressed(self, event):
        logger = logging.getLogger(__name__)
        button_id = event.button.id
        logger.debug("Button pressed in SettingsView: %s", button_id)
        if button_id == "save_button":
            ip_address = self.query_one("#ip_input").value
            logger.debug("Saving printer IP: %s", ip_address)
            set_printer_ip(ip_address)

            chars_per_line_value = self.query_one("#chars_per_line_input").value
            try:
                chars_per_line = int(chars_per_line_value)
                logger.debug("Saving chars_per_line: %d", chars_per_line)
                set_chars_per_line(chars_per_line)
            except ValueError:
                await self.app.show_error("Invalid number for chars per line.")
                logger.error("Invalid chars_per_line value: %s", chars_per_line_value)
                return

            enable_special_letters_value = self.query_one("#enable_special_letters_input").value
            if enable_special_letters_value.lower() in ("true", "yes", "1"):
                enable_special_letters = True
            elif enable_special_letters_value.lower() in ("false", "no", "0"):
                enable_special_letters = False
            else:
                await self.app.show_error("Invalid value for enable special letters. Use True or False.")
                logger.error("Invalid enable_special_letters value: %s", enable_special_letters_value)
                return
            logger.debug("Saving enable_special_letters: %s", enable_special_letters)
            set_enable_special_letters(enable_special_letters)

            self.app.pop_screen()
        elif button_id == "back_button":
            logger.debug("Back button clicked in SettingsView")
            self.app.pop_screen()


class ConfirmPrintScreen(Screen):
    def __init__(self, command_name: str):
        super().__init__()
        self.command_name = command_name

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Vertical(
            Label(f"Do you want to print {self.command_name.replace('_', ' ')}?"),
            Horizontal(
                Button("Yes", id="yes_button"),
                Button("No", id="no_button"),
            ),
            id="confirm_print_container",
        )

    async def on_button_pressed(self, event):
        logger = logging.getLogger(__name__)
        button_id = event.button.id
        logger.debug("Button pressed in ConfirmPrintScreen: %s", button_id)
        if button_id == "yes_button":
            logger.debug("Confirmed printing command: %s", self.command_name)
            if self.command_name == "small_note":
                await self.app.print_small_note()
            self.app.pop_screen()
        elif button_id == "no_button":
            logger.debug("Cancelled printing command: %s", self.command_name)
            self.app.pop_screen()


class NotificationScreen(Screen):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Vertical(
            Label(self.message),
            Button("OK", id="ok_button"),
            id="notification_container",
        )

    async def on_button_pressed(self, event):
        logger = logging.getLogger(__name__)
        logger.debug("OK button pressed in NotificationScreen")
        self.app.pop_screen()


class ThermalPrinterApp(App):
    async def on_mount(self):
        logger = logging.getLogger(__name__)
        logger.debug("Application mounted.")
        await self.push_screen(MainView())

    async def print_task(self, title: str, text: str):
        logger = logging.getLogger(__name__)
        ip_address = self.get_printer_ip()
        if not ip_address:
            await self.show_error("Printer IP address not set. Please set it in the settings.")
            logger.error("Printer IP address not set.")
            return
        try:
            logger.debug("Creating ThermalPrinter with IP: %s", ip_address)
            printer = ThermalPrinter(ip_address)
            logger.debug("Calling printer.task with title: %s, text: %s", title, text)
            printer.task(title, text)
            await self.show_message("Printed task.")
            logger.info("Printed task successfully.")
        except Exception as e:
            logger.error(f"Error printing task: {e}", exc_info=True)
            await self.show_error(f"Failed to print task: {e}")

    async def print_ticket(self, title: str, ticket_number: str, text: str):
        logger = logging.getLogger(__name__)
        ip_address = self.get_printer_ip()
        if not ip_address:
            await self.show_error("Printer IP address not set. Please set it in the settings.")
            logger.error("Printer IP address not set.")
            return
        try:
            logger.debug("Creating ThermalPrinter with IP: %s", ip_address)
            printer = ThermalPrinter(ip_address)
            logger.debug(
                "Calling printer.ticket with title: %s, ticket_number: %s, text: %s", title, ticket_number, text
            )
            printer.ticket(title, ticket_number, text)
            await self.show_message("Printed ticket.")
            logger.info("Printed ticket successfully.")
        except Exception as e:
            logger.error(f"Error printing ticket: {e}", exc_info=True)
            await self.show_error(f"Failed to print ticket: {e}")

    async def print_small_note(self):
        logger = logging.getLogger(__name__)
        ip_address = self.get_printer_ip()
        if not ip_address:
            await self.show_error("Printer IP address not set. Please set it in the settings.")
            logger.error("Printer IP address not set.")
            return
        try:
            logger.debug("Creating ThermalPrinter with IP: %s", ip_address)
            printer = ThermalPrinter(ip_address)
            logger.debug("Calling printer.small_note()")
            printer.small_note()
            await self.show_message("Printed small note.")
            logger.info("Printed small note successfully.")
        except Exception as e:
            logger.error(f"Error printing small note: {e}", exc_info=True)
            await self.show_error(f"Failed to print small note: {e}")

    def get_printer_ip(self) -> Optional[str]:
        logger = logging.getLogger(__name__)
        try:
            ip = get_printer_ip()
            logger.debug("Retrieved printer IP: %s", ip)
            return ip
        except ValueError:
            logger.debug("Printer IP not set in configuration.")
            return None

    async def show_error(self, message: str):
        logger = logging.getLogger(__name__)
        logger.error("Showing error message: %s", message)
        await self.push_screen(NotificationScreen(f"Error: {message}"))

    async def show_message(self, message: str):
        logger = logging.getLogger(__name__)
        logger.info("Showing message: %s", message)
        await self.push_screen(NotificationScreen(message))


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("app.log", encoding="utf-8"),
        ],
    )
    app = ThermalPrinterApp()
    app.run()


if __name__ == "__main__":
    main()
