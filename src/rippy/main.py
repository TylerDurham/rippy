import typer
# from rippy import new, config

from rippy.commands import config, new
from rich.console import Console
console = Console()

app = typer.Typer()

app.add_typer(new.app, name="new")
app.add_typer(config.app, name="config")

# @app.command(name="info")
# def info():
#     style = shared.PathInfoConsoleStyler()
#
#     table = Table("Key", "Description", "Path")
#
#     for path in shared.paths:
#         table.add_row(f"{style.key(path.name)}", f"{path.description}", f"{style.path(path.path)}")
#
#     console.print(table)
#

