import unittest
from unittest.mock import MagicMock

from add_todo_tool import AddTodoTool

class TestAddTodoTool(unittest.TestCase):

    def setUp(self):
        # Create a mock storage handler
        self.mock_storage_handler = MagicMock()
        
        # Example todo list to use in tests
        self.todo_list = [
            {"id": "1", "task": "Buy groceries", "timestamp": "2024-09-08T12:00:00Z"}
        ]
        
        # Mock the load method to return the predefined todo list
        self.mock_storage_handler.load.return_value = self.todo_list
        
        # Create an instance of AddTodoTool with the mock storage handler
        self.add_todo_tool = AddTodoTool(storage_handler=self.mock_storage_handler)

    def test_add_todo(self):
        # Add a new task
        new_task = "Buy milk"
        result = self.add_todo_tool.add_todo(new_task)

        # Check if the task was added correctly to the list
        self.assertEqual(len(self.add_todo_tool.todo_list), 2)
        self.assertEqual(self.add_todo_tool.todo_list[1]['task'], new_task)

        # Check if the save method was called once with the updated list
        self.mock_storage_handler.save.assert_called_once_with(self.add_todo_tool.todo_list)

        # Check the return message
        self.assertIn("Todo item added and saved", result)

if __name__ == "__main__":
    unittest.main()
