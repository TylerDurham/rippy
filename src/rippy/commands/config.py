from dataclasses import asdict, field, fields
from typing import Annotated, List

import typer as t

from rippy.core.config import MakeMKVSettings, RippySettings, read_config, write_config
from rippy.forms.config_form import ConfigForm

app = t.Typer()


# def complete_section():
#     return ["rippy", "rippy.movie", "rippy.tv-show"]
#
# @app.command("init")
# def init():
#     cf = ConfigForm()
#     cf.run()
#
# @app.command("list")
# def list():
#     pass
#


OPT_NAME = Annotated[str, t.Argument(help="The name of the property.")]

OPT_VALUE = Annotated[str, t.Argument(help="The value of the property.")]


@app.command()
def get(
    name: str = t.Argument(None, help="{help tbd}"),
    value: str = t.Argument(None, help="{help tbd}"),
    all: bool = t.Option(False, "--all, -a", help="{help tbd}"),
):
    """
    Gets the value for a config option.
    """

    section = None
    cfg = read_config()
    core_props = [f.name for f in fields(cfg.core)]
    makemkv_props = [f.name for f in fields(cfg.makemkv)]

    if name in core_props:
        section = cfg.core
    if name in makemkv_props:
        section = cfg.makemkv

    if all:
        print("[core]")
        for prop in core_props:
            print(f" - {prop} = {getattr(cfg.core, prop)})")

        print("[makemkv]")
        for prop in makemkv_props:
            print(f" - {prop} = {getattr(cfg.makemkv, prop)})")

    if not name == None and value == None:
        print(f"{getattr(section, name)}")
    if not name == None and not value == None:

        if not section == None:
            setattr(section, name, value)
            write_config(cfg, overwrite=True)

        write_config(cfg, overwrite=True)


if __name__ == "__main__":
    app()
