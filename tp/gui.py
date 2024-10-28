import logging
import sys

from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from tp.config import (
    get_chars_per_line,
    get_enable_special_letters,
    get_printer_ip,
    set_chars_per_line,
    set_enable_special_letters,
    set_printer_ip,
)
from tp.printer import ThermalPrinter

logger = logging.getLogger(__name__)


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Thermal Printer Application")
        self.init_ui()

    def init_ui(self) -> None:
        layout = QVBoxLayout()

        label = QLabel("Select a Printing Command:")
        layout.addWidget(label)

        button_layout = QHBoxLayout()

        task_button = QPushButton("Task")
        task_button.clicked.connect(self.open_task_dialog)
        button_layout.addWidget(task_button)

        small_note_button = QPushButton("Small Note")
        small_note_button.clicked.connect(self.print_small_note)
        button_layout.addWidget(small_note_button)

        ticket_button = QPushButton("Ticket")
        ticket_button.clicked.connect(self.open_ticket_dialog)
        button_layout.addWidget(ticket_button)

        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self.open_settings_dialog)
        button_layout.addWidget(settings_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def open_task_dialog(self) -> None:
        dialog = TaskDialog(self)
        dialog.exec()

    def open_ticket_dialog(self) -> None:
        dialog = TicketDialog(self)
        dialog.exec()

    def print_small_note(self) -> None:
        confirm = QMessageBox.question(
            self,
            "Confirm",
            "Do you want to print a small note?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                ip_address = get_printer_ip()
            except ValueError as e:
                QMessageBox.critical(self, "Error", str(e))
                return
            try:
                printer = ThermalPrinter(ip_address)
                printer.small_note()
                QMessageBox.information(self, "Success", "Printed small note.")
            except Exception as e:
                logger.error(f"Error printing small note: {e}", exc_info=True)
                QMessageBox.critical(self, "Error", f"Failed to print small note: {e}")

    def open_settings_dialog(self) -> None:
        dialog = SettingsDialog(self)
        dialog.exec()


class TaskDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Print Task")
        self.init_ui()

    def init_ui(self) -> None:
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.title_input = QLineEdit()
        self.text_input = QTextEdit()
        form_layout.addRow("Title:", self.title_input)
        form_layout.addRow("Text (supports markdown):", self.text_input)
        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        print_button = QPushButton("Print")
        print_button.clicked.connect(self.print_task)
        button_layout.addWidget(print_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def print_task(self) -> None:
        title = self.title_input.text()
        text = self.text_input.toPlainText()
        try:
            ip_address = get_printer_ip()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
            return
        try:
            printer = ThermalPrinter(ip_address)
            printer.task(title, text)
            QMessageBox.information(self, "Success", "Printed task.")
            self.accept()
        except Exception as e:
            logger.error(f"Error printing task: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Failed to print task: {e}")


class TicketDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Print Ticket")
        self.init_ui()

    def init_ui(self) -> None:
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.title_input = QLineEdit()
        self.ticket_number_input = QLineEdit()
        self.text_input = QTextEdit()
        form_layout.addRow("Title:", self.title_input)
        form_layout.addRow("Ticket Number:", self.ticket_number_input)
        form_layout.addRow("Text (supports markdown):", self.text_input)
        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        print_button = QPushButton("Print")
        print_button.clicked.connect(self.print_ticket)
        button_layout.addWidget(print_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def print_ticket(self) -> None:
        title = self.title_input.text()
        ticket_number = self.ticket_number_input.text()
        text = self.text_input.toPlainText()
        try:
            ip_address = get_printer_ip()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
            return
        try:
            printer = ThermalPrinter(ip_address)
            printer.ticket(title, ticket_number, text)
            QMessageBox.information(self, "Success", "Printed ticket.")
            self.accept()
        except Exception as e:
            logger.error(f"Error printing ticket: {e}", exc_info=True)
            QMessageBox.critical(self, "Error", f"Failed to print ticket: {e}")


class SettingsDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.init_ui()

    def init_ui(self) -> None:
        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.ip_input = QLineEdit()
        try:
            self.ip_input.setText(get_printer_ip())
        except ValueError:
            self.ip_input.setText("")
        form_layout.addRow("Printer IP Address:", self.ip_input)

        self.chars_per_line_input = QLineEdit()
        self.chars_per_line_input.setText(str(get_chars_per_line()))
        form_layout.addRow("Characters Per Line:", self.chars_per_line_input)

        self.enable_special_letters_input = QLineEdit()
        self.enable_special_letters_input.setText(str(get_enable_special_letters()))
        form_layout.addRow("Enable Special Letters (True/False):", self.enable_special_letters_input)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(save_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_settings(self) -> None:
        ip_address = self.ip_input.text()
        set_printer_ip(ip_address)

        chars_per_line_value = self.chars_per_line_input.text()
        try:
            chars_per_line = int(chars_per_line_value)
            set_chars_per_line(chars_per_line)
        except ValueError:
            QMessageBox.critical(self, "Error", "Invalid number for chars per line.")
            return

        enable_special_letters_value = self.enable_special_letters_input.text()
        if enable_special_letters_value.lower() in ("true", "yes", "1"):
            enable_special_letters = True
        elif enable_special_letters_value.lower() in ("false", "no", "0"):
            enable_special_letters = False
        else:
            QMessageBox.critical(self, "Error", "Invalid value for enable special letters. Use True or False.")
            return
        set_enable_special_letters(enable_special_letters)
        QMessageBox.information(self, "Success", "Settings saved.")
        self.accept()


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
