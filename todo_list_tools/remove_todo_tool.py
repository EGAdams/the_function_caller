import json

class RemoveTodoTool:
    """
    Provides a tool for removing a todo item from a list and updating the file.
    """
    
    def __init__(self, filename="todo_list.json"):
        self.filename = filename
        self.todo_list = self.load_todo_list()

    def schema():
        return {
            "name": "remove_todo",
            "description": "Remove a todo item from the list and update the file",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The task to remove from the todo list."
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

    def remove_todo(self, task):
        """Removes a todo item from the list and updates the file."""
        for item in self.todo_list:
            if item["task"] == task:
                self.todo_list.remove(item)
                self.save_todo_list()
                return f"Todo item removed and file updated: {json.dumps(item)}"
        return f"Todo item not found: {task}"