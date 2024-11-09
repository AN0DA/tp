import logging
import os
import subprocess  # nosec: B404
import sys

import typer

from tp.config import (
    CONFIG_FILE,
    get_chars_per_line,
    get_enable_special_letters,
    get_printer_ip,
    set_chars_per_line,
    set_enable_special_letters,
    set_printer_ip,
)
from tp.printer import ThermalPrinter
from tp.template_manager import TemplateManager
from tp.utils import compute_agenda_variables, is_new_version_available

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log", encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)

app = typer.Typer(help="Thermal Printer Application")
settings_app = typer.Typer(help="Settings commands")
config_app = typer.Typer(help="Configuration commands")

app.add_typer(settings_app, name="settings")
app.add_typer(config_app, name="config")

missing_ip_message = "Printer IP address not set. Please set it using 'settings set-ip'."


@print_app.command()
def task(
    title: str = typer.Option(None, help="Task Title"),
    text: str = typer.Option(None, help="Task Text (supports markdown)"),
) -> None:
    """
    Print a task.
    """
    if not title:
        title = typer.prompt("Enter Task Title")
    if not text:
        text = typer.prompt("Enter Task Text (supports markdown)")
    try:
        ip_address = get_printer_ip()
    except ValueError as e:
        typer.echo(str(e))
        typer.echo(missing_ip_message)
        sys.exit(1)
    try:
        printer = ThermalPrinter(ip_address)
        printer.task(title, text)
        typer.echo("Printed task.")
    except Exception as e:
        typer.echo(f"Failed to print task: {e}")
        logger.error(f"Error printing task: {e}", exc_info=True)
        sys.exit(1)


@app.command()
def print_template(template_name: str = typer.Argument(None)) -> None:
    """
    Print using a specified template.
    """
    template_manager = TemplateManager("tp/print_templates")
    if not template_name:
        typer.echo("Available templates:")
        for name in template_manager.list_templates():
            typer.echo(f"- {name}")
        template_name = typer.prompt("Enter the template name")

    template = template_manager.get_template(template_name)
    if not template:
        typer.echo(f"Template '{template_name}' not found.")
        sys.exit(1)

    context = {}
    if template_name == "agenda":
        context = compute_agenda_variables()
    else:
        for var in template.get("variables", []):
            if var.get("markdown", False):
                value = click.edit(var["description"], require_save=True)
            else:
                value = typer.prompt(var["description"])
            context[var["name"]] = value

    try:
        ip_address = get_printer_ip()
        with ThermalPrinter(ip_address, template_manager) as printer:
            printer.print_template(template_name, context)
        typer.echo(f"Printed using template '{template_name}'.")
    except Exception as e:
        typer.echo(f"Failed to print: {e}")
        logger.error(f"Error printing template '{template_name}': {e}", exc_info=True)
        sys.exit(1)


@settings_app.command("set-ip")
def set_ip(ip_address: str = typer.Argument(..., help="Printer IP Address")) -> None:
    """
    Set the printer IP address.
    """
    set_printer_ip(ip_address)
    typer.echo(f"Printer IP address set to {ip_address}")


@settings_app.command("set-chars-per-line")
def set_chars_per_line_command(chars_per_line: int = typer.Argument(..., help="Characters Per Line")) -> None:
    """
    Set the number of characters per line.
    """
    set_chars_per_line(chars_per_line)
    typer.echo(f"Characters per line set to {chars_per_line}")


@settings_app.command("set-enable-special-letters")
def set_enable_special_letters_command(
    enable: bool = typer.Argument(..., help="Enable special letters (True/False)"),
) -> None:
    """
    Enable or disable special letters.
    """
    set_enable_special_letters(enable)
    typer.echo(f"Enable special letters set to {enable}")


@settings_app.command()
def show() -> None:
    """
    Show current settings.
    """
    try:
        ip_address = get_printer_ip()
    except ValueError:
        ip_address = "Not set"
    chars_per_line = get_chars_per_line()
    enable_special_letters = get_enable_special_letters()
    typer.echo(f"Printer IP Address: {ip_address}")
    typer.echo(f"Characters Per Line: {chars_per_line}")
    typer.echo(f"Enable Special Letters: {enable_special_letters}")


@app.command()
def gui() -> None:
    """
    Launch the GUI version of the application.
    """
    try:
        import tp.gui

        tp.gui.main()
    except ImportError as e:
        typer.echo("Failed to launch GUI. PyQt6 might not be installed.")
        typer.echo("Install it using 'pip install PyQt6'")
        logger.error(f"Error launching GUI: {e}", exc_info=True)
        sys.exit(1)


@app.command()
def web() -> None:
    """
    Launch the web server with the web interface.
    """
    try:
        import tp.web_app

        tp.web_app.main()
    except ImportError as e:
        typer.echo("Failed to launch web interface. Flask might not be installed.")
        typer.echo("Install it using 'pip install Flask'")
        logger.error(f"Error launching web interface: {e}", exc_info=True)
        sys.exit(1)


@config_app.command("edit")
def config_edit() -> None:
    """
    Open the configuration file for editing.
    """
    config_file_path = os.path.abspath(CONFIG_FILE)
    typer.echo(f"Opening configuration file: {config_file_path}")
    try:
        if sys.platform == "win32":
            os.startfile(config_file_path)  # nosec: B606
        elif sys.platform == "darwin":
            subprocess.call(["open", config_file_path])  # nosec: B603, B607
        else:
            # For Linux and other platforms
            editor = os.environ.get("EDITOR", "nano")
            subprocess.call([editor, config_file_path])  # nosec: B603
    except Exception as e:
        typer.echo(f"Failed to open configuration file: {e}")
        logger.error(f"Error opening configuration file: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    app()
