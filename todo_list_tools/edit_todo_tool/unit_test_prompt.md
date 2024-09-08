
# Persona
- World-class Python Developer
- Expert in debugging and creating unit tests

# Goal
- Debug the unit test failures for the object: `EditTodoTool`

# Python Source Code for the `EditTodoTool` object:
```py
import json


class EditTodoTool:
    """
    Coordinates the editing of todo items and adding subtasks.
    """

    def __init__(self, storage_handler, task_finder, task_editor, subtask_manager):
        self.storage_handler = storage_handler
        self.task_finder = task_finder
        self.task_editor = task_editor
        self.subtask_manager = subtask_manager
        self.todo_list = self.storage_handler.load()

    @staticmethod
    def schema():
        return {
            "name": "edit_todo",
            "description": "Edit a todo item or add a subtask",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to edit (e.g., '19' or '19.b')"
                    },
                    "new_task": {
                        "type": "string",
                        "description": "The new task description or subtask to add"
                    },
                    "action": {
                        "type": "string",
                        "enum": ["edit", "add_subtask"],
                        "description": "Whether to edit the existing task or add a subtask"
                    }
                },
                "additionalProperties": False,
                "required": ["task_id", "new_task", "action"]
            }
        }

    def process_request(self, task_id, new_task, action):
        """Edits a todo item or adds a subtask."""
        task = self.task_finder.find_task(self.todo_list, task_id)
        if task is None:
            return f"Task with ID {task_id} not found."

        if action == "edit":
            self.task_editor.edit_task(task, new_task)
        elif action == "add_subtask":
            self.subtask_manager.add_subtask(task, task_id, new_task)
        else:
            return f"Invalid action: {action}"
        
        self.storage_handler.save(self.todo_list)
        return f"Task updated: {json.dumps(task)}"


# Unit Test for the tool: `EditTodoTool`
import unittest
from unittest.mock import MagicMock
from edit_todo_tool import EditTodoTool

class TestEditTodoTool(unittest.TestCase):

    def setUp(self):
        # Create mock objects for dependencies
        self.mock_storage_handler = MagicMock()
        self.mock_task_finder = MagicMock()
        self.mock_task_editor = MagicMock()
        self.mock_subtask_manager = MagicMock()

        # Create an instance of EditTodoTool with mock dependencies
        self.edit_todo_tool = EditTodoTool(
            storage_handler=self.mock_storage_handler,
            task_finder=self.mock_task_finder,
            task_editor=self.mock_task_editor,
            subtask_manager=self.mock_subtask_manager
        )

        # Example todo list to use in tests
        self.todo_list = [
            {"id": "19", "task": "Buy groceries", "timestamp": "2024-09-08T12:00:00Z"}
        ]
        self.mock_storage_handler.load.return_value = self.todo_list

    def test_edit_existing_task(self):
        # Mock finding the task
        task_id = "19"
        new_task = "Buy more groceries"
        self.mock_task_finder.find_task.return_value = self.todo_list[0]

        # Call the process_request method with action 'edit'
        result = self.edit_todo_tool.process_request(task_id, new_task, "edit")

        # Assert that TaskEditor.edit_task was called with the correct task and new_task
        self.mock_task_editor.edit_task.assert_called_once_with(self.todo_list[0], new_task)
        
        # Assert that the updated todo list was saved
        self.mock_storage_handler.save.assert_called_once_with(self.todo_list)

        # Assert the returned message
        self.assertIn("Task updated", result)

    def test_add_subtask_to_existing_task(self):
        # Mock finding the task
        task_id = "19"
        new_task = "Buy milk"
        self.mock_task_finder.find_task.return_value = self.todo_list[0]

        # Call the process_request method with action 'add_subtask'
        result = self.edit_todo_tool.process_request(task_id, new_task, "add_subtask")

        # Assert that SubtaskManager.add_subtask was called with the correct task, task_id, and new_task
        self.mock_subtask_manager.add_subtask.assert_called_once_with(self.todo_list[0], task_id, new_task)
        
        # Assert that the updated todo list was saved
        self.mock_storage_handler.save.assert_called_once_with(self.todo_list)

        # Assert the returned message
        self.assertIn("Task updated", result)

    def test_task_not_found(self):
        # Mock the task finder to return None (task not found)
        task_id = "99"
        new_task = "This task does not exist"
        self.mock_task_finder.find_task.return_value = None

        # Call the process_request method
        result = self.edit_todo_tool.process_request(task_id, new_task, "edit")

        # Assert that the TaskEditor.edit_task was never called
        self.mock_task_editor.edit_task.assert_not_called()

        # Assert that SubtaskManager.add_subtask was never called
        self.mock_subtask_manager.add_subtask.assert_not_called()

        # Assert that the storage handler save was never called
        self.mock_storage_handler.save.assert_not_called()

        # Assert the returned message
        self.assertEqual(result, f"Task with ID {task_id} not found.")

    def test_invalid_action(self):
        # Mock finding the task
        task_id = "19"
        new_task = "Buy more groceries"
        self.mock_task_finder.find_task.return_value = self.todo_list[0]

        # Call the process_request method with an invalid action
        result = self.edit_todo_tool.process_request(task_id, new_task, "invalid_action")

        # Assert that TaskEditor and SubtaskManager were not called
        self.mock_task_editor.edit_task.assert_not_called()
        self.mock_subtask_manager.add_subtask.assert_not_called()

        # Assert that the storage handler save was never called
        self.mock_storage_handler.save.assert_not_called()

        # Assert the returned message
        self.assertEqual(result, "Invalid action: invalid_action")

    def test_save_todo_list_after_edit(self):
        # Mock finding the task
        task_id = "19"
        new_task = "Buy more groceries"
        self.mock_task_finder.find_task.return_value = self.todo_list[0]

        # Call the process_request method with action 'edit'
        self.edit_todo_tool.process_request(task_id, new_task, "edit")

        # Assert that the todo list was saved
        self.mock_storage_handler.save.assert_called_once_with(self.todo_list)

    def test_save_todo_list_after_add_subtask(self):
        # Mock finding the task
        task_id = "19"
        new_task = "Buy milk"
        self.mock_task_finder.find_task.return_value = self.todo_list[0]

        # Call the process_request method with action 'add_subtask'
        self.edit_todo_tool.process_request(task_id, new_task, "add_subtask")

        # Assert that the todo list was saved
        self.mock_storage_handler.save.assert_called_once_with(self.todo_list)

if __name__ == "__main__":
    unittest.main()


# Output from running the unit tests
```bash
FF.FF.
======================================================================
FAIL: test_add_subtask_to_existing_task (test_edit_todo_tool.TestEditTodoTool.test_add_subtask_to_existing_task)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/eg1972/the_function_caller/todo_list_tools/edit_todo_tool/test_edit_todo_tool.py", line 59, in test_add_subtask_to_existing_task
    self.mock_storage_handler.save.assert_called_once_with(self.todo_list)
  File "/usr/lib/python3.11/unittest/mock.py", line 945, in assert_called_once_with
    return self.assert_called_with(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/unittest/mock.py", line 933, in assert_called_with
    raise AssertionError(_error_message()) from cause
AssertionError: expected call not found.
Expected: save([{'id': '19', 'task': 'Buy groceries', 'timestamp': '2024-09-08T12:00:00Z'}])
Actual: save(<MagicMock name='mock.load()' id='139766592168656'>)

======================================================================
FAIL: test_edit_existing_task (test_edit_todo_tool.TestEditTodoTool.test_edit_existing_task)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/eg1972/the_function_caller/todo_list_tools/edit_todo_tool/test_edit_todo_tool.py", line 41, in test_edit_existing_task
    self.mock_storage_handler.save.assert_called_once_with(self.todo_list)
  File "/usr/lib/python3.11/unittest/mock.py", line 945, in assert_called_once_with
    return self.assert_called_with(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/unittest/mock.py", line 933, in assert_called_with
    raise AssertionError(_error_message()) from cause
AssertionError: expected call not found.
Expected: save([{'id': '19', 'task': 'Buy groceries', 'timestamp': '2024-09-08T12:00:00Z'}])
Actual: save(<MagicMock name='mock.load()' id='139766590475152'>)

======================================================================
FAIL: test_save_todo_list_after_add_subtask (test_edit_todo_tool.TestEditTodoTool.test_save_todo_list_after_add_subtask)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/eg1972/the_function_caller/todo_list_tools/edit_todo_tool/test_edit_todo_tool.py", line 126, in test_save_todo_list_after_add_subtask
    self.mock_storage_handler.save.assert_called_once_with(self.todo_list)
  File "/usr/lib/python3.11/unittest/mock.py", line 945, in assert_called_once_with
    return self.assert_called_with(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/unittest/mock.py", line 933, in assert_called_with
    raise AssertionError(_error_message()) from cause
AssertionError: expected call not found.
Expected: save([{'id': '19', 'task': 'Buy groceries', 'timestamp': '2024-09-08T12:00:00Z'}])
Actual: save(<MagicMock name='mock.load()' id='139766590640400'>)

======================================================================
FAIL: test_save_todo_list_after_edit (test_edit_todo_tool.TestEditTodoTool.test_save_todo_list_after_edit)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/eg1972/the_function_caller/todo_list_tools/edit_todo_tool/test_edit_todo_tool.py", line 114, in test_save_todo_list_after_edit
    self.mock_storage_handler.save.assert_called_once_with(self.todo_list)
  File "/usr/lib/python3.11/unittest/mock.py", line 945, in assert_called_once_with
    return self.assert_called_with(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/unittest/mock.py", line 933, in assert_called_with
    raise AssertionError(_error_message()) from cause
AssertionError: expected call not found.
Expected: save([{'id': '19', 'task': 'Buy groceries', 'timestamp': '2024-09-08T12:00:00Z'}])
Actual: save(<MagicMock name='mock.load()' id='139766590735696'>)

----------------------------------------------------------------------
Ran 6 tests in 0.031s

FAILED (failures=4)

```

# Your Task
Rewrite the test file `test_edit_todo_tool.py` and/or the Python file `edit_todo_tool.py` to fix the unit test failures.
