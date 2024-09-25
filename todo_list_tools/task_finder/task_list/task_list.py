import sys
import os

# put the home directory (~) into a variable
home_directory = os.path.expanduser("~")
# Add the parent directory of the current file (task_list) to the system path
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append( home_directory + '/the_function_caller/todo_list_tools/' )

# from todo_list_tools.task.task import Task
from task import Task

class TaskList:
    """Manages a list of tasks and subtasks."""
    
    def __init__(self, tasks):
        self.tasks = [Task(task) for task in tasks]
    
    def find_task_by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
