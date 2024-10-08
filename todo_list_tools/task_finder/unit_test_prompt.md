
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

```
# Unit Test for the tool: `TaskFinder`
```python
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

# Linux `tree` output to help you fix the module not found errors
```bash
adamsl@DESKTOP-2OBSQMC:~/the_function_caller/todo_list_tools$ tree
.
├── __pycache__
│   ├── __init__.cpython-312.pyc
│   ├── test_edit_todo_tool.cpython-312.pyc
│   └── test_remove_todo_tool.cpython-312.pyc
├── add_todo_tool
│   ├── __pycache__
│   │   └── test_add_todo_tool.cpython-312.pyc
│   ├── add_todo_tool.py
│   └── test_add_todo_tool.py
├── all_classes.md
├── edit_todo_tool
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   ├── edit_todo_tool.cpython-312.pyc
│   │   └── test_edit_todo_tool.cpython-312.pyc
│   ├── edit_todo_tool.py
│   ├── fix_unit_tests.py
│   ├── test_edit_todo_tool.py
│   └── unit_test_prompt.md
├── find_python_classes.py
├── fix_module_path.py
├── fix_unit_tests.py
├── prompts
│   ├── break_edit_tool_into_smaller_objects.md
│   ├── complete_todo_instructions.md
│   ├── corrected_prompt_template.md
│   ├── fix_unit_tests.md
│   ├── new_prompt.md
│   └── unit_test_prompt.md
├── pull_prompt_break_object.py
├── pull_prompt_from_file.py
├── read_todo_tool.py
├── remove_todo_tool
│   ├── __pycache__
│   │   ├── remove_todo_tool.cpython-312.pyc
│   │   └── test_remove_todo_tool.cpython-312.pyc
│   ├── remove_todo_tool.py
│   └── test_remove_todo_tool.py
├── run_all_tests.py
├── storage_handler
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   ├── storage_handler.cpython-312.pyc
│   │   └── test_storage_handler.cpython-312.pyc
│   ├── storage_handler.py
│   └── test_storage_handler.py
├── task
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   ├── task.cpython-312.pyc
│   │   └── test_task.cpython-312.pyc
│   ├── fix_unit_tests.py
│   ├── task.py
│   ├── test_task.py
│   └── unit_test_prompt.md
├── task_editor
│   ├── __pycache__
│   │   └── task_editor.cpython-312.pyc
│   └── task_editor.py
├── task_factory
│   ├── __init__.py
│   ├── __pycache__
│   │   └── task_factory.cpython-312.pyc
│   └── task_factory.py
├── task_finder
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   ├── task_finder.cpython-312.pyc
│   │   └── test_task_finder.cpython-312.pyc
│   ├── class.md
│   ├── fix_unit_tests.py
│   ├── run_all_tests.py
│   ├── sequence.md
│   ├── simplify_moduraly.md
│   ├── task_finder.py
│   ├── task_iterator
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── task_iterator.cpython-312.pyc
│   │   │   └── test_task_iterator.cpython-312.pyc
│   │   ├── fix_unit_tests.py
│   │   ├── task_iterator.py
│   │   └── test_task_iterator.py
│   ├── task_list
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── task_list.cpython-312.pyc
│   │   │   └── test_task_list.cpython-312.pyc
│   │   ├── task_list.py
│   │   └── test_task_list.py
│   ├── test_task_finder.py
│   └── unit_test_prompt.md
└── todo_list_tool.py

23 directories, 77 files
adamsl@DESKTOP-2OBSQMC:~/the_function_caller/todo_list_tools$
```

# Your Task
Focus on fixing the "No module named" errors.  Use the output from the `tree` command to help you fix the module not found errors.
I only want you to fix the errors that are caused by the module not found errors.  Do not fix any other errors.
