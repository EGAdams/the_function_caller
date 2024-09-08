import sys
import os

# Add the parent directory of the current file (task_list) to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now you can import TaskList from task_list.py and Task from task.py
from task_list.task_list import TaskList  # This works after modifying sys.path


from task_list.task_list import TaskList

class TaskIterator:
    """Iterates through the tasks based on task ID parts."""
    
    def __init__(self, task_list, task_id):
        self.task_list = task_list
        self.parts = task_id.split('.')
    
    def iterate(self):
        current_list = self.task_list
        for idx, part in enumerate(self.parts):
            task = current_list.find_task_by_id(part)
            if task is None:
                return None
            # Check if it's the last part of the task_id
            if idx == len(self.parts) - 1:  
                return task
            # Move to the subtasks of the current task
            current_list = TaskList(task.subtasks) if task.subtasks else None
            if current_list is None:
                return None
        return None
