from typing import Annotated

import typer as t

import rippy.commands.errors as e

app = t.Typer()


@app.command(name="init")
def init(
    type: str = "movie",
    title: Annotated[
        str,
        t.Argument(
            help="The title of the movie or TV show. If no `title` is specified, you must use the `-r` option to try to get the title from the currently inserted disk."
        ),
    ] = "",
    read: Annotated[
        bool,
        t.Option(
            "-r",
            "--read",
            help="Attempt to get the title from the currently inserted disk.",
        ),
    ] = False,
    search: Annotated[
        bool, t.Option("-s", "--search", help="Search for the title at {api tbd}.")
    ] = False,
):
    """
    Initializes a new {app_name} directory for a movie or TV show.
    """

    check_inputs(title, read, search)

    print(f"type: {type}")
    print(f"title: {title}")
    print(f"read: {read}")
    print(f"search: {search}")


def check_inputs(title: str, read: bool, search: bool):

    if len(title) == 0 and not read and not search:
        raise e.E_NO_ARGS()

    if len(title) > 0 and read:
        raise e.E_INIT_TITLE_WITH_READ()

    if len(title) == 0 and search and not read:
        raise e.E_INIT_SEARCH_NO_READ_OR_TITLE()


if __name__ == "__main__":
    app()
