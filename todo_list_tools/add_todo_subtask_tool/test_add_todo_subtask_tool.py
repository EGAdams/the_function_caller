import unittest
import sys
import os
import json
from datetime import datetime


sys.path.append('/home/adamsl/the_function_caller/')
from todo_list_tools.add_todo_subtask_tool.add_todo_subtask_tool import AddTodoSubtaskTool
from todo_list_tools.storage_handler.storage_handler import StorageHandler
from todo_list_tools.task.task import Task
from todo_list_tools.task_finder.task_finder import TaskFinder

class TestAddTodoSubtaskTool(unittest.TestCase):
    
    def setUp(self):
        """Set up a test environment with a sample todo list file."""
        self.test_filename = "test_todo_list.json"
        self.sample_todo_list = [
            {
                "id": "1",
                "parent_id": None,
                "priority": 1,
                "born_on": "2024-01-01T00:00:00",
                "description": "Main Task",
                "status": "active",
                "subtasks": []
            },
            {
                "id": "2",
                "parent_id": None,
                "priority": 2,
                "born_on": "2024-01-02T00:00:00",
                "description": "Another Main Task",
                "status": "active",
                "subtasks": []
            }
        ]
        with open(self.test_filename, "w") as file:
            json.dump(self.sample_todo_list, file, indent=2)

        self.storage_handler = StorageHandler(self.test_filename)
        self.add_tool = AddTodoSubtaskTool(self.storage_handler)

    def tearDown(self):
        """Clean up the test environment."""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_add_valid_subtask(self):
        """Test adding a valid subtask to an existing task."""
        description = "Subtask for Main Task"
        parent_id = "1"
        result = self.add_tool.add_todo_subtask(description, parent_id)

        self.assertIn("Task added successfully", result)

        todo_list = self.storage_handler.load()
        parent_task = Task(todo_list[0])  # The first task
        
        self.assertTrue(parent_task.has_subtasks())
        subtask = parent_task.get_subtasks()[0]

        self.assertEqual(subtask.get_description(), description)
        self.assertEqual(subtask.parent_id, parent_id)

    def test_add_subtask_to_nonexistent_parent(self):
        """Test adding a subtask to a non-existent parent task."""
        description = "Orphan Subtask"
        parent_id = "999"  # Non-existent ID

        with self.assertRaises(SystemExit):
            self.add_tool.add_todo_subtask(description, parent_id)

    def test_add_subtask_with_invalid_description_type(self):
        """Test adding a subtask with an invalid description type."""
        description = 123  # Invalid type
        parent_id = "1"

        with self.assertRaises(SystemExit):
            self.add_tool.add_todo_subtask(description, parent_id)

    def test_add_subtask_with_invalid_parent_id_type(self):
        """Test adding a subtask with an invalid parent ID type."""
        description = "Subtask with Invalid Parent ID"
        parent_id = 123  # Invalid type

        with self.assertRaises(SystemExit):
            self.add_tool.add_todo_subtask(description, parent_id)

    def test_task_id_generation(self):
        """Test that the tool generates unique task IDs."""
        description = "Unique ID Subtask"
        parent_id = "1"
        self.add_tool.add_todo_subtask(description, parent_id)

        todo_list = self.storage_handler.load()
        parent_task = Task(todo_list[0])
        subtask_ids = [subtask.get_id() for subtask in parent_task.get_subtasks()]

        # Ensure the new task ID is unique and greater than existing IDs
        existing_ids = [task["id"] for task in self.sample_todo_list]
        new_id = subtask_ids[0]
        
        self.assertNotIn(new_id, existing_ids)

    def test_storage_persistence(self):
        """Test that the storage file is correctly updated after adding a subtask."""
        description = "Persistent Subtask"
        parent_id = "1"
        self.add_tool.add_todo_subtask(description, parent_id)

        with open(self.test_filename, "r") as file:
            data = json.load(file)

        parent_task = Task(data[0])
        subtasks = parent_task.get_subtasks()
        self.assertEqual(len(subtasks), 1)
        self.assertEqual(subtasks[0].get_description(), description)
    def test_add_subtask_over_10_levels_deep(self):
        """Test adding a subtask nested over 10 levels deep."""
        # Start with a single root task
        root_description = "Level 0"
        root_id = "1"
        root_task = Task({
            "id": root_id,
            "parent_id": None,
            "priority": 1,
            "born_on": "2024-01-01T00:00:00",
            "description": root_description,
            "status": "active",
            "subtasks": []
        })
        self.todo_list = [root_task.to_dict()]
        self.storage_handler.save(self.todo_list)
        self.add_tool = AddTodoSubtaskTool(self.storage_handler)
        
        current_parent_id = root_id
        depth = 11  # Adding 11 levels deep

        # Add subtasks level by level
        for level in range(1, depth + 1):
            description = f"Level {level}"
            result = self.add_tool.add_todo_subtask(description, current_parent_id)
            self.assertIn("Task added successfully", result)
            
            # Reload the todo list to get the updated structure
            todo_list = self.storage_handler.load()
            # print todo list
            print( todo_list )
            root_task = Task( todo_list[ 0 ])
            current_task = root_task.find_task_by_id( current_parent_id )
            self.assertIsNotNone(current_task, f"Parent task with ID {current_parent_id} should exist")
            self.assertTrue(current_task.has_subtasks(), f"Parent task at level {level-1} should have subtasks")
            
            # Get the newly added subtask
            new_subtask = current_task.get_subtasks()[-1]
            self.assertEqual(new_subtask.get_description(), description, f"Subtask at level {level} should have correct description")
            self.assertEqual(new_subtask.parent_id, current_parent_id, f"Subtask at level {level} should have correct parent_id")
            
            # Set the new parent_id for the next level
            current_parent_id = new_subtask.get_id()

        # Verify the entire hierarchy
        todo_list = self.storage_handler.load()
        root_task = Task(todo_list[0])
        current_task = root_task
        for level in range(1, depth + 1):
            self.assertTrue(current_task.has_subtasks(), f"Task at level {level-1} should have subtasks")
            current_task = current_task.get_subtasks()[-1]
            self.assertEqual(current_task.get_description(), f"Level {level}", f"Task at level {level} should have correct description")
            self.assertEqual(current_task.parent_id, root_id if level == 1 else str(level), f"Task at level {level} should have correct parent_id")

    def test_add_subtask_with_empty_description(self):
        """Test adding a subtask with an empty description."""
        description = ""
        parent_id = "1"
        
        result = self.add_tool.add_todo_subtask(description, parent_id)
        self.assertIn("Task added successfully", result)
        
        todo_list = self.storage_handler.load()
        parent_task = Task(todo_list[0])
        self.assertTrue(parent_task.has_subtasks(), "Parent task should have subtasks")
        subtask = parent_task.get_subtasks()[-1]
        self.assertEqual(subtask.get_description(), description, "Subtask should have an empty description")

    def test_add_subtask_with_special_characters_in_description(self):
        """Test adding a subtask with special characters in the description."""
        description = "Subtask @#*&^%$#@!()_+"
        parent_id = "1"
        
        result = self.add_tool.add_todo_subtask(description, parent_id)
        self.assertIn("Task added successfully", result)
        
        todo_list = self.storage_handler.load()
        parent_task = Task(todo_list[0])
        self.assertTrue(parent_task.has_subtasks(), "Parent task should have subtasks")
        subtask = parent_task.get_subtasks()[-1]
        self.assertEqual(subtask.get_description(), description, "Subtask should correctly store special characters in description")

    def test_add_multiple_subtasks_sequentially(self):
        """Test adding multiple subtasks sequentially to the same parent."""
        parent_id = "1"
        descriptions = [f"Subtask {i}" for i in range(1, 6)]  # Adding 5 subtasks

        for desc in descriptions:
            result = self.add_tool.add_todo_subtask(desc, parent_id)
            self.assertIn("Task added successfully", result)
        
        todo_list = self.storage_handler.load()
        parent_task = Task(todo_list[0])
        self.assertTrue(parent_task.has_subtasks(), "Parent task should have subtasks")
        self.assertEqual(len(parent_task.get_subtasks()), 5, "Parent task should have 5 subtasks")
        
        for i, subtask in enumerate(parent_task.get_subtasks(), start=1):
            self.assertEqual(subtask.get_description(), f"Subtask {i}", f"Subtask {i} should have correct description")
            self.assertEqual(subtask.parent_id, parent_id, f"Subtask {i} should have correct parent_id")

    def test_add_subtask_with_large_description(self):
        """Test adding a subtask with a very large description."""
        description = "A" * 1000  # 1000 characters
        parent_id = "1"
        
        result = self.add_tool.add_todo_subtask(description, parent_id)
        self.assertIn("Task added successfully", result)
        
        todo_list = self.storage_handler.load()
        parent_task = Task(todo_list[0])
        self.assertTrue(parent_task.has_subtasks(), "Parent task should have subtasks")
        subtask = parent_task.get_subtasks()[-1]
        self.assertEqual(subtask.get_description(), description, "Subtask should correctly store a large description")

    def test_add_subtask_with_duplicate_descriptions(self):
        """Test adding multiple subtasks with the same description."""
        description = "Duplicate Description"
        parent_id = "1"
        number_of_duplicates = 3
        
        for _ in range(number_of_duplicates):
            result = self.add_tool.add_todo_subtask(description, parent_id)
            self.assertIn("Task added successfully", result)
        
        todo_list = self.storage_handler.load()
        parent_task = Task(todo_list[0])
        self.assertEqual(len(parent_task.get_subtasks()), number_of_duplicates, f"Parent task should have {number_of_duplicates} subtasks")
        
        for subtask in parent_task.get_subtasks():
            self.assertEqual(subtask.get_description(), description, "All subtasks should have the duplicate description")

    def test_add_subtask_to_deeply_nested_parent(self):
        """Test adding a subtask to a deeply nested parent task."""
        # Create a nested structure 5 levels deep
        current_parent_id = "1"
        depth = 5
        for level in range(1, depth + 1):
            description = f"Level {level}"
            self.add_tool.add_todo_subtask(description, current_parent_id)
            todo_list = self.storage_handler.load()
            root_task = Task(todo_list[0])
            current_task = root_task.find_task_by_id( current_parent_id )
            self.assertIsNotNone(current_task, f"Parent task at level {level-1} should exist")
            self.assertTrue(current_task.has_subtasks(), f"Parent task at level {level-1} should have subtasks")
            new_subtask = current_task.get_subtasks()[-1]
            current_parent_id = new_subtask.get_id()
        
        # Now add a new subtask to the deepest level
        new_description = "Deep Subtask"
        result = self.add_tool.add_todo_subtask(new_description, current_parent_id)
        self.assertIn("Task added successfully", result)
        
        # Verify the new subtask is correctly added
        todo_list = self.storage_handler.load()
        root_task = Task( todo_list[ 0 ])
        deep_parent = root_task.find_task_by_id( current_parent_id )
        self.assertIsNotNone( deep_parent, "Deeply nested parent task should exist" )
        self.assertTrue(deep_parent.has_subtasks(), "Deeply nested parent task should have subtasks")
        new_subtask = deep_parent.get_subtasks()[-1]
        self.assertEqual(new_subtask.get_description(), new_description, "Deep subtask should have correct description")
        self.assertEqual(new_subtask.parent_id, current_parent_id, "Deep subtask should have correct parent_id")


if __name__ == "__main__":
    unittest.main()
