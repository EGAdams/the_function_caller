import unittest
from unittest.mock import MagicMock
from datetime import datetime
from todo_list_tools.add_todo_subtask_tool.add_todo_subtask_tool import EditTodoTool


class TestEditTodoTool(unittest.TestCase):

    def setUp(self):
        # Mocking the components
        self.mock_storage_handler = MagicMock()
        self.mock_task_finder = MagicMock()
        self.mock_task_editor = MagicMock()
        self.mock_subtask_manager = MagicMock()

        # Setting up the sample todo list
        self.todo_list = [
            {
                "id": "19",
                "task": "Buy groceries",
                "timestamp": "2024-09-08T12:00:00Z"
            },
            {
                "id": "2",
                "task": "Sample task 2",
                "timestamp": datetime.now().isoformat(),
                "subtasks": [
                    {
                        "id": "2.a",
                        "task": "Subtask 2.a",
                        "timestamp": datetime.now().isoformat()
                    }
                ]
            }
        ]
        self.mock_storage_handler.load.return_value = self.todo_list

        self.edit_todo_tool = EditTodoTool(
            storage_handler=self.mock_storage_handler,
            task_finder=self.mock_task_finder,
            task_editor=self.mock_task_editor,
            subtask_manager=self.mock_subtask_manager
        )

    # Test for editing an existing task
    def test_edit_existing_task(self):
        task_id = "19"
        new_task = "Buy more groceries"
        self.mock_task_finder.find_task.return_value = self.todo_list[0]

        result = self.edit_todo_tool.process_request(task_id, new_task, "edit")

        self.mock_task_editor.edit_task.assert_called_once_with(self.todo_list[0], new_task)
        self.mock_storage_handler.save.assert_called_once_with(self.todo_list)
        self.assertIn("Task updated", result)

    # Test for adding a subtask to an existing task
    def test_add_subtask_to_existing_task(self):
        task_id = "19"
        new_task = "Buy milk"
        self.mock_task_finder.find_task.return_value = self.todo_list[0]

        result = self.edit_todo_tool.process_request(task_id, new_task, "add_subtask")

        self.mock_subtask_manager.add_subtask.assert_called_once_with(self.todo_list[0], task_id, new_task)
        self.mock_storage_handler.save.assert_called_once_with(self.todo_list)
        self.assertIn("Task updated", result)

    # Test when a task is not found
    def test_task_not_found(self):
        task_id = "99"
        new_task = "This task does not exist"
        self.mock_task_finder.find_task.return_value = None

        result = self.edit_todo_tool.process_request(task_id, new_task, "edit")

        self.mock_task_editor.edit_task.assert_not_called()
        self.mock_subtask_manager.add_subtask.assert_not_called()
        self.mock_storage_handler.save.assert_not_called()
        self.assertEqual(result, f"Task with ID {task_id} not found.")

    # Test for invalid action
    def test_invalid_action(self):
        task_id = "19"
        new_task = "Buy more groceries"
        self.mock_task_finder.find_task.return_value = self.todo_list[0]

        result = self.edit_todo_tool.process_request(task_id, new_task, "invalid_action")

        self.mock_task_editor.edit_task.assert_not_called()
        self.mock_subtask_manager.add_subtask.assert_not_called()
        self.mock_storage_handler.save.assert_not_called()
        self.assertEqual(result, "Invalid action: invalid_action")

    # Test for saving the todo list after an edit
    def test_save_todo_list_after_edit(self):
        task_id = "19"
        new_task = "Buy more groceries"
        self.mock_task_finder.find_task.return_value = self.todo_list[0]

        self.edit_todo_tool.process_request(task_id, new_task, "edit")

        self.mock_storage_handler.save.assert_called_once_with(self.todo_list)

    # Test for saving the todo list after adding a subtask
    def test_save_todo_list_after_add_subtask(self):
        task_id = "19"
        new_task = "Buy milk"
        self.mock_task_finder.find_task.return_value = self.todo_list[0]

        self.edit_todo_tool.process_request(task_id, new_task, "add_subtask")

        self.mock_storage_handler.save.assert_called_once_with(self.todo_list)

    # Additional test for schema validation
    def test_schema(self):
        schema = self.edit_todo_tool.schema()
        self.assertIsInstance(schema, dict)
        self.assertEqual(schema["name"], "edit_todo")
        self.assertTrue(schema["strict"])
        self.assertIn("task_id", schema["parameters"]["properties"])
        self.assertIn("new_task", schema["parameters"]["properties"])
        self.assertIn("action", schema["parameters"]["properties"])

if __name__ == '__main__':
    unittest.main()
