import unittest
import json
import tempfile
import os
from unittest.mock import MagicMock
from todo_list_tools.remove_todo_tool.remove_todo_tool import RemoveTodoTool


class TestRemoveTodoTool(unittest.TestCase):
    
    # Test setup using mock storage handler
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, "test_todo_list.json")
        
        # Example todo list to use in both mock and file tests
        self.initial_todo_list = [
            {"id": "1", "task": "Buy groceries", "timestamp": "2024-09-08T12:00:00Z"},
            {"id": "2", "task": "Do laundry", "timestamp": "2024-09-08T13:00:00Z", "subtasks": [
                {"id": "2.1", "task": "Subtask 2.1"},
                {"id": "2.2", "task": "Subtask 2.2"}
            ]}
        ]
        
        with open(self.filename, 'w') as f:
            json.dump(self.initial_todo_list, f)
        
        # Create a mock storage handler
        self.mock_storage_handler = MagicMock()
        self.mock_storage_handler.load.return_value = self.initial_todo_list
        
        # Initialize RemoveTodoTool with file and mock storage handler
        self.remove_todo_tool_file = RemoveTodoTool(self.filename)
        self.remove_todo_tool_mock = RemoveTodoTool(storage_handler=self.mock_storage_handler)

    def tearDown(self):
        os.remove(self.filename)
        os.rmdir(self.temp_dir)

    # Test with mock storage handler

    def test_remove_existing_todo_mock(self):
        task_id = "1"
        result = self.remove_todo_tool_mock.remove_todo(task_id)

        # Check if the task was removed from the list
        self.assertEqual(len(self.remove_todo_tool_mock.todo_list), 1)
        self.assertNotIn({"id": "1", "task": "Buy groceries", "timestamp": "2024-09-08T12:00:00Z"}, self.remove_todo_tool_mock.todo_list)

        # Check if save was called
        self.mock_storage_handler.save.assert_called_once_with(self.remove_todo_tool_mock.todo_list)
        self.assertIn("Todo item removed", result)

    def test_remove_non_existing_todo_mock(self):
        task_id = "99"
        result = self.remove_todo_tool_mock.remove_todo(task_id)

        self.assertEqual(len(self.remove_todo_tool_mock.todo_list), 2)
        self.mock_storage_handler.save.assert_not_called()
        self.assertIn("Todo item not found", result)

    # File-based persistence tests

    def test_remove_top_level_task_file(self):
        result = self.remove_todo_tool_file.remove_todo("1")
        self.assertIn("Todo item removed", result)
        self.assertEqual(len(self.remove_todo_tool_file.todo_list), 1)
        self.assertNotIn({"id": "1", "task": "Buy groceries"}, self.remove_todo_tool_file.todo_list)

    def test_remove_subtask_file(self):
        result = self.remove_todo_tool_file.remove_todo("2.1")
        self.assertIn("Todo item removed", result)
        self.assertEqual(len(self.remove_todo_tool_file.todo_list[0]["subtasks"]), 1)
        self.assertNotIn({"id": "2.1", "task": "Subtask 2.1"}, self.remove_todo_tool_file.todo_list[0]["subtasks"])

    def test_remove_task_with_subtasks_file(self):
        result = self.remove_todo_tool_file.remove_todo("2")
        self.assertIn("Todo item removed", result)
        self.assertEqual(len(self.remove_todo_tool_file.todo_list), 1)
        self.assertNotIn({"id": "2", "task": "Do laundry"}, self.remove_todo_tool_file.todo_list)

    def test_remove_nonexistent_task_file(self):
        result = self.remove_todo_tool_file.remove_todo("99")
        self.assertIn("Todo item not found", result)
        self.assertEqual(len(self.remove_todo_tool_file.todo_list), 2)

    def test_remove_all_tasks_file(self):
        self.remove_todo_tool_file.remove_todo("1")
        self.remove_todo_tool_file.remove_todo("2")
        self.assertEqual(len(self.remove_todo_tool_file.todo_list), 0)

    def test_file_persistence(self):
        self.remove_todo_tool_file.remove_todo("1")
        new_tool = RemoveTodoTool(self.filename)
        self.assertEqual(len(new_tool.todo_list), 1)
        self.assertNotIn({"id": "1", "task": "Buy groceries"}, new_tool.todo_list)

    def test_empty_file(self):
        with open(self.filename, 'w') as f:
            json.dump([], f)
        empty_tool = RemoveTodoTool(self.filename)
        result = empty_tool.remove_todo("1")
        self.assertIn("Todo item not found", result)

    def test_malformed_json(self):
        with open(self.filename, 'w') as f:
            f.write("This is not valid JSON")
        with self.assertRaises(json.JSONDecodeError):
            RemoveTodoTool(self.filename)

    def test_schema(self):
        schema = RemoveTodoTool.schema()
        self.assertEqual(schema["name"], "remove_todo")
        self.assertTrue(schema["strict"])
        self.assertIn("task", schema["parameters"]["properties"])


if __name__ == '__main__':
    unittest.main()
