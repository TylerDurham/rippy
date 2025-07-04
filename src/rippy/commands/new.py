import typer
import makemkv
from rippy import search
import rich.console
from rich.prompt import Prompt
import rich.progress
import rich.table

app = typer.Typer()

console = rich.console.Console()

@app.command(name="movie")
def movie(movie_title: str = "", disc: int = 0, min_length: int = 3600):

    if len(movie_title) == 0:
        mkv = makemkv.MakeMKV(disc)
        disc_info = mkv.info(minlength=min_length, cache=10)
        titles = disc_info.get("titles")
        if titles and len(titles):
            movie_title = do_print_makemkv_info(titles, disc)
        else:
            raise RuntimeError(f"ERROR! No titles found on disc {disc}")
            
    answer = Prompt.ask(
        f"Would you like to search for metadata about '[bold blue]{movie_title}[/bold blue]'?", 
        choices=["yes", "no"],
        default="yes"
    )


    movies = search.find_movies(str(movie_title)) 
    do_print_movie_metadata(movies)
    if answer == "yes":
                selected_id = Prompt.ask("Please enter the id of the movie that best matches.", choices=[str(n) for n in range(1, len(movies))])
        

@app.command(name="tv-show")
def tv_show():
    print("Hello from 'tv-show' NOT IMPLEMENTED!")

if __name__ == "__main__":
    app()

def do_print_makemkv_info(titles, disc: int):
    title = titles[0]
    movie_title = title.get("name")
    information = title.get("information")
    chapter_count = title.get("chapter_count")
    # size = title.get("size")
    size_human = title.get("size_human")
    
    table = rich.table.Table("Key", "Value")
    table.add_row("Title", movie_title)
    table.add_row("information", information)
    table.add_row("Size", size_human)
    table.add_row("Chapter(s)", str(chapter_count))
    
    console.print(f"The following title information was found on disc {disc}:")
    console.print(table)

    return str(movie_title)

def do_print_movie_metadata(movies):
    """
    Prints a table of movies found during a metadata search.
    """
    table = rich.table.Table("ID", "Title", "Year", "Popularity", "Desciption")
    count = 0
    for movie in movies:
        count = count + 1
        table.add_row(
            str(count), 
            movie["title"], 
            movie["release_date"][:4], 
            str(movie["popularity"]),
            f'{movie["overview"][:64]}...\n'
        )

    console.print(table)
    
def do_select_movie_metadata():
    print("")
    
