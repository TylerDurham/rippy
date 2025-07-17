import typer as t 
from typing import Annotated, List 

app = t.Typer()

def complete_section(): 
    return ["rippy", "rippy.movie", "rippy.tv-show"]

@app.command("list")
def list():
    pass


OPT_SECTION = Annotated[
    str,
    t.Argument(
        help="The section name of the property.",
        autocompletion=complete_section
    )
]

OPT_NAME = Annotated[
    str,
    t.Argument(
        help="The name of the property."
    )
]

OPT_VALUE = Annotated[
    str,
    t.Argument(
        help="The value of the property."
    )
]

@app.command("get")
def get(
    section: Annotated[
        str,
        t.Argument(help="{help tbd}", autocompletion=complete_section)
    ] = "{default}",
    name: Annotated[
        str,
        t.Argument(help="{help tbd}")
    ] = "{default}"
):
    """
    Gets the value for a config option.
    """

    print(f"section: {section} name: {name}") 

@app.command("set")
def set(section: OPT_SECTION, name: OPT_NAME, value: OPT_VALUE):
    """
    Sets the value for a config option.
    """
    print(f"section: {section} name: {name} value: {value}") 

if __name__ == "__main__":
    app()
