import unittest
import json
import os
from datetime import datetime
from edit_todo_tool import EditTodoTool

class TestEditTodoTool(unittest.TestCase):

    def setUp(self):
        self.test_filename = "test_todo_list.json"
        self.edit_tool = EditTodoTool(self.test_filename)
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

    # Basic test for loading todo list
    def test_load_todo_list_empty(self):
        # Ensure that when the file does not exist, an empty list is returned
        os.remove(self.test_filename)
        todo_list = self.edit_tool.load_todo_list()
        self.assertEqual(todo_list, [])

    def test_load_todo_list_with_data(self):
        # Ensure that data loads correctly from the sample todo list
        todo_list = self.edit_tool.load_todo_list()
        self.assertEqual(len(todo_list), 2)
        self.assertEqual(todo_list[0]["task"], "Sample task 1")

    # Basic test for saving the todo list
    def test_save_todo_list(self):
        new_task = {"id": "3", "task": "New task", "timestamp": datetime.now().isoformat()}
        self.edit_tool.todo_list.append(new_task)
        self.edit_tool.save_todo_list()

        with open(self.test_filename, 'r') as f:
            saved_list = json.load(f)

        self.assertEqual(len(saved_list), 3)
        self.assertEqual(saved_list[2]["task"], "New task")

    # Basic tests for finding tasks
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

    # Basic test for editing an existing task
    def test_edit_existing_task(self):
        result = self.edit_tool.edit_todo("1", "Updated task 1", "edit")
        updated_task = self.edit_tool.find_task("1")
        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task["task"], "Updated task 1")
        self.assertIn("Task updated", result)

    # Basic test for adding a subtask
    def test_add_subtask(self):
        result = self.edit_tool.edit_todo("2", "New subtask", "add_subtask")
        updated_task = self.edit_tool.find_task("2")
        self.assertIsNotNone(updated_task)
        self.assertEqual(len(updated_task["subtasks"]), 2)
        self.assertEqual(updated_task["subtasks"][1]["task"], "New subtask")
        self.assertIn("Task updated", result)

    # Basic test for invalid actions
    def test_invalid_action(self):
        result = self.edit_tool.edit_todo("1", "Invalid action", "invalid_action")
        self.assertEqual(result, "Invalid action: invalid_action")

    # Schema validation test
    def test_schema(self):
        schema = self.edit_tool.schema()
        self.assertIsInstance(schema, dict)
        self.assertEqual(schema["name"], "edit_todo")
        self.assertTrue(schema["strict"])
        self.assertIn("task_id", schema["parameters"]["properties"])
        self.assertIn("new_task", schema["parameters"]["properties"])
        self.assertIn("action", schema["parameters"]["properties"])

if __name__ == '__main__':
    unittest.main()
