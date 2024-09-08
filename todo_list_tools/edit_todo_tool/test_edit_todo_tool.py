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
