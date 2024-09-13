import unittest
import sys
import os

# Add the parent directory of the current file (task_list) to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import unittest
from task_list.task_list import TaskList
from task_iterator import TaskIterator

class TaskIteratorTest(unittest.TestCase):
    
    def setUp(self):
        """Set up a mock TaskList for testing."""
        # Mock task list that accurately reflects tasks with subtasks
        self.todo_list = [
            {"id": "1", "subtasks": [
                {"id": "1.1", "subtasks": [
                    {"id": "1.1.1", "subtasks": []}
                ]},
                {"id": "1.2", "subtasks": []}
            ]},
            {"id": "2", "subtasks": []}
        ]
    
    def test_iterate_finds_task(self):
        """Test that TaskIterator correctly finds a task based on task_id."""
        task_list = TaskList(self.todo_list)
        task_iterator = TaskIterator(task_list, "1.1.1")
        
        task = task_iterator.iterate()
        
        self.assertIsNotNone(task)
        self.assertEqual(task.id, "1.1.1")
    
    def test_iterate_returns_none_for_invalid_task_id(self):
        """Test that TaskIterator returns None for an invalid task_id."""
        task_list = TaskList(self.todo_list)
        task_iterator = TaskIterator(task_list, "1.3")  # Non-existent task
        
        task = task_iterator.iterate()
        
        self.assertIsNone(task)
    
    def test_iterate_finds_task_with_no_subtasks(self):
        """Test that TaskIterator correctly finds a task with no subtasks."""
        task_list = TaskList(self.todo_list)
        task_iterator = TaskIterator(task_list, "1.2")  # No subtasks
        
        task = task_iterator.iterate()
        
        self.assertIsNotNone(task)
        self.assertEqual(task.id, "1.2")

    def test_iterate_finds_top_level_task(self):
        """Test that TaskIterator finds a top-level task."""
        task_list = TaskList(self.todo_list)
        task_iterator = TaskIterator(task_list, "2")  # Top-level task
        
        task = task_iterator.iterate()
        
        self.assertIsNotNone(task)
        self.assertEqual(task.id, "2")


if __name__ == '__main__':
    unittest.main()
