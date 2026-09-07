from sys import argv


class ConfigError(Exception):
    pass


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
    except IndexError as e:
        return (False, e)


def conv_dict(config: list[str]) -> tuple[bool, dict[str, str] | ConfigError]:
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
            raise ConfigError("Invalid 'KEY=VALUE' format")
        key = keyvalue[0].strip()
        value = keyvalue[1].strip()
        dic[key] = value
    return (True, dic)

"""
No se si process config deba de imprimir nada o solo devolver cosas 
o simplemente no neceste process config.
"""
def process_config() -> dict[str | str] | None:
    read = read_config()
    if not read[0]:
        print(read[1])
        return None
    try:
        return conv_dict(read[1])
    except ConfigError as e:
        print(e)

"""
main de prueba

def main() -> None:
    result = process_config()

    if result is None:
        return

    with open("result.txt", "w") as file:
        file.write(str(result))


if __name__ == "__main__":
    main()
"""
