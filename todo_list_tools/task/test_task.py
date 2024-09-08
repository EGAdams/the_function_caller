import unittest

# Assuming Task is defined in a module named task_finder
from task import Task

class TestTask(unittest.TestCase):
    
    def test_task_initialization(self):
        """Test that a Task object is initialized correctly."""
        task_data = {
            "id": "1",
            "subtasks": [{"id": "1.1"}, {"id": "1.2"}]
        }
        task = Task(task_data)
        
        # Verify task ID
        self.assertEqual(task.id, "1")
        
        # Verify subtasks
        self.assertEqual(len(task.subtasks), 2)
        self.assertEqual(task.subtasks[0].id, "1.1")
        self.assertEqual(task.subtasks[1].id, "1.2")

    def test_task_no_subtasks(self):
        """Test a Task object with no subtasks."""
        task_data = {
            "id": "2"
        }
        task = Task(task_data)
        
        # Verify task ID
        self.assertEqual(task.id, "2")
        
        # Verify there are no subtasks
        self.assertFalse(task.has_subtasks())

    def test_task_with_subtasks(self):
        """Test a Task object with subtasks."""
        task_data = {
            "id": "3",
            "subtasks": [{"id": "3.1"}]
        }
        task = Task(task_data)
        
        # Verify task has subtasks
        self.assertTrue(task.has_subtasks())
        self.assertEqual(len(task.subtasks), 1)
        self.assertEqual(task.subtasks[0].id, "3.1")
        
if __name__ == "__main__":
    unittest.main()
