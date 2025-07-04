import typer
from rippy import shared
from rich.table import Table
from rich.console import Console

console = Console()

app = typer.Typer()

@app.command(name="get")
def get():
    """
    Gets the current rippy configuration.
    """ 
    style = shared.PathInfoConsoleStyler()

    table = Table("Key", "Description", "Path")

    for path in shared.paths:
        table.add_row(f"{style.key(path.name)}", f"{path.description}", f"{style.path(path.path)}")

    console.print(table)

@app.command(name="set")
def set():
    print("Set!")

if __name__ == "__main__":
    app()
