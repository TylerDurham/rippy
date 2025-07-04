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
def movie(movie_title: str = "The Man who Knew Too Much", disc: int = 0, min_length: int = 3600):

    if len(movie_title) == 0:
        mkv = makemkv.MakeMKV(disc)
        disc_info = mkv.info(minlength=min_length, cache=10)
        titles = disc_info.get("titles")
        if titles and len(titles):
            title = titles[0]
            movie_title = title.get("name")
            information = title.get("information")
            chapter_count = title.get("chapter_count")
            size = title.get("size")
            size_human = title.get("size_human")
            
            table = rich.table.Table("Title", "Size")
            table.add_row(movie_title, size_human)
            
            console.print(f"The following title information was found on disc {disc}:")
        console.print(table)

    answer = Prompt.ask(
        f"Would you like to search for metadata about '[bold blue]{movie_title}[/bold blue]'?", 
        choices=["yes", "no"],
        default="yes"
    )


    if answer == "yes":
        movies = search.find_movies(str(movie_title)) 
        console.print(movies)
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
        selected_id = Prompt.ask("Please enter the id of the movie that best matches.", choices=[str(n) for n in range(1, len(movies))])
        

@app.command(name="tv-show")
def tv_show():
    print("Hello from 'tv-show' NOT IMPLEMENTED!")

if __name__ == "__main__":
    app()
    
