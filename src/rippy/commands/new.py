import typer as t 
from rippy.commands.task import CommandLineArgs, TaskSelections, TaskContext
from rippy.commands.task_get_disk_info import TaskGetDiskInfo
from rippy.commands.task_search_movie import TaskSearchMovie
from rippy.config import read_config
from rippy.commands.task_manager import TaskManager
from typing import Annotated, Optional

app = t.Typer()

@app.command(name="movie")
def movie(
    movie_title: 
        Annotated[Optional[str], t.Option("--movie-title", "-t", help="")] = None, 
    min_length: 
        Annotated[Optional[int], t.Option("--min_length", "-l", help="")] = 360):

    config = read_config()
    selections = TaskSelections(disk_number=None, movie_title=None)
    args = CommandLineArgs(movie_title=movie_title, min_length=min_length)
    context = TaskContext(args=args, config=config, selections=selections) 

    tasks = [
        TaskGetDiskInfo(),
        TaskSearchMovie()
    ]

    tm = TaskManager(tasks)
    tm.start(context)

@app.command(name="tv-show")
def tv_show(show_title: str | None):
    pass

if __name__ == "__main__":
    app()
