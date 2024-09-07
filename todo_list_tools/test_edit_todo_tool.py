import unittest
import json
import os
from datetime import datetime
from edit_todo_tool import EditTodoTool

class TestEditTodoTool(unittest.TestCase):
    def setUp(self):
        self.test_filename = "test_todo_list.json"
        self.edit_tool = EditTodoTool(self.test_filename)
        
        # Sample todo list for testing
        self.sample_todo_list = [
            {
                "id": "1",
                "task": "Sample task 1",
                "timestamp": datetime.now().isoformat()
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
        
        with open(self.test_filename, 'w') as f:
            json.dump(self.sample_todo_list, f)

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_load_todo_list(self):
        todo_list = self.edit_tool.load_todo_list()
        self.assertEqual(len(todo_list), 2)
        self.assertEqual(todo_list[0]["task"], "Sample task 1")

    def test_save_todo_list(self):
        new_task = {"id": "3", "task": "New task", "timestamp": datetime.now().isoformat()}
        self.edit_tool.todo_list.append(new_task)
        self.edit_tool.save_todo_list()
        
        with open(self.test_filename, 'r') as f:
            saved_list = json.load(f)
        
        self.assertEqual(len(saved_list), 3)
        self.assertEqual(saved_list[2]["task"], "New task")

    def test_find_task_top_level(self):
        task = self.edit_tool.find_task("1")
        self.assertIsNotNone(task)
        self.assertEqual(task["task"], "Sample task 1")

    def test_find_task_subtask(self):
        task = self.edit_tool.find_task("2.a")
        self.assertIsNotNone(task)
        self.assertEqual(task["task"], "Subtask 2.a")

    def test_find_task_nonexistent(self):
        task = self.edit_tool.find_task("999")
        self.assertIsNone(task)

    def test_edit_todo_existing_task(self):
        result = self.edit_tool.edit_todo("1", "Updated task 1", "edit")
        self.assertIn("Task updated", result)
        updated_task = self.edit_tool.find_task("1")
        self.assertEqual(updated_task["task"], "Updated task 1")

    def test_edit_todo_add_subtask(self):
        result = self.edit_tool.edit_todo("2", "New subtask", "add_subtask")
        self.assertIn("Task updated", result)
        updated_task = self.edit_tool.find_task("2")
        self.assertEqual(len(updated_task["subtasks"]), 2)
        self.assertEqual(updated_task["subtasks"][1]["task"], "New subtask")

    def test_edit_todo_nonexistent_task(self):
        result = self.edit_tool.edit_todo("999", "This should fail", "edit")
        self.assertEqual(result, "Task with ID 999 not found.")

    def test_edit_todo_invalid_action(self):
        result = self.edit_tool.edit_todo("1", "This should fail", "invalid_action")
        self.assertEqual(result, "Invalid action: invalid_action")

    def test_schema(self):
        schema = EditTodoTool.schema()
        self.assertIsInstance(schema, dict)
        self.assertEqual(schema["name"], "edit_todo")
        self.assertTrue(schema["strict"])
        self.assertIn("task_id", schema["parameters"]["properties"])
        self.assertIn("new_task", schema["parameters"]["properties"])
        self.assertIn("action", schema["parameters"]["properties"])

if __name__ == '__main__':
    unittest.main()
