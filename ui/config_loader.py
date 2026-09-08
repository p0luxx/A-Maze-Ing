from sys import argv

from pydantic import BaseModel, Field, ValidationError, model_validator


class ConfigError(Exception):
    """Represent errors caused by invalid configuration syntax."""


class ConfigVal(BaseModel):
    """Represent and validate maze configuration data."""

    width: int = Field(alias="WIDTH", ge=11, le=30)
    height: int = Field(alias="HEIGHT", ge=7, le=30)
    entry: tuple[int, int] = Field(alias="ENTRY")
    exit: tuple[int, int] = Field(alias="EXIT")
    output_file: str = Field(alias="OUTPUT_FILE")
    perfect: bool = Field(alias="PERFECT")
    seed: int | None = Field(default=None, alias="SEED")

    @model_validator(mode="after")
    def validate_coordinates(self) -> "ConfigVal":
        """Validate relationships between maze coordinates.

        Returns:
            The validated configuration instance.

        Raises:
            ValueError: If entry or exit coordinates are outside
                the grid, or if both coordinates are equal.
        """
        entry_x, entry_y = self.entry
        exit_x, exit_y = self.exit

        if (
            entry_x < 0
            or entry_x >= self.width
            or entry_y < 0
            or entry_y >= self.height
        ):
            raise ValueError(
                "Entry coordinates must be inside the grid"
            )

        if (
            exit_x < 0
            or exit_x >= self.width
            or exit_y < 0
            or exit_y >= self.height
        ):
            raise ValueError(
                "Exit coordinates must be inside the grid"
            )

        if self.entry == self.exit:
            raise ValueError(
                "Entry and exit coordinates cannot be the same"
            )

        return self


def read_config() -> list[str]:
    """Read the configuration file.

    Returns:
        The lines contained in the configuration file.

    Raises:
        IndexError: If no configuration file argument is provided.
        FileNotFoundError: If the configuration file does not exist.
        PermissionError: If the file cannot be read due to permissions.
    """
    file_name: str = argv[1]

    with open(file_name, "r") as file:
        return file.readlines()


def conv_dict(
    config: list[str],
) -> dict[str, str | tuple[int, int]]:
    """Convert configuration lines into a key-value dictionary.

    Args:
        config: Configuration file lines to process.

    Returns:
        The parsed configuration dictionary.

    Raises:
        ConfigError: If a line does not follow the KEY=VALUE format.
        ValueError: If coordinates cannot be converted to integers.
    """
    data: dict[str, str | tuple[int, int]] = {}

    for line in config:
        line = line.strip()

        if line.startswith("#") or not line:
            continue

        key_value: list[str] = line.split("=", 1)

        if len(key_value) != 2:
            raise ConfigError("Invalid 'KEY=VALUE' format")

        key = key_value[0].strip()
        value = key_value[1].strip()

        data[key] = value

    for key in ("ENTRY", "EXIT"):
        if key in data:
            raw_value = data[key]

            if not isinstance(raw_value, str):
                raise ConfigError(
                    f"Invalid {key} coordinate format"
                )

            coordinates = raw_value.split(",")

            if len(coordinates) != 2:
                raise ConfigError(
                    f"Invalid {key} coordinate format"
                )

            x = int(coordinates[0])
            y = int(coordinates[1])

            data[key] = (x, y)

    return data


def process_config() -> ConfigVal | None:
    """Read, parse, and validate the maze configuration.

    Returns:
        The validated configuration instance if processing succeeds.
        None if the configuration cannot be processed.
    """
    try:
        config_lines = read_config()
        config_data = conv_dict(config_lines)

        return ConfigVal.model_validate(config_data)

    except IndexError:
        print("Configuration file argument is missing")
    except FileNotFoundError as error:
        print(error)
    except PermissionError as error:
        print(error)
    except ConfigError as error:
        print(error)
    except ValidationError as error:
        print(error)
    except ValueError as error:
        print(error)

    return None


""" RECORDAR BORRAR
def main() -> None:
    config = process_config()

    if config is None:
        return

    print("Configuration validated")
    print(f"WIDTH: {config.width}")
    print(f"HEIGHT: {config.height}")
    print(f"ENTRY: {config.entry}")
    print(f"EXIT: {config.exit}")
    print(f"OUTPUT_FILE: {config.output_file}")
    print(f"PERFECT: {config.perfect}")
    print(f"SEED: {config.seed}")


if __name__ == "__main__":
    main()
"""
