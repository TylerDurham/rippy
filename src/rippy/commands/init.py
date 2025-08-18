from enum import Enum
from typing import Annotated

import requests
import typer as t
import os

import rippy.commands.errors as e
from rippy.core.config import RippyConfig

app = t.Typer()

cfg = RippyConfig().read()
API_KEY = cfg.api_key
RIP_DIR = cfg.rip_dir

def search_movies(title: str, api_key: str):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}&include_adult=false&language=en-US&page=1"

    headers = {"accept": "application/json", "Authorization": f"Bearer {api_key}"}

    response = requests.get(url, headers=headers)

    data = response.json()
    return data["results"]

def select_movie(movies):
    count = 0
    for movie in movies:
    
        # id = movie['id']
        title = movie['title']
        year = movie['release_date'][:4]
        description = movie["overview"]
        print(f'{count}] {title} ({year}): {description}')
        if count == 4: break
        count = count + 1

    selected_id = int(input("Enter the number of your selection: "))
    return movies[selected_id]

def make_dirs(title: str, year: int, id: str):
    movie_dir_name = f'{title} ({year})'
    

    os.makedirs(os.path.join(RIP_DIR, "@imports", movie_dir_name))
    os.makedirs(os.path.join(RIP_DIR, "movies", movie_dir_name))

    with open(os.path.join(RIP_DIR, "movies", movie_dir_name, '.plexinfo'), 'w') as file:
        file.write(f'Title: {movie_dir_name}\n')
        file.write(f'Year: {year}\n')
        file.write(f'tmdb: {id}')
        file.close()

class InitType(str, Enum):
    movie = "movie"
    tv_show = "tv-show"


@app.command(name="init")
def init(
    type: Annotated[
        InitType,
        t.Argument(
            help=f"The type of initialization to perform. Either a `{InitType.movie}` or `{InitType.tv_show}`"
        ),
    ] = InitType.movie,
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

    cfg = RippyConfig.read()
    
    movies = search_movies(title, cfg.api_key) # movie.search(title)
    selected = select_movie(movies)
    print(selected)

    title = selected['title']
    safe_title = title.replace(":", "-")
    movie_db_id = selected['id']
    year = selected['release_date'][:4]

    make_dirs(safe_title, year, movie_db_id)

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
