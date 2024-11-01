import json
from datetime import datetime

# Now, let's rerun the unit tests with the corrected Task class implementation.

# Redefine the Task class
# Define the Task class
class Task:
    """Represents a task with optional subtasks."""
    
    def __init__(self, task_dict):
        # Ensure task_dict is a dictionary
        if isinstance(task_dict, dict):
            self.id = task_dict.get('id')
            self.task = task_dict.get('task')
            self.subtasks = [Task(subtask) for subtask in task_dict.get('subtasks', [])]
        else:
            raise ValueError("task_dict must be a dictionary")

    def find_task_by_id(self, task_id):
        if self.id == task_id:
            return self
        for subtask in self.subtasks:
            result = subtask.find_task_by_id(task_id)
            if result:
                return result
        return None

    def has_subtasks(self):
        """Return True if the task has subtasks."""
        return len(self.subtasks) > 0
    
    def get_id(self):
        """Return the task's ID."""
        return self.id

    def get_task(self):
        """Return the task description."""
        return self.task

def add_subtask(self, subtask):
    """Add a new subtask to this task."""
    if not isinstance(subtask, Task):
        raise TypeError("subtask must be a Task object")
    self.subtasks.append(subtask)
    return self

def update_task(self, new_task_description):
    """Update the task description."""
    self.task = new_task_description
    return self

def to_dict(self):
    """Convert Task object to dictionary representation."""
    return {
        "id": self.id,
        "task": self.task,
        "subtasks": [subtask.to_dict() for subtask in self.subtasks]
    }

def remove_subtask(self, task_id):
    """Remove a subtask by its ID."""
    for i, subtask in enumerate(self.subtasks):
        if subtask.get_id() == task_id:
            return self.subtasks.pop(i)
        
    return None

def get_subtasks(self):
    """Return the list of subtasks."""
    return self.subtasks

def set_id(self, new_id):
    """Set a new ID for the task."""
    self.id = new_id
    return self
