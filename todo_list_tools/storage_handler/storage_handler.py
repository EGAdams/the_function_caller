import json

class StorageHandler:
    """Handles the loading and saving of the todo list to/from a file."""

    def __init__(self, filename="todo_list.json"):
        self.filename = filename

    def load(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save(self, todo_list):
        with open(self.filename, 'w') as file:
            json.dump(todo_list, file, indent=2)
