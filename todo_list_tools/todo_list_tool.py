import json
from datetime import datetime

class TodoListTool:
    """
    Provides a tool for managing a todo list.
    
    The `TodoListTool` class exposes methods to add and remove todo items.
    Each todo item is a JSON object with a timestamp and a task.
    """
    
    def __init__(self):
        self.todo_list = []

    def schema():
        return {
            "name": "todo_list",
            "description": "Manage a todo list with add and remove operations",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["add", "remove"],
                        "description": "The action to perform on the todo list."
                    },
                    "task": {
                        "type": "string",
                        "description": "The task to add or remove from the todo list."
                    }
                },
                "additionalProperties": False,
                "required": ["action", "task"]
            }
        }

    def add_todo(self, task):
        """Adds a new todo item to the list.
        
        Args:
            task (str): The task to add to the todo list.
        
        Returns:
            str: A message indicating the result of the operation.
        """
        timestamp = datetime.now().isoformat()
        todo_item = {"timestamp": timestamp, "task": task}
        self.todo_list.append(todo_item)
        return f"Todo item added: {json.dumps(todo_item)}"

    def remove_todo(self, task):
        """Removes a todo item from the list.
        
        Args:
            task (str): The task to remove from the todo list.
        
        Returns:
            str: A message indicating the result of the operation.
        """
        for item in self.todo_list:
            if item["task"] == task:
                self.todo_list.remove(item)
                return f"Todo item removed: {json.dumps(item)}"
        return f"Todo item not found: {task}"

    def manage_todo(self, action, task):
        """Manages the todo list based on the given action.
        
        Args:
            action (str): The action to perform (add or remove).
            task (str): The task to add or remove.
        
        Returns:
            str: A message indicating the result of the operation.
        """
        if action == "add":
            return self.add_todo(task)
        elif action == "remove":
            return self.remove_todo(task)
        else:
            return "Invalid action. Use 'add' or 'remove'."
