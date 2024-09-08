import json
from datetime import datetime

class AddTodoTool:
    """
    Provides a tool for adding a new todo item to a list and saving it.
    """
    
    def __init__(self, storage_handler):
        self.storage_handler = storage_handler
        self.todo_list = self.storage_handler.load()

    @staticmethod
    def schema():
        return {
            "name": "add_todo",
            "description": "Add a new todo item to the list",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The task to add to the todo list."
                    }
                },
                "additionalProperties": False,
                "required": ["task"]
            }
        }

    def add_todo(self, task):
        timestamp = datetime.now().isoformat()
        new_id = str(len(self.todo_list) + 1)
        todo_item = {"id": new_id, "timestamp": timestamp, "task": task}
        self.todo_list.append(todo_item)
        self.storage_handler.save(self.todo_list)
        return f"Todo item added and saved: {json.dumps(todo_item)}"
