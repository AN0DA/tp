import configparser

CONFIG_FILE = "tp_config.ini"


def get_printer_ip() -> str:
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    try:
        return config.get("Printer", "ip_address")
    except (configparser.NoSectionError, configparser.NoOptionError):
        raise ValueError("Printer IP address not set")


def set_printer_ip(ip_address: str) -> None:
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if not config.has_section("Printer"):
        config.add_section("Printer")
    config.set("Printer", "ip_address", ip_address)
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)


def get_chars_per_line() -> int:
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    try:
        return config.getint("Printer", "chars_per_line")
    except (configparser.NoSectionError, configparser.NoOptionError):
        return 32  # Default value


def set_chars_per_line(chars_per_line: int) -> None:
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if not config.has_section("Printer"):
        config.add_section("Printer")
    config.set("Printer", "chars_per_line", str(chars_per_line))
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)


def get_enable_special_letters() -> bool:
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    try:
        return config.getboolean("Printer", "enable_special_letters")
    except (configparser.NoSectionError, configparser.NoOptionError):
        return True  # Default value


def set_enable_special_letters(enable: bool) -> None:
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if not config.has_section("Printer"):
        config.add_section("Printer")
    config.set("Printer", "enable_special_letters", str(enable))
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)
