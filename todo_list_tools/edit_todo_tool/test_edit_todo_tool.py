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


if __name__ == "__main__":
    unittest.main()
    