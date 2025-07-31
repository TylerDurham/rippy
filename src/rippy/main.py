import typer as t

from rippy.commands import config, init

app = t.Typer()

app.add_typer(config.app)
app.add_typer(init.app)
