import unittest
import json
import os
from remove_todo_tool.remove_todo_tool import RemoveTodoTool
from storage_handler.storage_handler import StorageHandler

class TestRemoveTodoTool(unittest.TestCase):
    def setUp(self):
        self.filename = "test_file.json"
        self.storage_handler = StorageHandler(self.filename)
        self.initial_todo_list = [
            {"id": "1", "task": "Buy groceries", "timestamp": "2024-09-08T12:00:00Z"},
            {"id": "2", "task": "Do laundry", "timestamp": "2024-09-08T13:00:00Z", "subtasks": [
                {"id": "2.1", "task": "Subtask 2.1"},
                {"id": "2.2", "task": "Subtask 2.2"}
            ]}
        ]
        with open(self.filename, 'w') as f:
            json.dump(self.initial_todo_list, f)
        self.remove_todo_tool = RemoveTodoTool(self.filename, self.storage_handler)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_remove_top_level_task(self):
        result = self.remove_todo_tool.remove_todo("1")
        self.assertIn("Todo item removed", result)
        self.assertEqual(len(self.remove_todo_tool.todo_list), 1)
        self.assertNotIn({"id": "1", "task": "Buy groceries"}, self.remove_todo_tool.todo_list)

    def test_remove_subtask(self):
        result = self.remove_todo_tool.remove_todo("2.1")
        self.assertIn("Todo item removed", result)
        self.assertEqual(len(self.remove_todo_tool.todo_list[1]["subtasks"]), 1)
        self.assertNotIn({"id": "2.1", "task": "Subtask 2.1"}, self.remove_todo_tool.todo_list[1]["subtasks"])

    def test_remove_task_with_subtasks(self):
        result = self.remove_todo_tool.remove_todo("2")
        self.assertIn("Todo item removed", result)
        self.assertEqual(len(self.remove_todo_tool.todo_list), 1)
        self.assertNotIn({"id": "2", "task": "Do laundry"}, self.remove_todo_tool.todo_list)

    def test_remove_nonexistent_task(self):
        result = self.remove_todo_tool.remove_todo("99")
        self.assertIn("Todo item not found", result)
        self.assertEqual(len(self.remove_todo_tool.todo_list), 2)

    def test_remove_all_tasks(self):
        self.remove_todo_tool.remove_todo("1")
        self.remove_todo_tool.remove_todo("2")
        self.assertEqual(len(self.remove_todo_tool.todo_list), 0)

    def test_file_persistence(self):
        self.remove_todo_tool.remove_todo("1")
        new_tool = RemoveTodoTool(self.filename, self.storage_handler)
        self.assertEqual(len(new_tool.todo_list), 1)
        self.assertNotIn({"id": "1", "task": "Buy groceries"}, new_tool.todo_list)

    def test_empty_file(self):
        with open(self.filename, 'w') as f:
            json.dump([], f)
        empty_tool = RemoveTodoTool(self.filename, self.storage_handler)
        result = empty_tool.remove_todo("1")
        self.assertIn("Todo item not found", result)

    def test_schema(self):
        schema = RemoveTodoTool.schema()
        self.assertEqual(schema["name"], "remove_todo")
        self.assertTrue(schema["strict"])
        self.assertIn("task_id", schema["parameters"]["properties"])

if __name__ == '__main__':
    unittest.main()