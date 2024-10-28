import logging
import os

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.wrappers.response import Response

from tp.config import (
    get_chars_per_line,
    get_enable_special_letters,
    get_flask_debug,
    get_flask_secret_key,
    get_printer_ip,
    set_chars_per_line,
    set_enable_special_letters,
    set_printer_ip,
)
from tp.printer import ThermalPrinter

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = get_flask_secret_key()
app.config["DEBUG"] = get_flask_debug()


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/task", methods=["GET", "POST"])
def task() -> Response | str:
    if request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")
        try:
            ip_address = get_printer_ip()
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for("settings"))
        try:
            printer = ThermalPrinter(ip_address)
            printer.task(title or "", text or "")
            flash("Printed task.", "success")
            return redirect(url_for("index"))
        except Exception as e:
            logger.error(f"Error printing task: {e}", exc_info=True)
            flash(f"Failed to print task: {e}", "error")
            return redirect(url_for("task"))
    return render_template("task.html")


@app.route("/small_note", methods=["GET", "POST"])
def small_note() -> Response | str:
    if request.method == "POST":
        confirm = request.form.get("confirm")
        if confirm == "yes":
            try:
                ip_address = get_printer_ip()
            except ValueError as e:
                flash(str(e), "error")
                return redirect(url_for("settings"))
            try:
                printer = ThermalPrinter(ip_address)
                printer.small_note()
                flash("Printed small note.", "success")
                return redirect(url_for("index"))
            except Exception as e:
                logger.error(f"Error printing small note: {e}", exc_info=True)
                flash(f"Failed to print small note: {e}", "error")
                return redirect(url_for("small_note"))
        else:
            flash("Cancelled printing small note.", "info")
            return redirect(url_for("index"))
    return render_template("small_note.html")


@app.route("/ticket", methods=["GET", "POST"])
def ticket() -> Response | str:
    if request.method == "POST":
        title = request.form.get("title")
        ticket_number = request.form.get("ticket_number")
        text = request.form.get("text")
        try:
            ip_address = get_printer_ip()
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for("settings"))
        try:
            printer = ThermalPrinter(ip_address)
            printer.ticket(title or "", ticket_number or "", text or "")
            flash("Printed ticket.", "success")
            return redirect(url_for("index"))
        except Exception as e:
            logger.error(f"Error printing ticket: {e}", exc_info=True)
            flash(f"Failed to print ticket: {e}", "error")
            return redirect(url_for("ticket"))
    return render_template("ticket.html")


@app.route("/settings", methods=["GET", "POST"])
def settings() -> Response | str:
    if request.method == "POST":
        ip_address = request.form.get("ip_address")
        chars_per_line_value = request.form.get("chars_per_line")
        enable_special_letters_value = request.form.get("enable_special_letters")

        set_printer_ip(ip_address or "")

        try:
            chars_per_line = int(chars_per_line_value or 0)
            set_chars_per_line(chars_per_line)
        except ValueError:
            flash("Invalid number for chars per line.", "error")
            return redirect(url_for("settings"))

        if (enable_special_letters_value or "").lower() in ("true", "yes", "1"):
            enable_special_letters = True
        elif (enable_special_letters_value or "").lower() in ("false", "no", "0"):
            enable_special_letters = False
        else:
            flash("Invalid value for enable special letters. Use True or False.", "error")
            return redirect(url_for("settings"))
        set_enable_special_letters(enable_special_letters)
        flash("Settings saved.", "success")
        return redirect(url_for("index"))
    else:
        try:
            ip_address = get_printer_ip()
        except ValueError:
            ip_address = ""
        chars_per_line = get_chars_per_line()
        enable_special_letters = get_enable_special_letters()
        return render_template(
            "settings.html",
            ip_address=ip_address,
            chars_per_line=chars_per_line,
            enable_special_letters=enable_special_letters,
        )


def main() -> None:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    template_dir = os.path.join(dir_path, "templates")
    static_dir = os.path.join(dir_path, "static")
    app.template_folder = template_dir
    app.static_folder = static_dir

    app.run(host="0.0.0.0", port=5555)  # nosec: B104
