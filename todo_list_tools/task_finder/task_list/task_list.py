import sys
import os

# Add the parent directory of the current file (task_list) to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now you can import TaskList from task_list.py and Task from task.py
from task.task import Task


class TaskList:
    """Manages a list of tasks and subtasks."""
    
    def __init__(self, tasks):
        self.tasks = [Task(task) for task in tasks]
    
    def find_task_by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
