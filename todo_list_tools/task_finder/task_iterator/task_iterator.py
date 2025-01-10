import sys
import os
home_directory = os.path.expanduser("~")
sys.path.append( home_directory + '/the_function_caller/todo_list_tools' )

class TaskIterator:
    """Iterates through the tasks based on task ID parts."""
    
    def __init__( self, task_list, task_id ):
        self.task_list = task_list
        self.task_id = task_id
    
    def iterate( self ):
        current_tasks = self.task_list.tasks
        for task in current_tasks:
            result = task.find_task_by_id( self.task_id )
            if result:
                return result
        return None
