import unittest

import sys
import os

# Add the root directory of the project (two levels up from task_list)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# put the home directory (~) into a variable
# Add the parent directory of the current file (task_list) to the system path
sys.path.append( os.path.expanduser("~") + '/the_function_caller/todo_list_tools/' )
# Now you can import TaskList from task_list.py
# Assuming TaskList and Task are defined in a module named task_finder
from task_list import TaskList

class TestTaskList(unittest.TestCase):

    def setUp(self):
        """Sets up a common task list for testing."""
        self.todo_list = [
            {"id": "1", "subtasks": [{"id": "1.1"}, {"id": "1.2"}]},
            {"id": "2", "subtasks": []},
            {"id": "3"}
        ]
        self.task_list = TaskList(self.todo_list)
    
    def test_find_task_by_id_exists(self):
        """Test finding a task by ID when the task exists."""
        task = self.task_list.find_task_by_id("1")
        
        # Verify that the task is found
        self.assertIsNotNone(task)
        self.assertEqual(task.id, "1")
    
    def test_find_task_by_id_does_not_exist(self):
        """Test finding a task by ID when the task does not exist."""
        task = self.task_list.find_task_by_id("4")
        
        # Verify that the task is not found
        self.assertIsNone(task)

    def test_find_task_with_subtasks(self):
        """Test finding a task and its subtasks."""
        task = self.task_list.find_task_by_id("1")
        
        # Verify task has subtasks
        self.assertTrue(task.has_subtasks())
        self.assertEqual(len(task.subtasks), 2)
    
    def test_find_task_no_subtasks(self):
        """Test finding a task that has no subtasks."""
        task = self.task_list.find_task_by_id("2")
        
        # Verify task has no subtasks
        self.assertFalse(task.has_subtasks())

if __name__ == "__main__":
    unittest.main()
