from sys import argv
from pydantic import ValidationError


def read_config() -> tuple[bool, list[str] | OSError]:
    """Read the configuration file provided as a command-line argument.

    Returns:
        A tuple containing:
        - True and the configuration file lines if the file is read successfully.
        - False and the corresponding OSError if the file cannot be opened.
    """
    try:
        file_name: str = argv[1]
        with open(file_name, "r") as file:
            config: list[str] = file.readlines()
        return (True, config)
    except FileNotFoundError as e:
        return (False, e)
    except PermissionError as e:
        return (False, e)

"""
    En read_config queda pendiente gestionar el bool
"""
class ConfigError(Exception):
    pass


def conv_dict(config: list[str]) -> 
     tuple[bool, dict[str, str] | ConfigError):
    """Convert configuration lines into a key-value dictionary.

    Args:
        config: Configuration file lines to process.

    Returns:
        A tuple containing:
        - True and the resulting configuration dictionary if conversion succeeds.
        - False and a ConfigError if a line does not follow the KEY=VALUE format.
    """
    dic: dict[str, str] = {}
    for line in config:
        line = line.strip()
        if line.startswith("#"):
            continue
        if not line:
            continue
        keyvalue: list[str] = line.split("=", 1)
        if len(keyvalue) != 2:
            return (False, ConfigError("Invalid 'KEY=VALUE' format"))
        key = keyvalue[0].strip()
        value = keyvalue[1].strip()
        dic[key] = value
    return (True, dic)


def process_config() -> dict[str | str]:
    if not read_config[0]:
        print(read_config[1])
        return
    try:
        return (conv_dict(read_config[1]))        
    except ConfigError as e:
        print(e)
"""
    Revisar manyana por tu propia cuenta
"""
