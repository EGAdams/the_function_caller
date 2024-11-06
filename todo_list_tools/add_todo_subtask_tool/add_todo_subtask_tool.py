import os
import sys

sys.path.append( '/home/adamsl/the_function_caller/todo_list_tools' )

from task import Task
from task_finder import TaskFinder
import json
from datetime import datetime

class AddTodoSubtaskTool:
    """
    Provides a tool for adding a new todo item to a list and saving it.
    """
    
    def __init__(self, storage_handler):
        self.storage_handler = storage_handler
        todo_list_data = self.storage_handler.load()
        # Convert the list of dicts into a list of Task objects
        self.todo_list = [Task(task_dict) for task_dict in todo_list_data]

    @staticmethod
    def schema():
        return {
            "name": "add_todo_subtask",
            "description": "Add a new todo item to the list",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "object",
                        "description": "The task to add to the todo list. May contain subtasks which are also objects with the same properties",
                    },
                    "parent_id": {
                        "type": "string",
                        "description": "The ID of the parent task",
                    }
                },
                "additionalProperties": False,
                "required": ["task", "parent_id"]
            }
        }

    def get_all_task_ids(self):
        """Collect all task IDs from the todo list."""
        ids = []
        for task in self.todo_list:
            ids.extend(task.get_all_ids())
        return ids

    def add_todo_subtask(self, description: str, parent_id: str):
        # Validate input types
        if not isinstance(description, str) or not isinstance(parent_id, str):
            print("description is a " + str(type(description)))
            print("parent_id is a " + str(type(parent_id)))
            print("*** ERROR: add_todo_subtask only accepts string objects for description and parent_id ***")
            exit()

        # Generate a unique new ID
        existing_ids = self.get_all_task_ids()
        max_id = max([int(id) for id in existing_ids if id.isdigit()] + [0])
        new_id = str(max_id + 1)

        # Create a new Task object
        new_task = Task({
            "id": new_id,
            "parent_id": parent_id,
            "priority": 1,  # Default priority
            "born_on": datetime.now().isoformat(),
            "description": description,
            "subtasks": []
        })

        # Find the parent task
        parent_task = TaskFinder.find_task(self.todo_list, parent_id)

        if not parent_task:
            print(f"*** ERROR: Parent task with ID {parent_id} not found ***")
            exit()

        # Add the new task to the parent task's subtasks
        parent_task.add_subtask(new_task)

        # Save the updated todo list
        todo_list_data = [task.to_dict() for task in self.todo_list]
        self.storage_handler.save(todo_list_data)
        
        return f"Task added successfully: [ID: {new_id}] {description}"
