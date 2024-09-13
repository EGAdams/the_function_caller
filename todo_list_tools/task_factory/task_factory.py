import sys
import os


# Dynamically add '~/the_function_caller/todo_list_tools' to sys.path
# project_root = os.path.expanduser('~/the_function_caller/todo_list_tools')
sys.path.append( '/home/eg1972/the_function_caller/todo_list_tools' )


from task_finder.task_list.task_list import TaskList


class TaskFactory:
    """Factory for creating Task objects."""
    
    @staticmethod
    def create_task_list(todo_list):
        return TaskList(todo_list)
    