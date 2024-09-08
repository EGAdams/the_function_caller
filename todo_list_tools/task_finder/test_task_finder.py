import unittest
from task_finder import TaskFinder

class TestTaskFinder(unittest.TestCase):

    def setUp(self):
        """Sets up a sample todo list with tasks and subtasks."""
        self.todo_list = [
            {
                "id": "1",
                "task": "Root Task 1",
                "subtasks": [
                    {
                        "id": "1.a",
                        "task": "Subtask 1.a"
                    },
                    {
                        "id": "1.b",
                        "task": "Subtask 1.b"
                    }
                ]
            },
            {
                "id": "2",
                "task": "Root Task 2",
                "subtasks": [
                    {
                        "id": "2.a",
                        "task": "Subtask 2.a"
                    }
                ]
            }
        ]
    
    def test_find_root_task(self):
        """Test finding a root-level task."""
        task = TaskFinder.find_task(self.todo_list, "1")
        self.assertIsNotNone(task)
        self.assertEqual(task["id"], "1")
        self.assertEqual(task["task"], "Root Task 1")

    def test_find_subtask(self):
        """Test finding a subtask."""
        task = TaskFinder.find_task(self.todo_list, "1.a")
        self.assertIsNotNone(task)
        self.assertEqual(task["id"], "1.a")
        self.assertEqual(task["task"], "Subtask 1.a")
    
    def test_find_non_existent_task(self):
        """Test finding a non-existent task."""
        task = TaskFinder.find_task(self.todo_list, "3")
        self.assertIsNone(task)

    def test_find_non_existent_subtask(self):
        """Test finding a non-existent subtask."""
        task = TaskFinder.find_task(self.todo_list, "1.c")
        self.assertIsNone(task)
    
    def test_find_task_with_multiple_levels(self):
        """Test finding a task with more than one subtask level."""
        self.todo_list[0]["subtasks"][0]["subtasks"] = [
            {
                "id": "1.a.1",
                "task": "Subtask 1.a.1"
            }
        ]
        task = TaskFinder.find_task(self.todo_list, "1.a.1")
        self.assertIsNotNone(task)
        self.assertEqual(task["id"], "1.a.1")
        self.assertEqual(task["task"], "Subtask 1.a.1")
    
    def test_find_subtask_with_multiple_levels_missing(self):
        """Test finding a subtask with multiple levels that does not exist."""
        task = TaskFinder.find_task(self.todo_list, "2.b.1")
        self.assertIsNone(task)

if __name__ == '__main__':
    unittest.main()
