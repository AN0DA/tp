import typer

from tp.config import get_printer_ip, set_printer_ip
from tp.printer import ThermalPrinter
import typer

app = typer.Typer()


@app.command()
def task(title: str, text: str) -> None:
    ip_address = get_printer_ip()
    if not ip_address:
        typer.echo("Printer IP address not set. Please set it using the 'set-ip' command.")
        raise typer.Exit(code=1)
    printer = ThermalPrinter(ip_address)
    printer.task(title, text)


@app.command()
def small_note() -> None:
    ip_address = get_printer_ip()
    if not ip_address:
        typer.echo("Printer IP address not set. Please set it using the 'set-ip' command.")
        raise typer.Exit(code=1)
    printer = ThermalPrinter(ip_address)
    printer.small_note()


@app.command()
def ticket(title: str, ticket_number: str, text: str) -> None:
    ip_address = get_printer_ip()
    if not ip_address:
        typer.echo("Printer IP address not set. Please set it using the 'set-ip' command.")
        raise typer.Exit(code=1)
    printer = ThermalPrinter(ip_address)
    printer.ticket(title, ticket_number, text)


@app.command()
def set_ip(ip_address: str) -> None:
    set_printer_ip(ip_address)
    typer.echo(f"Printer IP address set to {ip_address}")


if __name__ == "__main__":
    app()
