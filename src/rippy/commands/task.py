from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from rich.prompt import Prompt
from rippy.config import RippyConfig

class TaskResult(Enum):
    Previous = 1
    Next = 2
    Cancel = 4

@dataclass(frozen=True)
class CommandLineArgs():
    
    movie_title: str | None
    min_length: int | None

@dataclass
class TaskSelections():
    disk_number: int | None
    movie_title: str | None

@dataclass(frozen=True)
class TaskContext():

    config: RippyConfig
    args: CommandLineArgs 
    selections: TaskSelections

class Task():

    __name: str

    def __init__(self):
        self.__name = self.__class__.__name__ 

    @abstractmethod
    def execute(self, context: TaskContext) -> TaskResult:
        pass 
    
    @property
    def name(self) -> str:
        return  self.__name

    def choose_direction(self):
        answer = Prompt.ask("Choose (p)revious, (n)ext, or (c)ancel", default="n", choices=["p", "n", "c"])

        if answer == "p":
            return TaskResult.Previous
        elif answer == "c":
            return TaskResult.Cancel
        else:
            return TaskResult.Next


