from typing import Annotated
import typer as t 

app = t.Typer()

@app.command(name="init")
def init(
        type: str = "movie",
        title: Annotated[
            str,
            t.Argument(help="The title of the movie or TV show. If no `title` is specified, you must use the `-r` option to try to get the title from the currently inserted disk.")
        ] = "",
        read: Annotated[
            bool,
            t.Option("-r", "--read", help="Attempt to get the title from the currently inserted disk.")
        ] = False,
        search: Annotated[
            bool,
            t.Option("-s", "--search", help="Search for the title at {api tbd}.")
        ] = False
    ):
    """
    Initializes a new {app_name} directory for a movie or TV show.
    """
    
    # Sanity check inputs
    check_inputs(title, read, search)

    print(f"type: {type}")
    print(f"title: {title}")
    print(f"read: {read}")
    print(f"search: {search}")

def check_inputs(title: str, read: bool, search: bool):

    if len(title) > 0 and read:
        raise ValueError("Invalid input: title should not be used with read.")

    if len(title) == 0 and search and not read:
        raise ValueError("Invalid input: `--search` should be used with either `title` or `--read`.")


if __name__ == "__main__":
    app()


