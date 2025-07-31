from typing import Annotated
from rippy.core.defaults import get_defaults
from rippy.core.config import RippyConfig
import typer as t

DEFAULTS = get_defaults()

app = t.Typer(name="config")

OPT_NAME = Annotated[str, t.Argument(
    help="The name of the property to get or set.")]
OPT_VALUE = Annotated[str, t.Argument(
    help="The value of the property to set.")]
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

    key = name.replace("-", "_")
    cfg = RippyConfig.read(config_file, ensure_path=True)
    # TODO: Ensure ints are supported!
    setattr(cfg, key, value)
    cfg.save(path_to_config_file=config_file, overwrite=True)

    # section = None
    # cfg = read_config()
    # core_props = [f.name for f in fields(cfg.core)]
    # makemkv_props = [f.name for f in fields(cfg.makemkv)]
    #
    # if name in core_props:
    #     section = cfg.core
    # if name in makemkv_props:
    #     section = cfg.makemkv
    #
    # if all:
    #     print("[core]")
    #     for prop in core_props:
    #         print(f" - {prop} = {getattr(cfg.core, prop)})")
    #
    #     print("[makemkv]")
    #     for prop in makemkv_props:
    #         print(f" - {prop} = {getattr(cfg.makemkv, prop)})")
    #
    # if not name == None and value == None:
    #     print(f"{getattr(section, name)}")
    # if not name == None and not value == None:
    #
    #     if not section == None:
    #         setattr(section, name, value)
    #         write_config(cfg, overwrite=True)
    #
    #     write_config(cfg, overwrite=True)


if __name__ == "__main__":
    app()
