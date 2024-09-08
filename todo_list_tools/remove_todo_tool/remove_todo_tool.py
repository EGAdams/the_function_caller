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

    def remove_todo(self, task_id):
        """Removes a todo item from the list and updates the file."""
        def remove_recursive(task_list, target_id):
            for index, item in enumerate(task_list):
                if item["id"] == target_id:
                    removed_item = task_list.pop(index)
                    return removed_item
                if "subtasks" in item:
                    result = remove_recursive(item["subtasks"], target_id)
                    if result:
                        return result
            return None

        removed_item = remove_recursive(self.todo_list, task_id)
        if removed_item:
            self.save_todo_list()
            return f"Todo item removed and file updated: {json.dumps(removed_item)}"
        return f"Todo item not found: {task_id}"
