
# Persona
- World-class Python Developer
- Expert in debugging and creating unit tests

# Goal
- Debug the unit test failures for the object: `EditTodoTool`

# Python Source Code for the `EditTodoTool` object:
```py
import json


class EditTodoTool:
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
                    "task_id": {"type": "string"},
                    "new_task": {"type": "string"},
                    "action": {"type": "string", "enum": ["edit", "add_subtask"]}
                },
                "additionalProperties": False,
                "required": ["task_id", "new_task", "action"]
            }
        }

    def process_request(self, task_id, new_task, action):
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
        return f"Task updated: {task}"

# Unit Test for the tool: `EditTodoTool`
import unittest
from unittest.mock import MagicMock
from edit_todo_tool import EditTodoTool

class TestEditTodoTool(unittest.TestCase):

    def setUp(self):
        self.mock_storage_handler = MagicMock()
        self.mock_task_finder = MagicMock()
        self.mock_task_editor = MagicMock()
        self.mock_subtask_manager = MagicMock()

        self.todo_list = [{"id": "19", "task": "Buy groceries", "timestamp": "2024-09-08T12:00:00Z"}]
        self.mock_storage_handler.load.return_value = self.todo_list

        self.edit_todo_tool = EditTodoTool(
            storage_handler=self.mock_storage_handler,
            task_finder=self.mock_task_finder,
            task_editor=self.mock_task_editor,
            subtask_manager=self.mock_subtask_manager
        )

    def test_edit_existing_task(self):
        task_id = "19"
        new_task = "Buy more groceries"
        self.mock_task_finder.find_task.return_value = self.todo_list[0]

        result = self.edit_todo_tool.process_request(task_id, new_task, "edit")

        self.mock_task_editor.edit_task.assert_called_once_with(self.todo_list[0], new_task)
        self.mock_storage_handler.save.assert_called_once_with(self.todo_list)
        self.assertIn("Task updated", result)

    def test_add_subtask_to_existing_task(self):
        task_id = "19"
        new_task = "Buy milk"
        self.mock_task_finder.find_task.return_value = self.todo_list[0]

        result = self.edit_todo_tool.process_request(task_id, new_task, "add_subtask")

        self.mock_subtask_manager.add_subtask.assert_called_once_with(self.todo_list[0], task_id, new_task)
        self.mock_storage_handler.save.assert_called_once_with(self.todo_list)
        self.assertIn("Task updated", result)

    def test_task_not_found(self):
        task_id = "99"
        new_task = "This task does not exist"
        self.mock_task_finder.find_task.return_value = None

        result = self.edit_todo_tool.process_request(task_id, new_task, "edit")

        self.mock_task_editor.edit_task.assert_not_called()
        self.mock_subtask_manager.add_subtask.assert_not_called()
        self.mock_storage_handler.save.assert_not_called()
        self.assertEqual(result, f"Task with ID {task_id} not found.")

    def test_invalid_action(self):
        task_id = "19"
        new_task = "Buy more groceries"
        self.mock_task_finder.find_task.return_value = self.todo_list[0]

        result = self.edit_todo_tool.process_request(task_id, new_task, "invalid_action")

        self.mock_task_editor.edit_task.assert_not_called()
        self.mock_subtask_manager.add_subtask.assert_not_called()
        self.mock_storage_handler.save.assert_not_called()
        self.assertEqual(result, "Invalid action: invalid_action")

    def test_save_todo_list_after_edit(self):
        task_id = "19"
        new_task = "Buy more groceries"
        self.mock_task_finder.find_task.return_value = self.todo_list[0]

        self.edit_todo_tool.process_request(task_id, new_task, "edit")

        self.mock_storage_handler.save.assert_called_once_with(self.todo_list)

    def test_save_todo_list_after_add_subtask(self):
        task_id = "19"
        new_task = "Buy milk"
        self.mock_task_finder.find_task.return_value = self.todo_list[0]

        self.edit_todo_tool.process_request(task_id, new_task, "add_subtask")

        self.mock_storage_handler.save.assert_called_once_with(self.todo_list)



# Output from running the unit tests
```bash
......
----------------------------------------------------------------------
Ran 6 tests in 0.021s

OK

```

# Your Task
Rewrite the test file `test_edit_todo_tool.py` and/or the Python file `edit_todo_tool.py` to fix the unit test failures.
