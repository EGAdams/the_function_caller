
# Persona
- World-class Python Developer
- Expert in debugging and creating unit tests

# Goal
- Debug the unit test failures for the object: `TaskFinder`

# Python Source Code for the `TaskFinder` object:
```py
import sys
import os

# Add the parent directory of the current file (task_list) to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now you can import TaskList from task_list.py and Task from task.py
from task_iterator.task_iterator import TaskIterator
from task_factory.task_factory import TaskFactory

class TaskFinder:
    """Responsible for finding tasks within a todo list by ID."""
    
    @staticmethod
    def find_task(todo_list, task_id):
        task_list = TaskFactory.create_task_list(todo_list)
        task_iterator = TaskIterator(task_list, task_id)
        return task_iterator.iterate()


# Unit Test for the tool: `TaskFinder`
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
        self.assertEqual(task.get_id(), "1")
        self.assertEqual(task.get_task(), "Root Task 1")

    def test_find_subtask(self):
        """Test finding a subtask."""
        task = TaskFinder.find_task(self.todo_list, "1.a")
        self.assertIsNotNone(task)
        self.assertEqual(task.get_id(), "1.a")
        self.assertEqual(task.get_task(), "Subtask 1.a")
    
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
        self.assertEqual(task.get_id(), "1.a.1")
        self.assertEqual(task.get_task(), "Subtask 1.a.1")
    
    def test_find_subtask_with_multiple_levels_missing(self):
        """Test finding a subtask with multiple levels that does not exist."""
        task = TaskFinder.find_task(self.todo_list, "2.b.1")
        self.assertIsNone(task)

if __name__ == '__main__':
    unittest.main()


# Output from running the unit tests
```bash
......
----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK

```

# Your Task
Rewrite the test file `test_task_finder.py` and/or the Python file `task_finder.py` to fix the unit test failures.
