
# Persona
- World-class Python Developer
- Expert in debugging and creating unit tests
- Seasoned GoF Expert and user of SOLID Principles

# Goal
- Debug the unit test failures and enhance the test coverage for the tool: `task_finder`

# Python Source Code for the tool: `task_finder`
```py
class TaskFinder:
    """Responsible for finding tasks within a todo list by ID."""

    @staticmethod
    def find_task(todo_list, task_id):
        parts = task_id.split('.')
        current_list = todo_list
        
        for part in parts:
            task_found = False
            for item in current_list:
                # Only consider the relevant part at each level
                if item.get("id") == part:
                    if part == parts[-1]:  # If it's the last part, return the item
                        return item
                    current_list = item.get("subtasks", [])
                    task_found = True
                    break
            if not task_found:
                return None
        return None


# Unit Test for the tool: `task_finder`
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


# Output from running the unit tests
```bash
...F.F
======================================================================
FAIL: test_find_subtask (test_task_finder.TestTaskFinder.test_find_subtask)
Test finding a subtask.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/eg1972/the_function_caller/todo_list_tools/task_finder/test_task_finder.py", line 45, in test_find_subtask
    self.assertIsNotNone(task)
AssertionError: unexpectedly None

======================================================================
FAIL: test_find_task_with_multiple_levels (test_task_finder.TestTaskFinder.test_find_task_with_multiple_levels)
Test finding a task with more than one subtask level.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/eg1972/the_function_caller/todo_list_tools/task_finder/test_task_finder.py", line 69, in test_find_task_with_multiple_levels
    self.assertEqual(task["id"], "1.a.1")
AssertionError: '1' != '1.a.1'
- 1
+ 1.a.1


----------------------------------------------------------------------
Ran 6 tests in 0.002s

FAILED (failures=2)

```

# Your Task
Rewrite the test file `test_task_finder.py` and/or the Python file `task_finder.py` to fix the unit test failures.
