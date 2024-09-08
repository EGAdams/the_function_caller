import unittest
from unittest.mock import MagicMock

from remove_todo_tool import RemoveTodoTool

class TestRemoveTodoTool(unittest.TestCase):

    def setUp(self):
        # Create a mock storage handler
        self.mock_storage_handler = MagicMock()
        
        # Example todo list to use in tests
        self.todo_list = [
            {"id": "1", "task": "Buy groceries", "timestamp": "2024-09-08T12:00:00Z"},
            {"id": "2", "task": "Do laundry", "timestamp": "2024-09-08T13:00:00Z"}
        ]
        
        # Mock the load method to return the predefined todo list
        self.mock_storage_handler.load.return_value = self.todo_list
        
        # Create an instance of RemoveTodoTool with the mock storage handler
        self.remove_todo_tool = RemoveTodoTool(storage_handler=self.mock_storage_handler)

    def test_remove_existing_todo(self):
        # Remove an existing task
        task_id = "1"
        result = self.remove_todo_tool.remove_todo(task_id)

        # Check if the task was removed from the list
        self.assertEqual(len(self.remove_todo_tool.todo_list), 1)
        self.assertNotIn({"id": "1", "task": "Buy groceries", "timestamp": "2024-09-08T12:00:00Z"}, self.remove_todo_tool.todo_list)

        # Check if the save method was called once with the updated list
        self.mock_storage_handler.save.assert_called_once_with(self.remove_todo_tool.todo_list)

        # Check the return message
        self.assertIn("Todo item removed and file updated", result)

    def test_remove_non_existing_todo(self):
        # Attempt to remove a non-existing task
        task_id = "99"
        result = self.remove_todo_tool.remove_todo(task_id)

        # Ensure the todo list remains unchanged
        self.assertEqual(len(self.remove_todo_tool.todo_list), 2)

        # Ensure save was not called
        self.mock_storage_handler.save.assert_not_called()

        # Check the return message
        self.assertIn("Todo item not found", result)

# Run the tests
if __name__ == "__main__":
    unittest.main()
