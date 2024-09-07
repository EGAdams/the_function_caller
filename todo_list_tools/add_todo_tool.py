import json
from datetime import datetime

class AddTodoTool:
    """
    Provides a tool for adding a new todo item to a list and saving it to a file.
    """
    
    def __init__(self, filename="todo_list.json"):
        self.filename = filename
        self.todo_list = self.load_todo_list()

    def schema():
        return {
            "name": "add_todo",
            "description": "Add a new todo item to the list and save it to a file",
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

    def load_todo_list(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_todo_list(self):
        with open(self.filename, 'w') as file:
            json.dump(self.todo_list, file, indent=2)

    def add_todo(self, task):
        timestamp = datetime.now().isoformat()
        new_id = str(len(self.todo_list) + 1)
        todo_item = {"id": new_id, "timestamp": timestamp, "task": task}
        self.todo_list.append(todo_item)
        self.save_todo_list()
        return f"Todo item added and saved: {json.dumps(todo_item)}"
