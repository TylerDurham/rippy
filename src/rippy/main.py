import typer as t

from rippy.commands import config, init

app = t.Typer()

app.command(name="config")(config.get)
app.add_typer(init.app)
