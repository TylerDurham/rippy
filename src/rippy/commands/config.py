from typing import Annotated
from rippy.core.defaults import get_defaults
from rippy.core.config import RippyConfig
import typer as t

DEFAULTS = get_defaults()

app = t.Typer(name="config")

def __parse_int(value: str):
    print(f"Parsing value {value}")
    try:
        return int(value)
    except ValueError:
        return value

OPT_NAME = Annotated[str, t.Argument(
    help="The name of the property to get or set.")]
OPT_VALUE = Annotated[str, t.Argument(
    help="The value of the property to set.",
    callback=lambda x: __parse_int(x))]
OPT_PATH = Annotated[str, t.Option(
    "--config-file", "-c", help="Specify the path to the config file. The default location is recommended for production.")]

@app.command(name="get")
def get_value(
    name: OPT_NAME,
    config_file: OPT_PATH = DEFAULTS.CONFIG_FILE_PATH
):
    """
    Gets the value for a config option.
    """

    key = name.replace("-", "_")
    cfg = RippyConfig.read(config_file, ensure_path=True)
    print(f"{getattr(cfg, key)}")


@app.command(name="set")
def set_value(
    name: OPT_NAME,
    value: OPT_VALUE,
    config_file: OPT_PATH = DEFAULTS.CONFIG_FILE_PATH
):
    """
    Sets the value for a config option.
    """
    fixed_name = name.replace("-", "_")     # HACK: I like dashes in TOML, but python prefers underscores.

    cfg = RippyConfig.read(config_file, ensure_path=True)
    setattr(cfg, fixed_name, value)
    cfg.save(path_to_config_file=config_file, overwrite=True)


if __name__ == "__main__":
    app()
    

