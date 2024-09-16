import sys
import os

# Add the parent directory of the current file ( task_list) to the system path
sys.path.append( '/home/adamsl/the_function_caller/todo_list_tools/' )

# Now you can import TaskList from task_list.py and Task from task.py
from task_finder.task_iterator.task_iterator import TaskIterator
from task_factory.task_factory   import TaskFactory

class TaskFinder:
    """Responsible for finding tasks within a todo list by ID."""

    @staticmethod
    def find_task( todo_list, task_id ):
        task_list = TaskFactory.create_task_list( todo_list )
        task_iterator = TaskIterator( task_list, task_id )
        return task_iterator.iterate()
