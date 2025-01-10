import sys
import os

# Add the parent directory of the current file ( task_list) to the system path
home_directory = os.path.expanduser("~")
sys.path.append( home_directory + '/the_function_caller/todo_list_tools' )

# Now you can import TaskList from task_list.py and Task from task.py
from task_finder.task_iterator.task_iterator import TaskIterator
from task_factory.task_factory   import TaskFactory

class TaskFinder:
    """
    Finds a task within a todo list by its ID.
    
    Args:
        todo_list (TaskList): The todo list to search.
        task_id (str): The ID of the task to find.
    
    Returns:
        Task: The task with the specified ID, or None if not found.
    """

    @staticmethod
    def find_task(todo_list, task_id):
        for task in todo_list:
            result = task.find_task_by_id(task_id)
            if result:
                return result
        return None

