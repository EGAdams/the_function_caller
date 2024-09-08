import unittest
import json
import tempfile
import os
from todo_list_tools.remove_todo_tool.remove_todo_tool import RemoveTodoTool

class TestRemoveTodoTool(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, "test_todo_list.json")
        self.initial_todo_list = [
            {"id": "1", "task": "Task 1"},
            {"id": "2", "task": "Task 2", "subtasks": [
                {"id": "2.1", "task": "Subtask 2.1"},
                {"id": "2.2", "task": "Subtask 2.2"}
            ]},
            {"id": "3", "task": "Task 3"}
        ]
        with open(self.filename, 'w') as f:
            json.dump(self.initial_todo_list, f)
        
        self.remove_todo_tool = RemoveTodoTool(self.filename)

    def tearDown(self):
        os.remove(self.filename)
        os.rmdir(self.temp_dir)

    def test_remove_top_level_task(self):
        result = self.remove_todo_tool.remove_todo("1")
        self.assertIn("Todo item removed", result)
        self.assertEqual(len(self.remove_todo_tool.todo_list), 2)
        self.assertNotIn({"id": "1", "task": "Task 1"}, self.remove_todo_tool.todo_list)

    def test_remove_subtask(self):
        result = self.remove_todo_tool.remove_todo("2.1")
        self.assertIn("Todo item removed", result)
        self.assertEqual(len(self.remove_todo_tool.todo_list[1]["subtasks"]), 1)
        self.assertNotIn({"id": "2.1", "task": "Subtask 2.1"}, self.remove_todo_tool.todo_list[1]["subtasks"])

    def test_remove_task_with_subtasks(self):
        result = self.remove_todo_tool.remove_todo("2")
        self.assertIn("Todo item removed", result)
        self.assertEqual(len(self.remove_todo_tool.todo_list), 2)
        self.assertNotIn({"id": "2", "task": "Task 2"}, self.remove_todo_tool.todo_list)

    def test_remove_nonexistent_task(self):
        result = self.remove_todo_tool.remove_todo("4")
        self.assertIn("Todo item not found", result)
        self.assertEqual(len(self.remove_todo_tool.todo_list), 3)

    def test_remove_all_tasks(self):
        self.remove_todo_tool.remove_todo("1")
        self.remove_todo_tool.remove_todo("2")
        self.remove_todo_tool.remove_todo("3")
        self.assertEqual(len(self.remove_todo_tool.todo_list), 0)

    def test_file_persistence(self):
        self.remove_todo_tool.remove_todo("1")
        new_tool = RemoveTodoTool(self.filename)
        self.assertEqual(len(new_tool.todo_list), 2)
        self.assertNotIn({"id": "1", "task": "Task 1"}, new_tool.todo_list)

    def test_schema(self):
        schema = RemoveTodoTool.schema()
        self.assertEqual(schema["name"], "remove_todo")
        self.assertTrue(schema["strict"])
        self.assertIn("task", schema["parameters"]["properties"])

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

if __name__ == '__main__':
    unittest.main()