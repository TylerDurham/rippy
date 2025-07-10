from rippy.commands.task import Task, TaskResult, TaskContext
from rich.console import Console

from makemkv import MakeMKV, ProgressParser

console = Console()

class TaskGetDiskInfo(Task):
    def execute(self, context: TaskContext) -> TaskResult:
        print(f"{self.name}")
        if context.args.movie_title == None :
            print("Initializeing MakeMKV")


        return self.choose_direction()


def __get_disk_titles(disk_no: int = 0):
    with ProgressParser() as progress:
        mkv = MakeMKV(disk_no, progress_handler=progress.parse_progress)
        info = mkv.info()

if __name__ == "__main__":
    __get_disk_titles(0)

