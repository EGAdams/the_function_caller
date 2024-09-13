import sys
import os

# Add the parent directory of the current file (task_list) to the system path
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append( '/home/eg1972/the_function_caller/todo_list_tools' )

# Now you can import TaskList from task_list.py and Task from task.py
# from task_list.task_list import TaskList

# Redefine the TaskIterator with the new logic to match the full task ID
class TaskIterator:
    """Iterates through the tasks based on task ID parts."""
    
    def __init__(self, task_list, task_id):
        self.task_list = task_list
        self.task_id = task_id
    
    def iterate(self):
        current_tasks = self.task_list.tasks
        for task in current_tasks:
            result = task.find_task_by_id(self.task_id)
            if result:
                return result
        return None

# Rerun the tests with the new logic
# unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TaskIteratorTest))

