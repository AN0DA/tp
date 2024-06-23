import configparser

CONFIG_FILE = "tp_config.ini"


def get_printer_ip() -> str:
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    try:  # Added try-except block to handle missing key
        return config.get("Printer", "ip_address")
    except configparser.NoOptionError:
        raise ValueError("Printer IP address not set")


def set_printer_ip(ip_address: str) -> None:
    config = configparser.ConfigParser()
    config["Printer"] = {"ip_address": ip_address}
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)
