import json
from datetime import datetime

class Task:
    """Represents an individual task."""

    def __init__(self, task_data):
        self.id = task_data.get("id")
        self.subtasks = task_data.get("subtasks", [])
    
    def has_subtasks(self):
        return bool(self.subtasks)





class TaskFactory:
    """Factory for creating Task objects."""
    
    @staticmethod
    def create_task_list(todo_list):
        return TaskList(todo_list)


class TaskFinder:
    """Responsible for finding tasks within a todo list by ID."""
    
    @staticmethod
    def find_task(todo_list, task_id):
        task_list = TaskFactory.create_task_list(todo_list)
        task_iterator = TaskIterator(task_list, task_id)
        return task_iterator.iterate()
