import json
from datetime import datetime

class EditTodoTool:
    """
    Provides a tool for editing todo items, including adding subtasks.
    """
    
    def __init__(self, filename="todo_list.json"):
        self.filename = filename
        self.todo_list = self.load_todo_list()

    @staticmethod
    def schema():
        return {
            "name": "edit_todo",
            "description": "Edit a todo item or add a subtask",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The ID of the task to edit (e.g., '19' or '19.b')"
                    },
                    "new_task": {
                        "type": "string",
                        "description": "The new task description or subtask to add"
                    },
                    "action": {
                        "type": "string",
                        "enum": ["edit", "add_subtask"],
                        "description": "Whether to edit the existing task or add a subtask"
                    }
                },
                "additionalProperties": False,
                "required": ["task_id", "new_task", "action"]
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

    def edit_todo(self, task_id, new_task, action):
        """Edits a todo item or adds a subtask."""
        task = self.find_task(task_id)
        if task is None:
            return f"Task with ID {task_id} not found."

        if action == "edit":
            task["task"] = new_task
            task["timestamp"] = datetime.now().isoformat()
        elif action == "add_subtask":
            if "subtasks" not in task:
                task["subtasks"] = []
            new_subtask_id = f"{task_id}.{chr(97 + len(task['subtasks']))}"
            task["subtasks"].append({
                "id": new_subtask_id,
                "task": new_task,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return f"Invalid action: {action}"
        
        self.save_todo_list()
        return f"Task updated: {json.dumps(task)}"

    def find_task(self, task_id):
        """Finds a task by its ID in the todo list."""
        parts = task_id.split('.')
        current_list = self.todo_list
        for part in parts:
            task_found = False
            for item in current_list:
                if item.get("id") == part:
                    if part == parts[-1]:
                        return item
                    current_list = item.get("subtasks", [])
                    task_found = True
                    break
            if not task_found:
                return None
        return None
