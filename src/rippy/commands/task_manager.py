from typing import List
from rippy.commands.task import Task, TaskResult, TaskContext

class TaskManager():
    __tasks: List[Task]     

    def __init__(self, tasks):
        self.__tasks = tasks

    def start(self, context: TaskContext):
        cur_task_no = 0

        if not self.__tasks == None and len(self.__tasks):
            while cur_task_no >= 0 and cur_task_no < len(self.__tasks):
                print(f"Executing task {cur_task_no}")
                task = self.__tasks[cur_task_no]
                result = task.execute(context)

                if result == TaskResult.Next:
                    cur_task_no += 1
                    
                elif result == TaskResult.Previous:
                    cur_task_no -= 1

                else:
                    cur_task_no = -1



