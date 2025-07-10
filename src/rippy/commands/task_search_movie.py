
from rippy.commands.task import Task, TaskResult, TaskContext

class TaskSearchMovie(Task):

    def execute(self, context: TaskContext) -> TaskResult:
        print(f"{self.name}")

        return self.choose_direction()
        


