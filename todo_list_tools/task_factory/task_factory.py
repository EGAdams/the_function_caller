import sys
import os

# Add the parent directory of the current file (task_list) to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now you can import TaskList from task_list.py and Task from task.py
from task_list.task_list import TaskList

class TaskFactory:
    """Factory for creating Task objects."""
    
    @staticmethod
    def create_task_list(todo_list):
        return TaskList(todo_list)
    